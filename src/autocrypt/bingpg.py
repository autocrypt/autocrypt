from __future__ import print_function, unicode_literals
import logging
import os
import sys
from subprocess import Popen, PIPE
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


class InvocationFailure(Exception):
    def __init__(self, ret, cmd, out, err):
        self.ret = ret
        self.cmd = cmd
        self.out = out
        self.err = err

    def __str__(self):
        lines = ["GPG Command '%s' retcode=%d" % (self.cmd, self.ret)]
        for name, olines in [("stdout:", self.out), ("stderr:", self.err)]:
            lines.append(name)
            for line in olines.splitlines():
                lines.append("  " + line)
        return "\n".join(lines)


class BinGPG(object):
    """ basic wrapper for gpg command line invocations. """
    InvocationFailure = InvocationFailure

    def __init__(self, homedir):
        self.homedir = homedir

    def _gpg_out(self, argv, input=None, strict=False):
        return self._gpg_outerr(argv, input=input, strict=strict)[0]

    def _gpg_outerr(self, argv, input=None, strict=False):
        args = ["gpg", "--homedir", str(self.homedir)]
        # make sure we use unicode for all provided arguments
        for arg in argv:
            if isinstance(arg, bytes):
                arg = arg.decode("utf8")
            args.append(arg)

        # open the process, pipe everything
        popen = Popen(args, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        logging.debug("exec: %s", " ".join(args))
        out, err = popen.communicate(input=input)
        ret = popen.wait()
        if ret != 0 or (strict and err):
            raise self.InvocationFailure(ret, " ".join(args),
                                         out=str(out), err=str(err))
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
        m = re.search(b"key ([0-9A-F]+)", err)
        assert m, err
        assert len(m.groups()) == 1
        keyid = m.groups()[0]
        logging.debug("created secret key: %s", keyid)
        return keyid

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
        return self._gpg_out(["--export", keyid], strict=True)

    def get_secret_keydata(self, keyid):
        return self._gpg_out(["--export-secret-key", keyid], strict=True)

    def encrypt(self, data, recipients):
        recs = []
        for r in recipients:
            recs.extend(["--recipient", r])
        return self._gpg_out(recs + ["--encrypt", "--always-trust"], input=data)

    def decrypt(self, enc_data):
        return self._gpg_out(["--decrypt"], input=enc_data)

    def import_keydata(self, keydata):
        self._gpg_out(["--import"], input=keydata)
