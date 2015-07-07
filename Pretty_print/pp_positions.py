import utilities
import csv
import os
import sys
from igraph import *

nb_of_positions_per_pattern = [1, 2, 1, 2, 2, 3, 1,  2,  1,  3,  2,  4,  4,  3,  3,  1,  4,  4,  4,  2,  3,  2,  3,  3,  2,  3,  2,  3, 2, 1]
pattern_to_first_position =   [0, 1, 3, 4, 6, 8, 11, 12, 14, 15, 18, 20, 24, 28, 31, 34, 35, 39, 43, 47, 49, 52, 54, 57, 60, 62, 65, 67, 70, 72]

def int_to_colors(i):
    colors = [['blue'], ['black', 'red'], ['black', 'green', 'red'], ['black', 'blue', 'green', 'red']]
    return colors[i-1]

def read_enumeration(path, quality):
    """
        read_enumeration returns the enumeration of positions in the file path+quality.csv
        if this file does not exist, it returns [] instead
    """
    file_to_read = path+'CSV/positions_'+quality+'.csv'
    if not os.path.isfile(file_to_read):
        return []
    reader = csv.reader(open(file_to_read, 'rb'), delimiter=';')
    result = []
    for line in reader:
        result.append(line)
    return result

def read_proportion(path, quality):
    file_to_read = path+'CSV/proportion_positions_'+quality+'.csv'
    if not os.path.isfile(file_to_read):
        return -1
    reader = csv.reader(open(file_to_read, 'rb'), delimiter=';')
    result = []
    for line in reader:
        result.append(line)
    return result

def pretty_print(path, quality, path_images, list_friends):
    enumeration = read_enumeration(path, quality)
    
    enumeration_sorted = []
    for i in range(0, len(enumeration)):
        added = False
        for i_sorted in range(0, len(enumeration_sorted)):
            if int(enumeration[i][0]) > int(enumeration[enumeration_sorted[i_sorted]][0]):
                enumeration_sorted.insert(i_sorted, i)
                added = True
                break
        if added == False:
            enumeration_sorted.append(i)
    
    colors_enumeration = []
    for elem in enumeration:
        colors_enumeration.append(utilities.create_list_colors(elem))
    
    proportion = read_proportion(path, quality)
    if proportion != -1:
        colors_proportion = []
        for elem in proportion:
            colors_proportion.append(utilities.create_list_colors(elem))
    if quality == 'statuses':
        quality_2 = 'commenters'
    else:
        quality_2 = quality
    if os.path.isfile(path+quality_2+'.gml'):
        graph = Graph.Load(path+quality_2+'.gml')
    if not os.path.isdir(path+'HTML'):
        os.mkdir(path+'HTML')
    file_html = open(path+'HTML/positions_'+quality+'.html', 'wb')
    
    utilities.print_begin(file_html)
    file_html.write('<table style="width:100%">')
    file_html.write('\n<tr>\n')
    file_html.write('   <td colspan = "3" ></td>')
    cmpt = 1
    for index_alter in enumeration_sorted:
        if cmpt%10 == 0:
            file_html.write('<td> </td>')
        file_html.write('<td colspan = "2" align = "center">'+list_friends[index_alter].encode('utf-8')+'</td>')
        cmpt += 1
    file_html.write('</tr>\n')        
    
    for index_pattern in range(0, 30):
        nb_of_positions = nb_of_positions_per_pattern[index_pattern]
        if index_pattern%10 == 0 and index_pattern != 0:
            file_html.write('\n<tr>\n')
            file_html.write('   <td colspan = "3" ></td>')
            cmpt = 1
            print enumeration_sorted
            for index_alter in enumeration_sorted:
                print index_alter,
                print ' : ',
                print graph.vs[index_alter],
                print ' ',
                print raph.vs[index_alter].degree() 
                if cmpt%10 == 0:
                    file_html.write('<td> </td>')
                file_html.write('<td colspan = "2" align = "center">'+list_friends[index_alter].encode('utf-8')+'</td>')
                cmpt += 1
            file_html.write('</tr>\n')
        file_html.write('<tr>\n')
        utilities.image(path_images, index_pattern, file_html, nb_of_positions)
        for index_position in range(0, nb_of_positions):
            if index_position != 0:
                file_html.write('\n<tr>')
            file_html.write('<td>'+str(pattern_to_first_position[index_pattern] + index_position + 1)+'</td>')
            file_html.write('   <td style="width:20px" bgcolor="'+str(int_to_colors(nb_of_positions)[index_position])+'">\n </td>')
            cmpt = 1
            for index_alter in enumeration_sorted:
                if cmpt%10 == 0 and index_position == 0:
                    utilities.image(path_images, index_pattern, file_html, nb_of_positions)
                cmpt += 1
                index_color = pattern_to_first_position[index_pattern] + index_position
                file_html.write('   ')
                utilities.appearance(enumeration[index_alter][index_color], file_html, colors_enumeration[index_alter][index_color])
            
                if proportion != -1:
                    file_html.write('<td class="ratio" style = "color:rgb')
                    if proportion[index_alter][pattern_to_first_position[index_pattern] + index_position] == 0:
                        file_html.write('(000,0,0)')
                    else:
                        file_html.write(colors_proportion[index_alter][index_color])
                    file_html.write('">('+str(proportion[index_alter][pattern_to_first_position[index_pattern] + index_position]))
                    file_html.write(')</td>')
                else:
                    file_html.write('<td class="ratio"> </td>')
            file_html.write('</tr>')
        file_html.write('<tr><td colspan = "'+str((len(enumeration))*2)+'"></td></tr>')
            
        file_html.write('\n')
        
    cmpt = 1
    file_html.write('   <td colspan = "3" ></td>')
    for index_alter in enumeration_sorted:
        if cmpt%10 == 0:
            file_html.write('<td> </td>')
        file_html.write('<td colspan = "2" align = "center">'+list_friends[index_alter].encode('utf-8')+'</td>')
        cmpt += 1
    file_html.write('</tr>\n')
    
    file_html.close() 
