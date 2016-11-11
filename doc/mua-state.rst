Internal state for MUA
======================

.. contents::


INBOME assumes that every communicating MUA has some structured
internal state about the peers that the user communicates with.

It may also need to store state about other MUAs used by the same
user, but that state will be documented in multi-device.rst

Multi-account MUAs
------------------

Some MUAs are capable of working with multiple e-mail accounts.

Per-peer state
--------------

Peers are distingished by canonicalized e-mail address.  If an MUA has
an address book, it is likely to separate contacts by human identity,
and each identity might have multiple e-mail addresses.
INBOME-enabled MUAs treat separate e-mail addresses (even when we know
they belong to the same person) as distinct for the purposes of
storing state.

FIXME: this is a draft -- we might not need all this state, and we
might need more.

For each peer, an INBOME-aware MUA will store:

- timestamp of most recent INBOME request: header received from peer

- most recent INBOME provide: header received from peer
  - timestamp of most recent receipt
  - number of times this exact header was received from this peer
  - timestamp of first receipt of this exact header

- most recent INBOME provide: header sent 
  - timestamp of most recent send
  - number of times this exact header was sent to this peer
  - timestamp of first send of this exact header

- timestamp of most recent mail received from peer

- timestamp of most recent mail sent to peer

FIXME: do we need to distinguish between one-to-one e-mail and
one-to-many e-mail?  for example, if Alice has an INBOME connection to
Bob such that all mails are encrypted, and then Bob sends Alice and
Carol a cleartext message, should that reset the state?

FIXME: how do we deal with Bcc'ed e-mail?

API implementation
------------------

FIXME: docuemnt how to implement the three-function API based on this
state?

what should ``process_incoming()`` do if it receives an INBOME request
but the requested address is not "our" address?


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
