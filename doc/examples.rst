Example Data Flows and State Transitions
========================================


Autocrypt key discovery happens through headers of mail messages sent
between mail apps. Similar to TLS's machine to machine handshake,
users first need to have a cleartext mail exchange.  Subsequent mails
from the receiving peer will may then be encrypted.  Mail apps show
encryptability to their users at "compose-mail" time and give them a
choice of encryption or cleartext, defaulting to what the other side
has specified in their header.

These examples try to walk a new reader through the basic flow.

.. note::

   Autocrypt key discovery is safe only against passive
   eavesdroppers. It is trivial for providers to perform active
   downgrade or man-in-the-middle attacks on Autocrypt's key
   discovery.  Users may, however, detect such tampering if they
   verify their keys out-of-band at some later point in time.  We hope
   this possibility will keep most providers honest or at least
   prevent them from performing active attacks on a massive scale.

Please also see https://github.com/autocrypt/autocrypt/tree/master/src/tests/data
for specific examples of Autocrypt messages.

.. contents::


Basic network protocol flow
---------------------------

Establishing encryption happens as a side effect when people send each other mail:

- A MUA (mail user agent) always adds an ``Autocrypt:`` header to all messages it
  sends out.

  The autocrypt header contains all necessary information to allow encryption
  (especially the key; see :ref:`autocryptheaderformat` for the format in detail).

- A MUA will scan incoming mails for encryption headers and associate
  the info with a canonicalized version of the ``From:`` address contained
  in the :rfc:`822` message.

- A MUA will encrypt a message if it earlier saw encryption keys
  (and the request to encrypt) for all recipients.


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

    Autocrypt: to=alice@a.example; type=p; prefer-encrypted=yes; key=...

Bob's MUA will scan the incoming mail, find Alice's key and store it associated
to the ``alice@a.example`` address taken from the ``to``-attribute.
When Bob now composes a mail to Alice his MUA will find the key and signal to
Bob that the mail will be encrypted and after finalization of the mail encrypt
it.  Moreover, Bob's MUA will add its own Encryption Info::

    Autocrypt: to=bob@b.example; type=p; prefer-encrypted=yes; key=...

When Alice's MUA now scans the incoming mail from Bob it will store
Bob's key and the fact that Bob sent an encrypted mail.  Subsequently
both Alice and Bob will have their MUAs encrypt mails to each other.

If ``prefer-encrypted`` is sent as 'yes' the MUA MUST default to encrypting
the next e-mail. If it is set as 'no' the MUA MUST default to plaintext.
If ``prefer-encrypted`` is not sent the MUA should stick to what it was doing
before. If the attribute has never been sent it's up to the MUA to decide. The
safe way to go about it is to default to plaintext to make sure the recipient
can read the e-mail.

We encourage MUA developers to propose heuristics for handling the undirected
case. We will document the best approaches to develop a shared understanding.


Group mail communication (1:N)
------------------------------

Consider a blank state and a first outgoing message from Alice to Bob
and Carol.  Alice's MUA adds a header just like in the 1:1 case so
that Bob's and Carol's MUAs will learn Alice's key.  After Bob and Carol
have each replied once, all MUAs will have appropriate keys for
encrypting the group communication.

It is possible that an encrypted mail is replied to in cleartext (unencrypted).
For example, consider this mail flow::

    Alice -> Bob, Carol
    Bob -> Alice, Carol
    Carol -> Alice  (not to Bob!)

Alice and Carol have now all encryption keys but Bob only has Alice's
because he never saw a mail from Carol.  Alice can now send an encrypted
mail to Bob and Carol but Bub will not be able to respond encrypted
before his MUA has seen a mail from Carol.  This is fine because Autocrypt
is about **opportunistic** encryption, i.e. encrypt if possible and
otherwise don't get in the way of users.


Losing access to decryption key
-------------------------------

If Alice loses access to her decryption secret:

- she lets her MUA generate a new key

- her MUA will add an Encryption-Info header containing the new key with each mail

- receiving MUAs will replace the old key with the new key

Meanwhile, if Bob sends Alice a mail encrypted to the old key she will
not be able to read it.  After she responds (e.g. with "Hey, can't read
your mail") Bob's MUA will see the new key and subsequently use it.

.. todo::

    Check if we can encrypt a mime mail such that non-decrypt-capable clients
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

Alice might decide to switch to a different MUA which does not support Autocrypt.

A MUA which previously saw an Autocrypt header and/or encryption from Alice
now sees an unencrypted mail from Alice and no encryption header. This
will disable encryption to Alice for subsequent mails.
