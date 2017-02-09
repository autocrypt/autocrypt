import os
import subprocess
import tempfile
import io


def cached_property(f):
    """returns a property definition which lazily computes and
    caches the result of calling f.  The property also allows
    setting the value (before or after read).
    """
    def get(self):
        propcache = self.__dict__.setdefault("_property_cache", {})
        try:
            return propcache[f]
        except KeyError:
            x = self._property_cache[f] = f(self)
            return x

    def set(self, val):
        propcache = self.__dict__.setdefault("_property_cache", {})
        propcache[f] = val
    return property(get, set)


class BinGPG(object):
    """ basic wrapper for gpg command line invocations. """
    def __init__(self, homedir):
        self.homedir = homedir

    def _gpg(self, argv):
        args = ["gpg", "--homedir", str(self.homedir)] + argv
        return subprocess.check_output(args)

    @cached_property
    def _version_info(self):
        return self._gpg(['--version']).decode()

    def get_version(self):
        vline = self._version_info.split('\n', 1)[0]
        return vline.split(' ')[2]

    def supports_eddsa(self):
        for l in self._version_info.split('\n'):
            if l.startswith('Pubkey:'):
                return 'eddsa' in map(
                    lambda x:x.strip().lower(), l.split(':', 1)[1].split(','))
        return False

    def import_keydata(self, keydata):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(keydata)
        self.import_keyfile(f.name)

    def import_keyfile(self, fn):
        assert os.path.exists(fn)
        self._gpg(["--import", fn])

