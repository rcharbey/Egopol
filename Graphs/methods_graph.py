import json
import gzip
from igraph import *
import os
sys.path.append('./Jsons')
import read_statuses
import numpy as np

def create_list_neighbors(graph):
    for v in graph.vs:
        v['list_neighbors'] = []
    for e in graph.es:
        if not e.source in graph.vs[e.target]['list_neighbors']:
            graph.vs[e.target]['list_neighbors'].append(e.source)
        if not e.target in graph.vs[e.source]['list_neighbors']:
            graph.vs[e.source]['list_neighbors'].append(e.target)
    for v in graph.vs:
        v['list_neighbors'].sort(reverse = True)

def degree_distribution(graph):
    result = []
    for v in graph.vs:
        result.append(v.degree())
        v['d'] = result[v.index]
    result.sort()
    return result

def degree_combination(graph):
    temp = []
    for v in graph.vs:
        temp.append(v.degree())
    result = []
    for v in graph.vs:
        result.append(v.degree())
        neighborhood = v.neighbors()
        for neighbor in neighborhood:
            result[v.index] += neighbor.degree()
        v["n_d"] = result[v.index]
    result.sort()
    return result

def export(path):
    graph = create_graph(path)
    export_file = open('graph.txt', 'w')
    export_file.write(str(len(graph.vs)))
    export_file.write(' ')
    export_file.write(str(len(graph.es)))
    export_file.write('\n')
    i = 0
    for e in graph.es:
        export_file.write(str(e.source))
        export_file.write(' ')
        export_file.write(str(e.target))
        if i != len(graph.es)-1:
            export_file.write('\n')
        i += 1

def gt_coloration(graph):
    folder = graph['folder']
    ego = graph['ego']

    path = 'GALLERY/%s/%s/Graphs/GT_graphs' % (folder, ego)
    if not os.path.isdir(path):
        os.mkdir(path)

    dico = read_statuses.gt_and_activity(folder, ego)

    palette = GradientPalette('grey', 'red', 5)
    quality = ['', 'comments', 'likes']

    for gt in dico:
        for i in range(1,3):
            current_dico = dico[gt][i]
            quintiles = np.percentile(np.array(current_dico.values()), np.arange(0, 100, 20))
            for v in graph.vs:
                value = current_dico.get(v['name'], 0)
                for threshold in quintile:
                    if value <= treshold:
                        v['color'] = palette.get(treshold)
            graph.write('%s/%s_%s.gml' % (path, gt, quality[i]), format = 'gml')













