from pyecharts import Graph
import pandas as pd

sim_frame = pd.read_csv('./data/philosophy.csv', index_col=0, encoding='utf8')
names = sim_frame.index
sim_frame = sim_frame ** 0.25

graph = Graph('哲♂学关系图', width=1000, height=1000)
nodes = [{'name': name, 'symbolSize': 30, 'value': 1} for name in names]
links = [{
    'source': i,
    'target': j,
    'value': sim_frame.loc[i, j]
} for i in names for j in names if i < j]
graph.add(
    '', nodes, links,
    is_focusnode=True,
    is_roam=True,
    is_rotatelabel=False,
    layout="force",
    graph_edge_length=list(range(100, 601, 100)),
    graph_gravity=0.1,
    graph_repulsion=8000,
    is_label_show=True,
    is_legend_show=True,
    line_curve=0,
)
graph.render('./data/philosophy.html')

