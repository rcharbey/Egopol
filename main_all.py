import argparse
parser = argparse.ArgumentParser(description="main")
parser.add_argument('--options', '-o', nargs='+')
args = parser.parse_args()

import sys
import os

dirname = 'DATA/csa/'
liste_ego = [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]
for ego in liste_ego:
    if not os.path.isdir('./GALLERY/csa/'+ego):
        sys.argv = ['main.py', 'csa', ego]
        if args.options != None:
            sys.argv.append('-o')
            for option in args.options:
                sys.argv.append(option)
        execfile("main.py")
        