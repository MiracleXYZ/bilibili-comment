from bilibili import *
import os
import time
import pickle
import jieba
import numpy as np
import pandas as pd
from gensim import corpora, models, similarities
from tqdm import tqdm_gui
from search import search_and_get_danmaku

def calc_similarities(doc_test_list):
    n_words = len(dictionary.keys())
    doc_test_vec = dictionary.doc2bow(doc_test_list)
    tfidf = models.TfidfModel(corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=n_words)
    sim = index[tfidf[doc_test_vec]]

    entry = np.zeros((1, n_words))
    for num, value in tfidf[doc_test_vec]:
        entry[0, num] = value
    return sim, entry

def user_similarity_analysis(names, uids, filename):
    doc_path = './data/all_doc_list.pkl'
    if os.path.exists(doc_path):
        with open(doc_path, 'rb') as f:
            all_doc_list = pickle.load(f)
    else:
        all_doc_list = []

    for name, uid in tqdm_gui(list(zip(names, uids))[len(all_doc_list):]):
        print('获取弹幕：{}'.format(name))
        user = User(uid)
        user.get_danmaku()
        print('弹幕长度：{}'.format(len(user.danmaku_list)))
        user.danmaku_list.extract_keywords(500)
        doc = user.danmaku_list.tags
        # doc = [word for sentence in user.danmaku_list for word in jieba.cut(sentence)]
        all_doc_list.append(doc)
        with open(doc_path, 'wb') as f:
            pickle.dump(all_doc_list, f)


    global dictionary, corpus
    dictionary = corpora.Dictionary(all_doc_list)
    corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]

    similarity_matrix = np.zeros((len(names), len(names)))
    dataset = np.zeros((len(names), len(dictionary.keys())))
    for idx, name in enumerate(names):
        doc_test_list = all_doc_list[idx]
        sim_row, data_row = calc_similarities(doc_test_list)
        similarity_matrix[idx, :] = sim_row
        dataset[idx, :] = data_row
    sim_frame = pd.DataFrame(similarity_matrix, index=names, columns=names)
    sim_frame.to_csv('data/{}.csv'.format(filename), encoding='utf8')

    df = pd.DataFrame(dataset, index=names)
    df.to_csv('data/{}_dataset.csv'.format(filename), encoding='utf8')

    return sim_frame, df

def tag_similarity_analysis(keywords, filename, tids_1=None):
    doc_path = './data/all_doc_list.pkl'
    if os.path.exists(doc_path):
        with open(doc_path, 'rb') as f:
            all_doc_list = pickle.load(f)
    else:
        all_doc_list = []

    for keyword in tqdm_gui(keywords[len(all_doc_list):]):
        danmaku_list = search_and_get_danmaku(keyword, tids_1)
        danmaku_list.extract_keywords(500)
        doc = danmaku_list.tags
        all_doc_list.append(doc)
        with open(doc_path, 'wb') as f:
            pickle.dump(all_doc_list, f)

    global dictionary, corpus
    dictionary = corpora.Dictionary(all_doc_list)
    corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]

    similarity_matrix = np.zeros((len(keywords), len(keywords)))
    dataset = np.zeros((len(keywords), len(dictionary.keys())))
    for idx, name in enumerate(keywords):
        doc_test_list = all_doc_list[idx]
        sim_row, data_row = calc_similarities(doc_test_list)
        similarity_matrix[idx, :] = sim_row
        dataset[idx, :] = data_row
    sim_frame = pd.DataFrame(similarity_matrix, index=keywords, columns=keywords)
    sim_frame.to_csv('data/{}.csv'.format(filename), encoding='utf8')

    df = pd.DataFrame(dataset, index=keywords)
    df.to_csv('data/{}_dataset.csv'.format(filename), encoding='utf8')

    return sim_frame, df

# if __name__ == '__main__':
#     names = ['絆愛', '輝夜月', '猫宮ひなた', '電脳少女シロ', 'ミライアカリ', '時乃空', '小希&小桃']
#     uids = [1473830, 265224956, 291296062, 11725160, 54081, 286179206, 5563350]
#     user_similarity_analysis(names, uids, 'VTubers')

# if __name__ == '__main__':
#     keywords = ['比利', '木吉', 'VAN', '贝奥兰迪', '香蕉君']
#     tag_similarity_analysis(keywords, 'philosophy')


if __name__ == '__main__':
    keywords = [
        '洛天依', '乐正绫', '言和', '乐正龙牙', '星尘', '心华',
        '初音MIKU', 'MIKU', '初音未来', '初音ミク',
        '镜音RIN', '镜音铃', '鏡音リン',
        '镜音LEN', '镜音连', '鏡音レン',
        '巡音LUKA', '巡音流歌', '巡音ルカ',
        'MEIKO', 'KAITO', 'GUMI'
    ]
    retry_count = 0
    while retry_count <= 10:
        try:
            tag_similarity_analysis(keywords, 'vocaloid')
            break
        except Exception as e:
            print(e)
            retry_count += 1
            print('Waiting...')
            time.sleep(60)
            print('Retrying...')



    

