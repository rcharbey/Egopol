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
sys.path.append("./Indicators")
sys.path.append("./Patterns_static")
sys.path.append("./Jsons")
import main_enumeration
import main_graphs
import main_indicators
import main_jsons

folder = args.folder
ego = args.ego
options = args.options


def init():
    dict_of_mutual_friends = main_jsons.main(folder, ego, 'friends')
    dict_of_mutual_commenters = main_jsons.main(folder, ego, 'statuses')
    if len(dict_of_mutual_friends) > 0:
        return main_graphs.main(dict_of_mutual_friends, dict_of_mutual_commenters, folder, ego)
    else:
        return None
    
def enumerate(quality):
    graph = main_graphs.import_graph(folder, ego, quality)
    enumeration = main_enumeration.main(graph, {})
    main_indicators.aggregation_patterns(ego, quality, enumeration[0])
    main_indicators.enumeration(folder, ego, quality, enumeration[0], './GALLERY')
    return enumeration[0]
    
def study_statuses():
    dict_of_commenters_per_status = main_jsons.main(folder, ego, 'commenters')
    list_of_printed_statuses = main_indicators.study_statuses(folder, ego, dict_of_commenters_per_status)
    return list_of_printed_statuses
    
def study_status(id_status):
    dict_of_commenters_per_status = main_jsons.main(folder, ego, 'commenters')
    list_of_commenters = dict_of_commenters_per_status[id_status]
    graph_friends = main_graphs.import_graph(folder, ego, 'friends')
    induced_graph_friends = main_graphs.induced_subgraph(graph_friends, id_status, list_of_commenters, 'friends')
    patterns_enumeration = main_enumeration.main(induced_graph_friends, {})
    main_indicators.aggregation_patterns(id_status, 'friends_induced', patterns_enumeration[0])
    main_indicators.aggregation_patterns(id_status, 'friends_induced', patterns_enumeration[0], './GALERY/'+folder+'/'+ego+'/statuses', './../../../PATTERNS', True)
    main_indicators.enumeration_induced_in_status(folder, ego, id_status, patterns_enumeration[0], 'friends_induced', './GALERY')
    return patterns_enumeration[0]
    
    #graph_commenters = main_graphs.import_graph(folder, ego, 'statuses')
    #induced_graph_commenters = main_graphs.induced_subgraph(graph_commenters, id_status, list_of_commenters, 'statuses')
    #enumeration = main_enumeration.main(induced_graph_commenters, {})
    #main_indicators.enumerate_induced(folder, ego, id_status, enumeration[0], 'status')

 
print ego

if options != None:
    if 'init' in options:
        init()
    elif 'enumerate' in options:
        enumerate('friends')
        enumerate('commenters')
    elif 'status' in options:
        if len(options) > 1:
            study_status(args.options[1])
        else:
            study_statuses()
    
else:
    triple = init()
    if triple != None :
        graph_friends = triple[0]
        if len(graph_friends.es) < 2000 and len(graph_friends.es) > 0:
            enumeration = enumerate('friends')
            enumerate('commenters')
            list_of_statuses = study_statuses()
            enumeration_status = [0]*len(enumeration)
            for status in list_of_statuses:
                temp = study_status(status[0])
                for i in range(0, len(temp)):
                    enumeration_status[i] += temp[i]
            #if len(list_of_statuses) > 0:
                #print_result_all_induced(enumeration_status)
    