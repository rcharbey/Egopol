import read_friends
import read_statuses
import read_ego
import read_qualify

def main(folder, ego, options):
    if options == 'friends' :
        return read_friends.dict_of_mutual(folder, ego)
    elif options == 'statuses' :
        list_of_friends = read_friends.list_of_friends(folder, ego)
        return read_statuses.dict_of_mutual_commenters(folder, ego, list_of_friends)
    elif options == 'commenters':
        list_of_friends = read_friends.list_of_friends(folder, ego)
        return read_statuses.dict_of_commenters_per_status(folder, ego, list_of_friends)
    
def list_of_friends(folder, ego):
    return read_friends.list_of_friends(folder, ego)

def calculate_info_commenters(folder, ego):
    list_friends = list_of_friends(folder, ego)
    return read_statuses.calculate_info_commenters(folder, ego, list_friends)

def calculate_info_likers(folder, ego):
    list_friends = list_of_friends(folder, ego)
    return read_statuses.calculate_info_likers(folder, ego, list_friends)

def calculate_info_likers_of_comment(folder, ego):
    list_friends = list_of_friends(folder, ego)
    return read_statuses.calculate_info_likers_of_comment(folder, ego, list_friends)

def calculate_dict_of_commenters_per_status(folder, ego):
    list_friends = list_of_friends(folder, ego)
    return read_statuses.dict_of_commenters_per_status(folder, ego, list_friends)

def calculate_dict_of_likers_per_status(folder, ego):
    list_friends = list_of_friends(folder, ego)
    return read_statuses.dict_of_likers_per_status(folder, ego, list_friends)

def calculate_dict_of_likers_of_comments_per_status(folder, ego):
    list_friends = list_of_friends(folder, ego)
    return read_statuses.dict_of_likers_of_comments_per_status(folder, ego, list_friends)
    
def find_status(folder, ego, id):
    return read_statuses.find_status(folder, ego, id)

def find_friend(folder, ego, id):
    return read_friends.find_friend(folder, ego, id)

def list_of_liked_pages(folder, ego):
    return read_ego.list_of_liked_pages(folder, ego)

def list_of_qualified(folder, ego):
    return read_qualify.list_of_qualified(folder, ego)