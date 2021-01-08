# 需要计算 分类精度、严重分类错误率、运行时间、偏差、方差
from sklearn.metrics import accuracy_score,recall_score
from sklearn.metrics import confusion_matrix
import numpy as np
import configparser
import os
import json
import pandas as pd

from roc import roc_curve

config = configparser.ConfigParser()
file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(file_path,'hyper_parameter.ini')
config.read_file(open(config_path))


def _calc_diff_generater(a,b):
    def cal_diff(y,predict,flag=True):
        if(flag):
            return np.sum(np.sum((y==a)&(predict==b)))
        else:
            return 0
    return cal_diff

calc_ig_01 = _calc_diff_generater(0,1)
calc_ig_10 = _calc_diff_generater(1,0)
calc_ig_23 = _calc_diff_generater(2,3)
calc_ig_12 = _calc_diff_generater(1,2)
calc_ig_13 = _calc_diff_generater(1,3)

# 如下几种情况被认为是严重错误
# 2->0，3->0，3->1，3->2
calc_err_20 = _calc_diff_generater(2,0)
calc_err_30 = _calc_diff_generater(3,0)
calc_err_31 = _calc_diff_generater(3,1)
calc_err_32 = _calc_diff_generater(3,2)

def calc_precision(y,y_pred,not_ig = True,
                                 ig_all = False,
                                 ig_01 = False,
                                 ig_10 = False,
                                 ig_23 = False,
                                 ig_12 = False,
                                 ig_13 = False):
    '''
    函数说明：计算算法的准确率
    参数说明：
        y_pred:模型在测试集上的预测结果
        y:实际测试数据集的标记
        not_ig:表示不忽略，优先级最高
        ig_all:表示忽略全部，优先级仅次于not_ig
        ig_01:忽略0->1的情况
        其他类似
    函数返回值:
        算法的准确率
    '''
    if not_ig:
        return accuracy_score(y_pred,y)
    if ig_all:
        meet_count = np.sum((y_pred == y))
        meet_count += calc_ig_01(y,y_pred)
        meet_count += calc_ig_10(y,y_pred)
        meet_count += calc_ig_23(y,y_pred)
        meet_count += calc_ig_12(y,y_pred)
        meet_count += calc_ig_13(y,y_pred)
        return meet_count/len(y)
    meet_count = np.sum((y_pred == y))
    meet_count += calc_ig_01(y,y_pred,flag = ig_01)
    meet_count += calc_ig_10(y,y_pred,flag = ig_10)
    meet_count += calc_ig_23(y,y_pred,flag = ig_23)
    meet_count += calc_ig_12(y,y_pred,flag = ig_12)
    meet_count += calc_ig_13(y,y_pred,flag = ig_13)
    return meet_count/len(y)


def calc_recall(y,y_pred,average='micro',not_ig = True,
                                         ig_all = False,
                                         ig_01 = False,
                                         ig_10 = False,
                                         ig_23 = False,
                                         ig_12 = False,
                                         ig_13 = False):
    '''
    函数说明：计算算法的回召率
    参数说明：
        y:实际测试数据集的标记
        y_pred:模型在测试集上的预测结果
        not_ig:表示不忽略，优先级最高
        ig_all:表示忽略全部，优先级仅次于not_ig
        ig_01:忽略0->1的情况
        其他类似
    函数返回值:
        算法的recall
    '''
    if average == 'micro':
        if not_ig:
            return recall_score(y,y_pred,average='micro')
        conf_matrix = confusion_matrix(y, y_pred)
        recall_item_denominator = [np.sum(conf_matrix[0]),
                                   np.sum(conf_matrix[1]),
                                   np.sum(conf_matrix[2]),
                                   np.sum(conf_matrix[3])]


        if ig_all:
            TP_all = conf_matrix[0,0]+conf_matrix[0,1]+conf_matrix[1,0]\
                     +conf_matrix[1,1]+conf_matrix[1,2]+conf_matrix[1,3]\
                     +conf_matrix[2,2]+conf_matrix[2,3]+conf_matrix[3,3]
            TP_average = TP_all / 4
            FN_all = conf_matrix[0,2]+conf_matrix[0,3]\
                    +0\
                    +conf_matrix[2,0]+conf_matrix[2,1]\
                    +conf_matrix[3,0]+conf_matrix[3,1]+conf_matrix[3,2]
            FN_average = FN_all / 4
            return TP_average/(TP_average+FN_average)
        TP_all = conf_matrix[0,0]+conf_matrix[1,1]+conf_matrix[2,2]+conf_matrix[3,3]
        FN_all = np.sum(conf_matrix) - TP_all
        if ig_01:
            TP_all += conf_matrix[0,1]
            FN_all -= conf_matrix[0,1]
        if ig_10:
            TP_all += conf_matrix[1,0]
            FN_all -= conf_matrix[1,0]
        if ig_23:
            TP_all += conf_matrix[2,3]
            FN_all -= conf_matrix[2,3]
        if ig_12:
            TP_all += conf_matrix[1,2]
            FN_all -= conf_matrix[1,2]
        if ig_13:
            TP_all += conf_matrix[1,3]
            FN_all -= conf_matrix[1,3]
        TP_average = TP_all / 4
        FN_average = FN_all / 4
        return TP_average/(TP_average+FN_average)
    if average == 'macro':
        if not_ig:
            return recall_score(y,y_pred,average='macro')
        conf_matrix = confusion_matrix(y, y_pred)
        recall_item_denominator = [np.sum(conf_matrix[0]),
                                   np.sum(conf_matrix[1]),
                                   np.sum(conf_matrix[2]),
                                   np.sum(conf_matrix[3])]
        for i in range(4):
            if recall_item_denominator[i] == 0:
                recall_item_denominator[i] = 1
        # print(conf_matrix)
        recall_item_numerator = [conf_matrix[0,0],
                                 conf_matrix[1,1],
                                 conf_matrix[2,2],
                                 conf_matrix[3,3]]
        if ig_all:
            recall_item_numerator[0] += conf_matrix[0,1]
            recall_item_numerator[1] += conf_matrix[1,0]
            recall_item_numerator[2] += conf_matrix[2,3]
            recall_item_numerator[1] += conf_matrix[1,2]
            recall_item_numerator[1] += conf_matrix[1,3]
            return np.sum(np.array(recall_item_numerator)/np.array(recall_item_denominator))/4

        if ig_01:
            recall_item_numerator[0] += conf_matrix[0,1]
        if ig_10:
            recall_item_numerator[1] += conf_matrix[1,0]
        if ig_23:
            recall_item_numerator[2] += conf_matrix[2,3]
        if ig_12:
            recall_item_numerator[1] += conf_matrix[1,2]
        if ig_13:
            recall_item_numerator[1] += conf_matrix[1,3]
        return np.sum(recall_item_numerator/recall_item_denominator)/4

def calc_bias(predict,y):
        '''
        函数说明：计算算法在测试集上的偏差
        参数说明：
            predict:模型在测试集上的预测结果
            y:实际测试数据集的标记
        函数返回值:
            算法的偏差
        '''
        return np.abs(predict.mean() - y.mean())

def cal_variance(predict,y):
    return (y-predict).var()

def cal_serious_err(predict,y):
    err_count = 0
    err_count += calc_err_20(predict,y)
    err_count += calc_err_30(predict,y)
    err_count += calc_err_31(predict,y)
    err_count += calc_err_32(predict,y)
    return err_count/len(y)


def write_to_file(X_test,y_test,y_pred,filename,index):
    index = np.where(y_test != y_pred)
    pd.DataFrame(np.c[X_test[index],y_test[index],y_pred[index]])


def calc_all(model,X_test,y,train_time,file_describe,save_img=False,filename='img.png',result_filename='xx',not_ig = config.getboolean('evaluation_criterion','not_ig'),
                                                                                                            ig_all = config.getboolean('evaluation_criterion','ig_all'),
                                                                                                            ig_01 = config.getboolean('evaluation_criterion','ig_01'),
                                                                                                            ig_10 = config.getboolean('evaluation_criterion','ig_10'),
                                                                                                            ig_23 = config.getboolean('evaluation_criterion','ig_23'),
                                                                                                            ig_12 = config.getboolean('evaluation_criterion','ig_12'),
                                                                                                            ig_13 = config.getboolean('evaluation_criterion','ig_13')):
    if save_img:
        img_path = os.path.join(file_path,'../frontend/public/images/{}'.format(filename))
        # print(img_path)
        roc_curve(X_test,y,model,average='macro',filename=img_path)
    predict = model.predict(X_test)
    result_data = pd.read_csv(result_filename)
    pd.DataFrame(np.c_[result_data.values,predict]).to_csv(path_or_buf=result_filename, index=False)
    precision = calc_precision(predict,y,not_ig=not_ig,ig_all=ig_all,ig_01=ig_01,ig_10=ig_10,ig_23=ig_23,ig_12=ig_12,ig_13=ig_13)
    recall = calc_recall(predict,y,average=config.get('sys','recall_average'),not_ig=not_ig,ig_all=ig_all,ig_01=ig_01,ig_10=ig_10,ig_23=ig_23,ig_12=ig_12,ig_13=ig_13)
    bias = calc_bias(predict,y)
    variance = cal_variance(predict,y)
    serious_err = cal_serious_err(predict,y)
    result = {'recall':recall,'precision':precision,'train_time':train_time,'bias':bias,'variance':variance,'serious_err':serious_err}
    jsonobj = json.dumps(result)
    file_describe.write(jsonobj)
    file_describe.write('\n')
    file_describe.close()
    return result

if __name__ == '__main__':
    print(calc_err_20(np.array([1,1,2,2,3]),np.array([0,0,0,0,0])))
