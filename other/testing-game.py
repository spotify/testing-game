#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import re

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', help='The directory to search for files in', required=False, default=os.getcwd())
args = parser.parse_args()

names = {}

for root, dirs, files in os.walk(args.directory):
    for name in files:
        filename, fileextension = os.path.splitext(name)
        
        absfile = os.path.join(root, name)
        
        if fileextension == '.m' or fileextension == '.mm':
            try:
                with open(absfile) as sourcefile:
                    source = sourcefile.read()
                    if source.find('XCTestCase') != -1:
                        p = subprocess.Popen(['git', 'blame', absfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        out, err = p.communicate()
                        
                        for blame_line in out.splitlines():
                            if blame_line.replace(' ', '').find('-(void)test') != -1:
                                blame_info = blame_line[blame_line.find('(')+1:]
                                blame_info = blame_info[:blame_info.find(')')]
                                blame_components = blame_info.split()
                                name_components = blame_components[:len(blame_components)-4]
                                name = ' '.join(name_components)
                                name_count = names.get(name, 0)
                                names[name] = name_count + 1
            except:
                'Could not open file: ' + absfile

total_tests = 0
for name in names:
    total_tests += names[name]

print "Total Tests: %(t)d" % { 't' : total_tests }
print "-------------------------------------------"
for t in sorted(names.items(), key=lambda x: x[1], reverse = True):
    percentage = (float(t[1]) / float(total_tests)) * 100.0
    print "%(n)s, %(t)d (%(p).2f%%)" % { 'n' : t[0], 't' : t[1], 'p' : percentage }