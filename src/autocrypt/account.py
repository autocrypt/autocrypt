from __future__ import unicode_literals

import os
import json
import shutil
import six
import uuid
from .bingpg import cached_property, BinGPG
from contextlib import contextmanager
from base64 import b64decode
from . import header
from email.utils import parsedate


class PersistentAttrMixin(object):
    def __init__(self, path):
        self._path = path

    @cached_property
    def _dict(self):
        if os.path.exists(self._path):
            with open(self._path, "r") as f:
                d = json.load(f)
        else:
            d = {}
        self._dict_old = d.copy()
        return d

    #def _reload(self):
    #    try:
    #        self._property_cache.pop("_dict")
    #    except AttributeError:
    #        pass

    def _commit(self):
        if self._dict != self._dict_old:
            with open(self._path, "w") as f:
                json.dump(self._dict, f)
            self._kv_dict_old = self._dict.copy()
            return True

    @contextmanager
    def atomic_change(self):
        # XXX allow multi-read/single-write multi-process concurrency model
        # by doing some file locking or using sqlite or something.
        try:
            yield
        except:
            self._dict = self._dict_old.copy()
            raise
        else:
            self._commit()


def persistent_property(name, typ):
    def get(self):
        return self._dict.setdefault(name, typ())
    def set(self, value):
        if not isinstance(value, typ):
            if not (typ == six.text_type and isinstance(value, bytes)):
                raise TypeError(value)
            value = value.decode("ascii")
        self._dict[name] = value
    return property(get, set)


class Config(PersistentAttrMixin):
    uuid = persistent_property("uuid", six.text_type)
    own_keyhandle = persistent_property("own_keyhandle", six.text_type)
    prefer_encrypt = persistent_property("prefer_encrypt", six.text_type)
    peers = persistent_property("peers", dict)

    def exists(self):
        return self.uuid


class Account(object):
    """ Autocrypt Account which stores state and keys into the specified dir.
    """
    class NotInitialized(Exception):
        pass

    def __init__(self, dir, gpgpath=None):
        self.dir = dir
        self.config = Config(os.path.join(self.dir, "config"))
        self.bingpg = BinGPG(os.path.join(self.dir, "gpghome"), gpgpath=gpgpath)

    def init(self):
        assert not self.exists()
        self.bingpg.init()
        with self.config.atomic_change():
            self.config.uuid = uuid.uuid4().hex
            keyhandle = self.bingpg.gen_secret_key(self.config.uuid)
            self.config.own_keyhandle = keyhandle
            self.config.prefer_encrypt = "notset"
        assert self.exists()

    def set_prefer_encrypt(self, value):
        if value not in ("yes", "no", "notset"):
            raise ValueError(repr(value))
        with self.config.atomic_change():
            self.config.prefer_encrypt = value

    def _ensure_exists(self):
        if not self.exists():
            raise self.NotInitialized(
                "Account directory %r not initialized" %(self.dir))

    def exists(self):
        return self.config.exists()

    def remove(self):
        shutil.rmtree(self.dir)
        self.config._dict.clear()

    def make_header(self, emailadr, headername="Autocrypt: "):
        """ return an Autocrypt header line which uses our own
        key and the provided emailadr.  We need the emailadr because
        an account may send mail from multiple aliases and we advertise
        the same key across those aliases.
        XXX discuss whether "to" is all that useful for level-0 autocrypt.
        """
        self._ensure_exists()
        return headername + header.make_ac_header_value(
            emailadr=emailadr,
            keydata=self.bingpg.get_public_keydata(self.config.own_keyhandle),
            prefer_encrypt=self.config.prefer_encrypt,
        )

    def export_public_key(self, keyhandle=None):
        """ return armored public key of this account or the one
        indicated by the key handle. """
        self._ensure_exists()
        keyhandle = self.config.own_keyhandle if keyhandle is None else keyhandle
        return self.bingpg.get_public_keydata(keyhandle, armor=True)

    def export_secret_key(self):
        """ return armored public key for this account. """
        self._ensure_exists()
        return self.bingpg.get_secret_keydata(self.config.own_keyhandle, armor=True)

    def process_incoming(self, msg):
        """ process incoming mail message and store information
        about potential Autocrypt header for the From/Autocrypt peer.
        """
        self._ensure_exists()
        From = header.parse_email_addr(msg["From"])[1]
        old = self.config.peers.get(From, {})
        d = header.parse_one_ac_header_from_msg(msg)
        date = msg.get("Date")
        if d:
            if d["to"] == From:
                if parsedate(date) >= parsedate(old.get("*date", date)):
                    d["*date"] = date
                    with self.config.atomic_change():
                        self.config.peers[From] = d
                return d["to"]
        elif old:
            # we had an autocrypt header and now forget about it
            # because we got a mail which doesn't have one
            with self.config.atomic_change():
                self.config.peers[From] = {}

    def get_latest_public_keyhandle(self, emailadr):
        state = self.config.peers.get(emailadr)
        if state:
            keydata = b64decode(state["key"])
            return self.bingpg.import_keydata(keydata)
