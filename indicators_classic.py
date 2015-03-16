# -*- coding: utf-8 -*-

import os
import csv

def main(folder, ego, graph):
    if not os.path.isfile('GALLERY/'+folder+'/'+ego+'/Graphs/friends.gml'):
        return
    
    infos = []
    n = len(graph.vs)
    
    #nom - 0
    infos.append(ego)
    
    #nombre d'amis - 1
    infos.append(len(graph.vs))
    
    #nombre de liens - 2
    infos.append(len(graph.es))
    
    #sommets isolés - 3
    cmpt_sommets_isoles = 0
    for v in graph.vs:
        if v.degree() == 0:
            cmpt_sommets_isoles += 1
    infos.append(cmpt_sommets_isoles)
                
    #Louvain - 4 
    clusters_list = graph.community_multilevel()
    compt_com = 0
    for clu in clusters_list:
        if len(clu) >= 3:
            compt_com += 1
    infos.append(compt_com)
    
    #Modularité - 5
    infos.append(round(clusters_list.modularity,2))
    
    #max CC - 6
    graph_list = graph.decompose()
    max_nb = 0
    max_index = 0
    i = 0
    for g in graph_list:
        if len(g.vs) > max_nb:
            max_index = i
            max_nb = len(g.vs)
        i += 1
    infos.append(max_nb)
    
    #Louvain max CC - 7
    graph_max_cc = graph_list[max_index]
    clusters_list = graph_max_cc.community_multilevel()
    
    compt_com_max_cc = 0
    for cl in clusters_list:
        if len(cl) >= 6:
            compt_com_max_cc += 1
    infos.append(compt_com_max_cc)

    #Diametre - 8
    infos.append(graph.diameter())
        
    #Coefficient de clustering - 9
    infos.append(round(graph.transitivity_undirected(),2))
    
    #Densité - 10
    infos.append(round(graph.density(),2))
    
    #Betweenness (Freeman) - 11
    btw_list = graph.betweenness()
    max_btw = 0
    for btw in btw_list:
        if btw > max_btw:
            max_btw = btw
    sum_btw = 0
    for btw in btw_list:
        sum_btw += max_btw - btw
    divisor = n**3 - 4*(n**2) + 5*n - 2
    infos.append(2*round((sum_btw/divisor),2))
    
    #Type
    type = ''
    if infos[11] > 0.2:
        if infos[5] > 0.28:
            if infos[5] >= 0.4 and infos[8] >= 4:
                infos.append('Chainage')
            else:
                infos.append('Fleur')
        else:
            infos.append('Dense centré')
    else:
        if infos[5] > 0.28:
            if infos[10] > 0.1:
                infos.append('Noyaux dissociés')
            else:
                infos.append('Dispersé')
        else:
            infos.append('Dense non centré')
    
    file = open('GALLERY/General/indicators_classics.csv','ab')
    csv_writer = csv.writer(file, delimiter = ';')
    new_info = []
    for i in infos:
        if isinstance(i, str):
            new_info.append(unicode(i.decode('utf-8')).encode('utf-8'))
        elif isinstance(i, unicode):
            new_info.append(i.encode('utf-8'))
        else:
            new_info.append(i)
    
    print new_info
            
    csv_writer.writerow(new_info)
    file.close()