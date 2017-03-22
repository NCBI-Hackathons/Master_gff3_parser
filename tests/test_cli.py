from cli import command
from tests.test_utilities import Capturing
from cli.assembly import fetch_assembly_report


def test_fetch_GRCh38():
    url = fetch_assembly_report("GRCh38")
    print(url)
    assert not url == "gasdf"
    assert url == "http://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.26_GRCh38/GCF_000001405.26_GRCh38_assembly_report.txt"
	


"""
def test_vars():
    with Capturing() as out:
        result = command.main(['--flag'])
    assert True
"""
