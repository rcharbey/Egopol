# -*- coding: utf-8 -*-

import gzip
import json
import os
import csv

def open_json(folder, ego):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/statuses.jsons"):
        f = open("DATA/"+path+"/statuses.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/statuses.jsons.gz"
        f = gzip.open(gz, 'rb')
    return f

def print_list_of_commenters(folder, ego, list_of_friends):
    f = open_json(folder, ego)
    to_write = open('GALLERY/'+folder+'/'+ego+'/Graphs/list_of_commenters.json', 'w')
    cmters_already_seen = set()

    for line in f:
        status = json.loads(line)
        if 'comments' in status:
            for comment in status['comments']:
                if 'name' in comment['from']:
                    if comment['from']['name'] == None:
                        commenter = u'None'
                    else:
                        commenter = comment['from']['name']
                else:
                    commenter = comment["from"]["id"]
                if commenter == ego:
                    commenter = 0
                else:
                    if commenter not in cmters_already_seen and commenter in list_of_friends:
                        cmters_already_seen.add(commenter)
    to_write.write(json.dumps([list_of_friends.index(e) for e in list(cmters_already_seen) if e != None]))
    to_write.close()

def read_list_of_commenters(folder, ego):
    path = folder + '/' + ego
    f = open("GALLERY/"+path+"/Graphs/list_of_commenters.json", 'rb')
    for line in f:
        list_of_commenters = json.loads(line)
        return list_of_commenters

def dict_of_commenters_per_status(folder, ego):
    f = open_json(folder, ego)
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
                if commenter == ego.decode('utf-8'):
                    commenter = 0
                if commenter not in commenters:
                    commenters[commenter] = 1
                else:
                    commenters[commenter] += 1
        result[status['id']] = commenters
    return result

def dict_of_likers_per_status(folder, ego):
    f = open_json(folder, ego)
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
                if liker == ego.decode('utf-8'):
                    liker = 0
                likers.append(liker)
        result[status['id']] = likers
    return result

def dict_of_likers_of_comments_per_status(folder, ego):
    path = folder +'/' + ego
    f = open_json(folder, ego)
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
                        if liker not in likers:
                            likers[liker] = 1
                        else:
                            likers[liker] += 1
        result[status['id']] = likers
    return result

def dict_of_mutual_commenters(folder, ego, list_of_friends):
    f = open_json(folder, ego)
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

def calculate_info_likers(folder, ego):
    f = open_json(folder, ego)
    result = {}

    for line in f:
        status = json.loads(line)
        if 'likes' in status:
            for like in status['likes']:
                if 'name' in like:
                    liker = like['name']
                else:
                    liker = like['id']
                if liker in result:
                    result[liker] += 1
                else:
                    result[liker] = 1

    return result

def calculate_info_likers_of_comment(folder, ego):
    f = open_json(folder, ego)
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
                        if liker in result:
                            result[liker] += 1
                        else:
                            result[liker] = 1
    return result

def find_status(folder, ego, id):
    f = open_json(folder, ego)
    for line in f:
        status = json.loads(line)
        if status['id'] == id:
            return status

def gt_per_status(folder, ego, list_of_gt = None):
    dict_gt_per_status = {}
    with open('%s/statuses-csv/%s.csv' % (os.path.expanduser("~"), ego), 'r') as reader:
        csv_reader = csv.reader(reader, delimiter = ';')
        csv_reader.next()
        for line in csv_reader:
            if list_of_gt:
                if not line[16] in list_of_gt:
                    continue
            dict_gt_per_status[line[2]] = line[16]
    return dict_gt_per_status

def gt_and_activity(folder, ego):
    dict_commenters_per_status = dict_of_commenters_per_status(folder, ego)
    dict_likers_per_status = dict_of_likers_per_status(folder, ego)

    dict_gt_per_status = gt_per_status(folder, ego)

    result = {}
    for status in dict_gt_per_status:
        gt = dict_gt_per_status[status]
        if not gt in result:
            #[nb statuses, nb com, nb likes, {nb com per commenter}, {nb likes per commenter}, nb commenter, nb liker]
            result[gt] = [0, 0, 0, {}, {}, 0, 0]
        ln_com = result[gt][3]
        ln_likes = result[gt][4]
        result[gt][0] += 1

        for commenter in dict_commenters_per_status.get(status, []):
            nb_com = dict_commenters_per_status[status][commenter]
            if not commenter in ln_com:
                ln_com[commenter] = nb_com
                result[gt][5] += 1
            else:
                ln_com[commenter] += nb_com
            result[dict_gt_per_status[status]][1] += nb_com

        for liker in dict_likers_per_status.get(status, []):
            if not liker in ln_likes:
                ln_likes[liker] = 1
                result[gt][6] += 1
            else:
                ln_likes[liker] += 1
            result[dict_gt_per_status[status]][2] += 1

    new_result = {}

    for status in result:
        if result[status][0] >= 5 and (result[status][1] >= 5 or result[status][2] >= 5):
            new_result[status] = result[status]

    return new_result