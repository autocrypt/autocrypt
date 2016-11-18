INBOME in-band key discovery
=============================

INBOME key discovery requires support only from mail programs and works with any existing provider, it works fully offline and is only based on the two core abilities every mail program has: sending and receiving mail.

Similar to TLS's machine to machine handshake, users first need to have a cleartext mail exchange to negotiate encryption.  INBOME-supporting MUAs add encryption key information to every mail they send out.  Subsequent mails from the receiving peer will then be encrypted. Mail programs signal encryption-status to their users at "compose-mail" time but avoid asking for decisions about keys. In fact, key exporting, importing and upgrading all happens automatically and without user intervention. In accordance with :rfc:`7435` INBOME is fine with dropping back to cleartext in some cases (see below).

INBOME key discovery is safe only against passive eavesdroppers. It is trivial for providers to perform active downgrade or man-in-the-middle attacks on INBOME's key discovery.  Users may, however, detect such tampering if they out-of-band verify their keys at some later point in time.  This possiblity in turn is likely to keep most providers honest or at least prevent them from performing active attacks on a massive scale.


.. contents::

Basic network protocol flow
---------------------------------

Establishing encryption happens as a side effect when people send each other mail:

- A MUA always adds an ``INBOME-Encryption:`` header to all messages it
  sends out.

- A MUA will scan incoming mails for encryption headers and associate
  the info with a canonicalized version of the ``From:`` address contained
  in the rfc822 message.

- A MUA will encrypt a message if it earlier saw encryption keys for all
  recipients.

INBOME does not prescribe or describe encryption algorithms or key formats.  It is meant to work nicely with ordinary PGP keys, however.

"Happy path" example: 1:1 communication
---------------------------------------

Consider a blank state and a first outgoing message from Alice to Bob::

    From: alice@a.example
    To: bob@b.example
    ...

Upon sending this mail, Alice's MUA will add a header which contains her
encryption key::

    INBOME-Encryption: keydata=<alice_encoded_encryption_key>

Bob's MUA will scan the incoming mail, find Alice's key and store it
associated to the ``alice@a.example`` address.  When Bob now composes a
mail to Alice his MUA will find the key and signal to Bob that the mail
will be encrypted and after finalization of the mail encrypt it.
Moreover, Bob's MUA will add its own Encryption Info::

    INBOME-Encryption: keydata=<bob_encoded_encryption_key>

When Alice's MUA now scans the incoming mail from Bob it will store
Bob's key and the fact that Bob sent an encrypted mail.  Subsequently
both Alice and Bob will have their MUAs encrypt mails to each other.


group (1:N) mail communication
------------------------------------------

Consider a blank state and a first outgoing message from Alice to Bob
and Carol.  Alice's MUA will add a header just like in the 1:1 case so
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
before his MUA has seen a mail from Carol.  This is fine because INBOME
is about **opportunistic** encryption, i.e. encrypt if possible and
otherwise don't get in the way of users.

Loosing access to decryption key
-------------------------------------------

If Alice looses access to her decryption secret:

- she lets her MUA generate a new key

- her MUA will add an Encryption-Info header containing the new key with each mail 

- receiving MUAs will replace the old key with the new key

Meanwhile, if Bob sends Alice a mail encrypted to the old key she will
not be able tor ead it.  After she responds (e.g. with "Hey, can't read
your mail") Bob's MUA will see the new key and subsequently use it.

.. todo::

    Check if we can encrypt a mime mail such that non-decrypt-capable clients 
    will show a message that helps Alice to reply in the suggested way.  We don't
    want people to read handbooks before using INBOME so any guidance we can
    "automatically" provide in case of errors is good.

.. note::

    Unless we can get perfect recoverability (also for device loss etc.) we will
    always have to consider this "fatal" case of loosing a secret key and how
    users can deal with it.  Especially in the federated email context We do 
    not think perfect recoverability is feasible.


Dowgrading / switch to a MUA without INBOME support
------------------------------------------------------

Alice might decide to switch to a different MUA which does not support INBOME.  

A MUA which previously saw an INBOME header and/or encryption from Alice
now sees an unencrypted mail from Alice and no encryption header. This
will disable encryption to Alice for subsequent mails.


A note on INBOME and existing spam infrastructure
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

INBOME works well with existing provider Anti-Spam infrastructures
because they can continue to check the initial cleartext mails for
suspicious content. Only if a user replies to a (likely non-spam) mail
will INBOME make a MUA send an encryption key.  Without being able to
get sufficiently many replies from users it will likely be to
massively harvest encryption keys; there is no central registery for
key-mail address relations.  Massive collection of key/mailaddress
associations would require co-operation from or compromise of big mail
providers which is unlikely given they have been fighting unsolicited
mails for decades and their business models depend on it. But even if
a user's encryption key becomes public the worst outcome are increased
numbers of unsoliticed mails arriving at the MUA side. Upgrading to a
new key can mitigate the problem and is supported by INBOME.


