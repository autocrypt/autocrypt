from __future__ import unicode_literals
import pytest
import py
from autocrypt.account import KVStoreMixin, kv_persisted_property
from autocrypt import header
from email.mime.text import MIMEText
from email.utils import formatdate


@pytest.fixture
def kvstore(tmpdir):
    return KVStoreMixin(tmpdir.join("kvstore").strpath)



def test_kvstore(kvstore):
    kvstore._kv_dict["hello"] = 3
    kvstore.kv_commit()
    assert kvstore._kv_dict["hello"] == 3
    kv2 = KVStoreMixin(kvstore._kv_path)
    assert kvstore._kv_dict["hello"] == 3
    del kv2._kv_dict["hello"]
    kv2.kv_commit()
    kvstore.kv_reload()
    assert "hello" not in kvstore._kv_dict


def test_persisted_property(tmpdir):
    class A(KVStoreMixin):
        hello = kv_persisted_property("hello", int)

    a = A(tmpdir.join("kvstore").strpath)
    a.hello = 42
    assert a.hello == 42
    a.kv_commit()
    a = A(tmpdir.join("kvstore").strpath)
    assert a.hello == 42


def test_account_header_defaults(account):
    adr = "hello@xyz.org"
    with pytest.raises(account.NotInitialized):
        account.make_header(adr)
    account.init()
    h = account.make_header(adr)
    d = header.parse_one_ac_header_from_string(h)
    assert d["to"] == adr
    assert d["key"] == account.bingpg.get_public_keydata(account.own_keyhandle, b64=True)
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
    assert d["key"] == account.bingpg.get_public_keydata(account.own_keyhandle, b64=True)
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
    inc_adr = ac2.process_incoming_mail(msg)
    assert inc_adr == adr
    keyid = ac2.get_latest_public_keyid(adr)
    enc = ac2.bingpg.encrypt(data=b"123", recipients=[keyid])
    data = ac1.bingpg.decrypt(enc)
    assert data == b"123"


def test_account_parse_incoming_mails_replace(account_maker):
    ac1 = account_maker()
    ac2 = account_maker()
    ac3 = account_maker()
    adr = "alice@a.org"
    msg1 = gen_mail_msg(From="Alice <%s>" % adr, To=["b@b.org"],
                        Autocrypt=ac2.make_header(adr, headername=""))
    adr = ac1.process_incoming_mail(msg1)
    assert ac1.get_latest_public_keyid(adr) == ac2.own_keyhandle
    msg2 = gen_mail_msg(From="Alice <%s>" % adr, To=["b@b.org"],
                        Autocrypt=ac3.make_header(adr, headername=""))
    adr = ac1.process_incoming_mail(msg2)
    assert ac1.get_latest_public_keyid(adr) == ac3.own_keyhandle


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
    ac1.process_incoming_mail(msg2)
    assert ac1.get_latest_public_keyid(adr) == ac3.own_keyhandle
    ac1.process_incoming_mail(msg1)
    assert ac1.get_latest_public_keyid(adr) == ac3.own_keyhandle
    msg3 = gen_mail_msg(From="Alice <%s>" % adr, To=["b@b.org"],
                        Date='Thu, 16 Feb 2017 17:00:00 -0000')
    ac1.process_incoming_mail(msg3)
    assert not ac1.get_latest_public_keyid(adr)



def test_account_export_public_key(account, datadir):
    account.init()
    msg = header.parse_message_from_file(datadir.open("rsa2048-simple.eml"))
    adr = account.process_incoming_mail(msg)
    keyid = account.get_latest_public_keyid(adr)
    x = account.export_public_key(keyid)
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
