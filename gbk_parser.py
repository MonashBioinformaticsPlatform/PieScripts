#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
import gzip
import argparse


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

def do_attribute(attribute, feature_line):

    if attribute.startswith('/') and attribute.endswith('"'):
        attribute = attribute.strip('/')
        feature_line += attribute
        feature_line += ';'
        return feature_line

    else:
        #if element.endswith('"') and not element.startswith('/'):
        if ( attribute.endswith('"') or attribute.endswith('') ) and not attribute.startswith('/'):
            feature_line = feature_line.strip(';') + "_" + attribute
            feature_line += ';'
        else:
            feature_line += attribute.strip('/')
            feature_line += ';'

    return feature_line.strip(';')

def trim_translation(o):
    t = "translation="
    get_start = o.find(t)
    get_end = o.find('"', get_start+len(t)+1)
    if get_start != -1:
        o = o[:get_start] + o[get_end+1:]
    return o.strip(';')

def messy(feature):
    name_idx_start = feature.find(';Name=')
    name_idx_end = feature.find(';', name_idx_start+1)
    diff = name_idx_end - name_idx_start
    start_idx = feature.rfind('.\t')

    name = feature[name_idx_start+1:name_idx_end]
    feature = feature[:start_idx+2] + \
                name + \
                ';' + \
                feature[start_idx+2:name_idx_start] + \
                ';' + \
                feature[name_idx_start+diff+1:]

    return feature

gene_counter = 0
cds_counter = 0
other_coutner = 0
parent_counter = 0

def gff_parser(feature):
    res = None
    if "\tgene\t" in feature:
        id = 'ID=gene%s;' % str(gene_counter) 

        if "gene=" in feature:
            id += 'Name='
            feature = feature.replace('gene=', id)
            feature = messy(feature)
        else:
            get_start = feature.rfind('.\t')
            feature = feature[:get_start+2] + id + feature[get_start+2:]
        res = tuple((feature, 'g'))

    elif "\tCDS\t" in feature:
        #id = 'ID=cds%s;Parent=gene%s;' % (str(cds_counter), str(parent_counter))
        cds_counter = gene_counter - 1
        id = 'ID=cds%s;Parent=gene%s;' % (str(cds_counter), str(cds_counter))

        if "gene=" in feature:
            id += 'Name='
            feature = feature.replace('gene=', id)
            feature = messy(feature)

        else:
            get_start = feature.rfind('.\t')
            feature = feature[:get_start+2] + id + feature[get_start+2:]

        res = tuple((feature, 'c'))
    else:
        if gene_counter:
            other_counter = gene_counter - 1
        else:
            other_counter = gene_counter

        id = 'ID=misc%s;Parent=gene%s;' % (str(other_counter), str(other_counter))

        if "gene=" in feature:
            id += 'Name='
            feature = feature.replace('gene=', id)
            feature = messy(feature)
        else:
            get_start = feature.rfind('.\t')
            feature = feature[:get_start+2] + id + feature[get_start+2:]

        res = tuple((feature, 'o'))

    return res

def gbk_parser(gbk_handler):

    V = "VERSION"
    F = "FEATURE"
    B = "BASE COUNT"
    
    ok = False
    genome = 'unknown'
    source = 'circular'
    new_feature = ''
    for i in handler:
        line = i.strip()
        if line.startswith(V):
            genome = line.split()[1].strip()
        # one loop over the block of interest
        if line.startswith(B):
            ok = False
    
        if ok:
            if ".." in line:
                if new_feature:
                    yield new_feature.strip(';')
                    #chk = make_gff(trim_translation(new_feature))
                    #if chk[1] == 'g':
                    #    gene_counter += 1
                    #print chk[0]
                    #print trim_translation(new_feature)
                new_feature = '\t'.join((genome, source))
                new_feature += '\t'
                new_feature += '\t'.join(get_coords(line))
                new_feature += '\t'
            else:
                new_feature = do_attribute(line, new_feature)
                #new_feature += ';'
    
        if line.startswith(F):
            ok = True


if __name__ == '__main__':

    parser = argparse.ArgumentParser(usage='%(prog)s --gbk_file <path/to/GenBank file>',
                                     description="Parsers GenBank into GFF file",
                                    add_help=True
                                    )
    parser.add_argument('--gbk_file',
                        required=True,
                        help="provide GenBank file"
                        )
    parser.add_argument('--keep_seq',
                        action='store_true',
                        help="If you want to keep translation - amino acid sequence"
                       )
    parser.add_argument('--make_gff',
                        action='store_true',
                        help="If you want to make proper GFF3 file format"
                       )
    
    args = parser.parse_args()
    gbk_file = args.gbk_file
    keep_seq = args.keep_seq
    make_gff = args.make_gff
    
    handler = None
    
    if gbk_file.endswith(".gz"):
        handler = gzip.open(gbk_file, 'rt')
    else:
        handler = open(gbk_file)

    gbk = gbk_parser(handler)
    for i in gbk:
        if keep_seq:
            if make_gff:
                gff = gff_parser(i)
                if gff[1] == 'g':
                    gene_counter += 1
                print(gff[0])
            else:
                print(i)
        else:
            i = trim_translation(i)
            if make_gff:
                gff = gff_parser(i)
                if gff[1] == 'g':
                    gene_counter += 1
                print(gff[0])
            else:
                print(i)
