import sys
import os

dirname = 'DATA/csa/'
liste_ego = [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f))]
for ego in liste_ego:
    if not os.path.isdir('./GALLERY/csa/'+ego):
        sys.argv = ['main.py', 'csa', ego]
        execfile("main.py")
        