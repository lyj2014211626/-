# TODO: evaluate.calc_all函数的参数
import time
import os
import json

import read_data
import evaluate
import tools
from get_hyper_paras import get_section
from config import read_config

file_path = os.path.dirname(os.path.abspath(__file__))
result_file_path = os.path.join(file_path,'../frontend/data/net.json')

from functools import partial
import tensorflow as tf

class Temp_result_model:
    def __init__(self,result):
        self.result = result
    def predict(self,any_all_ok):
        return np.array(self.result)

import numpy as np

def next_batch(num, data, labels):
    '''
    Return a total of `num` random samples and labels.
    '''
    idx = np.arange(0 , len(data))
    np.random.shuffle(idx)
    idx = idx[:num]
    data_shuffle = [data[ i] for i in idx]
    labels_shuffle = [labels[ i] for i in idx]

    return np.asarray(data_shuffle), np.asarray(labels_shuffle)

n_inputs = 40
n_hidden1 = 300
n_hidden2 = 100
n_outputs = 4

batch_norm_momentum = 0.9
learning_rate = 0.01

X_tensor = tf.placeholder(tf.float32, shape=(None, n_inputs), name = 'X')
y_tensor = tf.placeholder(tf.int64, shape=None, name = 'y')
training = tf.placeholder_with_default(False, shape=(), name = 'training')#给Batch norm加一个placeholder

with tf.name_scope("dnn"):
    he_init = tf.contrib.layers.variance_scaling_initializer()
    #对权重的初始化

    my_batch_norm_layer = partial(
        tf.layers.batch_normalization,
        training = training,
        momentum = batch_norm_momentum
    )

    my_dense_layer = partial(
        tf.layers.dense,
        kernel_initializer = he_init
    )

    hidden1 = my_dense_layer(X_tensor ,n_hidden1 ,name = 'hidden1')
    bn1 = tf.nn.elu(my_batch_norm_layer(hidden1))
    hidden2 = my_dense_layer(bn1, n_hidden2, name = 'hidden2')
    bn2 = tf.nn.elu(my_batch_norm_layer(hidden2))
    logists_before_bn = my_dense_layer(bn2, n_outputs, name = 'outputs')
    logists = my_batch_norm_layer(logists_before_bn)

with tf.name_scope('loss'):
    xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels = y_tensor, logits= logists)
    loss = tf.reduce_mean(xentropy, name = 'loss')

with tf.name_scope('train'):
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    training_op = optimizer.minimize(loss)

with tf.name_scope("eval"):
    correct = tf.nn.in_top_k(logists, y_tensor, 1)
    accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

init = tf.global_variables_initializer()
saver = tf.train.Saver()

n_epoches = 1
batch_size = 100
# 注意：由于我们使用的是 tf.layers.batch_normalization() 而不是 tf.contrib.layers.batch_norm()（如本书所述），
# 所以我们需要明确运行批量规范化所需的额外更新操作（sess.run([ training_op，extra_update_ops], ...)。
extra_update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)



def net(i_time=10):
    '''
    函数说明：神经网络算法
    参数说明：
        i_time：生成模型取平均表现的个数
        X,y,X_test,y_test如果传值的话，会运行的快一些
    '''


    one_hot_key = read_config['net']['one_hot_key']
    standard_scaler = read_config['net']['standard_scaler']
    for i in range(i_time):

        temp_file_name = os.path.join(file_path,'../output_data/net/net{}.csv'.format(i))
        X,y,X_test,y_test = read_data.trans_data(one_hot_key=one_hot_key,standard_scaler=standard_scaler,filename=temp_file_name)
        start = time.clock()

        with tf.Session() as sess:
            init.run()
            for epoch in range(n_epoches):
                for iteraton in range(len(X)//batch_size):
                    X_batch, y_batch = next_batch(batch_size,X,y)
                    sess.run([training_op,extra_update_ops],
                             feed_dict={training:True, X_tensor:X_batch, y_tensor:y_batch})
                output = logists.eval(feed_dict= {X_tensor:X_test,
                                                  y_tensor:y_test})
            resultx = [int(np.where(i == i.max())[0]) for i in output]
            model = Temp_result_model(resultx)

        end = time.clock()
        train_time = end - start
        if i == 0:
            # print(type(knn_clf),type(X_test),type(y_test),type(train_time))
            file_describe = open(result_file_path,'w')
            result = evaluate.calc_all(model,X_test,y_test,train_time,file_describe,save_img=False,filename="net.png",result_filename=temp_file_name)
        else:
            file_describe = open(result_file_path,'a')
            tools.dict_add(result,evaluate.calc_all(model,X_test,y_test,train_time,file_describe,result_filename=temp_file_name))
        tools.add_complete()
    tools.dict_div(result,i_time)
    file_describe = open(result_file_path,'a')
    jsonobj = json.dumps(result)
    file_describe.write(jsonobj)
    file_describe.write('\n')
    file_describe.close()
    return result


if __name__ == '__main__':
    print(net(i_time=8))
    ## print('???')
