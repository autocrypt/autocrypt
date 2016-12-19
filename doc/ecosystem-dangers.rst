Potential ecosystem dangers of Autocrypt
========================================

This document is a place to describe particular concerns that Autocrypt
creates for the e-mail ecosystem as a whole.  It does not address
attacks against the cryptography or compromises to the message
confidentiality it aims to support.

These risks may not be large risks, or they may be mitigatable in some
way, but we document them here for general awareness.

In all, we currently believe that the benefits to the ecosystem of
having more end-to-end message confidentiality outweigh these
potential risks.


Failures of Search
------------------

If Autocrypt clients are incapable of searching encrypted mail, users of
Autocrypt-capable clients may find e-mail less useful for normal
communication.

Message Deliverability
----------------------

Autocrypt headers that use RSA 2048 are large enough that, when
unwrapped, they exceed the SMTP line length limit of 1000 ASCII
characters.

It's conceivable that some MTAs or MUAs will choke upon trying to deal
with these headers, and render the message undeliverable or
unreadable.  We have no evidence of this happening today (December
2016), but maybe we're just not yet tickling the systems that have
these problems.

Possible mitigations:

  - sending duplicate headers each with parts of the key data.  But
    this makes reassembly and message-parsing logic significantly more
    complex, and it would be nice to not need it.


Denial of Service: malicious creation of unreadable mail
--------------------------------------------------------

An active attacker who wants to interrupt communication between two
parties can do so if they know that one party uses an Autocrypt-capable
agent.  Consider the case where Mallory wants to interrupt
communications between Alice and Bob, and she knows that Bob uses an
Autocrypt-capable client.

Mallory crafts a new key K.  She can throw away the secret key
material entirely if she wants to.  She then forges an e-mail from
Alice and adds an Autocrypt header to it containing that public key and
`prefer-encrypted=yes`.  If Bob writes a message to Alice after
receiving that key, and before receiving any other legitimate message
to Alice, his message will be encrypted to a key that Alice cannot
read.

this represents a risk to Alice, even if she has never adopted an
Autocrypt-capable client in the first place.

Mitigations:

 - Alice's next mail to Bob will correct Bob's client's state so that
   futre mails will be back to Alice's actualy preferred state.  So
   the attacker must sustain a series of forgeries if the denial of
   service attack is intended to be sustained.

 - we should specify that any spam/malware flag set from a filter that
   the user trusts should be sufficient to discourage processing of
   Autocrypt headers, so that Mallory needs to craft a
   sufficiently-plausible message (including DKIM and whatever other
   indicators the filters care about) to make it into the
   Autocrypt-capable agent's internal state storage.

Killing off strong encryption
-----------------------------

Autocrypt is significantly weaker than traditional models of mail
encryption.  In particular, it provides no resistance to an active
attacker (an attacker who can modify and/or inject mail as it passes
through the SMTP network).  The no-UI feature makes it so that most
users will never properly verify each other's encryption keys.

There is a concern that if opportunistically-encrypted mail becomes
the standard, no one will bother to implement good UX for users in strong
identity verification.
