# TODO: evaluate.calc_all函数的参数
from sklearn.svm import SVC
import time
import numpy as np

import read_data
import evaluate
import tools
from get_hyper_paras import get_section
from config import read_config


def svm(X=None,y=None,X_test=None,y_test=None,i_time=10):
    '''
    函数说明：svm算法
    参数说明：
        i_time：生成模型取平均表现的个数
        X,y,X_test,y_test如果传值的话，会运行的快一些
    '''
    if X==None or y==None or X_test==None or y_test==None:
        one_hot_key = read_config['svm']['one_hot_key']
        standard_scaler = True
        X,y = read_data.get_train_data(one_hot_key=one_hot_key,standard_scaler=standard_scaler)
        X_test,y_test = read_data.get_test_data(one_hot_key=one_hot_key,standard_scaler=standard_scaler)
        '''
        del_index = np.append(np.where(y==2),np.where(y==3))
        X = np.delete(X,del_index,axis=0)
        y = np.delete(y,del_index,axis=0)

        del_index_test = np.append(np.where(y_test==2),np.where(y_test==3))
        X_test = np.delete(X_test,del_index_test,axis=0)
        y_test = np.delete(y_test,del_index_test,axis=0)
        '''
        X1=np.copy(X)
        y1=np.copy(y)
        X_test1=np.copy(X_test)
        y_test1=np.copy(y_test)

        y[y==2] = 1
        y[y==3] = 1
        y_test[y_test==2] = 1
        y_test[y_test==3] = 1
    hyper_paras = get_section('svm')

    for i in np.linspace(3, 13,250):
        #print(type(hyper_paras['kernel']),type(hyper_paras['degree']),type(hyper_paras['gamma']),type(hyper_paras['shrinking']),type(hyper_paras['c']))
        # 这里重点：使用类别平衡算法


        #svm_clf = SVC(kernel=hyper_paras['kernel'],class_weight='balanced')
        svm_clf = SVC(class_weight={0:1,1:i})
        '''
        svm_clf = SVC(kernel=hyper_paras['kernel'],
                      degree=hyper_paras['degree'],
                      gamma=hyper_paras['gamma'],
                      shrinking=eval(hyper_paras['shrinking']),
                      C=hyper_paras['c'],
                      class_weight=hyper_paras['class_weight'])
        '''
        start = time.clock()
        svm_clf.fit(X,y)
        end = time.clock()
        train_time = end - start

        result = evaluate.calc_all(svm_clf,X_test,y_test,train_time)
        tools.dict_div(result,i_time)
        print(result)


if __name__ == '__main__':
    svm(i_time=1)
