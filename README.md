[![Coverage Status](https://coveralls.io/repos/github/NCBI-Hackathons/Master_gff3_parser/badge.svg?branch=master)](https://coveralls.io/github/NCBI-Hackathons/Master_gff3_parser?branch=master) [![Build Status](https://travis-ci.org/NCBI-Hackathons/Master_gff3_parser.svg?branch=master)](https://travis-ci.org/NCBI-Hackathons/Master_gff3_parser)

# SeqIDMapper (an amazing tool that does wonderful stuff)—Documentation
Different formats of sequence IDs are currently in use at different institutes, although there is effort in making everything as standardized as possible moving forward (https://genome.ucsc.edu/FAQ/FAQreleases.html#release4; O’Leary et al. 2016). However, there is a need for a easy-to-use tool that can seamlessly convert sequence IDs from one format to another for GTF, GFF3, BAM files etc. Downstream, GTF/GFF3 files are often used for transcriptome annotation by TopHat (https://ccb.jhu.edu/software/tophat/manual.shtml) or reference annotation by CuffLinks (http://cole-trapnell-lab.github.io/cufflinks/cufflinks/index.html). Quick and easy conversion of the sequence IDs can help make NGS analyses pipelines much more efficient for both veteran and new users of bioinformatics. 

A summary of the commands is provided below.

Command | Description
------------ | -------------
seqconv guess | Infers file type
seqconv convert | Converts sequence IDs
seqconv help | Print help menu
seqconv version | What version of SeqIDMapper
seqconv contact | Feature requests, begs, mailing lists


### Installation

```
some lines of code go here and then something happens
```
