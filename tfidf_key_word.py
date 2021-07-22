import os
import re
import configparser

import jieba
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer

from connect_db import dbs

root_abs_path = os.path.dirname(os.path.abspath(__file__))

# 读取数据库
cf = configparser.ConfigParser()
cf.read(os.path.join(root_abs_path, 'config.ini'), encoding='utf8')
postgresql_info = dict(cf.items('postgresql'))
pconn = dbs['postgresql'](postgresql_info)
df_sql = '''
    SELECT
        txt
    FROM
        xx
    '''
df = pconn.read_sql(df_sql).fillna('')

# 加载去停用词
with open('cn_stopwords.txt') as f:
    stop_words = f.readlines()
pat = re.compile(r'[^A-Za-z0-9]+$')  # 过滤字母和数字组合

# 预处理文本
corpus_origin = []
corpus = []
for txt in tqdm(df['txt']):
    processed = re.sub(r'\s+', '', txt)
    if processed:
        corpus_origin.append(txt)
        corpus.append(' '.join([word for word in jieba.lcut(processed) if word not in stop_words and pat.match(word)]))

# 抽取tfidf关键词并获取最多前10个，按权重由大到小排
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
keywords = []
bagwords = np.array(vectorizer.get_feature_names())
for item in tqdm(X.toarray()):
    select = item > 0
    select_words = sorted(zip(bagwords[select], item[select]), key=lambda x: x[1], reverse=True)
    keywords.append(' '.join([sw[0] for sw in select_words[:10]]))  # 获取前几个

# 写入Excel
pd.DataFrame({'txt': corpus_origin, 'keywords': keywords}).to_excel('keywords.xlsx', index=False)
