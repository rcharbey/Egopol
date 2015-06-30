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

def create_list_colors(table):
    temp = []
    for elem in table:
        temp.append(elem)
        
    colors = []
    prev_max = None
    suppressed_elem = 0
    while suppressed_elem < len(temp):
        maximum = -1
        for elem in temp:
            if float(elem) > float(maximum) :
                if prev_max == None or float(elem) < float(prev_max):
                    maximum = elem
        colors.append([])
        for i in range(0, len(temp)):
            if temp[i] == maximum:
                colors[len(colors) - 1].append(i)
                suppressed_elem += 1
        prev_max = maximum
    
    result = [0]*len(table)
    for j in range(0, len(colors)):
        for color in colors[j]:
            red = int(255-j*(255/float(len(colors))))
            if red < 10:
                str_red = '00'+str(red)
            elif red < 100:
                str_red = '0'+str(red)
            else:
                str_red = str(red)
            result[color] = '('+str_red+',0,0)'
   
    return result

def print_begin(fichier):
    fichier.write('<!DOCTYPE html>')
    fichier.write('\n')
    fichier.write('<html>')
    fichier.write('\n\n')
    fichier.write('<body>')
    fichier.write('\n')
    
def appearance_pattern(pattern_appearance, file_html, color):
    file_html.write('<td style = "color:rgb')
    if pattern_appearance == 0:
        file_html.write('(000,0,0)')
    else:
        file_html.write(str(color))
    file_html.write('">'+str(pattern_appearance))
    file_html.write('</td>')

def image_pattern(path_patterns, i, file_html):
    file_html.write('<td><img src="'+path_patterns+'/pattern')
    if i+1 < 10:
        file_html.write('0')
    file_html.write(str(i+1)+'.svg" width="70" height = "70" alt="pattern')
    if i+1 < 10:
        file_html.write('0')
    file_html.write(str(i+1)+'"></td>')

def enumeration(file_html, infos, path_patterns):
    """
            enumeration writes the content of infos in file_html.
            it uses the colors computed by create_list_colors and picks the images in path_patterns
            it works for both patterns and positions (but only for one alter this far)
    """
    colors = create_list_colors(infos[0])
    if len(infos) > 1:
        colors_significativity = create_list_colors(infos[1])
    print_begin(file_html)
    
    file_html.write('<table style="width:100%">')
    
    for i in range(1, len(infos[0])):
        file_html.write('<tr>\n')
        image_pattern(path_patterns, i, file_html)
        appearance_pattern(infos[0][i], file_html, colors)
        
        j = 1
        while len(infos) > j:
            file_html.write('<td style = "color:rgb')
            if infos[j][i-1] == 0:
                file_html.write('(000,0,0)')
            else:
                file_html.write(colors_significativity[i-1])
            file_html.write('">'+str(infos[j][i-1]))
            file_html.write('</td>')
            j += 1
            
        file_html.write('\n')
        file_html.write('</tr>')
        file_html.write('\n')
    
    file_html.close()  
    
def status(folder, ego, list_of_statuses):
    if not os.path.isdir('GALLERY/'+folder):
        os.mkdir('GALLERY/'+folder)
    if not os.path.isdir('GALLERY/'+folder+'/'+ego):
        os.mkdir('GALLERY/'+folder+'/'+ego)
        
    fichier = open('GALLERY/'+folder+'/'+ego+'/resultats_status.html',"w")
    print_begin(fichier)
    
    fichier.write('<table style="width:100%">')
    fichier.write('<tr>\n')
    
    fichier.write('<td>Id du status</td><td>nombre de commentateurs</td><td>nombre de commentaires de ego</td>\n')
    fichier.write('</tr>')
    
    result = []
    
    for status in list_of_statuses:
        if status[1] - status[2] > 2:
            result.append(status)
            fichier.write('<tr>')
            fichier.write('<td>'+str(status[0])+'</td><td>'+str(status[1])+'</td><td>'+str(status[2])+'</td>')
            fichier.write('</tr>')
            
    return result
    
def main():
    #for quality in ['aggregation_patterns_induced_friends', 'aggregation_patterns_induced_statuses', 'aggregation_patterns_friends', 'aggregation_patterns_statuses']:
        #name = 'GALLERY/'+quality
        #if os.path.isfile(name+'.csv'):
            #enumeration(open(name + '.html', 'w'), read_csv(name + '.csv'), 'PATTERNS')
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    print list_folders
    for folder in list_folders: 
        if folder != 'all_2015-05-15':
            continue
        print folder
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            if not 'ea37' in ego:
                continue
            print 'pretty print : ',
            print ego
            path = 'GALLERY/'+folder+'/'+ego+'/Enumeration/'
            for quality in ['patterns_friends', 'patterns_statuses']:
                name_csv = path + 'CSV/' + quality + '.csv'
                name_html = path + 'HTML/' + quality + '.html'
                if os.path.isfile(name_csv):
                    enumeration(open(name_html, 'w'), read_csv(name_csv), '../../../../PATTERNS')
            #if not os.path.isdir(path+'statuses'):
                #continue
            #path = path + 'statuses/'
            #for quality in ['aggregation_patterns_induced_friends', 'aggregation_patterns_induced_statuses']:
                #name = path + quality
                #if os.path.isfile(name+'.csv'):
                    #enumeration(open(name + '.html', 'w'), read_csv(name + '.csv'), '../../../PATTERNS')
            #list_statuses = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            #for status in list_statuses:
                #for quality in ['patterns_induced_friends', 'patterns_induced_statuses']:
                    #name = path + status + '/' + quality
                    #if os.path.isfile(name+'.csv'):
                        #enumeration(open(name + '.html', 'w'), read_csv(name + '.csv'), '../../../../PATTERNS')    