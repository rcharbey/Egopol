import csv
import os

def read_csv(name):
    if not os.path.isfile(name):
        return [0]*73
    csv_file = open(name, 'rb')
    reader = csv.reader(csv_file, delimiter=';')
    result = [0]*73
    for line in reader:
        for i in range(0, len(line)):
            result[i] += int(line[i])
    return result

def refresh_aggregation(name, positions_enumeration):
    if os.path.isfile(name):
        prev = read_csv(name)
    else:
        prev = [0]*len(positions_enumeration)
    new_aggregation = [0]*len(positions_enumeration)
    for i in range(0, len(positions_enumeration)):
        new_aggregation[i] = int(prev[i]) + int(positions_enumeration[i])
    csv_file = open(name, 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(new_aggregation)

def aggregate(quality):
    list_folders = [f for f in os.listdir('GALLERY') if os.path.isdir(os.path.join('GALLERY', f))]
    if os.path.isfile('GALLERY/aggregation_positions_'+quality+'.csv'):
        os.remove('GALLERY/aggregation_positions_'+quality+'.csv')
    csv_file = open('GALLERY/aggregation_positions_'+quality+'.csv', 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow([0]*30)
    csv_file.close()
    for folder in list_folders: 
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            if os.path.isfile('GALLERY/'+folder+'/'+ego + '/Enumeration/CSV/positions_'+quality+'.csv'):
                positions_enumeration = read_csv('GALLERY/'+folder+'/'+ego + '/Enumeration/CSV/positions_'+quality+'.csv')
            else:
                continue
            refresh_aggregation('GALLERY/aggregation_positions_'+quality+'.csv', positions_enumeration)

aggregate('friends')
#aggregate('commenters')