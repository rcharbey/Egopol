# -*- coding: utf-8 -*-

import gzip
import json
import os

def dict_of_commenters_per_status(folder, ego, list_of_friends):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/statuses.jsons"):
        f = open("DATA/"+path+"/statuses.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/statuses.jsons.gz"
        f = gzip.open(gz, 'rb')
    
    result = {}

    for line in f:
        status = json.loads(line)
        commenters = {}
        if 'comments' in status:
            for comment in status["comments"]:
                if 'name' in comment['from']:
                    commenter = comment['from']['name']
                else:
                    commenter = comment["from"]["id"]
                if commenter == ego:
                    print 'ego commente'
                    commenter = 0
                elif commenter not in list_of_friends:
                    continue
                if commenter not in commenters:
                    commenters[commenter] = 1
                else:
                    commenters[commenter] += 1
        result[status['id']] = commenters
    return result

def dict_of_likers_per_status(folder, ego, list_of_friends):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/statuses.jsons"):
        f = open("DATA/"+path+"/statuses.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/statuses.jsons.gz"
        f = gzip.open(gz, 'rb')
    
    result = {}

    for line in f:
        status = json.loads(line)
        likers = []
        if 'likes' in status:
            for like in status['likes']:
                if 'name' in like:
                    liker = like['name']
                else:
                    liker = like['id']
                if liker == ego:
                    liker = 0
                elif liker not in list_of_friends:
                    continue
                likers.append(liker)
        result[status['id']] = likers
    return result

def dict_of_likers_of_comments_per_status(folder, ego, list_of_friends):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/statuses.jsons"):
        f = open("DATA/"+path+"/statuses.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/statuses.jsons.gz"
        f = gzip.open(gz, 'rb')
    
    result = {}

    for line in f:
        status = json.loads(line)
        likers = {}
        if 'comments' in status:
            for comment in status['comments']:
                if 'likes' in comment:
                    for like in comment['likes']:
                        if 'name' in like:
                            liker = like['name']
                        else:
                            liker = like['id']
                        if 'name' in like:
                            gz_bis = 'DATA/'+path+'/ego.json.gz'
                            f_bis = gzip.open(gz_bis, 'rb')
                            infos = json.loads(f_bis)
                            if liker == infos['name']:
                                liker = 0
                        elif liker == ego:
                            liker = 0
                        elif liker not in list_of_friends:
                            continue
                        if liker not in likers:
                            likers[liker] = 1
                        else:
                            likers[liker] += 1
        result[status['id']] = likers
    return result

def dict_of_mutual_commenters(folder, ego, list_of_friends):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/statuses.jsons"):
        f = open("DATA/"+path+"/statuses.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/statuses.jsons.gz"
        f = gzip.open(gz, 'rb')
    
    result = {}
    
    for friend in list_of_friends:
        result[friend] = []
    
    for line in f:
        status = json.loads(line)
        if 'comments' in status:
            for comment in status['comments']:
                if 'name' in comment['from']:
                    commenter = comment['from']['name']
                else:
                    commenter = comment['from']['id']
                if commenter in list_of_friends:
                    for comment_2 in status['comments']:
                        if 'name' in comment_2['from']:
                            commenter_2 = comment_2['from']['name']
                        else:
                            commenter_2 = comment_2['from']['id']
                        if commenter_2 in list_of_friends and commenter_2 != commenter:
                            result[commenter].append(commenter_2)
                            
    return result

def calculate_info_commenters(folder, ego, list_of_friends):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/statuses.jsons"):
        f = open("DATA/"+path+"/statuses.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/statuses.jsons.gz"
        f = gzip.open(gz, 'rb')
    
    result = {}
    
    for line in f:
        list_commenters_of_line = []
        status = json.loads(line)
        if 'comments' in status:
            for comment in status['comments']:
                if 'name' in comment['from']:
                    commenter = comment['from']['name']
                else:
                    commenter = comment['from']['id']
                if commenter in list_of_friends:
                    if commenter in result:
                        result[commenter]['nb_of_comments'] += 1
                        if commenter not in list_commenters_of_line:
                            result[commenter]['nb_of_statuses'] += 1
                            list_commenters_of_line.append(commenter)
                    else:
                        result[commenter] = {'nb_of_comments' : 1, 'nb_of_statuses' : 1}
                        list_commenters_of_line.append(commenter)
                        
    return result

def calculate_info_likers(folder, ego, list_of_friends):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/statuses.jsons"):
        f = open("DATA/"+path+"/statuses.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/statuses.jsons.gz"
        f = gzip.open(gz, 'rb')
    
    result = {}
    
    for line in f:
        status = json.loads(line)
        if 'likes' in status:
            for like in status['likes']:
                if 'name' in like:
                    liker = like['name']
                else:
                    liker = like['id']
                if liker in list_of_friends:
                    if liker in result:
                        result[liker] += 1
                    else:
                        result[liker] = 1
                        
    return result

def calculate_info_likers_of_comment(folder, ego, list_of_friends):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/statuses.jsons"):
        f = open("DATA/"+path+"/statuses.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/statuses.jsons.gz"
        f = gzip.open(gz, 'rb')
    
    result = {}
    for line in f:
        status = json.loads(line)
        if 'comments' in status:
            for comment in status['comments']:
                if 'likes' in comment: 
                    for like in comment['likes']:
                        if 'name' in like:
                            liker = like['name']
                        else:
                            liker = like['id']
                        if liker in list_of_friends:
                            if liker in result:
                                result[liker] += 1
                            else:
                                result[liker] = 1
    return result

def find_status(folder, ego, id):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/statuses.jsons"):
        f = open("DATA/"+path+"/statuses.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/statuses.jsons.gz"
        f = gzip.open(gz, 'rb')
    for line in f:
        status = json.loads(line)
        if status['id'] == id:
            return status