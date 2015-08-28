#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

htmlTemplate = '''
<!DOCTYPE>

<html>
<head>
    <title>Biodalliance Genome Browser</title>
    <script language="javascript" src="dalliance13.6a.js"></script>
    <script language="javascript">
      new Browser({
        //----------------------------------------------------------------------------------------------------
        fullscreen: true, // attempt to fit dalliance component to the containing window 
        maxHeight: 900,  // maximum hight in CSS pixels 
        pageName:     'mouseTwo-holder', // Target element ID
        //----------------------------------------------------------------------------------------------------
        %s
    
        coordSystem: {
          speciesName: 'Mus musculus',
          taxon: 9606, // NCBI taxon if defined, set to zero if you dont't have one
          auth: 'Ensembl ', //Organization which did the gnoeme sequence/assemble
          version: '38',

        },
    
        sources:     [{name:        'Reference genome',
                       tier_type:   'Sequence',
                       desc:        'There will be longer desctiption placed here',
                       twoBitURI:   '%s'
                      },
                      {name:        'Annotation',
                       desc:        'Genes annotation, showing Exons and Introns boundaries',
                       bwgURI:      '%s',
                       collapseSuperGroups: true,
                       trixURI:     '%s',
                      }, %s
                     ],
      });
    </script>
</head>
<body>
    <div id="mouseTwo-holder"></div>
</body>
</html>   
'''

coordinatesTemplate = '''
        chr:      '%s', // Use the same name you have in your .2bit file
        viewStart: %s,
        viewEnd:   %s,
'''

bamTrackTemplate = '''
                       {name:       '%s',
                       disabled:     true, // This is "untick" track
                       bamURI:      '%s',
                       baiURI:      '%s.bai',
                       style: [
                               {type: "density",
                                zoom: "low",
                                style: {glyph: "HISTOGRAM",
                                        COLOR1: "black",
                                        COLOR2: "red",
                                        HEIGHT: 30,
                                        }
                               },
                               {type: "density",
                                zoom: "medium",
                                style: {glyph: "HISTOGRAM",
                                        COLOR1: "black",
                                        COLOR2: "red",
                                        HEIGHT: 30,
                                        }
                               },
                               {type: "bam",
                                zoom: "high",
                                style: {glyph: "__SEQUENCE",
                                        FGCOLOR: "black",
                                        BGCOLOR: "blue",
                                        HEIGHT: 8,
                                        BUMP: true,
                                        LABEL: false,
                                        ZINDEX: 20,
                                        __SEQCOLOR: "mismatch"
                                       }
                               },
                              ],
                       },

'''

import sys, os, argparse

parser = argparse.ArgumentParser(usage='%(prog)s --dataDirectory <path/to/yourData> --referenceFiles <path/to/yourReferenceFiles>',
                                 description='This scripts makes BioDalliance webpage',
                                 )
parser.add_argument('--dataDirectory',
                    required=True,
                    help="specify directory with data files to be made into BioDalliance tracks"
                    )
parser.add_argument('--referenceFiles',
                    required=True,
                    help='specify directory with reference files e.g refFile.2bit and refAnnotation.bb'
                    )             
parser.add_argument('--defaultCoordinates',
                    nargs=3,
                    default=[12, 24565477, 24624103],
                    help="This will be your default coordinates for BioDallaince browser.\
                          Pass coordinates as follows <Chromosome Start End>"
                    )
parser.add_argument('--serverName',
                    default='bioinformatics.erc.monash.edu'
                    )

args = parser.parse_args()
dataDirectory = args.dataDirectory
referenceFiles = args.referenceFiles
defaultCoordinates = args.defaultCoordinates
serverName = args.serverName

coordinates = coordinatesTemplate % tuple(defaultCoordinates)

refFiles = os.listdir(referenceFiles)
dataFiles = os.listdir(dataDirectory)

genome = ''
annotation = ''
index = ''

for i in refFiles:
    if i.endswith('.2bit'):
        genome = os.path.join(referenceFiles, i)
    if i.endswith('bb'):
        annotation = os.path.join(referenceFiles, i)
    if i.endswith('ix'):
        index = os.path.join(referenceFiles, i)

bamTracks = []

for bamFile in dataFiles:
    if bamFile.endswith('sorted.bam'):
        name = bamFile.split('_')[0]
        bam = os.path.join(dataDirectory, bamFile)
        bamTrack = bamTrackTemplate % (name, bam, bam)
        bamTracks.append(bamTrack)

#print htmlTemplate % (genome, annotation, index, [i.strip() for i in bamTracks])
print htmlTemplate % (coordinates, genome, annotation, index, ' '.join(bamTracks))
