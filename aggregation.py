import os
import csv    
import sys
 
def read_csv(name):
    if not os.path.isfile(name):
        return [0]*30
    csv_file = open(name, 'rb')
    reader = csv.reader(csv_file, delimiter=';')
    for line in reader:
        return line

def refresh_aggregation(name, patterns_enumeration):
    if os.path.isfile(name):
        prev = read_csv(name)
    else:
        prev = [0]*len(patterns_enumeration)
    new_aggregation = [0]*len(patterns_enumeration)
    for i in range(0, len(patterns_enumeration)):
        new_aggregation[i] = int(prev[i]) + int(patterns_enumeration[i])
    csv_file = open(name, 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(new_aggregation)
    
def aggregate(quality):
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    if os.path.isfile('GALLERY/aggregation_patterns_'+quality+'.csv'):
        os.remove('GALLERY/aggregation_patterns_'+quality+'.csv')
    csv_file = open('GALLERY/aggregation_patterns_'+quality+'.csv', 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow([0]*30)
    csv_file.close()
    for folder in list_folders: 
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            if os.path.isfile('GALLERY/'+folder+'/'+ego + '/Enumeration/CSV/patterns_'+quality+'.csv'):
                patterns_enumeration = read_csv('GALLERY/'+folder+'/'+ego + '/Enumeration/CSV//patterns_'+quality+'.csv')
            else:
                continue
            refresh_aggregation('GALLERY/aggregation_patterns_'+quality+'.csv', patterns_enumeration)
       
def aggregate_status(quality):
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    os.remove('GALLERY/aggregation_patterns_'+quality+'.csv',) 
    for folder in list_folders: 
        dirname = 'GALLERY/'+folder
        list_ego = [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]
        for ego in list_ego:
            path = dirname+'/'+ego
            if not os.path.isdir(path+'/statuses'):
                continue
            os.remove(path+'/statuses/aggregation_patterns_'+quality+'.csv',)
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
    if os.path.isfile('GALLERY/'+folder+'/'+ego+'/Enumeration/CSV/'+patch+'patterns_'+quality+'.csv'):
        enumeration = read_csv('GALLERY/'+folder+'/'+ego+'/Enumeration/CSV/'+patch+'patterns_'+quality+'.csv')
    else:
        return
    if os.path.isfile('GALLERY/aggregation_patterns_'+quality+'.csv'):
        aggregation = read_csv('GALLERY/aggregation_patterns_'+quality+'.csv')
    else:
        aggregation = [0]*len(enumeration)
    proportion = calculate_proportion(aggregation, enumeration)
    csv_enumeration = open('GALLERY/'+folder+'/'+ego+'/Enumeration/CSV/'+patch+'patterns_'+quality+'.csv', 'wb')
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
            add_aggregation_data(folder, ego, 'friends_fc')
            if os.path.isdir(dirname+'/'+ego+'/statuses'):
                add_aggregation_data(folder, ego, 'induced_friends', True)

if __name__ == '__main__':
    #aggregate('friends')
    aggregate('friends_fc')
    #aggregate('statuses')
    #aggregate_status('induced_friends')
    add_aggregation_data_all()