import json
import jieba
import re
import numpy as np
import pandas as pd
from zhconv import convert
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA


# 读取csv文件
def load_csv_data(data_path):
    df = pd.read_csv(data_path)
    return df

# 将某列的文本字符串转成列表并切词
def col_jieba_fun(series):
    # 获得字符串
    col = series[col_name]

    # 字符串变列表
    if col.startswith("[") and col.endswith("]"):
        col = json.loads(col)
    else:
        col = re.split(",|，", col)

    # 对于中文，进入jieba前不需要添加空格
    # 不过，如果是中英文混合，就必须空格了
    col_str = " ".join(col)
    col_list = jieba.lcut(col_str, cut_all=False)
    return col_list

# 对切词后的列表进行过滤
def col_jieba_filter_fun(series):

    col_list_filter = []
    # 得到tag列表
    col_list = series[col_name_jieba]
    # print(tags_list[0])

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

# 转成tfidf向量
def get_tfidf(df, col_name):
    text = df[col_name]
    
    vectorizer = TfidfVectorizer()
    # 返回的是nparray
    vector = vectorizer.fit_transform(text)
    return pd.DataFrame(vector.toarray()), vectorizer

# 对tfidf降维到n维
def get_tfidf_pca(tfidf, n=20):
    pca = PCA(n_components=n)
    tfidf_pca = pca.fit_transform(tfidf)
    tfidf_pca = pd.DataFrame(tfidf_pca)
    return tfidf_pca

# 测试tfidf是否正确
def test_tfidf(num=0):
    # 获取第num条数据
    words = df[col_name_jieba_filter][num].split(" ")
    print(words)

    # 交换vocabulary_的key和value。交换后可以通过索引得到词。
    new_vocab = {}
    for word, index in vectorizer.vocabulary_.items():
        new_vocab[str(index)] = word

    # 第num条数据的非零值对应的word
    for index, value in enumerate(tfidf.iloc[num]):
        if value:
            print(new_vocab[str(index)], value)
    
    # 每个词的idf，保存为文件
    with open("./word_idf_temp", "w") as fo:
        for word, index in vectorizer.vocabulary_.items():
            fo.write("{}\t{}\n".format(word, vectorizer.idf_[index]))

# 将文本列保存下来。格式：index + 文本
def save_text():
    file = col_name_jieba_filter + '_temp'
    with open(file, "w") as fo:
        for index, line in enumerate(df[col_name_jieba_filter]):
            fo.write("{}:\t{}\n".format(index, line))


if __name__ == "__main__":
    print("running...")

    # csv文件和待处理的列名
    data_path = './sample_20220821_spark.csv'
    col_name = 'tags'
    #col_name = 'skills'
    col_name_jieba = col_name + '_jieba'
    col_name_jieba_filter = col_name_jieba + '_filter'

    # 读取csv文件
    df = load_csv_data(data_path)
    # 空值填充
    df[col_name].fillna('[]', inplace=True)
    # 对要处理的文本列进行预处理
    df[col_name_jieba] = df.apply(col_jieba_fun, axis=1)
    df[col_name_jieba_filter] = df.apply(col_jieba_filter_fun, axis=1)
    print(df[[col_name, col_name_jieba, col_name_jieba_filter]])

    tfidf, vectorizer = get_tfidf(df, col_name_jieba_filter)
    print(tfidf)

    tfidf_pca = get_tfidf_pca(tfidf, 10)
    print(tfidf_pca)

    
    save_text()
    print("all is well")

    print("============================test=============================")
    # 测试第num条数据
    test_tfidf(num=110)
    
