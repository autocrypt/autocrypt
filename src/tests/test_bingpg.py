from __future__ import unicode_literals

import pytest
from autocrypt.bingpg import cached_property, BinGPG, CalledProcessError

def test_cached_property_object():
    l = []
    class A(object):
        @cached_property
        def x1(self):
            l.append('x')
            return 1

    a = A()
    assert len(l) == 0
    assert a.x1 == 1
    assert l == ['x']
    assert a.x1 == 1
    assert l == ['x']
    a.x1 = 10
    assert a.x1 == 10
    assert l == ['x']


class TestBinGPG:
    def test_failed_invocation_outerr(self, bingpg2):
        with pytest.raises(CalledProcessError) as e:
            bingpg2._gpg_outerr(["qwe"])

    def test_key_roundtrip(self, bingpg, bingpg2):
        keyid = bingpg.gen_secret_key(emailadr="hello@xyz.org")
        pub_keydata = bingpg.export_public_keydata(keyid=keyid)
        bingpg2.import_keydata(pub_keydata)
        out_encrypt = bingpg2.encrypt(b"123", recipients=[keyid])
        out = bingpg.decrypt(out_encrypt)
        assert out == b"123"


