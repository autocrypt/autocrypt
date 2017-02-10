#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab 2

"""Functions to create, file import/export OpenPGP keys"""
# FIXME: this file should be moved to ../autocrypt/ and possibly
# merged with gpg.py

import logging
import sys
from base64 import b64encode
from pgpy import PGPKey, PGPUID
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm
from pgpy.constants import SymmetricKeyAlgorithm, CompressionAlgorithm

logger = logging.getLogger(__name__)


def generate_rsa_key(uid='alice@testsuite.autocrypt.org',
                     alg_key=PubKeyAlgorithm.RSAEncryptOrSign,
                     alg_subkey=PubKeyAlgorithm.RSAEncryptOrSign,
                     size=2048):
    # RSAEncrypt is deprecated, therefore using RSAEncryptOrSign
    # also for the subkey
    """Generate PGPKey object.

    :param alg_key: algorithm for primary key
    :param alg_subkey: algorithm for subkey
    :param size: key size
    :param uid: e-mail address
    :return: key
    :type alg_key: PubKeyAlgorithm
    :type alg_subkey: PubKeyAlgorithm
    :type size: integer
    :type uid: string
    :rtype: PGPKey

    """
    # NOTE: default algorithm was decided to be RSA and size 2048.
    key = PGPKey.new(alg_key, size)
    # NOTE: pgpy implements separate attributes for name and e-mail address.
    # name is mandatory.
    # Here using e-mail address for the attribute name in order for
    # the uid to be the e-mail address.  If name attribute is set to
    # empty string and email to the e-mail address, the uid will be '
    # <e-mail address>', for instance:
    # " <alice@testsuite.autocrypt.org>" - which we do not want.
    uid = PGPUID.new(uid)
    # NOTE: it is needed to specify all arguments in current pgpy version.
    # FIXME: see which defaults we would like here
    key.add_uid(uid,
                usage={KeyFlags.Sign},
                hashes=[HashAlgorithm.SHA512, HashAlgorithm.SHA256],
                ciphers=[SymmetricKeyAlgorithm.AES256,
                         SymmetricKeyAlgorithm.AES192,
                         SymmetricKeyAlgorithm.AES128],
                compression=[CompressionAlgorithm.ZLIB,
                             CompressionAlgorithm.BZ2,
                             CompressionAlgorithm.ZIP,
                             CompressionAlgorithm.Uncompressed])
    subkey = PGPKey.new(alg_subkey, size)
    key.add_subkey(subkey, usage={KeyFlags.EncryptCommunications,
                                  KeyFlags.EncryptStorage})
    logger.debug('Created key with fingerprint %s', key.fingerprint)
    return key


def generate_ec_key():
    # NOTE: currently pgpy does not implement ed25519 nor cv25519
    pass


def key_from_file(key_path='/tmp/pubkey.asc'):
    """Create PGPKey object from an armored key file (either public or private)

    :param key_path: path to the key
    :return: key
    :type key_path: string
    :rtype: PGPKey

    """
    key, _ = PGPKey.from_file(key_path)
    logger.debug('Imported key with fingerprint %s', key.fingerprint)
    return key


def import_key_into_keyring(key, gnupghome_path='/tmp/gnupg'):
    """Import key into a filesystem compatible GNUpg keyring

    :param key: key to import
    :param gnupghome_path: keyring path
    :type key: PGPKey
    :type gnupghome_path: string

    .. note::
        pgpy does not implement filesystem keyring
    """
    # NOTE: currently pgpy does not implement filesystem keyring
    pass


def export_key_to_file(key, key_path='/tmp/key.asc'):
    """Export key to file.

    :param key: key (either public or private)
    :type key: PGPKey
    :param key_path: filesystem path to write the key to
    :type key_path: string

    """
    with open(key_path, 'w') as fp:
        fp.write(str(key))
    logger.debug('Exported private key with fingerprint %s to file %s', key.fingerprint, key_path)


def export_pubkey_to_file(key, pubkey_path='/tmp/pubkey.asc'):
    """Export public key to file from either a public or private key.

    :param key: key (either public or private)
    :type key: PGPKey
    :param key_path: filesystem path to write the key to
    :type key_path: string

    """
    if key.is_public:
        export_key_to_file(key, pubkey_path)
    else:
        pubkey = key.pubkey
        export_key_to_file(pubkey, pubkey_path)
    logger.debug('Exported public key with fingerprint %s to file %s', key.fingerprint, pubkey_path)


def key_shortid(key):
    return key.fingerprint.replace(' ', '')[:8]


def key_longid(key):
    return key.fingerprint.replace(' ', '')[:16]


def key_fp(key):
    """Key fingerprint.

    :param key: key (either public or private)
    :type key: PGPKey
    :return: key fingerprint
    :rtype: string

    """
    return key.fingerprint


def key_armor_str(key):
    """Key armored string.

    :param key: key (either public or private)
    :type key: PGPKey
    :return: key armored string
    :rtype: string

    """
    return str(key)


def key_bytes(key):
    """Key bytes.

    :param key: key (either public or private)
    :type key: PGPKey
    :return: key bytes
    :rtype: string

    """
    if sys.version_info >= (3, 0):
        keybytes = bytes(key)
    else:
        keybytes = key.__bytes__()
    return keybytes


def key_base64(key):
    """Base 64 representation of key bytes.

    :param key: key (either public or private)
    :type key: PGPKey
    :return: Base 64 representation of key bytes
    :rtype: string

    """
    keybytes = key_bytes(key)
    keybase64 = b64encode(keybytes)
    return keybase64
