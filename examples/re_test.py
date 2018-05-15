# import re
# from bs4 import BeautifulSoup

# s = '''<a href="https://weektalk.jin10.com/?id=104" target="_blank"><img src="https://image.jin10.com/1524464690.jpg" width="754" height="120"></a>'''
# soup = BeautifulSoup(s, 'lxml')


# p = re.compile()

# before = '<a href="'
# after = '" target="_blank">'

# m = re.match(before + '.+' + after, s)
# s = s.replace(m.group(0), m.group(0)[9:-18])

import re

##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(s):
    re_delete = {
        'script': r'<\s*?script[^>]*?>',
        '/script': r'<\s*?/\s*?script\s*?>',
        'style': r'<\s*?style[^>]*?>',
        '/style': r'<\s*?/\s*?style\s*?>',
        'a': r'<\s*?a[^>]*?>',
        '/a': r'<\s*?/\s*?a\s*?>',
        'img': r'<\s*?img[^>]*?>',
        '/img': r'<\s*?/\s*?img\s*?>',
        'font': r'<\s*?font[^>]*?>',
        '/font': r'<\s*?/\s*?font\s*?>',
    }
    re_br = {
        'br': r'<br\s*?/?>',
        '/br': r'</?\s*?br>',
    }

    for pattern in re_delete.values():
        match = re.compile(pattern)
        s = match.sub('', s)
    for pattern in re_br.values():
        match = re.compile(pattern)
        s = match.sub('\n', s)
    return s



if __name__=='__main__':
    s = '''<a href="https://weektalk.jin10.com/?id=104" target="_blank"><img src="https://image.jin10.com/1524464690.jpg" width="754" height="120"></a>'''
    news=filter_tags(s)
    print(news)

