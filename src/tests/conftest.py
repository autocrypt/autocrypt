import traceback
from click.testing import CliRunner
import pytest
import py
from _pytest.pytester import LineMatcher
from autocrypt.bingpg import BinGPG, find_executable
from autocrypt import header
from autocrypt.account import Account as OrigAccount


def pytest_addoption(parser):
    parser.addoption("--no-test-cache", action="store_true",
                     help="ignore test cache state")


@pytest.fixture(params=["gpg1", "gpg2"], scope="session")
def gpgpath(request):
    name = "gpg" if request.param == "gpg1" else "gpg2"
    path = find_executable(name)
    if path is None:
        pytest.skip("can not find executable: %s" % request.name)
    return path


def _makegpg(request, p, gpgpath, testcache):
    p.chmod(0o700)
    class MyBinGPG(BinGPG):
        def gen_secret_key(self, emailadr):
            next_backup = testcache.next_backup(request, gpgpath)
            if next_backup.exists():
                return next_backup.restore(p)
            else:
                ret = super(MyBinGPG, self).gen_secret_key(emailadr)
                if p.exists():
                    next_backup.store(p, ret)
                return ret

    bingpg = MyBinGPG(p.strpath, gpgpath=gpgpath)
    request.addfinalizer(bingpg.killagent)
    return bingpg


@pytest.fixture
def bingpg(request, tmpdir, gpgpath, testcache):
    p = tmpdir.mkdir("keyring")
    return _makegpg(request, p, gpgpath, testcache=testcache)


@pytest.fixture
def bingpg2(request, tmpdir, gpgpath, testcache):
    p = tmpdir.mkdir("keyring2")
    return _makegpg(request, p, gpgpath, testcache=testcache)


class ClickRunner:
    def __init__(self, main):
        self.runner = CliRunner()
        self._main = main
        self._rootargs = []

    def add_rootargs(self, options):
        self._rootargs = list(options) + self._rootargs

    def run_ok(self, args, fnmatch_lines=None):
        __tracebackhide__ = True
        argv = self._rootargs + args
        res = self.runner.invoke(self._main, argv, catch_exceptions=False)
        if res.exit_code != 0:
            print(res.output)
            raise Exception("cmd exited with %d: %s" %(res.exit_code, argv))
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
    from autocrypt.main import autocrypt_main
    return ClickRunner(autocrypt_main)


@pytest.fixture()
def datadir(request):
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
        def parse_ac_header_from_email(self, name):
            with self.open(name) as fp:
                msg = header.parse_message_from_file(fp)
                return header.parse_one_ac_header_from_msg(msg)
    return D(request.fspath.dirpath("data"))


@pytest.fixture(scope="session")
def testcache():
    counters = {}
    class TestCache:
        def next_backup(self, func_request, extra=""):
            count_key = func_request.node.nodeid + extra
            count = counters.setdefault(count_key, 0)
            key = count_key + str(count)
            try:
                return NextBackup(func_request, key)
            finally:
                counters[count_key] += 1
    return TestCache()


class NextBackup:
    def __init__(self, func_request, key):
        self.cache = func_request.config.cache
        self.disabled = func_request.config.getoption("--no-test-cache")
        self.key = key
        self.backup_path = self.cache._cachedir.join(self.key)

    def exists(self):
        dummy = object()
        return not self.disabled and \
               self.cache.get(self.key, dummy) != dummy and \
               self.backup_path.exists()

    def store(self, path, ret):
        self.backup_path.dirpath().ensure(dir=1)
        py.path.local(path).copy(self.backup_path) #, mode=True)
        self.cache.set(self.key, ret)

    def restore(self, path):
        self.backup_path.copy(py.path.local(path)) # , mode=True)
        return self.cache.get(self.key, None)


@pytest.fixture
def Account(request, testcache):
    class MyAccount(OrigAccount):
        def init(self):
            next_backup = testcache.next_backup(request)
            if next_backup.exists():
                ret = next_backup.restore(self.dir)
                self.kv_reload()
            else:
                ret = super(MyAccount, self).init()
                next_backup.store(self.dir, ret)
            return ret
    return MyAccount


@pytest.fixture
def account(tmpdir, Account):
    return Account(tmpdir.join("account").strpath)
