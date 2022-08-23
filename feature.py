# -*- coding: UTF-8 -*-
import re
import json
import pandas as pd
from zhconv import convert
import jieba

'''
可以添加自定义词典
出现了”以上“？
'''

# 读取csv文件
def load_csv_data(data_path):
    df = pd.read_csv(data_path)
    return df

# 给定列名，生成字典
def gen_col_dict(df, col_name):
    dict_col = []
    for line in df[col_name].dropna():
        # print(line)
        # 转中文简体
        line = convert(line, "zh-hans")
        # 转英文小写
        line = line.lower()

        # 字符串转列表。
        # 一般而言，每一行都是列表数据，但有的数据入库时忘了[]。
        if line.startswith("["):
            line = json.loads(line)
        else:
            # 如果后续需要更多的分词标点，记得添加
            line = re.split(",|，", line)
        dict_col.extend(line)
    return dict_col

# 保存字典到文件
def dict_to_file(dict_col, file_path):
    with open(file_path, "w") as fo:
        for line in dict_col:
            fo.write(line + "\n")

# 对每个元素分词，生成分词后的字典
def jieba_process(dict_col):
    dict_col_jieba = []
    for word in dict_col:
        # 精确模式
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
    col_name = 'skills'

    # 读取csv文件
    df = load_csv_data(data_path)

    # 原始col列构成的字典
    dict_col = gen_col_dict(df, col_name)
    dict_to_file(dict_col, './dict_tags')
    print("原始词典{}的大小是{}".format('dict_tags', len(dict_col)))

    # jieba分词后的字典
    dict_col_jieba = jieba_process(dict_col)
    dict_to_file(dict_col_jieba, './dict_tags_jieba')
    print("jieba分词后{}的大小是{}".format('dict_tags_jieba', len(dict_col_jieba)))

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
    dict_to_file(dict_col_filter, './dict_tags_jieba_filter')

    print("all is well")