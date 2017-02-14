from __future__ import print_function, unicode_literals
import os
import pytest
from autocrypt.header import parse_autocrypt_header_from_string


@pytest.fixture
def account_dir(tmpdir):
    return tmpdir.join("account").strpath

@pytest.fixture
def mycmd(cmd, tmpdir):
    cmd.add_rootargs(["--basedir", tmpdir.join("account").strpath])
    return cmd


def test_help(cmd):
    res = cmd.run_ok(["--help"], fnmatch_lines="""
        *access Autocrypt*
    """)


def test_gen_account_help(cmd):
    cmd.run_ok(["init", "--help"], fnmatch_lines="""
        *generate autocrypt account*
    """)


def test_gen_account(mycmd):
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

def test_gen_account_and_show_header(mycmd):
    mycmd.run_fail(["make-header", "xyz"], """
        *Account*not initialized*
    """)
    mycmd.run_ok(["init"])
    out = mycmd.run_ok(["make-header", "this@xyz.org"])
    d = parse_autocrypt_header_from_string(out)
    assert d["to"] == "this@xyz.org"
    out2 = mycmd.run_ok(["make-header", "this@xyz.org"])
    assert out == out2


def test_gen_account_and_show_header_with_envvar(cmd, tmpdir):
    with tmpdir.as_cwd():
        os.environ["AUTOCRYPT_BASEDIR"] = "."
        test_gen_account_and_show_header(cmd)
