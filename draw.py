# -*- coding: utf-8 -*-
import pylab
import random
import numpy as np
import sys


class MiniPlotTool :
    '''
    A mini tool to draw lines using pylab
    '''
    basecolors = ['red','green','yellow','blue','black','cyan','magenta']

    def __init__(self, baseConfig) :
        self.figsize = baseConfig.get('figsize',None)
        self.axis = baseConfig.get('axis',None)
        self.title = baseConfig.get('title','NoName')
        self.ylabel = baseConfig.get('ylabel','NoName')
        self.grid = baseConfig.get('grid',False)
        self.xaxis_locator = baseConfig.get('xaxis_locator',None)
        self.yaxis_locator = baseConfig.get('yaxis_locator',None)
        self.legend_loc = baseConfig.get('legend_loc',0)
        
        if self.figsize != None :
            pylab.figure(figsize = self.figsize)
        if self.axis != None :
            pylab.axis(self.axis)
        
        pylab.title(self.title)
        pylab.ylabel(self.ylabel)
        ax = pylab.gca()
        pylab.grid(self.grid)
        if self.xaxis_locator != None :
            ax.xaxis.set_major_locator( pylab.MultipleLocator(self.xaxis_locator) )
        if self.yaxis_locator != None :
            ax.yaxis.set_major_locator( pylab.MultipleLocator(self.yaxis_locator) )
        self.lineList = []
        self.id = 1

    def addline(self, lineConf) :
        self.lineList.append((self.id, lineConf))
        self.id += 1
        return {'id' : self.id - 1}

    def removeline(self, lineId) :
        for i in range(len(self.lineList)) :
            id, conf = self.lineList[i]
            if id == lineId :
                del self.lineList[i]
                break
        else :
            return {'status' : -1}
        print len(self.lineList)
        return {'status' : 0}

    def __parselineConf(self, lineConf) :
        X = lineConf['X']
        Y = lineConf['Y']
        marker = lineConf.get('marker',None)
        color = lineConf.get('color', random.choice(MiniPlotTool.basecolors))
        markerfacecolor = lineConf.get('markerfacecolor',color)
        label = lineConf.get('label','QXC')
        linewidth = lineConf.get('linewidth',1)
        linestyle = lineConf.get('linestyle','-')
        return X, Y, marker, color, markerfacecolor, label, linewidth, linestyle

    def plotSingleLine(self, lineConf):
        X, Y, marker, color, markerfacecolor, label, linewidth, linestyle = self.__parselineConf(lineConf)
        pylab.plot(X, Y, marker = marker, color = color, markerfacecolor = markerfacecolor, label=label, linewidth = linewidth, linestyle = linestyle)
        pylab.legend(loc = self.legend_loc)

    def plot(self) :
        colors = [MiniPlotTool.basecolors[i % len(MiniPlotTool.basecolors)] for i in range(len(self.lineList))]
        for i in range(len(self.lineList)) :
            id, conf = self.lineList[i]
            if conf.get('color',None) :
                conf['color'] = colors[i]
            X, Y, marker, color, markerfacecolor, label, linewidth, linestyle = self.__parselineConf(conf)
            pylab.plot(X, Y, marker = marker, color = color, markerfacecolor = markerfacecolor, label=label, linewidth = linewidth, linestyle = linestyle)
        pylab.legend(loc = self.legend_loc)

    def show(self) :
        pylab.show()

        
if __name__ == '__main__' :
    #test
    index = sys.argv[2]
    baseConfig = {
        #'figsize' : (6,8),
        #'axis': [0,10,0,10],
        #'title' : 'hello title',
        #'ylabel' : 'hello ylabel',
        'grid' : True,
        #'xaxis_locator' : 0.5,
        #'yaxis_locator' : 1,
        #'legend_loc' : 'upper right'
    }
    tool = MiniPlotTool(baseConfig)
    line= np.loadtxt(sys.argv[1], usecols=(int(index),), unpack=True)
    
    X = [ i for i in range(len(line))]
    #Y = [random.randint(1,10) for i in range(10)]
    Y = line
    Y2 = range(len(line))
    y2 = 4
    j = 0
    for y in Y:
        if y > 4:
            step = 1
        else:
            step = -1
        y2 += step
        Y2[j] = y2
        j +=1
    #Y2 = [random.randint(1,10) for i in range(10)]
    print "Y:", Y
    print "Y2:", Y2
    lineConf = {
        'X' : X,
        'Y' : Y,
        #'marker' : 'x',
        #'color' : 'b',
        #'markerfacecolor' : 'r',
        'label' : index,
        #'linewidth' : 3,
        #'linestyle' : '--'
    }
    lineConf2 = {
        'X' : X,
        'Y' : Y2,
        'marker' : 'o',
        'color' : 'b',
        'markerfacecolor' : 'r',
        'label' : '222',
        'linewidth' : 3,
        'linestyle' : '--'
    }
    #tool.plotSingleLine(lineConf)
    print tool.addline(lineConf)
    print tool.addline(lineConf2)

    #print tool.removeline(1)
    tool.plot()
    tool.show()
