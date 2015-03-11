# -*- coding: utf-8 -*-
import numpy as np
import os
import csv
from matplotlib.mlab import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from numpy import corrcoef, sum, log, arange
from pylab import pcolor, show, colorbar, xticks, yticks
import pylab

import argparse
parser = argparse.ArgumentParser(description="main")
parser.add_argument('d', help="number of dimensions")
parser.add_argument('quality', help="patterns or positions")
parser.add_argument('--options', '-o', nargs='+')
args = parser.parse_args()

def read_enumeration(path, param):
    file_to_read = path+'Enumeration/CSV/'+param['prop']+param['quality']+'_friends.csv'
    reader = csv.reader(open(file_to_read, 'rb'), delimiter=';')
    
    temp = []
    for line in reader:
        temp.append(line)
        if param['quality'] == 'patterns':
            break
    
    temp_2 = []
    
    if param['restriction'] == '3_':
        if param['quality'] == 'patterns':
            temp_2.append(temp[0][1:3])
        else:
            for vector in temp:
                temp_2.append(vector[1:5])
    elif param['restriction'] == '4_':
        if param['quality'] == 'patterns':
            temp_2.append(temp[0][3:9])
        else:
            for vector in temp:
                temp_2.append(vector[4:15])
    elif param['restriction'] == '5_':
        if param['quality'] == 'patterns':
            temp_2.append(temp[0][9:30])
        else:
            for vector in temp:
                temp_2.append(vector[15:73])
    else:
        temp_2 = temp
            
    result = []
    for vector in temp_2:
        result.append([float(x) for x in vector])
    
    return result

def create_blocs(param):
    file_blocs = open('GALLERY/General/Percentiles/'+param['prop']+param['quality']+'.csv', 'rb')
    csv_blocs = csv.reader(file_blocs, delimiter = ';')
    
    stats = []
    for row in csv_blocs:
        if param['number'] == '_quartiles':
            stats.append([row[4], row[9], row[14]])
        elif param['number'] == '_quintiles':
            stats.append([row[3], row[7], row[11], row[15]])
        else:
            stats.append([row[1], row[3], row[5], row[7], row[9], row[11], row[13], row[15], row[17]])
    file_blocs.close()
    return stats

def value_to_bloc(enumeration, stats, i):
    found = False
    for decile in range(len(stats[i])):
        if enumeration[i] < float(stats[i][decile]):
            enumeration[i] = decile + 1
            found = True
            break
    if found == False:
        enumeration[i] = len(stats[i])+1

def pick_all_data(param):
    temp = []
    noms = []
    
    if param['number'] != '':
        stats = create_blocs(param)
    
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders:
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            if os.path.isfile('GALLERY/'+folder+'/'+ego+'/Enumeration/CSV/'+param['prop']+param['quality']+'_friends.csv'):
                enumeration = read_enumeration('GALLERY/'+folder+'/'+ego+'/', param)
                for vector in enumeration:
                    if param['number'] != '':
                        for i in range(len(vector)):
                            value_to_bloc(vector, stats, i)
                    temp.append(vector)
                noms.append((folder, ego))
    return temp, noms 

def pca(data, file_to_write):
    data_pca = np.array(data)
    try:
        results = PCA(data_pca)
    except:
        raise

    file = open(file_to_write, 'w')
    somme = 0
    for variance in results.fracs:
        somme += round(variance*100,1)
        file.write(str(somme) + '% ')
    file.close()

    x = []
    y = []
    z = []
    for item in results.Y:
        x.append(item[0])
        y.append(item[1])
        z.append(item[2])
        
    pltData = [x,y,z]
    return pltData

def plot_3D(pltData, param):
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
    
def plot_2D(pltData, param):
    fig, ax = plt.subplots()
    ax.scatter(pltData[0], pltData[1])
    
    # make simple, bare axis lines through space:
    xAxisLine = ((min(pltData[0]), max(pltData[0])), (0, 0)) # 2 points make the x-axis line at the data extrema along x-axis 
    ax.plot(xAxisLine[0], xAxisLine[1], 'r') # make a red line for the x-axis.
    yAxisLine = ((0, 0), (min(pltData[1]), max(pltData[1]))) # 2 points make the y-axis line at the data extrema along y-axis
    ax.plot(yAxisLine[0], yAxisLine[1], 'r') # make a red line for the y-axis.

    plt.savefig('GALLERY/General/PCA/'+param['restriction']+param['prop']+param['quality']+param['number']+'.svg', bbox_inches='tight')
    print 'GALLERY/General/PCA/'+param['restriction']+param['prop']+param['quality']+param['number']+'.svg'
    #plt.show()
    
def create_param():
    param = {'prop' : '', 'number' : '', 'restriction' : ''}
    
    param['dimension'] = args.d
    param['quality'] = args.quality
    
    if args.options != None:
        if 'prop' in args.options:
            param['prop'] = 'proportion_'
        if 'quartiles' in args.options:
            param['number'] = '_quartiles'
        elif 'quintiles' in args.options:
            param['number'] = '_quintiles'
        elif 'deciles' in args.options:
            param['number'] = '_deciles'
        if 'l3' in args.options:
            param['restriction'] = '3_'
        elif 'l4' in args.options:
            param['restriction'] = '4_'
        elif 'l5' in args.options:
            param['restriction'] = '5_'
    
    return param
    
def main():
    param = create_param()
    print param
    print args
    file_to_delete = 'GALLERY/General/Aggregations/all_'+param['restriction']+param['prop']+param['quality']+'_friends.csv'
    if os.path.isfile(file_to_delete):
        os.remove(file_to_delete)
    
    data, noms = pick_all_data(param)
    
    data_kmean = np.array(data)
    data_kmean.transpose()
    
    R = corrcoef(data_kmean)
    pcolor(R)
    #colorbar()
    #yticks(arange(0.5,10.5),range(0,10))
    #xticks(arange(0.5,10.5),range(0,10))
    pylab.savefig('GALLERY/General/PCA/'+param['restriction']+param['prop']+param['quality']+param['number']+'.png')
    
    file_to_write = 'GALLERY/General/Aggregations/all_'+param['restriction']+param['prop']+param['quality']+param['number']+'_friends'
    writer = csv.writer(open(file_to_write+'.csv', 'wb'), delimiter = ';')
    for line in data:
        writer.writerow(line)
    print file_to_write
       
    file_to_write = 'GALLERY/General/PCA/'+param['restriction']+param['prop']+param['quality']+param['number']+'_variance.txt'
    pltData = pca(data, file_to_write)    
    
    if param['dimension'] == '3D':
        plot_3D(pltData, param)
    else:
        plot_2D(pltData[0:2], param)
        
    os.system('Rscript pca.R '+param['restriction']+param['prop']+param['quality']+param['number'])

        
main()

                