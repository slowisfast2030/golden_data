import json
import pandas as pd
from zhconv import convert
import jieba

'''
转中文简体
转英文小写
可以添加自定义词典
jieba精确模式合适

原始数据的列是一个列表，列表里的每一个元素一般都是单一的，但是也有类似于斜杆分割的情况。建议分词后ji'zhong
通过jieba分词后会有很多标点符号，可以获取分词后的词典整体过滤
'''

# 读取csv文件
def load_csv_data(data_path):
    df = pd.read_csv(data_path)
    return df

# 给定列名，对给定列名生成词典
def gen_col_dict(df, col_name):
    dict_col = []
    for line in df[col_name].dropna():
        # 转中文简体
        line = convert(line, "zh-hans")
        # 转英文小写
        line = line.lower() 
        # 字符串转列表
        line = json.loads(line)
        dict_col.extend(line)
    return dict_col

def dict_to_file(dict_col, file_path):
    with open(file_path, "w") as fo:
        for line in dict_col:
            fo.write(line + "\n")

# 对dict_col字典的每一个元素进行分词处理
def jieba_process(dict_col):
    dict_col_jiaba = []
    for word in dict_col:
        seg_list = jieba.lcut(word, cut_all=False)
        dict_col_jiaba.extend(seg_list)
    return dict_col_jiaba


if __name__ == "__main__":
    print("running...")

    data_path = './sample_20220821_spark.csv'
    col_name = 'tags'

    df = load_csv_data(data_path)

    # jieba分词前的字典
    dict_col = gen_col_dict(df, col_name)
    dict_to_file(dict_col, './linus_col_dict')

    # jieba分词后的字典
    dict_col_jieba = jieba_process(dict_col)
    dict_to_file(dict_col_jieba, './linus_col_dict_jieba')

    print("all is well")