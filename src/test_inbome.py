import pytest

from inbome import parse_inbome_header


@pytest.fixture
def gpg(tmpdir, datadir):
    from inbome_gpg import GPG
    p = tmpdir.mkdir("keyring")
    p.chmod(0o700)
    g = GPG(p.strpath)
    # import RSA 2048 key for "bot@autocrypt.org"
    g.import_keyfile(datadir.join("testbot.secretkey").strpath)
    return g

@pytest.fixture()
def datadir(request):
    class D:
        def __init__(self, basepath):
            self.basepath = basepath
        def open(self, name):
            return self.basepath.join(name).open()
        def join(self, name):
            return self.basepath.join(name)

    return D(request.fspath.dirpath("data"))


def test_example1(datadir, gpg):
    with datadir.open("example1.mail") as fp:
        d = parse_inbome_header(fp)
        assert d["to"] == "dkg@fifthhorseman.net"
        assert "key" in d and d["key"]

    gpg.import_keydata(d["key"])


