import gzip
import json

def dict_of_mutual(folder, ego):
    
    path = folder +'/' + ego
    gz = "DATA/"+path+"/friends.jsons.gz"
    f = gzip.open(gz, 'rb')
    
    result = {}
    
    for line in f:
        jr = json.loads(line)
        result[jr['id']] = []
        if 'mutual' in jr:
            for neighbor in jr['mutual']:
                result[jr['id']].append(neighbor['id'])
    f.close()
    return result


def list_of_friends(folder, ego):
    
    path = folder + '/' + ego
    gz = "DATA/"+path+"/friends.jsons.gz"
    f = gzip.open(gz, 'rb')
    
    result = []
    for line in f:
        status = json.loads(line)
        result.append(status["id"])
        
    f.close()    
    return result

def find_friend(folder, ego, id):
    path = folder + '/' + ego
    gz = "DATA/"+path+"/statuses.jsons.gz"
    f = gzip.open(gz, 'rb')
    for line in f:
        friend = json.loads(line)
        if friend['id'] == id:
            return friend
