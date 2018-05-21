from bilibili import Topic
from collections import Counter
import pandas as pd
from pyecharts import Bar
import json
import textwrap

topic = Topic('CP22')
topic.get_feed()

with open('cards.json', 'w', encoding='utf8') as f:
    json.dump(topic.cards, f)

with open('cards_info.json', 'w', encoding='utf8') as f:
    json.dump(topic.cards_info, f)

with open('cards_text.json', 'w', encoding='utf8') as f:
    json.dump(topic.cards_text, f)

topic.cards_text.generate_wordcloud('./images/bilibili22_update.jpg', './images/CP22.png')
usercount = pd.Series(Counter(topic.usernames))
usercount.name = 'count'
usercount = usercount.sort_values(ascending=False)
# usercount.to_csv('usercount_CP22.csv', encoding='utf8')

usercount_head = usercount.head(10)
attr = list(usercount_head.index)
attr = [textwrap.fill(name, width=4) for name in attr]
values = list(usercount_head.values)
bar = Bar('用户发表动态数量 - #{}'.format('CP22'), 'by @MiracleXYZ')
bar.add('CP22', attr, values, xaxis_interval=0, is_legend_show=False)
bar.render('./usercount.html')
try:
    bar.render('./usercount.png')
except Exception as e:
    print(e)



# with open('cards_info.json', 'w') as f:
#     json.dump(topic.cards_info, f)
# print(len(topic.new_cards))
# print(len(topic.history_cards))

# topic.get_new_cards()
# cards = topic.new_cards

