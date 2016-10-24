#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Author: serine
# Initial release: 30/10/2015
# Last update: 4/5/2016

import os, sys, argparse

parser = argparse.ArgumentParser(usage='%(prog)s --bamsDir <path/to/BAM file directory>',
                                 description="This scripts makes html file with summary report \
                                              about your alignment run using STAR `*Log.final.out` files",
                                add_help=True
                                )
parser.add_argument('--bamsDir',
                     required=True,
                    help="specify directory with your BAM files, which should also hold `*Log.final.out` files"
                    )

args = parser.parse_args()
bamsDir = args.bamsDir
# times
job_on = "Started job on"
mapping_on = "Started mapping on"
job_off = "Finished on"
# general stats
total_reads = "Number of input reads"
input_length = "Average input read length"
average_length = "Average mapped length"
# Mapped
uniquely_mapped = "Uniquely mapped reads number"
uniquely_percent = "Uniquely mapped reads %"
multi_mapper = "Number of reads mapped to multiple loci"
multi_percent = "% of reads mapped to multiple loci"
too_many_map = "Number of reads mapped to too many loci"
too_many_percent = "% of reads mapped to too many loci"
# Unmapped
miss_match = "% of reads unmapped: too many mismatches"
too_short = "% of reads unmapped: too short"
# Chimeric 
chimeric = "Number of chimeric reads"
chimeric_percent = "% of chimeric reads"

times = [job_on,
        mapping_on,
        job_off
        ]

general = [total_reads,
           input_length,
           average_length
           ]

mapped = [uniquely_mapped,
          uniquely_percent,
          multi_mapper,
          multi_percent,
          too_many_map,
          too_many_percent
          ]

unmapped = [miss_match,
           too_short
           ]

chimeric = [chimeric,
            chimeric_percent
            ]

tables = [times, general, mapped, unmapped, chimeric]

#rename = {
#        job_on: 'Starting time',
#        mapping_on: 'Mapping started',
#        job_off: 'Mapping finished',
#        total_reads: total_reads,
#        input_length: input_length,
#        average_length: average_length,
#        uniquely_mapped: 
#        }
# get all in the bam directory
listOfFiles = os.listdir(bamsDir) 

# parsing function
def get_value(key, line):
    if line.startswith(key):
        return key, line.split("|")[-1].strip()

# make a hash of hashes
# where every nested hash represents individual samples
# file content
def getDataObj(listOfFiles, tables):
    # init empty hash
    dataDict = {}
    # flatterning tables list 
    keys = [i for l in tables for i in l]
    #
    for textFile in listOfFiles:
        filesDataDict = {}
        # select only Log.final.out files, which are STAR mappings stats files
        if textFile.endswith("Log.final.out"):
            # make samples name from the file
            name = textFile.split('_')[0]
            makePath = os.path.join(bamsDir, textFile)
            # open each stats files
            with open(makePath) as fileHandle:
                for i in fileHandle:
                    line = i.strip()
                    tmp_data = [get_value(key, line) for key in keys if key in line]
                    if tmp_data:
                        k,v = tmp_data[0]
                        filesDataDict[k] = v
            dataDict[name] = filesDataDict

    return dataDict

# this outputs specially sorted hash
# for easy join into table
def getOrdObj(dataObj, tables):
    ordDict = {}
    # flatterning tables list 
    keys = [i for l in tables for i in l]
    for sample in sorted(dataObj.keys()):
        v = dataObj[sample]
        # append samples names into hash
        # under key 'samples'
        if 'samples' not in ordDict:
            ordDict['samples'] = []
        ordDict['samples'].append(sample)
        # merge all values into single list 
        # under common key
        # because hash is ordered we can related sample names to data column
        for key in keys:
            if key not in ordDict:
                ordDict[key] = []
            ordDict[key].append(v[key])

    return ordDict

def getHTMLtable(ordObj, keys):
    htmlList = []
    # this is number of columns
    # extra one for naming column
    # each column corresponds to a sample, whereas rows to different types of information e.g mapped reads
    samplesN = len(ordObj['samples'])+1
    header = True
    #for k,v in ordObj.items():
    for key in keys:
        if header:
            h = list(ordObj['samples'])
            h.insert(0, '')
            cells = '<td>%s</td>'*samplesN
            skeleton = '<tr>%s</tr>' % cells
            row = skeleton % tuple(h)
            htmlList.append(row)
            header = False
    
        d = list(ordObj[key])
        d.insert(0, key)
        cells = '<td>%s</td>'*samplesN
        skeleton = '<tr>%s</tr>' % cells
        row = skeleton % tuple(d)
        htmlList.append(row)

    return htmlList

dataObj = getDataObj(listOfFiles, tables)
ordObj = getOrdObj(dataObj, tables)
#htmlList = getHTMLtable(ordObj, chimeric)
#print htmlList

for keys in tables:
    htmlList = getHTMLtable(ordObj, keys)
    print "<table class='check' border=1 frame=void rules=all cellpadding=5px>"
    #print htmlList
    print '\n'.join(htmlList)
    print '</table>'
    print '<br>'
