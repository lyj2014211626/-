# TODO: evaluate.calc_all函数的参数
from xgboost import XGBClassifier
import time
import os
import json

import read_data
import evaluate
import tools
from get_hyper_paras import get_section
from config import read_config

file_path = os.path.dirname(os.path.abspath(__file__))
result_file_path = os.path.join(file_path,'../frontend/data/xgboost.json')

def xgboost(X=None,y=None,X_test=None,y_test=None,i_time=10):
    '''
    函数说明：xgboost算法
    参数说明：
        i_time：生成模型取平均表现的个数
        X,y,X_test,y_test如果传值的话，会运行的快一些
    '''
    one_hot_key = read_config['xgboost']['one_hot_key']
    standard_scaler = read_config['xgboost']['standard_scaler']
    hyper_paras = get_section('xgboost')


    for i in range(i_time):
        xgboost = XGBClassifier(max_depth=hyper_paras['max_depth'],
                                     learning_rate=hyper_paras['learning_rate'],
                                     n_estimators=hyper_paras['n_estimators'],
                                     n_jobs=hyper_paras['n_jobs'],
                                     booster=hyper_paras['booster'])
        temp_file_name = os.path.join(file_path,'../output_data/xgboost/xgboost{}.csv'.format(i))
        X,y,X_test,y_test = read_data.trans_data(one_hot_key=one_hot_key,standard_scaler=standard_scaler,filename=temp_file_name)
        start = time.clock()
        xgboost.fit(X,y)
        end = time.clock()
        train_time = end - start
        if i == 0:
            # print(type(knn_clf),type(X_test),type(y_test),type(train_time))
            file_describe = open(result_file_path,'w')
            result = evaluate.calc_all(xgboost,X_test,y_test,train_time,file_describe,save_img=True,filename="xgboost.png",result_filename=temp_file_name)
        else:
            file_describe = open(result_file_path,'a')
            tools.dict_add(result,evaluate.calc_all(xgboost,X_test,y_test,train_time,file_describe,result_filename=temp_file_name))
        tools.add_complete()
    tools.dict_div(result,i_time)
    file_describe = open(result_file_path,'a')
    jsonobj = json.dumps(result)
    file_describe.write(jsonobj)
    file_describe.write('\n')
    file_describe.close()
    return result


if __name__ == '__main__':
    print(xgboost(i_time=2))
    ## print('???')
