import configparser
import os

file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(file_path,'hyper_parameter.ini')
complete_file_path = os.path.join(file_path,'../complete_file.txt')
config = configparser.ConfigParser()
config.read_file(open(config_path))
i_time = config.getint('sys','i_time')

with open(complete_file_path,'w') as f:
    f.write("0,"+str(i_time * 11))

with open(os.path.join(file_path,"pid.txt"),'w') as f:
    f.write(str(os.getpid()))

from knn import knn
from ada_boost import ada_boost
from random_forest import random_forest
from logistic import logistic
from svm import svm
from decision_tree import c4_5,cart
from k_mean import k_mean
from xgboost_clf import xgboost
from gbdt_clf import gbdt
from net import net

print('knn:',knn(i_time=i_time))
print('AdaBoost:',ada_boost(i_time=i_time))
print('random forest',random_forest(i_time=i_time))
print('logistic regression:',logistic(i_time=i_time))
print('C4.5:',c4_5(i_time=i_time))
print('cart:',cart(i_time=i_time))
print('k_mean',k_mean(i_time=i_time))
print('xgboost',xgboost(i_time=i_time))
print('gbdt',gbdt(i_time=i_time))
print('SVM:',svm(i_time=i_time))
print('net',net(i_time=i_time))
