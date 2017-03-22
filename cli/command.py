import sys
import os
import argparse
from . import _program, bcolors
from cli.assembly import *
from cli.filetype import file_from_stream, file_from_name

usage_str = '''seqconv <command> [<args>]

Commands
   convert     Convert sequence identifiers

'''

id_types = '''
in/out id types:
  * refseq (rs)
  * genbank (gb)
  * ucsc (uc)
  * sequence-name (sn)
  * assembly-unit (au)

'''

id_types_indent = '\n'.join(["\t" + x for x in id_types.split("\n")]) + "\n"

conv_str = '''seqconv convert [--ref <reference> --in <input-id>] --out <output-id> <file>

Usage
   --ref     reference genome
   --in      input id type (optional)
   --out     output id type
   <file>    file or stream
''' + id_types


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
        parser.add_argument('--ref', type=str, default=None)
        parser.add_argument('--in', type=str, default=None)
        parser.add_argument('--out', type=str)
        parser.add_argument('<file>', type=read_file)          
            
        args = parser.parse_args(sys.argv[2:])
        in_id = getattr(args,'in')
        fname = getattr(args, "<file>")

        # Check if in and out specified correctly
        if in_id != None and in_id not in id2col.keys():
            sys.stderr.write(bcolors.FAIL + "\n\tInvalid input ID specified\n\n" + id_types_indent + bcolors.ENDC)           
            exit(1)    

        if args.out not in id2col.keys():
            sys.stderr.write(bcolors.FAIL + "\n\tInvalid output ID specified\n\n" + id_types_indent + bcolors.ENDC)           
            exit(1)            

        # Check if file or stream exists
        if not os.path.isfile(fname) and fname != "-":
            sys.stderr.write(bcolors.FAIL + "\n\t'%s' not found\n\n" % fname + bcolors.ENDC)           
            exit(1)

        if fname == "-":
            fout = file_from_stream(sys.stdin)
            col_number = fout.id_column
        else:
            if not os.path.isfile(fname):
                pass
            fout, col_number = file_from_name(fname)
        
        assembly_report = fetch_assembly_report(args.ref)
        converter(p_assemblyreport=assembly_report,
                  f_input=fout,
                  pos_col=col_number,
                  id_from=in_id,
                  id_to=args.out)


def main(args = sys.argv[1:]):
    comm()

if __name__ == '__main__':
    main()
