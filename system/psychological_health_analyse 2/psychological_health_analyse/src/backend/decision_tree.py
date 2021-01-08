# TODO: evaluate.calc_all函数的参数
# TODO: 方法id3没有实现，实现的话，需要修改sklearn库，并且需要重新编译
from sklearn.tree import DecisionTreeClassifier
import time
import os
import json

import read_data
import evaluate
import tools
from get_hyper_paras import get_section
from config import read_config

file_path = os.path.dirname(os.path.abspath(__file__))


def _tree_cls(method,i_time=10):
    '''
    函数说明：id3,c4.5,cart算法
    参数说明：
        method:根据传入的方法，调用相应的fit方法，就会对应执行不同的决策树算法，取值['id3','c4.5','cart']
        i_time：生成模型取平均表现的个数
        X,y,X_test,y_test如果传值的话，会运行的快一些
    '''
    if method in ['id3','cart','c4_5']:
        one_hot_key = read_config[method]['one_hot_key']
        standard_scaler = read_config[method]['standard_scaler']
        result_file_path = os.path.join(file_path,'../frontend/data/{}.json'.format(method))
        img_path = '{}.png'.format(method)
    else:
        raise ValueError('wrong input,just suuport id3,c4_5,cart.')
        #X_test,y_test = read_data.get_test_data(one_hot_key=one_hot_key,standard_scaler=standard_scaler)
    hyper_paras = get_section(method)

    for i in range(i_time):
        tree_clf = DecisionTreeClassifier(criterion=hyper_paras['criterion'],
                                          max_depth=hyper_paras['max_depth'],
                                          min_samples_split=hyper_paras['min_samples_split'])
        temp_file_name = os.path.join(file_path,'../output_data/{}/{}{}.csv'.format(method,method,i))
        X,y,X_test,y_test = read_data.trans_data(one_hot_key=one_hot_key,standard_scaler=standard_scaler,filename=temp_file_name)
        start = time.clock()
        tree_clf.fit(X,y)
        end = time.clock()
        train_time = end - start
        if i == 0:
            # print(type(knn_clf),type(X_test),type(y_test),type(train_time))
            file_describe = open(result_file_path,'w')
            result = evaluate.calc_all(tree_clf,X_test,y_test,train_time,file_describe,save_img=True,filename=img_path,result_filename=temp_file_name)
        else:
            file_describe = open(result_file_path,'a')
            tools.dict_add(result,evaluate.calc_all(tree_clf,X_test,y_test,train_time,file_describe,result_filename=temp_file_name))
        tools.add_complete()
    tools.dict_div(result,i_time)
    file_describe = open(result_file_path,'a')
    jsonobj = json.dumps(result)
    file_describe.write(jsonobj)
    file_describe.write('\n')
    file_describe.close()
    return result

def c4_5(i_time=1):
    return _tree_cls('c4_5',i_time=i_time)

def cart(i_time=1):
    return _tree_cls('cart',i_time=i_time)

if __name__ == '__main__':
    print(c4_5(i_time=2))
    print(cart(i_time=2))
