# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab

from click.testing import CliRunner
import logging
import os
import itertools
import pytest
import py
from _pytest.pytester import LineMatcher
from autocrypt.bingpg import find_executable, BinGPG
from autocrypt import mime
from autocrypt.account import Account


def pytest_addoption(parser):
    parser.addoption("--no-test-cache", action="store_true",
                     help="ignore test cache state")

    parser.addoption("--with-gpg2", action="store_true",
                     help="run tests also with gpg2")


@pytest.fixture(params=["gpg1", "gpg2"], scope="module")
def gpgpath(request):
    """ return twice with system paths of "gpg" and "gpg2"
    respectively.  If one is not present the test requesting
    this fixture is skipped. By default we do not run gpg2
    tests because they are much slower.  A clean "tox" run
    will also run the gpg2 tests.
    """
    name = "gpg" if request.param == "gpg1" else "gpg2"
    if name == "gpg2" and not request.config.getoption("--with-gpg2"):
        pytest.skip("skip gpg2 tests unless you specify --slow")
    path = find_executable(name)
    if path is None:
        pytest.skip("can not find executable: %s" % request.name)
    return path


@pytest.fixture(autouse=True)
def _testcache_bingpg_(request, get_next_cache, monkeypatch):
    # cache generation of secret keys
    old_gen_secret_key = BinGPG.gen_secret_key

    def gen_secret_key(self, emailadr):
        basekey = request.node.nodeid
        next_cache = get_next_cache(basekey)
        if self.homedir and next_cache.exists():
            logging.debug("restoring homedir {}".format(self.homedir))
            return next_cache.restore(self.homedir)
        else:
            if self.homedir is None:
                assert "GNUPGHOME" in os.environ
            ret = old_gen_secret_key(self, emailadr)
            if self.homedir is not None:
                if os.path.exists(self.homedir):
                    next_cache.store(self.homedir, ret)
            return ret

    monkeypatch.setattr(BinGPG, "gen_secret_key", gen_secret_key)

    # make sure any possibly started agents are killed
    old_init = BinGPG.__init__

    def __init__(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        request.addfinalizer(self.killagent)

    monkeypatch.setattr(BinGPG, "__init__", __init__)
    return


@pytest.fixture
def bingpg_maker(request, tmpdir, gpgpath):
    """ return a function which creates initialized BinGPG instances. """
    counter = itertools.count()

    def maker(native=False):
        if native:
            bingpg = BinGPG(gpgpath=gpgpath)
        else:
            p = tmpdir.mkdir("bingpg%d" % next(counter))
            bingpg = BinGPG(p.strpath, gpgpath=gpgpath)
            bingpg.init()
        return bingpg
    return maker


@pytest.fixture
def bingpg(bingpg_maker):
    """ return an initialized bingpg instance. """
    return bingpg_maker()


@pytest.fixture
def bingpg2(bingpg_maker):
    """ return an initialized bingpg instance different from the first. """
    return bingpg_maker()


class ClickRunner:
    def __init__(self, main):
        self.runner = CliRunner()
        self._main = main
        self._rootargs = []

    def set_basedir(self, account_dir):
        self._rootargs.insert(0, "--basedir")
        self._rootargs.insert(1, account_dir)

    def run_ok(self, args, fnmatch_lines=None):
        __tracebackhide__ = True
        argv = self._rootargs + args
        # we use our nextbackup helper to cache account creation
        # unless --no-test-cache is specified
        res = self.runner.invoke(self._main, argv, catch_exceptions=False)
        if res.exit_code != 0:
            print(res.output)
            raise Exception("cmd exited with %d: %s" % (res.exit_code, argv))
        return self._perform_match(res, fnmatch_lines)

    def run_fail(self, args, fnmatch_lines=None):
        __tracebackhide__ = True
        argv = self._rootargs + args
        res = self.runner.invoke(self._main, argv, catch_exceptions=False)
        if res.exit_code == 0:
            print (res.output)
            raise Exception("command did not fail: %s" % argv)
        return self._perform_match(res, fnmatch_lines)

    def _perform_match(self, res, fnmatch_lines):
        __tracebackhide__ = True
        if fnmatch_lines:
            lm = LineMatcher(res.output.splitlines())
            lines = [x.strip() for x in fnmatch_lines.strip().splitlines()]
            try:
                lm.fnmatch_lines(lines)
            except:
                print(res.output)
                raise
        return res.output


@pytest.fixture
def cmd():
    """ invoke a command line subcommand. """
    from autocrypt.main import autocrypt_main
    return ClickRunner(autocrypt_main)


@pytest.fixture()
def datadir(request):
    """ get, read, open test files from the "data" directory. """
    class D:
        def __init__(self, basepath):
            self.basepath = basepath

        def open(self, name, mode="r"):
            return self.basepath.join(name).open(mode)

        def join(self, name):
            return self.basepath.join(name).strpath

        def read_bytes(self, name):
            with self.open(name, "rb") as f:
                return f.read()

        def read(self, name):
            with self.open(name, "r") as f:
                return f.read()

        def parse_ac_header_from_email(self, name):
            with self.open(name) as fp:
                msg = mime.parse_message_from_file(fp)
                return mime.parse_one_ac_header_from_msg(msg)

    return D(request.fspath.dirpath("data"))


@pytest.fixture(scope="session")
def get_next_cache(pytestconfig):
    cache = pytestconfig.cache
    counters = {}

    def next_cache(basekey):
        count = counters.setdefault(basekey, itertools.count())
        key = basekey + str(next(count))
        return DirCache(cache, key)
    return next_cache


class DirCache:
    def __init__(self, cache, key):
        self.cache = cache
        self.disabled = cache.config.getoption("--no-test-cache")
        self.key = key
        self.backup_path = self.cache._cachedir.join(self.key)

    def exists(self):
        dummy = object()
        return not self.disabled and \
               self.cache.get(self.key, dummy) != dummy and \
               self.backup_path.exists()

    def store(self, path, ret):
        self.backup_path.dirpath().ensure(dir=1)
        py.path.local(path).copy(self.backup_path)
        self.cache.set(self.key, ret)

    def restore(self, path):
        self.backup_path.copy(py.path.local(path))
        return self.cache.get(self.key, None)


@pytest.fixture
def account(account_maker):
    """ return an uninitialized Autocrypt account. """
    return account_maker(init=False)


@pytest.fixture
def account_maker(tmpdir, gpgpath):
    """ return a function which creates a new Autocrypt account, by default initialized.
    pass init=False to the function to avoid initizialtion.
    """
    count = itertools.count()

    def maker(init=True):
        basedir = tmpdir.mkdir("account%d" % next(count)).strpath
        ac = Account(basedir)
        if init:
            ac.init(gpgbin=gpgpath)
        return ac
    return maker
