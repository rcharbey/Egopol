import os

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
    
 
def previous_enumeration(quality, path):
    if not os.path.isfile(path+'/aggregation_patterns_'+quality+'.html'):
        return [0]*30
    aggregation_file = open(path+'/aggregation_patterns_'+quality+'.html', 'r')
    result = []
    place = 0
    for line in aggregation_file:
        current_value = ''
        if len(line) > 100:
            if place == 0:
                for j in range(0, len(line)) :
                    if line[j] == ')':
                        place = j + 3
            i = place
            while line[i] != '<':
                current_value += line[i]
                i += 1
            result.append(current_value)
    return result 

def previous_enumeration_aggregation(file_html):
    result = []
    place = 0
    for line in file_html:
        current_value = ''
        if len(line) > 100:
            if place == 0:
                for j in range(0, len(line)) :
                    if line[j] == ')':
                        place = j + 3
                        break
            i = place
            while line[i] >= '0' and line[i] <= '9':
                current_value += line[i]
                i += 1
            result.append(current_value)
    return result 
 
def calculate_sum(enumeration):
    result = 0
    for elem in enumeration:
        result += int(elem)
    return result

def calculate_proportion(quality, patterns_enumeration, path):
    result = []
    prev_enumeration = previous_enumeration(quality, path)
        
    sum_agreg = calculate_sum(prev_enumeration)
    sum_current = calculate_sum(patterns_enumeration)        
        
    if sum_current != 0 and sum_agreg != 0:
        for i in range(0, len(patterns_enumeration)):
            prop_pattern_current = patterns_enumeration[i]/float(sum_current)
            prop_pattern_general = int(prev_enumeration[i])/float(sum_agreg)
            if prop_pattern_general != 0:
                result.append(round(prop_pattern_current/prop_pattern_general,2))
            else:
                result.append(0)
    
    else:
        result = [0]*len(patterns_enumeration)
        
    return result 
    
def list_of_elem_already_saw(file_html):
    result = []
    for line in file_html:
        if line[0:3] != '<!-':
            return result
        elem = ''
        i = 5
        while (i < len(line) and line[i] != ' '):
            elem += line[i]
            i += 1
        result.append(elem)
    return result