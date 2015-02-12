from igraph import *
import socket

def create_graph(dict_of_mutual_commenters, folder, ego):
    graph = Graph.Full(0)
    n = 0
    name_to_id = {}
    for commenter in dict_of_mutual_commenters:
        if len(dict_of_mutual_commenters[commenter]) == 0:
            continue
        graph.add_vertex(name = commenter)
        name_to_id[commenter] = n
        n += 1
    for commenter in graph.vs:
        for cocom in dict_of_mutual_commenters[commenter['name']]:
            if not cocom in name_to_id:
                continue
            cocom_vertex = graph.vs[name_to_id[cocom]]
            if cocom_vertex.index <= commenter.index:
                continue
            already_in = False
            for neighbors in commenter.neighbors():
                if neighbors.index == cocom_vertex.index:
                    already_in = True
                    for edge in graph.es:
                        if (edge.source == commenter.index and edge.target == cocom_vertex.index):
                            edge['nbst'] += 1
                            break
            if already_in == False:
                graph.add_edge(commenter.index ,cocom_vertex.index, **{'nbst' : 1})
                
    graph['folder'] = folder
    graph['ego'] = ego
    for v in graph.vs:
        v['name'] = v['name'].encode('utf8')
    return graph

def draw_graph(graph):
    graph.es['curved'] = 0.3
    for e in graph.es:
        e['width'] = 2*math.log(e['nbst'], 2) + 1
        
    layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)    
    if not os.path.isdir('GALLERY/'+graph['folder']):
        os.mkdir('GALLERY/'+graph['folder'])
    if not os.path.isdir('GALLERY/'+graph['folder']+'/'+graph['ego']):
        os.mkdir('GALLERY/'+graph['folder']+'/'+graph['ego'])
    place = 'GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs/commenters.svg'
    if socket.gethostname() != 'ccadovir01':
        plot(graph, place, layout = layout, vertex_size = 10)
      
def write_graph(graph):
    if not os.path.isdir('GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs'):
        os.mkdir('GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs')
    graph.write('GALLERY/'+graph['folder']+'/'+graph['ego']+'/Graphs/commenters.gml', format = 'gml')
    
def import_graph(folder, ego):
    graph =  Graph.Read('GALLERY/'+folder+'/'+ego+'/Graphs/commenters.gml', format = 'gml')
    graph['folder'] = folder
    graph['ego'] = ego
    return graph

def induced_graph(graph, id_status, list_of_vertices):
    induced = graph.induced_subgraph(list_of_vertices)
    induced.es['curved'] = 0.3
    folder = graph['folder']
    ego = graph['ego']
    
    for e in induced.es:
        #if e['nbst'] > 0:
        e['color'] = 'black'
            #e['width'] = 2*math.log(e['nbst'] + 1, 2)
        
    layout = induced.layout_fruchterman_reingold(repulserad = len(induced.vs)**3)
    if not os.path.isdir('GALLERY/'+folder+'/'+ego+'/statuses/'):
        os.mkdir('GALLERY/'+folder+'/'+ego+'/statuses')    
    if not os.path.isdir('GALLERY/'+folder+'/'+ego+'/statuses/'+id_status):
        os.mkdir('GALLERY/'+folder+'/'+ego+'/statuses/'+id_status)
    place = 'GALLERY/'+folder+'/'+ego+'/statuses/'+id_status+'/induit_commenters.svg'
    #plot(induced, place, layout = layout, vertex_size = 10)
    return induced