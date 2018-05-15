import jieba
import jieba.analyse
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import re

def jieba_cut(sentence):
    seg = jieba.cut(sentence, cut_all=True)
    segList = []
    for i in seg:
        segList.append((i))
    return segList

def plain_comment(input, output):
    f = open(input, "r", encoding='UTF-8')
    f2 = open(output, "w", encoding='UTF-8')
    count = 0
    dr = re.compile(r'<[^>]+>', re.S)
    while 1:
        line = f.readline()
        if not line:
            break
        pass
        dd = dr.sub('', line)
        count = count + 1
        f2.writelines(dd)
    print(count)

def gen_wordcloud(input, output, mask, font='C://Windows/Fonts/msyh.ttc'):
    '''
    Generate word cloud using the parameters given.
    :param input_path: File path of the original text.
    :param output: File path of the output picture. (.png)
    :param mask: File path of the mask (background picture).
    :param font: FIle path of font. (Default: Microsoft YaHei)
    :return: Generate a file named 'output'.
    '''
    with open(input, 'r', encoding='UTF-8') as file:
        text = file.read()

    segList = jieba_cut(text)
    sentence = ' '.join(segList)

    tags = jieba.analyse.extract_tags(sentence, 1000)
    tags_sentence = ' '.join(tags)

    vs_coloring = plt.imread((mask))
    image_colors = ImageColorGenerator(vs_coloring)
    wordCloud = WordCloud(background_color="white",
                          mask = vs_coloring,
                          font_path = font,
                          random_state=50,
                          max_words=3000,
                          scale=8).generate(tags_sentence)
    plt.imshow(wordCloud.recolor(color_func=image_colors))
    plt.axis("off")
    plt.show()
    wordCloud.to_file(output)

def generate_wordcloud(input, output, mask):
    plain = input[:-4] + '_temp.txt'
    plain_comment(input, plain)
    gen_wordcloud(plain, output, mask)




