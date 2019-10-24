Autocrypt bot
+++++++++++++

Implemented using `py-autocrypt`_.

.. _py-autocrypt: https://py-autocrypt.readthedocs.io/

Responder
~~~~~~~~~~

We deploy a preliminary auto-responder which accepts and sends mails
with Autocrypt headers.  Just sent a mail to bot@autocrypt.org and wait for the reply
and look at the headers.  As of January 2017, the Bot does not implement the full
Level 1 protocol.

Bot Dovecot IMAP
~~~~~~~~~~~~~~~~

You can login to IMAP/Dovecot (port 993, TLS mandatory) with the
username "bot" and the password as stored in ``gitcrypt/credentials.txt``.
Ask on IRC or the mailing list and provide your gpg public key for access to
the password credentials using `git-crypt <https://www.agwa.name/projects/git-crypt/>`_.

ssh access to bot account
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can ssh to the bot account: ``ssh -l bot mail.autocrypt.org``,
ECDSA key fingerprint is ``SHA256:4RWh81zOd/Pgq3mHhKpyLdVZJfOpq+DgqKheUIhJgWQ``.
Ask on IRC to get your SSH key added (anyone already with access
to the bot@autocrypt.org account can add it to ``.ssh/authorized_keys``).
