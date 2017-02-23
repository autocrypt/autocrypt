
Mail Program Autocrypt Development Branches
-------------------------------------------

Last updated: 17th January 2017

Python: `Python Reference CLI tool and API <https://github.com/autocrypt/py-autocrypt>`_ (`docs <https://py-autocrypt.readthedocs.org>`_)

Enigmail: `Enigmail autocrypt branch <https://sourceforge.net/p/enigmail/source/ci/master/tree/>`_

Android K9: `K9 autocrypt branch <https://github.com/k9mail/k-9/commits/trust-id>`_

Mailpile: XXX to-be-filled-in

Notmuch/Alot: XXX to-be-filled-in

Bitmask/LEAP: `ongoing refactorings <https://0xacab.org/leap/bitmask-dev/merge_requests/55/diffs>`_

Go: `Go Autocrypt <https://github.com/autocrypt/go-autocrypt>`_

**Please-fill-in-your-development-branch here**


Autocrypt bot
-------------

Responder
+++++++++

We deploy a preliminary auto-responder which accepts and sends mails
with Autocrypt headers.  Just sent a mail to ``bot at autocrypt dot
org`` and wait for the reply and look at the headers.  As of Janury
2017, the Bot does not implement the full level-0 protocol.

Bot Dovecot IMAP
++++++++++++++++

You can login to IMAP/Dovecot (port 993, TLS mandatory) with the
username "bot" and the password as stored in ``gitcrypt/credentials.txt``.
Ask on IRC or the mailing list and provide your gpg public key for access to
the password credentials using `git-crypt <https://www.agwa.name/projects/git-crypt/>`_.

ssh access to bot account
+++++++++++++++++++++++++

You can ssh to the bot account: ``ssh -l bot mail.autocrypt.org``,
ECDSA key fingerprint is ``SHA256:4RWh81zOd/Pgq3mHhKpyLdVZJfOpq+DgqKheUIhJgWQ``.
Ask on IRC to get your SSH key added (anyone already with access
to the bot@autocrypt.org account can add it to ``.ssh/authorized_keys``).

