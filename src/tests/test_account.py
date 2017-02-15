from __future__ import unicode_literals
import pytest
from autocrypt.account import Account, KVStoreMixin, kv_persisted_property
from autocrypt import header


@pytest.fixture
def kvstore(tmpdir):
    return KVStoreMixin(tmpdir.join("kvstore").strpath)

@pytest.fixture
def account(tmpdir):
    return Account(tmpdir.join("account").strpath)

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
    assert d["key"] == account.bingpg.get_public_keydata(account.own_keyhandle)
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
    assert d["key"] == account.bingpg.get_public_keydata(account.own_keyhandle)
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
