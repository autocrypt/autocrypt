
INBOME - in-band opportunistic mail encryption (Version -0.1)
--------------------------------------------------------------

STATUS: experimental draft (arising from several discussions at the PGPSummit 2016 and OpenPGPConf 2016 between holger krekel, dkg, Vincent Breitmoser and others).  It is not yet a formal draft, rather aims to summarize and focus discussions and is work in progress.

INBOME is a protocol for increasing encryption of mails within the existing mail infrastructure and its standards and practises. It distributes encryption keys through social messages among peers and only requires support from MUAs.  **No changes are required from MTAs and providers**. It thus tries to avoid the social and technical complexities arising from requiring changes on both MUAs and MTAs.

INBOME shares the perspectives and ideas layed out in RFC4535 ("Opportunistic Security"), in particular, it:

- aims to be safe against passive eavesdropping attacks (network and providers).

- is designed for incremental deployment (does not assume everybody uses INBOME)

- prefers sending cleartext over asking users key-related questions

When operating with defaults, INBOME is susceptible to downgrade and MITM attacks, particularly on the MTA/provider computers where a mails passes through.  However, MUAs may allow users to opt into detecting some of those attacks at the cost of requiring more UI interactions. In all cases, MUAs MUST provide a clear indication at mail composition time if encryption is active.

The rough message of INBOME supporting MUAs to users is: after you exchanged some messages subsequent messages will be end-to-end encrypted, i.e. mails can not be read by your providers or any entities which have access to your provider's data. Conversely, INBOME concedes that the first mails are not encrypted which is consistent with Opportunistic Security perspectives.

A note on INBOME and existing spam infrastructure
----------------------------------------------------------

Mike Hearn raised some fundamental concerns in his `Modern anti-spam and E2E crypto post on the modern crypto mailing list <https://moderncrypto.org/mail-archive/messaging/2014/000780.html>`_ on how end-to-end encrypted mails and spam infrastructure possibly interfere.  While it's conceivable to imagine new ways to fight spam in an E2E setting by increased DKIM usage and additional measures and policies the topic is a serious one as adoption of more encrypted mails could be seriously hampered if encryption can bypass current anti-spam technology.

INBOME works well with existing provider Anti-Spam infrastructures because they can continue to check the initial cleartext mails for suspicious content. Only if a user replies to a (likely non-spam) mail will INBOME make a MUA send an encryption key.  Without being able to get sufficiently many replies from users it will likely be to massively harvest encryption keys; there is no central registery for key-mail address relations.  Massive collection of key/mailaddress associations would require co-operation from or compromise of big mail providers which is unlikely given they have been fighting unsolicited mails for decades and their business models depend on it. But even if a user's encryption key becomes public the worst outcome are increased numbers of unsoliticed mails arriving at the MUA side. Upgrading to a new key can mitigate the problem and is supported by INBOME.


Basic protocol flow
---------------------------------

Establishing encryption is reminiscent of TLS/STARTTLS handshakes and roughly works like this:

- A MUA will send an INBOME request header along with each mail it sends out to a peer for which it doesn't have an encryption key.

- A MUA which sends a mail to an address from where it earlier saw an INBOME
  request will add an appropriate encryption key.

- A MUA which sees an INBOME encryption key in an incoming messsage will store
  it for later use.


INBOME basic operations
-------------------------------

MUAs maintain INBOME state by parsing incoming and amending outgoing messages. The state holding object provides the following conceptual operations:

- ``process_incoming(mime_cleartext_mail)``: analyze incoming mail and update local INBOME information.

- ``get_encrypt_key(recipient_address)``: Return encryption key or None for recipient_address.

- ``process_outgoing(mime_cleartext_mail)``: Return new Mime mail with headers and attachments added.

Note that these INBOME operations do not perform any encryption or decryption but rather handle key distribution.

The ``get_encrypt_key`` operation should be used at mail composition time.  If a MUA can obtain encryption keys this way for all recipients, it signals to the user that the mail content will be encrypted.

"Happy path" example: 1:1 communication
------------------------------------------

Consider a blank state and a first outgoing message from Alice to Bob::

    From: alice@a.org
    To: bob@b.org
    ...

``process_outgoing()`` will add an INBOME header::

    INBOME: request;adr=bob@b.org

after which the MUA sends the complete message out in cleartext.  Bob's INBOME implementation will in its ``process_incoming`` detect the ``INBOME`` request header, internally mark the from-address as INBOME-capable and in state "requesting".  When Bob now sends a mail back to Alice, its ``process_outgoing`` will provide the requested key::

    INBOME: provide=bob@b.org;keydata=<encoded_encryption_key_bob>

and another header to itself request a key from Alice::

    INBOME: request;adr=alice@a.org

After Bob's MUA sends out the mail, Alice's ``process_incoming`` will parse the message and store Bob's encryption key.  On sending a mail, Alice's ``process_outgoing`` will add::

    INBOME: provide;adr=alice@a.org;keydata=<encoded_encryption_key_of_alice>

As Bob's MUA now got Alice's encryption key, both Alice and Bob can from now on send encrypted mails to each other.  The initial two mails (Alice->Bob, Bob->Alice) were sent in the clear.  In any subsequent mail exchange the MUAs must add a "happy encryption" header:

    INBOME: encrypted

If one side stops sending an INBOME header the other side must stop sending encrypted mails. This automatic downgrade is neccessary to accomodate user scenarios such as the following:

- Alice might choose to not use INBOME or an INBOME supporting MUA because it is buggy

- Alice might have a second device and discover that it doesn't support INBOME yet and rather prefer to read mails on both devices.

- Alice might loose her device and start over from some webmail account which does not support INBOME


Happy path example: 1:N communication
------------------------------------------

Consider a blank state and a first outgoing message from Alice to Bob and Carol::

    From: alice@a.org
    To: bob@b.org, carol@c.org

    ...

``process_outgoing()`` will add two INBOME request headers with explicit addresses::

    INBOME: request;adr=bob@b.org
    INBOME: request;adr=carol@c.org

Bob's INBOME implementation will in its ``process_incoming`` detect the ``INBOME`` request headers.  When Bob now sends a mail back to Alice, ``process_outgoing`` adds two headers like in the 1:1 case::

    INBOME: provide=bob@b.org;keydata=<encoded_encryption_key_of_bob>
    INBOME: request=alice@b.org

After Bob's MUA sends out the mail, Alice's and Carol's ``process_incoming`` will parse INBOME headers and store Bob's encryption key.  Both Alice and Carol can subsequently reply encrypted and still need to provide their own key for bob to allow him to perform encryption.


Open issues / notes
-------------------------

- Instead of transporting keysdata through INBOME headers we could also add attachments, e.g. application/pgp-keys ones and put INBOME headers into it.

- Generation and maintenance of secret decryption keys is not handled/discussed yet.  One idea from the Summit/Conf discussions is to use self-sent messages to transfer private key material (which should be encrypted with a backup code so that provider can not obtain the private key)

- multi-device support: idea is to use self-sent messages to pair devices and synchronize both encryption and decryption key material between them.

- is INBOME a good name? :)

- The actual encryption/signing steps are not defined by IBAME.  For now we assume the practical implementation uses GPG keys and either a separate or the default user's keyrings to store keys coming over INBOME.

- We allow peers to gossip keys for all participating parties in an email conversation to speed up key discovery among them.  If a peer got two different keys for a target address (which can happen because of group gossiping and upgraded/regenerated keys) the peer shall encrypt to both keys if possible and request a key from the peer so that it can resolve the conflict.

- We assume that a MUA only sends a key to a peer if the peer's last message indicated IBAME abilities/requests.  If a peer has sent a non IBAME mail, a MUA shall by default send a cleartext mail (unless explicitely requested by its user to continue sending encrypted).

- how does INBOME interact with today's mailing list managers?

- under what circumstances precisely do you downgrade from encryption to
  cleartext?  Could we consider the ``USER-AGENT`` header which often will indicate if the other side is using multiple devices/MUAs?  can we otherwise practically distinguish different MUAs from parsing messages/headers?

- how to deal with spammers downgrade encryption by using a fake from?
  (it's not their intention, just a side effect).  How much can we rely on DKIM?

