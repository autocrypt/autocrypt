
import pytest
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
