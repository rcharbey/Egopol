# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('../webapp/')
for super_folder in ['Raphael', 'Algopol']:
    for folder in ['Enumeration', 'Graphs', 'Jsons', 'Indicators', 'Pretty_print']:
        sys.path.append('%s/%s/Egopol/%s/' % (os.path.expanduser("~"), super_folder, folder))

import argparse
import main_enumeration
import main_graphs
import main_jsons
import csv
import main_pretty_print
import main_indicators
from algopol.statuses import ParsedStatus


def create_folders(folder, ego):
    for path in [
        'GALLERY/',
        'GALLERY/' + folder,
        'GALLERY/' + folder + '/'+ ego,
        'GALLERY/' + folder + '/'+ ego + '/Graphs',
        'GALLERY/' + folder + '/'+ ego + '/Enumeration',
        'GALLERY/' + folder + '/'+ ego + '/Enumeration/CSV',
        'GALLERY/' + folder + '/'+ ego + '/Enumeration/HTML',
        'GALLERY/' + folder + '/'+ ego + '/CSV',
        'GALLERY/' + folder + '/'+ ego + '/Statuses',
        'GALLERY_STATUSES',
        'GALLERY_STATUSES/'+folder,
        'GALLERY/General']:
        if not os.path.isdir(path):
            os.mkdir(path)

def induced_graph_friends(args):
    folder = args.folder
    ego = args.ego
    main_jsons.create_correspondence_table(args.folder, args.ego)
    list_of_commenters = main_jsons.read_list_of_commenters(folder, ego)
    mutual_friends = main_jsons.dict_of_mutual_friends(folder, ego)
    list_of_commenters.sort(reverse = True)
    i = len(mutual_friends) - 1
    for i in mutual_friends.keys():
        if i not in list_of_commenters:
            del mutual_friends[i]
    for i in mutual_friends:
        to_del = []
        for mutual in mutual_friends[i]:
            if mutual not in list_of_commenters:
                to_del.append(mutual)
        for elem in to_del:
            mutual_friends[i].remove(elem)
    main_graphs.light_graph(mutual_friends, folder, ego, True)

def init_light(args):
    main_jsons.create_correspondence_table(args.folder, args.ego)
    mutual_friends = main_jsons.dict_of_mutual_friends(args.folder, args.ego)
    main_graphs.light_graph(mutual_friends, args.folder, args.ego)

def init(args):
    correspondence = main_jsons.create_correspondence_table(args.folder, args.ego)
    #if os.path.isfile('GALLERY/'+args.folder+'/'+args.ego+'/Graphs/friends.gml'):
        #return (main_graphs.import_graph(args.folder, args.ego, 'friends'), None, None)
    #print 'initialisé'
    mutual_friends = main_jsons.dict_of_mutual_friends(args.folder, args.ego)
    #dict_of_mutual_commenters = main_jsons.main(args.folder, args.ego, 'statuses')
    if len(mutual_friends) > 0:
        return main_graphs.create_friends_graph(mutual_friends, correspondence, args.folder, args.ego)
    else:
        return None

def enumerate(args, quality, graph_format = 'gml', induced = False):
    """
       enumerate imports the graph from the ml file created by init and runs the enumeration algo on it.
       once the result shows up, it prints it in two differents csv files. One for the patterns and the other for the positions.
    """
    graph = main_graphs.import_graph(args.folder, args.ego, quality, graph_format, induced)
    enumeration = main_enumeration.main(graph, {})
    path = 'GALLERY/'+args.folder+'/'+args.ego+'/Enumeration/CSV/'
    if induced:
        patch = '_fc'
    else:
        patch = ''
    writer_patterns = csv.writer(open(path+'patterns_'+quality+patch+'.csv', 'wb'), delimiter=';')
    writer_patterns.writerow(enumeration[0])
    writer_positions= csv.writer(open(path+'positions_'+quality+patch+'.csv', 'wb'), delimiter = ';')
    for i in range(0, len(graph.vs)):
        writer_positions.writerow(enumeration[1][i])
    return enumeration

def display(args):
    name = 'GALLERY/'+args.folder+'/'+args.ego+'/Graphs/light_graph'
    if not os.path.isfile(name):
        init_light(args)
    graph = main_graphs.import_graph(args.folder, args.ego, 'friends', 'edgelist')
    main_graphs.display_light(graph)


def clusters_per_gt(couple_of_gt, folder, ego):
    cluster_per_alter = main_graphs.cluster_per_alter(folder, ego)
    gt_per_status = main_jsons.gt_per_status(folder, ego)
    nb_cluster = max(cluster_per_alter.values())
    if nb_cluster < 3:
        return
    accounter_per_gt = {}
    max_per_gt = {}
    file_name = 'matrix'
    for gt in couple_of_gt:
        file_name += '_%s' % gt
        accounter_per_gt[gt] = {'comments' : [0]*(nb_cluster+1), 'likes' : [0]*(nb_cluster+1)}
    for id_status in gt_per_status:
        gt = gt_per_status[id_status]
        if gt in couple_of_gt:
            accounter_gt = accounter_per_gt[gt]
            status = main_jsons.find_status(folder, ego, id_status)
            for quality in ['comments', 'likes']:
                accounter_gt_quality = accounter_gt[quality]
                for active_alter in [activity.get('from', activity).get('name', activity.get('from', activity)['id']) for activity in status.get(quality, [])]:
                    cluster = cluster_per_alter.get(active_alter, -1)
                    if cluster == -1:
                        continue
                    accounter_gt_quality[cluster] += 1

    print accounter_per_gt

    for gt in couple_of_gt:
         max_per_gt[gt] = {'comments' : [], 'likes' : []}
         for quality in ['comments', 'likes']:
             for i in range(0,3):
                 to_class = accounter_per_gt[gt][quality]
                 maximum = -1
                 max_id = -1
                 for j in range(0, len(to_class)):
                     if to_class[j] > maximum:
                         maximum = to_class[j]
                         max_id = j
                 max_per_gt[gt][quality].append(max_id)
                 to_class[max_id] = -1
    with open('GALLERY/General/%s' % file_name, 'a') as file_to_write:
        csv_writer = csv.writer(file_to_write, delimiter = ';')
        for quality in ['comments', 'likes']:
            common = 0
            for cluster in max_per_gt[couple_of_gt[0]][quality]:
                if cluster == -1:
                    break
                if cluster in max_per_gt[couple_of_gt[1]][quality]:
                    common += 1

            csv_writer.writerow([ego, quality, max_per_gt[couple_of_gt[0]][quality], max_per_gt[couple_of_gt[1]][quality], common])

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="main")
    parser.add_argument('folder', help="ego's folder")
    parser.add_argument('ego', help="ego's name")
    parser.add_argument('--options', '-o', nargs='+')
    args = parser.parse_args()

    create_folders(args.folder, args.ego)

    folder = args.folder
    ego = args.ego
    options = args.options
    print str(args.folder) + ' ' + str(ego) + ' ' + str(options)

    if options != None:
        if 'light' in options:
            init_light(args)
        if 'init' in options:
            init(args)
        if 'display' in options:
            display(args)
        elif 'enumerate' in options:
            if 'indu' in options:
                enumerate(args, 'friends', 'edgelist', True)
            else:
                enumerate(args, 'friends')
                enumerate(args, 'commenters')

        elif 'indu' in options:
            induced_graph_friends(args)
        if 'indicators' in options:
            main_indicators.main(folder, ego)


        elif 'gt_coloration' in args.options:
            main_graphs.gt_coloration(folder, ego, main_jsons.gt_and_activity(folder, ego))
        elif 'gt_display' in args.options:
            main_graphs.display_gt_coloration(folder, ego)
            main_pretty_print.gt_pretty_print(folder, ego)
        elif 'cluster_per_gt' in options:
            clusters_per_gt([option for option in args.options if option in ParsedStatus.GUESSED_TYPES.get_name_set()], folder, ego)

    else:
        graph_friends = init(args)
        if graph_friends != None :
            #graph_friends = triple[0]
            #graph_commenters = triple[1]
            print 'enumeration friends'
            if len(graph_friends.es) < 3000 and len(graph_friends.es) > 0:
                enumerate(args, 'friends', graph_format = 'edgelist')
                print 'done'
            else:
                print 'squeezed'
            print 'enumeration friends done'
            #if len(graph_commenters.es) < 2000 and len(graph_commenters.es) > 0:
                #enumerate(args, 'commenters')
                #print 'done'
            #else:
                #enumeration_status = [0]*len(enumeration)
            #for status in list_of_statuses:
                #temp = study_status(args, status[0])
                #for i in range(0, len(temp)):
                    #enumeration_status[i] += temp[i]
            #if len(list_of_statuses) > 0:
                #print_result_all_induced(enumeration_status)
            #indicators.main(args.folder, args.ego)