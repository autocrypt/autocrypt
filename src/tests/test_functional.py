import pytest

from inbome.parse import parse_inbome_header

def test_rsa2048_simple(datadir, gpg):
    with datadir.open("rsa2048-simple.eml") as fp:
        d = parse_inbome_header(fp)
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert "key" in d and d["key"]

    gpg.import_keydata(d["key"])

def test_25519_simple(datadir, gpg):
    with datadir.open("25519-simple.eml") as fp:
        d = parse_inbome_header(fp)
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert "key" in d and d["key"]

    gpg.import_keydata(d["key"])

def test_rsa2048_explicit_type(datadir, gpg):
    with datadir.open("rsa2048-explicit-type.eml") as fp:
        d = parse_inbome_header(fp)
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert "key" in d and d["key"]

    gpg.import_keydata(d["key"])

def test_rsa2048_unknown_non_critical(datadir, gpg):
    with datadir.open("rsa2048-unknown-non-critical.eml") as fp:
        d = parse_inbome_header(fp)
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert "key" in d and d["key"]

    gpg.import_keydata(d["key"])
