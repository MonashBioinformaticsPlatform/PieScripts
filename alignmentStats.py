#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Author: serine
# Date: 30/10/2015

import os, sys, argparse

parser = argparse.ArgumentParser(usage='%(prog)s --bamsDirectory <path/to/BAM file directory>',
                                 description="This scripts makes html file with summary report \
                                              about your alignment run using STAR `*Log.final.out` files",
                                add_help=True
                                )
parser.add_argument('--bamsDirectory',
                     required=True,
                    help="specify directory with your BAM files, which should also hold `*Log.final.out` files"
                    )

args = parser.parse_args()
bamsDirectory = args.bamsDirectory

job_on = "Started job on"
mapping_on = "Started mapping on"
job_off = "Finished on"
total_reads = "Number of input reads"
uniquely_mapped = "Uniquely mapped reads number"
uniquely_percent = "Uniquely mapped reads %"
input_length = "Average input read length"
average_length = "Average mapped length"

keys = [job_on,
        mapping_on,
        job_off,
        total_reads,
        uniquely_mapped,
        uniquely_percent,
        input_length,
        average_length
        ]
#                       Number of splices: Total |       47255354
#            Number of splices: Annotated (sjdb) |       46803118
#                       Number of splices: GT/AG |       46738945
#                       Number of splices: GC/AG |       438119
#                       Number of splices: AT/AC |       40256
#               Number of splices: Non-canonical |       38034
#                      Mismatch rate per base, % |       0.27%
#                         Deletion rate per base |       0.01%
#                        Deletion average length |       2.11
#                        Insertion rate per base |       0.01%
#                       Insertion average length |       1.92
#                             MULTI-MAPPING READS:
#        Number of reads mapped to multiple loci |       6387522
#             % of reads mapped to multiple loci |       7.95%
#        Number of reads mapped to too many loci |       173849
#             % of reads mapped to too many loci |       0.22%
#                                  UNMAPPED READS:
#       % of reads unmapped: too many mismatches |       0.00%
#                 % of reads unmapped: too short |       6.01%
#                     % of reads unmapped: other |       0.06%

list_of_files = os.listdir(bamsDirectory) 
data_dict = {}

def make_dict(name, key, line):
    if line.startswith(key):
        if name not in data_dict:
            data_dict[name] = []
        data_dict[name].append((key, line.split("|")[-1].strip()))
        return key, line.split("|")[-1].strip()


for text_file in list_of_files:
    if text_file.endswith("final.out"):
        name = text_file.split('_')[0]
        make_path = os.path.join(bamsDirectory, text_file)
        for i in open(make_path):
            line = i.strip()
            [make_dict(name, key, line) for key in keys]

header = True

table_two = "<table class='check' border=1 frame=void rules=all cellpadding=5px>"
print "<table class='check' border=1 frame=void rules=all cellpadding=5px>"

for k,v in data_dict.items():
    if header:
        table_data = [i[0] for i in v]
        table_data.insert(0, "Sample")
        temp_out = table_data.pop(5)
        table_data.insert(-1, temp_out)
        header_run_info = table_data[0:4]
        header_fastq_info = table_data[4:]
        header_fastq_info.insert(0, "Sample")
        table_two += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' % tuple(header_run_info)
        print '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % tuple(header_fastq_info)
        header = False

    table_data = [i[1] for i in v]
    table_data.insert(0, k)
    temp_out = table_data.pop(5)
    table_data.insert(-1, temp_out)
    run_info = table_data[0:4]
    fastq_info = table_data[4:]
    fastq_info.insert(0, k)
    table_two += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' % tuple(run_info)
    print '<tr> <td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % tuple(fastq_info)

print "</table>"
print '''<p>Some long text descriptiont goes here </p>'''
print table_two
print "</table>"
