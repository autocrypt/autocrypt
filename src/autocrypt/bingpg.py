from __future__ import print_function, unicode_literals
import logging
from distutils.version import LooseVersion as V
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
        key = f.__name__
        try:
            return propcache[key]
        except KeyError:
            x = self._property_cache[key] = f(self)
            return x

    def set(self, val):
        propcache = self.__dict__.setdefault("_property_cache", {})
        propcache[f.__name__] = val
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
        if gpgpath is None:
            gpgpath = find_executable("gpg")
        self.gpgpath = gpgpath
        self.isgpg2 = os.path.basename(gpgpath) == "gpg2"

    def init(self):
        if not os.path.exists(self.homedir):
            # we create the dir if the basedir exists, otherwise we fail
            os.mkdir(self.homedir)

        if V("2.0") <= V(self.get_version()) < V("2.1.12"):
            p = os.path.join(self.homedir, "gpg-agent.conf")
            assert not os.path.exists(p)
            with open(p, "w") as f:
                f.write("allow-loopback-pinentry\n")

    def killagent(self):
        if self.isgpg2:
            args = [find_executable("gpg-connect-agent"),
                    "--homedir", self.homedir, "--no-autostart",
                    "KILLAGENT"]
            popen = Popen(args)
            popen.wait()

    @contextmanager
    def temp_written_file(self, data):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(data)
        try:
            yield f.name
        finally:
            os.remove(f.name)

    def _gpg_out(self, argv, input=None, strict=False, encoding="utf8"):
        return self._gpg_outerr(argv, input=input, strict=strict, encoding=encoding)[0]

    def _gpg_outerr(self, argv, input=None, strict=False, encoding="utf8"):
        """ return stdout and stderr output of invoking gpg with the
        specified parameters.

        If the invocation leads to a non-zero exit
        status an InvocationFailure exception is thrown.  It is also
        thrown if strict is True and there was non-empty stderr output.
        stderr output will always be returned as a text type while
        stdout output will be encoded if encoding is set (default is "utf8").
        If you want binary stdout output specify encoding=None.
        """
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
        err = err.decode("ascii")
        if encoding:
            out = out.decode(encoding)
        return out, err

    @cached_property
    def _version_info(self):
        return self._gpg_out(['--version'])

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

        keyhandle = self._find_keyhandle(err)
        logging.debug("created secret key: %s", keyhandle)
        return keyhandle

    def list_public_keyhandles(self):
        out = self._gpg_out(["--skip-verify", "--with-colons", "--list-public-keys"])
        return [line.split(":")[4]
                    for line in out.splitlines()
                        if line.startswith("pub:")]

    _gpgout_keyhandle_pattern = re.compile("key (?:ID )?([0-9A-F]+)")
    def _find_keyhandle(self, string):
        m = self._gpgout_keyhandle_pattern.search(string)
        assert m and len(m.groups()) == 1, string
        x = m.groups()[0]

        # now search the fingerprint
        assert len(x) == 8   # keyid has 8 hex bytes
        for fp in self.list_public_keyhandles():
            if fp[-8:] == x:
                if not isinstance(x, six.text_type):
                    fp = fp.decode("ascii")
                return fp
        raise ValueError("could not find fingerprint")

    def list_secret_key_packets(self, keyhandle):
        return self.list_packets(self.get_secret_keydata(keyhandle))

    def list_public_key_packets(self, keyhandle):
        return self.list_packets(self.get_public_keydata(keyhandle))

    def list_packets(self, keydata):
        out = self._gpg_out(["--list-packets"], input=keydata)
        # build up a list of (pkgname, pkgvalue, lines) tuples
        packets = []
        lines = []
        last_package_type = None
        for rawline in out.splitlines():
            line = rawline.strip()
            c = line[0:1]
            if c == "#":
                continue
            if c == ":":
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

    def get_public_keydata(self, keyhandle, armor=False, b64=False):
        args = ["-a"] if armor else []
        args.extend(["--export", str(keyhandle)])
        out = self._gpg_out(args, strict=True, encoding=None)
        return out if not b64 else b64encode_u(out)

    def get_secret_keydata(self, keyhandle, armor=False):
        args = ["-a"] if armor else []
        args.extend(["--export-secret-key", keyhandle])
        return self._gpg_out(args, strict=True, encoding=None)

    def encrypt(self, data, recipients):
        recs = []
        for r in recipients:
            recs.extend(["--recipient", r])
        return self._gpg_out(recs + ["--encrypt", "--always-trust"], input=data,
                             encoding=None)

    def sign(self, data, keyhandle):
        return self._gpg_out(["--detach-sign", "-u", keyhandle], input=data,
                             encoding=None)

    def verify(self, data, signature):
        with self.temp_written_file(signature) as sig_fn:
            out, err = self._gpg_outerr(["--verify", sig_fn, "-"], input=data)
        return self._find_keyhandle(err)

    def decrypt(self, enc_data):
        out, err = self._gpg_outerr(["--with-colons", "--decrypt"],
                                    input=enc_data, encoding=None)
        lines = err.splitlines()
        l = []
        while lines:
            line1 = lines.pop(0)
            m = re.match("gpg.*with (\d+)-bit (\w+).*"
                         "ID (\w+).*created (.*)", line1)
            if m:
                bits, keytype, id, date = m.groups()
                line2 = lines.pop(0)
                if line2.startswith("    "):
                   uid = line2.strip().strip('"')
                l.append(KeyInfo(keytype, bits, id, uid, date))
        return out, l

    def import_keydata(self, keydata):
        out, err = self._gpg_outerr(["--skip-verify", "--import"], input=keydata)
        return self._find_keyhandle(err)


class KeyInfo:
    def __init__(self, type, bits, id, uid, date_created):
        self.type = type
        self.bits = int(bits)
        self.id = id
        self.uid = uid
        self.date_created = date_created

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

