import os
import sys
from itertools import islice
import gzip

class f_stream:
    """
        Read the first few lines
        of the stream to try to infer the 
        filetype
    """

    def __init__(self, stdin):
        self.stdin = stdin
        self.out_line_set = []
        lc = 0
        while lc <= 2:
            lc += 1
            line = self.stdin.readline()
            if not line:
                break
            self.out_line_set.append(line)

        if self.out_line_set[0].startswith("@"):
            self.id_column = 2
        else:
            self.id_column = 0

    def __iter__(self):
        for line in self.out_line_set:
            yield line
        for line in self.stdin:
            yield line


def file_from_name(fname):
    """
        Determine filetype from filename and return stream and id column
    """
    fname_l = fname.lower().replace(".gz", "")
    if any([fname_l.endswith(x) for x in ['gff', 'gff3','bed','gtf', 'vcf']]):
        id_column = 0
    elif [fname_l.endswith(x) for x in ['sam','bam']]:
        id_column = 2

    if fname.lower().endswith(".gz"):
        fout = gzip.GzipFile(fname, 'r')
    else:
        fout = open(fname, 'r')
    return fout, id_column

def file_from_stream(stdin):
    fout = f_stream(stdin)
    return fout


if __name__ == '__main__':
    main()

