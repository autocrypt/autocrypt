import pytest
from autocrypt.parse import extract_autocrypt_header, parse_message

def parse_autocrypt_header(fp):
    msg = parse_message(fp)
    return extract_autocrypt_header(msg)

def test_rsa2048_simple(datadir, bingpg):
    with datadir.open("rsa2048-simple.eml") as fp:
        d = parse_autocrypt_header(fp)
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert "key" in d and d["key"]

    bingpg.import_keydata(d["key"])

def test_25519_simple(datadir, bingpg):
    if (not bingpg.supports_eddsa()):
        pytest.xfail("No support for EDDSA")
    with datadir.open("25519-simple.eml") as fp:
        d = parse_autocrypt_header(fp)
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert "key" in d and d["key"]

    bingpg.import_keydata(d["key"])

def test_rsa2048_explicit_type(datadir, bingpg):
    with datadir.open("rsa2048-explicit-type.eml") as fp:
        d = parse_autocrypt_header(fp)
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert "key" in d and d["key"]

    bingpg.import_keydata(d["key"])

def test_rsa2048_unknown_non_critical(datadir, bingpg):
    with datadir.open("rsa2048-unknown-non-critical.eml") as fp:
        d = parse_autocrypt_header(fp)
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert "key" in d and d["key"]

    bingpg.import_keydata(d["key"])

def test_rsa2048_unknown_critical(datadir, bingpg):
    with datadir.open("rsa2048-unknown-critical.eml") as fp:
        d = parse_autocrypt_header(fp)
        assert d == {}

def test_unknown_type(datadir, bingpg):
    with datadir.open("unknown-type.eml") as fp:
        d = parse_autocrypt_header(fp)
        assert d == {}
