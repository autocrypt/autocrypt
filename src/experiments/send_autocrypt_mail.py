#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab 2

""""""
import argparse
import logging

import gpg_utils
import generate_autocrypt
from _version import version

DEBUG = False


def main():
    global DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug',
                        help='Set logging level to debug',
                        action='store_true')
    # TODO: add directories where import/export keys
    parser.add_argument('-o', '--outputdir', help='',
                         default=None)
    parser.add_argument('-v', '--version', action='version',
                        help='version',
                        version='%(prog)s ' + version)
    parser.add_argument('-f', '--sender',
                        help='Email sender address and OpenPGP UID',
                        default='user@localhost')
                        # default='alice@testsuite.autocrypt.org')
    parser.add_argument('-t', '--recipient',
                        help='Email recipient address',
                        default='root@localhost')
                        # default='bot@autocrypt.org')
    parser.add_argument('-g', '--gen',
                        help='Generate a OpenPGP key pair',
                        default=True)
    parser.add_argument('-s', '--subkey',
                        help='Generate encryption subkey',
                        default=True)
    parser.add_argument('-p', '--protect',
                        help='Protect private key',
                        default=False)
    parser.add_argument('-m', '--mail',
                        help='Generate key and send mail, '\
                              'otherwise generate only key',
                        default=True)
    args = parser.parse_args()

    if args.debug:
        DEBUG = True
        FORMAT = "%(levelname)s: %(filename)s:%(lineno)s -"\
                 "%(funcName)s - %(message)s"
        logging.basicConfig(format=FORMAT, level=logging.DEBUG)
        logger = logging.getLogger(__name__)
    else:
        from logging import handlers
        FORMAT = "%(asctime)s %(name)s %(module)s[%(process)s]:"\
                 " %(levelname)s - %(message)s"
        datefmt = "%b %d %H:%M:%S"
        logging.basicConfig(format=FORMAT, level=logging.INFO,
                            datefmt=datefmt)
        logger = logging.getLogger(__name__)
        h = handlers.SysLogHandler(address='/dev/log')
        formatter = logging.Formatter(FORMAT)
        h.setFormatter = formatter
        logger.addHandler(h)

    if args.gen is True:
        # generate a new key
        key = gpg_utils.generate_rsa_key(args.sender,
                                         add_subkey=args.subkey)
        # export key to files
        gpg_utils.export_key_to_file(key, outputdir=args.outputdir)
        gpg_utils.export_pubkey_to_file(key, outputdir=args.outputdir)
    else:
        # import key from a file
        key = gpg_utils.key_from_file()
    if args.mail is True:
        keybase64 = gpg_utils.key_base64(key)
        keyfp = gpg_utils.key_fp(key)
        msg = generate_autocrypt.generate_email(keybase64,
                                                keyfp,
                                                args.sender,
                                                args.recipient)
        generate_autocrypt.send_email(msg, args.sender,
                                      args.recipient)


if __name__ == '__main__':
    main()
