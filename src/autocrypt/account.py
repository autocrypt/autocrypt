# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab

""" Contains Account class which offers all autocrypt related access
and manipulation methods. It also contains some internal helpers
which help to persist config and peer state.
"""


from __future__ import unicode_literals

import os
import json
import shutil
import six
import uuid
from .bingpg import cached_property, BinGPG
from contextlib import contextmanager
from base64 import b64decode
from . import mime
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

    # def _reload(self):
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
    """ Autocrypt Account class which allows to manipulate autocrypt
    configuration and state for use from mail processing agents.
    Autocrypt uses a standalone GPG managed keyring and persists its
    config to a default app-config location.

    You can init an account and then use it to generate Autocrypt
    headers and process incoming mails to discover and memorize
    a peer's Autocrypt headers.
    """
    class NotInitialized(Exception):
        pass

    def __init__(self, dir, gpgpath="gpg"):
        """ Initialize the account configuration and internally
        used gpggrapper.

        :type dir: unicode
        :param dir:
             directory in which autocrypt will store all state
             including a gpg-managed keyring.
        :type gpgpath: unicode
        :param gpgpath:
            If the path contains path separators and points
            to an existing file we use it directly.
            If it contains no path separators, we lookup
            the path to the binary under the system's PATH.
            If we can not determine an eventual binary
            we raise ValueError.
        """
        self.dir = dir
        self.config = Config(os.path.join(self.dir, "config"))
        self.bingpg = BinGPG(os.path.join(self.dir, "gpghome"), gpgpath=gpgpath)

    def init(self):
        """ Initialize this account with a new secret key, uuid
        and default settings.
        """
        assert not self.exists()
        self.bingpg.init()
        with self.config.atomic_change():
            self.config.uuid = uuid.uuid4().hex
            keyhandle = self.bingpg.gen_secret_key(self.config.uuid)
            self.config.own_keyhandle = keyhandle
            self.config.prefer_encrypt = "notset"
        assert self.exists()

    def set_prefer_encrypt(self, value):
        """ set prefer-encrypt setting to be used when generating a
        header with make_header.

        :param value: one of "yes", "no", "notset"
        """

        if value not in ("yes", "no", "notset"):
            raise ValueError(repr(value))
        with self.config.atomic_change():
            self.config.prefer_encrypt = value

    def _ensure_exists(self):
        if not self.exists():
            raise self.NotInitialized(
                "Account directory {!r} not initialized".format(self.dir))

    def exists(self):
        """ return True if the account directory exists and has been properly
        initialized (through an earlier call to init()).
        """
        return self.config.exists()

    def remove(self):
        """ remove the account directory and reset this account configuration
        to empty.  You need to call init() to reinitialize.
        """
        shutil.rmtree(self.dir)
        self.config._dict.clear()

    def make_header(self, emailadr, headername="Autocrypt: "):
        """ return an Autocrypt header line which uses our own
        key and the provided emailadr.

        :type emailadr: unicode
        :param emailadr:
            pure email address which we use as the "to" attribute
            in the generated Autocrypt header.  An account may generate
            and send mail from multiple aliases and we advertise
            the same key across those aliases.
            (XXX discuss whether "to" is all that useful for level-0 autocrypt.)

        :type headername: unicode
        :param headername:
            the prefix we use for the header, defaults to "Autocrypt".
            By specifying an empty string you just get the header value.

        :rtype: unicode
        :returns: autocrypt header with prefix and value
        """
        self._ensure_exists()
        return headername + mime.make_ac_header_value(
            emailadr=emailadr,
            keydata=self.bingpg.get_public_keydata(self.config.own_keyhandle),
            prefer_encrypt=self.config.prefer_encrypt,
        )

    def process_incoming(self, msg):
        """ process incoming mail message and store information
        from any Autocrypt header for the From/Autocrypt peer
        which created the message.

        :type msg: email.message.Message
        :param msg: instance of a standard email Message.
        """
        self._ensure_exists()
        From = mime.parse_email_addr(msg["From"])[1]
        old = self.config.peers.get(From, {})
        d = mime.parse_one_ac_header_from_msg(msg)
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
        """ get latest public keyhandle we have for a given
        emailadress.

        :type emailadr: unicode
        :param emailadr: pure email address without any prefixes or real names.
        """
        state = self.config.peers.get(emailadr)
        if state:
            keydata = b64decode(state["key"])
            return self.bingpg.import_keydata(keydata)

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
