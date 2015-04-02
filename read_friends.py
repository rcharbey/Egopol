# -*- coding: utf-8 -*-

import gzip
import json
import os

def create_correspondence_table(folder, ego):
    path = folder +'/' + ego
    table_to_write = open('GALLERY/'+path+'/Graphs/correspondence_table', 'w')
    if os.path.isfile("DATA/"+path+"/friends.jsons"):
        f = open("DATA/"+path+"/friends.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/friends.jsons.gz"
        f = gzip.open(gz, 'rb')
    for line in f:
        friend = json.loads(line)
        if 'name' in friend:
            table_to_write.write((friend['name'] + u'\n').encode('utf8'))
        else:
            table_to_write.write((friend['id'] + u'\n').encode('utf8'))
    f.close()    
    table_to_write.close()
    

def list_of_mutual(folder, ego, list_of_friends):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/friends.jsons"):
        f = open("DATA/"+path+"/friends.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/friends.jsons.gz"
        f = gzip.open(gz, 'rb')
    result = {}
    
    n = 0
    for line in f:
        jr = json.loads(line)
        result.append([])
        if 'mutual' in jr:
            for neighbor in jr['mutual']:
                if neighbor in list_of_friends:
                    result[n].append(list_of_friends.index(neighbor))
    f.close()
    return result


def list_of_friends(folder, ego):
    path = folder +'/' + ego
    result = []
    f = open('GALLERY/'+path+'/correspondence_table', 'r')
    for line in f:
        result.append(line)
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
