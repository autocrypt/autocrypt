INBOME key discovery
=========================

.. contents::

Basic network protocol flow
---------------------------------

Establishing encryption happens as a side effect when people mail each other:

- An MUA will send an INBOME-Encryption-Info: header to all messages it
  sends out which contains encryption key info.

- An MUA which sends a mail to recipients where it earlier saw 
  respective INBOME Encryption Info headers will encrypt the message
  accordingly.


INBOME key discovery processing
-------------------------------

In order to better understand how MUAs process encryption info we talk about three different conceptual operations:

- ``process_incoming(mime_mail)``: analyze incoming mail and
  update local INBOME information.

- ``get_encrypt_key(recipient_address)``: Return encryption key or
  None for recipient_address.

- ``process_outgoing(mime_mail)``: Return new mime mail with
  headers and attachments added.

Note that these INBOME operations do not perform any encryption or
decryption but rather implement key discovery.


"Happy path" example: 1:1 communication
---------------------------------------

Consider a blank state and a first outgoing message from Alice to Bob::

    From: alice@a.example
    To: bob@b.example
    ...

``process_outgoing()`` will add an INBOME encryption info header::

    INBOME-Encryption-Info: keydata=<alice_encoded_encryption_key>

after which Alice's MUA sends the amended message out in cleartext.
Bob's INBOME implementation will in its ``process_incoming`` detect
the header and store the key for Alice.  

When Bob now composes a mail to Alice his MUA can obtain a key from ``get_encrypt_key('alice@a.example')`` and will signal the fact that it can encrypt to Alice in the composition screen.  Also, Bob's ``process_outgoing`` will provide his own encryption info because it has not yet seen an encrypted mail from Alice::

    INBOME-Encryption-Info: keydata=<bob_encoded_encryption_key>

When Alice's MUA ``process_incoming`` sees Bob's mail it keeps track both of Bob MUA's key and of the fact that it got an encrypted mail from Alice.

Subsequently both Alice and Bob will have their MUAs encrypt mails to each other without having to add an ``INBOME-Encryption-Info`` header.  

group (1:N) mail communication
------------------------------------------

If Alice sends mail to both Bob and Carol their MUAs will each see Alice's encryption key. If now Bob and Carol reply once, all MUAs have the other keys and everybody can then send encrypted mails to the others.  In other words, a MUA can only encrypt a mail towards multiple recipients if it previously got a message from each of its recipients which contained an encryption info.  

If Alice mailed to both Bob and Carol and only Bob answers (CCing Carol) then Bob and Alice can nevertheless encrypt to each other if they enter a 1:1 communication.

.. todo::

   If Alice already has Bob and Carol's encryption keys can we make Alice's MUA
   provide these keys of Bob and Carol in the initial encrypted group mail? 
   This would help keeping initial group conversations encrypted which is especially
   interesting if the group communication involves many more participants.

   Note that Alice can only have gotten Bob and Carol's keys if she saw a message
   from each of them.  Socially it's thus not likely that she will want to send a 
   message which claims wrong keys wrt to Bob and Carol.

Loosing access to decryption key
-------------------------------------------

If Alice looses access to her decryption secret:

- she lets her MUA generate a new key

- her MUA will add an Encryption-Info header containing the new key with each mail 

- receiving MUAs will replace the old key with the new key

Meanwhile, if Bob sends her a mail using the old encryption key she will have to respond with a message like "Sorry Bob, i've lost my device/key/... please write again".  This social mail exchange will lead to an updated key which works.

.. todo::

    Check if we can encrypt a mime mail such that non-decrypt-capable clients 
    will show a message that leads Alice to reply in the suggested way.  We don't
    want people to read handbooks before using INBOME so any guidance we can
    "automatically" provide in case of errors is good.

.. note::

    Unless we can get perfect recoverability (also for device loss etc.) we will
    always have to consider this "fatal" case of loosing a secret key and how
    users can deal with it.


switch to a MUA with no support for INBOME
-------------------------------------------

Alice might decide to switch to a different MUA which does not support INBOME.  

In this case a MUA which previously saw an INBOME header and/or encryption from Alice now sees an unencrypted mail from Alice and no encryption header. This will disable encryption to Alice for subsequent mails.


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


Known Open questions / notes 
-----------------------------

- Instead of transporting keysdata through INBOME headers we could
  also add attachments, e.g. application/pgp-keys ones and put INBOME
  headers into it.

- We don't currently address signatures at all -- how does INBOME
  interact with message signing?

- The actual encryption/signing mechanism are not defined by INBOME.
  For now we assume the practical implementation uses OpenPGP keys and
  either a separate or the default user's keyrings to store keys
  coming over INBOME.

- We can allow peers to gossip keys for all participating parties in an
  email conversation to speed up key discovery among them.  If a peer
  got two different keys for a target address (which can happen
  because of group gossiping and upgraded/regenerated keys) the peer
  shall encrypt to both keys if possible and request a key from the
  peer so that it can resolve the conflict.  FIXME: how are we
  encouraging key gossip in a group?

- We assume that an MUA only sends a key to a peer if the peer's last
  message indicated INBOME abilities/requests.  If a peer has sent a
  non INBOME mail, an MUA shall by default send a cleartext mail
  (unless explicitly requested by its user to continue sending
  encrypted).

- how does INBOME interact with today's mailing list managers?  This
  might not be relevant except for encrypted mailing lists.

- under what circumstances precisely do you downgrade from encryption
  to cleartext?  Could we consider the ``User-Agent`` header which
  often will indicate if the other side is using multiple
  devices/MUAs?  can we otherwise practically distinguish different
  MUAs from parsing messages/headers?  There's an ongoing push to drop
  User-Agent headers from most MUAs, in an attempt to minimize
  published metadata, so relying on User-Agent isn't a reasonable
  approach.  However, each MUA could select and publish a UUID as part
  of its INBOME header, if we find it's important for one peer to know
  when the other is using multiple clients.

- how to deal with spammers downgrade encryption by using a fake from?
  (it's not their intention, just a side effect).  How much can we
  rely on DKIM?

