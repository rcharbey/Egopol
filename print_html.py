import os
import read_html

def begin(fichier):
    fichier.write('<!DOCTYPE html>')
    fichier.write('\n')
    fichier.write('<html>')
    fichier.write('\n\n')
    fichier.write('<body>')
    fichier.write('\n')
    
def end(fichier):
    fichier.write('\n')
    fichier.write('</body>')
    fichier.write('\n')
    fichier.write('</html>')

def appearance_pattern(patterns_enumeration, i, file_html):
    colors = read_html.create_list_colors(patterns_enumeration)
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

def enumeration(file_html, quality, patterns_enumeration, path_patterns, aggregation = False, path_aggregation = None):
    begin(file_html)
    if aggregation == False:
        tab_proportion = read_html.calculate_proportion(quality, patterns_enumeration, path_aggregation)
    
    file_html.write('<table style="width:100%">')
            
    for i in range(1, len(patterns_enumeration)+1):
        file_html.write('<tr>\n')
        image_pattern(path_patterns, i, file_html)
        appearance_pattern(patterns_enumeration, i, file_html)
        
        if aggregation == False:
            file_html.write(' ('+str(tab_proportion[i-1])+')')
            
        file_html.write('</td>\n')
        file_html.write('</tr>')
        file_html.write('\n')
    
    file_html.close()  
        
def aggregation(elem_to_add, quality, patterns_enumeration, path, path_patterns, to_aggregate):
    if os.path.isfile(path+'/aggregation_patterns_'+quality+'.html'):
        file_html = open(path+'/aggregation_patterns_'+quality+'.html', "r")
        list_of_elem = read_html.list_of_elem_already_saw(file_html)
        prev_enumeration = read_html.previous_enumeration_aggregation(file_html)
        file_html.close()
    else:
        list_of_elem = []
        prev_enumeration = [0]*len(patterns_enumeration)
    if elem_to_add in list_of_elem:
        return
    file_html = open(path+'/aggregation_patterns_'+quality+'.html', "w")
    for already_saw in list_of_elem:
        file_html.write('<!-- '+already_saw+' -->\n')
    file_html.write('<!-- '+elem_to_add+' -->\n')
    aggregated_enumeration = [0]*len(patterns_enumeration)
    i = 0
    while i<len(patterns_enumeration):
        aggregated_enumeration[i] = patterns_enumeration[i] + int(prev_enumeration[i])
        i += 1
    if to_aggregate != None:
        enumeration(file_html, quality, aggregated_enumeration, path_patterns, False, './GALLERY')
    else:
        enumeration(file_html, quality, aggregated_enumeration, path_patterns, True)
    file_html.close()
  
def status(folder, ego, list_of_statuses):
    if not os.path.isdir('GALLERY/'+folder):
        os.mkdir('GALLERY/'+folder)
    if not os.path.isdir('GALLERY/'+folder+'/'+ego):
        os.mkdir('GALLERY/'+folder+'/'+ego)
        
    fichier = open('GALLERY/'+folder+'/'+ego+'/resultats_status.html',"w")
    begin(fichier)
    
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