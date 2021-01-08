# TODO: evaluate.calc_all函数的参数
from sklearn.ensemble import AdaBoostClassifier
import time
import os
import json

import read_data
import evaluate
import tools
from get_hyper_paras import get_section
from config import read_config

file_path = os.path.dirname(os.path.abspath(__file__))
result_file_path = os.path.join(file_path,'../frontend/data/adaboost.json')

def ada_boost(i_time=10):
    '''
    函数说明：adaboost算法
    参数说明：
        i_time：生成模型取平均表现的个数
        X,y,X_test,y_test如果传值的话，会运行的快一些
    '''
    hyper_paras = get_section('ada_boost')

    one_hot_key = read_config['adaboost']['one_hot_key']
    standard_scaler = read_config['adaboost']['standard_scaler']
    for i in range(i_time):
        ada_clf = AdaBoostClassifier(n_estimators=hyper_paras['n_estimators'],
                                       learning_rate=hyper_paras['learning_rate'],
                                       algorithm=hyper_paras['algorithm'],
									   )
        temp_file_name = os.path.join(file_path,'../output_data/adaboost/adaboost{}.csv'.format(i))
        X,y,X_test,y_test = read_data.trans_data(one_hot_key=one_hot_key,standard_scaler=standard_scaler,filename=temp_file_name)
        start = time.clock()
        ada_clf.fit(X,y)
        end = time.clock()
        train_time = end - start
        if i == 0:
            # print(type(knn_clf),type(X_test),type(y_test),type(train_time))
            file_describe = open(result_file_path,'w')
            result = evaluate.calc_all(ada_clf,X_test,y_test,train_time,file_describe,save_img=True,filename="adaboost.png",result_filename=temp_file_name)
        else:
            file_describe = open(result_file_path,'a')
            tools.dict_add(result,evaluate.calc_all(ada_clf,X_test,y_test,train_time,file_describe,result_filename=temp_file_name))
        tools.add_complete()
    tools.dict_div(result,i_time)
    file_describe = open(result_file_path,'a')
    jsonobj = json.dumps(result)
    file_describe.write(jsonobj)
    file_describe.write('\n')
    file_describe.close()
    return result


if __name__ == '__main__':
    print(ada_boost(i_time=2))
    ## print('???')
