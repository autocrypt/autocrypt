Autocrypt Level 1: Enabling encryption, avoiding annoyances
===========================================================

This document describes the basic capabilities required for a mail app
to be Autocrypt-capable at Level 1. The design of Level 1 is driven by
usability concerns and by the realities of incremental deployment. A
user may use both Autocrypt-enabled mail apps and traditional plain
ones and we'd like to avoid annoyances like unexpected unreadable
mails while supporting users who want to explicitly turn on
encryption.

For ease of implementation and deployment, Level 1 does not support
multi-device configurations.  We intend to :doc:`support the multi-device
use case (and other features) as part of Level 1<next-steps>`.  We
want to keep Level 1 minimal enough that it's easy for developers to
adopt it and we can start to drive efforts from real-life experiences
as soon as possible.

Throughout this document, we refer to a mail app or Mail User Agent (MUA)
as though it was only capable of controlling a single e-mail account.  An
MUA that is capable of connecting to multiple e-mail accounts should
have a separate Autocrypt state for each e-mail account it has access
to.

.. contents::

Requirements on MUA/E-mail Provider interactions
------------------------------------------------

Autocrypt tries to impose minimal requirements on how MUAs and
e-mail services interact.  We assume that an Autocrypt-capable MUA
has credentials and capabilities to perform these network services:

- The ability to send e-mail (e.g. via SMTP or Submission) where the
  MUA can control the entire message being sent, including both
  message headers and message body.

- The ability to receive e-mail where the MUA gets access to the
  entire message being received, including both message headers and
  message body.

- Optionally, a way to scan the user's Sent folder for mail with
  specific headers.

If a particular e-mail account does not expose one of the required
features (e.g. if it only exposes a javascript-driven web interface
for message composition that does not allow setting of e-mail headers)
then the e-mail account cannot be used with Autocrypt.  An
Autocrypt-capable MUA may still access and control the account, but it
will not be able to enable Autocrypt on it.

.. todo::

    Discuss with webmail developers how to work with, refine
    the interactions.

Secret key generation and storage
---------------------------------

The MUA MUST be capable of generating and storing two RSA 2048-bit
secret keys, one for signing and self-certification and the other for
decrypting.  It MUST be capable of assembling these keys into an
OpenPGP certificate (:rfc:`RFC 4880 "Transferable Public
Key"<4880#section-11.1>`) that indicates these capabilities.

The secret key material should be protected from access by other
applications or co-tenants of the device, at least as well as the
passwords the MUA retains for the user's IMAP or SMTP accounts.

Avoiding Client Conflicts
-------------------------

If more than one Autocrypt-enabled client generates a key and then
distributes it to communication peers, encrypted mail sent to the user
is only readable by the MUA that sent the last message. This can lead
to behavior that is unpredictable and confusing for the user.

As a simple measure of mitigation, Level 1 MUAs SHOULD check before
key generation whether there is evidence in the user's mailbox of
other active Autocrypt clients. To do this, they SHOULD scan the
user's Sent folder for mail that contains Autocrypt headers. If such
mail exists, the MUA SHOULD warn the user and abort key generation,
unless explicitly instructed to proceed regardless.

In cases where an Autocrypt-capable MUA is unable to identify the
user's Sent folder, or is unable to access any pre-existing message
archive (e.g. a POP-only MUA), the MUA MUST warn the user that
Autocrypt should be enabled on **only one** client before enabling
Autocrypt on the given account.

To solve this problem in a better way, bi-directional communication
between the user's different MUAs is required. However, this is out of
scope for Level 1.

Autocrypt Setup Message
-----------------------

For proper support of a multi-device scenario, it is necessary to have
bi-directional communication between different MUAs. This is possible
e.g. via access to a shared IMAP mailbox. Because of the complexity of
this approach however, multi-device support in the sense of devices
coordinating with each other is out of scope for Autocrypt Level 1. It
is still important to avoid "lock-in" of secret key material on a
particular client. For this reason, Autocrypt includes a way to
"export" the user's keys and the user's prefer-encrypt state for other clients to pick up,
asynchronously and with explicitly required user interaction.

The mechanism available in Autocrypt level 1 is a specially-formatted
e-mail message called the Autocrypt Setup Message.  An
already-configured Autocrypt client can generate an Autocrypt Setup
Message, and send it to itself.  A not-yet-configured Autocrypt client
(a new client in a multi-device case, or recovering from device
failure or loss) can import the Autocrypt Setup Message and recover
the ability to read existing messages.

An Autocrypt Setup Message is protected with a strong Setup Code.

Message Structure
+++++++++++++++++

The Autocrypt Setup Message itself is an e-mail message with a
specific format, which contains a payload protected by the setup code.

- Both the To and From headers MUST be the address of the user.

- The Autocrypt Setup Message MUST contain an ``Autocrypt-Setup-Message: v1`` header.

- The Autocrypt Setup Message MUST have a ``multipart/mixed`` structure,
  and it MUST have as first part a human-readable description about
  the purpose of the message (e.g. ``text/plain`` or ``text/html`` or
  ``multipart/alternative``).

- The second mime part (called "payload") of the Autocrypt setup message
  MUST be of Content-Type ``application/autocrypt-setup``.  There MUST NOT
  be another part with the same content-type.

- The payload MUST contain a single ASCII-armored block of OpenPGP
  symmetrically encrypted data, and MAY include other text above or
  below the ASCII-armored data, which MUST be ignored while
  processing. Implementors MAY choose to provide human-readable
  explanations as discussed in
  :doc:`suggestions for key-transfer format<transfer-format>`.

- Decrypting the payload MUST produce a ``multipart/mixed`` mime structure
  which MUST have an ``Autocrypt-Prefer-Encrypt`` header containing the value
  of the user's prefer-encrypt setting. The first embedded mime part
  MUST be of content-type ``application/autocrypt-key-backup`` containing
  an ASCII-armored OpenPGP transferable secret key in the Mime body.

- The symmetric encryption algorithm used MUST be AES-128.
  The passphrase MUST be the Setup Code (see below), used
  with `OpenPGP's salted+iterated S2K algorithm
  <https://tools.ietf.org/html/rfc4880#section-3.7.1.3>`_.

Setup Code
++++++++++

The setup code MUST be generated by the implementation itself using a
CSPRNG, and presented directly to the user for safekeeping. It MUST
NOT be included in the cleartext of the Autocrypt Setup Message, or
otherwise transmitted over e-mail.

An Autocrypt Level 1 client MUST generate a setup code as UTF-8 string
of 36 numeric characters, divided into nine blocks of four, separated
by dashes. The dashes are part of the secret code and there are no
spaces. This format holds about 119 bits of entropy. It is designed to
be unambiguous, pronounceable, script-independent (chinese, cyrillic
etc.), easily input on a mobile device and split into blocks that are
easily kept in short term memory. For instance::

    9503-1923-2307-
    1980-7833-0983-
    1998-7562-1111

An Autocrypt Setup Message payload that uses this structure for its
setup code SHOULD include a ``Passphrase-Format`` header with value
``numeric9x4`` in the ASCII-armored data. This allows providing a
specialized input form during decryption, with greatly improved
usability.

As a further measure to improve usability, it is RECOMMENDED to reveal
the first two digits of the first block in a ``Passphrase-Begin``
header, sacrificing about 7 bits of entropy. Those digits can be
pre-filled during decryption, which reassures the user that they have
the correct code before typing the full 36 digits. It also helps
mitigate a possible type of phishing attack that asks the user to
input their setup code.

The headers might look like this::

    Passphrase-Format: numeric9x4
    Passphrase-Begin: 95

If those digits are included in the headers like this, they may also
be used in the descriptive text that is part of the Setup Message, to
distinguish different messages.


Setup Message Creation
++++++++++++++++++++++

An Autocrypt client MUST NOT create an Autocrypt Setup Message without
explicit user interaction.  When the user takes this action for a
specific account, the client:

 * Generates a strong setup code from a CSPRNG.
 * Optionally, displays the setup code to the user, prompts the user
   to write it down, and then hides it and asks the user to re-enter
   it before continuing.  This minor annoyance is a recommended
   defense against worse annoyance: it ensures that the code was
   actually written down and the Autocrypt Setup Message is not
   rendered useless.
 * Produces an ASCII-armored, minimized OpenPGP transferable secret
   key out of the key associated with that account embedded into a
   multipart/mixed structure also containing a header with the user's
   prefer-encrypt state.
 * Symmetrically encrypts the OpenPGP transferable secret key using
   the secret code as the password.
 * Composes a new self-addressed e-mail message that contains the
   payload as a MIME part with the appropriate Content-Type and other
   headers.
 * Sends the generated e-mail message to its own account.
 * Suggests to the user to either back up the message or to import it
   from another Autocrypt-capable client.

A Level 1 client MUST be able to create an Autocrypt Setup Message, to
preserve users' ability to recover from disaster, and to choose to use
a different Autocrypt-capable client in the future.


Setup Message Import
++++++++++++++++++++

An Autocrypt-capable client SHOULD support the ability to wait for and
import an Autocrypt Setup Message when the user has not yet configured
Autocrypt.  This could happen either when a user of an unconfigured
Autocrypt client decides to enable Autocrypt, or the client could
proactively scan the client's mailbox for a message that matches these
characteristics, and it could alert the client if it discovers one.

If the client finds an Autocrypt Setup Message, it should offer to
import it to enable Autocrypt.  If the user agrees to do so:

 * The client prompts the user for their corresponding Setup Code.
   If there is a ``Passphrase-Format`` header in the outer OpenPGP armor and
   its value is ``alphanumeric``, then the client MAY present a specialized
   input dialog assisting the user to enter a code in the format described
   above.
   If there is no ``Passphrase-Format`` header, or the value is unknown,
   then the client MUST provide a plain UTF-8 string text entry.

 * The client should try decrypting the message with the supplied
   Setup Code.  The Code serves both for decryption as well as authenticating
   the message.  Extra care needs to be taken with some PGP implementations
   that the Setup Code is actually used for decryption.
   :doc:`Preventing against injected private keys<bad-import>`

 * If it decrypts the client SHOULD import the secret
   key material as its own Autocrypt key (``own_state.secret_key`` as
   discussed in `Account Preferences`_).

Why were some of these choices made?
++++++++++++++++++++++++++++++++++++

We chose salted+iterated S2K.  While the use of a memory-hard KDF like
scrypt or argon2 would be desirable in the future, this is not
specified in OpenPGP so far, and it is a bigger concern to preserve
compatibility and avoid friction with presently deployed OpenPGP
software.

While the message structure is complex, it's actually fairly easy to
pack and unpack with common OpenPGP tools.  It was selected to ease
implementation and deployment, not for cleanliness or purity :)

Example:

::

	To: me@mydomain.com
	From: me@mydomain.com
	Autocrypt-Setup-Message: v1
	Content-type: multipart/mixed; boundary="==break1=="

	--==break1==
	Content-Type: text/plain

	This is the Autocrypt setup message.

	--==break1==
	Content-Type: application/autocrypt-key-backup
    Content-Disposition: attachment; filename="autocrypt-key-backup.html"

	<html>
	<body>
	<p>
	    This is the Autocrypt setup file used to transfer keys between clients.
	</p>
    <pre>
    -----BEGIN PGP MESSAGE-----
    Version: BCPG v1.53
    Passphrase-Format: numeric9x4
    Passphrase-Begin: 12

    hQIMAxC7JraDy7DVAQ//SK1NltM+r6uRf2BJEg+rnpmiwfAEIiopU0LeOQ6ysmZ0
    CLlfUKAcryaxndj4sBsxLllXWzlNiFDHWw4OOUEZAZd8YRbOPfVq2I8+W4jO3Moe
    -----END PGP MESSAGE-----
    </pre>
	</body>
	</html>
	--==break1==--

The encrypted message part contains:

::

	Content-type: multipart/mixed; boundary="==break2=="
	Autocrypt-Prefer-Encrypt: mutual

	--==break2==
	Content-type: application/autocrypt-key-backup

	-----BEGIN PGP PRIVATE KEY BLOCK-----
	Version: GnuPG v1.2.3 (GNU/Linux)

	xcLYBFke7/8BCAD0TTmX9WJm9elc7/xrT4/lyzUDMLbuAuUqRINtCoUQPT2P3Snfx/jou1YcmjDgwT
	Ny9ddjyLcdSKL/aR6qQ1UBvlC5xtriU/7hZV6OZEmW2ckF7UgGd6ajE+UEjUwJg2+eKxGWFGuZ1P7a
	4Av1NXLayZDsYa91RC5hCsj+umLN2s+68ps5pzLP3NoK2zIFGoCRncgGI/pTAVmYDirhVoKh14hCh5
	.....
	-----END PGP PRIVATE KEY BLOCK-----
	--==break2==--

Header injection in outbound mail
---------------------------------

During message composition, if the ``From:`` header of the
outgoing e-mail matches an address that the Autocrypt-capable agent
knows the secret key material (``own_state.secret_key``) for, it
SHOULD include an Autocrypt header. This header MUST contain the
associated public key material (``own_state.public_key``) as ``keydata``
attribute, and the same sender address that is used in the ``From``
header in the ``addr`` attribute to confirm the association.  The most
minimal Level 1 MUA will only include these two attributes.  If
``own_state.prefer_encrypt`` is set to ``mutual`` then the header MUST
have a ``prefer-encrypt`` attribute set to ``mutual``.

If the ``From`` address changes during message composition (E.g. if
the user selects a different outbound identity), the Autocrypt-capable
client MUST change the ``Autocrypt`` header appropriately.

See :ref:`mua-happypath` for examples of outbound headers and
the following sections for header format definitions and parsing.

..  _autocryptheaderformat:

The ``Autocrypt`` Header
------------------------

The ``Autocrypt`` header has the following format::

    Autocrypt: addr=a@b.example.org; [type=1;] [prefer-encrypt=mutual;] key=BASE64

The ``addr`` attribute indicates the single recipient address this
header is valid for. In case this address differs from the one the MUA
considers the sender of the e-mail in parsing, which will usually be
the one specified in the ``From`` header, the entire header MUST be
treated as invalid.

The ``type`` and ``keydata`` attributes specify the type and data of the
key material.  For now the only supported type is ``1``, which
represents a specific subset of OpenPGP (see the next section), and is
also the default.  Headers with an unknown ``type`` MUST be treated as
invalid.  The value of the ``keydata`` attribute is a Base64
representation of the public key material.  This is a simple
ascii-armored key format without a checksum (which would then be Radix64)
and without pgp message markers (``---BEGIN...`` etc.).  For ease of
parsing, the ``keydata`` attribute MUST be the last attribute in the header.

The ``prefer-encrypt`` attribute can only occur with the value
``mutual``.  Its presence the Autocrypt header indicates an agreement
to encrypt by default with other peers who have the same preference.
An Autocrypt Level 1 client that sees the attribute with any other
value (or that does not see the attribute at all) should interpret the
value as ``nopreference``.

Additional attributes unspecified here are also possible before the
``keydata`` attribute.  If an attribute name starts with an underscore
(``_``), it is a "non-critical" attribute.  An attribute name without
a leading underscore is a "critical" attribute.  The MUA SHOULD ignore
any unsupported non-critical attribute and continue parsing the rest
of the header as though the attribute does not exist, but MUST treat
the entire header as invalid if it encounters a "critical" attribute
it doesn't support.

When parsing an incoming message, a MUA MUST examine all ``Autocrypt``
headers, rather than just the first one. If there is more than one
valid header, this MUST be treated as an error, and all ``Autocrypt``
headers discarded as invalid.

.. todo::

   - Document why we skip on more than one valid header?

``type=1``: OpenPGP Based key data
++++++++++++++++++++++++++++++++++

For maximum interoperability, a certificate sent by an
Autocrypt-enabled Level 1 MUA MUST consist of an :rfc:`OpenPGP
"Transferable Public Key"<4880#section-11.1>`) containing exactly these five
OpenPGP packets:

 - a signing-capable primary key ``Kp``
 - a user id
 - a self signature
 - an encryption-capable subkey ``Ke``
 - a binding signature over ``Ke`` by ``Kp``

The content of the user id packet is only decorative. By convention, it
contains the same address used in the ``addr`` attribute in angle brackets,
conforming to the :rfc:`2822` grammar ``angle-addr``. For compatibility
concerns the user id SHOULD NOT be an empty string.

These packets MUST be assembled in binary format (not ASCII-armored),
and then base64-encoded.

A Level 1 MUA MUST be capable of processing and handling 2048-bit RSA
public keys.  It MAY support other OpenPGP key formats found in
a ``type=1`` Autocrypt header (for example, by passing it agnostically
to an OpenPGP backend for handling).

Secret key protection at rest
-----------------------------

The MUA SHOULD NOT protect the private key with a password. All
encrypted outgoing messages MUST also be signed, which would require the
user to enter their password for both reading and sending mail. This
introduces too much friction to become part of a routine daily workflow.
Protection of the user's keys at rest and other files is achieved more
easily and securely with full-disk encryption.


.. _`autocryptpeermap`:

The autocrypt peer map
----------------------

MUAs SHOULD maintain an ``autocrypt_peer_map`` which maps a
:doc:`canonicalized e-mail address <address-canonicalization>` to a
``peer_entry`` which summarizes what we know from processing the
flow of incoming messages.  This knowledge is used for computing an
`encryption recommendation <encryption-recommendation>`_ for mail
composition.   It is expected that future Autocrypt specifications
mandate synchronization of the ``autocrypt_peer_map`` among
multiple devices of a user.

Peer Entry attributes
+++++++++++++++++++++

Each ``peer_entry`` has the following attributes:

* ``last_seen``: UTC timestamp of the most recent effective date of
  all processed messages for this peer.
* ``last_seen_autocrypt``: UTC timestamp of the most recent effective
  date of all processed messages for this peer that contained a valid
  Autocrypt header.
* ``public_key``: the public key for this e-mail address, ``null`` if
  none exists or if the key is invalid.
* ``key_status``: a quad-state: ``nopreference``, ``mutual``, ``reset``, or
  ``gossip``.

Agents MAY also store additional information like the complete chronology
of keys seen from a peer, or statistical information about incoming messages
which might be used for determining how likely the other side can read
encrypted messages.  See :doc:`optional-state` for related considerations.

Updating a peer entry from an incoming message
++++++++++++++++++++++++++++++++++++++++++++++

Updating a ``peer_entry`` depends on the ``effective_date`` and the
Autocrypt header of each incoming message.  The ``effective_date`` is
defined by the ``Date`` header or, if it is in the future or invalid,
the current date.  Updating can happen at arrival or display time of
a message and messages may be processed in non-chronological order.
A MUA updates a ``peer_entry`` by following all of the following steps:

- If the incoming message contains no Autocrypt header and ``effective_date``
  is more recent than ``last_seen`` then update as follows:

  * set ``last_seen`` to the effective message date
  * set ``key_status`` to ``reset``

- If the message contains an Autocrypt header and the
  ``effective_date`` is more recent than ``last_seen_autocrypt``,
  then:

  * set ``public_key`` from the corresponding ``keydata`` value of
    the Autocrypt header
  * set ``last_seen_autocrypt`` to ``effective_date``

- If the message contains an Autocrypt header and the
  ``effective_date`` is at least as recent as ``last_seen``,
  then:

  * set ``last_seen`` to ``effective_date``
  * set ``key_status`` to ``mutual`` if the Autocrypt header contains
    a ``prefer-encrypt=mutual`` attribute, or ``nopreference`` otherwise

.. note::

  - An implementation MAY also choose to obtain public keys from other sources
    (e.g. local keyring).

  - If an implementation chooses to automatically ingest keys from a
    ``application/pgp-keys`` attachment, it SHOULD do so only if the
    contained public key has a user id which matches the ``From``.

.. _spam-filters:

.. todo::

   the spec currently doesn't say how to integrate Autocrypt
   processing on message receipt with spam filtering.  Should we say
   something about not doing Autocrypt processing on message receipt
   if the message is believed to be spam?


.. _`encryption-recommendation`:

Encryption recommendation for message composition
--------------------------------------------------

On message composition, an Autocrypt-capable agent also has an
opportunity to decide whether to try to encrypt an e-mail.  Autocrypt
aims to provide a reasonable recommendation for the agent.

Any Autocrypt-capable agent may have other means for making this
decision outside of Autocrypt (see :doc:`other-crypto-interop`).
Autocrypt provides a recommendation to this process, but there is no
requirement for Autocrypt-capable agents to always follow the
Autocrypt recommendation.

That said, all Autocrypt-capable agents should be able to calculate
the same Autocrypt recommendation due to their internal state.

The Autocrypt recommendation depends on the list of recipient
addresses for the message being composed.  When the user edits the
list of recipients, the recommendation may change.  The MUA should
reflect this change.

.. note::

   It's possible that the user manually overriddes the Autocrypt
   recommendation and then edits the list of recipients.  The MUA
   SHOULD retain the user's manual choices for a given message even if
   the Autcrypt recommendation changes.

.. todo::

   Discuss how to deal with the case where the user manually selects
   encryption and subsequently adds a recipient whom the MUA has no
   key.

Autocrypt can produce four possible recommendations to the agent
during message composition:

 * ``disable``: Disable or hide any UI that would allow the user to
   choose to encrypt the message.  Prepare the message in cleartext.

 * ``discourage``: Enable UI that would allow the user to choose to
   encrypt the message, but do not default to encryption. Prepare the
   message in cleartext. If the user manually enables encryption, the
   MUA SHOULD warn that the recipient may not be able to read the
   message. This warning message MAY be supplemented using optional
   counters and user-agent state as suggested in
   :doc:`optional-state`.

 * ``available``: Enable UI that would allow the user to choose to
   encrypt the message, but do not default to encryption.  Prepare the
   message in cleartext.

 * ``encrypt``: Enable UI that would allow the user to choose to send
   the message in cleartext, and default to encryption.  Prepare the
   message as an encrypted message.

Recommendations for single-recipient messages
+++++++++++++++++++++++++++++++++++++++++++++

The Autocrypt recommendation for a message composed to a single
e-mail address is computed from the ``own_state`` of an Autocrypt
account, the ``peer_entry`` as found in the ``autocrypt_peer_map``
for the e-mail address, and a boolean ``is_reply_to_encrypted``
indicating whether this is a reply to an encrypted message.
A MUA SHOULD implement the following algorithm:

1. If the ``public_key`` is ``null``, the recommendation is ``disable``.

2. If ``is_reply_to_encrypted`` is True, the recommendation is ``encrypt``.

3. If ``key_status`` is ``mutual`` and ``own_state.prefer_encrypt`` is
   ``mutual``, then the recommendation is ``encrypt``.

4. If ``key_status`` is ``gossip``, the recommendation is ``discourage``.

5. If ``key_status`` is ``reset`` and the ``last_seen_autocrypt`` is more
   than one month ago, then the recommendation is ``discourage``.

Otherwise, the recommendation is ``available``.

Recommendations for messages to multiple addresses
++++++++++++++++++++++++++++++++++++++++++++++++++

For level 1 agents, the Autocrypt recommendation for a message
composed to multiple recipients is derived from the recommendations
for each recipient individually:

1. If any recipient has a recommendation of ``disable`` or ``discourage``
   then the overall recommendation is ``disable`` or ``discourage`` respectively.

2. If all recipients have a recommendation of ``encrypt`` then the overall
   recommendation is ``encrypt``.

3. Otherwise, the recommendation is ``available``.

Cleartext replies to encrypted mail
+++++++++++++++++++++++++++++++++++

As you can see above, in the common use case, a reply to an encrypted
message will also be encrypted. Due to Autocrypt's opportunistic
approach to key discovery, however, it is possible that
``peer_entry.public_key`` is ``null`` which means the reply will be
sent in the clear.

To avoid leaking cleartext from the original encrypted message in this
case, the MUA MAY prepare the cleartext reply without including any
of the typically quoted and attributed text from the previous message.
Additionally, the MUA MAY include brief text in message body along the
lines of::

  The message this is a reply to was sent encrypted, but this reply is
  unencrypted because I don't yet know how to encrypt to
  ``bob@example.com``.  If ``bob@example.com`` would reply here, my
  future messages in this thread will be encrypted.

The above recommendations are only "MAY" and not "SHOULD" or "MUST"
because we want to accomodate a user-friendly level 1 MUA that stays
silent and does not impede the user's ability to reply.  Opportunistic
encryption means we can't guarantee encryption in every case.

Encrypt outbound mail as requested
----------------------------------

An outgoing e-mail will be sent encrypted in either of two cases:

- the Autocrypt recommendation for the list of recipients is
  ``encrypt``, and not explicitly overridden by the user
- the Autocrypt recommendation is ``available`` or ``discouraged``,
  and the user chose to encrypt.

In this case, the MUA MUST construct the encrypted message as a
:rfc:`PGP/MIME <3156>` message that is signed by the user's Autocrypt
key, and encrypted to each currently known Autocrypt key of all
recipients, as well as the sender's.

For messages that are going to be encrypted when sent, the MUA MUST
take care not to leak the cleartext of drafts or other
partially-composed messages to their e-mail provider (e.g. in the
"Drafts" folder). If there is a chance that a message could be
encrypted, the MUA SHOULD encrypt drafts only to itself before storing
it remotely.

.. note::

   An e-mail that is said to be "encrypted" here will be both signed
   and encrypted in the cryptographic sense.

Key Gossip
----------

It is a common use case to send an encrypted mail to a group of
recipients. To ensure that these recipients can encrypt messages when
replying to that same group, the keys of all recipients can be
included in the encrypted payload.

The ``Autocrypt-Gossip`` header has the format as the ``Autocrypt``
header (see `autocryptheaderformat`_). Its ``addr`` attribute
indicates the recipient address this header is valid for as usual, but
may relate to any recipient in the ``To`` or ``Cc`` header.

Key Gossip Injection in Outbound Mail
+++++++++++++++++++++++++++++++++++++

An Autocrypt MUA MAY include ``Autocrypt-Gossip`` headers in messages
with more than one recipient. These headers MUST be placed in the root
MIME part of the encrypted message payload. The encrypted payload in
this case contains one Autocrypt-Gossip header for each recipient,
which MUST include ``addr`` and ``keydata`` attributes with the relevant
data from the recipient's Autocrypt peer state.

Updating Autocrypt Peer State from Key Gossip
+++++++++++++++++++++++++++++++++++++++++++++

An incoming message may contain one or more Autocrypt-Gossip headers
in the encrypted payload. Each of these headers may update the
Autocrypt peer state of the recipient indicated by its ``addr`` value,
in the following way:

1. If the ``addr`` value does not match any recipient in the mail's
   ``To`` or ``Cc`` header, the entire header MUST be ignored.

2. If the existing ``last_seen_autocrypt`` value is older than the
   effective message date and the existing ``key_status`` is ``gossip``, or
   the ``last_seen_autocrypt`` value is null:

    - set ``keydata`` to the corresponding value of the
      ``Autocrypt-Gossip`` header
    - set ``last_seen`` to the effective message date
    - set ``key_status`` to ``gossip``

Specific User Interface Elements
--------------------------------

Ideally, Autocrypt users see very little UI.  However, some UI is
inevitable if we want users to be able to interoperate with existing,
non-Autocrypt users.

Account Preferences
+++++++++++++++++++

Level 1 MUAs MUST allow the user to disable Autocrypt completely for
each account they control.  For level 1, we expect most MUAs to have
Autocrypt disabled by default.

Level 1 MUAs maintain an internal structure ``own_state`` for each
account on which Autocrypt is enabled. ``own_state`` has the following
members:

 * ``secret_key`` -- the RSA 2048-bit secret key used for this
   account (see "Secret Key Generation and storage" above).
 * ``public_key`` -- the OpenPGP transferable public key derived
   from the secret key.
 * ``prefer_encrypt`` -- the user's own
   preferences on this account, either ``mutual`` or ``nopreference``.
   This SHOULD be set to ``nopreference`` by default.

If Autocrypt is enabled for a given account, the MUA SHOULD allow the
user to switch the setting for ``own_state.prefer_encrypt``, but this
choice might normally be hidden in a "preferences pane" or something
similar.

Please see :doc:`ui-examples` for specific examples of how this might
look.

Aliases
-------

If a user sends emails with multiple aliases throught the same account
the client SHOULD use the same autocrypt key for all aliases.  The
Autocrypt Setup Message is not designed to handle multiple keys.  In
addition syncronisation issues arrise if new keys for aliases are
created on different devices.

A client MAY allow to enable autocrypt only for a subset of the aliases
and allow configuring ``prefer_encrypt`` on a per alias basis.

Message Composition
+++++++++++++++++++

If an MUA is willing to compose encrypted mail, it SHOULD include some
UI mechanism at message composition time for the user to choose between
encrypted message or cleartext.  This may be as simple as a single
checkbox.

If the Autocrypt recommendation is ``disable`` for a given message,
the MUA MAY choose to avoid exposing this UI during message
composition at all.

If the Autocrypt recommendation is either ``available`` or
``encrypt``, the MUA SHOULD expose this UI during message composition
to allow the user to make a different decision.

