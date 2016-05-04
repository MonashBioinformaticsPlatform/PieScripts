#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
import os

server = 'http://bioinformatics.erc.monash.edu'
dir = sys.argv[1]
listOfFiles = os.listdir(dir)

pwd = os.path.dirname(os.path.realpath(__file__))
home = os.path.expanduser("~")
p = pwd[pwd.index(home):]

fastqcDict = {}


for f in listOfFiles:
    if f.endswith(".html"):
         makeLink = server+os.path.join(p,dir,f)
         name = f.split('.')[0]
         fastqcDict[name] = makeLink

print "<table class='check' border=1 frame=void rules=all align=center cellpadding=5px>"

for k in  sorted(fastqcDict.keys()):
    print '<tr> <td> <a href="%s">%s</a> </td> </tr>' % (fastqcDict[k], k)

print "</table>"
