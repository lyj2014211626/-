# TODO: evaluate.calc_all函数的参数
from sklearn.svm import SVC
import time
import os
import json

import read_data
import evaluate
import tools
from get_hyper_paras import get_section
from config import read_config

file_path = os.path.dirname(os.path.abspath(__file__))
result_file_path = os.path.join(file_path,'../frontend/data/svm.json')

def svm(X=None,y=None,X_test=None,y_test=None,i_time=10):
    '''
    函数说明：svm算法
    参数说明：
        i_time：生成模型取平均表现的个数
        X,y,X_test,y_test如果传值的话，会运行的快一些
    '''
    one_hot_key = read_config['svm']['one_hot_key']
    standard_scaler = read_config['svm']['standard_scaler']
    hyper_paras = get_section('svm')

    for i in range(i_time):
        #print(type(hyper_paras['kernel']),type(hyper_paras['degree']),type(hyper_paras['gamma']),type(hyper_paras['shrinking']),type(hyper_paras['c']))
        # 这里重点：使用类别平衡算法

        svm_clf = SVC(kernel=hyper_paras['kernel'],
                      degree=hyper_paras['degree'],
                      gamma=hyper_paras['gamma'],
                      shrinking=eval(hyper_paras['shrinking']),
                      probability=True,
                      )
        '''
        svm_clf = SVC(kernel=hyper_paras['kernel'],
                      class_weight='balanced')
        '''
        temp_file_name = os.path.join(file_path,'../output_data/svm/svm{}.csv'.format(i))
        X,y,X_test,y_test = read_data.trans_data(one_hot_key=one_hot_key,standard_scaler=standard_scaler,filename=temp_file_name)
        start = time.clock()
        svm_clf.fit(X,y)
        end = time.clock()
        train_time = end - start
        if i == 0:
            # print(type(knn_clf),type(X_test),type(y_test),type(train_time))
            file_describe = open(result_file_path,'w')
            result = evaluate.calc_all(svm_clf,X_test,y_test,train_time,file_describe,save_img=True,filename="svm.png",result_filename=temp_file_name)
        else:
            file_describe = open(result_file_path,'a')
            tools.dict_add(result,evaluate.calc_all(svm_clf,X_test,y_test,train_time,file_describe,result_filename=temp_file_name))
        tools.add_complete()
    tools.dict_div(result,i_time)
    file_describe = open(result_file_path,'a')
    jsonobj = json.dumps(result)
    file_describe.write(jsonobj)
    file_describe.write('\n')
    file_describe.close()
    return result


if __name__ == '__main__':
    print(svm(i_time=8))
