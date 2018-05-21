import os,sys 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0, parentdir)  
from bilibili import *
from pyecharts import Bar
import jieba
import jieba.analyse

jieba.analyse.set_stop_words('./stop_words.txt')

unn = Bangumi(24053)
unn.get_danmaku()

danmaku_list = unn.danmaku_list
danmaku_list.generate_wordcloud('./images/unnatural/mask.jpg', './images/unnatural/unnatural_no_stop_2.png')

danmaku_list.extract_keywords_with_weight(20)
tags = danmaku_list.tags
attr, values = zip(*tags)
values = [round(value * 100, 2) for value in values]
bar = Bar('UNNATURAL弹幕词频分析', 'by @MiracleXYZ')
bar.add('UNNATURAL', attr, values, xaxis_interval=0)
bar.render('./images/unnatural/unnatural_no_stop_html.png')