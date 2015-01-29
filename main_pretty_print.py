import os
import sys
sys.path.append('./Pretty_print')

import pp_patterns
import pp_positions

def main():
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders: 
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            print 'pretty print : ',
            print ego
            path = 'GALLERY/'+folder+'/'+ego+'/'
            for quality in ['friends', 'commenters']:
                pp_patterns.pretty_print(path+'Enumeration/', quality, '../../../../PATTERNS')
                pp_positions.pretty_print(path+'Enumeration/', quality, '../../../../PATTERNS')
            if not os.path.isdir(path+'Statuses'):
                continue
            path = path + 'Statuses/'
            for quality in ['_induced_friends', '_induced_statuses']:
                pp_patterns.pretty_print(path+'aggregation_', quality, '../../../PATTERNS')
            list_statuses = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            for status in list_statuses:
                for quality in ['_induced_friends', '_induced_statuses']:
                    pp_patterns.pretty_print(path+status+'/', quality, '../../../../PATTERNS')
                    
main()
                    