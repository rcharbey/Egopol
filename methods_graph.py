import json
import gzip
from igraph import *

# python indicators.py DATA/export_sample/011171e509d303ecf1710551179e5c1a6e299f0e

def create_graph(path):
    gz = path+"/friends.jsons.gz"
    f = gzip.open(gz, 'rb')
    list_of_edges = []
    index_to_vertex = {}
    vertex_to_index = {}
    nb_of_vertices = 0
    for line in f:
        jr = json.loads(line)
        if not "mutual" in jr:
            vertex_to_index[jr["id"]] = nb_of_vertices
            index_to_vertex[nb_of_vertices] = jr["id"]
            nb_of_vertices += 1
    f.close()
    f = open(path, 'r')
    for line in f:
        jr = json.loads(line)
        if not "mutual" in jr:
            continue
        if not jr["id"] in vertex_to_index:
            vertex_to_index[jr["id"]] = nb_of_vertices
            index_to_vertex[nb_of_vertices] = jr["id"]
            nb_of_vertices += 1
        for neighbor in jr["mutual"]:
            if not neighbor["id"] in vertex_to_index:
                vertex_to_index[neighbor["id"]] = nb_of_vertices
                index_to_vertex[nb_of_vertices] = neighbor["id"]
                nb_of_vertices += 1
            if vertex_to_index[jr["id"]] > vertex_to_index[neighbor["id"]]:
                list_of_edges.append((vertex_to_index[jr["id"]], vertex_to_index[neighbor["id"]]))
    f.close()
    graph = Graph(list_of_edges)
    for v in graph.vs:
        v["name"] = index_to_vertex[v.index]
    return (graph, index_to_vertex, vertex_to_index)    
    
    
def create_list_neighbors(graph):
    vs = graph.vs
    es = graph.es
    list_neighbors = []
    for v in vs:
        list_neighbors.append([])
    for e in es:
        list_neighbors[e.target].append(vs[e.source])
        list_neighbors[e.source].append(vs[e.target])
    for l in list_neighbors:
        l.sort(key =lambda vertex: vertex.index,  reverse = True)
    return list_neighbors  
<<<<<<< HEAD
    
def calculate_degree_distribution(graph):
    result = []
    for v in graph.vs:
        result.append(v.degree())
    result.sort()
    return result
    
def calculate_degree_combination(graph):
    temp = []
    for v in graph.vs:
        temp.append(v.degree())
    result = []
    for v in graph.vs:
        result.append(v.degree())
        neighborhood = v.neighbors()
        for neighbor in neighborhood:
            result[v.index] += neighbor.degree()
        v["neighbor_degree"] = result[v.index]
    result.sort()
    return result
=======
>>>>>>> 6454b59ed887fbbaa0fa1851cf4a615ca7941246
