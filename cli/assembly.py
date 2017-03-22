import re
import os
import sys
import optparse
from cli import bcolors
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

id2col = {'sn':0,
          'gb':5,
          'rs':6,
          'au':7,
          'uc':9,
          'sequence-name':0,
          'assembly-unit':7,
          'genbank':5,
          'refseq':6,
          'ucsc':9}

# TODO debug python2x
# TODO full name of id format

# Managing python version
if sys.version_info >= (3,0):
    from urllib.request import urlopen # Python3
else:
    from urllib2 import urlopen # Python 2

##### FUNCTIONS
def fetch_assembly_report(assembly):
    """
        Fetch an assembly report from an assembly name
    """
    q_type = "Assembly%20Name"
    if assembly.startswith("GCF_") or assembly.startswith("GCA_"):
        q_type = "Assembly%20Accession"
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=assembly&term={assembly}[{q_type}]"

    # with does not work with python2 ==> remooving all with
    response = urlopen(search_url.format(assembly=assembly, q_type=q_type))
    r = str(response.read())
    id_set = list(map(int, re.findall("<Id>([0-9]+)</Id>", r))) # cast as list python 3.5
    if not id_set:
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=assembly&term={assembly}[All%20Names]"
        response = urlopen(search_url.format(assembly=assembly, q_type=q_type))
        r = str(response.read())
        id_set = list(map(int, re.findall("<Id>([0-9]+)</Id>", r))) # cast as list python 3.5
        if len(id_set) > 1:
            sys.stderr.write(bcolors.FAIL + ("\n\tAmbiguous reference name\n\n" % assembly) + bcolors.ENDC)
            exit(1)           

    if not id_set:
        sys.stderr.write(bcolors.FAIL + ("\n\tReference '%s' not found\n\n" % assembly) + bcolors.ENDC)
        exit(1)
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=assembly&id={id}"

    response = urlopen(fetch_url.format(id=id_set[0]))
    r = str(response.read())

    re.findall("<FtpPath_Assembly_rpt>(.*)</FtpPath_Assembly_rpt>", r , re.I|re.M)

    GCF_assembly_report_url = re.findall("<FtpPath_Assembly_rpt>(.*)</FtpPath_Assembly_rpt>", r)[0]
    print(GCF_assembly_report_url)
    return GCF_assembly_report_url.replace("ftp://", "http://")


def get_mapper(p_assemblyreport, id_from=None, id_to='sn'):
    """
    Get correspondance of id provided by user
    use sn, gb, rs, au, uc as id descriptor
    Column based 1
    1, sn, Sequence-Name
    5 gb, GenBank-Accn
    7, rs, RefSeq-Accn
    8, au, Assembly-Unit
    10, uc, UCSC-style-name

    if id_from is not given, we store all possibility to guess the from


    NCBI report assembly file example:
    Sequence-Name Sequence-Role   Assigned-Molecule       Assigned-Molecule-Location/Type GenBank-Accn    Relationship    RefSeq-Accn     Assembly-Unit   Sequence-Length UCSC-style-name
    1       assembled-molecule      1       Chromosome      CM000663.2      =       NC_000001.11    Primary Assembly        248956422       chr1
    2       assembled-molecule      2       Chromosome      CM000664.2      =       NC_000002.12    Primary Assembly        242193529       chr2
    3       assembled-molecule      3       Chromosome      CM000665.2      =       NC_000003.12    Primary Assembly        198295559       chr3



    :param p_assemblyreport: p_assembly_report path to the input assembly report file
    :param id_from: institution id use sn, gb, rs, au, uc, is None, guessing mode
    :param id_to: instituion id use sn, gb, rs, au, uc
    :return: d_from2to [id from] -> id to
    """

    sys.stderr.write('Converting from {} to {}'.format(id_from,id_to))



    d_from2to = {}

    # Fetch assembly_report to NCBI
    f = urlopen(p_assemblyreport)
    # with statement does not work with python2
    # with urlopen(p_assemblyreport) as f:
    # with open(p_assemblyreport)as f:


    # Assembly report idformat order storage
    d_order = {'GenBank-Accn':None,
            'Sequence-Name':None,
           'RefSeq-Accn':None,
           'Assembly-Unit':None,
           'UCSC-style-name':None}


    d_cor = {'GenBank-Accn':['gb', 'genbank'],
            'Sequence-Name':['sn','sequence-name'],
           'RefSeq-Accn':['rs','refseq'],
           'Assembly-Unit':['au','assembly-unit'],
           'UCSC-style-name':['us','ucsc']}

    # This dictionary is fully updated LATER from assembly report
    id2col = {'sn':0,
          'gb':5,
          'rs':6,
          'au':7,
          'uc':9,
          'sequence-name':0,
          'assembly-unit':7,
          'genbank':5,
          'refseq':6,
          'ucsc':9}

    if True:
        for line in f:
            line = line.decode("utf-8")

            if line.startswith('#'):

                # find order of the id format in the assembly report file
                if 'Sequence-Name' in line:

                    # UPDATE OF THE DICTIONARY TO GET THE CORRECT ORDER
                    # Load the order from assembly report header
                    for colpos, idformat in enumerate(line[1:].strip().split('\t')):

                        if idformat in d_order:
                            single_letter_id, fullname_id = d_cor[idformat]
                            id2col[single_letter_id] = colpos
                            id2col[fullname_id] = colpos



                    # find correct colum for convertion
                    to_col = id2col[id_to]

                    # format specified by user
                    if id_from:
                        from_col = id2col[id_from]
                    # guess format
                    else:
                        l_id_from = [id for id in id2col if id!= id_from]

                continue



            sp = line.strip().split('\t')


            try:
                id_to = sp[to_col]
            except:
                id_to = 'NA'

            # user specified the id_from
            if id_from:
                cur_id_from = sp[from_col]
                d_from2to[cur_id_from.lower()] = [id_to, id_from]



            # guessing mode
            else:
                for ite_id_from in l_id_from:
                    cur_from_col = id2col[ite_id_from]


                    try:
                        cur_id_from = sp[cur_from_col]
                    except:
                        cur_id_from = 'NA'

                    d_from2to[cur_id_from.lower()] = [id_to, ite_id_from]


    return d_from2to


def convert(f_input, d_mapper, pos_col, guess=None, na=False):
    """

    :param p_gff3: path to input gff3 file
    :param d_mapper: [idtoconvert] -> idconverted
    :param na: manage the way to output the line if id_to point to NA
    :param pos_col is the column position we need to convert, 0 based!
    :param na True screeh the non converted line is NA convertion is faced, False na is indicated in stderr
    :return: None

    """

    sys.stderr.write('Starting Conversion\n')
    # recall key to reduce time
    current_idfrom = None
    current_idto = None
    length_idfrom = None
    current_format = None
    id_format = None
    last_error = None
    print(d_mapper)
    for line in f_input:
        line = line#.decode("utf-8")
        # comment lines => no convertion
        # sharp for gff and arobase for sam
        if line.startswith('#') or line.startswith('@'):
            str_gff = line

        # ##sequence-region line
        # TODO scan only if gff3?
        elif line.startswith('##sequence-region'):
            sp = line.strip().split()
            idtoconvert = sp[1].lower()

            # if can't mapp we skip the line
            try:
                idconverted, id_format = d_mapper[idtoconvert]
            except:
                new_error = 'Cannot convert id: {0}\n'.format(idtoconvert)
                if last_error != new_error:
                    sys.stderr.write(new_error)
                    last_error = new_error
                continue

            current_idfrom = idtoconvert
            current_idto = idconverted
            length_idfrom = len(current_idfrom)
            current_format = id_format

            # if map to an NA we skip the line
            if idconverted.lower() in ['na', '<>']:
                new_error = 'No corresponding id for {0} from {1}\n'.format(current_idfrom, current_format)
                if last_error != new_error:
                    sys.stderr.write(new_error)
                    last_error = new_error

                if na:
                    sys.stdout.write(line)
                continue

            # output format
            str_gff = '##sequence-region {seqid} {eol}\n'.format(seqid = current_idto, eol=' '.join(sp[2:]))

        elif line.startswith('#'):
            str_gff = line

        # coord lines ==> convertion
        else:
            sp = line.strip().split('\t')
            # check if previous line has the same accession to avoid another dictionary search
            if current_idfrom == line[:length_idfrom].lower():
                idconverted = current_idto
            else:
                idtoconvert = sp[pos_col].lower() # pos_col is 0 based

                try:
                    idconverted, id_format = d_mapper[idtoconvert]
                except:
                    new_error = 'Cannot convert id: {0}\n'.format(idtoconvert)
                    if last_error != new_error:
                        sys.stderr.write(new_error)
                        last_error = new_error
                    if na:
                        sys.stdout.write(line)
                    continue

                current_idfrom = idtoconvert
                current_idto = idconverted
                length_idfrom = len(idtoconvert)

            # if mapp to an NA we skip the line
            if idconverted.lower() in ['na', '<>']:
                new_error = 'No corresponding id for {0} from {1}\n'.format(current_idfrom, current_format)
                if last_error != new_error:
                    sys.stderr.write(new_error)
                    last_error = new_error
                if na:
                    sys.stdout.write(line)
                continue

            # output format
            sp[pos_col] = idconverted
            str_gff = '\t'.join(sp)+'\n'

            #str_gff ='{seqid}\t{eol}'.format(seqid=idconverted, eol=line[length_idfrom:])

        # final output writing
        sys.stdout.write(str_gff)

    if guess:
        sys.stderr.write('FORMAT detected: {}'.format(id_format))
    return None

def converter(p_assemblyreport=None,\
              f_input=None,\
              pos_col=None,
              id_from=None,
              id_to=None,
              na=False):
    """

    :param p_assemblyreport: p_assembly_report path to the input assembly report file
    :param f_input: is an opened file of any format gff3, sam, gtf etc...
    :param pos_col: is the column number to convert in the f_input object file
    :param id_from: institution id use sn, gb, rs, au, uc
    :param id_to: instituion id use sn, gb, rs, au, uc
    :param na True when no convertion possible, non converted line is given, False only stderr message
    :return:
    """

    # get mapping
    # id: 1, sn, Sequence-Name
    # id: 5 gb, GenBank-Accn
    # id: 7, rs, RefSeq-Accn
    # id: 8, au, Assembly-Unit
    # id: 10, uc, UCSC-style-name
    # d_mapper [inst_from] -> inst_to
    d_mapper = get_mapper(p_assemblyreport, id_from, id_to)

    # apply the mapp to convert the gff3
    try:
        if not id_from:
            convert(f_input=f_input,
                    pos_col=pos_col,
                    d_mapper=d_mapper,
                    guess=True, na=False)
        else:
                    convert(f_input=f_input,
                    pos_col=pos_col,
                    d_mapper=d_mapper,
                    guess=False, na=False)
    except (KeyboardInterrupt, SystemExit, BrokenPipeError):
        pass

    return None

if __name__== '__main__':

    ### TESTING AREA
    #

    # USER PROVIDE ASSEMBLY NAME
    assembly_name = 'GCF_000003055.6'

    # ID FROM CAN BE GUESSED IS None
    id_from = None

    # ID TO IS THE FORMAT CONVERTION DESIRED
    id_to = 'rs'

    # GFF3 FILE INPUT
    p_gff3 = 'cow_bosTau6_UCSC_2009'
    # new format => this is a file object
    f_gff3 = open(p_gff3)

    # Column number
    pos_col = 0

    # OUTPUT FILE
    p_output = 'converted.gff3'


    #### CORE
    # GET ASSEMBLY REPORT
    p_assembly_report = fetch_assembly_report(assembly_name)

    #p_assembly_report='GCF_000001405.36_GRCh38.p10_assembly_report.txt'
    converter(p_assemblyreport=p_assembly_report,\
              f_input=f_gff3,\
              pos_col=pos_col,\
              id_from=id_from,\
              id_to=id_to,
              na=True)
