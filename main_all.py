import argparse
parser = argparse.ArgumentParser(description="main")
parser.add_argument('--options', '-o', nargs='+')
parser.add_argument('--dataset', '-d', nargs='+')
args = parser.parse_args()

import sys
import os
import pretty_print
import aggregation
import csv
sys.path.append("./Graphs")
sys.path.append("./Enumeration")
sys.path.append("./Jsons")
sys.path.append("./Indicators")
import main_enumeration
import main_graphs
import main_jsons
import indicators
import tarfile
import shutil

def main():
    if args.options != None:
        if 'pretty_print' in args.options:
            pretty_print.main()
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
            indicators.main(None, None, tab_options)        
            return
    
    list_folders = args.getattr('dataset', ['csa', 'all', 'p5'])
    print args.options
    for folder in list_folders:
        list_ego = [f for f in os.listdir('DATA/'+folder) if os.path.isdir(os.path.join('DATA/'+folder, f))]
        for ego in list_ego:
            sys.argv = ['main.py', folder, ego]
            if args.options != None:
                sys.argv.append('-o')
                for option in args.options:
                    sys.argv.append(option)
            execfile("main.py")
                
main()