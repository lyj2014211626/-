import configparser
import os
import tools

config = configparser.ConfigParser()

file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(file_path,'hyper_parameter.ini')
config.read_file(open(config_path))

def get_section(section):
    '''
    函数说明：从参数配置文件中取得模型的超参数
    '''
    # 返回相应节点的参数，但是字典值全是string，需要转换一下
    temp_paras = config.items(section)
    # [('algorithm', 'ball_tree'), ('leaf_size', '16'), ('n_neighbors', '12')]
    temp_dict = {}
    for item in temp_paras:
        temp_dict[item[0]] = item[1]
    #print(temp_dict)
    tools.trans_dict(temp_dict)
    return temp_dict

if __name__ == '__main__':
    print(get_section('knn'))
