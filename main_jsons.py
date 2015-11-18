# -*- coding: utf-8 -*-

import sys
sys.path.append('./Jsons')
import read_friends
import read_statuses
import read_ego
import read_qualify
import os
from os import path

def dict_of_mutual_friends(folder, ego):
    return read_friends.dict_of_mutual(folder, ego)

def print_list_of_commenters(folder, ego):
    list_of_friends = read_friends.list_of_friends(folder, ego)
    read_statuses.print_list_of_commenters(folder, ego, list_of_friends)

def read_list_of_commenters(folder, ego):
    print_list_of_commenters(folder, ego)
    return read_statuses.read_list_of_commenters(folder, ego)

def create_correspondence_table(folder, ego):
    return read_friends.create_correspondence_table(folder, ego)

def list_of_friends(folder, ego):
    return read_friends.list_of_friends(folder, ego)

def calculate_info_commenters(folder, ego):
    return read_statuses.calculate_info_commenters(folder, ego)

def calculate_info_likers(folder, ego):
    return read_statuses.calculate_info_likers(folder, ego)

def calculate_info_likers_of_comment(folder, ego):
    return read_statuses.calculate_info_likers_of_comment(folder, ego)

def calculate_dict_of_commenters_per_status(folder, ego):
    return read_statuses.dict_of_commenters_per_status(folder, ego)

def calculate_dict_of_likers_per_status(folder, ego):
    return read_statuses.dict_of_likers_per_status(folder, ego)

def calculate_dict_of_likers_of_comments_per_status(folder, ego):
    return read_statuses.dict_of_likers_of_comments_per_status(folder, ego)

def find_status(folder, ego, id):
    return read_statuses.find_status(folder, ego, id)

def find_friend(folder, ego, id):
    return read_friends.find_friend(folder, ego, id)

def list_of_liked_pages(folder, ego):
    return read_ego.list_of_liked_pages(folder, ego)

def list_of_qualified(folder, ego):
    return read_qualify.list_of_qualified(folder, ego)

def gt_and_activity(folder, ego):
    return read_statuses.gt_and_activity(folder, ego)

def gt_per_status(folder, ego):
    return read_statuses.gt_per_status(folder, ego)

def dict_of_commenters_per_status(folder, ego):
    return read_statuses.dict_of_commenters_per_status(folder, ego)

def dict_of_likers_per_status(folder, ego):
    return read_statuses.dict_of_likers_per_status(folder, ego)