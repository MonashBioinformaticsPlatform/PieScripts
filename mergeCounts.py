#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# (+_+)

import argparse, sys, os, re, gffutils

# Create optional arguments using argparse module
parser = argparse.ArgumentParser(usage='%(prog)s --filesDir <path/to/yourData>',
                                 description="This script mergers read counts files that you would typically\
                                              get from htseq-counts or featureCounts, into one file, where\
                                              each column represents a file."
                                 )
parser.add_argument('--filesDir',
                    required=True,
                    help="specify path/to/yourData directory"
                    )
parser.add_argument('--readsColumn',
                    type=int,
                    default=7,
                    help="specify in which column is your read count information. Default assumes featureCounts `.txt` file format and that is column 7"
                    )
parser.add_argument('--usersBiotype',
                    type=str,
                    default=None,
                    help="specify biotype of your interest e.g for differential gene expression you would only\
                          be interested in protein coding biotype. Specify `--usersBiotype` exactly as it is\
                          written in the GFF/GTF file that you have used to make in upsreat counting tools.\
                          Default is None"
                    )
parser.add_argument('--nameDelimiter',
                    type=str,
                    default='_',
                    help="specify on which character you want to 'split' your file name. This is to generate\
                          column names from file names. The script will grab everything to the left of the\
                          delimiter character specified. Default splits on '_' (underscore)."
                    )
parser.add_argument('--headerLines',
                    type=int,
                    default=2,
                    help="specify number of line to skip in the count file, default assumes featureCount, which\
                          has two header lines"
                    )
parser.add_argument('--dbFile',
                    help="specify path/to/databaseFile. You can make such file using python `gffutils` library.\
                          This is augment your merged read count file with other informatin, such as\
                          Public gene names and Biotype"
                    )

args = parser.parse_args()
filesDir = args.filesDir
nameDelimiter = args.nameDelimiter
usersBiotype = args.usersBiotype
# off set for python, since python indexing starts at zero
readsColumn = args.readsColumn - 1
headerLines = args.headerLines
dbFile = args.dbFile

listOfFiles = os.listdir(filesDir)

dataDict = {}
header = True

for textFile in listOfFiles:
    if textFile.endswith("txt"):
        f = open(os.path.join(filesDir, textFile))
        # skip the header
        # featureCounts only has two lines of header
        for i in range(headerLines):
            f.next()
        #-------------------------------------------------------
        # This section is specific for columns name formating
        #-------------------------------------------------------
        preName = textFile.split(nameDelimiter)
        fileName = preName[0]

        for line in f:
            c = line.strip().split()
            geneId = c[0]
            if geneId not in dataDict:
                dataDict[geneId] = []
            dataDict[geneId].append((c[readsColumn], fileName))

if dbFile:
    db = gffutils.FeatureDB(dbFile, keep_order=True)
    features = db.all_features()

    for line in features:
        if line.featuretype == 'gene':
            geneId = line.id
            geneName = line.attributes['gene_name'].pop()
            geneType = line.attributes['gene_biotype'].pop()
            if usersBiotype:
                if geneType == usersBiotype:
                    v = dataDict[geneId]
                    dataItems = '\t'.join([f[0] for f in v])
                    if header:
                        header = '\t'.join([f[1] for f in v])
                        print '\t'.join(('Ensembl ID', 'Gene Name', 'Biotype', header))
                        header = False
                    print '\t'.join((geneId, geneName, geneType, dataItems))
            else:
                v = dataDict[geneId]
                dataItems = '\t'.join([f[0] for f in v])
                if header:
                    header = '\t'.join([f[1] for f in v])
                    print '\t'.join(('Ensembl ID', 'Gene Name', 'Biotype', header))
                    header = False
                print '\t'.join((geneId, geneName, geneType, dataItems))
else:
    for k,v in dataDict.items():
        if header:
            header = '\t'.join([f[1] for f in v])
            print '\t'.join(('Ensembl ID', header))
            header = False
    
        row = '\t'.join([i[0] for i in v])
        print '\t'.join((k, row))
