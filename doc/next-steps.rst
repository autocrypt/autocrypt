Future Enhancements to Autocrypt
================================

Please see :doc:`level0` for information about Level 0 requirements.
Here, we document future improvements, which we hope will be
incorporated in Level 1, or possibly some later Level.



Expiry
------

.. todo::

   We need documentation about sensible key expiry
   policies. Autocrypt-capable clients that choose to have an expiry
   policy on their secret key material should use message composition
   as an opportunity to refresh their secret key material or update
   the expiration dates in their public certificate.

   
Client sync
-----------

Please see :doc:`peering`

.. todo::

   We need to specify how to sync internal Autocrypt state between
   clients.  We want to be able to sync the state without sending sync
   data for every message processed, while we also want all synced
   peers to have the same internal state as much as possible.  We
   currently believe that syncing updates to ``pah`` and ``changed``
   should be sufficient, and that peers do not need to sync
   ``last_seen``.  This has not been proved in practice.

New Types
---------
   
.. todo::

   how to deal with multiple types (at least when a new type is
   specified).  When we support types other than `p`, it's possible
   that users will have multiple keys available, each with a different
   type.  That seems likely to introduce some awkward choices during
   message composition time, particularly for multi-recipient
   messages.


RSA2048 to Curve 25519
----------------------

.. todo::

   Document change in preference for keys from RSA 2048 to Curve 25519.


Backups
-------

see :doc:`backup`

.. todo::

   We need guidance on how backups might be done safely.
