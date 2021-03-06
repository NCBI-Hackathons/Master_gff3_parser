[![Coverage Status](https://coveralls.io/repos/github/NCBI-Hackathons/Master_gff3_parser/badge.svg?branch=master)](https://coveralls.io/github/NCBI-Hackathons/Master_gff3_parser?branch=master) [![Build Status](https://travis-ci.org/NCBI-Hackathons/Master_gff3_parser.svg?branch=master)](https://travis-ci.org/NCBI-Hackathons/Master_gff3_parser) [![](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat)](http://seqconv.readthedocs.io/en/latest/)

# Squidstream (an amazing tool that does wonderful stuff)—Documentation
Generic Feature Format version 3 (GFF3) is a file type that is commonly used in bioinformatic applications. Different institutions have varying naming conventions for the genomic identifier column in the GFF3 format. Therefore, there can be GFF3 files that use different seqids for the same genomic feature.  In addition, there are other file formats that also have sequence identifiers, such as GTF, BED, SAM, and BAM files. Squidstream is an easy-to-use command line tool that can convert the genomic feature reference name for chromosomes, scaffolds, and contigs in different file formats to the corresponding seqid from NCBI’s RefSeq database.  GFF3 files are a common input into many different types of bioinformatics tools and pipelines, and Squidstream provides naming consistency in these input files by converting the sequence feature IDs in the entire file to the desired ID format using a single command.

![Squidstream Workflow:](https://github.com/NCBI-Hackathons/Master_gff3_parser/blob/master/GFF3%20formats.png)
Figure 1. Examples of NCBI, UCSC, and RefSeq GFF3 files.

Sequence Identifier Conversion Examples:
* Annotation with RefSeq ID to UCSC ID for use in  UCSC Genome Browser tracks
* Convert to NCBI ID to search KEGG GENES Database
* RefSeq to Genbank ID


Squidstream was built in Python and runs from the command line. Users provide the input file, the specific reference genome, and the desired name of the output file.

A summary of the **seqconv** commands is provided below.

Command | Description
------------ | -------------
convert | Converts sequence IDs

Links to file format descriptions:
[GFF3,](https://www.google.com/url?q=https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md&sa=D&ust=1490199000838000&usg=AFQjCNGJrt_qqhwtBufCdrc0sT28hntlVg)
[SAM,](https://samtools.github.io/hts-specs/SAMv1.pdf)
[BED,](http://useast.ensembl.org/info/website/upload/bed.html)
[GFF/GTF](http://useast.ensembl.org/info/website/upload/gff.html)


### Installation

Linux:

```
python setup.py install
```

OSX:

```
python setup.py install
```

![Squidstream Workflow:](https://github.com/NCBI-Hackathons/Master_gff3_parser/blob/master/SquidStream%20workflow.png)

Figure 2. Squidstream workflow.

