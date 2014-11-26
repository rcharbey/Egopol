import gzip
import json

def dict_of_commenters_per_status(folder, ego, list_of_friends):
    path = folder + '/' + ego
    gz = "DATA/"+path+"/statuses.jsons.gz"
    f = gzip.open(gz, 'rb')
    
    result = {}

    for line in f:
        status = json.loads(line)
        commenters = {}
        if 'comments' in status:
            for comment in status["comments"]:
                commenter = comment["from"]["id"]
                if commenter == ego:
                    commenter = 0
                elif commenter not in list_of_friends:
                    continue
                if commenter not in commenters:
                    commenters[commenter] = 1
                else:
                    commenters[commenter] += 1
        result[status['id']] = commenters
    return result


def dict_of_mutual_commenters(folder, ego, list_of_friends):
    path = folder + '/' + ego
    gz = "DATA/"+path+"/statuses.jsons.gz"
    f = gzip.open(gz, 'rb')
    
    result = {}
    
    for friend in list_of_friends:
        result[friend] = []
    
    for line in f:
        status = json.loads(line)
        if 'comments' in status:
            for comment in status['comments']:
                commenter = comment['from']['id']
                if commenter in list_of_friends:
                    for comment_2 in status['comments']:
                        commenter_2 = comment_2['from']['id']
                        if commenter_2 in list_of_friends and commenter_2 != commenter:
                            result[commenter].append(commenter_2)
                            
    return result

def list_of_commenters(folder, ego, list_of_friends):
    path = folder + '/' + ego
    gz = "DATA/"+path+"/statuses.jsons.gz"
    f = gzip.open(gz, 'rb')
    
    result = []
    
    for line in f:
        status = json.loads(line)
        if 'comments' in status:
            for comment in status['comments']:
                commenter = comment['from']['id']
                if commenter not in result and commenter in list_of_friends:
                    result.append(commenter)
                    
    return result
    