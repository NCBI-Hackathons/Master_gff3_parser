import sys
import argparse
from . import _program
from shell import bcolors

def read_file(input):
    return input


class comm(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Sequence ID Conversion',
            usage='''seqconv <command> [<args>]

Commands
   convert     Convert sequence identifiers
   resolve     Attempt to identify the reference genome.
''')
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
            usage='''seqconv convert [--ref <reference> --in <input-id>] --out <output-id> <file>

Commands
   convert     Convert sequence identifiers

''')
        # prefixing the argument with -- means it's optional
        parser.add_argument('--ref', type=str, default=None)
        parser.add_argument('--in', type=str)
        parser.add_argument('--out', type=str)
        parser.add_argument('<file>', type=read_file)          

        sys.stderr.write(bcolors.BLUE + "\nConverting IDs\n" + bcolors.ENDC)
            
        args = parser.parse_args(sys.argv[2:])

        if not args.ref:
            # Resolve reference code goes here.
            pass

        # Code for checking input/output formats goes here!

        print(args)

        # Code for transforming goes here!

    def resolve(self):
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository',
            usage='''seqconv resolve <file>

Attempt to identify the reference genome given a GFF, BED, or SAM/BAM.

''')
        parser.add_argument('<file>', type=read_file)
        sys.stderr.write(bcolors.BLUE + "\n\tAttempting to identify reference genome\n" + bcolors.ENDC)
        args = parser.parse_args(sys.argv[2:])

        # Code for identifying reference goes here!




def main(args = sys.argv[1:]):
    comm()

if __name__ == '__main__':
    main()
