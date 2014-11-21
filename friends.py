from igraph import *

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
            already_in = False
            for already_neighbor in graph.vs[name_to_id[friend]].neighbors():
                if name_to_id[neighbor] == already_neighbor.index:
                    already_in = True
                    break
            if already_in == False:
                graph.add_edge(name_to_id[friend], name_to_id[neighbor])
    graph['folder'] = folder
    graph['ego'] = ego
    return graph

def draw_graph(graph):
    graph.es['curved'] = 0.3
    layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)    
    if not os.path.isdir('GALLERY/'+graph['folder']):
        os.mkdir('GALLERY/'+graph['folder'])
    if not os.path.isdir('GALLERY/'+graph['folder']+'/'+graph['ego']):
        os.mkdir('GALLERY/'+graph['folder']+'/'+graph['ego'])
    place = 'GALLERY/'+graph['folder']+'/'+graph['ego']+'/friends.svg'
    #plot(graph, place, layout = layout, vertex_size = 10)
      
def write_graph(graph):
    graph.write('GALLERY/'+graph['folder']+'/'+graph['ego']+'/friends.gml', format = 'gml')
    
def import_graph(folder, ego):
    graph = Graph.Read('GALLERY/'+folder+'/'+ego+'/friends.gml', format = 'gml')
    graph['folder'] = folder
    graph['ego'] = ego
    return graph

def induced_graph(graph, id_status, list_of_vertices):
    induced = graph.induced_subgraph(list_of_vertices)
    induced.es['curved'] = 0.3
    folder = graph['folder']
    ego = graph['ego']
        
    layout = induced.layout_fruchterman_reingold(repulserad = len(induced.vs)**3)
    if not os.path.isdir('GALLERY/'+folder+'/'+ego+'/statuses/'):
        os.mkdir('GALLERY/'+folder+'/'+ego+'/statuses')    
    if not os.path.isdir('GALLERY/'+folder+'/'+ego+'/statuses/'+id_status):
        os.mkdir('GALLERY/'+folder+'/'+ego+'/statuses/'+id_status)
    place = 'GALLERY/'+folder+'/'+ego+'/statuses/'+id_status+'/induit_friends.svg'
    #plot(induced, place, layout = layout, vertex_size = 10)
    return induced