# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab

from __future__ import unicode_literals
import pytest
import six
from autocrypt import mime
from base64 import b64decode


def make_ac_dict(**kwargs):
    d = {}
    for name, val in kwargs.items():
        d[six.text_type(name)] = val
    d.setdefault("type", "p")
    d.setdefault("prefer-encrypt", "notset")
    return d

def test_parse_message_from_file(datadir):
    msg = mime.parse_message_from_file(datadir.open("rsa2048-simple.eml"))
    assert msg.get_all("Autocrypt")
    assert msg.get_payload()

def test_parse_message_from_string(datadir):
    msg = mime.parse_message_from_string(datadir.read("rsa2048-simple.eml"))
    assert msg.get_all("Autocrypt")
    assert msg.get_payload()


def test_make_and_parse_header_value():
    adr, keydata = "x@xy.z", "123"
    h = mime.make_ac_header_value(emailadr=adr, keydata=keydata)
    d = mime.parse_ac_headervalue(h)
    assert not mime.verify_ac_dict(d)
    assert d == make_ac_dict(to=adr, key=keydata)


def test_make_and_parse_header_errors():
    adr, keydata = "x@xy.z", "123"
    h = mime.make_ac_header_value(
        emailadr=adr, keydata=keydata, prefer_encrypt="notset", keytype="x")
    assert "prefer-encrypt" not in h, h
    d = mime.parse_ac_headervalue(h)
    assert "unknown key type" in mime.verify_ac_dict(d)[0]
    assert d == make_ac_dict(to=adr, key=keydata, type="x")


class TestEmailCorpus:
    def test_rsa2048_simple(self, datadir, bingpg):
        d = datadir.parse_ac_header_from_email("rsa2048-simple.eml")
        assert d["to"] == "alice@testsuite.autocrypt.org", d
        keyhandle = bingpg.import_keydata(b64decode(d["key"]))

    def test_25519_simple(self, datadir, bingpg):
        if (not bingpg.supports_eddsa()):
            pytest.xfail("No support for EDDSA")
        d = datadir.parse_ac_header_from_email("25519-simple.eml")
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert "key" in d and d["key"]
        bingpg.import_keydata(b64decode(d["key"]))

    def test_rsa2048_explicit_type(self, datadir, bingpg):
        d = datadir.parse_ac_header_from_email("rsa2048-explicit-type.eml")
        assert d["to"] == "alice@testsuite.autocrypt.org"
        bingpg.import_keydata(b64decode(d["key"]))

    def test_rsa2048_unknown_non_critical(self, datadir, bingpg):
        d = datadir.parse_ac_header_from_email("rsa2048-unknown-non-critical.eml")
        assert d["to"] == "alice@testsuite.autocrypt.org"
        assert d["_monkey"] == "ignore"
        bingpg.import_keydata(b64decode(d["key"]))

    def test_rsa2048_unknown_critical(self, datadir):
        d = datadir.parse_ac_header_from_email("rsa2048-unknown-critical.eml")
        l = mime.verify_ac_dict(d)
        assert len(l) == 1
        assert "unknown critical attr 'danger'" in l[0]

    def test_unknown_type(self, datadir):
        d = datadir.parse_ac_header_from_email("unknown-type.eml")
        l = mime.verify_ac_dict(d)
        assert len(l) == 1
        assert "unknown key type 'x'" in l[0]
