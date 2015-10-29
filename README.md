# This is tasty as repo, yam ! 

> This is communal repository to which anyone is welcome to contribute they own python scripts. 
> Please follow the convention and do append quick summary about your script into `README.md` file.
> Use \#\#\# to mark your heading following your python script name without `.py` suffix 

## Content

- [makeIGV-link](#makeigv-link)
- [alignmentStats](#alignmentStats)
- [makeBioDalliance](#makebiodalliance)
- [mergeCounts](#mergecounts)
- [getChromSizes](#getchromsizes)

#### alignmentStats

Easy to use python script to get summary report on your alignment run. This script only works with STAR alignment, because this script parsers `*Log.final.out` files that STAR produces by default.

Usage: `./alignmentStats.py --bamsDirectory <BAM files directory> >> index.html`

### makeIGV-link

Simple script that can make special URL links encoding your data into URL, such as BAM
files, so that you can visualise it in [Intergrative Genomics Viewer](http://www.broadinstitute.org/igv/) or
IGV for short. Here is [IGV's guide](http://www.broadinstitute.org/igv/ControlIGV) on 'special IGV URLs'.
IGV is pretty cool in that it's enable your to launch and use it without needing to install it on your local
machine. Sometimes you do need to install some JAVA dependencies on your local machine to be able to run IGV
over internet. Here is a link on how to start [IGV with web start](http://www.broadinstitute.org/igv/startingIGV).

To start with `makeIGV-link.py` simply download the file and run it in command line with `--help` option.

Option to download the file:

- Just the file
`wget https://raw.githubusercontent.com/MonashBioinformaticsPlatform/PieScripts/master/makeIGV-link.py`

OR 

- Clone the whole repository
`git clone https://github.com/MonashBioinformaticsPlatform/PieScripts.git`

### makeBioDalliance 

[BioDalliance](http://www.biodalliance.org/) is this awesome _browser_ to view genomic data. It is a self
contained JavaScript object that you can embed into web page. Major advantage of BioDalliance is it's truly
platform independed and you can run it from any device that supports web browser. This is the future and totally
different way to interact with your data. You can view your data on the smart phone or a table or desktop. With
everything being in the _cloud_ these days you don't want to limit yourself to desktop only applications. 

To start with `makeDalliance.py` simply download the file and run it in command line with `--help` option.

Option to download the file:

- Just the file `wget https://raw.githubusercontent.com/MonashBioinformaticsPlatform/PieScripts/master/makeDalliance.py`

OR 

- Clone the whole repository `git clone https://github.com/MonashBioinformaticsPlatform/PieScripts.git`

### mergeCounts

Quick script that you can use to merge read counts files that you would typically get from htseq-count or
featureCounts. Usually for each BAM file you will get a single text `.txt` file with gene names in first
column and actual counts in the second column, some tools can output more information than that into `.txt`.
e.g featureCounts output 7 different columns. Some downstream applications accept single file only for 
further differential gene expression analysis e.g [Degut](http://www.vicbioinformatics.com/degust/) requires
single TSV or CSV file for its upload. 

Default settings thus far optimased for `featureCounts`:

- `readsColumn` set to 7 
- `usersBiotype` is turned off, i.e it will print everything coding and non coding types
- `nameDelimiter` is set to underscore character - `_`
- `headerLines` is set to 2

To start with `mergeCounts.py` simply download the file and run it in command line with `--help` option.

Option to download the file:

- Just the file `wget https://raw.githubusercontent.com/MonashBioinformaticsPlatform/PieScripts/master/mergeCounts.py`

OR 

- Clone the whole repository `git clone https://github.com/MonashBioinformaticsPlatform/PieScripts.git`

### getChromSizes

This is almost two lines of code using biopython to get chromosome (or other sequence identifier) and its 
length. Some tools may require that you give a file with chromosome sizes usually with `.chrom.sizes`
extension. Here is a reference to [IGV](http://www.broadinstitute.org/igv/chromSizes) needing such file.

To start with `getChromSizes.py` simply download the file and run it in command line with `--help` option.

Option to download the file:

- Just the file `wget https://raw.githubusercontent.com/MonashBioinformaticsPlatform/PieScripts/master/getChromSizes.py`

OR 

- Clone the whole repository `git clone https://github.com/MonashBioinformaticsPlatform/PieScripts.git`
