Autocrypt-capable MUAs level 1 implementation status
=====================================================

Last updated: ``2017-11-03``

================= ======== ======== ======== ======== ======== ======== ======== ======== ========
 MUA/feature      header   keygen   peer     header   recommen encrypt  setup    setup    uid
                  parsing           state    inject   dation            message  process  decorat
================= ======== ======== ======== ======== ======== ======== ======== ======== ========
 `delta-chat`_    y        y        y        y        y        y        started  y        y
 `k9`_            y        y [1]_   y        y        y        y        branch   branch   y
 `enigmail`_      y        y        y        y [2]_   n        y        y        y        n
 `py-autocrypt`_  y        y        y        y        n        n        n        n        y
 `notmuch`_       y        n        n        n        n        n        n        n        y
 `mailpile`_
================= ======== ======== ======== ======== ======== ======== ======== ======== ========

.. todo::

    TODO @hpk42

Legend:

.. [1] require passphrase
.. [2] always send

.. _delta-chat: https://delta.chat
.. _k9: https://k9mail.github.io/
.. _enigmail: https://www.enigmail.net
.. _py-autocrypt: https://py-autocrypt.readthedocs.io/
.. _notmuch: https://notmuchmail.org/
.. _mailpile: https://www.mailpile.is/

For developers
--------------

Source code:

- `py-autocrypt code <https://github.com/autocrypt/py-autocrypt>`_`

- `Enigmail code <https://sourceforge.net/p/enigmail/source/ci/master/tree/>`_

- K9: TODO

- Mailpile: TODO

- Notmuch/Alot: TODO

- `Bitmask/LEAP refactorings <https://0xacab.org/leap/bitmask-dev/merge_requests/55/diffs>`_

- `Go Autocrypt <https://github.com/autocrypt/go-autocrypt>`_

- Delta-Chat: TODO

Autocrypt bot
+++++++++++++++

Implemented using py-autocrypt.

Responder
~~~~~~~~~~

We deploy a preliminary auto-responder which accepts and sends mails
with Autocrypt headers.  Just sent a mail to ``bot at autocrypt dot
org`` and wait for the reply and look at the headers.  As of Janury
2017, the Bot does not implement the full level-1 protocol.

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
