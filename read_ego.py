import gzip
import json

def list_of_liked_pages(folder, ego):
    path = folder + '/' + ego
    gz = "DATA/"+path+"/ego.json.gz"
    f = gzip.open(gz, 'rb')
    for line in f:
        infos = json.loads(line)
        result = []
        if 'likes' in infos:
            for liked in infos['likes']:
                result.append({'name' : liked['name'], 'category' : liked['category']})
        return result