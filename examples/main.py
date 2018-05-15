
# coding: utf-8


import requests
from bs4 import BeautifulSoup
import json
import re
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator


def crawl_danmaku(cid):
    url = 'https://comment.bilibili.com/{}.xml'.format(cid)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    danmaku = soup.select('d')
    danmaku_list = [danmaku[i].get_text() for i in range(len(danmaku))]
    return danmaku_list

def extract_keywords(danmaku_list, top=500):
    jieba.add_word('花Q')
    jieba.add_word('嗨多磨')
    seg = [' '.join(jieba.cut(dan)) for dan in danmaku_list]

    sentence = ' '.join(seg)

    tags = jieba.analyse.extract_tags(sentence, top)
    tags_sentence = ' '.join(tags)
    return tags_sentence

def gen_wordcloud(tags_sentence, mask, font, scale=8):
    coloring = plt.imread(mask)
    image_colors = ImageColorGenerator(coloring)
    wordCloud = WordCloud(background_color="white",
                          mask=coloring,
                          font_path=font,
                          random_state=60,
                          max_words=3000,
                          scale=scale).generate(tags_sentence)
    wordCloud.recolor(color_func=image_colors)
    return wordCloud

def save_wordcloud(wordCloud, output):
    wordCloud.to_file(output)

def wordcloud_workflow(aid, mask, output, scale=8):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        #'Cookie': cookie
    }

    avurlstr = 'https://www.bilibili.com/video/av{}/'

    cids = []
    print('Getting cids...')
    avurl = avurlstr.format(aid)
    wb_data = requests.get(avurl, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    match1 = [cid[5:-1] for cid in re.findall("cid='\d+'", wb_data.text)]
    cids.extend(match1)
    if len(match1) == 0:
        match2 = [cid[4:-1] for cid in re.findall('cid=\d+&', wb_data.text)]
        cids.extend(match2)
    cids = list(set(cids))
    print('{} cids totally catched.'.format(len(cids)))

    danmaku = []
    for cid in cids:
        danmaku_list = crawl_danmaku(cid)
        danmaku.extend(danmaku_list)
        print('#', end='')

    print('Number of danmaku:', len(danmaku))

    tags_sentence = extract_keywords(danmaku)

    font = 'C://Windows/Fonts/msyh.ttc'

    wordCloud = gen_wordcloud(tags_sentence, mask, font, scale=scale)
    save_wordcloud(wordCloud, output)

    print('Wordcloud successfully generated.')



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--uid', type=int, default=None)
    parser.add_argument('--page', type=int, default=10)
    parser.add_argument('--mask', type=str, default=None)
    parser.add_argument('--output', type=str, default=None)
    args = parser.parse_args()
    uid = args.uid
    page = args.page
    mask = args.mask
    output = args.output

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        #'Cookie': cookie
    }

    urlstr = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&pagesize=30&tid=0&page={}&keyword=&order=pubdate'
    avurlstr = 'https://www.bilibili.com/video/av{}/'

    aids = []
    print('Getting aids...')
    for page in range(1, page + 1):
        url = urlstr.format(uid, page)
        wb_data = requests.get(url, headers=headers)
        vlist = json.loads(wb_data.text)['data']['vlist']
        aids.extend([video['aid'] for video in vlist])

    cids = []
    print('Getting cids...')
    for aid in aids:
        avurl = avurlstr.format(aid)
        wb_data = requests.get(avurl, headers=headers)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        match1 = [cid[5:-1] for cid in re.findall("cid='\d+'", wb_data.text)]
        cids.extend(match1)
        if len(match1) == 0:
            match2 = [cid[4:-1] for cid in re.findall('cid=\d+&', wb_data.text)]
            cids.extend(match2)
        print('#', end='')
    print('{} aids and {} cids totally catched.'.format(
        len(aids), len(cids)
    ))

    danmaku = []
    for cid in cids:
        
        danmaku_list = crawl_danmaku(cid)
        danmaku.extend(danmaku_list)
        print('#', end='')

    print('Number of danmaku:', len(danmaku))

    tags_sentence = extract_keywords(danmaku)

    font = 'C://Windows/Fonts/msyh.ttc'

    wordCloud = gen_wordcloud(tags_sentence, mask, font)
    save_wordcloud(wordCloud, output)

    print('Wordcloud successfully generated.')



