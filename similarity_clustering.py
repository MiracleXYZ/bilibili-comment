import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from sklearn import cluster, covariance, manifold
from matplotlib import animation
from matplotlib.colors import Normalize

import warnings
warnings.filterwarnings('ignore')

# sim_frame = pd.read_csv('./data/philosophy.csv', index_col=0, encoding='utf8')
# names = sim_frame.index
# covariance_ = np.array(sim_frame) ** 0.45
theme = 'vocaloid'

dataset = pd.read_csv('./data/{}_dataset.csv'.format(theme), index_col=0, encoding='utf8')
names = dataset.index

for name in names:
    if (dataset.loc[name] == 0).all():
        dataset = dataset.drop(name, axis=0)
names = dataset.index


edge_model = covariance.GraphLassoCV()
X = dataset.copy().T
X /= X.std(axis=0)
edge_model.fit(X)

_, labels = cluster.affinity_propagation(edge_model.covariance_)
n_labels = labels.max()

names = np.array(names)
codes = np.array(names)

for i in range(n_labels + 1):
    print('Cluster %i: %s' % ((i + 1), ', '.join(names[labels == i])))

# np.random.seed(124)
# embedding = np.random.randn(2, len(names))

# def generate_polygons(num, center=False):
#     polynum = num - 1 if center else num
#     coords = [(0, 0)] if center else []
#     angle = 2 * np.pi / polynum
#     for i in range(polynum):
#         coords.append((np.cos(i * angle), np.sin(i * angle)))
#     xs, ys = zip(*coords)
#     embedding = np.zeros((2, num))
#     embedding[0, :], embedding[1, :] = xs, ys
#     return embedding
    
# embedding = generate_polygons(len(names))
# for n_neighbors in [1, 2, 3, 4, 5, 6, 10]:
animation = False
for n_neighbors in [1, 2, 3, 4, 5, 6, 10]:

    node_position_model = manifold.LocallyLinearEmbedding(
        n_components=2, eigen_solver='dense', n_neighbors=n_neighbors)

    embedding = node_position_model.fit_transform(X.T).T

    # Display a graph of the partial correlations
    partial_correlations = edge_model.precision_.copy()
    d = 1 / np.sqrt(np.diag(partial_correlations))
    partial_correlations *= d
    partial_correlations *= d[:, np.newaxis]
    non_zero = (np.abs(np.triu(partial_correlations, k=1)) > 0.01)

    # Plot the edges
    start_idx, end_idx = np.where(non_zero)
    # a sequence of (*line0*, *line1*, *line2*), where::
    #            linen = (x0, y0), (x1, y1), ... (xm, ym)
    segments = [[embedding[:, start], embedding[:, stop]]
                for start, stop in zip(start_idx, end_idx)]
    values = np.abs(partial_correlations[non_zero])

    text_positions = np.array([])
    for index, (name, label, (x, y)) in enumerate(
            zip(names, labels, embedding.T)):
        dx = x - embedding[0]
        dx[index] = 1
        dy = y - embedding[1]
        dy[index] = 1
        this_dx = dx[np.argmin(np.abs(dy))]
        this_dy = dy[np.argmin(np.abs(dx))]
        if this_dx > 0:
            horizontalalignment = 'left'
            x = x + .002
        else:
            horizontalalignment = 'right'
            x = x - .002
        if this_dy > 0:
            verticalalignment = 'bottom'
            y = y + .002
        else:
            verticalalignment = 'top'
            y = y - .002
        text_positions = np.append(text_positions, dict(
            x=x, y=y, s=name, size=10,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            bbox=dict(
                    facecolor='w',
                    edgecolor=plt.cm.spectral(label / float(n_labels)),
                    alpha=.6
            )
        ))




    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    ## Visualization
    fig = plt.figure(1, facecolor='w', figsize=(10, 8), dpi=200)
    plt.clf()
    ax = plt.axes([0., 0., 1., 1.])
    plt.axis('off')
    plt.xlim(embedding[0].min() - .15 * embedding[0].ptp(),
            embedding[0].max() + .10 * embedding[0].ptp(),)
    plt.ylim(embedding[1].min() - .03 * embedding[1].ptp(),
            embedding[1].max() + .03 * embedding[1].ptp())

    lc = LineCollection(segments,
                        zorder=0, cmap=plt.cm.hot_r,
                        norm=plt.Normalize(0, .7 * values.max()))
    lc.set_array(values)
    lc.set_linewidths(0.15 / values)
    ax.add_collection(lc)


    if animation:
        sca = ax.scatter([], [], cmap=plt.cm.spectral)
        texts = []

        def init():
            sca.set_offsets([])
            return sca, tuple(texts)

        def animate(i):
            x = embedding[0][labels <= i]
            y = embedding[1][labels <= i]
            s = 100 * d[labels <= i] ** 2
            c = labels[labels <= i]
            sca.set_offsets(np.c_[x, y])
            sca.set_sizes(s)
            sca.set_color(plt.cm.spectral(c / n_labels))

            for text_position in text_positions[labels == i]:
                text = plt.text(**text_position)
                texts.append(text)
            return sca, tuple(texts)

        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(labels), repeat=False, interval=500)
        anim.save('data/{}_{}.mp4'.format(theme, n_neighbors), fps=2, extra_args=['-vcodec', 'libx264'])
    else:
        plt.scatter(embedding[0], embedding[1], s=100 * d ** 2, c=labels, cmap=plt.cm.spectral)
        for text_position in text_positions:
            plt.text(**text_position)
        plt.savefig('data/{}_{}.png'.format(theme, n_neighbors))

    # anim.save('kichiku_{}.gif'.format(n_neighbors), writer='imagemagick')

    # plt.show()
