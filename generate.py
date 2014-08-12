from igraph import *
import patterns
import methods_graph

#question : comment faire pour identifier les positions d'un graphe ?

def evol_one_pattern(pattern):
    new_patterns = []
    graph_temp = pattern.copy()
    i = 2**(len(graph_temp.vs)) - 1 #remplacer len(graph_temp.vs) par nb_of_positions asap !
    while i > 0:
        i = 0

def generate(i):
    prev_patterns = patterns.PATTERNS[i-2]
    new_patterns = []
    for prev_pattern in prev_patterns:
        print prev_pattern
        print methods_graph.calculate_degree_distribution(prev_pattern)
        print methods_graph.calculate_degree_combination(prev_pattern)
        
        
    
generate(6)
    