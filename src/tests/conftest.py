import traceback
from click.testing import CliRunner
import pytest
from _pytest.pytester import LineMatcher
from autocrypt.bingpg import BinGPG, find_executable


@pytest.fixture(params=["gpg", "gpg2"], scope="session")
def gpgpath(request):
    path = find_executable(request.param)
    if path is None:
        pytest.skip("can not find executable: %s" % request.name)
    return path


def _makegpg(request, p, gpgpath):
    p.chmod(0o700)
    bingpg = BinGPG(p.strpath, gpgpath=gpgpath)
    request.addfinalizer(bingpg.killagent)
    return bingpg


@pytest.fixture
def bingpg(request, tmpdir, gpgpath):
    p = tmpdir.mkdir("keyring")
    return _makegpg(request, p, gpgpath)


@pytest.fixture
def bingpg2(request, tmpdir, gpgpath):
    p = tmpdir.mkdir("keyring2")
    return _makegpg(request, p, gpgpath)


class ClickRunner:
    def __init__(self, main):
        self.runner = CliRunner()
        self._main = main
        self._rootargs = []

    def add_rootargs(self, options):
        self._rootargs = list(options) + self._rootargs

    def run_ok(self, args, fnmatch_lines=None):
        argv = self._rootargs + args
        res = self.runner.invoke(self._main, argv)
        if res.exit_code != 0:
            #print (res.output)
            #if not isinstance(res.exception, SystemExit):
            #    traceback.print_exception(*res.exc_info)
            raise Exception("cmd exited with %d: %s" %(res.exit_code, argv))

        return self._perform_match(res, fnmatch_lines)

    def run_fail(self, args, fnmatch_lines=None):
        argv = self._rootargs + args
        res = self.runner.invoke(self._main, argv, catch_exceptions=False)
        if res.exit_code == 0:
            print (res.output)
            raise Exception("command did not fail: %s" % argv)
        return self._perform_match(res, fnmatch_lines)

    def _perform_match(self, res, fnmatch_lines):
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

    return D(request.fspath.dirpath("data"))
