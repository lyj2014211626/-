import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE, ADASYN
from collections import Counter
from imblearn.over_sampling import RandomOverSampler



file_path = os.path.dirname(os.path.abspath(__file__))
# 默认数据文件存放路径
train_data_path = os.path.join(file_path,'../../data/train_data.xlsx')
test_data_path = os.path.join(file_path,'../../data/test_data.xlsx')
all_data_path = os.path.join(file_path,'../../data/data.xlsx')

pd_train_data = pd.read_excel(train_data_path,sheet_name="Sheet1")
pd_test_data = pd.read_excel(test_data_path,sheet_name="Sheet1")
pd_all_data = pd.read_excel(all_data_path,sheet_name="Sheet1")

# 独热编码的编码器
sexual_encoder = LabelBinarizer().fit(pd_all_data.values[:,1])
academy_encoder = LabelBinarizer().fit(pd_all_data.values[:,2])
grade_encoder = LabelBinarizer().fit(pd_all_data.values[:,3].astype('|S4'))

def _smote(X,y):
    X_resampled_smote, y_resampled_smote = SMOTE().fit_sample(X, y)
    return X_resampled_smote,y_resampled_smote
    #print(sorted(Counter(y_resampled_smote).items()))

def _adasyn(X,y):
    X_resampled_smote, y_resampled_smote = ADASYN().fit_sample(X, y)
    return X_resampled_smote,y_resampled_smote
    #print(sorted(Counter(y_resampled_smote).items()))

def _random(X,y):
    ros = RandomOverSampler(random_state=0)
    X_resampled, y_resampled = ros.fit_sample(X, y)
    return X_resampled,y_resampled

def trans_data(input_data,one_hot_key=True,standard_scaler=False):
    '''
    函数说明：从指定位置读数据，只支持xlsx文件，因为保留的信息较多，可以对他进行独热编码
    参数说明：
        one_hot_key:是否采用独热编码
        standard_scaler:是否使用变量标准化
    函数返回值:
        以元组(features,target_label)的形式返回数据
    '''
    data = input_data.values
    data = data[:,1:]
    features = data[:,:-1]
    # print(features.shape)
    target_label = data[:,-1].astype(np.int32)

    if one_hot_key:
        sexual = features[:,0]
        academy = features[:,1]
        grade = features[:,2]
        encoded_sexual = sexual_encoder.transform(sexual)
        encoded_academy = academy_encoder.transform(academy)
        encoded_grade = grade_encoder.transform(grade.astype('|S4'))
        features = np.c_[features[:,3:],encoded_sexual,encoded_academy,encoded_grade]
        # print(features)
    else:
        features = np.c_[features[:,3:].astype(np.float32),features[:,:3]]

    if standard_scaler:
        scaler = StandardScaler()
        features = np.c_[scaler.fit_transform(features[:,:16].astype(np.float64)),features[:,16:]]

    return _smote(features,target_label)


def get_train_data(one_hot_key=True,standard_scaler=False):
    return trans_data(pd_train_data,one_hot_key=one_hot_key,standard_scaler=standard_scaler)

def get_test_data(one_hot_key=True,standard_scaler=False):
    return trans_data(pd_test_data,one_hot_key=one_hot_key,standard_scaler=standard_scaler)


def get_split_data(test_size=0.2,random_state=42,one_hot_key=True,standard_scaler=False):
    '''
    函数说明：将数据根据指定的比例分为测试集和训练集
    参数说明：
        test_size:测试集比例
        random_state:随机划分测试集的随机数种子
        one_hot_key:是否采用独热编码
        standard_scaler:是否使用变量标准化
    函数返回值:
        以元组(features,target_label)的形式返回数据
    '''
    X,y = get_train_data(one_hot_key=one_hot_key,standard_scaler=standard_scaler)
    return train_test_split(X,y,test_size=test_size,random_state=random_state)

if __name__ == '__main__':
    #X,y = trans_data(one_hot_key=False,standard_scaler=False)
    #print(X.shape)
    #print(y.shape)
    X,y = get_train_data()
    X_test,y_test = get_test_data()
    print(X.shape,X_test.shape)
    print(y.shape,y_test.shape)
