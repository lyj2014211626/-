# TODO: evaluate.calc_all函数的参数
# TODO: 没法做那个评价宽松。。。/好像也可以。。。
from itertools import combinations, permutations
from sklearn.cluster import KMeans
import time
import numpy as np
import os
import json

import read_data
import evaluate
import tools
from get_hyper_paras import get_section
from config import read_config

file_path = os.path.dirname(os.path.abspath(__file__))
result_file_path = os.path.join(file_path,'../frontend/data/k_mean_none.json')
real_result_file_path = os.path.join(file_path,'../frontend/data/k_mean.json')

def _cal_precision(y,y_pred):
    match = list(permutations([0, 1, 2, 3], 4))
    max_sum = 0
    for item in match:
        sum = 0
        for i in range(4):
            sum += np.sum(np.logical_and((y==i),(y_pred==item[i])))
        if(max_sum < sum):
            max_sum = sum
    return max_sum/len(y)

def k_mean(X=None,y=None,X_test=None,y_test=None,i_time=10):
    '''
    函数说明：k均值算法
    参数说明：
        i_time：生成模型取平均表现的个数
        X,y,X_test,y_test如果传值的话，会运行的快一些
    '''
    one_hot_key = read_config['k_mean']['one_hot_key']
    standard_scaler = read_config['k_mean']['standard_scaler']

    for i in range(i_time):
        k_mean = KMeans(n_clusters=4)
        temp_file_name = os.path.join(file_path,'../output_data/k_mean/k_mean{}.csv'.format(i))
        X,y,X_test,y_test = read_data.trans_data(one_hot_key=one_hot_key,standard_scaler=standard_scaler,filename=temp_file_name)
        start = time.clock()
        k_mean.fit(X)
        y_predict = k_mean.predict(X_test)
        end = time.clock()
        train_time = end - start
        if i == 0:
            file_describe = open(result_file_path,'w')
            result = evaluate.calc_all(k_mean,X_test,y_test,train_time,file_describe,result_filename=temp_file_name)
            result['precision'] = _cal_precision(y_test,y_predict)
            file_describe = open(real_result_file_path,'w')
            jsonobj = json.dumps(result)
            file_describe.write(jsonobj)
            file_describe.write('\n')
            file_describe.close()

        else:
            file_describe = open(result_file_path,'a')
            # 这儿数据有问题
            temp_result = evaluate.calc_all(k_mean,X_test,y_test,train_time,file_describe,save_img=True,filename="k_mean.png",result_filename=temp_file_name)
            temp_result['precision'] = _cal_precision(y_test,y_predict)
            file_describe = open(real_result_file_path,'a')
            jsonobj = json.dumps(result)
            file_describe.write(jsonobj)
            file_describe.write('\n')
            file_describe.close()
            tools.dict_add(result,temp_result)
        tools.add_complete()
    tools.dict_div(result,i_time)
    file_describe = open(real_result_file_path,'a')
    jsonobj = json.dumps(result)
    file_describe.write(jsonobj)
    file_describe.write('\n')
    file_describe.close()
    return result


if __name__ == '__main__':
    print(k_mean(i_time=2))
