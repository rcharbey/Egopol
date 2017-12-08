# -*- coding: utf-8 -*-

import sys
import os
import csv
sys.path.append('%s/Egopol/Enumeration' % os.path.expanduser("~"))
from igraph import Graph
import argparse
import enumerate


def import_graph(folder, ego):
    if not os.path.isfile('GALLERY/'+folder+'/'+ego+'/Graphs/friends.gml'):
        return Graph.Formula('')
    graph = Graph.Read_GML('GALLERY/'+folder+'/'+ego+'/Graphs/friends.gml')
    graph['folder'] = folder
    graph['ego'] = ego
    return graph

            
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="main")
    parser.add_argument('ego', help="ego's name")
    parser.add_argument('k', help="graphlets size")
    args = parser.parse_args()

    folder = 'three'
    ego = args.ego
    k = args.k
    
    """
       enumerate imports the graph from the ml file created by init and runs the enumeration algo on it.
       once the result shows up, it prints it in two differents csv files. One for the patterns and the other for the positions.
    """
    graph = import_graph(folder, ego)
    pt, ps = enumerate.characterize_with_patterns(graph, int(k))
    
    home = os.path.expanduser('~')
    
    with open('%s/results/patterns_per_ego/%s_k%s.csv' % (home,ego, k), 'w') as patterns_w:
        csv_wp = csv.writer(patterns_w, delimiter = ';')
        csv_wp.writerow(pt) 
        
    with open('%s/results/positions_per_alter/%s_k%s.csv' % (home,ego, k), 'w') as pos_w:
        csv_wpos = csv.writer(pos_w, delimiter = ';')
        for i in range(len(ps)):
            csv_wpos.writerow([graph.vs[i]['name']] + ps[i])