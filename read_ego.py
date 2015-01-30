import gzip
import json
import os

def list_of_liked_pages(folder, ego):
    path = folder +'/' + ego
    if os.path.isfile("DATA/"+path+"/ego.json"):
        f = open("DATA/"+path+"/ego.json", 'rb')
    else:
        gz = "DATA/"+path+"/ego.json.gz"
        f = gzip.open(gz, 'rb')
    for line in f:
        infos = json.loads(line)
        result = []
        if 'likes' in infos:
            for liked in infos['likes']:
                result.append({'name' : liked['name'], 'category' : liked['category']})
        return result