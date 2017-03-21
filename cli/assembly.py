import re
import os
import sys
import optparse


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

    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=assembly&term={assembly}[Assembly%20Name]"

    # with does not work with python2 ==> remooving all with
    response = urlopen(search_url.format(assembly=assembly))
    r = str(response.read())
    # with urlopen(search_url.format(assembly=assembly)) as response:
    #         r = str(response.read())

    id_set = list(map(int, re.findall("<Id>(.*)</Id>", r))) # cast as list python 3.5
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=assembly&id={id}"
    #r = requests.get(fetch_url.format(id = id_set[0])).text

    response = urlopen(fetch_url.format(id=id_set[0]))
    r = str(response.read())
    # with urlopen(fetch_url.format(id=id_set[0])) as response:
    #         r = str(response.read())

    re.findall("<FtpPath_Assembly_rpt>(.*)</FtpPath_Assembly_rpt>", r)

    GCF_assembly_report_url = re.findall("<FtpPath_Assembly_rpt>(.*)</FtpPath_Assembly_rpt>", r)[0]
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

    sys.stderr.write('from {} to {}'.format(id_from,id_to))
    # find correct colum for convertion
    id2col = {'sn':0,
                 'gb':5,
                 'rs':6,
                 'au':7,
                 'uc':9}
    to_col = id2col[id_to]

    # format specified by user
    if id_from:
        from_col = id2col[id_from]
    # guess format
    else:
        l_id_from = [id for id in id2col if id!= id_from]



    d_from2to = {}


    # Fetch assembly_report to NCBI
    f = urlopen(p_assemblyreport)
    # with statement does not work with python2
    #with urlopen(p_assemblyreport) as f:
    #with open(p_assemblyreport)as f:

    if True:
        for line in f:
            line = line.decode("utf-8")


            if line.startswith('#'):
                continue

            sp = line.strip().split('\t')


            try:
                id_to = sp[to_col]
            except:
                id_to = 'NA'

            # user specified the id_from
            if id_from:
                cur_id_from = sp[from_col]
                d_from2to[cur_id_from] = [id_to, id_from]



            # guessing mode
            else:
                for ite_id_from in l_id_from:
                    cur_from_col = id2col[ite_id_from]


                    try:
                        cur_id_from = sp[cur_from_col]
                    except:
                        cur_id_from = 'NA'

                    d_from2to[cur_id_from] = [id_to, ite_id_from]


    return d_from2to


def convert(f_input, d_mapper, pos_col, guess=None):
    """

    :param p_gff3: path to input gff3 file
    :param d_mapper: [idtoconvert] -> idconverted
    :param na: manage the way to output the line if id_to point to NA
    :param pos_col is the column position we need to convert, 0 based!
    :return: None

    """

    sys.stderr.write('STARTING CONVERTION\n')



    # recall key to reduce time
    current_idfrom = None
    current_idto = None
    length_idfrom = None
    current_format = None

    for line in f_input:

        # comment lines => no convertion
        # sharp for gff and arobase for sam
        if line.startswith('# ') or line.startswith('@'):
            str_gff = line

        # ##sequence-region line
        # TODO scan only if gff3?
        elif line.startswith('##sequence-region'):
            sp = line.strip().split()
            idtoconvert = sp[1]

            # if can't mapp we skip the line
            try:
                idconverted, id_format = d_mapper[idtoconvert]
            except:
                sys.stderr.write('Cannot find idtoconvert in the mapper {0}\n'.format(idtoconvert))
                continue

            current_idfrom = idtoconvert
            current_idto = idconverted
            length_idfrom = len(current_idfrom)
            current_format = id_format


            # if mapp to an NA we skip the line
            if idconverted.lower() == 'na':
                sys.stderr.write('No corresponding to {0} in {1}\n'.format(current_idfrom, current_format))
                continue

            # output format
            str_gff = '##sequence-region {seqid} {eol}\n'.format(seqid = current_idto, eol=' '.join(sp[2:]))

        elif line.startswith('#'):
            str_gff = line

        # coord lines ==> convertion
        else:
            sp = line.strip().split('\t')
            # check if previous line has the same accession to avoid another dictionary search
            if current_idfrom == line[:length_idfrom]:
                idconverted = current_idto
            else:
                idtoconvert = sp[pos_col] # pos_col is 0 based

                try:
                    idconverted, id_format = d_mapper[idtoconvert]
                except:
                    sys.stderr.write('Cannot find idtoconvert in the mapper {0}\n'.format(idtoconvert))
                    continue

                current_idfrom = idtoconvert
                current_idto = idconverted
                length_idfrom = len(idtoconvert)

            if idconverted.lower() == 'na':
                sys.stderr.write('No corresponding to {0} in {1}\n'.format(idtoconvert, id_format))
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
              id_to=None):
    """

    :param p_assemblyreport: p_assembly_report path to the input assembly report file
    :param f_input: is an opened file of any format gff3, sam, gtf etc...
    :param pos_col: is the column number to convert in the f_input object file
    :param id_from: institution id use sn, gb, rs, au, uc
    :param id_to: instituion id use sn, gb, rs, au, uc
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
    if not id_from:
        convert(f_input=f_input,
                pos_col=pos_col,
                d_mapper=d_mapper,
                guess=True)
    else:
                convert(f_input=f_input,
                pos_col=pos_col,
                d_mapper=d_mapper,
                guess=False)

    return None

if __name__== '__main__':

    ### TESTING AREA
    #

    # USER PROVIDE ASSEMBLY NAME
    assembly_name = 'GRCh38.p10'

    # ID FROM CAN BE GUESSED IS None
    id_from = None

    # ID TO IS THE FORMAT CONVERTION DESIRED
    id_to = 'uc'

    # GFF3 FILE INPUT
    p_gff3 = 'GCF_000001405.36_GRCh38.p10_genomic.gff'
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
              id_to=id_to)



