import types
import os

def dict_add(dict_a,dict_b):
    '''
    函数说明：两个具有相同键值的字典相加，结果保留在第一个字典里
            没有检查字典键值是否相同，系要检查
    '''
    for key in dict_a.keys():
        dict_a[key] += dict_b[key]

def dict_div(dict_a,b):
    '''
    函数说明：字典的数字部分除上一个整数
    '''
    NumberTypes = (int,float,complex)
    for key in dict_a.keys():
        # 检查值是否为数字类型
        if(isinstance(dict_a[key], NumberTypes)):
            dict_a[key] /= b

def __is_number(s):
    '''
    函数说明：判断s是不是数字类型的字符串
    '''
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def trans_dict(dict_a):
    '''
    函数说明：将dict中value为数字类型的字符串转换为相应的数字类型
    '''
    for key,value in dict_a.items():
        # 检查值是否为数字类型
        if(__is_number(value)):
            dict_a[key] = eval(value)

file_path = os.path.dirname(os.path.abspath(__file__))
complete_file_path = os.path.join(file_path,'../complete_file.txt')
def add_complete():
    temp_str = ''
    with open(complete_file_path,'r+') as f:
        #temp_str
        temp_str = f.readline()
    with open(complete_file_path,'w+') as f:
        str_list = temp_str.split(',')
        str_list[0] = str(int(str_list[0])+1)
        f.write(",".join(str_list))

if __name__ == '__main__':
    add_complete()
