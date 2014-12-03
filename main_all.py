import argparse
parser = argparse.ArgumentParser(description="main")
parser.add_argument('--options', '-o', nargs='+')
args = parser.parse_args()

import sys
import os
import pretty_print
import aggregation

def main():
    dirname = 'DATA/csa_2014-09-16/'
    liste_ego = [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]
    if args.options != None:
        if 'pretty_print' in args.options:
            pretty_print.main()
            return
        elif 'aggregation' in args.options:
            aggregation.main()
            return
        
    for ego in liste_ego:
        if not os.path.isdir('./GALLERY/csa_2014-09-16/'+ego):
            sys.argv = ['main.py', 'csa_2014-09-16', ego]
            if args.options != None:
                sys.argv.append('-o')
                for option in args.options:
                    sys.argv.append(option)
            execfile("main.py")
            
main()
        