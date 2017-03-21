import os
import sys
import argparse
from clint.textui import puts, indent, colored
from itertools import islice


def get_ext(file):
    filename, file_extension = os.path.splitext(file)
    if "." in file_extension:
        param, value = file_extension.split(".",1)
    return value, filename

def check_header(header):
    # takes a list and iterates through to find format
    format = 'NA'
    for line in header:
        if header[0]== "##gff-version 3\n":
            format = 'gff3'
            break
#            break            
        if line.startswith('@'):
            format = 'sam'
        elif check_gff3_file_format(header) is True:
            format = 'gff3'
        elif check_gtf_file_format(header) is True:
            format = 'gtf'
        elif check_bed_file_format(header) is True:
            format = 'bed'
#    print format
    return format


def check_num_of_columns(header):
    cols = ''
    for line in header:
        if line.startswith("#"):
            next
        else:
            items = line.split("\t")
            cols = len(items)
    return cols

def check_gff3_file_format(header):
    status = False
    gff3_header = False
    nine_cols = True
    cols = check_num_of_columns(header)
    if header[0] == "##gff-version 3\n":
        gff3_header = True
        cols = check_num_of_columns(header)
        if cols == '9':
            nine_cols = True
        if nine_cols == True and gff3_header == True:
            status = True
    return status


def check_bed_file_format(header):
    status = False
    cols = check_num_of_columns(header)
    print (cols)
    if cols >= 3 and cols <= 12:
        status = True
    return status

def check_gtf_file_format(header):
    status = False
    cols = check_num_of_columns(header)
    if cols == 9:
        status = True
    return status

def get_header(file):
    head = ''
    print (file)
    with open(file) as myfile:
        head = list(islice(myfile, 100))
    return head

def infer_type(input_file):
    header = get_header(input_file)
    ext, file = get_ext(input_file)
    if ext == 'gff' or ext == 'gff3' or ext == 'gtf' or ext =='bed':
        if ext == 'gff3' or ext =='gff':
            gff3_status = check_gff3_file_format(header)
            if gff3_status == True:
                print ("%s passes as gff.  Replace IDs in column 1", input_file)
        elif ext == 'gtf':
            gtf_status = check_gtf_file_format(header)
            if gtf_status is True:
                print ("%s passes as gtf.  Replace IDs in column 1", input_file)
#### Need bedfile for testing
        elif ext =='bed':
            print ('bed')
            check_bed_file_format(header)
####
        elif ext =='sam':
            print ('sam')
#        else:
#            print "Filetype %s is not supported" %(ext)                
        header_format = check_header(header)
        if header_format == "NA":
            print (error)
        else:
            print ("processing header")
            print (header_format)

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

