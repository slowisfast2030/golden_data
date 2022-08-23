# -*- coding: UTF-8 -*-

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


去重 
去掉标点符号
去掉数字
去掉单个字母和汉字

出现了”以上“？
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
    dict_col_jieba = []
    for word in dict_col:
        seg_list = jieba.lcut(word, cut_all=False)
        dict_col_jieba.extend(seg_list)
    return dict_col_jieba

# 去重
def dict_filter_dedup(dict_col):
    dict_col_filter = list(set(dict_col))
    return dict_col_filter

# 过滤单个字符
def dict_filter_single_symbol(dict_col):
    dict_col_filter = []
    for word in dict_col:
        if len(word) <= 1:
            continue
        dict_col_filter.append(word)
    return dict_col_filter

# 过滤数字
def dict_filter_num(dict_col):
    dict_col_filter = []
    for word in dict_col:
        if word.isdigit():
            continue
        dict_col_filter.append(word)
    return dict_col_filter

# 过滤标点符号
def dict_filter_pun(dict_col):
    dict_col_filter = []
    # 待过滤标点符号
    pun_masks_english = [",", ".", "/", "[", "]", "{", "}", "(", ")", ":", "*", "#", "!", " ", "\"", "\\"]
    pun_masks_chinese = ["，", "。", "、", "（", "）", "：", "！", "”", "“"]
    pun_masks = pun_masks_english + pun_masks_chinese

    for word in dict_col:
        # 过滤标点符号
        flag = 1
        for pun in pun_masks:
            if pun in word:
                flag = 0
                break
        if flag == 1:
            dict_col_filter.append(word)
    return dict_col_filter


if __name__ == "__main__":
    print("running...")

    # csv文件和待处理的列名
    data_path = './sample_20220821_spark.csv'
    col_name = 'tags'

    # 读取csv文件
    df = load_csv_data(data_path)

    # 原始col列构成的字典
    dict_col = gen_col_dict(df, col_name)
    dict_to_file(dict_col, './linus_col_dict')
    print("原始词典{}的大小是{}".format('dict_col', len(dict_col)))

    # jieba分词后的字典
    dict_col_jieba = jieba_process(dict_col)
    dict_to_file(dict_col_jieba, './linus_col_dict_jieba')
    print("jieba分词后{}的大小是{}".format('dict_col_jieba', len(dict_col_jieba)))

    # 执行一系列过滤操作后的字典
    dict_col_filter = dict_col_jieba
    dict_col_filter = dict_filter_dedup(dict_col_filter)
    print("去重后{}的大小是{}".format('dict_col_filter', len(dict_col_filter)))
    dict_col_filter = dict_filter_single_symbol(dict_col_filter)
    print("去除单个字符后{}的大小是{}".format('dict_col_filter', len(dict_col_filter)))
    dict_col_filter = dict_filter_num(dict_col_filter)
    print("去除数字后{}的大小是{}".format('dict_col_filter', len(dict_col_filter)))
    dict_col_filter = dict_filter_pun(dict_col_filter)
    print("去除标点后{}的大小是{}".format('dict_col_filter', len(dict_col_filter)))
    
    # 保存过滤后的字典
    dict_to_file(dict_col_filter, './linus_col_dict_jieba_filter')

    print("all is well")