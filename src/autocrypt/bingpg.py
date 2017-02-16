from __future__ import print_function, unicode_literals
import logging
import os
import sys
import six
from subprocess import Popen, PIPE
from contextlib import contextmanager
from base64 import b64encode
import tempfile
import io
import re
iswin32 = sys.platform == "win32" or (getattr(os, '_name', False) == 'nt')

def b64encode_u(x):
    res = b64encode(x)
    if isinstance(res, bytes):
        res = res.decode("ascii")
    return res


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

    def __init__(self, homedir, gpgpath=None):
        self.homedir = str(homedir)
        # for gpg2>2.1 and <2.1.12 we need to explicitely allow loopback pinentry
        if not os.path.exists(self.homedir):
            os.makedirs(self.homedir)
        with open(os.path.join(self.homedir, "gpg-agent.conf"), "w") as f:
            f.write("allow-loopback-pinentry\n")

        if gpgpath is None:
            gpgpath = find_executable("gpg")
        assert os.path.isfile(gpgpath)
        self.gpgpath = gpgpath
        self.isgpg2 = os.path.basename(gpgpath) == "gpg2"
        self._tempbase = os.path.join(self.homedir, "tmp")
        if not os.path.exists(self._tempbase):
            os.makedirs(self._tempbase)

    def killagent(self):
        if self.isgpg2:
            args = [find_executable("gpg-connect-agent"),
                    "--homedir", self.homedir, "--no-autostart",
                    "KILLAGENT"]
            popen = Popen(args)
            popen.wait()


    @contextmanager
    def temp_written_file(self, data):
        with tempfile.NamedTemporaryFile(dir=self._tempbase, delete=False) as f:
            f.write(data)
        try:
            yield f.name
        finally:
            os.remove(f.name)

    def _gpg_out(self, argv, input=None, strict=False):
        return self._gpg_outerr(argv, input=input, strict=strict)[0]

    def _gpg_outerr(self, argv, input=None, strict=False):
        args = [self.gpgpath, "--homedir", self.homedir, "--batch",
                "--no-permission-warning"]

        args.extend(["--passphrase", "''"])
        if self.isgpg2:
            args.extend(["--pinentry-mode=loopback"])
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
        spec = "\n".join([
            "%no-protection",
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
        ]).encode("utf8")
        with self.temp_written_file(spec) as fn:
            out, err = self._gpg_outerr(["--gen-key", fn])

        # quickly find key id or fingerprint
        keyid = self._find_keyid(err)
        logging.debug("created secret key: %s", keyid)
        return keyid

    _gpgout_keyid_pattern = re.compile(b"key (?:ID )?([0-9A-F]+)")
    def _find_keyid(self, string):
        m = self._gpgout_keyid_pattern.search(string)
        assert m and len(m.groups()) == 1, string
        x = m.groups()[0]
        if not isinstance(x, six.text_type):
            x = x.decode("ascii")
        return x

    def list_secret_key_packets(self, keyid):
        return self._list_packets(self.get_secret_keydata(keyid))

    def list_public_key_packets(self, keyid):
        return self._list_packets(self.get_public_keydata(keyid))

    def list_packets(self, keydata):
        out = self._gpg_out(["--list-packets"], input=keydata)
        # build up a list of (pkgname, pkgvalue, lines) tuples
        packets = []
        lines = []
        last_package_type = None
        for rawline in out.splitlines():
            line = rawline.strip()
            c = line[0:1]
            if c == b"#":
                continue
            if c == b":":
                i = line[1:].find(c)
                if i != -1:
                    ptype = line[1:i+1]
                    pvalue = line[i+2:].strip()
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

    def get_public_keydata(self, keyid, armor=False, b64=False):
        args = ["-a"] if armor else []
        args.extend(["--export", str(keyid)])
        out = self._gpg_out(args, strict=True)
        return out if not b64 else b64encode_u(out)

    def get_secret_keydata(self, keyid, armor=False):
        args = ["-a"] if armor else []
        args.extend(["--export-secret-key", keyid])
        return self._gpg_out(args, strict=True)

    def encrypt(self, data, recipients):
        recs = []
        for r in recipients:
            recs.extend(["--recipient", r])
        return self._gpg_out(recs + ["--encrypt", "--always-trust"], input=data)

    def sign(self, data, keyid):
        return self._gpg_out(["--detach-sign", "-u", keyid], input=data)

    def verify(self, data, signature):
        with self.temp_written_file(signature) as sig_fn:
            out, err = self._gpg_outerr(["--verify", sig_fn, "-"], input=data)
        return self._find_keyid(err)

    def decrypt(self, enc_data):
        return self._gpg_out(["--decrypt"], input=enc_data)

    def import_keydata(self, keydata):
        out, err = self._gpg_outerr(["--import"], input=keydata)
        return self._find_keyid(err)


def find_executable(name):
    """ return a path object found by looking at the systems
        underlying PATH specification.  If an executable
        cannot be found, None is returned. copied and adapted
        from py.path.local.sysfind.
    """
    if os.path.isabs(name):
        return name if os.path.isfile(name) else None
    else:
        if iswin32:
            paths = os.environ['Path'].split(';')
            if '' not in paths and '.' not in paths:
                paths.append('.')
            try:
                systemroot = os.environ['SYSTEMROOT']
            except KeyError:
                pass
            else:
                paths = [re.sub('%SystemRoot%', systemroot, path)
                         for path in paths]
        else:
            paths = os.environ['PATH'].split(':')
        tryadd = []
        if iswin32:
            tryadd += os.environ['PATHEXT'].split(os.pathsep)
        tryadd.append("")

        for x in paths:
            for addext in tryadd:
                p = os.path.join(x, name) + addext
                try:
                    if os.path.isfile(p):
                        return p
                except Exception:
                    pass
    return None

