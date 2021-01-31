Autocrypt-capable MUAs level 1 implementation status
====================================================

Last updated: ``2021-01-31``

+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|*MUA/project*                         |*header |*keygen*|*peer |*header|*recommend*|*encrypt*|*setup  |*setup  |*gossip*|*uid       |
|                                      |parsing*|        |state*|inject*|           |         |message*|process*|        |decorative*|
|                                      |        |        |      |       |           |         |        |        |        |           |
+======================================+========+========+======+=======+===========+=========+========+========+========+===========+
|.. image:: images/logos/deltachat.png |✔       |✔       |✔     |✔      |✔          |✔        |✔       |✔       |✔       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`delta.chat`_                         |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/k9.png        |✔       |✔       |✔     |✔      |✔          |✔        |✔       |branch  |✔       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`K-9 Mail`_                           |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/tb-ac.png     |✔       |✔       |✔     |✔      |✔          |✔        |✘       |✔       |✔       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`Autocrypt-Thunderbird`_              |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/enigmail.png  |✔       |✔       |✔     |✔      |✘          |✔        |✔       |✔       |✔       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`Enigmail`_                           |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/Mutt.gif      |✔       |✔       |✔     |✔      |✔          |✔        |✘       |✔       |✔       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`Mutt`_                               |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/neomutt.png   |✔       |✔       |✔     |✔      |✔          |✔        |✘       |✔       |✔       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`Neomutt`_                            |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|`Letterbox`_                          |✔       |✔       |✔     |✔      |✔          |✔        |✘       |✔       |✘       |✔          |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/balsa.jpg     |✔       |✘       |✔     |✔      |✔          |✔        |✘       |✘       |✘       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`Balsa`_                              |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/muacrypt.png  |✔       |✔       |✔     |✔      |✔          |✔        |✘       |✔       |✔       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`muacrypt`_                           |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|`pyac`_                               |✔       |✔       |✔     |✔      |✘          |✔        |✔       |✔       |✔       |✔          |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/notmuch.png   |branch  |✘       |✘     |✘      |✘          |✘        |✘       |✘       |✘       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`notmuch`_                            |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/mailpile.png  |✔       |✔       |✘     |✔      |✘          |✘        |✘       |✘       |✘       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`mailpile`_                           |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|`gmime`_                              |≥3.0.4  |N/A     |N/A   |≥3.0.4 |N/A        |N/A      |✘       |✘       |✘       |✔          |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/emacs.png     |✔       |✔       |✔     |✔      |✔          |✔        |✘       |✘       |✘       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`Emacs`_                              |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/fairemail.png |✔       |✔       |✔     |✔      |✘          |✔        |✘       |✘       |✘       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`FairEmail`_                          |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+

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

.. _delta.chat: https://delta.chat/
.. _K-9 Mail: https://k9mail.github.io/
.. _Autocrypt-Thunderbird: https://addons.thunderbird.net/en-US/thunderbird/addon/autocrypt/
.. _Enigmail: https://www.enigmail.net/
.. _Mutt: http://mutt.org/
.. _Neomutt: https://neomutt.org/
.. _`Letterbox`: https://letterbox-app.org/
.. _`Balsa`: https://mail.gnome.org/archives/balsa-list/2018-December/msg00020.html
.. _muacrypt: https://muacrypt.readthedocs.io/
.. _pyac: https://pyac.readthedocs.io/
.. _notmuch: https://notmuchmail.org/
.. _mailpile: https://www.mailpile.is/
.. _gmime: https://github.com/jstedfast/gmime/
.. _Emacs: https://melpa.org/#/autocrypt
.. _FairEmail: https://email.faircode.eu/

For developers
--------------

Source code:

- `Enigmail code <https://gitlab.com/enigmail/enigmail>`_

- `K9 code <https://github.com/k9mail/k-9>`_

- `Autocrypt-Thunderbird code <https://github.com/autocrypt-thunderbird/autocrypt-thunderbird>`_

- `Delta.Chat code <https://github.com/deltachat/>`_

- `Mailpile code <https://github.com/mailpile/Mailpile>`_

- `Mutt code <https://gitlab.com/muttmua/mutt>`_

- `Neomutt code <https://github.com/neomutt/neomutt>`_

- `Letterbox code <https://git.imp.fu-berlin.de/enzevalos>`_

- Notmuch/Alot: TODO

- `muacrypt (uses gpg) <https://github.com/hpk42/muacrypt>`_

- `pyac code <https://github.com/juga0/pyac>`_ (uses `PGPy
  <https://pgpy.readthedocs.io>`_)

- `Bitmask/LEAP refactorings <https://0xacab.org/leap/bitmask-dev/merge_requests/55/diffs>`_

- `Go Autocrypt <https://github.com/autocrypt/go-autocrypt>`_

- `FairEmail code <https://github.com/M66B/FairEmail/>`_


Testing Autocrypt
+++++++++++++++++

There is an Autocrypt Bot which accepts and sends mails with Autocrypt
headers. Just write an E-Mail to bot@autocrypt.org. :doc:`Find out more about the bot...<bot>`
