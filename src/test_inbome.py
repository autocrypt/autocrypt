import pytest

from inbome import parse_inbome_header

@pytest.fixture()
def examples(request):
    class ex:
        def __init__(self, basepath):
            self.basepath = basepath
        def open(self, name):
            return self.basepath.join(name).open()

    return ex(request.fspath.dirpath("data"))


def test_example1(examples):
    with examples.open("example1.mail") as fp:
        d = parse_inbome_header(fp)
        assert d["to"] == "dkg@fifthhorseman.net"
        assert "key" in d and d["key"]

