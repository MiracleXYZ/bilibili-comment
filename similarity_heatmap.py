from pyecharts import HeatMap
import pandas as pd
import numpy as np

sim_frame = pd.read_csv('./data/philosophy.csv', index_col=0, encoding='utf8')
names = list(sim_frame.index)
data_array = np.round(np.array(sim_frame) ** 0.25 * 100, 0).astype(int)
x_len, y_len = data_array.shape
data = [[i, j, data_array[i][j]] for i in range(x_len) for j in range(y_len)]

x_axis = names
y_axis = names

heatmap = HeatMap(title='哲学', subtitle='by @MiracleXYZ')
heatmap.add(
    "相似度矩阵", x_axis, y_axis, data, is_visualmap=True,
    visual_text_color="#000", visual_orient='vertical',
    visual_range=[0, 100],
    visual_range_text=['低', '高'],
    visual_pos='left',
    label_pos='inside'
    )
    
heatmap.render('./data/philosophy_heatmap.html')

