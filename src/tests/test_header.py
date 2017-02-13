from __future__ import unicode_literals
from autocrypt.header import make_header, parse_autocrypt_headervalue

def test_genkey_make_and_parse_header(bingpg2):
    keyid = bingpg2.gen_secret_key(emailadr="hello@xyz.org")
    keydata = bingpg2.get_public_keydata(keyid)
    h = make_header(emailadr="hello@xyz.org", keydata=keydata)
    assert h.startswith("Autocrypt: ")
    value = h[10:]
    d = parse_autocrypt_headervalue(value)
    assert d["key"] == keydata
    assert d["to"] == "hello@xyz.org"
