import json
import gzip
from igraph import *
import os
import read_statuses
import numpy as np
from igraph.drawing import colors
import re

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

def gt_coloration(graph, dico):
    folder = graph['folder']
    ego = graph['ego']

    path = 'GALLERY/%s/%s/Graphs/GT_graphs' % (folder, ego)
    if not os.path.isdir(path):
        os.mkdir(path)

    palette = ['cyan1', 'cyan2', 'cyan3', 'cyan4']
    quality = ['', '', '', 'comments', 'likes']

    file_with_info = open('%s/infos.txt' % path, 'w')

    lists_all = [[], []]
    for gt in dico:
        for i in range(3,5):
            lists_all[i-3].extend([value for value in dico[gt][i].values() if value > 1])
    quintiles_all = []
    for i in range(0,2):
        quintiles_all.append([np.percentile(lists_all[i], x) for x in [25, 50, 75, 100]])

    for gt in dico:
        for i in range(3,5):
            current_dico = dico[gt][i]
            if dico[gt][i-2] < 5:
                continue
            for v in graph.vs:
                v['color'] = 'white'
                value = current_dico.get(v['name'], 0)
                if int(value) == 0:
                    continue
                if int(value) == 1:
                    v['color'] = 'lightcyan'
                    continue
                for threshold in quintiles_all[i-3]:
                    if value <= threshold:
                        v['color'] = palette[quintiles_all[i-3].index(threshold)]
                        break
            if gt == 'App/Jeux':
                graph.write('%s/App_Jeux_%s.gml' % (path, quality[i]), format = 'gml')
            else:
                graph.write('%s/%s_%s.gml' % (path, re.escape(gt), quality[i]), format = 'gml')

        file_with_info.write('%s %s %s %s %s %s\n' % (gt, dico[gt][0], dico[gt][1], dico[gt][2], dico[gt][5], dico[gt][6]))


def display_gt_coloration(folder, ego):
    path = 'GALLERY/%s/%s/Graphs/GT_graphs' % (folder, ego)
    graphs_list = [graph for graph in os.listdir(path) if (os.path.isfile(os.path.join(path,graph)) and '.gml' in graph)]
    for graph_path in graphs_list:
        graph = Graph.Read_GML('%s/%s' % (path,graph_path))
        for v in graph.vs:
            v['size'] = 5*math.log(2+v.degree())
        graph.vs[0]
        graph.es['curved'] = 0.3
        layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)
        place = '%s/SVG/%s.svg' % (path, graph_path[0:-4])
        if not os.path.isdir('%s/SVG' % path):
            os.mkdir('%s/SVG' % path)
        plot(graph, place, layout = layout, vertex_color = [v['color'] for v in graph.vs])

    with open(path+'/style.css', 'w') as css_file:
        css_file.write(
'td.nb {\n \
    text-align: right; \n\
    }\n\
td.ratio {\n\
      border-right: solid thin black;\n\
      padding: 0 4px;\n\
    }\n\
\n\
figure {\n\
  display: inline-block;\n\
}'
        )














