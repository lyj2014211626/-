
# coding: utf-8

import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn import model_selection
from sklearn.svm import SVC
from scipy.stats import chisquare
from scipy.stats import chi2_contingency
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_validate
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt


# In[130]:


def get_df(fileName):
    df = pd.read_excel(fileName).replace(2, 0).drop(columns = ['ID'])
    return df
def feature_select(df):
    fea_dict = {}
    for col in df.columns[0:-1]:
        a,p,c,b = chi2_contingency(pd.crosstab(df[col],df['Event']))
        if(p < 0.5):
            fea_dict[col] = 1-p
    
    return dict(sorted(fea_dict.items(), key=lambda x : x[1], reverse=True))


# In[168]:


def return_acc(estimator, x, y,thresholds=0.5):
    yPred = (estimator.predict_proba(x)[:,1] >= thresholds).astype(int)
    return accuracy_score(y, yPred)
def return_pre(estimator, x, y,thresholds=0.5):
    yPred = (estimator.predict_proba(x)[:,1] >= thresholds).astype(int)
    return precision_score(y, yPred, pos_label = 1)
def return_rec(estimator, x, y,thresholds=0.5):
    yPred = (estimator.predict_proba(x)[:,1] >= thresholds).astype(int)
    return recall_score(y, yPred, pos_label = 1)
def return_f1_score(estimator, x, y,thresholds=0.5):
    yPred = (estimator.predict_proba(x)[:,1] >= thresholds).astype(int)
    return f1_score(y, yPred, pos_label = 1)
def return_auc(estimator, x, y):
    y_score = estimator.predict_proba(x)[:,1]
    false_positive_rate,true_positive_rate,thresholds=roc_curve(y, y_score,pos_label = 1)
    roc_auc = auc(false_positive_rate, true_positive_rate)
    return roc_auc
def optimal_thresholds(estimator, x, y):
    y_score = estimator.predict_proba(x)[:,1]
    fpr,tpr,thre = roc_curve(y, y_score,pos_label=1)
    opti_ind = np.argmax(tpr-fpr)
    return thre[opti_ind]
def plot_roc(labels, predict_prob):
    false_positive_rate,true_positive_rate,thresholds=roc_curve(labels, predict_prob,pos_label = 1)
    roc_auc=auc(false_positive_rate, true_positive_rate)
    plt.title('ROC')
    plt.plot(false_positive_rate, true_positive_rate,'g',label='AUC = %0.4f'% roc_auc,LineWidth = 3)
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--',LineWidth = 3)
    plt.ylabel('TPR')
    plt.xlabel('FPR')
    plt.show()
def optimal_para():
    parameters = [
        {
            'C': [1, 3, 5, 7, 9, 11],
            'gamma': [0.00001, 0.0001, 0.001, 0.1, 1],
            'kernel': ['rbf']
        },
        {
            'C': [1, 3, 5, 7, 9, 11],
            'kernel': ['linear']
        }
    ]
    clf = GridSearchCV(SVM, parameters, cv=4, n_jobs=8, scoring='roc_auc')
    clf.fit(X_train, Y_train)
    return clf.best_params_
def svc_clf(seed = 42):
    df = get_df('data/fchd_20190404_16000_0608_all_final.xlsx')
    feature = feature_select(df)
    x = df[list(feature.keys())].values
    y = df.values[:,-1]
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state = seed)
    SVM = SVC(probability=True,class_weight='balanced',random_state=seed, C=1,kernel='rbf',gamma=0.1)
    SVM.fit(x_train, y_train)
    thresholds = optimal_thresholds(SVM, x_test, y_test)
    return SVM, thresholds, feature
def svm(df):
    SVM, thresholds = svc_clf()
    x = df[list(feature.keys())].values
    res = (SVM.predict_proba(x)[:,1]>=thresholds).astype(int)
    df.append(pd.DataFrame(res, columns=['res']), ignore_index=True)
    return df

