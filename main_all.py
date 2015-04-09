import argparse
parser = argparse.ArgumentParser(description="main")
parser.add_argument('--options', '-o', nargs='+')
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
            aggregation.main()
            return
        elif 'indicators' in args.options:
            if 'light' in args.options:
                tab_options = ['light']
            else:
                tab_options = None
            indicators.main(options = tab_options)        
            return
    
    list_folders = [f for f in os.listdir('DATA') if os.path.isdir(os.path.join('DATA', f))]
    for folder in list_folders:
        if 'all_2014' in folder:
            continue
        list_ego = [f for f in os.listdir('DATA/'+folder) if os.path.isdir(os.path.join('DATA/'+folder, f))]
        for ego in list_ego:
            sys.argv = ['main.py', folder, ego]
            if args.options != None:
                sys.argv.append('-o')
                for option in args.options:
                    sys.argv.append(option)
            execfile("main.py")
                
main()