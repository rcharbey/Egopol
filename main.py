# -*- coding: utf-8 -*-

import argparse
parser = argparse.ArgumentParser(description="main")
parser.add_argument('folder', help="ego's folder")
parser.add_argument('ego', help="ego's name")
parser.add_argument('--options', '-o', nargs='+')
args = parser.parse_args()

import os
import sys
sys.path.append("./Graphs")
sys.path.append("./Enumeration")
sys.path.append("./Jsons")
sys.path.append("./Indicators")
import main_enumeration
import main_graphs
import main_jsons
import csv
import pretty_print
import indicators

def init(args):
    #if os.path.isfile('GALLERY/'+args.folder+'/'+args.ego+'/Graphs/friends.gml'):
        #return (main_graphs.import_graph(args.folder, args.ego, 'friends'), None, None)
    #print 'initialisé'
    dict_of_mutual_friends = main_jsons.main(args.folder, args.ego, 'friends')
    dict_of_mutual_commenters = main_jsons.main(args.folder, args.ego, 'statuses')
    #dict_of_mutual_commenters = None
    if len(dict_of_mutual_friends) > 0:
        return main_graphs.main(dict_of_mutual_friends, dict_of_mutual_commenters, args.folder, args.ego)
    else:
        return None
    
def enumerate(args, quality):
    """
       enumerate imports the graph from the ml file created by init and runs the enumeration algo on it.
       once the result shows up, it prints it in two differents csv files. One for the patterns and the other for the positions.
    """
    graph = main_graphs.import_graph(args.folder, args.ego, quality)
    enumeration = main_enumeration.main(graph, {})
    if not os.path.isdir('GALLERY/'+args.folder+'/'+args.ego+'/Enumeration/'):
        os.mkdir('GALLERY/'+args.folder+'/'+args.ego+'/Enumeration/')
    if not os.path.isdir('GALLERY/'+args.folder+'/'+args.ego+'/Enumeration/CSV/'):
        os.mkdir('GALLERY/'+args.folder+'/'+args.ego+'/Enumeration/CSV/')
    path = 'GALLERY/'+args.folder+'/'+args.ego+'/Enumeration/CSV/'
    writer_patterns = csv.writer(open(path+'patterns_'+quality+'.csv', 'wb'), delimiter=';')
    writer_patterns.writerow(enumeration[0])
    writer_positions= csv.writer(open(path+'positions_'+quality+'.csv', 'wb'), delimiter = ';')
    for i in range(0, len(graph.vs)):
        writer_positions.writerow(enumeration[1][i])
    return enumeration
  
print args.options

if not os.path.isdir('GALLERY/'+args.folder):
    os.mkdir('GALLERY/'+args.folder)
if not os.path.isdir('GALLERY/'+args.folder+'/'+args.ego):
    os.mkdir('GALLERY/'+args.folder+'/'+args.ego)  
  
if args.options != None:
    if 'init' in args.options:
        init(args)
    elif 'enumerate' in args.options:
        enumerate(args, 'friends')
        enumerate(args, 'commenters')
    
else:
    triple = init(args)
    if triple != None :
        graph_friends = triple[0]
        graph_commenters = triple[1]
        print 'enumeration friends'
        if len(graph_friends.es) < 3000 and len(graph_friends.es) > 0:
            enumerate(args, 'friends')[0]
            print 'done'
        else:
            print 'squeezed'
        print 'enumeration commenters done'
        if len(graph_commenters.es) < 2000 and len(graph_commenters.es) > 0:
            enumerate(args, 'commenters')
            print 'done'
        else:
            print 'squeezed'
            
        indicators.main(args.folder, args.ego)