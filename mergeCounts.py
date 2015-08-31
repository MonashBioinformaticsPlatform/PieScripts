#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# (+_+)

import argparse, sys, os, re, gffutils

# Create optional arguments using argparse module
parser = argparse.ArgumentParser(usage='',
                                 description="This script mergers read counts files that you would typically\
                                              get from htseq-counts or featureCounts, into one file, where\
                                              each column represents a file."
                                 )
parser.add_argument('--fileDir',
                    required=True,
                    help="specify files directory"
                    )
parser.add_argument('--skipHeader',
                    type=int,
                    default=0,
                    help="specify number of line to skip in the count file, default assumes featureCount, which\
                          has two header lines"
                    )
parser.add_argument('--dbFile',
                    help="specify files directory"
                    )

args = parser.parse_args()
skipHeader = args.skipHeader
fileDir = args.fileDir
dbFile = args.dbFile

listOfFiles = os.listdir(fileDir)

dataDict = {}
header = True

for textFile in listOfFiles:
    if textFile.endswith("txt"):
        f = open(os.path.join(fileDir, textFile))
        # skip the header
        # featureCounts only has two lines of header
        for i in range(skipHeader):
            f.next()
        #-------------------------------------------------------
        # This section is specific for columns name formating
        #-------------------------------------------------------
        preName = textFile.split('_')
        fileName = preName[0]

        for line in f:
            c = line.strip().split()
            geneId = c[0]
            if geneId not in dataDict:
                dataDict[geneId] = []
            dataDict[geneId].append((c[6], fileName))

if dbFile:
    db = gffutils.FeatureDB(dbFile, keep_order=True)
    features = db.all_features()

    for line in features:
        if line.featuretype == 'gene':
            geneId = line.id
            geneName = line.attributes['gene_name'].pop()
            geneType = line.attributes['gene_biotype'].pop()
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
