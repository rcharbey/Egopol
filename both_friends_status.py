import sys
from igraph import *
import math
import os
import socket

#Creation/Affichage du graphes amis/commentaires 

def create_graph(graph_friends, graph_commenters, folder, ego):
    graph = Graph.Full(0)
    for v in graph_friends.vs:
        graph.add_vertex(name = v['name'])
    for e in graph_friends.es:
        graph.add_edge(e.source, e.target, **{'friends' : True, 'nbst' : 0})
    for e_com in graph_commenters.es:
        source_com = graph_commenters.vs[e_com.source]['name']
        target_com = graph_commenters.vs[e_com.target]['name']
        found = False
        for e in graph.es:
            source = graph.vs[e.source]['name']
            target = graph.vs[e.target]['name']
            if (source == source_com and target == target_com) or (target == source_com and e.source == target_com):
                   e['nbst'] = e_com['nbst']
                   found = True
                   break
        if found == False:
            for v in graph.vs:
                if v['name'] == source_com:
                    source = v.index
                    break
            for v in graph.vs:
                if v['name'] == target_com:
                    target = v.index
                    break
            graph.add_edge(source, target, **{'friends' : False, 'nbst' : 1})
    graph['folder'] = folder
    graph['ego'] = ego
    return graph
    

def draw_graph_weighted(graph):
    graph.es['curved'] = 0.3
    for e in graph.es:
        if e['friends'] == True:
            if e['nbst'] == 0:
                e['color'] = 'grey'
            else:
                e['color'] = 'red'
        else:
            e['color'] = 'green'
        if e['nbst'] > 0:
            e['width'] = 2*math.log(e['nbst'] + 1, 2)
    
    layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)
    if not os.path.isdir('GALLERY/'+graph['folder']):
        os.mkdir('GALLERY/'+graph['folder'])
    if not os.path.isdir('GALLERY/'+graph['folder']+'/'+graph['ego']):
        os.mkdir('GALLERY/'+graph['folder']+'/'+graph['ego'])
    place = 'GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs/both_weighted'
    if socket.gethostname() != 'ccadovir01':
        plot(graph, place+'.svg', layout = layout, vertex_size = 10)
    graph.write(place+'.gml', format = 'gml')
    
def draw_graph(graph):
    path = 'GALLERY/' + graph['folder'] + '/' + graph['ego']
    graph.es['curved'] = 0.3
    for e in graph.es:
        e['weight'] = 1
        if e['friends'] == True:
            if e['nbst'] == 0:
                e['color'] = 'grey'
            else:
                e['color'] = 'red'
        else:
            e['weight'] = 0
            e['color'] = 'green'
        if e['nbst'] > 0:
            e['width'] = 2*math.log(e['nbst'] + 1, 2)
    
    
    layout = graph.layout_fruchterman_reingold(weights = graph.es['weight'], repulserad = len(graph.vs)**3)    
    if not os.path.isdir('GALLERY/'+graph['folder']):
        os.mkdir('GALLERY/'+graph['folder'])
    if not os.path.isdir(path):
        os.mkdir(path)
    place = path+'/Graphs/both.svg'
    if socket.gethostname() != 'ccadovir01':
        plot(graph, place, layout = layout, vertex_size = 10)

