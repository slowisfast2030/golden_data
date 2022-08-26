import json
import jieba
import re
import numpy as np
import pandas as pd
from zhconv import convert
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA


def load_csv_data(data_path):
    '''
    读取csv文件
    '''
    df = pd.read_csv(data_path)
    return df

def col_jieba_fun(series):
    '''
    将文本字符串转成列表并切词
    '''
    col = series[col_name]

    # 字符串变列表
    if col.startswith("[") and col.endswith("]"):
        col = json.loads(col)
    else:
        col = re.split(",|，|/| ", col)

    # 列表变字符串
    # 对于中文，进入jieba前不需要添加空格；不过，如果是中英文混合，就必须空格了
    col_str = " ".join(col)

    # 切词
    col_list = jieba.lcut(col_str, cut_all=False)
    return col_list

def col_jieba_filter_fun(series):
    '''
    对切词后的列表进行过滤
    '''
    col_list_filter = []
    
    # 得到切词列表
    col_list = series[col_name_jieba]

    pun_masks_english = [",", ".", "/", "[", "]", "{", "}", "(", ")", ":", "*", "#", "!", " ", "\"", "\\"]
    pun_masks_chinese = ["，", "。", "、", "（", "）", "：", "！", "”", "“"]
    pun_masks = pun_masks_english + pun_masks_chinese

    # 过滤
    for tag in col_list:
        # 转中文简体
        tag = convert(tag, "zh-hans")
        # 转英文小写
        tag = tag.lower()

        # 过滤数字
        if tag.isdigit():
            continue
        
        # 过滤单个字符
        if len(tag) <= 1:
            continue
        
        # 过滤标点
        flag = 1
        for pun in pun_masks:
            if pun in tag:
                flag = 0
                break
        if flag == 1:
            col_list_filter.append(tag)
    return " ".join(col_list_filter)

def get_tfidf(df, col_name):
    '''
    转成tfidf向量
    '''
    text = df[col_name]
    
    vectorizer = TfidfVectorizer()
    vector = vectorizer.fit_transform(text)
    return pd.DataFrame(vector.toarray()), vectorizer

def get_tfidf_pca(tfidf, n=20):
    '''
    对tfidf降维到n维
    '''
    pca = PCA(n_components=n)
    tfidf_pca = pca.fit_transform(tfidf)
    tfidf_pca = pd.DataFrame(tfidf_pca)
    return tfidf_pca

def get_jieba_filter_from_col(data_path, col_name):

    global col_name_jieba 
    col_name_jieba = col_name + '_jieba'

    global col_name_jieba_filter 
    col_name_jieba_filter = col_name_jieba + '_filter'
    # 读取csv文件
    df = load_csv_data(data_path)

    # step1 空值填充
    df[col_name].fillna('', inplace=True)

    # step2 jieba分词
    df[col_name_jieba] = df.apply(col_jieba_fun, axis=1)

    # step3 分词过滤
    df[col_name_jieba_filter] = df.apply(col_jieba_filter_fun, axis=1)
    print(df[[col_name, col_name_jieba, col_name_jieba_filter]])

    pass


if __name__ == "__main__":
    print("running...")

    data_path = '../data/all_sample_20220821_spark.csv'
    #col_name = 'tags'
    col_name = 'skills'
    num = 10

    print("all is well")

    
    
