import os
import csv    
import sys
 
def read_csv(name):
    if not os.path.isfile(name):
        return [0]*30
    csv_file = open(name, 'rb')
    reader = csv.reader(csv_file, delimiter=';')
    result = []
    place = 0
    for line in reader:
        return line

def refresh_aggregation(name, patterns_enumeration):
    if os.path.isfile(name):
        prev = read_csv(name)
    else :
        prev = [0]*len(patterns_enumeration)
    new_aggregation = [0]*len(patterns_enumeration)
    for i in range(0, len(patterns_enumeration)):
        new_aggregation[i] = int(prev[i]) + int(patterns_enumeration[i])
    csv_file = open(name, 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(new_aggregation)
    
def aggregate(quality):
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders: 
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            if os.path.isfile('GALLERY/'+folder+'/'+ego + '/patterns_'+quality+'.csv'):
                patterns_enumeration = read_csv('GALLERY/'+folder+'/'+ego + '/patterns_'+quality+'.csv')
            else:
                return
            refresh_aggregation('GALLERY/aggregation_patterns_'+quality+'.csv', patterns_enumeration)
       
def aggregate_status(quality):
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders: 
        dirname = 'GALLERY/'+folder
        list_ego = [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]
        for ego in list_ego:
            path = dirname+'/'+ego
            if not os.path.isdir(path+'/statuses'):
                continue
            list_statuses = [f for f in os.listdir(path+'/statuses') if os.path.isdir(os.path.join(path+'/statuses', f))]
            for status in list_statuses:
                patterns_enumeration = read_csv(path+'/statuses/'+status+'/patterns_'+quality+'.csv')
                refresh_aggregation('GALLERY/aggregation_patterns_'+quality+'.csv', patterns_enumeration)
                refresh_aggregation(path+'/statuses/aggregation_patterns_'+quality+'.csv', patterns_enumeration)
       
def calculate_sum(patterns_enumeration):
    result = 0
    for elem in patterns_enumeration:
        result += int(elem)
    return result

def calculate_proportion(aggregation, patterns_enumeration):
    result = []
        
    sum_agreg = calculate_sum(aggregation)
    sum_current = calculate_sum(patterns_enumeration)        
        
    if sum_current != 0 and sum_agreg != 0:
        for i in range(0, len(patterns_enumeration)):
            prop_pattern_current = int(patterns_enumeration[i])/float(sum_current)
            prop_pattern_general = int(aggregation[i])/float(sum_agreg)
            if prop_pattern_general != 0:
                result.append(round(prop_pattern_current/prop_pattern_general,2))
            else:
                result.append(0)
    
    else:
        result = [0]*len(patterns_enumeration)
        
    return result

def add_aggregation_data(folder, ego, quality, statuses = False):
    if statuses :
        patch = 'statuses/aggregation_'
    else:
        patch = ''
    if os.path.isfile('GALLERY/'+folder+'/'+ego+'/'+patch+'patterns_'+quality+'.csv'):
        enumeration = read_csv('GALLERY/'+folder+'/'+ego+'/'+patch+'patterns_'+quality+'.csv')
    else:
        return
    if os.path.isfile('GALLERY/aggregation_patterns_'+quality+'.csv'):
        aggregation = read_csv('GALLERY/aggregation_patterns_'+quality+'.csv')
    else:
        aggregation = [0]*len(enumeration)
    proportion = calculate_proportion(aggregation, enumeration)
    csv_enumeration = open('GALLERY/'+folder+'/'+ego+'/'+patch+'patterns_'+quality+'.csv', 'wb')
    writer = csv.writer(csv_enumeration, delimiter = ';')
    writer.writerow(enumeration)
    writer.writerow(proportion)
    
def add_aggregation_data_all():
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders:
        dirname = 'GALLERY/'+folder
        list_ego = [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]
        for ego in list_ego:
            add_aggregation_data(folder, ego, 'friends')
            add_aggregation_data(folder, ego, 'statuses')
            if os.path.isdir(dirname+'/'+ego+'/statuses'):
                add_aggregation_data(folder, ego, 'induced_friends', True)
            
def read_html(file_html):
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
        
def html_to_csv(quality):
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders: 
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            path = 'GALLERY/'+folder+'/'+ego
            if quality == 'induced_friends':
                if not os.path.isdir(path+'/statuses'):
                    continue
                list_statuses = [f for f in os.listdir(path+'/statuses/') if os.path.isdir(os.path.join(path+'/statuses/', f))]
                for status in list_statuses:
                    if os.path.isfile(path+'/statuses/'+ status +'/patterns_induced_friends_induced.html'):
                        file_html = open(path+'/statuses/'+status+'/patterns_induced_friends_induced.html', 'r')
                        result = read_html(file_html)
                        csv_file = open(path+'/statuses/'+status+'/patterns_'+quality+'.csv', 'wb')
                        writer = csv.writer(csv_file, delimiter=';')
                        writer.writerow(result) 
            if os.path.isfile(path+'/patterns_'+quality+'.html'):
                file_html = open(path+'/patterns_'+quality+'.html', 'r')
                result = read_html(file_html)
                if quality == 'commenters':
                    csv_file = open(path+'/patterns_statuses.csv', 'wb')
                else:
                    csv_file = open(path+'/patterns_'+quality+'.csv', 'wb')
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(result)  

def main():
    html_to_csv('friends')
    html_to_csv('commenters')
    html_to_csv('induced_friends')
    aggregate('friends')
    aggregate('statuses')
    aggregate_status('induced_friends')
    add_aggregation_data_all()
    
main()