import json
import gzip
from igraph import *
     
def create_list_neighbors(graph):
    for v in graph.vs:
        v['list_neighbors'] = []
    for e in graph.es:
        graph.vs[e.target]['list_neighbors'].append(e.source)
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
