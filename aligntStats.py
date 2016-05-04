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

    dataDict = {}
    keys = [i for l in tables for i in l]

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

#print getDataObj(listOfFiles, tables)

#def get_data_dict(list_of_files, keys):
#    # initialise dictionary
#    data_dict = {}
#    # loop over all files in the bam directory
#    for text_file in list_of_files:
#        # select only Log.final.out files, which are STAR mappings stats files
#        if text_file.endswith("Log.final.out"):
#            # make samples name from the file
#            name = text_file.split('_')[0]
#            make_path = os.path.join(bamsDir, text_file)
#            # open each stats files
#            with open(make_path) as file_handle:
#                for i in file_handle:
#                    line = i.strip()
#                    tmp_data = [get_value(key, line) for key in keys if key in line]
#                    if tmp_data:
#                        k,v = tmp_data[0]
#                        if k not in data_dict:
#                            data_dict[k] = {}
#                        data_dict[k][name] = v
#    return data_dict
#
##$data_dict = get_data_dict(list_of_files, times.keys())
##$print data_dict
#
#def get_table(data_dict):
#    header = True
#    
#    #header_list = ["<table class='check' border=1 frame=void rules=all cellpadding=5px>"]
#    check = "<table class='check' border=1 frame=void rules=all cellpadding=5px>"+'\n'
#    
#    table_list = []
#    
#    cell = '<td>%s</td>'
#    get_sample_n = None
#    
#    for k,v in data_dict.items():
#        #print k,v
#        if header:
#            sample_name = [i for i in sorted(v.keys())]
#            get_sample_n = len(sample_name)+1
#            sample_name.insert(0, '')
#            cells = cell*get_sample_n
#            row = '<tr>%s</tr>' % cells
#            row_cell = row % tuple(sample_name)
#            #header_list.append(row_cell)
#            check += row_cell+'\n'
#            header = False
#    
#        data_values = [data_dict[k][i] for i in sorted(v.keys())]
#        cells = cell*get_sample_n
#        data_values.insert(0, k)
#        row = '<tr>%s</tr>' % cells
#        row_cell = row % tuple(data_values)
#        #table_list.insert(times[k], row_cell)
#        #print times[k]
#        check += row_cell+'\n'
#        
#    #table_list.append("</table>")
#    
#    #check = '\n'.join(( '\n'.join(header_list), '\n'.join(table_list) ))
#    #
#    #print check
#    
#    return check
#
#for table in tables:
#    data_dict = get_data_dict(list_of_files, table)
#    print get_table(data_dict)
#    print '<br>'
