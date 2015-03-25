# -*- coding: utf-8 -*-

import json
import os
import gzip

def list_of_qualified(folder, ego):
    path = folder +'/' + ego
    result = []
    if os.path.isfile("DATA/"+path+"/qualify.json"):
        f = open("DATA/"+path+"/qualify.json", 'rb')
    else:
        gz = "DATA/"+path+"/qualify.json.gz"
        f = gzip.open(gz, 'rb')
    
    for line in f:
        jr = json.loads(line)
    for friend in jr['friends']:
        result.append(friend)
    return result