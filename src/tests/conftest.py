
import pytest

@pytest.fixture
def bingpg(tmpdir, datadir):
    from autocrypt.bingpg import BinGPG
    p = tmpdir.mkdir("keyring")
    p.chmod(0o700)
    g = BinGPG(p.strpath)
    # import RSA 2048 key for "bot@autocrypt.org"
    g.import_keyfile(datadir.join("testbot.secretkey"))
    return g

@pytest.fixture()
def datadir(request):
    class D:
        def __init__(self, basepath):
            self.basepath = basepath
        def open(self, name):
            return self.basepath.join(name).open()
        def join(self, name):
            return self.basepath.join(name).strpath

    return D(request.fspath.dirpath("data"))

