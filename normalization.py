# -*- coding: utf-8 -*-

import csv
import os

def create_tab_pos():
    """
    reads and returns the enumeration of positions in an array
    """
    path_to_read = path+'positions_friends.csv'
    if not os.path.isfile(path_to_read):
        return []
    file_to_read = open(path_to_read, 'rb')
    csv_reader = csv.reader(file_to_read, delimiter = ';')
    result = []
    for line in csv_reader:
        result.append([])
        for elem in line:
            result[len(result) - 1].append(int(elem))
    file_to_read.close()
    return result

def create_tab_pat():
    """
    reads and returns the enumeration of positions in an array
    """
    path_to_read = path+'patterns_friends.csv'
    if not os.path.isfile(path_to_read):
        return []
    file_to_read = open(path_to_read, 'rb')
    csv_reader = csv.reader(file_to_read, delimiter = ';')
    result = []
    for line in csv_reader:
        for elem in line:
            result.append(int(elem))
        break
    file_to_read.close()
    return result

def is_eligible(positions, k):
    """ 
    returns True if the alters appears in at least one pattern of size k
    and write in normalized_positions_friends the normalized positions of this alter
    """
    min_boundary, max_boundary = [(0, 1), (1, 3), (3, 15), (16, 73)][k-2]
        
    for position in positions[min_boundary:max_boundary]:
        if position > 0:
            pos_to_write = open(path+'normalized_positions_friends.csv', 'ab')
            csv_writer = csv.writer(pos_to_write, delimiter = ';')
            temp = [0]*min_boundary
            temp.extend(positions[min_boundary:max_boundary])
            csv_writer.writerow(temp)
            pos_to_write.close()
            return True
    if k == 3:
        pos_to_write = open(path+'normalized_positions_friends.csv', 'ab')
        csv_writer = csv.writer(pos_to_write, delimiter = ';')
        csv_writer.writerow(positions)
        pos_to_write.close()
    return False

def process_one_alter(positions, k):
    """
    k is the max size of a pattern which contains the alter
    this function returns the tab of the number of positions 
    in which the alter appears that can be removed
    """
    positions_to_visit = [[0], [0, 1, 3], [0, 1, 3, 4, 7, 10, 11, 13, 14]][k-3]
    result = []
    i = 0
    for position in positions_to_visit:
        pos_counting[positions_to_visit.index(position)] += positions[position]        

def fill_pos_counting(tab_pos):
    """
    counts the number of positions that can be removed
    """
    for alter_pos in tab_pos:
        k = 5
        while k > 2:
            if is_eligible(alter_pos, k):
                process_one_alter(alter_pos, k)
                break
            k = k-1
            
def count_number_of_patterns_to_delete():
    pattern_to_modulo = [2, 2, 3, 2, 1, 1, 4, 2, 4]
    result = []
    for pos in pos_counting:
        result.append(pos//pattern_to_modulo[pos_counting.index(pos)])
    return result

if __name__ == '__main__':
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders:
        print folder
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            path = 'GALLERY/'+folder+'/'+ego+'/Enumeration/CSV/'
            if os.path.isfile(path+'patterns_friends.csv') and os.path.isfile(path+'positions_friends.csv'):
                print folder + ' / ' + ego
                if os.path.isfile(path+'normalized_positions_friends.csv'):
                    os.remove(path+'normalized_positions_friends.csv')
                if os.path.isfile(path+'normalized_patterns_friends.csv'):
                    os.remove(path+'normalized_patterns_friends.csv')
                pos_counting = [0]*9
                pat_to_write = open(path+'normalized_patterns_friends.csv', 'wb')
                tab_pos = create_tab_pos()
                fill_pos_counting(tab_pos)
                to_delete = count_number_of_patterns_to_delete()
                normalized_pat = []
                init = create_tab_pat()
                for i in range(0,9):
                    normalized_pat.append(init[i] - to_delete[i])
                csv_writer = csv.writer(pat_to_write, delimiter = ';')
                normalized_pat.extend(init[9:])
                csv_writer.writerow(normalized_pat)
                pat_to_write.close()