# -*- coding: utf-8 -*-
import numpy as np
import os
import csv
from matplotlib.mlab import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

import argparse
parser = argparse.ArgumentParser(description="main")
parser.add_argument('d', help="number of dimensions")
parser.add_argument('quality', help="patterns or positions")
args = parser.parse_args()

def read_enumeration(path, quality):
    file_to_read = path+'Enumeration/CSV/proportion_'+quality+'_friends.csv'
    reader = csv.reader(open(file_to_read, 'rb'), delimiter=';')
    result = []
    for line in reader:
        result.append(line)
        break
    return [float(x) for x in result[0]]

def pick_all_data(quality):
    temp = []
    noms = []
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders:
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            if os.path.isfile('GALLERY/'+folder+'/'+ego+'/Enumeration/CSV/proportion_'+quality+'_friends.csv'):
                temp.append(read_enumeration('GALLERY/'+folder+'/'+ego+'/', quality))
                noms.append((folder, ego))
    return temp, noms 

def pca(data):
    data_pca = np.array(data)
    try:
        results = PCA(data_pca)
    except:
        raise

    somme = 0
    for variance in results.fracs:
        somme += round(variance*100,1)
        print str(somme) + '% ',

    x = []
    y = []
    z = []
    for item in results.Y:
        x.append(item[0])
        y.append(item[1])
        z.append(item[2])
        
    pltData = [x,y,z]
    return pltData

def plot_3D(pltData):
    fig1 = plt.figure() # Make a plotting figure
    ax = Axes3D(fig1) # use the plotting figure to create a Axis3D object.
    ax.scatter(pltData[0], pltData[1], pltData[2], 'bo') # make a scatter plot of blue dots from the data

    # make simple, bare axis lines through space:
    xAxisLine = ((min(pltData[0]), max(pltData[0])), (0, 0), (0,0)) # 2 points make the x-axis line at the data extrema along x-axis 
    ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r') # make a red line for the x-axis.
    yAxisLine = ((0, 0), (min(pltData[1]), max(pltData[1])), (0,0)) # 2 points make the y-axis line at the data extrema along y-axis
    ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r') # make a red line for the y-axis.
    zAxisLine = ((0, 0), (0,0), (min(pltData[2]), max(pltData[2]))) # 2 points make the z-axis line at the data extrema along z-axis
    ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r') # make a red line for the z-axis.

    plt.show() # show the plot
    
def plot_2D(pltData):
    fig, ax = plt.subplots()
    ax.scatter(pltData[0], pltData[1])

    plt.show()
    
def main():
    data, noms = pick_all_data(args.quality)
    pltData = pca(data)
    if args.d == '3D':
        plot_3D(pltData)
    else:
        plot_2D(pltData[0:2])
        
main()

                