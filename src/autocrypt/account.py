from __future__ import unicode_literals

import os
import json
import shutil
import six
import uuid
from .bingpg import BinGPG, cached_property
from base64 import b64decode
from . import header


class KVStoreMixin(object):
    def __init__(self, path):
        self._kv_path = path

    @cached_property
    def _kv_dict(self):
        if os.path.exists(self._kv_path):
            with open(self._kv_path, "r") as f:
                d = json.load(f)
        else:
            d = {}
        self._kv_dict_old = d.copy()
        return d

    def kv_reload(self):
        try:
            self._property_cache.clear()
        except AttributeError:
            pass
        self._kv_dict

    def kv_commit(self):
        d = self._kv_dict
        if d != self._kv_dict_old:
            with open(self._kv_path, "w") as f:
                json.dump(d, f)
            self._kv_dict_old = d.copy()
            return True


def kv_persisted_property(name, typ):
    def get(self):
        return self._kv_dict[name]
    def set(self, value):
        if not isinstance(value, typ):
            raise TypeError("value %r is not of type %r" %(value, typ))
        self._kv_dict[name] = value
    return property(get, set)


class Account(KVStoreMixin):
    """ Autocrypt Account which stores state and keys into the specified dir.
    """
    class NotInitialized(Exception):
        pass

    def __init__(self, dir):
        self.dir = dir
        kvstore_path = os.path.join(self.dir, "config")
        super(Account, self).__init__(kvstore_path)

    uuid = kv_persisted_property("uuid", six.text_type)
    own_keyhandle = kv_persisted_property("own_keyhandle", six.text_type)
    _prefer_encrypt = kv_persisted_property("prefer_encrypt", six.text_type)

    @cached_property
    def bingpg(self):
        return BinGPG(os.path.join(self.dir, "gpghome"))

    def init(self):
        assert not self.exists()
        account_uuid = six.text_type(uuid.uuid4().hex)
        keyhandle = self.bingpg.gen_secret_key(account_uuid)
        assert isinstance(keyhandle, six.text_type)
        self.uuid = account_uuid
        self.own_keyhandle = keyhandle
        self._prefer_encrypt = "notset"
        self.kv_commit()

    def set_prefer_encrypt(self, value):
        if value not in ("yes", "no", "notset"):
            raise ValueError(repr(value))
        self._prefer_encrypt = value
        self.kv_commit()

    def _ensure_exists(self):
        if not self.exists():
            raise self.NotInitialized(
                "Account directory %r not initialized" %(self.dir))

    def exists(self):
        return bool(self._kv_dict)

    def remove(self):
        shutil.rmtree(self.dir)
        self._property_cache.clear()

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
            keydata=self.bingpg.get_public_keydata(self.own_keyhandle),
            prefer_encrypt=self._prefer_encrypt,
        )

    def export_public_key(self, keyid=None):
        """ return armored public key for this account. """
        self._ensure_exists()
        keyid = self.own_keyhandle if keyid is None else keyid
        return self.bingpg.get_public_keydata(keyid, armor=True)

    def export_private_key(self):
        """ return armored public key for this account. """
        self._ensure_exists()
        return self.bingpg.get_secret_keydata(self.own_keyhandle, armor=True)

    def process_incoming_mail(self, msg):
        self._ensure_exists()
        d = header.parse_one_ac_header_from_msg(msg)
        if d["to"] == header.parse_email_addr(msg["From"])[1]:
            peers = self._kv_dict.setdefault("peers", {})
            peers[d["to"]] = d
            self.kv_commit()
            return d["to"]

    def get_latest_public_keyid(self, emailadr):
        peers = self._kv_dict.get("peers", {})
        state = peers.get(emailadr)
        if state:
            keydata = b64decode(state["key"])
            return self.bingpg.import_keydata(keydata)
