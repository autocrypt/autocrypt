Example Data Flows and State Transitions
========================================


Autocrypt key discovery happens through headers of mail messages sent
between mail apps. Similar to TLS's machine to machine handshake,
users first need to have a cleartext mail exchange.  Subsequent mails
from the receiving peer may then be encrypted.  Mail apps show
encryptability to their users at "compose-mail" time and give them a
choice of encryption or cleartext, defaulting to what the other side
has specified in their header.

These examples try to walk a new reader through the basic flow.
For example headers, see also :ref:`Level1 spec header examples <example-headers>`.

.. contents::


Basic network protocol flow
---------------------------

Establishing encryption happens as a side effect when people send each other mail:

- A MUA (mail user agent) adds an ``Autocrypt:``
  header to all messages it sends out.  The header
  contains all necessary information to allow encryption
  (especially the encryption key; see :ref:`autocryptheaderformat` for
  the format in detail).

- A MUA will scan incoming mails for encryption headers and associate
  the info with a canonicalized version of the ``From:``
  address contained in the :rfc:`822` message.

- A MUA will encrypt a message if it has encryption keys
  for all recipients and it determined through user choice or
  recipient-determined policies that the message should be encrypted.


.. _mua-happypath:

"Happy path" example: 1:1 communication
---------------------------------------

.. image:: ./images/autocrypthappy.*

Consider a blank state and a first outgoing message from Alice to Bob::

    From: alice@a.example
    To: bob@b.example
    ...

Upon sending this mail, Alice's MUA will add a header which contains her
encryption key::

    Autocrypt: addr=alice@a.example; prefer-encrypt=mutual; keydata=...

Bob's MUA will scan the incoming mail, find Alice's key and store it
associated to the ``alice@a.example`` address taken from the
``addr``-attribute.  When Bob now composes a mail to Alice his MUA will
find the key and signal to Bob that the mail will be encrypted and
after finalization of the mail encrypt it.  Moreover, Bob's MUA will
add its own encryption info::

    Autocrypt: addr=bob@b.example; prefer-encrypt=mutual; keydata=...

When Alice's MUA now scans the incoming mail from Bob it will store
Bob's key and the fact that Bob sent an encrypted mail.  Subsequently
both Alice and Bob will have their MUAs encrypt mails to each other.

If ``prefer-encrypted`` is sent as ``mutual`` and this is also the choice set for the MUA,
the MUA MUST default to encrypting the next e-mail.  In all other cases, the MUA MUST
default to plaintext to make sure the recipient can read the e-mail.



Group mail communication (1:N)
------------------------------

Consider a blank state and a first outgoing message from Alice to Bob
and Carol.  Alice's MUA adds a header just like in the 1:1 case so
that Bob's and Carol's MUAs will learn Alice's key.  

If Bob and Carol have not exchanged E-Mails yet, they can only encrypt to her,
but not to each other.  To enable them to answer encrypted to everyone, Alice
includes an extra header for each recipient, the ``Autocrypt-Gossip:`` header,
which propagates their keys to every other recipient.  This way, Bob and Carol
can immediately engage in the encrypted group conversation, even if they didn't
know each other before.

Gossip is a bit less trustworthy than a 1:1 Autocrypt key exchange; an attacker
could use it to spread wrong keys of other people. That's why ``Autocrypt:``
headers are always preferred to the Gossip-Headers.

Because Autocrypt is about **opportunistic** encryption, you still have
this opportunity of propagating the keys of others to facilitate group
communication.  Other security measures like fingerprint verification can
follow on top.

Losing access to decryption key
-------------------------------

If Alice loses access to her decryption secret:

- she lets her MUA generate a new key

- her MUA will add an :mailheader:`Autocrypt` header containing the
  new key with each mail

- receiving MUAs will replace the old key with the new key

Meanwhile, if Bob sends Alice a mail encrypted to the old key she will
not be able to read it.  After she responds (e.g. with "Hey, can't read
your mail") Bob's MUA will see the new key and subsequently use it.

.. todo::

    Check if we can encrypt a MIME e-mail such that non-decrypt-capable MUAs
    will show a message that helps Alice to reply in the suggested way.  We don't
    want people to read handbooks before using Autocrypt so any guidance we can
    "automatically" provide in case of errors is good.

.. note::

    Unless we can get perfect recoverability (also for device loss etc.) we will
    always have to consider this "fatal" case of losing a secret key and how
    users can deal with it.  Especially in the federated e-mail context we do
    not think perfect recoverability is feasible.


Downgrading / switch to a MUA without Autocrypt support
-------------------------------------------------------

Alice might decide to switch to a different MUA which does not support
Autocrypt.

A MUA which previously saw an :mailheader:`Autocrypt` header and/or
encryption from Alice now sees an unencrypted mail from Alice and no
:mailheader:`Autocrypt` header. This will disable encryption to Alice
for subsequent mails.

Autocrypt relies on non-Autocrypt-capable MUAs to act as a sort of
"reset" for the user in the case where they stop using Autocrypt.
