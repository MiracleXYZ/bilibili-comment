from bilibili import *

dragonMaid = Bangumi('bangumi_test.json')
dragonMaid.get_danmaku()
danmaku = dragonMaid.danmaku_list

danmaku.generate_wordcloud('images/kanna/kanna03.jpg', 'images/kanna/kannawc2.png', scale=4, random_state=50)
danmaku.generate_wordcloud('images/kanna/kanna04.jpg', 'images/kanna/kannawc3.png', scale=4, random_state=50)