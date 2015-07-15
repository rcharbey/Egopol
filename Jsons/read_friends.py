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

def choose_quality(folder, ego):
    f = open_json(folder, ego)
    for line in f:
        jr = json.loads(line)
        if 'name' in jr:
            f.close()
            return 'name'
        else:
            f.close()
            return 'id'            

def create_correspondence_table(folder, ego):
    path = folder +'/' + ego
    table_to_write = open('GALLERY/'+path+'/Graphs/correspondence_table', 'w')
    f = open_json(folder, ego)
    result = []
    for line in f:
        friend = json.loads(line)
        print friend
        if 'name' in friend:
            to_write = (friend['name'])
        else:
            to_write = (friend['id'])
        result.append(to_write)
        table_to_write.write(to_write.encode('utf8'))
        table_to_write.write('\n')
    f.close()    
    table_to_write.close()
    return result
    
def list_of_friends(folder, ego):
    path = folder +'/' + ego
    result = []
    f = open('GALLERY/'+path+'/Graphs/correspondence_table', 'r')
    for line in f:
        result.append(line[0:len(line)-1].decode('utf-8'))
    return result

def dict_of_mutual(folder, ego):
    quality = choose_quality(folder, ego)
    f = open_json(folder, ego)
    result = {}
    friends = list_of_friends(folder, ego)
    i = 0
    for line in f:
        jr = json.loads(line)
        result[i] = []
        if 'mutual' in jr:
            for neighbor in jr['mutual']:
                if neighbor[quality] in friends:
                    result[i].append(friends.index(neighbor[quality]))
        i += 1
    f.close()
    return result

def find_friend(folder, ego, id):
    f = open_json(folder, ego)
    for line in f:
        friend = json.loads(line)
        if ('name' in friend and friend['name'] == id) or friend['id'] == id:
            return friend
    return {'id' : id}
