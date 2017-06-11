Autocrypt Level 0: Enabling encryption, avoiding annoyances
===========================================================

This document describes the basic capabilities required for a mail app
to be Autocrypt-capable at Level 0.  The design of Level 0 is driven by
usability concerns and by the realities of incremental deployment.  A user
may use both Autocrypt-enabled mail apps and traditional plain ones
and we'd like to avoid annoyances like unexpected unreadable mails
while supporting users who want to explicitly turn on encryption.

For ease of implementation and deployment, Level 0 does not support
multi-device configurations.  We intend to :doc:`support the multi-device
use case (and other features) as part of Level 1<next-steps>`.  We
want to keep Level 0 minimal enough that it's easy for developers to
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

As a simple measure of mitigation, Level 0 MUAs SHOULD check before
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
scope for Level 0.

Autocrypt Setup Message
-----------------------

For proper support of a multi-device scenario, it is necessary to have
bi-directional communication between different MUAs. This is possible
e.g. via access to a shared IMAP mailbox. Because of the complexity of
this approach however, multi-device support in the sense of devices
coordinating with each other is out of scope for Autocrypt Level 0. It
is still important to avoid "lock-in" of secret key material on a
particular client. For this reason, Autocrypt includes a way to
"export" the user's keys and the user's prefer-encrypt state for other clients to pick up,
asynchronously and with explicitly required user interaction.

The mechanism available in Autocrypt level 0 is a specially-formatted
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

- The Autocrypt Setup Message MUST contain an ``Autocrypt-Setup-Message: v0`` header.

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

An Autocrypt level 0 client MUST generate a setup code as UTF-8 string
of 24 uppercase alphanumeric characters, divided into six blocks of
four, separated by dashes. The dashes are part of the secret
code. This format holds about 124 bits of data. It is designed to be
unambiguous, pronounceable, and split into blocks that can be easily
kept in short term memory. For instance::

    AB1D-E2GH-IJK3-4NOP-Q5ST-XYZ6

An Autocrypt Setup Message payload that uses this structure for its
setup code SHOULD include the following ``Passphrase-Format`` header
in the outer OpenPGP armor::

    Passphrase-Format: alphanumeric

This OpenPGP header MUST NOT be present with this value if the Setup
Code does not match the format described above.

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

A Level 0 client MUST be able to create an Autocrypt Setup Message, to
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
   Setup Code.  If it decrypts the client SHOULD import the secret
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
	Autocrypt-Setup-Message: v0
	Content-type: multipart/mixed; boundary="==break0=="

	--==break0==
	Content-Type: text/plain

	This is the Autocrypt setup message.

	--==break0==
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
    Passphrase-Format: alphanumeric

    hQIMAxC7JraDy7DVAQ//SK1NltM+r6uRf2BJEg+rnpmiwfAEIiopU0LeOQ6ysmZ0
    CLlfUKAcryaxndj4sBsxLllXWzlNiFDHWw4OOUEZAZd8YRbOPfVq2I8+W4jO3Moe
    -----END PGP MESSAGE-----
    </pre>
	</body>
	</html>
	--==break0==--

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

During message composition, if the :mailheader:`From:` header of the
outgoing e-mail matches an address that the Autocrypt-capable agent
knows the secret key material for, it SHOULD include an Autocrypt
header. This header contains the associated public key material as
``key`` attribute, and the same sender address that is used in the
``From`` header in the ``addr`` attribute to confirm the
association. The most minimal Level 0 MUA will only include these two
attributes.

If the :mailheader:`From:` address changes during message composition
(E.g. if the user selects a different outbound identity), the
Autocrypt-capable client MUST change the :mailheader:`Autocrypt`
header appropriately.

See :ref:`mua-happypath` for examples of outbound headers and
the following sections for header format definitions and parsing.

..  _autocryptheaderformat:

Deriving a Parsed :mailheader:`Autocrypt` Header from a Message
---------------------------------------------------------------

The :mailheader:`Autocrypt` header has the following format::

    Autocrypt: addr=a@b.example.org; [type=0;] [prefer-encrypt=mutual;] key=BASE64

The ``addr`` attribute indicates the single recipient address this
header is valid for. In case this address differs from the one the MUA
considers the sender of the e-mail in parsing, which will usually be
the one specified in the :mailheader:`From` header, the entire header
MUST be treated as invalid.

The ``type`` and ``key`` attributes specify the type and data of the
key material.  For now the only supported type is ``0``, which
represents a specific subset of OpenPGP (see the next section), and is
also the default.  Headers with an unknown ``type`` MUST be treated as
invalid.  The value of the ``key`` attribute is a Base64
representation of the public key material.  This is a simple
ascii-armored key format without a checksum (which would then be Radix64)
and without pgp message markers (``---BEGIN...`` etc.).  For ease of
parsing, the ``key`` attribute MUST be the last attribute in the header.

The ``prefer-encrypt`` attribute can only occur with the value
``mutual``, any other value is undefined. Its presence in the header
indicates an agreement with encryption by default.

Additional attributes unspecified here are also possible before the
``key`` attribute.  If an attribute name starts with an underscore
(``_``), it is a "non-critical" attribute.  An attribute name without
a leading underscore is a "critical" attribute.  The MUA SHOULD ignore
any unsupported non-critical attribute and continue parsing the rest
of the header as though the attribute does not exist, but MUST treat
the entire header as invalid if it encounters a "critical" attribute
it doesn't support.

When parsing an incoming message, a MUA MUST examine all
:mailheader:`Autocrypt` headers, rather than just the first one.  If
there is more than one valid header, this MUST be treated as an error,
and all :mailheader:`Autocrypt` headers discarded as invalid.

.. todo::

   - Document why we skip on more than one valid header?

``type=0``: OpenPGP Based key data
++++++++++++++++++++++++++++++++++

For maximum interoperability, a certificate sent by an
Autocrypt-enabled Level 0 MUA MUST consist of an :rfc:`OpenPGP
"Transferable Public Key"<4880#section-11.1>`) containing exactly these five
OpenPGP packets:

 - a signing-capable primary key ``Kp``
 - a user id
 - a self signature
 - an encryption-capable subkey ``Ke``
 - a binding signature over ``Ke`` by ``Kp``

The content of the user id packet is only decorative. By convention, it
contains the same address used in the ``addr`` attribute in angle brackets,
conforming to the :rfc:`2822` grammar ``angle-addr``.

These packets MUST be assembled in binary format (not ASCII-armored),
and then base64-encoded.

A Level 0 MUA MUST be capable of processing and handling 2048-bit RSA
keys.  It SHOULD be capable of handling Curve 25519 keys (ed25519 for
``Kp`` and cv25519 for ``Ke``), but some underlying toolkits may not
yet support Curve 25519.  It MAY support other OpenPGP key formats.


Internal state storage
----------------------

.. note::

    You should be familiar with :ref:`mua-happypath` before reading the
    following.

We define the effective date of a message as the sending time of the
message as indicated by its :mailheader:`Date` header, or the time of
first receipt if that date is in the future or unavailable.

If a remote peer disables Autocrypt or drops back to using a
non-Autocrypt MUA only we must be able to disable sending encrypted
mails to this peer automatically.  MUAs capable of Autocrypt level 0
therefore MUST store state about the capabilities of their remote
peers.

Agents MAY also store additional information gathered for heuristic
purposes, or for other cryptographic schemes.  However, in order to
support future syncing of Autocrypt state between agents, it is
critical that Autocrypt-capable agents maintain the state specified
here.

Conceptually, we represent this state as a table named
``autocrypt_peer_state`` indexed by the peer's :doc:`canonicalized
e-mail address <address-canonicalization>` and key type.  In level 0,
there is only one type, ``0``, so level 0 agents can implement this by
indexing only the peer's e-mail address.

For each e-mail address and type, an agent MUST store the following
attributes:

* ``last_seen``: UTC timestamp of the most recent effective date of
  all processed messages for this peer.
* ``last_seen_autocrypt``: UTC timestamp of the most recent effective
  date of all processed messages for this peer that contained a valid
  Autocrypt header.
* ``key``: the raw key material
* ``state``: a tri-state: ``nopreference``, ``mutual`` or ``reset``

.. note::

  - The above is not necessarily an exhaustive list of peer state to
    keep; implementors are encouraged to improve upon this scheme as
    they see fit. Suggestions for additional (optional) state that an
    agent may want to keep about a peer can be found in
    :doc:`optional-state`.
  - An implementation MAY also choose to use keys from other sources
    (e.g. local keyring) at own discretion.
  - If an implementation chooses to automatically ingest keys from a
    ``application/pgp-keys`` attachment, it should only do so if they
    have a matching user id.


Updating Autocrypt Peer State
-----------------------------

Incoming messages may be processed by an Autocrypt-client at different
times, such as upon receipt or display. When this happens, the
Autocrypt state for the sending peer is updated with this new
information. This update process depends on:

- the "effective date" of the message.

- the ``key`` and ``prefer-encrypt`` attributes of the single valid
  parsed :mailheader:`Autocrypt` header (see above), if available.

If the parsed Autocrypt header is unavailable, and the effective
message date is more recent than the current value of ``last_seen``,
update the state as follows and terminate:

- set ``last_seen`` to the effective message date
- set ``state`` to ``reset``

Otherwise, if either the effective message date is older than the
``last_seen_autocrypt`` value, or it is older than the current value
of ``last_seen`` plus the parsed Autocrypt header is unavailable, no
changes are required and the update process terminates.

At this point, the message in processing contains the most recent
Autocrypt header. Update the state as follows:

- set ``key`` to the corresponding value of the Autocrypt header
- set ``last_seen_autocrypt`` to the effective message date

If the effective date of the message is more recent than or equal to
the current ``last_seen`` value, it is also the most recent message
overall. Additionally update the state as follows:

- set ``last_seen`` to the effective message date
- set ``state`` to ``mutual`` if the Autocrypt header contained a
  ``prefer-encrypt=mutual`` attribute, or ``nopreference`` otherwise

.. _spam-filters:

.. todo::

   the spec currently doesn't say how to integrate Autocrypt
   processing on message receipt with spam filtering.  Should we say
   something about not doing Autocrypt processing on message receipt
   if the message is believed to be spam?


Provide a recommendation for message encryption
-----------------------------------------------

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
   encrypt the message, but do not default to encryption.  Prepare the
   message in cleartext.  If the user manually enables encryption,
   warn them that the recipient may not be able to read the message.

 * ``available``: Enable UI that would allow the user to choose to
   encrypt the message, but do not default to encryption.  Prepare the
   message in cleartext.

 * ``encrypt``: Enable UI that would allow the user to choose to send
   the message in cleartext, and default to encryption.  Prepare the
   message as an encrypted message.

Recommendations for single-recipient messages
+++++++++++++++++++++++++++++++++++++++++++++

The Autocrypt recommendation for a message composed to a single
recipient with e-mail address ``A`` depends primarily on the value
stored in ``autocrypt_peer_state[A]``. It is derived by the following
algorithm:

1. If the ``key`` is ``null``, the recommendation is ``disable``.
2. If the ``key`` is known for some reason to be unusable for
   encryption (e.g. it is otherwise known to be revoked or expired),
   then the recommendation is ``disable``.
3. If the message is composed as a reply to an encrypted message, then
   the recommendation is ``encrypt``.
4. If ``state`` is ``mutual``, and the user's own
   ``own_state.prefer_encrypt`` is ``mutual`` as well, then the
   recommendation is ``encrypt``.
5. If ``state`` is ``reset`` and the ``last_seen_autocrypt`` is more
   than one month ago, then the recommendation is ``discourage``.

Otherwise, the recommendation is ``available``.

Recommendations for messages to multiple addresses
++++++++++++++++++++++++++++++++++++++++++++++++++

For level 0 agents, the Autocrypt recommendation for a message
composed to multiple recipients is derived from the recommendations
for each recipient individually.

If any recipient has a recommendation of ``disable`` then the message
recommendation is ``disable``.

If the message being composed is a reply to an encrypted message, or
if every recipient other than "myself" (the e-mail address that the
message is ``From:``) has a recommendation of ``encrypt`` then the
message recommendation is ``encrypt``.

If any recipient has a recommendation of ``discourage`` then the message
recommendation is ``discourage``.

Otherwise, the message recommendation is ``available``.

Cleartext replies to encrypted mail
+++++++++++++++++++++++++++++++++++

As you can see above, in the common use case, a reply to an encrypted
message will also be encrypted. Due to Autocrypt's opportunistic
approach to key discovery, however, it's possible that the ``key``
state in the recipient's Autocrypt peer state is ``null``, which means
the reply will be sent in the clear.

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
because we want to accomodate a user-friendly level 0 MUA that stays
silent and does not impede the user's ability to reply.  Opportunistic
encryption means we can't guarantee encryption in every case.

Encrypt outbound mail as requested
----------------------------------

As the user composes mail, in some circumstances, the MUA may be
instructed by the user to encrypt the message.  If the recipient's
keys are all of ``type=0``, and the sender has keys for all recipients
(as well as themselves), they should construct the encrypted message
as a :rfc:`PGP/MIME <3156>` encrypted+signed message, encrypted to all
recipients and the public key whose secret is controlled by the MUA
itself.

If the recommendation is ``discourage`` the user SHOULD be presented
with a clear warning explaining that there is reason to believe one or
more recipients will not be able to read the mail if it is sent
encrypted.  This message SHOULD state which recipients are considered
problematic and provide useful information to help the user guage the
risk.  The optional counters and user-agent state described in
:doc:`optional-state` can be useful for this message.

For messages that are going to be encrypted when sent, the MUA MUST
take care not to leak the cleartext of drafts or other
partially-composed messages to their e-mail provider (e.g. in the
"Drafts" folder).

If there is a chance that a message could be encrypted, the MUA
SHOULD encrypt drafts only to itself before storing it remotely.

Specific User Interface Elements
--------------------------------

Ideally, Autocrypt users see very little UI.  However, some UI is
inevitable if we want users to be able to interoperate with existing,
non-Autocrypt users.

Account Preferences
+++++++++++++++++++

Level 0 MUAs MUST allow the user to disable Autocrypt completely for
each account they control.  For level 0, we expect most MUAs to have
Autocrypt disabled by default.

Level 0 MUAs maintain an internal structure ``own_state`` for each
account on which Autocrypt is enabled. ``own_state`` has the following
members:

 * ``secret_key`` -- the secret key used for this account (see "Secret
   Key Generation and storage" above).
 * ``key`` -- the OpenPGP transferable public key derived from
   ``secret_key``.
 * ``prefer_encrypt`` -- the user's own
   preferences on this account, either ``mutual`` or ``nopreference``.
   This SHOULD be set to ``nopreference`` by default.

If Autocrypt is enabled for a given account, the MUA SHOULD allow the
user to switch the setting for ``own_state.prefer_encrypt``, but this
choice might normally be hidden in a "preferences pane" or something
similar.

Please see :doc:`ui-examples` for specific examples of how this might
look.

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

.. todo::

   - Should we really recommend hiding the encrypt UI? This reduces UI
     consistency!
