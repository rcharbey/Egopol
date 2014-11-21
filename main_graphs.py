import friends
import commenters
import both_friends_status
    
def main(dict_friends, dict_commenters, folder, ego):
    
    graph_friends = friends.create_graph(dict_friends, folder, ego)
    if len(graph_friends.es) > 0:
        #friends.draw_graph(graph_friends)
        friends.write_graph(graph_friends)

    graph_commenters = commenters.create_graph(dict_commenters, folder, ego)
    if len(graph_commenters.es) > 0:
        #commenters.draw_graph(graph_commenters) 
        commenters.write_graph(graph_commenters)
    
    graph_both = both_friends_status.create_graph(graph_friends, graph_commenters, folder, ego)
    #if len(graph_both.es) > 0:
        #both_friends_status.draw_graph_weighted(graph_both)
        #both_friends_status.draw_graph(graph_both)
    
    return (graph_friends, graph_commenters, graph_both)

def import_graph(folder, ego, quality):
    if quality == 'friends' :
        return friends.import_graph(folder, ego)
    elif quality == 'commenters' :
        return commenters.import_graph(folder, ego)
    
def induced_subgraph(graph, id_status, list_of_vertices, quality):
    if quality == 'friends' :
        return friends.induced_graph(graph, id_status, list_of_vertices)
    elif quality == 'commenters' :
        return commenters.induced_graph(graph, id_status, list_of_vertices)


