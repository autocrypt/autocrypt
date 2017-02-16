from __future__ import unicode_literals

import os
import json
import shutil
import six
import uuid
from .bingpg import BinGPG, cached_property
from base64 import b64decode
from . import header
from email.utils import parsedate


class KVStoreMixin(object):
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

    def kv_exists(self):
        return os.path.exists(self._path)

    def kv_reload(self):
        self._dict.clear()
        if os.path.exists(self._path):
            self._dict.clear()
            with open(self._path, "r") as f:
                self._dict.update(json.load(f))
        self._dict_old = self._dict.copy()

    def kv_commit(self):
        if self._dict != self._dict_old:
            with open(self._path, "w") as f:
                json.dump(self._dict, f)
            self._kv_dict_old = self._dict.copy()
            return True


def kv_property(name, typ):
    def get(self):
        return self._dict.setdefault(name, typ())
    def set(self, value):
        if not isinstance(value, typ):
            raise TypeError(value)
        self._dict[name] = value
    return property(get, set)


class Config(KVStoreMixin):
    uuid = kv_property("uuid", six.text_type)
    own_keyhandle = kv_property("own_keyhandle", six.text_type)
    prefer_encrypt = kv_property("prefer_encrypt", six.text_type)
    peers = kv_property("peers", dict)


class Account(object):
    """ Autocrypt Account which stores state and keys into the specified dir.
    """
    class NotInitialized(Exception):
        pass

    def __init__(self, dir):
        self.dir = dir
        kvstore_path = os.path.join(self.dir, "config")
        self.config = Config(kvstore_path)


    @cached_property
    def bingpg(self):
        return BinGPG(os.path.join(self.dir, "gpghome"))

    def init(self):
        assert not self.exists()
        account_uuid = six.text_type(uuid.uuid4().hex)
        keyhandle = self.bingpg.gen_secret_key(account_uuid)
        assert isinstance(keyhandle, six.text_type)
        self.config.uuid = account_uuid
        self.config.own_keyhandle = keyhandle
        self.config.prefer_encrypt = "notset"
        self.config.kv_commit()
        assert self.exists()

    def set_prefer_encrypt(self, value):
        if value not in ("yes", "no", "notset"):
            raise ValueError(repr(value))
        self.config.prefer_encrypt = value
        self.config.kv_commit()

    def _ensure_exists(self):
        if not self.exists():
            raise self.NotInitialized(
                "Account directory %r not initialized" %(self.dir))

    def exists(self):
        return self.config.kv_exists()

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

    def export_public_key(self, keyid=None):
        """ return armored public key for this account. """
        self._ensure_exists()
        keyid = self.config.own_keyhandle if keyid is None else keyid
        return self.bingpg.get_public_keydata(keyid, armor=True)

    def export_private_key(self):
        """ return armored public key for this account. """
        self._ensure_exists()
        return self.bingpg.get_secret_keydata(self.config.own_keyhandle, armor=True)

    def process_incoming_mail(self, msg):
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
                    self.config.peers[From] = d
                    self.config.kv_commit()
                return d["to"]
        elif old:
            # we had an autocrypt header and now forget about it
            # because we got a mail which doesn't have one
            self.config.peers[From] = {}
            self.config.kv_commit()

    def get_latest_public_keyid(self, emailadr):
        state = self.config.peers.get(emailadr)
        if state:
            keydata = b64decode(state["key"])
            return self.bingpg.import_keydata(keydata)
