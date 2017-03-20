

import os
import sys
import argparse
from clint.textui import puts, indent, colored

# Infer the filetype if not specified.
# is specified, check if it makes sense
#Filetypes to use
# gff3
# gff2
# gtf
# bed
# sam

def get_ext(file):
    filename, file_extension = os.path.splitext(file)
    if "." in file_extension:
        param, value = file_extension.split(".",1)
    return value, filename

def check_gff3_file_format(file):
    print file
    with open(file) as myfile:
        test_passed = 0
        head = [next(myfile) for x in xrange(10)]
        if head[0] == "##gff-version 3":
            test_passed++
        
        for line in head:

        print head
#One method if the seqID is in column 1

def infer_type(input_file):
    ext, file = get_ext(input_file)
    if ext == 'gff' or ext == 'gff3' or ext == 'gtf' or ext =='bed':
        if ext == 'gff3' or ext =='gff':
            gff3_valid = check_gff3_file_format(input_file)
            print gff3_valid

        print "%s  extension reports as %s.  Replace IDs in column 1" % (input_file, ext)
    else:
        print "Filetype %s is not supported" %(ext)


def main(args = sys.argv[1:]):
    parser = argparse.ArgumentParser()

    parser.add_argument("--square",
                        help="Used for testing",
                        type=int,
                        default=None)

    parser.add_argument("--input_file",
                        help="input file",
                        type=str)

    args = parser.parse_args(args)

    if args.square:
        print(args.square**2)
    elif (args.input_file):            
        infer_type(args.input_file)
    else:
        with indent(4):
            puts(colored.blue("Arguments"))
            puts(colored.green("Input file: ") + str(args.input_file))

if __name__ == '__main__':
    main()

