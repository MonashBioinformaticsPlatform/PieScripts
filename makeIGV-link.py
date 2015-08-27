#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import sys, os, re, argparse, getpass

parser = argparse.ArgumentParser(usage='%(prog)s --dataDirectory <path/to/yourData>',
                                 description="This scripts makes special URL links that you can use to view your\
                                              data in IGV. IGV can display several different file formats\
                                              including VCF and BAM",
                                add_help=True
                                )
parser.add_argument('--dataDirectory',
                     required=True,
                    help="specify directory with your data files to be made into IGV links"
                    )
parser.add_argument('--defaultCoordinates',
                    nargs=3,
                    default=map(str, [12, 24565477, 24624103]),
                    help="This will be your default coordinates when IGV loads for the first time when IGV loads.\
                          Pass coordinates as follows <Chromosome Start End>"
                    )
parser.add_argument('--serverName',
                    default='bioinformatics.erc.monash.edu',
                    help='Provide your hosting server name'
                    )

args = parser.parse_args()
dataDirectory = args.dataDirectory
defaultCoordinates = args.defaultCoordinates
serverName = args.serverName

# Get list of all data files e.g all BAM files
listOfFiles = os.listdir(dataDirectory)

getChromosome = defaultCoordinates.pop(0)
coordinates = ':'.join((getChromosome, '-'.join(defaultCoordinates)))

header = True

# This is set localhost on which IGV listens
localHost = 'http://localhost:60151/load?file=http%3A%2F%2F'
# Making path to the server, which is hosting the data
theServer = localHost+serverName
trackInfoTemplate = '%s&genome=mm10&merge=true&name=%s&locus=chr%s'

#print "<h4><a href='igv.jnlp'>Click this link to launch IGV</a></h4>"
print "<table class='check' border=1 frame=void rules=all align=center cellpadding=5px>"
for i in listOfFiles:
        if i.endswith('bam'):
                getFullPath = os.path.abspath(dataDirectory)
                userName = getpass.getuser()
                getRightPathIndex = getFullPath.index('/home/'+userName)
                getRightPath = getFullPath[getRightPathIndex:]+'/'
                urlPath = theServer+getRightPath.replace('/', '%2F')
                bamFile = os.path.join(getRightPath, i)
                name = i.strip().split("_")[0]
                bamName = name+'.sorted.bam'
                trackInfo = trackInfoTemplate % (i, name, coordinates)
                if header:
                        print '<tr><td>IGV links</td><td>BAM files</td><tr>'
                        header = False

                print '<tr><td><a href="%s">%s</a></td><td><a href="%s">%s</a></td></tr>' % (urlPath+trackInfo, name, bamFile, bamName)
print "</table>"
