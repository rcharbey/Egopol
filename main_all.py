import argparse
parser = argparse.ArgumentParser(description="main")
parser.add_argument('--folders', '-f', nargs='+')
parser.add_argument('--options', '-o', nargs='+')
parser.add_argument('--dataset', '-d', nargs='+')
args = parser.parse_args()

import sys
import os
import aggregation
import csv

import main_enumeration
import main_graphs
import main_jsons
import main_indicators
import main_pretty_print
import tarfile
import shutil
sys.path.append('../webapp')
from algopol.statuses import ParsedStatus

def clusters_per_gt(list_of_gt):
    file_name = 'matrix'
    for gt in list_of_gt:
        file_name += '_%s' % gt
    temp = ['id', 'quality']
    temp.extend(list_of_gt)
    temp.append('common clusters')
    with open('GALLERY/General/%s' % file_name, 'w') as file_to_write:
        csv_writer = csv.writer(file_to_write, delimiter = ';')
        csv_writer.writerow(temp)

def clusters_per_gt(list_of_gt):
    file_name = 'matrix'
    for gt in list_of_gt:
        file_name += '_%s' % gt
    temp = ['id']
    temp.extend(list_of_gt)
    temp.append('common clusters')
    with open('GALLERY/General/%s' % file_name, 'w') as file_to_write:
        csv_writer = csv.writer(file_to_write, delimiter = ';')
        csv_writer.writerow(temp)

def main():
    if args.options != None:
        if 'pretty_print' in args.options:
            main_pretty_print.main()
            return
        elif 'aggregation' in args.options:
            aggregation.add_aggregation_data_all()
            return
        elif 'indicators' in args.options:
            if 'light' in args.options:
                tab_options = ['light']
            elif 'lightcom' in args.options:
                tab_options = ['lightcom']
            else:
                tab_options = None
            main_indicators.main(args.dataset, None, tab_options)
            return
        elif 'cluster_per_gt' in args.options:
            list_of_gt = [option for option in args.options if option in ParsedStatus.GUESSED_TYPES.get_name_set()]
            clusters_per_gt(list_of_gt)

    list_folders = args.dataset if args.dataset else ['csa', 'all', 'p5', 'entretiens']
    for folder in list_folders:
        if args.folders and folder not in args.folders:
            continue
        list_ego = [f for f in os.listdir('GALLERY/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            print ego
            sys.argv = ['main.py', folder, ego]
            if args.options != None:
                sys.argv.append('-o')
                for option in args.options:
                    sys.argv.append(option)
            execfile("main.py")

main()