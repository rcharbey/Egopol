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

    palette = ['blue', 'cyan1', 'cyan2', 'cyan3', 'cyan4']
    quality = ['', '', '', 'comments', 'likes']

    file_with_info = open('%s/infos.txt' % path, 'w')

    lists_all = [[], []]
    for gt in dico:
        print gt
        for i in range(3,5):
            lists_all[i-3].append(gt[i])
    quintiles_all = []
    for i in range(0,2):
        print lists_all[i]
        quintiles_all.append([np.percentile(lists_all[i], x) for x in [20, 40, 60, 80, 100]])

    for gt in dico:
        for i in range(3,5):
            current_dico = dico[gt][i]
            if dico[gt][i-2] < 5:
                continue
            for v in graph.vs:
                value = current_dico.get(v['name'], 0)
                if int(value) == 0:
                    v['color'] = 'white'
                    continue
                for threshold in quintiles:
                    if value <= threshold:
                        v['color'] = palette[quintiles_all[i-3].index(threshold)]
                        continue
            graph.write('%s/%s_%s.gml' % (path, gt, quality[i]), format = 'gml')
        file_with_info.write('%s %s %s %s\n' % (gt, dico[gt][0], dico[gt][1], dico[gt][2]))

def display_gt_coloration(folder, ego):
    path = 'GALLERY/%s/%s/Graphs/GT_Graphs' % (folder, ego)
    graphs_list = [graph for graph in os.listdir(path) if (os.path.isfile(os.path.join(path,graph)) and '.gml' in graph)]
    for graph_path in graphs_list:
        graph = Graph.Read_GML('%s/%s' % (path,graph_path))
        for v in graph.vs:
            v['size'] = 5*math.log(2+v.degree())
        graph.es['curved'] = 0.3
        layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)
        place = '%s/SVG/%s.svg' % (path, graph_path[0:-4])
        plot(graph, place, layout = layout, vertex_color = [v['color'] for v in graph.vs])













