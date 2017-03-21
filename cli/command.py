import sys
import argparse
from . import _program
from cli.assembly import *
from cli.filetype import file_from_stream, file_from_name


class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

usage_str = '''seqconv <command> [<args>]

Commands
   convert     Convert sequence identifiers
   resolve     Attempt to identify the reference genome.
'''

conv_str = '''seqconv convert [--ref <reference> --in <input-id>] --out <output-id> <file>

Commands
   convert     Convert sequence identifiers

'''

resolve_str = '''seqconv resolve <file>

Attempt to identify the reference genome given a GFF, BED, or SAM/BAM.

'''

def read_file(input):
    return input


class comm(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Sequence ID Conversion',
            usage=usage_str)
        parser.add_argument('command', help='Subcommand to run')
        sub_comm = sys.argv[1:2]
        args = parser.parse_args(sub_comm)
        if not hasattr(self, args.command):
            sys.stderr.write(bcolors.FAIL + "\n\t%s: Unrecognized command\n" % sub_comm[0] + bcolors.ENDC)
            exit(1)
        getattr(self, args.command)()

    def convert(self):
        parser = argparse.ArgumentParser(
            description='Record changes to the repository',
            usage=conv_str)
        # prefixing the argument with -- means it's optional
        parser.add_argument('--ref', type=str, default=None)
        parser.add_argument('--id_from', type=str, default=None)
        parser.add_argument('--id_to', type=str)
        parser.add_argument('<file>', type=read_file)          

        sys.stderr.write(bcolors.BLUE + "\nConverting IDs\n" + bcolors.ENDC)
            
        args = parser.parse_args(sys.argv[2:])
        print(args)
        if not args.ref:
            # Resolve reference code goes here.
            pass

        # Code for checking input/output formats goes here!

        fname = getattr(args, "<file>")
        if fname == "-":
            fout = file_from_stream(sys.stdin)
            col_number = fout.id_column
        else:
            fout, col_number = file_from_name(fname)
        
        p_assembly_report = fetch_assembly_report(args.ref)

        #p_assembly_report='GCF_000001405.36_GRCh38.p10_assembly_report.txt'
        converter(p_assemblyreport=p_assembly_report,
                  f_input=fout,
                  pos_col=col_number,
                  id_from=args.id_from,
                  id_to=args.id_to)




        # Code for transforming goes here!
    def resolve(self):
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository',
            usage=resolve_str)
        parser.add_argument('<file>', type=read_file)
        sys.stderr.write(bcolors.BLUE + "\n\tAttempting to identify reference genome\n" + bcolors.ENDC)
        args = parser.parse_args(sys.argv[2:])

        # Code for identifying reference goes here!




def main(args = sys.argv[1:]):
    comm()

if __name__ == '__main__':
    main()
