from igraph import *

def create_graph(dict_of_mutual_commenters, folder, ego):
    graph = Graph.Full(0)
    n = 0
    name_to_id = {}
    for commenter in dict_of_mutual_commenters:
        if len(dict_of_mutual_commenters[commenter]) == 0:
            continue
        already_in = False
        for v in graph.vs:
            if v['name'] == commenter:
                already_in = True
        if already_in == False:
            graph.add_vertex(name = commenter)
            name_to_id[commenter] = n
            n += 1
    for commenter in graph.vs:
        for cocom in dict_of_mutual_commenters[commenter['name']]:
            cocom_vertex = graph.vs[name_to_id[cocom]]
            if cocom_vertex.index <= commenter.index:
                continue
            already_in = False
            for neighbors in commenter.neighbors():
                if neighbors.index == cocom_vertex.index:
                    already_in = True
                    for edge in graph.es:
                        if (edge.source == commenter.index and edge.target == cocom_vertex.index):
                            edge['nb_st'] += 1
                            break
            if already_in == False:
                graph.add_edge(commenter.index ,cocom_vertex.index, **{'nb_st' : 1})
                
    graph['folder'] = folder
    graph['ego'] = ego
    return graph

def draw_graph(graph):
    graph.es['curved'] = 0.3
    for e in graph.es:
        if e['nb_st'] > 0:
            e['color'] = 'black'
            e['width'] = 2*math.log(e['nb_st'] + 1, 2)
        else :
            e['color'] = 'rgba(0,0,0,0)'
        
    layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)    
    place = 'GALERY/'+graph['folder']+'/'+graph['ego']+'/commenters.svg'
    plot(graph, place, layout = layout, vertex_size = 10)
      
def write_graph(graph):
    graph.write('GALERY/'+graph['folder']+'/'+graph['ego']+'/statuses.txt', format = 'gml')
    
def import_graph(folder, ego):
    graph =  Graph.Read('GALERY/'+folder+'/'+ego+'/statuses.txt', format = 'gml')
    graph['folder'] = folder
    graph['ego'] = ego
    return graph

def induced_graph(graph, id_status, list_of_vertices):
    induced = graph.induced_subgraph(list_of_vertices)
    induced.es['curved'] = 0.3
    folder = graph['folder']
    ego = graph['ego']
    
    for e in induced.es:
        #if e['nb_st'] > 0:
        e['color'] = 'black'
            #e['width'] = 2*math.log(e['nb_st'] + 1, 2)
        
    layout = induced.layout_fruchterman_reingold(repulserad = len(induced.vs)**3)
    if not os.path.isdir('GALERY/'+folder+'/'+ego+'/Statuses/'+id_status):
        os.mkdir('GALERY/'+folder+'/'+ego+'/Statuses/'+id_status)
    place = 'GALERY/'+folder+'/'+ego+'/Statuses/'+id_status+'/induit_commenters.svg'
    plot(induced, place, layout = layout, vertex_size = 10)
    return induced