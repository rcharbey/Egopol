# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:43:36 2015

@author: raphael
"""

import utilities
import os
from igraph import *

def pretty_print(folder, ego):

    path = 'GALLERY/%s/%s/Graphs/GT_Graphs' % (folder, ego)

    graphs_list = [graph for graph in os.listdir(path) if os.path.isfile(os.path.join(path,graph))]

    qualities = ['comments', 'likes']

    file_with_info = open('%s/infos.txt' % path)
    infos = []
    for line in file_with_info:
        info.append(line.split(' '))
    info.sort(key=lambda gt: gt[1], reverse=True)

    with open('%s/pretty_print.html' % path, 'w') as file_html:
        utilities.print_begin(file_html)
        for gt in infos:
            for quality in qualities:
                path_img = '%s/SVG/%s_%s.svg' % (path, gt[0], quality)
                if os.path.isfile(path_img):
                    file_html.write('<figure><img src="%s" width="70" height = "70" alt="image /><figcaption>%s %s statuts %s %s</figcaption>' \
                                    % (path_img, gt[0], gt[1], gt[2+[qualities.index[quality]]], quality))


