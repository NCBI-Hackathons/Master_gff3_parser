import re
import requests
import os
import sys
import optparse
import urllib.request

def fetch_assembly_report(assembly):
    """
        Fetch an assembly report from an assembly name
    """
    # if sys.version_info >= (3,0):
    #     urllib.request.urlopen()
    # else:
    #     pass

    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=assembly&term={assembly}[Assembly%20Name]"
    r = requests.get(search_url.format(assembly = assembly)).text
    id_set = list(map(int, re.findall("<Id>(.*)</Id>", r))) # cast as list python 3.5
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=assembly&id={id}"
    r = requests.get(fetch_url.format(id = id_set[0])).text
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
    with open(p_assemblyreport)as f:
        for line in f:
            if line.startswith('#'):
                continue

            sp = line.split('\t')


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


def convert(p_gff3, d_mapper, p_output, guess=False):
    """

    :param p_gff3: path to input gff3 file
    :param d_mapper: [idtoconvert] -> idconverted
    :param na: manage the way to output the line if id_to point to NA
    :param guess: if True we try to detect the id format
    :return: None

    """


    with open(p_output, 'w') as fout:

        with open(p_gff3) as f:
            # recall key to reduce time
            current_idfrom = None
            current_idto = None
            length_idfrom = None
            current_format = None

            for line in f:

                # comment lines => no convertion
                if line.startswith('# '):
                    str_gff = line

                # ##sequence-region line
                elif line.startswith('##sequence-region'):
                    sp = line.split()
                    idtoconvert = sp[1]

                    # if can't mapp we skip the line
                    try:
                        idconverted, id_format = d_mapper[idtoconvert]
                    except:
                        print ('Can find idtoconvert in the mapper', idtoconvert)
                        # TODO write a log file
                        continue

                    current_idfrom = idtoconvert
                    current_idto = idconverted
                    length_idfrom = len(current_idfrom)
                    current_format = id_format

                    # if mapp to an NA we skip the line
                    if idconverted == 'NA':
                        print ('No corresponding to {0} in {1}'.format(current_idfrom, current_format))
                        # TODO write a log file
                        continue

                    # output format
                    str_gff = '##sequence-region {seqid} {eol}'.format(seqid = current_idto, eol=' '.join(sp[2:]))

                elif line.startswith('#'):
                    str_gff = line

                # coord lines ==> convertion
                else:
                    # check if previous line has the same accession to avoid another dictionary search
                    if current_idfrom == line[:length_idfrom]:
                        idconverted = current_idto
                    else:
                        sp = line.split('\t')
                        idtoconvert = sp[0]

                        try:
                            idconverted, id_format = d_mapper[idtoconvert]
                        except:
                            # TODO write a log file
                            print ('Can find idtoconvert in the mapper', idtoconvert)
                            continue

                        current_idfrom = idtoconvert
                        current_idto = idconverted
                        length_idfrom = len(idtoconvert)

                    if idconverted == 'NA':
                        # TODO write a log file
                        print ('No corresponding to {} in {}'.format(idtoconvert, id_format))
                        continue



                    # output format
                    str_gff ='{seqid}\t{eol}'.format(seqid=idconverted, eol=line[length_idfrom:])

                # final output writing
                fout.write (str_gff)

    if guess:
        print ('FORMAT detected: ', id_format)
    return None

def converter(p_assemblyreport, id_from, id_to, p_gff3, p_output):
    """

    :param p_assemblyreport: p_assembly_report path to the input assembly report file
    :param id_from: institution id use sn, gb, rs, au, uc
    :param id_to: instituion id use sn, gb, rs, au, uc
    :param p_gff3: path to input gff3 file
    :param d_mapper: [idtoconvert] -> idconverted
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
        convert(p_gff3, d_mapper, p_output, guess=True)
    else:
        convert(p_gff3, d_mapper, p_output)

    return None

if __name__== '__main__':

    ### TESTING
    #
    assembly_name = 'GRCh38'
    id_from = None
    id_to = 'oc'
    p_gff3 = ''


    p_assembly_report = fetch_assembly_report(assembly_name)

    # assembly report
    # http://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.26_GRCh38/GCF_000001405.26_GRCh38_assembly_report.txt

    # generate the path to gff3
    # https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.26_GRCh38/GCF_000001405.26_GRCh38_genomic.gff.gz
    ## gff3 is provided by the users!!
    p_gff3 = p_assembly_report.split('_assembly_report.txt')[0]+ '_genomic.gff.gz'



    # TODO downloading assembly_report
    # TODO switch from requests to urllib
    # TODO detect python2 vs python3 to adapt urllib




    print (p_assembly_report, p_gff3)



    pass