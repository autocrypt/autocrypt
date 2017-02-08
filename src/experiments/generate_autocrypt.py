#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab 2

"""Functions to create Autocrypt header and send Email"""
# FIXME: this file should be moved to ../autocrypt/.
# It is bassically the opposite to parse.py.

import logging
import smtplib
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

AUTOCRYPT_HEADER = "to=%(uid)s; key=%(key)s\n"


def generate_Autocrypt_header(keybase64,
                              uid='alice@testsuite.autocrypt.org'):
    """Generate Autocrypt header

    :param key: key (either public or private)
    :type key: PGPKey
    :param uid: e-mail address
    :type uid: string
    :return: Autocrypt header
    :rtype: string

    """
    # FIXME: this is done right now in autocrypt.bot,
    # it should be reused
    autocrypt_header = AUTOCRYPT_HEADER %\
        {'uid': uid, 'key': keybase64}
    return autocrypt_header



def generate_email(keybase64,
                   keyfp,
                   sender='alice@testsuite.autocrypt.org',
                   recipient='bot@autocrypt.org',
                   subject='This is an example Autocrypt Email'):
    """Generate an Email with an Autocrypt header

    :param keybase64: public key in base64
    :type key: string
    :param keyfp: key fingerprint
    :type uid: string
    :param sender: the sender Email address
    :type sender: string
    :param recipient: the recipient Email address
    :type recipient: string
    :param subject: the Email subject
    :type subject: string
    :return: Autocrypt Email message
    :rtype: MIMEText

    """
    # TODO: several recipients
    msg = MIMEText(keyfp)
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg['Autocrypt'] = AUTOCRYPT_HEADER %\
        {'uid': sender, 'key': keybase64}
    logger.debug('Generated Email: %s', msg.as_string())
    return msg


def send_email(msg,
               sender='alice@testsuite.autocrypt.org',
               recipient='bot@autocrypt.org',
               smtp_server='localhost'):
    """Send an Autocrypt Email

    :param msg: Autocrypt Email message
    :type msg: MIMEText
    :param sender: the sender Email address
    :type sender: string
    :param recipient: the recipient Email address
    :type recipient: string
    :param smtp_server: the SMTP server domain
    :type smtp_server: string

    """
    # TODO: several recipients
    s = smtplib.SMTP(smtp_server)
    s.sendmail(sender, recipient, msg.as_string())
    logger.debug('Sending Email to %s from %s to %s',
                 smtp_server, sender, recipient)
    s.quit()
