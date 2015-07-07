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

def create_graph(dict_of_mutual, correspondance, folder, ego):
    graph = Graph.Full(0)
    for friend in correspondance:
        graph.add_vertex()
        graph.vs[len(graph.vs) - 1]['name'] = friend.decode('utf-8')
    for friend in correspondance:
        id_friend = correspondance.index(friend)
        for id_neighbor in dict_of_mutual[id_friend]:
            if id_neighbor > id_friend:
                graph.add_edge(id_friend, id_neighbor)
    #add_graph_infos(graph, folder, ego)
    graph['folder'] = folder
    graph['ego'] = ego.encode('utf8')
    graph.write('GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs/light_graph', format = 'edgelist')
    return graph

def light_graph(dict_of_mutual, folder, ego, induced = False):
    """
    this function create a file representing the frienship graph with an edge per line 
    and a correspondence_table between the friends and their id
    """
    patch = ''
    if induced:
        patch = '_fc'
    graph_to_write = open('GALLERY/'+folder+'/'+ego+'/Graphs/light_graph'+patch, 'w')
    file_to_write = open('GALLERY/'+folder+'/'+ego+'/Graphs/correspondence_table_com', 'w')
    table = []
    for id_friend in dict_of_mutual.keys():
        if not id_friend in table:
            table.append(id_friend)
            file_to_write.write(str(id_friend)+'\n')
        for id_neighbor in dict_of_mutual[id_friend]:
            if not id_neighbor in table:
                table.append(id_neighbor)
                file_to_write.write(str(id_neighbor)+'\n')
            if id_neighbor > id_friend:
                graph_to_write.write(str(table.index(id_friend)) + ' ' + str(table.index(id_neighbor)) + '\n')
    graph_to_write.close()   
    
def display_light(graph, show = True, fc = False):
    graph.es['curved'] = 0.3
    layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)   
    for v in graph.vs:
        v['size'] = 10
        v['label'] = v.index  
    if fc:
        patch = '_fc'
    else:
        patch = ''
    place = 'GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs/light_graph'+patch+'.svg'
    if socket.gethostname() != 'ccadovir01':
        plot(graph, place, layout = layout)  
    visual_style = {}
    visual_style['layout'] = layout
    visual_style['vertex_label_dist'] = 1
    if show == True:
        plot(graph, **visual_style)

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
      
def write_graph(graph, induced = False):
    graph.write('GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs/friends.gml', format = 'gml')
    
def import_graph(folder, ego, graph_format, fc = False):
    if graph_format == 'edgelist':
        if fc:
            graph = Graph.Read_Edgelist('GALLERY/'+folder+'/'+ego+'/Graphs/light_graph_fc', directed = False)
        else:
            graph = Graph.Read_Edgelist('GALLERY/'+folder+'/'+ego+'/Graphs/light_graph', directed = False)
    else:
        graph = Graph.Read_GML('GALLERY/'+folder+'/'+ego+'/Graphs/friends.gml')
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