import pytest

from inbome.parse import parse_inbome_header

def test_example1(datadir, gpg):
    with datadir.open("example1.mail") as fp:
        d = parse_inbome_header(fp)
        assert d["to"] == "dkg@fifthhorseman.net"
        assert "key" in d and d["key"]

    gpg.import_keydata(d["key"])


