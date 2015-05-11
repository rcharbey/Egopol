import csv
import main_jsons
import os

folder = 'csa_2014-09-16'

list_ego = [f for f in os.listdir('DATA/'+folder) if os.path.isdir(os.path.join('DATA/'+folder, f))]
for ego in list_ego:
    file_result = open('Mehwish/commenters_per_status_'+ego+'.csv', 'wb')
    csv_file = csv.writer(file_result, delimiter = ',')
    dict = main_jsons.calculate_dict_of_commenters_per_status(folder, ego)  
    for elem in dict:
        temp = [elem]
        for commenter in dict[elem]:
            if commenter:
                temp.append(commenter.encode('utf-8'))
                temp.append(dict[elem][commenter])
        print temp
        csv_file.writerow(temp)
    file_result.close()