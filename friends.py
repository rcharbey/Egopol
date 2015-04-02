# -*- coding: utf-8 -*-

from igraph import *
import sys
sys.path.append('./Json')
import main_jsons
import socket

def add_graph_infos(graph, folder, ego):
    infos_commenters = main_jsons.calculate_info_commenters(folder, ego)
    infos_likers = main_jsons.calculate_info_likers(folder, ego)
    for v in graph.vs:
        if v['name'] in infos_likers:
            v['nb_likes'] = int(infos_likers[v['name']])
        else:
            v['nb_likes'] = 0
        if v['name'] in infos_commenters:
            v['nb_comments'] = int(infos_commenters[v['name']]['nb_of_comments'])
        else:
            v['nb_comments'] = 0
    for v in graph.vs:
        v['sum_comments_likes'] = int(v['nb_comments']) + int(v['nb_likes'])
        v['name'] = v['name'].encode('utf8')

def create_graph(dict_of_mutual, folder, ego):
    graph = Graph.Full(0)
    n = 0
    name_to_id = {}
    for friend in dict_of_mutual:
        graph.add_vertex(name = friend)
        name_to_id[friend] = n
        n += 1
    for friend in dict_of_mutual:
        for neighbor in dict_of_mutual[friend]:
            if neighbor not in dict_of_mutual:
                continue
            if name_to_id[friend] <= name_to_id[neighbor]:
                continue
            graph.add_edge(name_to_id[friend], name_to_id[neighbor])
    add_graph_infos(graph, folder, ego)
    graph['folder'] = folder
    graph['ego'] = ego.encode('utf8')
    return graph

def light_graph(dict_of_mutual, folder, ego):
    '''
    this function create a file representing the frienship graph with an edge per line 
    and a correspondence_table between the friends and their id
    '''
    table_to_write = open('GALLERY/'+folder+'/'+ego+'/Graphs/correspondence_table', 'w')
    graph_to_write = open('GALLERY/'+folder+'/'+ego+'/Graphs/light_graph', 'w')
    correspondence_table = {}
    n = 0
    for friend in dict_of_mutual:
        correspondence_table[friend] = n
        table_to_write.write((friend + u'\n').encode('utf8'))
        n += 1
    table_to_write.close()
    for friend in dict_of_mutual:
        id_friend = correspondence_table[friend]
        for neighbor in dict_of_mutual[friend]:
            id_neighbor = correspondence_table[neighbor]
            if id_neighbor > id_friend:
                graph_to_write.write(str(id_friend) + ' ' + str(id_neighbor) + '\n')
    graph_to_write.close()         
               

def draw_graph(graph):
    graph.es['curved'] = 0.3
    layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)         
    place = 'GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs/friends_comments_likes.svg'
    for v in graph.vs:
        v['size'] = 10*math.log(2+v['sum_comments_likes'])
        if v['sum_comments_likes'] > 10:
            v['label'] = v['name']
    if socket.gethostname() != 'ccadovir01':
        plot(graph, place, layout = layout)
    for v in graph.vs:
        v['size'] = 10
        v['label'] = None
        
    place = 'GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs/friends_degree.svg'
    for v in graph.vs:
        v['size'] = 10*math.log(2+v.degree())
        if v.degree() > 10:
            v['label'] = v['name']
    if socket.gethostname() != 'ccadovir01':
        plot(graph, place, layout = layout)
    for v in graph.vs:
        v['size'] = 10
        v['label'] = None
        
    place = 'GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs/friends_degree_comments_likes.svg'
    max_sum = 0
    for v in graph.vs:
        if v['sum_comments_likes'] > max_sum:
            max_sum = v['sum_comments_likes']
    for v in graph.vs:
        v['size'] = 10*math.log(2+v.degree())
        if v['sum_comments_likes'] < 0.25*max_sum:
            v['color'] = 'blue'
        elif v['sum_comments_likes'] < 0.5*max_sum:
            v['color'] = 'green'
        elif v['sum_comments_likes'] < 0.75*max_sum:
            v['color'] = 'orange'
        else:
            v['color'] = 'red'
        if v.degree() > 10:
            if v['sum_comments_likes'] > max_sum/2:
                v['label'] = v['name']
                v['label_size'] = 5*math.log(2+v.degree())
    if socket.gethostname() != 'ccadovir01':
        plot(graph, place, layout = layout)
    for v in graph.vs:
        v['size'] = 10
        v['label'] = None
      
def write_graph(graph):
    graph.write('GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs/friends.gml', format = 'gml')
    
def import_graph(folder, ego, graph_format):
    graph = Graph.Read('GALLERY/'+folder+'/'+ego+'/Graphs/friends.gml', format = graph_format)
    graph['folder'] = folder
    graph['ego'] = ego
    return graph

def induced_graph(graph, id_status, list_of_vertices):
    induced = graph.induced_subgraph(list_of_vertices)
    induced.es['curved'] = 0.3
    folder = graph['folder']
    ego = graph['ego']
        
    layout = induced.layout_fruchterman_reingold(repulserad = len(induced.vs)**3)
    if not os.path.isdir('GALLERY/'+folder+'/'+ego+'/Statuses/'+id_status):
        os.mkdir('GALLERY/'+folder+'/'+ego+'/Statuses/'+id_status)
    place = 'GALLERY/'+folder+'/'+ego+'/Statuses/'+id_status+'/induit_friends.svg'
    #plot(induced, place, layout = layout, vertex_size = 10)
    return induced