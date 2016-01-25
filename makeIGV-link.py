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
                    help="This will be your default coordinates when IGV loads for the first time when IGV loads.\
                          Pass coordinates as a string e.g follows chr12:24565477-24624103"
                    )
parser.add_argument('--serverName',
                    default='bioinformatics.erc.monash.edu',
                    help='Provide your hosting server name'
                    )
parser.add_argument('--launchIGVfile',
					help="Specify path to your igv.jnlp - java web start file, to launch IGV"
		            )
parser.add_argument('--genome',
					help="Specifie your species genome. You can use IGV abbreviation e.g mm10 for Mus musculus 10 genome or specify URL of your FASTA reference file. For custome reference files, please make sure you FASTA reference is indexed, you cam use `samtools faidx` command for that"
		            )

args = parser.parse_args()
dataDirectory = args.dataDirectory
defaultCoordinates = args.defaultCoordinates
serverName = args.serverName
launchIGVfile = args.launchIGVfile
genome = args.genome

# Get list of all data files e.g all BAM files
listOfFiles = os.listdir(dataDirectory)

header = True

# This is set localhost on which IGV listens
localHost = 'http://localhost:60151/load?file=http%3A%2F%2F'
# Making path to the server, which is hosting the data
the_server = localHost+serverName


# to get IGV link, optional
if launchIGVfile:
	# if there is a www/ directory in the path
	# it shouldn't be reflected in the url
	# disect it out
    try:
        getWWWindex = launchIGVfile.index("www/")
        first_bit = launchIGVfile[:getWWWindex]
        second_bit = launchIGVfile[getWWWindex+4:]
        launchIGVfile = first_bit+second_bit
        print "<h4><a href='%s'>Click this link to launch IGV</a></h4>" % launchIGVfile
	# if www/ isn't found in the path, then assume user accounted for the right URL path
    except:
        print "<h4><a href='%s'>Click this link to launch IGV</a></h4>" % launchIGVfile

print "<table class='check' border=1 frame=void rules=all align=center cellpadding=5px>"
for i in listOfFiles:
    if i.endswith('bam'):
        get_full_path = os.path.abspath(dataDirectory)
        home_variable = os.getenv('HOME')
        get_right_path = get_full_path.index(home_variable)
        get_right_path = get_full_path[get_right_path:]+'/'
        path_to_file = the_server+get_right_path.replace('/', '%2F')
        bam_file = os.path.join(get_right_path, i)
        bam_file_root_name = i.strip().split("_")[0]
        bam_file_name = bam_file_root_name + ".sorted.bam"
        name = 'name=%s' % bam_file_name
		# build igv url
        if genome and defaultCoordinates:
            genome_var = 'genome=%s&merge=true' % genome
            locus = 'locus=%s' % defaultCoordinates
            igv_url = '&'.join((path_to_file, i, genome_var, locus, name))
        if genome:
            genome_var = 'genome=%s&merge=true' % genome
            igv_url = '&'.join((path_to_file, i, genome_var, name))
        if defaultCoordinates:
            locus = 'locus=%s' % defaultCoordinates
            igv_url = '&'.join((path_to_file, i, locus, name))
        if header:
            print '<tr><td>IGV links</td><td>BAM files</td><tr>'
            header = False

        print '<tr><td><a href="%s">%s</a></td><td><a href="%s">%s</a></td></tr>' % (igv_url, bam_file_root_name, bam_file, bam_file_name)

print "</table>"
