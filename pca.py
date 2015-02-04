# -*- coding: utf-8 -*-
import mdp
import numpy as np
import os
import csv

def read_enumeration(path):
    file_to_read = path+'Enumeration/CSV/patterns_friends.csv'
    reader = csv.reader(open(file_to_read, 'rb'), delimiter=';')
    result = []
    for line in reader:
        result.append(line)
        break
    return [float(x) for x in result[0]]

def pick_all_data():
    result = []
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders:
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            if os.path.isfile('GALLERY/'+folder+'/'+ego+'/Enumeration/CSV/patterns_friends.csv'):
                result.append(read_enumeration('GALLERY/'+folder+'/'+ego+'/'))
    return result

data = pick_all_data()
np_data = np.array(data)
principal_components = mdp.pca(np_data)
writer = csv.writer(open('GALLERY/pca.txt', 'wb'), delimiter = ' ')
for vector in principal_components:
    writer.writerow(vector)
                