import argparse
parser = argparse.ArgumentParser(description="main")
parser.add_argument('--options', '-o', nargs='+')
args = parser.parse_args()

import sys
import os
import pretty_print
import aggregation
import csv
import status
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
            indicators.main()        
            return
    
    list_folders = [f for f in os.listdir('DATA') if os.path.isdir(os.path.join('DATA', f))]
    for folder in list_folders:
        list_ego = [f for f in os.listdir('DATA/'+folder) if os.path.isdir(os.path.join('DATA/'+folder, f))]
        for ego in list_ego:
            if not os.path.isdir('GALLERY/'+folder+'/'+ego):
                sys.argv = ['main.py', folder, ego]
                if args.options != None:
                    sys.argv.append('-o')
                    for option in args.options:
                        sys.argv.append(option)
                execfile("main.py")
    
    for file_zip in [f for f in os.listdir('DATA') if os.path.isfile('DATA/'+f)]:
        tar = tarfile.open('DATA/'+file_zip, 'r')
        folder = file_zip[0:len(file_zip)-7]
        for ego in [elem for elem in tar if (elem.isdir() and 'export' not in elem.name)]:
            tar.extract(ego.name+'/friends.jsons.gz', path='DATA/'+folder)
            tar.extract(ego.name+'/statuses.jsons.gz', path='DATA/'+folder)
            if not os.path.isdir('GALLERY/'+folder+'/'+ego.name):
                sys.argv = ['main.py', folder, ego.name]
                if args.options != None:
                    sys.argv.append('-o')
                    for option in args.options:
                        sys.argv.append(option)
                execfile("main.py")
            shutil.rmtree('DATA/'+folder+'/'+ego.name)
        #shutil.rmtree('DATA/'+folder)
main()
        