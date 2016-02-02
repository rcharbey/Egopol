# -*- coding: utf-8 -*-

import sys
sys.path.append('Egopol/Graphs')
sys.path.append('./Graphs')
import methods_graph
import index_neighbors_degree
import index_dictionary
import index_degree

PT = []
PS = []

def in_neighborhood_vsub(graph, list_neighbors, length_vsub):
    for n in list_neighbors:
        if graph.vs[n]['id_sub'] != -1 and graph.vs[n]['id_sub'] != length_vsub-1:
            return True
    return False

def add_vertex(graph, vertex):
    vertex['id_sub'] = len(graph.vs)
    graph.add_vertex(name = vertex['name'], **{'id_principal' : vertex.index})

def extend_subgraph(graph, k, method, graph_sub, v, vext):
    if len(graph_sub.es) > 0 :
        if method == 'dictionary':
            index_dictionary.index_pattern(graph_sub, PT, PS)
        elif method == 'neighbor_degree':
            index_neighbors_degree.index_pattern(graph_sub, PT, PS)
        elif method == 'degree' :
            index_degree.index_pattern(graph_sub, PT, PS)
    if method == 'dictionary':
        list_class = list(graph_sub.vs['evol_class'])
    if len(graph_sub.vs) == k:
        return
    while vext:
        w = vext.pop()
        vext2 = list(vext)
        add_vertex(graph_sub, w)
        if method == 'dictionary':
            graph_sub.vs[len(graph_sub.vs) - 1]['neighbors_evol_classes'] = []
        for nei in w['list_neighbors']:
            u = graph.vs[nei]
            if u.index >= v.index:
                if u['id_sub'] == -1 :
                    if not in_neighborhood_vsub(graph, u['list_neighbors'], len(graph_sub.vs)):
                        vext2.append(u)
                else:
                    if method == 'dictionary':
                        graph_sub.vs[len(graph_sub.vs)-1]['neighbors_evol_classes'].append(graph_sub.vs[u['id_sub']]['evol_class'])
                    graph_sub.add_edge(len(graph_sub.vs) - 1, u['id_sub'])
            else:
                break

        extend_subgraph(graph, k, method, graph_sub, v, vext2)
        graph_sub.delete_vertices(w['id_sub'])
        w['id_sub'] = -1
        if method == 'dictionary':
            graph_sub.vs['evol_class'] = list_class

def characterize_with_patterns(graph, k, method):
    print graph
    methods_graph.create_list_neighbors(graph)
    global PT
    global PS
    PT = 30*[0]
    PS = []
    for v in graph.vs:
        PS.append(73*[0])
        v['id_sub'] = -1
    for v in graph.vs:

        graph_sub = Graph.Formula()
        v['id_sub'] = 0
        if not 'name' in v.attributes():
            v['name'] = str(v.index)
        graph_sub.add_vertex(name = v['name'], **{'id_principal' : v.index, 'evol_class' : 1, 'pattern_sub' : 0, 'neighbors_evol_classes' : []})

        vext = []
        for nei in v['list_neighbors']:
            if nei > v.index:
                vext.append(graph.vs[nei])

        if len(vext) > 0:
            extend_subgraph(graph, k, method, graph_sub, v, vext)
        v['id_sub'] = -1
    return (PT, PS)