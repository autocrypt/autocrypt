
import pytest
from autocrypt.bingpg import BinGPG

@pytest.fixture
def bingpg(tmpdir, datadir):
    p = tmpdir.mkdir("keyring")
    g = _makegpg(p)
    # import RSA 2048 key for "bot@autocrypt.org"
    keydata = datadir.read_bytes("testbot.secretkey")
    g.import_keydata(keydata)
    return g

def _makegpg(p):
    p.chmod(0o700)
    return BinGPG(p.strpath)

@pytest.fixture
def bingpg2(tmpdir):
    p = tmpdir.mkdir("keyring2")
    return _makegpg(p)

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
