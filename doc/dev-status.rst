Autocrypt-capable MUAs level 1 implementation status
====================================================

Last updated: ``2017-12-14``

+--------------------------------------+--------+--------+--------+--------+--------------+--------+--------+--------+----------+
|MUA/project                           |header  |keygen  |peer    |header  |recommend     |encrypt |setup   |setup   |uid       |
|                                      |parsing |        |state   |inject  |              |        |message |process |decorative|
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

- ``MUA/project``: denotes a mail app, library or tool.

- ``header parsing``: compliant parsing of the Autocrypt header

- ``keygen``: secret key generation follows Autocrypt UI guidance

- ``peerstate``: state is kept according to spec

- ``header inject``: proper creation of outgoing Autocrypt header

- ``recommend``: implements Autocrypt recommendation

- ``encrypt``: encrypts outgoing messages properly

- ``setup message``: proper generation and processing of Autocrypt Setup Message

- ``setup process``: follows guidance with respect to Autocrypt account setup

- ``uid decorative``: UID in key data is only used for decorative
  purposes, and in particular not for looking up keys for an e-mail address.


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

- `Delta.Chat code <https://github.com/deltachat/>`_

Testing Autocrypt
+++++++++++++++++

There is an Autocrypt Bot which accepts and sends mails with Autocrypt
headers. Just write an E-Mail to bot@autocrypt.org. :doc:`Find out more about the bot...<bot>`
