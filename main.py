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
    dict_of_mutual_friends = main_jsons.main(args.folder, args.ego, 'friends')
    dict_of_mutual_commenters = main_jsons.main(args.folder, args.ego, 'statuses')
    if len(dict_of_mutual_friends) > 0:
        return main_graphs.main(dict_of_mutual_friends, dict_of_mutual_commenters, args.folder, args.ego)
    else:
        return None
    
def enumerate(args, quality):
    graph = main_graphs.import_graph(args.folder, args.ego, quality)
    enumeration = main_enumeration.main(graph, {})
    path = 'GALLERY/'+args.folder+'/'+args.ego+'/'
    csv_file = open(path+'patterns_'+quality+'.csv', 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(enumeration[0])
    return enumeration[0]
    
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
    path = 'GALLERY/'+args.folder+'/'+args.ego+'/statuses/'+id_status+'/'
    csv_file = open(path+'patterns_induced_friends.csv', 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(patterns_enumeration[0])
    return patterns_enumeration[0]
    
    #graph_commenters = main_graphs.import_graph(args.folder, args.ego, 'statuses')
    #induced_graph_commenters = main_graphs.induced_subgraph(graph_commenters, id_status, list_of_commenters, 'statuses')
    #enumeration = main_enumeration.main(induced_graph_commenters, {})
    #methods_htmls.enumerate_induced(args.folder, args.ego, id_status, enumeration[0], 'status')

if args.options != None:
    if 'init' in args.options:
        init()
    elif 'enumerate' in args.options:
        enumerate(args, 'friends')
        enumerate(args, 'commenters')
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
        if len(graph_friends.es) < 2000 and len(graph_friends.es) > 0:
            enumeration = enumerate(args, 'friends')
        if len(graph_commenters.es) < 2000 and len(graph_commenters.es) > 0:
            enumerate(args, 'commenters')
        list_of_statuses = study_statuses(args)
        if enumeration == None:
            enumeration_status = [0]*30
        else:
            enumeration_status = [0]*len(enumeration)
        for status in list_of_statuses:
            temp = study_status(args, status[0])
            for i in range(0, len(temp)):
                enumeration_status[i] += temp[i]
        #if len(list_of_statuses) > 0:
            #print_result_all_induced(enumeration_status)
        indicators.main(args.folder, args.ego)
    