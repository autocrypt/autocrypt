from __future__ import unicode_literals
import pytest
import six
from autocrypt import header


def make_ac_dict(**kwargs):
    d = {}
    for name, val in kwargs.items():
        d[six.text_type(name)] = val
    d.setdefault("type", "p")
    d.setdefault("prefer-encrypt", "notset")
    return d


def test_genkey_make_and_parse_header():
    adr, keydata = "x@xy.z", b"123"
    h = header.make_header(emailadr=adr, keydata=keydata)
    assert h.startswith("Autocrypt: ")
    d = header.parse_ac_headervalue(h[10:])
    assert not header.verify_ac_dict(d)
    assert d == make_ac_dict(to=adr, key=keydata)


def test_genkey_make_and_parse_header_errors():
    adr, keydata = "x@xy.z", b"123"
    h = header.make_header(
        emailadr=adr, keydata=keydata, prefer_encrypt="notset", keytype="x")
    assert "prefer-encrypt" not in h, h
    d = header.parse_ac_headervalue(h[10:])
    assert "unknown key type" in header.verify_ac_dict(d)[0]
    assert d == make_ac_dict(to=adr, key=keydata, type="x")


class TestEmailCorpus:
    def test_rsa2048_simple(self, datadir, bingpg):
        d = datadir.parse_ac_header_from_email("rsa2048-simple.eml")
        assert d["to"] == "alice@testsuite.autocrypt.org", d
        keyid = bingpg.import_keydata(d["key"])

    def test_25519_simple(self, datadir, bingpg):
        if (not bingpg.supports_eddsa()):
            pytest.xfail("No support for EDDSA")
        d = datadir.parse_ac_header_from_email("25519-simple.eml")
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert "key" in d and d["key"]
        bingpg.import_keydata(d["key"])

    def test_rsa2048_explicit_type(self, datadir, bingpg):
        d = datadir.parse_ac_header_from_email("rsa2048-explicit-type.eml")
        assert d["to"] == "alice@testsuite.autocrypt.org"
        bingpg.import_keydata(d["key"])

    def test_rsa2048_unknown_non_critical(self, datadir, bingpg):
        d = datadir.parse_ac_header_from_email("rsa2048-unknown-non-critical.eml")
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert d["_monkey"] == "ignore"
        bingpg.import_keydata(d["key"])

    def test_rsa2048_unknown_critical(self, datadir):
        d = datadir.parse_ac_header_from_email("rsa2048-unknown-critical.eml")
        l = header.verify_ac_dict(d)
        assert len(l) == 1
        assert "unknown critical attr 'danger'" in l[0]

    def test_unknown_type(self, datadir):
        d = datadir.parse_ac_header_from_email("unknown-type.eml")
        l = header.verify_ac_dict(d)
        assert len(l) == 1
        assert "unknown key type 'x'" in l[0]
