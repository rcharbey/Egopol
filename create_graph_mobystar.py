import math
from igraph import *
import v_current

def line_to_int(line, start):
    result = 0
    current = start
    while line[current] != ' ':
        result = result*10 + int(line[current])
        current += 1
    return result
    

def recherche_index_info(line, i):
    index_nb_cc = 4*(i-1)
    j = 0
    k = 1
    while k < i:
        while line[j+1] != ' ':
            index_nb_cc += 1
            j += 1
        j += 4
        k += 1
    return index_nb_cc
    
def recherche_index_debut_graphe(line):
    curseur = recherche_index_info(line, 4)
    while line[curseur] != ' ':
        curseur += 1
    return (curseur + 2)
    
def add_edge(line, curseur):
    string = ""
    while line[curseur] != ' ':
        string += line[curseur]
        curseur += 1
    string += '-'
    curseur += 1
    while line[curseur] != ' ':
        string += line[curseur]
        curseur += 1
    return (string+',', curseur+1)
    
def create_cc(line, curseur):
    nb_vertices = line_to_int(line, curseur)
    curseur += int(math.log(nb_vertices, 10)) + 2
    nb_edges = line_to_int(line, curseur)
    if nb_edges == 0:
        return ("", curseur + 2)
    curseur += int(math.log(nb_edges, 10)) + 2
    string = ""
    compteur = nb_edges
    while compteur > 0:
        couple = add_edge(line, curseur)
        string += couple[0]
        curseur = couple[1]
        compteur -= 1
    return (string, curseur)            
    
def create_graph_tel():
    file_tel = open("./DATAMOBISTAR/data.txt",'r')
    for line in file_tel:
        nb_cc = line_to_int(line, recherche_index_info(line, 3))
        curseur = recherche_index_debut_graphe(line)
        string = ""
        while nb_cc > 0:
            couple = create_cc(line, curseur)
            string += couple[0]
            curseur = couple[1]
            nb_cc -= 1
    return Graph.Formula(string)