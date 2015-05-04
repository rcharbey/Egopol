import os
import sys
sys.path.append('Proportion')

import prop_patterns
import prop_positions

def main():
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders:
        dirname = 'GALLERY/'+folder
        list_ego = [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]
        for ego in list_ego:
            #prop_patterns.add_aggregation_data(folder, ego, 'friends')
            #prop_patterns.add_aggregation_data(folder, ego, 'statuses')
            prop_patterns.add_aggregation_data(folder, ego, 'friends_fc')
            #prop_positions.add_aggregation_data(folder, ego, 'friends')
            #prop_positions.add_aggregation_data(folder, ego, 'statuses')
            prop_positions.add_aggregation_data(folder, ego, 'friends_fc')
            if os.path.isdir(dirname+'/'+ego+'/statuses'):
                prop_patterns.add_aggregation_data(folder, ego, 'induced_friends', True)
                
main()