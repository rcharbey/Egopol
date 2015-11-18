import sys
sys.path.append('./Graphs')

import friends
import commenters
import both_friends_status
import os
import methods_graph

def main(dict_friends, dict_commenters, correspondence, folder, ego):
    graph_friends = friends.create_graph(dict_friends, correspondence, folder, ego)
    if len(graph_friends.es) > 0:
        #friends.draw_graph(graph_friends)
        friends.write_graph(graph_friends)

    graph_commenters = commenters.create_graph(dict_commenters, folder, ego)
    if len(graph_commenters.es) > 0:
        #commenters.draw_graph(graph_commenters)
        commenters.write_graph(graph_commenters)
    #graph_commenters = None

    #graph_both = both_friends_status.create_graph(graph_friends, graph_commenters, folder, ego)
    #if len(graph_both.es) > 0:
        #both_friends_status.draw_graph_weighted(graph_both)
        #both_friends_status.draw_graph(graph_both)
    graph_both = None

    return (graph_friends, graph_commenters, graph_both)

def create_friends_graph(dict_friends, correspondence, folder, ego):
    graph_friends = friends.create_graph(dict_friends, correspondence, folder, ego)
    friends.write_graph(graph_friends)
    return graph_friends

def light_graph(dict_of_mutual, folder, ego, induced = False):
    friends.light_graph(dict_of_mutual, folder, ego, induced)

def import_graph(folder, ego, quality, graph_format = 'gml', fc = False):
    if quality == 'friends' :
        return friends.import_graph(folder, ego, graph_format, fc)
    elif quality == 'commenters' :
        return commenters.import_graph(folder, ego, graph_format)

def induced_subgraph(graph, id_status, list_of_vertices, quality):
    if quality == 'friends' :
        return friends.induced_graph(graph, id_status, list_of_vertices)
    elif quality == 'commenters' :
        return commenters.induced_graph(graph, id_status, list_of_vertices)

def display_light(graph, show = True, fc = False):
    friends.display_light(graph, show, fc)

def gt_coloration(folder, ego, dico):
    methods_graph.gt_coloration(import_graph(folder, ego, 'friends'), dico)

def display_gt_coloration(folder, ego):
    methods_graph.display_gt_coloration(folder, ego)

def cluster_per_alter(folder, ego):
    return friends.cluster_per_alter(folder, ego)



