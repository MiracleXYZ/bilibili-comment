from bilibili import *
import pickle

with open('VAN.pkl', 'rb') as f:
    danmaku_list = pickle.load(f)

print(len(danmaku_list))
danmaku_list.generate_wordcloud('./images/VANprofile.jpg', './images/VANoutput.png')