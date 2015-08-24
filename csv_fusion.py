###
###   fusion all csv from a directory in one csv called fusion.csv inside the directory. 
###   Skip the first line for every csv from the directory.
###   You need to be in the parent of directory to run the function ( which means that '.' is OK in directory )
###


# -*- coding: utf-8 -*-

import argparse
parser = argparse.ArgumentParser(description="see the comments upside")
parser.add_argument('directory', help="directory")
args = parser.parse_args()

import os
import sys
import csv

directory = args.directory

new_csv = open('%s/fusion.csv' % directory, 'wb')

# Picks up the first line on any .csv
for old_file in os.listdir(directory):
    if not str(old_file[-4:-1]) + str(old_file)[len(old_file)-1] == '.csv':
        continue 
    old_csv =  open('%s/%s' % (directory, old_file), 'rb')
    new_csv.write(old_csv.readline())
    old_csv.close()
    break
    
# Write the rest from every .csv 
i = 100
for old_file in os.listdir(directory):
    if i == 0:
        break
    if not str(old_file[-4:-1]) + str(old_file)[len(old_file)-1] == '.csv':
        continue
    old_csv =  open('%s/%s' % (directory, old_file), 'rb')
    csv_test = csv.reader(old_csv, delimiter = ';')
    try:
        csv_test.next()
        rarity = csv_test.next()
        if rarity[3] == '':
            continue
        print old_file
        if 'fusion' in old_file:
            print 'pass'
            continue
        for line in old_csv:
            new_csv.write(line)
    except StopIteration:
        old_csv.close()
        continue
    old_csv.close()
    i = i -1
    
new_csv.close()
    
    
