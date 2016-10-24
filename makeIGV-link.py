#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import sys, os, re, argparse, getpass

parser = argparse.ArgumentParser(usage='%(prog)s --dir <path/to/yourData>',
                                 description="This scripts makes special URL links that you can use to view your data in IGV. IGV can display several different file formats including VCF and BAM",
                                 add_help=True
                                 )
parser.add_argument('--dir',
                    required=True,
                    help="specify directory with your data files to be made into IGV links. This directory should be located in the hostable place i.e you should be able to grab individual file on url"
                    )
parser.add_argument('--coord',
                    help="This will be your default coordinates when IGV loads for the first time when IGV loads. Pass coordinates as a string e.g follows chr12:24565477-24624103"
                    )
parser.add_argument('--host_name',
                    default='http://bioinformatics.erc.monash.edu',
                    help='Provide your hosting server name [bioinformatics.erc.monash.edu]'
                    )
parser.add_argument('--igvFile',
                    help="Specify path to your igv.jnlp - java web start file, to launch IGV [igv.jnlp]",
                    default="igv.jnlp"
                    )
parser.add_argument('--genome',
                    help="Specifie your species genome. You can use IGV abbreviation e.g mm10 for Mus musculus 10 genome or specify URL of your FASTA reference file. For custome reference files, please make sure you FASTA reference is indexed, you cam use `samtools faidx` command for that"
                    )
parser.add_argument('--sep',
                    default='_',
                    help = 'This is main separator within the file'
                    )

args = parser.parse_args()
dir = args.dir
coord = args.coord
host_name = args.host_name
igvFile = args.igvFile
genome = args.genome
sep = args.sep

#genome = None
#genome_load = ""
#
#if args.genome:
#    if "http" in args.genome:
#        genome_load = args.genome.replace(':', '%3A').replace("/", "%2F")
#    else:
#        genome_load = args.genome


# Get list of all data files e.g all BAM files
listOfFiles = os.listdir(dir) 
header = True

# This is set localhost on which IGV listens
#localHost = 'http://localhost:60151/load?file=http%3A%2F%2F'
igv_localhost = 'http://localhost:60151/load?'
# Making path to the server, which is hosting the data
hosting_server = 'file=%s' % host_name.replace(':', '%3A').replace('/', '%2F')

# to get IGV link, optional
if igvFile:
    #if there is a www/ directory in the path
    #it shouldn't be reflected in the url
    #disect it out
    try:
        getWWWindex = igvFile.index("www/")
        first_bit = igvFile[:getWWWindex]
        second_bit = igvFile[getWWWindex+4:]
        igvFile = first_bit+second_bit
        print "<h4><a href='%s'>Click this link to launch IGV</a></h4>" % igvFile
        # if www/ isn't found in the path, then assume user accounted for the right URL path
    except:
        print "<h4><a href='%s'>Click this link to launch IGV</a></h4>" % igvFile

#genome_load = igv_localhost+"genome="+genome_load
#print "<h4><a href='%s'>Load genome</a></h4>" % genome_load
print "<table class='check' border=1 frame=void rules=all align=center cellpadding=5px>"
for i in listOfFiles:
    if i.endswith('bam'):
        get_full_path = os.path.abspath(dir)
        home_variable = os.getenv('HOME')
        get_right_path = get_full_path.index(home_variable)
        get_right_path = get_full_path[get_right_path:]+'/'
        
        full_path = igv_localhost + hosting_server + get_right_path.replace('/', '%2F') + i
        
        bam_file = os.path.join(get_right_path, i)
        bam_file_root_name = i.strip().split(sep)[0]
        bam_file_name = bam_file_root_name + ".sorted.bam"
        name = 'name=%s' % bam_file_root_name

        if genome:
            if coord:
                genome_var = 'genome=%s&merge=true' % genome
                locus = 'locus=%s' % coord
                igv_url = '&'.join((full_path, genome_var, locus, name))
            else:
                genome_var = 'genome=%s&merge=true' % genome
                igv_url = '&'.join((full_path, genome_var, name))
        else:
            if coord:
                locus = 'locus=%s' % coord
                igv_url = '&'.join((full_path, locus, name))
            else:
                igv_url = '&'.join((full_path, name))

        if header:
            print '<tr><td>IGV links</td><td>BAM files</td><tr>'
            header = False
        
        print '<tr><td><a href="%s">%s</a></td><td><a href="%s">%s</a></td></tr>' % (igv_url, bam_file_root_name, bam_file, bam_file_name)

print "</table>"
