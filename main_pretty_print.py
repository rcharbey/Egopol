import os
import sys
sys.path.append('%s/Egopol/Pretty_print' % os.path.expanduser("~"))

import pp_patterns
import pp_positions
import main_jsons
import pp_gt_graphs

def extract_friends(folder, ego):
    pp_positions.pretty_print_extraction('GALLERY/%s/%s/Enumeration/' % (folder, ego), '../../../../PATTERNS')

def gt_pretty_print(folder, ego):
    pp_gt_graphs.pretty_print(folder, ego)

def main():
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    print list_folders
    for folder in list_folders:
        if folder != 'entretiens':
            continue
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        print list_ego
        for ego in list_ego:
            print 'pretty print : ',
            print ego
            list_friends = main_jsons.list_of_friends(folder, ego)
            path = 'GALLERY/'+folder+'/'+ego+'/'
            for quality in ['friends', 'commenters', 'friends_fc']:
                pp_patterns.pretty_print(path+'Enumeration/', quality, '../../../../PATTERNS')
                pp_positions.pretty_print(path+'Enumeration/', quality, '../../../../PATTERNS', list_friends)
            if not os.path.isdir(path+'Statuses'):
                continue
            path = path + 'Statuses/'
            for quality in ['_induced_friends', '_induced_statuses']:
                pp_patterns.pretty_print(path+'aggregation_', quality, '../../../PATTERNS')
            list_statuses = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            for status in list_statuses:
                for quality in ['_induced_friends', '_induced_statuses']:
                    pp_patterns.pretty_print(path+status+'/', quality, '../../../../PATTERNS')

