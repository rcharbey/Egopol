# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:43:36 2015

@author: raphael
"""

import utilities
import os
from igraph import *

def write_figure(file_html, path_img, gt, nb_statuses, nb_qual, qual):
    if os.path.isfile(path_img):
        file_html.write('\
<figure> \n \
    <object data="%s" type="image/svg+xml"> \n \
    </object> \n \
    <figcaption> \n \
        %s %s statuts %s %s \n \
    </figcaption> \n \
</figure> \n' % (path_img, gt, nb_statuses, nb_qual, qual))

def pretty_print(folder, ego):

    path = 'GALLERY/%s/%s/Graphs/GT_Graphs' % (folder, ego)

    graphs_list = [graph for graph in os.listdir(path) if os.path.isfile(os.path.join(path,graph))]

    qualities = ['comments', 'likes']

    file_with_info = open('%s/infos.txt' % path)
    infos = []
    for line in file_with_info:
        infos.append(line[0:-1].split(' '))
    infos.sort(key=lambda gt: gt[1], reverse=True)

    with open('%s/pretty_print.html' % path, 'w') as file_html:
        utilities.print_begin(file_html)
        for gt in infos:
            print gt
            for quality in qualities:
                path_img = '%s/SVG/%s_%s.svg' % (path, gt[0], quality)
                write_figure(file_html, path_img, gt[0], gt[1], gt[2+qualities.index(quality)], quality)


