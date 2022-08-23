import jieba
from sklearn.feature_extraction.text import CountVectorizer

def load_dict(dict_path=None):
    dict_col = open(dict_path)
    # 这里的名字取得不太好。严格来讲，这里的列表是文档的集合。列表元素是文档。
    # 当然，把列表元素设置为一个个词也行。只不过对于词就不需要分词了。对于文档还会分词。
    dict_col = ["hello", "world peace", "mit thu"]
    # 分词结果：{'hello': 0, 'world': 4, 'peace': 2, 'mit': 1, 'thu': 3}
    vectorizer = CountVectorizer()
    # 分词并建立词汇表
    vectorizer.fit(dict_col)
    return vectorizer

def gen_vector(vectorizer, text):
    text = jieba.lcut(text, cut_all=False)
    print("分词的结果:", text)
    text = sorted(text)
    text = [" ".join(text)]
    print(text)
    vector = vectorizer.transform(text)
    return vector.toarray()[0]

if __name__ == "__main__":
    dict_path = "./dict_col_jieba_filter"
    text = '"THu","HeLlo mit","运营","搭建","招聘","架构","法律","客服"'
    text = "hello thu mit hello 青海中国"
    vectorizer = load_dict(dict_path)
    print("词袋:", vectorizer.vocabulary_)

    vector = gen_vector(vectorizer, text)
    print(vector)