# -*- coding: utf-8 -*-

import gzip
import json
import os

def dict_of_mutual(folder, ego):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/friends.jsons"):
        f = open("DATA/"+path+"/friends.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/friends.jsons.gz"
        f = gzip.open(gz, 'rb')
    result = {}
    
    for line in f:
        jr = json.loads(line)
        if 'name' in jr:
            quality = 'name'
        else:
            quality = 'id'
        result[jr[quality]] = []
        if 'mutual' in jr:
            for neighbor in jr['mutual']:
                result[jr[quality]].append(neighbor[quality])
    f.close()
    return result


def list_of_friends(folder, ego):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/friends.jsons"):
        f = open("DATA/"+path+"/friends.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/friends.jsons.gz"
        f = gzip.open(gz, 'rb')
    
    result = []
    for line in f:
        friend = json.loads(line)
        if 'name' in friend:
            result.append(friend['name'])
        else:
            result.append(friend["id"])
    f.close()    
    return result

def find_friend(folder, ego, id):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/friends.jsons"):
        f = open("DATA/"+path+"/friends.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/friends.jsons.gz"
        f = gzip.open(gz, 'rb')
    for line in f:
        friend = json.loads(line)
        if ('name' in friend and friend['name'] == id) or friend['id'] == id:
            return friend
    return {'id' : id}
