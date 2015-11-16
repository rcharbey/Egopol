# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:43:36 2015

@author: raphael
"""

import utilities
import os
from igraph import *

def write_figure(file_html, path_img, gt, nb_statuses, nb_qual, qual):
    file_html.write('\
<figure> \n \
    <img src="%s" widht="200" height="200"> \n \
    <figcaption> \n \
        %s<br> %s statuts<br> %s %s \n \
    </figcaption> \n \
</figure>' % (path_img, gt, nb_statuses, nb_qual, qual))

def pretty_print(folder, ego):

    path = 'GALLERY/%s/%s/Graphs/GT_Graphs' % (folder, ego)

    qualities = ['comments', 'likes']

    file_with_info = open('%s/infos.txt' % path)
    infos = []
    for line in file_with_info:
        infos.append(line[0:-1].split(' '))
    infos.sort(key=lambda gt: int(gt[1]), reverse=True)

    with open('%s/pretty_print.html' % path, 'w') as file_html:
        utilities.print_begin(file_html)
        for gt in infos:
            for quality in qualities:
                path_img = 'SVG/%s_%s.svg' % (gt[0], quality)
                if os.path.isfile(path+'/'+path_img):
                    write_figure(file_html, path_img, gt[0], gt[1], gt[2+qualities.index(quality)], quality)


