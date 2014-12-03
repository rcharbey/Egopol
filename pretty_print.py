import os
import csv

def read_csv(name):
    if not os.path.isfile(name):
        return [0]*30
    csv_file = open(name, 'rb')
    reader = csv.reader(csv_file, delimiter=';')
    result = []
    for line in reader:
        result.append(line)
    return result

def create_list_colors(patterns_table):
    temp = []
    for elem in patterns_table:
        temp.append(elem)
        
    colors = []
    prev_max = None
    suppressed_elem = 0
    while suppressed_elem < len(temp):
        max = -1
        for elem in temp:
            if elem > max :
                if prev_max == None or elem < prev_max:
                    max = elem
        colors.append([])
        for i in range(0, len(temp)):
            if temp[i] == max:
                colors[len(colors) - 1].append(i)
                suppressed_elem += 1
        prev_max = max
    
    result = [0]*len(patterns_table)
    for j in range(0, len(colors)):
        for pat in colors[j]:
            red = int(255-j*(255/float(len(colors))))
            if red < 10:
                str_red = '00'+str(red)
            elif red < 100:
                str_red = '0'+str(red)
            else:
                str_red = str(red)
            result[pat] = '('+str_red+',0,0)'
   
    return result

def print_begin(fichier):
    fichier.write('<!DOCTYPE html>')
    fichier.write('\n')
    fichier.write('<html>')
    fichier.write('\n\n')
    fichier.write('<body>')
    fichier.write('\n')
    
def appearance_pattern(patterns_enumeration, i, file_html, colors):
    file_html.write('<td style = "color:rgb')
    if patterns_enumeration[i-1] == 0:
        file_html.write('(000,0,0)')
    else:
        file_html.write(colors[i-1])
    file_html.write('">'+str(patterns_enumeration[i-1]))

def image_pattern(path_patterns, i, file_html):
    file_html.write('<td><img src="'+path_patterns+'/pattern')
    if i < 10:
        file_html.write('0')
    file_html.write(str(i)+'.svg" width="70" height = "70" alt="pattern')
    if i < 10:
        file_html.write('0')
    file_html.write(str(i)+'"></td>')

def enumeration(file_html, infos, path_patterns):
    colors = create_list_colors(infos[0])
    print_begin(file_html)
    
    file_html.write('<table style="width:100%">')
    
    for i in range(1, len(infos[0])+1):
        file_html.write('<tr>\n')
        image_pattern(path_patterns, i, file_html)
        appearance_pattern(infos[0], i, file_html, colors)
        
        j = 1
        while len(infos) > j:
            file_html.write(' ('+str(infos[j][i-1])+')')
            j += 1
            
        file_html.write('</td>\n')
        file_html.write('</tr>')
        file_html.write('\n')
    
    file_html.close()  
    
def main():
    for quality in ['aggregation_patterns_induced_friends', 'aggregation_patterns_induced_statuses', 'aggregation_patterns_friends', 'aggregation_patterns_statuses']:
        name = 'GALLERY/'+quality
        if os.path.isfile(name+'.csv'):
            enumeration(open(name + '.html', 'w'), read_csv(name + '.csv'), 'PATTERNS')
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders: 
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            path = 'GALLERY/'+folder+'/'+ego+'/'
            for quality in ['patterns_friends', 'patterns_statuses']:
                name = path + quality
                if os.path.isfile(name+'.csv'):
                    enumeration(open(name + '.html', 'w'), read_csv(name + '.csv'), '../../PATTERNS')
            if not os.path.isdir(path+'statuses'):
                continue
            path = path + 'statuses/'
            for quality in ['aggregation_patterns_induced_friends', 'aggregation_patterns_induced_statuses']:
                name = path + quality
                if os.path.isfile(name+'.csv'):
                    enumeration(open(name + '.html', 'w'), read_csv(name + '.csv'), '../../../PATTERNS')
            list_statuses = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            for status in list_statuses:
                for quality in ['patterns_induced_friends', 'patterns_induced_statuses']:
                    name = path + status + '/' + quality
                    if os.path.isfile(name+'.csv'):
                        enumeration(open(name + '.html', 'w'), read_csv(name + '.csv'), '../../../../PATTERNS')