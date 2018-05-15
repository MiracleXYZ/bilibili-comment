import matplotlib.colors as col
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class DrawPcolor(object):
    def __init__(self):
        ##self define the colorbar
        startcolor = '#006400'  # a dark green 
        midcolor = '#ffffff'    # a bright white
        endcolor = '#ee0000'    # a dark red
        self.Mycmap = col.LinearSegmentedColormap.from_list('MyColorbar',[startcolor,midcolor,endcolor])#use the "fromList() method

    def Pcolor(self, *args, **kwargs):
        #*args is a tuple,**kwargs is a dict;
        #Here args means the Matrix Corr, kwargs includes the key of the " AddText function"
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot(111)   
        self.Data = args[0]
        heatmap = self.ax.pcolor(self.Data,cmap=self.Mycmap);#cmap=plt.cm.Reds)
        self.fig.colorbar(heatmap)
        # want a more natural, table-like display
        self.ax.invert_yaxis()
        self.ax.xaxis.tick_top()
        self.ax.set_xticks(np.arange(self.Data.shape[0]) + 0.5, minor=False)
        self.ax.set_yticks(np.arange(self.Data.shape[1]) + 0.5, minor=False)
        
        if kwargs['AddText']==True:
            for y in range(self.Data.shape[1]):
                for x in range(self.Data.shape[0]):
                    self.ax.text(x + 0.5, y + 0.5, '%.2f' % self.Data[y, x],
                             horizontalalignment='center',
                             verticalalignment='center',
                             )
        self.fig.show()

    def Set_labelticks(self,*tick_labels):
        # put the major ticks at the middle of each cell
        self.ax.set_xticklabels(tick_labels[0],rotation=0, minor=False) 
        self.ax.set_yticklabels(tick_labels[1],rotation=0, minor=False ) 
        self.fig.show()

def Main():
    sim_frame = pd.read_csv('./data/philosophy.csv', index_col=0, encoding='utf8')
    names = sim_frame.index
    xlabel_ticks = names
    ylabel_ticks = names
    MyPict = DrawPcolor()
    MyPict.Pcolor(np.array(sim_frame), 3, 4, 4, AddText=True, b=1) # params 3,4,4,b has no effect on the exec
    MyPict.Set_labelticks(xlabel_ticks, ylabel_ticks)
    plt.savefig('data/philosophy.pdf')


if __name__=='__main__':
    Main()