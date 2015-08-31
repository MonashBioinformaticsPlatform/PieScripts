#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from Bio import SeqIO
import sys, argparse

parser = argparse.ArgumentParser(usage='%(prog)s --fastaRef <path/to/FASTA-file>',
                                 description="This script goes through your FASTA file and prints out\
                                              chromosomes or other sequence identifier e.g contig name and\
                                              the length of that sequence. Default is tab delimited"
                                )
parser.add_argument('--fastaRef',
                    required=True,
                    help="specify path/to/FASTA-file"
                    )
parser.add_argument('--columnDelimiter',
                    type=str,
                    default='\t',
                    help="specify how you want to delimiter your columns e.g space (' '), comma or other character"
                    )

args = parser.parse_args()
fastaRef = args.fastaRef
columnDelimiter = args.columnDelimiter

f = open(fastaRef)

for seqRecord in SeqIO.parse(f, 'fasta'):
    seqLength = str(len(seqRecord.seq))
    seqId = seqRecord.id
    print columnDelimiter.join((seqId, seqLength))
