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
import status

def init(args):
    print args
    if os.path.isfile('GALLERY/'+args.folder+'/'+args.ego+'/Graphs/commenters.gml'):
        return None
    if len(main_jsons.list_of_friends(args.folder, args.ego)) > 1000:
        return
    dict_of_mutual_friends = main_jsons.main(args.folder, args.ego, 'friends')
    dict_of_mutual_commenters = main_jsons.main(args.folder, args.ego, 'statuses')
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
    
def study_statuses(args):
    dict_of_commenters_per_status = main_jsons.main(args.folder, args.ego, 'commenters')
    dict_of_number_of_comments_by_ego = status.dict_of_number_of_comments_by_ego(dict_of_commenters_per_status)
    dict_of_number_of_commenters = status.dict_of_number_of_commenters(dict_of_commenters_per_status)
    sorted_list = status.sorted_list_of_status(dict_of_number_of_comments_by_ego, dict_of_number_of_commenters)
    list_of_printed_statuses = pretty_print.status(args.folder, args.ego, sorted_list)
    return list_of_printed_statuses
    
def study_status(args, id_status):
    dict_of_commenters_per_status = main_jsons.main(args.folder, args.ego, 'commenters')
    list_of_commenters = dict_of_commenters_per_status[id_status]
    graph_friends = main_graphs.import_graph(args.folder, args.ego, 'friends')
    induced_graph_friends = main_graphs.induced_subgraph(graph_friends, id_status, list_of_commenters, 'friends')
    patterns_enumeration = main_enumeration.main(induced_graph_friends, {})
    path = 'GALLERY/'+args.folder+'/'+args.ego+'/Statuses/'+id_status+'/'
    csv_file = open(path+'patterns_induced_friends.csv', 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(patterns_enumeration[0])
    return patterns_enumeration[0]
    
    #graph_commenters = main_graphs.import_graph(args.folder, args.ego, 'statuses')
    #induced_graph_commenters = main_graphs.induced_subgraph(graph_commenters, id_status, list_of_commenters, 'statuses')
    #enumeration = main_enumeration.main(induced_graph_commenters, {})
    #methods_htmls.enumerate_induced(args.folder, args.ego, id_status, enumeration[0], 'status')
  

if not os.path.isdir('GALLERY/'+args.folder):
    os.mkdir('GALLERY/'+args.folder)
if not os.path.isdir('GALLERY/'+args.folder+'/'+args.ego):
    os.mkdir('GALLERY/'+args.folder+'/'+args.ego)  
  
if args.options != None:
    if 'init' in args.options:
        init(args)
    elif 'enumerate' in args.options:
        enumerate(args, 'friends')
        #enumerate(args, 'commenters')
    elif 'status' in args.options:
        if len(args.options) > 1:
            study_status(args, args.options[1])
        else:
            study_statuses(args)
    
else:
    triple = init(args)
    if triple != None :
        graph_friends = triple[0]
        graph_commenters = triple[1]
        enumeration = None
        if len(graph_friends.es) < 3000 and len(graph_friends.es) > 0:
            enumeration = enumerate(args, 'friends')[0]
            print 'enumeration friends done'
        else:
            print len(graph_friends.es)
        if len(graph_commenters.es) < 2000 and len(graph_commenters.es) > 0:
            enumerate(args, 'commenters')
            print 'enumeration commenters done'
        list_of_statuses = study_statuses(args)
        if enumeration == None:
            enumeration_status = [0]*30
        else:
            enumeration_status = [0]*len(enumeration)
        #for status in list_of_statuses:
            #temp = study_status(args, status[0])
            #for i in range(0, len(temp)):
                #enumeration_status[i] += temp[i]
        #if len(list_of_statuses) > 0:
            #print_result_all_induced(enumeration_status)
        indicators.main(args.folder, args.ego)
    