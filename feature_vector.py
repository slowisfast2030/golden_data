import jieba
from sklearn.feature_extraction.text import CountVectorizer

def load_dict(dict_path=None):
    dict_col = open(dict_path)
    dict_col = ["hello", "world peace", "mit thu"]
    vectorizer = CountVectorizer()
    # 分词并建立词汇表
    vectorizer.fit(dict_col)
    
    return vectorizer

def gen_vector(vectorizer, text):
    text = jieba.lcut(text, cut_all=False)
    text = sorted(text)
    text = [" ".join(text)]
    print(text)
    vector = vectorizer.transform(text)
    return vector.toarray()[0]

if __name__ == "__main__":
    dict_path = "./dict_col_jieba_filter"
    text = '"thu","HeLlo mit","运营","搭建","招聘","架构","法律","客服"'

    vectorizer = load_dict(dict_path)
    print(vectorizer.vocabulary_)

    vector = gen_vector(vectorizer, text)
    print(vector)