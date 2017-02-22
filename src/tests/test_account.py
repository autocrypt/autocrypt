# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab

from __future__ import unicode_literals
import os
import pytest
from autocrypt.account import Config, Account
from autocrypt import mime


def test_config(tmpdir):
    config = Config(tmpdir.join("config").strpath)

    with pytest.raises(AttributeError):
        config.qwe

    assert config.uuid == ""
    assert config.own_keyhandle == ""
    assert config.peers == {}

    assert not config.exists()
    with config.atomic_change():
        config.uuid = "123"
        assert config.exists()
        assert config.uuid == "123"
    assert config.uuid == "123"

    try:
        with config.atomic_change():
            config.uuid = "456"
            raise ValueError()
    except ValueError:
        assert config.uuid == "123"
    else:
        assert 0


def test_account_header_defaults(account):
    adr = "hello@xyz.org"
    with pytest.raises(account.NotInitialized):
        account.make_header(adr)
    account.init()
    assert account.config.gpgmode == "own"
    h = account.make_header(adr)
    d = mime.parse_one_ac_header_from_string(h)
    assert d["to"] == adr
    key = account.bingpg.get_public_keydata(account.config.own_keyhandle, b64=True)
    assert d["key"] == key
    assert d["prefer-encrypt"] == "notset"
    assert d["type"] == "p"


def test_account_init_with_existing(account_maker, datadir, gpgpath, monkeypatch):
    acc1 = account_maker()
    monkeypatch.setenv("GNUPGHOME", acc1.bingpg.homedir)
    acc2 = account_maker(init=False)
    gpgbin = os.path.basename(gpgpath)
    acc2.init_with_existing(gpgbin=gpgbin, keyhandle=acc1.config.own_keyhandle)
    assert acc2.config.own_keyhandle == acc1.config.own_keyhandle
    assert acc2.config.gpgmode == "system"
    assert acc2.config.gpgbin == gpgbin


@pytest.mark.parametrize("pref", ["yes", "no", "notset"])
def test_account_header_prefer_encrypt(account, pref):
    adr = "hello@xyz.org"
    account.init()
    with pytest.raises(ValueError):
        account.set_prefer_encrypt("random")
    account.set_prefer_encrypt(pref)
    h = account.make_header(adr)
    d = mime.parse_one_ac_header_from_string(h)
    assert d["to"] == adr
    key = account.bingpg.get_public_keydata(account.config.own_keyhandle, b64=True)
    assert d["key"] == key
    assert d["prefer-encrypt"] == pref
    assert d["type"] == "p"


def test_account_handling(tmpdir):
    tmpdir = tmpdir.strpath
    acc = Account(tmpdir)
    assert not acc.exists()
    acc.init()
    assert acc.exists()
    acc.remove()
    assert not acc.exists()


def test_account_parse_incoming_mail_and_raw_encrypt(account_maker):
    adr = "a@a.org"
    ac1 = account_maker()
    ac2 = account_maker()
    msg = mime.gen_mail_msg(
        From="Alice <%s>" % adr, To=["b@b.org"],
        Autocrypt=ac1.make_header(adr, headername=""))
    inc_adr = ac2.process_incoming(msg)
    assert inc_adr == adr
    keyhandle = ac2.get_latest_public_keyhandle(adr)
    enc = ac2.bingpg.encrypt(data=b"123", recipients=[keyhandle])
    data, descr_info = ac1.bingpg.decrypt(enc)
    assert data == b"123"


def test_account_parse_incoming_mails_replace(account_maker):
    ac1 = account_maker()
    ac2 = account_maker()
    ac3 = account_maker()
    adr = "alice@a.org"
    msg1 = mime.gen_mail_msg(
        From="Alice <%s>" % adr, To=["b@b.org"],
        Autocrypt=ac2.make_header(adr, headername=""))
    adr = ac1.process_incoming(msg1)
    assert ac1.get_latest_public_keyhandle(adr) == ac2.config.own_keyhandle
    msg2 = mime.gen_mail_msg(
        From="Alice <%s>" % adr, To=["b@b.org"],
        Autocrypt=ac3.make_header(adr, headername=""))
    adr = ac1.process_incoming(msg2)
    assert ac1.get_latest_public_keyhandle(adr) == ac3.config.own_keyhandle


def test_account_parse_incoming_mails_replace_by_date(account_maker):
    ac1 = account_maker()
    ac2 = account_maker()
    ac3 = account_maker()
    adr = "alice@a.org"
    msg2 = mime.gen_mail_msg(
        From="Alice <%s>" % adr, To=["b@b.org"],
        Autocrypt=ac3.make_header(adr, headername=""),
        Date='Thu, 16 Feb 2017 15:00:00 -0000')
    msg1 = mime.gen_mail_msg(
        From="Alice <%s>" % adr, To=["b@b.org"],
        Autocrypt=ac2.make_header(adr, headername=""),
        Date='Thu, 16 Feb 2017 13:00:00 -0000')
    ac1.process_incoming(msg2)
    assert ac1.get_latest_public_keyhandle(adr) == ac3.config.own_keyhandle
    ac1.process_incoming(msg1)
    assert ac1.get_latest_public_keyhandle(adr) == ac3.config.own_keyhandle
    msg3 = mime.gen_mail_msg(
        From="Alice <%s>" % adr, To=["b@b.org"],
        Date='Thu, 16 Feb 2017 17:00:00 -0000')
    ac1.process_incoming(msg3)
    assert not ac1.get_latest_public_keyhandle(adr)


def test_account_export_public_key(account, datadir):
    account.init()
    msg = mime.parse_message_from_file(datadir.open("rsa2048-simple.eml"))
    adr = account.process_incoming(msg)
    keyhandle = account.get_latest_public_keyhandle(adr)
    x = account.export_public_key(keyhandle)
    assert x
