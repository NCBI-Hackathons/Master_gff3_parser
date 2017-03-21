[![Coverage Status](https://coveralls.io/repos/github/NCBI-Hackathons/Master_gff3_parser/badge.svg?branch=master)](https://coveralls.io/github/NCBI-Hackathons/Master_gff3_parser?branch=master) [![Build Status](https://travis-ci.org/NCBI-Hackathons/Master_gff3_parser.svg?branch=master)](https://travis-ci.org/NCBI-Hackathons/Master_gff3_parser) [![](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat)](https://ncbi-hackathons.github.io/Master_gff3_parser/)

# SeqIDMapper (an amazing tool that does wonderful stuff)—Documentation
Generic Feature Format version 3 (GFF3) is a file type that is commonly used in bioinformatic applications. Different institutions have varying naming conventions for the seqid identifier column in the GFF3 format. Therefore, there can be GFF3 files that use different seqids for the same genomic feature.  In addition, there are other file formats that also have sequence identifiers, such as GTF, BED, SAM, and BAM files. SeqIDMapper is an easy-to-use command line tool that can convert the sequence reference name in different file formats to the corresponding seqid from NCBI’s RefSeq database.  GFF3 files are a common input into many different types of bioinformatics tools and pipelines, and SeqIDMapper provides naming consistency in these input files.


A summary of the commands is provided below.

Command | Description
------------ | -------------
seqconv guess | Infers file type
seqconv convert | Converts sequence IDs
seqconv help | Print help menu
seqconv version | What version of SeqIDMapper
seqconv contact | Feature requests, bugs, mailing lists


### Installation

```
some lines of code go here and then something happens
```
![SeqIDMapper Workflow:](https://github.com/NCBI-Hackathons/Master_gff3_parser/blob/master/seqidmapper.png?raw=true)
Figure 1. SeqIDMapper workflow.
