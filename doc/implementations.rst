Autocrypt-capable MUAs level 1 implementation status
=====================================================

Last updated: ``2017/11/03``

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

Leyend: TBD

.. [1] require passphrase
.. [2] always send

.. _delta-chat: https://delta.chat
.. _k9: https://k9mail.github.io/
.. _enigmail: https://www.enigmail.net
.. _py-autocrypt: https://py-autocrypt.readthedocs.io/
.. _notmuch: https://notmuchmail.org/
.. _mailpile: https://www.mailpile.is/
