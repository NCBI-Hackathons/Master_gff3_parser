import re
import requests

def fetch_assembly_report(assembly):
    """
        Fetch an assembly report from an assembly name
    """
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=assembly&term={assembly}[Assembly%20Name]"
    r = requests.get(search_url.format(assembly = assembly)).text
    id_set = map(int, re.findall("<Id>(.*)</Id>", r))
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=assembly&id={id}"
    r = requests.get(fetch_url.format(id = id_set[0])).text
    GCF_assembly_report_url = re.findall("<FtpPath_Assembly_rpt>(.*)</FtpPath_Assembly_rpt>", r)[0]
    return GCF_assembly_report_url.replace("ftp://", "http://")
    