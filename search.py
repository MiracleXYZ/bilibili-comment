from bilibili import *
import pickle
import os
from tqdm import tqdm, tqdm_gui
import jieba
# jieba.add_word('♂')

def search_and_get_danmaku(keyword, tids_1=None, dump=False):
    search = Search('video', keyword, tids_1)
    results = search.get_results()
    danmaku_list = DanmakuList([])
    print('Getting danmaku...')
    for video in tqdm(results, ascii=True):
        try:
            video.get_danmaku()
        except Exception as e:
            print(video.aid)
            print(video.episodes)
            print(e)
            raise e
        danmaku_list.extend(video.danmaku_list)
    print('Length of danmaku_list:', len(danmaku_list))
    if dump:
        with open('{}.pkl'.format(keyword), 'wb') as f:
            pickle.dump(danmaku_list, f)
    return danmaku_list

def danmaku_wc(keyword, mask, output):
    filename = '{}.pkl'.format(keyword)
    if not os.path.exists(filename):
        search_and_get_danmaku(keyword, dump=True)
    with open(filename, 'rb') as f:
        danmaku_list = pickle.load(f)
    print('length of danmaku list:', len(danmaku_list))
    danmaku_list.generate_wordcloud(mask, output)

if __name__ == '__main__':
    danmaku_wc('与ta恋爱的话', './images/heart2.jpg', './images/heart_output.png')