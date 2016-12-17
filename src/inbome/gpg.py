import os
import subprocess
import tempfile
import io

class GPG:
    """ super basic wrapper for gpg command line invocations. """
    def __init__(self, homedir):
        self.homedir = homedir
        self.version_info = None

    def _gpg(self, argv):
        args = ["gpg", "--homedir", str(self.homedir)] + argv
        return subprocess.check_output(args)

    def _get_version_info(self):
        if self.version_info is None:
            self.version_info = self._gpg(['--version']).decode()
        return self.version_info

    def get_version(self):
        vline = self._get_version_info().split('\n', 1)[0]
        return vline.split(' ')[2]

    def supports_eddsa(self):
        for l in self._get_version_info().split('\n'):
            if l.startswith('Pubkey:'):
                return 'eddsa' in map(lambda x:x.strip().lower(), l.split(':', 1)[1].split(','))
        return False

    def import_keydata(self, keydata):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(keydata)
        self.import_keyfile(f.name)

    def import_keyfile(self, fn):
        assert os.path.exists(fn)
        self._gpg(["--import", fn])
