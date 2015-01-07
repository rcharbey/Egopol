def image(path_to_images, i, file_html, rowspan = 1):
    file_html.write('<td rowspan = "'+str(rowspan)+'"><img src="'+path_to_images+'/pattern')
    if i+1 < 10:
        file_html.write('0')
    file_html.write(str(i+1)+'.svg" width="70" height = "70" alt="image')
    if i+1 < 10:
        file_html.write('0')
    file_html.write(str(i+1)+'"></td>')
    
def appearance(number, file_html, color):
    file_html.write('<td style = "color:rgb')
    if number == 0:
        file_html.write('(000,0,0)')
    else:
        file_html.write(color)
    file_html.write('">'+str(number))
    file_html.write('</td>')
    
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