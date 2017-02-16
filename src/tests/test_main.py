from __future__ import print_function, unicode_literals
import os
import six
import pytest
from autocrypt.header import parse_one_ac_header_from_string


@pytest.fixture
def account_dir(tmpdir):
    return tmpdir.join("account").strpath

@pytest.fixture
def mycmd(cmd, tmpdir, testcache, request):
    # cache "autocrypt init" calls in cross-testrun test cache
    next_backup = testcache.next_backup(request)
    cmd.set_basedir(tmpdir.join("account").strpath, next_backup)
    return cmd


def test_help(cmd):
    res = cmd.run_ok([], """
        *init*
        *make-header*
        *export-public-key*
        *export-private-key*
    """)
    res = cmd.run_ok(["--help"], """
        *access and manage*
    """)


def test_init_help(cmd):
    cmd.run_ok(["init", "--help"], """
        *init*
    """)


def test_init(mycmd):
    mycmd.run_ok(["init"], """
            *account*created*
    """)
    mycmd.run_fail(["init"], """
            *account*exists*
    """)
    mycmd.run_ok(["init", "--replace"], """
            *deleting account dir*
            *account*created*
    """)

def test_init_and_make_header(mycmd):
    mycmd.run_fail(["make-header", "xyz"], """
        *Account*not initialized*
    """)
    adr = "x@yz.org"
    mycmd.run_ok(["init"])
    out = mycmd.run_ok(["make-header", adr])
    d = parse_one_ac_header_from_string(out)
    assert "prefer-encrypt" not in out
    assert "type" not in out
    assert d["to"] == adr
    out2 = mycmd.run_ok(["make-header", adr])
    assert out == out2

    mycmd.run_ok(["set-prefer-encrypt", "yes"])
    out3 = mycmd.run_ok(["make-header", adr])
    d3 = parse_one_ac_header_from_string(out3)
    assert d3["prefer-encrypt"] == "yes"


def test_exports_and_show(mycmd):
    mycmd.run_ok(["init"])
    out = mycmd.run_ok(["export-public-key"])
    check_ascii(out)
    out = mycmd.run_ok(["export-private-key"])
    check_ascii(out)
    out = mycmd.run_ok(["show"], """
        account-dir:*
        uuid:*
        own-keyhandle:*
        prefer-encrypt: notset
    """)


def check_ascii(out):
    if isinstance(out, six.text_type):
        out.encode("ascii")
    else:
        out.decode("ascii")


def test_init_and_show_header_with_envvar(cmd, tmpdir):
    with tmpdir.as_cwd():
        os.environ["AUTOCRYPT_BASEDIR"] = "."
        test_init_and_make_header(cmd)


def test_process_incoming_mail(mycmd, datadir):
    mycmd.run_ok(["init"])
    fn = datadir.join("rsa2048-simple.eml")
    mycmd.run_ok(["process-incoming-mail", fn], """
        *processed mail from alice@testsuite.autocrypt.org*key: D993BD7F*
    """)
    out1 = mycmd.run_ok(["export-public-key", "alice@testsuite.autocrypt.org"], """
        *---BEGIN PGP*
    """)
    out2 = mycmd.run_ok(["export-public-key", "D993BD7F"], """
        *---BEGIN PGP*
    """)
    assert out1 == out2

    mycmd.run_ok(["show"], """
        *---peers---*
        alice@testsuite.autocrypt.org*D993BD7F*1636 bytes*prefer-encrypt*
    """)
