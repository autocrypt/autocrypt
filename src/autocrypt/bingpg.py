from __future__ import print_function, unicode_literals
import os
import sys
from subprocess import Popen, PIPE, CalledProcessError
import tempfile
import io
import re


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

    def _gpg_out(self, argv, input=None):
        return self._gpg_outerr(argv, input=input)[0]

    def _gpg_outerr(self, argv, input=None):
        args = ["gpg", "--homedir", str(self.homedir)] + argv
        popen = Popen(args, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        out, err = popen.communicate(input=input)
        ret = popen.wait()
        if ret != 0:
            raise CalledProcessError(ret, " ".join(args), out + err)
        return out, err

    @cached_property
    def _version_info(self):
        return self._gpg_out(['--version']).decode()

    def get_version(self):
        vline = self._version_info.split('\n', 1)[0]
        return vline.split(' ')[2]

    def supports_eddsa(self):
        for l in self._version_info.split('\n'):
            if l.startswith('Pubkey:'):
                return 'eddsa' in map(
                    lambda x:x.strip().lower(), l.split(':', 1)[1].split(','))
        return False

    def gen_secret_key(self, emailadr):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write("\n".join([
                "Key-Type: RSA",
                "Key-Length: 2048",
                "Key-Usage: sign",
                "Subkey-Type: RSA",
                "Subkey-Length: 2048",
                "Subkey-Usage: encrypt",
                #"Name-Real: " + uid,
                "Name-Email: " + emailadr,
                "Expire-Date: 0",
                "%commit"
            ]).encode("utf8"))
        try:
            out, err = self._gpg_outerr(["--batch", "--gen-key", f.name])
        finally:
            os.remove(f.name)
        # quickly find key id or fingerprint
        m = re.search(b"([0-9A-F]+)", err)
        assert m, err
        assert len(m.groups()) == 1
        return m.groups()[0]

    def list_secret_key_packets(self, keyid):
        sk = self._gpg_out(["--export-secret-key", keyid])
        return self._list_packets(keyid)

    def list_public_key_packets(self, keyid):
        sk = self._gpg_out(["--export", keyid])
        return self._list_packets(sk)

    def list_packets(self, keydata):
        out = self._gpg_out(["--list-packets"], input=keydata)
        # build up a list of (pkgname, pkgvalue, lines) tuples
        packets = []
        lines = []
        last_package_type = None
        pattern = re.compile(b":([^:]+):(.*)")
        for line in out.splitlines():
            m = pattern.search(line)
            if m:
                ptype, pvalue = m.groups()
                pvalue = pvalue.strip()
                if last_package_type is not None:
                    packets.append(last_package_type + (lines,))
                    lines = []
                last_package_type = (ptype, pvalue)
            else:
                assert last_package_type, line
                lines.append(line)
        else:
            packets.append(last_package_type + (lines,))
        return packets

    def get_public_keydata(self, keyid):
        return self._gpg_out(["--export", keyid])

    def get_secret_keydata(self, keyid):
        return self._gpg_out(["--export-secret-key", keyid])

    def encrypt(self, data, recipients):
        recs = []
        for r in recipients:
            recs.extend(["--recipient", r])
        return self._gpg_out(recs + ["--encrypt", "--always-trust"], input=data)

    def decrypt(self, enc_data):
        return self._gpg_out(["--decrypt"], input=enc_data)

    def import_keydata(self, keydata):
        self._gpg_out(["--import"], input=keydata)
