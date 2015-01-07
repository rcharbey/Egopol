import csv
import utilities
import os

def read_enumeration(path, quality):
    """
        read_enumeration returns the enumeration of patterns in the file path+patterns_+quality.csv
        if this file does not exist, it returns [0]*30 instead
    """
    file_to_read = path+'patterns_'+quality+'.csv'
    if not os.path.isfile(file_to_read):
        return [0]*30
    reader = csv.reader(open(file_to_read, 'rb'), delimiter=';')
    result = []
    for line in reader:
        result.append(line)
        break
    return result[0]

def read_proportion(path, quality):
    file_to_read = path+'proportion_patterns_'+quality+'.csv'
    if not os.path.isfile(file_to_read):
        return -1
    reader = csv.reader(open(file_to_read, 'rb'), delimiter=';')
    result = []
    for line in reader:
        result.append(line)
        break
    return result[0]
    
def pretty_print(path, quality, path_images):
    file_html = open(path+'patterns_'+quality+'.html', 'wb')
    
    enumeration = read_enumeration(path, quality)
    colors_enumeration = utilities.create_list_colors(enumeration)
    
    proportion = read_proportion(path, quality)
    if proportion != -1:
        colors_proportion = utilities.create_list_colors(proportion)
    
        
    utilities.print_begin(file_html)
    file_html.write('<table style="width:100%">')
    
    for i in range(0, len(enumeration)):
        file_html.write('<tr>\n')
        utilities.image(path_images, i, file_html)
        utilities.appearance(enumeration[i], file_html, colors_enumeration[i])
        
        if proportion != -1:
            file_html.write('<td style = "color:rgb')
            if proportion[i] == 0:
                file_html.write('(000,0,0)')
            else:
                file_html.write(colors_proportion[i])
            file_html.write('">'+str(proportion[i]))
            file_html.write('</td>')
            
        file_html.write('\n')
        file_html.write('</tr>')
        file_html.write('\n')
    
    file_html.close() 