from __future__ import unicode_literals
import pytest
import py
from autocrypt.account import KVStoreMixin, kv_property
from autocrypt import header
from email.mime.text import MIMEText
from email.utils import formatdate



def test_kvstore(tmpdir):
    class KV(KVStoreMixin):
        x = kv_property("x", int)
        y = kv_property("y", dict)

    kv = KV(tmpdir.join("kvstore").strpath)

    assert not kv.kv_exists()
    with pytest.raises(AttributeError):
        kv.z

    assert kv.x == 0
    assert kv.y == {}

    with pytest.raises(TypeError):
        kv.x = "123"

    kv.x = 13
    kv.y["1"] = 2
    kv.kv_commit()
    assert kv.kv_exists()

    assert kv.x == 13
    assert kv.y == {"1": 2}
    kv2 = KV(kv._path)
    assert kv2.kv_exists()
    assert kv2.x == 13
    assert kv2.y == {"1": 2}
    kv2.kv_commit()


def test_account_header_defaults(account):
    adr = "hello@xyz.org"
    with pytest.raises(account.NotInitialized):
        account.make_header(adr)
    account.init()
    h = account.make_header(adr)
    d = header.parse_one_ac_header_from_string(h)
    assert d["to"] == adr
    key = account.bingpg.get_public_keydata(account.config.own_keyhandle, b64=True)
    assert d["key"] == key
    assert d["prefer-encrypt"] == "notset"
    assert d["type"] == "p"


@pytest.mark.parametrize("pref", ["yes", "no", "notset"])
def test_account_header_prefer_encrypt(account, pref):
    adr = "hello@xyz.org"
    with pytest.raises(ValueError):
        account.set_prefer_encrypt("random")
    account.init()
    account.set_prefer_encrypt(pref)
    h = account.make_header(adr)
    d = header.parse_one_ac_header_from_string(h)
    assert d["to"] == adr
    key = account.bingpg.get_public_keydata(account.config.own_keyhandle, b64=True)
    assert d["key"] == key
    assert d["prefer-encrypt"] == pref
    assert d["type"] == "p"


def test_account_handling(Account, tmpdir):
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
    msg = gen_mail_msg(From="Alice <%s>" % adr, To=["b@b.org"],
                       Autocrypt=ac1.make_header(adr, headername=""))
    inc_adr = ac2.process_incoming(msg)
    assert inc_adr == adr
    keyhandle = ac2.get_latest_public_keyhandle(adr)
    enc = ac2.bingpg.encrypt(data=b"123", recipients=[keyhandle])
    data = ac1.bingpg.decrypt(enc)
    assert data == b"123"


def test_account_parse_incoming_mails_replace(account_maker):
    ac1 = account_maker()
    ac2 = account_maker()
    ac3 = account_maker()
    adr = "alice@a.org"
    msg1 = gen_mail_msg(From="Alice <%s>" % adr, To=["b@b.org"],
                        Autocrypt=ac2.make_header(adr, headername=""))
    adr = ac1.process_incoming(msg1)
    assert ac1.get_latest_public_keyhandle(adr) == ac2.config.own_keyhandle
    msg2 = gen_mail_msg(From="Alice <%s>" % adr, To=["b@b.org"],
                        Autocrypt=ac3.make_header(adr, headername=""))
    adr = ac1.process_incoming(msg2)
    assert ac1.get_latest_public_keyhandle(adr) == ac3.config.own_keyhandle


def test_account_parse_incoming_mails_replace_by_date(account_maker):
    ac1 = account_maker()
    ac2 = account_maker()
    ac3 = account_maker()
    adr = "alice@a.org"
    msg2 = gen_mail_msg(From="Alice <%s>" % adr, To=["b@b.org"],
                        Autocrypt=ac3.make_header(adr, headername=""),
                        Date='Thu, 16 Feb 2017 15:00:00 -0000')
    msg1 = gen_mail_msg(From="Alice <%s>" % adr, To=["b@b.org"],
                        Autocrypt=ac2.make_header(adr, headername=""),
                        Date='Thu, 16 Feb 2017 13:00:00 -0000')
    ac1.process_incoming(msg2)
    assert ac1.get_latest_public_keyhandle(adr) == ac3.config.own_keyhandle
    ac1.process_incoming(msg1)
    assert ac1.get_latest_public_keyhandle(adr) == ac3.config.own_keyhandle
    msg3 = gen_mail_msg(From="Alice <%s>" % adr, To=["b@b.org"],
                        Date='Thu, 16 Feb 2017 17:00:00 -0000')
    ac1.process_incoming(msg3)
    assert not ac1.get_latest_public_keyhandle(adr)



def test_account_export_public_key(account, datadir):
    account.init()
    msg = header.parse_message_from_file(datadir.open("rsa2048-simple.eml"))
    adr = account.process_incoming(msg)
    keyhandle = account.get_latest_public_keyhandle(adr)
    x = account.export_public_key(keyhandle)
    assert x


def gen_mail_msg(From, To, Autocrypt=None, Date=None):
    msg = MIMEText('''Autoresponse''')
    msg['From'] = From
    msg['To'] = ",".join(To)
    msg['Subject'] = "testmail"
    msg['Date'] = Date or formatdate()
    if Autocrypt:
        msg["Autocrypt"] = Autocrypt
    return msg
