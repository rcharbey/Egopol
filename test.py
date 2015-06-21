# -*- coding: utf-8 -*-

import main_enumeration
import main_jsons
import main_graphs
import os
import csv
import gzip
import json

def create_folders():
    for path in ['GALLERY/', 'GALLERY/Info-alters/']:
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

create_folders()
folder = 'all_2015-05-15'
list_ego = [f for f in os.listdir('DATA/all_2015-05-15') if os.path.isdir(os.path.join('DATA/all_2015-05-15', f))]
for ego in list_ego:
    correspondance = main_jsons.create_correspondence_table(folder, ego)
    mutual_friends = main_jsons.dict_of_mutual_friends(folder, ego)
    if len(mutual_friends) > 100:
        continue
    dict_of_mutual_commenters = {}
    if len(mutual_friends) > 0:
        graph =  main_graphs.main(mutual_friends, dict_of_mutual_commenters, correspondance, folder, ego)[0]
    else:
        continue
    print ego

    info_commenters = main_jsons.calculate_info_commenters(folder, ego)
    info_likers = main_jsons.calculate_info_likers(folder, ego)
    info_likers_of_comment = main_jsons.calculate_info_likers_of_comment(folder, ego)
    csv_file = open('GALLERY/Info-alters/'+ego+'.csv', 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(['id', 
                    'id graph',
                    'degree',
                    'nombre de commentaires', 
                    'nombre de statuts commentés', 
                    'nombre de likes', 
                    #'centre d\'une croix',
                    #'centre d\'un noeud papillon',
                    #'element d\'une clique',
                    #'centre motif 13',
                    #'bleu motif 13',
                    'since',
                    'close',
                    'affect',
                    'begin',
                    'link',
                    'betweeness',
                    'closeness'])


    sorted_info = []
    #enumeration = main_enumeration.main(graph, [])
    #path = 'GALLERY/'+folder+'/'+ego+'/Enumeration/CSV/'
    #writer_patterns = csv.writer(open(path+'patterns_friends.csv', 'wb'), delimiter=';')
    #writer_patterns.writerow(enumeration[0])
    #writer_positions= csv.writer(open(path+'positions_friends.csv', 'wb'), delimiter = ';')
    #for i in range(0, len(graph.vs)):
        #writer_positions.writerow(enumeration[1][i])

    #enumeration = enumeration[1]
    qualif = read_qualified(folder, ego)  
    tab_since = [u'toujours',u' +5 ans', u'1 a 5 ans', u'moins d\'un an']
    tab_close = [u'tous les jours', u'toutes les semaines', u'une fois par mois', u'tous les 3 mois', u'tous les 6 mois', u'une fois par an', u'moins d\'une fois par an']
    tab_begin = [u'tous les jours', u'toutes les semaines', u'une fois par mois', u'tous les 3 mois', u'tous les 6 mois', u'une fois par an', u'moins d\'une fois par an']


    for friend in correspondance:
        short = correspondance.index(friend)
        #ps = enumeration[short]
        
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
            
        sommet = graph.vs[short]
        
        infos_list = ((friend,
                        short,
                        sommet.degree(),
                        info_commenter['nb_of_comments'], 
                        info_commenter['nb_of_statuses'], 
                        info_liker, 
                        #ps[19],
                        #ps[48],
                        #ps[72],
                        #ps[27],
                        #ps[25],
                        since,
                        close,
                        affect,
                        begin,
                        link,
                        sommet.betweeness()
                        sommet.closeness()
                        ))
        
        sorted_info.append([unicode(s).encode("utf-8") for s in infos_list])
        
    sorted_info.sort(key=lambda tup: 4*tup[1]+2*tup[3], reverse = True) 

    for info in sorted_info:
        writer.writerow(info) 
        
    csv_file.close()