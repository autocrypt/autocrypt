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

    def test_gen_key_and_list_secret_packets(self, bingpg, bingpg2):
        keyid = bingpg.gen_secret_key(emailadr="hello@xyz.org")
        keydata = bingpg.get_secret_keydata(keyid)
        packets = bingpg.list_packets(keydata)
        # maybe the below a bit too strict?
        assert len(packets) == 5
        assert packets[0][0] == b"secret key packet"
        assert packets[1][0] == b"user ID packet"
        assert packets[1][1] == b'" <hello@xyz.org>"'
        assert packets[2][0] == b"signature packet"
        assert packets[3][0] == b"secret sub key packet"
        assert packets[4][0] == b"signature packet"

    def test_gen_key_and_list_public_packets(self, bingpg, bingpg2):
        keyid = bingpg.gen_secret_key(emailadr="hello@xyz.org")
        keydata = bingpg.get_public_keydata(keyid)
        packets = bingpg.list_packets(keydata)
        assert len(packets) == 5
        assert packets[0][0] == b"public key packet" == packets[0][0]
        assert packets[1][0] == b"user ID packet"
        assert packets[1][1] == b'" <hello@xyz.org>"'
        assert packets[2][0] == b"signature packet"
        assert packets[3][0] == b"public sub key packet"
        assert packets[4][0] == b"signature packet"

    def test_transfer_key_and_encrypt_decrypt_roundtrip(self, bingpg, bingpg2):
        keyid = bingpg.gen_secret_key(emailadr="hello@xyz.org")
        pub_keydata = bingpg.get_public_keydata(keyid=keyid)
        bingpg2.import_keydata(pub_keydata)
        out_encrypt = bingpg2.encrypt(b"123", recipients=[keyid])
        out = bingpg.decrypt(out_encrypt)
        assert out == b"123"


