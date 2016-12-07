#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# author: serine
# date: 06/11/2016

import sys
import gzip
import argparse


#keys = ["LOCUS",
#        "DEFINITION",
#        "ACCESSION",
#        "VERSION",
#        "KEYWORDS",
#        "SOURCE",
#        "ORGANISM",
#        "REFERENCE",
#        "AUTHORS",
#        "TITLE",
#        "JOURNAL",
#        "COMMENT",
#        "FEATURES",
#        "BASE",
#        "ORIGIN"]


def get_coords(s):

    strand = "+"
    items = [a.strip() for a in s.split(' ') if a]
    name = items[0]
    string = items[1]

    if string.startswith("complement"):
        string = string[string.index("(")+1:].strip(")")
        strand = "-"

    coords = string.split("..")
    start = str(coords[0])
    end = str(coords[1])

    return name, start, end, '.', strand, '.'

def get_features(elements, source, counter):
    addon = 1

    build = '' 
    for element in elements:
        if '..' in element:
            if build:
                #print build.strip(';')
                build = build.strip(';') + '\n'
    
            build += source
            build += '\t'
            build += "circular"
            build += '\t'
            build += '\t'.join(get_coords(element))
            build += '\t'
            build += "id=%s.%s" % (str(counter), str(addon))
            build += ';'
            addon += 1

        else:
            if element.endswith('"') and not element.startswith('/'):
                build = build.strip(';') + " " + element
                build += ';'
            else:
                build += element.strip('/')
                build += ';'

    
    return build.strip(';')


def main(handler):

    source_start = "ACCESSION"
    source_end = "VERSION"
    
    key_start = "FEATURES"
    key_end = "BASE"

    all = handler.read()
    source = all[all.index(source_start):all.index(source_end)]
    source = [a.strip() for a in source.split(' ') if a][1]
    features = all[all.index(key_start):all.index(key_end)]
    
    idx = 1
    my_string = features
    current_idx = 0
    counter = 0
    gff_file = ""
    while idx:
        try:
            current_idx = my_string.index(" gene", idx+1)
            if idx > 1:
                gene = my_string[idx:current_idx]
                # remove amino acid sequence, its not needed in gff file
                try:
                    t_idx = gene.index("/translation=")
                    gene = gene[:t_idx]
                except ValueError:
                    pass
    
                elements = [a.strip() for a in gene.split('\n') if a]
                #print get_features(elements, source, counter)
                gff_file += get_features(elements, source, counter)
                gff_file += '\n'
                counter += 1
            idx = current_idx
        except ValueError:
            gene = my_string[idx:]
            elements = [a.strip() for a in gene.split('\n') if a]
            #print get_features(elements, source, counter)
            gff_file += get_features(elements, source, counter)
            gff_file += '\n'
            idx = 0
    
    yield gff_file.strip('\n')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(usage='%(prog)s --gbk_file <path/to/GenBank file>',
                                     description="Parsers GenBank into GFF file",
                                    add_help=True
                                    )
    parser.add_argument('--gbk_file',
                        required=True,
                        help="provide GenBank file"
                        )
    
    args = parser.parse_args()
    gbk_file = args.gbk_file

    handler = None
    
    if gbk_file.endswith(".gz"):
        handler = gzip.open(gbk_file)
    else:
        handler = open(gbk_file)

    for i in main(handler):
        print i
