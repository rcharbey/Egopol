import read_html
import print_html
import os
import sys

sys.path.append('./Indicators')
import status

def enumeration(folder, ego, quality, patterns_enumeration, path_aggregation = None):
    file_html = open_html_ego(folder, ego, quality)
    print_html.enumeration(file_html, quality, patterns_enumeration, './../../PATTERNS', False, path_aggregation)
    
    #print_patterns_enumeration(file_html, quality, patterns_enumeration, path_patterns, aggregation = False, path_aggregation = None):
    
def enumeration_induced_in_status(folder, ego, id_status, patterns_enumeration, quality, path_aggregation = None):
    file_html = open_html_status(folder, ego, id_status, quality)
    print_html.enumeration(file_html, quality, patterns_enumeration, './../../../../PATTERNS', False, path_aggregation)
    
def enumeration_all_induced(folder, ego, patterns_enumeration, quality):
    file_html = open_html_aggregation_status(folder, ego, quality)
    print_html.enumeration(file_html, quality, pattern_enumeration, './../../../PATTERNS', aggregation = True)
    
def study_statuses(folder, ego, dict_of_commenters_per_status):
    dict_of_number_of_comments_by_ego = status.dict_of_number_of_comments_by_ego(dict_of_commenters_per_status)
    dict_of_number_of_commenters = status.dict_of_number_of_commenters(dict_of_commenters_per_status)
    sorted_list = status.sorted_list_of_status(dict_of_number_of_comments_by_ego, dict_of_number_of_commenters)
    return print_html.status(folder, ego, sorted_list)

def aggregation_patterns(elem_to_add, quality, patterns_enumeration, path_aggregation = None, path_patterns = None, to_aggregate = None):
    if path_aggregation == None:
        path_aggregation = './GALLERY'
    if path_patterns == None:
        path_patterns = './PATTERNS'
    print_html.aggregation(elem_to_add, quality, patterns_enumeration, path_aggregation, path_patterns, to_aggregate)

def open_html_aggregation_galery(quality, path = None):
    if path == None:
        path = './GALLERY'
    if os.path.isfile(path+'/aggregation_patterns_'+quality+'.html'):
        file_html = open(path+'/aggregation_patterns_'+quality+'.html', "r")
    else:
        file_html = open(path+'/aggregation_patterns_'+quality+'.html', "w")
    return file_html

def open_html_ego(folder, ego, quality):
    if not os.path.isdir('GALLERY/'+folder):
        os.mkdir('GALLERY/'+folder)
    if not os.path.isdir('GALLERY/'+folder+'/'+ego):
        os.mkdir('GALLERY/'+folder+'/'+ego)
    
    file_html = open('GALLERY/'+folder+'/'+ego+'/patterns_'+quality+'.html',"w")
    return file_html

def open_html_aggregation_status(folder, ego, quality):
    if not os.path.isdir('GALLERY/'+folder):
        os.mkdir('GALLERY/'+folder)
    if not os.path.isdir('GALLERY/'+folder+'/'+ego):
        os.mkdir('GALLERY/'+folder+'/'+ego)
    if not os.path.isdir('GALLERY/'+folder+'/'+ego+'/statuses/'):
        os.mkdir('GALLERY/'+folder+'/'+ego+'/statuses/')
        
    file_html = open('GALLERY/'+folder+'/'+ego+'/statuses/patterns_induced_'+quality+'.html',"w")
    return file_html
    
def open_html_status(folder, ego, id_status, quality):
    if not os.path.isdir('GALLERY/'+folder):
        os.mkdir('GALLERY/'+folder)
    if not os.path.isdir('GALLERY/'+folder+'/'+ego):
        os.mkdir('GALLERY/'+folder+'/'+ego)
    if not os.path.isdir('GALLERY/'+folder+'/'+ego+'/statuses/'):
        os.mkdir('GALLERY/'+folder+'/'+ego+'/statuses/')    
    if not os.path.isdir('GALLERY/'+folder+'/'+ego+'/statuses/'+id_status):
        os.mkdir('GALLERY/'+folder+'/'+ego+'/statuses/'+id_status)
    
    file_html = open('GALLERY/'+folder+'/'+ego+'/statuses/'+id_status+'/patterns_induced_'+quality+'.html',"w")
    return file_html

