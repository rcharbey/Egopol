import gzip
import json

def dict_of_mutual(folder, ego):
    
    path = folder +'/' + ego
    gz = "DATA/"+path+"/friends.jsons.gz"
    f = gzip.open(gz, 'rb')
    
    result = {}
    
    for line in f:
        jr = json.loads(line)
        if 'name' in jr:
            result[jr['name']] = []
        else:
            result[jr['id']] = []
        if 'mutual' in jr:
            for neighbor in jr['mutual']:
                if 'name' in jr:
                    result[jr['name']].append(neighbor['name'])
                else:
                    result[jr['id']].append(neighbor['id'])
    f.close()
    return result


def list_of_friends(folder, ego):
    
    path = folder + '/' + ego
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
    path = folder + '/' + ego
    gz = "DATA/"+path+"/statuses.jsons.gz"
    f = gzip.open(gz, 'rb')
    for line in f:
        friend = json.loads(line)
        if friend['id'] == id or ('name' in friend and friend['name'] == id):
            return friend
    return {'id' : id}
