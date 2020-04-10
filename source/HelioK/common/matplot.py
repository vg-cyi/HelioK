import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import numpy as np

colorMain = '#567CB5'
colorGrid = '#B0B0B0FF'
colorAxes = '#303030'

def lighter(c, w = 0.333):
    # blend hex color with white
    c = mcolors.hex2color(c)
    c = (1. - w)*np.array(c) + w*np.array((1., 1., 1.))
    return mcolors.rgb2hex(c)

colorList = ["#5f7590", "#90807c", "#c9945b", "#eaa958", "#f3c074", "#fcd791", "#fff2bf"]

def makeMap(colors):   
    cMap = mcolors.LinearSegmentedColormap.from_list("", colorList)
    cMap.set_under(colorList[0])
    cMap.set_over(colorList[-1])
    return cMap

cMap = makeMap(colorList)
cMapInverted = makeMap(colorList.reverse())
