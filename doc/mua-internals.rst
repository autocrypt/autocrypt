MUA internals (requirements, operations, state)
===============================================

.. contents::


INBOME requirements for MUAs
---------------------------------------------------

INBOME works for people who use INBOME-aware MUAs.  We expect the MUAs
to have the following capabilities:

- know what account(s) they are associated with, including the
  public-facing e-mail address associated with each account.

- be able to fetch e-mail from the corresponding accounts

- send e-mail to arbitrary e-mail addresses (including its own
  account(s)).

- If the MUA can check multiple e-mail accounts, it should be able to
  distinguish somehow between mail delivered to each of those
  accounts.  That is, if the MUA checks the mailbox for
  ``bob@home.example`` and also for ``robert@work.example``, it should
  know which messages came for which address.  (Inspecting headers may
  be sufficient for this).  This is necessary because some messages
  that affect the state of an INBOME peering don't bear INBOME headers
  at all (e.g. messages from new, non-INBOME-capable MUAs)

- be able to store persistent state about the user's communications
  partners (see peerstate_) and about the user's other devices (see
  :doc:`multi-device`)

.. _peerstate:

Per-peer state
--------------

For each peer, an INBOME-aware MUA will store the timestamp and value of the ``INBOME-Encryption`` header value it saw from the last message from that peer.  

Peers are distingished by canonicalized e-mail address.  If an MUA has
an address book, it is likely to separate contacts by human identity,
and each identity might have multiple e-mail addresses.
However, INBOME-enabled MUAs treat separate e-mail addresses (even when we know
they belong to the same person) as distinct for the purposes of
storing state.

core operations 
------------------

For the time being, INBOME mandates that clients always add an ``INBOME-Encryption`` header. This makes it trivial for MUAs which receive mails to determine if the other side supports INBOME or not.

In order to better understand how MUAs process and use this encryption info we talk about two conceptual core operations:

- ``scan_incoming(mime_mail)``: update local INBOME state from incoming
  mail.

- ``get_encrypt_key(recipient_address)``: Return encryption key or
  None for recipient_address.

The ``scan_incoming`` function sees the full incoming :rfc:`822` message.  It will not neccessarily see messages in the order in which they were sent.  In order to keep track of the "latest" mail from a peer it will associate a timestamp with each message.  This is computed from the Date header or, if that lies in the future, is taken to be the current time. ``scan_incoming`` will update a peer's inbome info in either one of these cases:

- it never saw an earlier mail from that peer
- it saw a mail earlier but it's recorded timestamp preceded the current timestamp

The ``get_encrypt_key`` function will return an encryption key it scanned from an earlier mail if and only if the last mail from the peer contained that info.

State will be stored and queried using `address canonicalization`_.



.. _`address canonicalization`:

E-mail Address canonicalization
-------------------------------

Domain part (the part after the @):

FIXME: We need to choose a canonicalization form for the domain side
of the e-mail address.  There are risks for user presentation around
phishing with IDNs, which we should be careful about.


Local part (the part before the @):

SMTP specs say this part is domain-specific, and byte-for-byte
arbitrarily sensitive.  In practice, nearly every e-mail domain treats
the local part of the address as a case-insensitive string.  That is,
while it is permitted by the standards, ``John@example.org`` is very
unlikely to deliver to a different mailbox than ``john@example.org``.
INBOME-aware MUAs will canonicalize the local part of an e-mail
address by making it all lower-case.

FIXME: some people (and some e-mail domains) have known variations
which all deliver to the same account.  For example, the mailbox that
receives ``john@example.org`` might automatically receive all mail
addressed like ``john-whatever@example.org``.  gmail today supports
arbitrary dot injection (e.g. ``johndoe@example.org`` delivers to the
same mailbox as ``john.doe@example.org``).  Do we want to try to
support these somehow?  It would be simplest to declare anyone using
aliasing schemes like this as out-of-scope for INBOMEv1.

FIXME: do we want to allow sophisticated users to explicitly merge
known shared aliases as long as the domain side stays the same?  For
example, if i happen to know that ``jdoe@example.org`` delivers to the
same mailbox as ``john@example.org``, can i declare that to an
INBOME-aware MUA?  How would such an explicit merge affect state
management?
