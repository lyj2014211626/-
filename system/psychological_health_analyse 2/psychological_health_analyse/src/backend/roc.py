from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn.preprocessing import label_binarize
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


def roc_curve(X_test,y_test,estimator,average='macro',filename=None):
	'''
	函数功能：画出模型的roc曲线
	参数说明：
	    X_test：输入的测试数据
	    y_test：测试数据的标签
	    estimator：模型
	    average：['macro','micro']选择F_macro or F_micro
	'''
	if filename != None and "k_mean" in filename:
		return 
	# 先将标签数据独热编码
	y_one_hot = label_binarize(y_test, np.arange(4))
	# 计算模型在测试集上得到的预测结果相应的概率
	y_score = estimator.predict_proba(X_test)
	# 得到相应的threshold对应的查全率，查准率
	fpr, tpr, thresholds = metrics.roc_curve(y_one_hot.ravel(),y_score.ravel())
	# 计算auc值
	auc = metrics.auc(fpr, tpr)
	# matplotlib画图
	# matplotlib.rcParams['font.sans-serif'] = u'SimHei'
	plt.figure()
	matplotlib.rcParams['axes.unicode_minus'] = False
	plt.plot(fpr, tpr, c = 'r', lw = 2, alpha = 0.7, label = u'AUC=%.3f' % auc)
	plt.plot((0, 1), (0, 1), c = '#808080', lw = 1, ls = '--', alpha = 0.7)
	plt.xlim((-0.01, 1.02))
	plt.ylim((-0.01, 1.02))
	plt.xticks(np.arange(0, 1.1, 0.1))
	plt.yticks(np.arange(0, 1.1, 0.1))
	plt.xlabel('False Positive Rate', fontsize=13)
	plt.ylabel('True Positive Rate', fontsize=13)
	plt.grid(b=True, ls=':')
	plt.legend(loc='lower right', fancybox=True, framealpha=0.8, fontsize=12)
	plt.title(u'ROC and AUC', fontsize=17)
	if filename != None:
		plt.savefig(filename)
	else:
		plt.show()

def get_auc_score(X_test,y_test,estimator,average='macro'):
	'''
	函数说明：获取auc值，auc值能够评价模型好坏，roc值越大，相应的模型也就越好
	'''
	y_one_hot = label_binarize(y_test, np.arange(4))
	y_score = estimator.predict_proba(X_test)
	return metrics.roc_auc_score(y_one_hot, y_score, average=average)
