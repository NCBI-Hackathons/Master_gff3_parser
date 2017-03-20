import sys
import argparse
from . import _program
from clint.textui import puts, puts_err, indent, colored


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
            with indent(4):
                puts_err(colored.red("\n%s: Unrecognized command\n" % sub_comm[0]))
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

        with indent(4):
            puts_err(colored.blue("\nConverting IDs\n"))

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
        with indent(4):
            puts_err(colored.blue("\nAttempting to identify reference genome\n"))
        args = parser.parse_args(sys.argv[2:])

        # Code for identifying reference goes here!




def main(args = sys.argv[1:]):
    comm()

if __name__ == '__main__':
    main()
