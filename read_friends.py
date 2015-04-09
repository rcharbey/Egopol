# -*- coding: utf-8 -*-

import gzip
import json
import os

def open_json(folder, ego):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/friends.jsons"):
        f = open("DATA/"+path+"/friends.jsons", 'rb')
    else:
        gz = "DATA/"+path+"/friends.jsons.gz"
        f = gzip.open(gz, 'rb')
    return f

def create_correspondence_table(folder, ego):
    path = folder +'/' + ego
    table_to_write = open('GALLERY/'+path+'/Graphs/correspondence_table', 'w')
    f = open_json(folder, ego)
    for line in f:
        friend = json.loads(line)
        if 'name' in friend:
            table_to_write.write((friend['name'] + u'\n').encode('utf8'))
        else:
            table_to_write.write((friend['id'] + u'\n').encode('utf8'))
    f.close()    
    table_to_write.close()
    

def list_of_mutual(folder, ego, list_of_friends):
    f = open_json(folder, ego)
    result = []
    n = 0
    for line in f:
        jr = json.loads(line)
        result.append([])
        if 'mutual' in jr:
            for neighbor in jr['mutual']:
                if 'name' in neighbor:
                    neighbor = neighbor['name']
                else:
                    neighbor = neighbor['id']
                if neighbor in list_of_friends:
                    result[n].append(list_of_friends.index(neighbor))
        n += 1
    f.close()
    return result


def list_of_friends(folder, ego):
    path = folder +'/' + ego
    result = []
    f = open('GALLERY/'+path+'/Graphs/correspondence_table', 'r')
    for line in f:
        result.append(line[0:len(line)-1].decode('utf-8'))
    return result

def find_friend(folder, ego, id):
    f = open_json(folder, ego)
    for line in f:
        friend = json.loads(line)
        if ('name' in friend and friend['name'] == id) or friend['id'] == id:
            return friend
    return {'id' : id}
