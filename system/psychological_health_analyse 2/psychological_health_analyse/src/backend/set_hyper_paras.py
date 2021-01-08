import configparser
import os

file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(file_path,'hyper_parameter.ini')

def set_section(section,hyper_paras):
    '''
    函数说明：设置超参数文件的模型超参数
    参数说明：
        section:字符串，配置文件的section，即模型名字
        hyper_paras：字典，需要设置超参数名称和值
    '''
    config = configparser.ConfigParser()
    config.read_file(open(config_path))
    for para in hyper_paras.keys():
        config.set(section,para,str(hyper_paras[para]))
    with open(config_path, 'w') as configfile:
        config.write(configfile)

if __name__ == '__main__':
    paras = {'algorithm':'ball_tree','leaf_size':16,'n_neighbors':12}
    set_section('knn',paras)
