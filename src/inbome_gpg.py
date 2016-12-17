import os
import subprocess
import tempfile

class GPG:
    """ super basic wrapper for gpg command line invocations. """
    def __init__(self, homedir):
        self.homedir = homedir

    def _gpg(self, argv):
        args = ["gpg", "--homedir", str(self.homedir)] + argv
        subprocess.check_call(args)

    def import_keydata(self, keydata):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(keydata)
        assert os.path.exists(f.name)
        self._gpg(["--import", f.name])
        os.remove(f.name)
