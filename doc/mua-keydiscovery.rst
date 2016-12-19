Autocrypt in-band key discovery
=============================

Autocrypt key discovery requires support only from mail programs and works with any existing mail provider, it works fully offline and is only based on the two core abilities every mail program has: sending and receiving mail.

Similar to TLS's machine to machine handshake, users first need to have a cleartext mail exchange to negotiate encryption.  Autocrypt-supporting MUAs add encryption key information to every mail they send out.  Subsequent mails from the receiving peer will then be encrypted. Mail programs signal encryption-status to their users at "compose-mail" time but avoid asking for decisions about keys. In fact, key exporting, importing and upgrading all happens automatically and without user intervention. In accordance with :rfc:`7435` Autocrypt is fine with dropping back to cleartext in some cases (see below).

Autocrypt key discovery is safe only against passive eavesdroppers. It is trivial for providers to perform active downgrade or man-in-the-middle attacks on Autocrypt's key discovery.  Users may, however, detect such tampering if they out-of-band verify their keys at some later point in time.  This possiblity in turn is likely to keep most providers honest or at least prevent them from performing active attacks on a massive scale.


.. contents::

Basic network protocol flow
---------------------------------

Establishing encryption happens as a side effect when people send each other mail:

- A MUA always adds an ``Autocrypt-Encryption:`` header to all messages it
  sends out.

- A MUA will scan incoming mails for encryption headers and associate
  the info with a canonicalized version of the ``From:`` address contained
  in the :rfc:`822` message.

- A MUA will encrypt a message if it earlier saw encryption keys for all
  recipients.

Autocrypt does not prescribe or describe encryption algorithms or key formats.  It is meant to work nicely with ordinary PGP keys, however.

Header Format
-------------

The ``Autocrypt-Encryption:`` header MUST have the following format:
```
Autocrypt-ENCRYPTION: to=aaa@bbb.cc; [type=(p|...);] [prefer-encrypted=(yes|no);] key=BASE64
```

Where key includes a Base64 representation of a minimal key. For now we only support 'p' as the type, which represents a specific subset of OpenPGP (see key-formats.rst).
'prefer-encrypted' indicates that agents should default to encrypting when composing emails.
Autocrypt compatible Agents MUST include one header with a key in a Autocrypt compatible format.

"Happy path" example: 1:1 communication
---------------------------------------

Consider a blank state and a first outgoing message from Alice to Bob::

    From: alice@a.example
    To: bob@b.example
    ...

Upon sending this mail, Alice's MUA will add a header which contains her
encryption key::

    Autocrypt-Encryption: to=alice@a.example; type=p; prefer-encrypted=yes; key=...

Bob's MUA will scan the incoming mail, find Alice's key and store it associated
to the ``alice@a.example`` address taken from the ``to``-attribute.
When Bob now composes a mail to Alice his MUA will find the key and signal to
Bob that the mail will be encrypted and after finalization of the mail encrypt
it.
Moreover, Bob's MUA will add its own Encryption Info::

    Autocrypt-Encryption: to=bob@b.example; type=p; prefer-encrypted=yes; key=...

When Alice's MUA now scans the incoming mail from Bob it will store
Bob's key and the fact that Bob sent an encrypted mail.  Subsequently
both Alice and Bob will have their MUAs encrypt mails to each other.

If ``prefer-encrypted`` is sent as 'yes' the MUA MUST default to encrypting
the next email. If it is set as 'no' the MUA MUST default to plaintext.
If ``prefer-encrypted`` is not sent the MUA should stick to what it was doing
before. If the attribute has never been sent it's up to the MUA to decide. The
save way to go about it is to default to plaintext to make sure the recipient
can read the email.

We encourage MUA developers to propose heuristics for handling the undirected
case. We will document the best approaches to develop a shared understanding.

group mail communication (1:N)
------------------------------------------

Consider a blank state and a first outgoing message from Alice to Bob
and Carol.  Alice's MUA add a header just like in the 1:1 case so
that Bob and Carol's MUA will learn Alice's key.  After Bob and Carol
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


Loosing access to decryption key
-------------------------------------------

If Alice loses access to her decryption secret:

- she lets her MUA generate a new key

- her MUA will add an Encryption-Info header containing the new key with each mail

- receiving MUAs will replace the old key with the new key

Meanwhile, if Bob sends Alice a mail encrypted to the old key she will
not be able tor ead it.  After she responds (e.g. with "Hey, can't read
your mail") Bob's MUA will see the new key and subsequently use it.

.. todo::

    Check if we can encrypt a mime mail such that non-decrypt-capable clients
    will show a message that helps Alice to reply in the suggested way.  We don't
    want people to read handbooks before using Autocrypt so any guidance we can
    "automatically" provide in case of errors is good.

.. note::

    Unless we can get perfect recoverability (also for device loss etc.) we will
    always have to consider this "fatal" case of loosing a secret key and how
    users can deal with it.  Especially in the federated email context We do
    not think perfect recoverability is feasible.


Dowgrading / switch to a MUA without Autocrypt support
------------------------------------------------------

Alice might decide to switch to a different MUA which does not support Autocrypt.

A MUA which previously saw an Autocrypt header and/or encryption from Alice
now sees an unencrypted mail from Alice and no encryption header. This
will disable encryption to Alice for subsequent mails.


A note on Autocrypt and existing spam infrastructure
----------------------------------------------------------

Mike Hearn raised some fundamental concerns in his `Modern anti-spam
and E2E crypto post on the modern crypto mailing list
<https://moderncrypto.org/mail-archive/messaging/2014/000780.html>`_
on how end-to-end encrypted mails and spam infrastructure possibly
interfere.  While it's conceivable to imagine new ways to fight spam
in an E2E setting by increased DKIM usage and additional measures and
policies the topic is a serious one as adoption of more encrypted
mails could be seriously hampered if encryption can bypass current
anti-spam technology.

Autocrypt works well with existing provider Anti-Spam infrastructures
because they can continue to check the initial cleartext mails for
suspicious content. Only if a user replies to a (likely non-spam) mail
will Autocrypt make a MUA send an encryption key.  Without being able to
get sufficiently many replies from users it will likely be to
massively harvest encryption keys; there is no central registery for
key-mail address relations.  Massive collection of key/mailaddress
associations would require co-operation from or compromise of big mail
providers which is unlikely given they have been fighting unsolicited
mails for decades and their business models depend on it. But even if
a user's encryption key becomes public the worst outcome are increased
numbers of unsoliticed mails arriving at the MUA side. Upgrading to a
new key can mitigate the problem and is supported by Autocrypt.


