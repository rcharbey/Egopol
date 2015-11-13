import json
import gzip
from igraph import *
import os
sys.path.append('./Jsons')
import read_statuses
import numpy as np
import friends
from igraph.drawing import colors

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

    palette = GradientPalette('grey', 'red', 6)
    quality = ['', 'comments', 'likes']

    for gt in dico:
        for i in range(1,3):
            current_dico = dico[gt][i]
            quintiles = [np.percentile(np.array(current_dico.values()), x) for x in [25, 40, 50, 60, 80, 100]]
            for v in graph.vs:
                value = current_dico.get(v['name'], 0)
                for threshold in quintiles:
                    if value <= threshold:
                        v['color'] = known_colors[palette._get(threshold)]
            graph.write('%s/%s_%s.gml' % (path, gt, quality[i]), format = 'gml')

def display_gt_coloration(folder, ego):
    path = 'GALLERY/%s/%s/Graphs/GT_Graphs' % (folder, ego)
    graphs_list = [graph for graph in os.listdir(path) if os.path.isfile(os.path.join(path,graph))]
    for graph_path in graphs_list:
        graph = friends.import_graph(folder, ego, 'gml')
        graph.es['curved'] = 0.3
        layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)
        place = '%s/%s.svg' % (path, graph_path[0:-4])
        plot(graph, place, layout = layout)













