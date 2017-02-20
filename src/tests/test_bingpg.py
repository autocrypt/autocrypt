# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab

from __future__ import unicode_literals

import os
import pytest
from autocrypt.bingpg import cached_property, BinGPG


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


def test_find_executable(tmpdir, gpgpath):
    bn = os.path.basename(gpgpath)
    b = BinGPG(tmpdir.strpath, gpgpath=bn)
    assert b.gpgpath == gpgpath
    if bn == "gpg":
        b = BinGPG(tmpdir.strpath)
        assert b.gpgpath == gpgpath


def test_find_executable_not_existing(tmpdir):
    with pytest.raises(ValueError):
        BinGPG(tmpdir.strpath, gpgpath="123")


class TestBinGPG:
    def test_failed_invocation_outerr(self, bingpg2):
        with pytest.raises(bingpg2.InvocationFailure):
            bingpg2._gpg_outerr(["qwe"])

    def test_gen_key_and_check_packets(self, bingpg):
        keyhandle = bingpg.gen_secret_key(emailadr="hello@xyz.org")
        return
        keydata = bingpg.get_secret_keydata(keyhandle)
        packets = bingpg.list_packets(keydata)
        # maybe the below a bit too strict?
        assert len(packets) == 5
        assert packets[0][0] == "secret key packet"
        assert packets[1][0] == "user ID packet"
        assert packets[1][1] == '" <hello@xyz.org>"'
        assert packets[2][0] == "signature packet"
        assert packets[3][0] == "secret sub key packet"
        assert packets[4][0] == "signature packet"

        keydata = bingpg.get_public_keydata(keyhandle)
        packets = bingpg.list_packets(keydata)
        assert len(packets) == 5
        assert packets[0][0] == "public key packet" == packets[0][0]
        assert packets[1][0] == "user ID packet"
        assert packets[1][1] == '" <hello@xyz.org>"'
        assert packets[2][0] == "signature packet"
        assert packets[3][0] == "public sub key packet"
        assert packets[4][0] == "signature packet"

    @pytest.mark.parametrize("armor", [True, False])
    def test_transfer_key_and_encrypt_decrypt_roundtrip(self, bingpg, bingpg2, armor):
        keyhandle = bingpg.gen_secret_key(emailadr="hello@xyz.org")
        priv_keydata = bingpg.get_secret_keydata(keyhandle=keyhandle, armor=armor)
        if armor:
            priv_keydata.decode("ascii")
        public_keydata = bingpg.get_public_keydata(keyhandle=keyhandle, armor=armor)
        if armor:
            public_keydata.decode("ascii")
        keyhandle2 = bingpg2.import_keydata(public_keydata)
        assert keyhandle2 == keyhandle
        out_encrypt = bingpg2.encrypt(b"123", recipients=[keyhandle])

        out, decrypt_info = bingpg.decrypt(out_encrypt)
        assert out == b"123"
        assert len(decrypt_info) == 1
        k = decrypt_info[0]
        assert str(k)
        assert k.bits == 2048
        assert k.type == "RSA"
        assert k.date_created
        # fish out encryption sub key and check if it matches
        for ptype, _, lines in bingpg2.list_public_key_packets(keyhandle):
            if "key packet" in ptype:
                for x in lines:
                    if x.startswith("keyid: "):
                        print(x[len("keyid: "):].strip())
                        if x[len("keyid: "):].strip()[-8:] == k.id:
                            return
        else:
            assert 0, k.id

    def test_gen_key_and_sign_verify(self, bingpg):
        keyhandle = bingpg.gen_secret_key(emailadr="hello@xyz.org")
        sig = bingpg.sign(b"123", keyhandle=keyhandle)
        keyhandle_verified = bingpg.verify(data=b'123', signature=sig)
        assert keyhandle == keyhandle_verified
