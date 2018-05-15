from bilibili import *
from pyecharts import Bar

unn = Bangumi(24053)

# grid = Grid()
lengths = []
for num, ep in enumerate(unn.episodes):
    ep.crawl_danmaku()
    danmaku_list = ep.danmaku_list
    lengths.append(len(danmaku_list))
    danmaku_list.extract_keywords_with_weight(20)
    tags = danmaku_list.tags
    attr, values = zip(*tags)
    values = [round(value * 100, 2) for value in values]
    bar = Bar('UNNATURAL弹幕词频分析', 'by @MiracleXYZ')
    bar.add('第{}话'.format(num), attr, values, xaxis_interval=0)
    bar.render('images/unnatural/第{}话.html'.format(num))
    # grid.add(bar)

bar = Bar('UNNATURAL弹幕数量', 'by @MiracleXYZ')
bar.add('弹幕数量', list(range(11)), lengths, xaxis_interval=0)
bar.render('./images/unnatural/lengths.html')

# grid.render('images/unnatural/unnatural.html')



