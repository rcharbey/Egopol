def dict_of_number_of_comments_by_ego(dict_of_commenters_per_status):
    result = {}
    for status in dict_of_commenters_per_status:
        result[status] = 0
        for commenter in dict_of_commenters_per_status[status]:
            if commenter == 0:
                result[status] += 1
    return result
            
def dict_of_number_of_commenters(dict_of_commenters_per_status):
    dict_ego = dict_of_number_of_comments_by_ego(dict_of_commenters_per_status)
    result = {}
    for status in dict_of_commenters_per_status:
        result[status] = len(dict_of_commenters_per_status[status])
        if dict_ego[status] != 0:
            result[status] -= 1
    return result

def sorted_list_of_status(dict_ego, dict_commenters):
    result = []
    for status in dict_commenters:
        result.append((status, dict_commenters[status], dict_ego[status]))
    result.sort(key=lambda tup: tup[1], reverse = True) 
    return result        