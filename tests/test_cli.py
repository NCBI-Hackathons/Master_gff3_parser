from cli import command
from tests.test_utilities import Capturing
from cli.assembly import fetch_assembly_report


def test_fetch_GRCh38():
    url = fetch_assembly_report("GRCh38")
    print(url)
    assert url == "gasdf"



def test_vars():
    with Capturing() as out:
        result = command.main(['--flag'])
    assert True

