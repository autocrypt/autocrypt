Future Enhancements to Autocrypt
================================

Please see :doc:`level0` for information about Level 0 requirements.
Here, we document future improvements, which we hope will be
incorporated in Level 1, or possibly some later Level.  This is an
unordered list.  If you have ideas about how to address one of these
points, feel free to jump in!  (but let's try to stay focused on
getting Level 0 stable before we invest too much energy in these next
steps)

.. contents::

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
   specified).  When we support types other than `0`, it's possible
   that users will have multiple keys available, each with a different
   type.  That seems likely to introduce some awkward choices during
   message composition time, particularly for multi-recipient
   messages.

X.509 and S/MIME
++++++++++++++++

.. todo::

   Someone is bound to ask for this as a "key type"


Deletable ("forward secure") encrypted mail
+++++++++++++++++++++++++++++++++++++++++++

.. todo::

   Given the Autocrypt infrastructure for key exchange, there's no
   reason we couldn't define a mechanism for pairwise, ratcheted,
   session-key establishment for e-mail.

RSA2048 to Curve 25519
----------------------

.. todo::

   Document change in preference for keys from RSA 2048 to Curve 25519.


Backups
-------

see :doc:`backup`

.. todo::

   We need guidance on how backups might be done safely.


Guidance on masking Key IDs
---------------------------

If any recipients are in :mailheader:`Bcc:` (rather than
:mailheader:`To:` or :mailheader:`Cc:`), and the key types used are
all OpenPGP (``type=0``), then the agent SHOULD mask the recipient key
ID in the generated PKESK packets that correspond to the Bcc'ed
recipents.  It does not need to mask recipient key IDs of normal
recipients.

Masking of Key IDs is done by setting the key ID to all-zeros.  See
the end of :rfc:`section 5.1 RFC 4880<4880#section-5.1>` for more
details.  Users of GnuPG can use the ``--hidden-recipient`` argument to
indicate a recipient who will be masked.

This is so that the message encryption does not leak much additional
metadata beyond what is already found in the headers of the message.
It still leaks the number of additional recipients, but the additional
work and usability issues involved with fixing that metadata leak
suggest that it's better to leave that to a future level.


Encrypted headers
-----------------

.. todo::

   Document interaction with encrypted headers: if something like
   `Memory Hole <http://modernpgp.org/memoryhole/>`_ ever makes it
   possible to hide normal :mailheader:`To:` and :mailheader:`Cc:`
   headers, then we need to rethink our approach to handling PKESK
   leakage further.


Webmail
-------

.. todo::

   How does Autocrypt interact with webmail?  Can we describe hooks
   for webmail and browser extensions that make sense?

Search
------

.. todo::

   Guidance for implementers on dealing with searching a mailbox that
   has both cleartext and encrypted messages. (session key caching,
   etc)

Gossip (or "introduction e-mails")
----------------------------------

.. todo::

   Can we specify a sensible practice for passing around keys for
   other people that we know about?

   Or maybe it'd be simpler to define a standard workflow for
   "introduction e-mails", where the sender tells multiple recipients
   about the keys she has for all of them.

Out-of-band key verification
----------------------------

.. todo::

   Can we specify a simple, user-friendly way that Autocrypt users can
   confirm each others' "Autocrypt info" out of band?

   If we do specify such a thing, what additional UI/UX would be
   required?


Heuristics for dealing with "nopreference"
------------------------------------------

.. todo::

   in Level 0, the Autocrypt recommendations for composing mail to a
   remote peer with ``prefer-encrypted`` set to ``nopreference`` look
   very much the same as the recommendations for when
   ``prefer-encrypted`` is set to ``no``.  But different heuristics
   could be applied to the ``nopreference`` case for MUAs that want to
   help users be slightly more aggressive about sending encrypted
   mail.

   Documenting reasonable heuristics for MUAs to use in this case
   would be very helpful.
