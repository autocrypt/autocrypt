Autocrypt-capable MUAs level 1 implementation status
====================================================

Last updated: ``2017-12-14``

+--------------------------------------+--------+--------+--------+--------+--------------+--------+--------+--------+----------+
|MUA/feature                           |header  |keygen  |peer    |header  |recommend     |encrypt |setup   |setup   |uid       |
|                                      |parsing |        |state   |inject  |during compose|        |message |process |decorative|
|                                      |        |        |        |        |              |        |        |        |          |
+======================================+========+========+========+========+==============+========+========+========+==========+
|.. image:: images/logos/deltachat.png |✔       |✔       |✔       |✔       |✔             |✔       |started |started |✔         |
|                                      |        |        |        |        |              |        |        |        |          |
|`delta.chat`_                         |        |        |        |        |              |        |        |        |          |
+--------------------------------------+--------+--------+--------+--------+--------------+--------+--------+--------+----------+
|.. image:: images/logos/k9.png        |✔       |✔ [1]_  |✔       |✔       |✔             |✔       |branch  |branch  |✔         |
|                                      |        |        |        |        |              |        |        |        |          |
|`K-9 Mail`_                           |        |        |        |        |              |        |        |        |          |
+--------------------------------------+--------+--------+--------+--------+--------------+--------+--------+--------+----------+
|.. image:: images/logos/enigmail.png  |✔       |✔       |✔       |✔ [2]_  |✘             |✔       |✔       |✔       |✘         |
|                                      |        |        |        |        |              |        |        |        |          |
|`Enigmail`_                           |        |        |        |        |              |        |        |        |          |
+--------------------------------------+--------+--------+--------+--------+--------------+--------+--------+--------+----------+
|`py-autocrypt`_                       |✔       |✔       |✔       |✔       |✘             |✘       |✘       |✘       |✔         |
+--------------------------------------+--------+--------+--------+--------+--------------+--------+--------+--------+----------+
|.. image:: images/logos/notmuch.png   |branch  |✘       |✘       |✘       |✘             |✘       |✘       |✘       |✔         |
|                                      |        |        |        |        |              |        |        |        |          |
|`notmuch`_                            |        |        |        |        |              |        |        |        |          |
+--------------------------------------+--------+--------+--------+--------+--------------+--------+--------+--------+----------+
|.. image:: images/logos/mailpile.png  |        |        |        |        |              |        |        |        |          |
|                                      |        |        |        |        |              |        |        |        |          |
|`mailpile`_                           |        |        |        |        |              |        |        |        |          |
+--------------------------------------+--------+--------+--------+--------+--------------+--------+--------+--------+----------+
|`gmime`_                              |≥3.0.4  |N/A     |N/A     |≥3.0.4  |N/A           |N/A     |✘       |✘       |✔         |
+--------------------------------------+--------+--------+--------+--------+--------------+--------+--------+--------+----------+

Logos are copyright their respective owners.

Legend:

.. todo::

    describe the headers of each of the columns in the above table @hpk42

.. [1] require passphrase
.. [2] always send

.. _delta.chat: https://delta.chat/
.. _K-9 Mail: https://k9mail.github.io/
.. _Enigmail: https://www.enigmail.net/
.. _py-autocrypt: https://py-autocrypt.readthedocs.io/
.. _notmuch: https://notmuchmail.org/
.. _mailpile: https://www.mailpile.is/
.. _gmime: https://github.com/jstedfast/gmime/

For developers
--------------

Source code:

- `py-autocrypt code <https://github.com/autocrypt/py-autocrypt>`_

- `Enigmail code <https://sourceforge.net/p/enigmail/source/ci/master/tree/>`_

- K9: TODO

- Mailpile: TODO

- Notmuch/Alot: TODO

- `Bitmask/LEAP refactorings <https://0xacab.org/leap/bitmask-dev/merge_requests/55/diffs>`_

- `Go Autocrypt <https://github.com/autocrypt/go-autocrypt>`_

- Delta-Chat: TODO

Autocrypt bot
+++++++++++++++

Implemented using `py-autocrypt`_.

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
