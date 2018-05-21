# coding: utf-8

import requests
from bs4 import BeautifulSoup
import json
import re
import jieba
import jieba.analyse
from tqdm import tqdm, trange
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from selenium import webdriver

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

class DanmakuList(list):
    def extract_keywords(self, top=500):
        seg = [' '.join(jieba.cut(dan)) for dan in self]
        sentence = ' '.join(seg)
        tags = jieba.analyse.extract_tags(sentence, top)
        tags_sentence = ' '.join(tags)
        self.tags = tags
        self.tags_sentence = tags_sentence
    def extract_keywords_with_weight(self, top=100):
        seg = [' '.join(jieba.cut(dan)) for dan in self]
        sentence = ' '.join(seg)
        tags = jieba.analyse.extract_tags(sentence, top, withWeight=True)
        self.tags = tags
    def gen_wordcloud(self, mask, font, scale, random_state):
        coloring = plt.imread(mask)
        if coloring.dtype != np.uint8:
            coloring = (coloring * 255).astype(np.uint8)
        image_colors = ImageColorGenerator(coloring)
        wordCloud = WordCloud(
            background_color="white",
            mask=coloring,
            font_path=font,
            random_state=random_state,
            max_words=3000,
            scale=scale).generate(self.tags_sentence)
        wordCloud.recolor(color_func=image_colors)
        self.word_cloud = wordCloud
    def save_wordcloud(self, output):
        self.word_cloud.to_file(output)
    def generate_wordcloud(self, mask, output, font='C://Windows/Fonts/msyh.ttc', scale=8, top=500,
        random_state=42):
        self.extract_keywords(top)
        self.gen_wordcloud(mask, font, scale, random_state)
        self.save_wordcloud(output)
        
class Episode(object):
    def __init__(self, cid):
        self.__url_template = 'https://comment.bilibili.com/{}.xml'
        self.cid = cid
        self.comment_url = self.__url_template.format(cid)
    def crawl_danmaku(self):
        # print('\tCrawing danmaku for episode {}...'.format(self.cid))
        wb_data = requests.get(self.comment_url, headers=HEADERS)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        danmaku = soup.select('d')
        danmaku_list = DanmakuList([danmaku[i].get_text() for i in range(len(danmaku))])
        self.danmaku_list = danmaku_list
    def __str__(self):
        return 'Bilibili Episode (cid={})'.format(self.cid)

class Video(object):
    def __init__(self, aid):
        self.__url_template = 'https://www.bilibili.com/video/av{}/'
        self.aid = aid
        self.url = self.__url_template.format(aid)
        self.get_episodes()
    def get_episodes(self):
        # print('Getting episodes for video {}...'.format(self.aid))
        cids = []
        wb_data = requests.get(self.url, headers=HEADERS)
        match1 = [cid[5:-1] for cid in re.findall("cid='\d+'", wb_data.text)]
        cids.extend(match1)
        if len(match1) == 0:
            match2 = [cid[4:-1] for cid in re.findall('cid=\d+&', wb_data.text)]
            cids.extend(match2)
        cids = list(set(cids))
        episodes = [Episode(cid) for cid in cids]
        self.episodes = episodes
    def get_danmaku(self):
        # print('Getting danmaku for video {}...'.format(self.aid))
        danmaku_list = DanmakuList([])
        for episode in self.episodes:
            episode.crawl_danmaku()
            danmaku_list.extend(episode.danmaku_list)
        self.danmaku_list = danmaku_list
    def __str__(self):
        return 'Bilibili Video (aid={})'.format(self.aid)

class User(object):
    def __init__(self, mid):
        self.mid = mid
        self.__urlstr = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&pagesize=30&tid=0&page={}&order=pubdate'
        self.get_videos()
    def get_videos(self):
        def get_pages(url):
            wb_data = requests.get(url, headers=HEADERS)
            return json.loads(wb_data.text)['data']['pages']
        aids = []
        first_page = self.__urlstr.format(self.mid, 1)
        pages = get_pages(first_page)
        for page in tqdm(range(1, pages + 1), ascii=True):
            url = self.__urlstr.format(self.mid, page)
            wb_data = requests.get(url, headers=HEADERS)
            vlist = json.loads(wb_data.text)['data']['vlist']
            aids.extend([video['aid'] for video in vlist])
        videos = [Video(aid) for aid in tqdm(aids, ascii=True)]
        self.videos = videos
    def get_danmaku(self):
        danmaku_list = DanmakuList([])
        for video in tqdm(self.videos, ascii=True):
            video.get_danmaku()
            danmaku_list.extend(video.danmaku_list)
        self.danmaku_list = danmaku_list
    def __str__(self):
        return 'Bilibili User (mid={})'.format(self.mid)

class Bangumi(object):
    def __init__(self, sid):
        self.sid = sid
        self.get_profile()
        epList = self.profile['epList']
        self.aids = [ep['aid'] for ep in epList]
        self.cids = [ep['cid'] for ep in epList]
        self.episodes = [Episode(cid) for cid in self.cids]
    def get_profile(self):
        browser = webdriver.Chrome()
        browser.get("view-source:https://www.bilibili.com/bangumi/play/ss{}".format(self.sid))
        wbdata = browser.page_source
        browser.close()
        self.profile = json.loads(re.findall('\{"ver":\{.+"seasonFollowed":false\}', wbdata)[0])
    def get_danmaku(self):
        print('Getting danmaku for bangumi...')
        danmaku_list = DanmakuList([])
        for episode in tqdm(self.episodes, ascii=True):
            episode.crawl_danmaku()
            danmaku_list.extend(episode.danmaku_list)
        self.danmaku_list = danmaku_list

class Search(object):
    def __init__(self, search_type, keyword, tids_1=None):
        if not search_type in ['video', 'bangumi', 'pgc']:
            raise ValueError('search_type illegal or not implemented')
        self.search_type = search_type
        self.keyword = keyword
        self.params = {
            'search_type': search_type,
            'keyword': keyword
        }
        if tids_1 is not None:
            self.params['tids'] = tids_1
        self.__url = 'https://search.bilibili.com/api/search'
        self.compile()
    def compile(self):
        print('Compiling search results for keyword {}...'.format(self.keyword))
        def get_pages(url, params):
            wb_data = requests.get(url, params, headers=HEADERS)
            first_page = json.loads(wb_data.text)
            return first_page['numPages']
        numPages = get_pages(self.__url, self.params)
        results = []
        for page in tqdm(range(1, numPages + 1), ascii=True):
            self.params['page'] = page
            wb_data = requests.get(self.__url, self.params, headers=HEADERS)
            wb_json = json.loads(wb_data.text)['result']
            results.extend(wb_json)
        print('Got {} results in {} pages'.format(len(results), numPages))
        self.results = results
    def get_results(self):
        print('Returning results...')
        if self.search_type == 'video':
            return [Video(result['aid']) for result in tqdm(self.results, ascii=True)]
        elif self.search_type == 'bangumi' or 'pgc':
            return [Bangumi(result['sid']) for result in self.results[0]['bgmlist']]

class Topic(object):
    def __init__(self, topic_name):
        self.name = topic_name
        self.__new_feed = 'https://api.vc.bilibili.com/topic_svr/v1/topic_svr/topic_new?topic_name={}'.format(topic_name)
        self.__history_feed = 'https://api.vc.bilibili.com/topic_svr/v1/topic_svr/topic_history?topic_name={}'.format(topic_name) + '&offset_dynamic_id={}'
    def get_new_cards(self):
        print('Getting new cards...')
        new_feed_data = requests.get(self.__new_feed, headers=HEADERS)
        new_feed_data.encoding = 'utf-8'
        new_feed = json.loads(new_feed_data.text)
        new_cards = new_feed['data']['cards']
        self.new_cards = new_cards
    def get_history_cards(self):
        print('Getting history cards...')
        history_cards = []
        dynamic_id = 0
        while 1:
            feed_data = requests.get(self.__history_feed.format(dynamic_id), headers=HEADERS)
            feed_data.encoding = 'utf-8'
            feed = json.loads(feed_data.text)['data']
            history_cards.extend(feed['cards'])
            dynamic_id = feed['cards'][-1]['desc']['dynamic_id']
            print(dynamic_id)
            if feed['has_more'] == 0:
                break
        self.history_cards = history_cards
    def get_feed(self):
        self.get_new_cards()
        self.get_history_cards()
        self.cards = self.new_cards + self.history_cards
        self.cards_info = [json.loads(card['card']) for card in self.cards]
        self.cards_text = DanmakuList(sum([get_card_text(card_info) for card_info in self.cards_info], []))
        self.usernames = sum([get_user_name(card_info) for card_info in self.cards_info], [])
    
    
def get_card_text(card_info):
    text = DanmakuList([])
    if 'origin' in card_info.keys():
        text.append(card_info['item']['content'])
        text.extend(get_card_text(json.loads(card_info['origin'])))
    elif 'aid' in card_info.keys():
        text.append(card_info['title'])
        text.append(card_info['desc'])
        text.append(card_info['dynamic'])
    elif 'summary' in card_info.keys():
        text.append(card_info['title'])
        text.append(card_info['summary'])
    else:
        try:
            if 'description' in card_info['item'].keys():
                text.append(card_info['item']['description'])
            if 'content' in card_info['item'].keys():
                text.append(card_info['item']['content'])
        except Exception as e:
            print(card_info)
            raise e
    return text

def get_user_name(card_info):
    usernames = []
    if 'origin' in card_info.keys():
        usernames.extend(get_user_name(json.loads(card_info['origin'])))
    elif 'aid' in card_info.keys():
        usernames.append(card_info['owner']['name'])
    elif 'summary' in card_info.keys():
        usernames.append(card_info['author']['name'])
    else:
        if 'uname' in card_info['user'].keys():
            usernames.append(card_info['user']['uname'])
        if 'name' in card_info['user'].keys():
            usernames.append(card_info['user']['name'])
    return usernames
    


        




# if __name__ == '__main__':
#     import pickle

#     search = Search('video', 'VAN')
#     results = search.get_results()
#     danmaku_list = DanmakuList([])
#     for video in results:
#         video.get_danmaku()
#         danmaku_list.extend(video.danmaku_list)
#     print('Length of danmaku_list:', len(danmaku_list))
    
#     with open('VAN.pkl', 'wb') as f:
#         pickle.dump(danmaku_list, f)
