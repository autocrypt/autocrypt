INBOME key discovery
----------------------------

Basic protocol flow
---------------------------------

Establishing encryption is reminiscent of TLS/STARTTLS handshakes and
roughly works like this:

- INBOME-supporting MUAs are expected to keep `state <mua-state>`_ 
  about the peers that they negotiate encryption with.

- An MUA will send an INBOME request header along with each mail it
  sends out to a peer for which it has no encryption key.

- An MUA which sends a mail to an address from where it earlier saw an
  INBOME request will add an appropriate encryption key.

- An MUA which sees an INBOME encryption key in an incoming messsage
  will store it for later use with that peer.

- When sending an e-mail to a peer who has established a key in this
  fashion, the e-mail will be automatically encrypted.
  
INBOME basic operations
-------------------------------

MUAs maintain INBOME state by parsing incoming and amending outgoing
messages. The state-holding object provides the following conceptual
operations:

- ``process_incoming(mime_cleartext_mail)``: analyze incoming mail and
  update local INBOME information.

- ``get_encrypt_key(recipient_address)``: Return encryption key or
  None for recipient_address.

- ``process_outgoing(mime_cleartext_mail)``: Return new Mime mail with
  headers and attachments added.

Note that these INBOME operations do not perform any encryption or
decryption but rather handle key management.

The ``get_encrypt_key`` operation should be used at mail composition
time.  If a MUA can obtain encryption keys this way for all
recipients, it signals to the user that the mail content will be
encrypted.

"Happy path" example: 1:1 communication
------------------------------------------

Consider a blank state and a first outgoing message from Alice to
Bob::

    From: alice@a.example
    To: bob@b.example
    ...

``process_outgoing()`` will add an INBOME header::

    INBOME: request;adr=bob@b.example

after which the MUA sends the complete message out in cleartext.
Bob's INBOME implementation will in its ``process_incoming`` detect
the ``INBOME`` request header, internally mark the from-address as
INBOME-capable and in state "requesting".  When Bob now sends a mail
back to Alice, its ``process_outgoing`` will provide the requested
key::

    INBOME: provide=bob@b.example;keydata=<encoded_encryption_key_bob>

and another header to itself request a key from Alice::

    INBOME: request;adr=alice@a.example

After Bob's MUA sends out the mail, Alice's ``process_incoming`` will
parse the message and store Bob's encryption key.  On sending a mail,
Alice's ``process_outgoing`` will add::

    INBOME: provide;adr=alice@a.example;keydata=<encoded_encryption_key_of_alice>

As Bob's MUA now has Alice's encryption key, both Alice and Bob can
from now on send encrypted mails to each other.  The initial two mails
(Alice->Bob, Bob->Alice) were sent in the clear.  In any subsequent
mail exchange the MUAs must add a "happy encryption" header::

    INBOME: encrypted


FIXME: what is the point of the "happy encryption" INBOME: encrypted
header?  if the mail is encrypted, isn't that sufficient knowledge?
If one party of an established connection chooses to send a cleartext
message (e.g. they are cc'ing someone who does not use INBOME), what
happens to the state?
    
If one side stops sending an INBOME header the other side must stop
sending encrypted mails. This automatic downgrade is neccessary to
accomodate user scenarios such as the following:

- Alice might choose to not use INBOME or an INBOME supporting MUA
  because it is buggy

- Alice might have a second device and discover that it doesn't
  support INBOME yet and rather prefer to read mails on both devices.

- Alice might lose her device and start over from some webmail account
  which does not support INBOME


Happy path example: 1:N communication
------------------------------------------

Consider a blank state and a first outgoing message from Alice to Bob
and Carol::

    From: alice@a.example
    To: bob@b.example, carol@c.example

    ...

``process_outgoing()`` will add two INBOME request headers with
explicit addresses::

    INBOME: request;adr=bob@b.example
    INBOME: request;adr=carol@c.example

Bob's INBOME implementation will in its ``process_incoming`` detect
the ``INBOME`` request headers.  When Bob now sends a mail back to
Alice, ``process_outgoing`` adds two headers like in the 1:1 case::

    INBOME: provide=bob@b.example;keydata=<encoded_encryption_key_of_bob>
    INBOME: request=alice@a.example

After Bob's MUA sends out the mail, Alice's ``process_incoming`` will
parse INBOME headers and store Bob's encryption key.

FIXME: but if Bob replies to both Alice and Carol, and Carol has not
sent Bob an INBOME: request, does Bob send her an INBOME: provide
anyway?

Ideally, both Alice and Carol can subsequently reply encrypted and
still need to provide their own key for Bob to allow him to perform
encryption.


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

