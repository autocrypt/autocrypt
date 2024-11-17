Autocrypt-capable MUAs level 1 implementation status
====================================================

Last updated: ``2024-11-17``

Note that the below table is not complete and not up-to-date.
Many more mail user agents support at least a subset of Autocrypt.

You are very welcome to submit a PR to update the below information, thanks!


+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|*MUA/project*                         |*header |*keygen*|*peer |*header|*recommend*|*encrypt*|*setup  |*setup  |*gossip*|*uid       |
|                                      |parsing*|        |state*|inject*|           |         |message*|process*|        |decorative*|
|                                      |        |        |      |       |           |         |        |        |        |           |
+======================================+========+========+======+=======+===========+=========+========+========+========+===========+
|.. image:: images/logos/deltachat.png |✔       |✔       |✔     |✔      |✔          |✔        |✔       |✔       |✔       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`delta.chat`_                         |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/evo.png       |✔       |✘       |✘     |✔      |✘          |✔        |✘       |✘       |✘       |✘          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`evolution`_                          |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/tbird.png     |✔       |✔       |✘     |✔      |✔          |✔        |✘       |✘       |✔       |✘          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`thunderbird`_                        |        |        |      |       |           |         |        |        |        |           |
+--------------------------------------+--------+--------+------+-------+-----------+---------+--------+--------+--------+-----------+
|.. image:: images/logos/k9.png        |✔       |✔       |✔     |✔      |✔          |✔        |branch  |branch  |✔       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`K-9 Mail`_                           |        |        |      |       |           |         |        |        |        |           |
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
|.. image:: images/logos/lttrs.png     |✔       |✔       |✔     |✔      |✔          |✔        |✔       |✔       |✘       |✔          |
|                                      |        |        |      |       |           |         |        |        |        |           |
|`Ltt.rs`_                             |        |        |      |       |           |         |        |        |        |           |
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

_ ``gossip``: sends out Autocrypt-Gossip headers

- ``uid decorative``: UID in key data is only used for decorative
  purposes, and in particular not for looking up keys for an e-mail address.

.. _delta.chat: https://delta.chat/
.. _evolution: https://gitlab.gnome.org/GNOME/evolution/-/wikis/home
.. _thunderbird: https://www.thunderbird.net/
.. _K-9 Mail: https://k9mail.github.io/
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
.. _Ltt.rs: https://ltt.rs

For developers
--------------

Source code:

- `K9 code <https://github.com/k9mail/k-9>`_

- `Delta.Chat code <https://github.com/deltachat/>`_

- `Mutt code <https://gitlab.com/muttmua/mutt>`_

- `Neomutt code <https://github.com/neomutt/neomutt>`_

- `Letterbox code <https://git.imp.fu-berlin.de/enzevalos>`_

- Notmuch/Alot: TODO

- `FairEmail code <https://github.com/M66B/FairEmail/>`_


