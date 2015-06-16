# -*- coding: utf-8 -*-

import main_enumeration
import main_jsons
import main_graphs
import os
import csv
import gzip
import json

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

def read_qualified(folder, ego):
    path = folder +'/' + ego
    result = {}
    if os.path.isfile("DATA/"+path+"/qualify.json"):
        f = open("DATA/"+path+"/qualify.json", 'rb')
    else:
        gz = "DATA/"+path+"/qualify.json.gz"
        f = gzip.open(gz, 'rb')
    
    for line in f:
        jr = json.loads(line)
    for friend in jr['friends']:
        result[friend['user_id']] = friend['data'] 
    return result

folder = 'all_2015-15-05'
list_ego = [f for f in os.listdir('DATA/all_2015-15-05') if os.path.isdir(os.path.join('DATA/all_2015-15-05', f))]
for ego in list_ego:
    create_folders(folder, ego)
    main_jsons.create_correspondence_table(folder, ego)
    list_of_friends = main_jsons.list_of_friends(folder, ego)
    if len(list_of_friends) > 100:
        continue
    mutual_friends = main_jsons.dict_of_mutual_friends(folder, ego)
    dict_of_mutual_commenters = {}
    if len(mutual_friends) > 0:
        graph =  main_graphs.main(mutual_friends, dict_of_mutual_commenters, folder, ego)[0]
    else:
        continue
    print ego

    table_to_read = open('GALLERY/'+folder+'/'+ego+'/Graphs/correspondence_table', 'r')
    correspondance = []
    for line in table_to_read:
        correspondance.append(line)

    info_commenters = main_jsons.calculate_info_commenters(folder, ego)
    info_likers = main_jsons.calculate_info_likers(folder, ego)
    info_likers_of_comment = main_jsons.calculate_info_likers_of_comment(folder, ego)
    csv_file = open('GALLERY/'+folder+'/'+ego+'/'+'CSV/info_commenters_likers.csv', 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(['id', 
                    'nombre de commentaires', 
                    'nombre de statuts commentés', 
                    'nombre de likes', 
                    'centre d\'une croix',
                    'centre d\'un noeud papillon',
                    'element d\'une clique',
                    'centre motif 13',
                    'bleu motif 13',
                    'since',
                    'close',
                    'affect',
                    'begin',
                    'link'])


    sorted_info = []
    enumeration = main_enumeration.main(graph, [])
    print enumeration[0]
    path = 'GALLERY/'+folder+'/'+ego+'/Enumeration/CSV/'
    writer_patterns = csv.writer(open(path+'patterns_friends.csv', 'wb'), delimiter=';')
    writer_patterns.writerow(enumeration[0])
    writer_positions= csv.writer(open(path+'positions_friends.csv', 'wb'), delimiter = ';')
    for i in range(0, len(graph.vs)):
        writer_positions.writerow(enumeration[1][i])

    enumeration = enumeration[1]
    qualif = read_qualified(folder, ego)  
    tab_since = ['toujours',' +5 ans', '1 à 5 ans', 'moins d\'un an']
    tab_close = ['tous les jours', 'toutes les semaines', 'une fois par mois', 'tous les 3 mois', 'tous les 6 mois', 'une fois par an', 'moins d\'une fois par an']
    tab_begin = ['tous les jours', 'toutes les semaines', 'une fois par mois', 'tous les 3 mois', 'tous les 6 mois', 'une fois par an', 'moins d\'une fois par an']


    for friend in list_of_friends:
        
        if friend+'\n' in correspondance:
            friend_id_in_graph = correspondance.index(friend+'\n')
        else:
            continue
        ps = enumeration[friend_id_in_graph]
        
        #nb commentaires + nb status commentés
        if friend in info_commenters:
            info_commenter = info_commenters[friend]
        else:
            info_commenter = {'nb_of_comments' : 0, 'nb_of_statuses' : 0}
        
        #nb likes
        if friend in info_likers:
            info_liker = info_likers[friend]
        else:   
            info_liker = 0
            
        #read_qualified
        since = ''
        close = ''
        begin = ''
        link = ''
        affect = ''
        if friend in qualif:
            qualif_friend = qualif[friend]
            since = tab_since[int(qualif_friend['since']) - 1]
            close = tab_close[int(qualif_friend['close']) - 1]
            begin = tab_begin[int(qualif_friend['begin']) - 1]
            for type_link in ['family','friend','coworker','acquaintance']:
                if qualif_friend[type_link] == True:
                    link += type_link + ' '
            affect = qualif_friend['affect']

        
        infos_list = ((friend, 
                            info_commenter['nb_of_comments'], 
                            info_commenter['nb_of_statuses'], 
                            info_liker, 
                            ps[19],
                            ps[48],
                            ps[72],
                            ps[27],
                            ps[25],
                            since,
                            close,
                            affect,
                            begin,
                            link))
        
        sorted_info.append([unicode(s).encode("utf-8") for s in infos_list])
        
    sorted_info.sort(key=lambda tup: 4*tup[1]+2*tup[3], reverse = True) 

    for info in sorted_info:
        writer.writerow(info) 
        
    csv_file.close()