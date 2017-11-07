Autocrypt Level 1: Enabling encryption, avoiding annoyances
===========================================================

Autocrypt makes it easy for people to encrypt email.  This document
describes the basic capabilities required for a mail app to be
Autocrypt-capable at Level 1.

The design of Level 1 is driven by usability concerns and by the
realities of incremental deployment. A user may mix both
Autocrypt-enabled MUAs and traditional MUAs, and we'd
like to avoid annoyances like unexpectedly unreadable mails while also
supporting users who want to explicitly turn on encryption.

For ease of implementation and deployment, Level 1 focuses on the use
of Autocrypt on a single device.  We intend to :doc:`support
multi-device synchronization (and other features) as part of Level
2<next-steps>`.  We want to keep Level 1 simple enough that it's easy
for developers to adopt it so we can drive efforts from real-life
experiences as soon as possible.

.. only:: builder_html

   .. contents::

.. only:: builder_readthedocs

   .. contents::

Overview
--------

Approach and High Level Overview
++++++++++++++++++++++++++++++++

Autocrypt's primary goal is to automate both secret and public key
management so that users can encrypt mail without specialized
knowledge.

This specification adds an :ref:`Autocrypt-specific mail header
<autocrypt-header>` to outgoing mails, which contains, among other
information, the sender's :term:`public key`.  Transferring public
keys in-band means that key discovery in Autocrypt does not require
external infrastructure like OpenPGP keyservers or x509 PKI.

Autocrypt provides a :ref:`set of rules <update-peers>` that
tracks this information for each communication peer.  Autocrypt uses
this information to determine whether encryption is possible and makes
a :ref:`recommendation <recommendation>` about whether encryption
should be enabled for a given set of recipients.

Autocrypt aggressively distributes keys, but conservatively recommends
encryption to avoid disruption to established email workflows.
Specifically, Autocrypt only recommends that an email be encrypted if
encryption is possible, and:

1) The sender specifically requests encryption during message
   composition;
2) The email is in reply to an encrypted message; or,
3) The sender and the recipients have explicitly stated that they
   :ref:`prefer <prefer-encrypt>` encrypted email.


Requirements on MUA/E-mail Provider interactions
++++++++++++++++++++++++++++++++++++++++++++++++

Autocrypt tries to impose minimal requirements on :term:`MUA` and
e-mail service interactions.  Specifically, an Autocrypt-capable MUA
needs to be able to:

- Control the contents of outgoing e-mail including the ability to set
  custom e-mail headers;

- Send e-mail on its own (required by the :ref:`Autocrypt Setup
  Message <setup-message>`);

- Read whole, raw e-mails including message headers; and,

- Optionally, scan the user's mailbox for mail with
  specific headers.

If a particular e-mail account does not expose one of the required
features (e.g., if it only exposes a javascript-driven web interface
for message composition that does not allow setting e-mail headers),
then the e-mail account cannot be used with Autocrypt.  An
Autocrypt-capable MUA may still access and control the account, but it
will not be able to enable Autocrypt on it.


Autocrypt Internal State
++++++++++++++++++++++++

An Autocrypt MUA needs to associate information with the peers it
communicates with and the accounts it controls.

.. _peers:

Communication Peers
~~~~~~~~~~~~~~~~~~~

Each communication peer is identified by an e-mail address.  Autocrypt
associates state with each peer.  Conceptually, we represent this
state as a table named ``peers``, which is indexed by the peer's
:doc:`canonicalized e-mail address <address-canonicalization>`, .

For the peer with the address ``addr``, an MUA MUST associate the
following attributes with ``peers[addr]``:

* ``last_seen``: The UTC timestamp of the most recent effective date
  (:ref:`definition <effective_date>`) of all messages that the MUA has
  processed from this peer.
* ``autocrypt_timestamp``: The UTC timestamp of the most recent
  effective date of all messages containing a valid ``Autocrypt`` header
  that the MUA has processed from this peer.
* ``public_key``: The value of the ``keydata`` attribute derived from
  the most recent ``Autocrypt`` header received from the peer.
* ``prefer_encrypt``: The ``prefer-encrypt`` value (either
  ``nopreference`` or ``mutual``) derived from most recent ``Autocrypt``
  header received from the peer.

Autocrypt-capable MUAs that implement :ref:`Gossip <gossip>` should
also associate the following additional attributes with
``peers[addr]``:

* ``gossip_timestamp``: the UTC timestamp of the most recent effective
  date of all messages containing a valid ``Autocrypt-Gossip`` header
  about the peer.
* ``gossip_key``: the value of the ``keydata`` attribute derived from
  the most recent message containing a valid ``Autocrypt-Gossip``
  header about the peer.

How this information is managed and used is discussed in :ref:`peer-management`.

.. _accounts:

Accounts controlled by the MUA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Level 1 MUA maintains an internal structure ``accounts`` indexed by
the account's :doc:`canonicalized e-mail address
<address-canonicalization>` (``addr``).  For each account controlled
by the MUA, ``accounts[addr]`` has the following attributes:

 * ``enabled``: a boolean value, indicating whether Autocrypt is
   enabled for this account.
 * ``secret_key``: The RSA secret key material used for
   the account (see :ref:`secretkeys`).
 * ``public_key``: The OpenPGP transferable public key (:rfc:`OpenPGP
   "Transferable Public Key"<4880#section-11.1>`) derived
   from the secret key.
 * ``prefer_encrypt``: The user's encryption
   preference for this account.  This is either ``mutual`` or ``nopreference``.
   This SHOULD default to ``nopreference``.

If ``accounts[addr].enabled`` is ``true``, the MUA SHOULD allow the
user to switch the setting for ``accounts[addr].prefer_encrypt``.
This choice might be hidden in something like a "preferences pane".
See :ref:`preference-ui` for a specific example of how this could
look.

How this information is managed and used is discussed in :ref:`account-management`.

.. _peer-management:

Peer State Management
---------------------

An Autocrypt MUA updates the state it holds for each communication
peer using the e-mails received from that peer.  Specifically,
Autocrypt updates the state using the ``Autocrypt`` e-mail header.

.. _autocrypt-header:

The ``Autocrypt`` Header
++++++++++++++++++++++++

The ``Autocrypt`` header has the following format::

    Autocrypt: addr=a@b.example.org; [prefer-encrypt=mutual;] keydata=BASE64

The ``addr`` attribute is mandatory, and contains the single recipient
address this header is valid for.  If this address differs from
the one in the ``From`` header, the entire ``Autocrypt`` header MUST be treated
as invalid.

.. _prefer-encrypt:

The ``prefer-encrypt`` attribute is optional and can only occur with
the value ``mutual``.  Its presence in the ``Autocrypt`` header
indicates an agreement to enable encryption by default with other peers who have
the same preference.  An Autocrypt Level 1 MUA that sees the
attribute with any other value (or that does not see the attribute at
all) should interpret the value as ``nopreference``.

The ``keydata`` attribute is mandatory, and contains the key data for
the specified ``addr`` recipient address.  The value of the
``keydata`` attribute is a Base64 representation of the binary
:rfc:`OpenPGP "Transferable Public Key"<4880#section-11.1>`. For ease
of parsing, the ``keydata`` attribute MUST be the last attribute in
this header.

Additional attributes are possible before the ``keydata``
attribute.  If an attribute name starts with an underscore (``_``), it
is a "non-critical" attribute.  An attribute name without a leading
underscore is a "critical" attribute.  The MUA SHOULD ignore any
unsupported non-critical attributes and continue parsing the rest of
the header as though the attribute does not exist.  It MUST treat the
entire ``Autocrypt`` header as invalid if it encounters a "critical"
attribute that it doesn't support.

To introduce incompatible changes, future versions of Autocrypt may
send multiple Autocrypt headers, and hide the incompatible headers
from Level 1 MUAs by using critical attributes.  According to the
above rules, such headers will be judged invalid, and discarded by
level 1 clients.  Such an update to the specification will also have
to describe how clients deal with multiple valid headers.


OpenPGP Based key data
~~~~~~~~~~~~~~~~~~~~~~

The ``keydata`` sent by an Autocrypt-enabled Level 1 MUA MUST consist
of an :rfc:`OpenPGP "Transferable Public Key"<4880#section-11.1>`
containing exactly these five OpenPGP packets:

 - a signing-capable primary key
 - a user id
 - a self signature over the user id by the primary key
 - an encryption-capable subkey
 - a binding signature over the subkey by the primary key

The content of the user id packet is only decorative. By convention, it
contains the same address used in the ``addr`` attribute placed in angle brackets.
(This makes it conform to the :rfc:`5322` grammar ``angle-addr``.) For compatibility
concerns, the user id SHOULD NOT be an empty string.

These packets MUST be assembled in binary format (not ASCII-armored),
and then base64-encoded.

A Level 1 MUA MUST be capable of processing and handling 2048-bit and
3072-bit RSA public keys.  It MAY support other OpenPGP key formats
found in an Autocrypt header (for example, by passing it agnostically
to an OpenPGP backend for handling).

Header injection in outbound mail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

During message composition, if the ``From:`` header of the outgoing
e-mail (the ``from-addr``) matches an address for which
``accounts[from-addr].enabled`` is ``true`` and the Autocrypt-capable
MUA has secret key material (``accounts[from-addr].secret_key``), the
MUA SHOULD include an Autocrypt header.

This header MUST contain the corresponding public key material
(``accounts[from-addr].public_key``) as the ``keydata`` attribute, and
``from-addr`` as the ``addr`` attribute.  The most minimal Level 1
compliant MUA will only include these two attributes.  If
``accounts[from-addr].prefer_encrypt`` is set to ``mutual``, then the
header MUST have a ``prefer-encrypt`` attribute with the value
``mutual``.

The MUA MUST NOT include more than one valid Level 1 ``Autocrypt``
header (see :ref:`update-peers`).

If the ``From`` address changes during message composition (e.g., if
the user selects a different outbound identity), then the MUA MUST
change the ``Autocrypt`` header accordingly.

An MUA SHOULD send out the same ``keydata`` value in all messages from
a given outbound identity, irrespective of the message's recipients.
If a new OpenPGP certificate is generated (e.g., if the user has a new
key, or updates some OpenPGP metadata), then all subsequent outbound
Autocrypt headers SHOULD use the new certificate for the ``keydata``
attribute.

See :ref:`example-headers` for examples of outbound headers and
the following sections for header format definitions and parsing.

..  _autocryptheaderformat:

Internal state storage
++++++++++++++++++++++

See :ref:`peers` for the information stored for each
communication peer.

Autocrypt MUAs keep state about each peer, to handle
several nuanced situations that have caused trouble or annoyance in the
past.  This state is updated even when the peer sends mail without an
``Autocrypt`` header.

For example, if a remote peer disables Autocrypt or drops back to
only using a non-Autocrypt MUA, we must stop sending
encrypted mails to this peer automatically.

In addition to the per-peer state described in :ref:`peers`,
MUAs MAY also store other information gathered for heuristic
purposes, or for other cryptographic schemes (see
:doc:`optional-state` for some example ideas).

However, in order to support future synchronization of Autocrypt state
between MUAs, it is critical that Autocrypt-capable MUAs maintain the
state specified here, regardless of what additional state they track.

.. note::

  - An implementation MAY also choose to use keys from other sources
    (e.g., a local keyring) at its own discretion.
  - If an implementation chooses to automatically ingest a key from an
    ``application/pgp-keys`` attachment as though it was found in an
    ``Autocrypt`` header, it should only do so if the attached key has
    a :rfc:`User ID <4880#section-5.11>` that matches the message's
    ``From`` address.

.. _update-peers:

Updating Autocrypt Peer State
+++++++++++++++++++++++++++++

Incoming messages may be processed to update the ``peers`` entry for
the sender identified by ``from-addr`` as extracted from the ``From``
header, by an MUA at receive or display time.

Messages SHOULD be ignored (i.e., ``peers[from-addr]`` SHOULD NOT be
updated) in the following cases:

  - The content-type is ``multipart/report``. In this case, it can be assumed
    the message was auto-generated. This avoids triggering a ``reset``
    state from received Message Disposition Notifications (:rfc:`3798`).

  - There is more than one address in the ``From`` header.

  - The MUA believes the message to be spam. If the user marks the
    message as not being spam the message MAY then be processed for
    ``Autocrypt`` headers.

When parsing an incoming message, an MUA SHOULD examine all ``Autocrypt``
headers, rather than just the first one. If there is more than one
valid header, this SHOULD be treated as an error, and all ``Autocrypt``
headers discarded as invalid.

Updating ``peers[from-addr]`` depends on:

.. _effective_date:

- the ``effective date`` of the message, which we define as the sending
  time of the message as indicated by its ``Date`` header, or the time
  of receipt if that date is in the future or unavailable.

- the ``keydata`` and ``prefer-encrypt`` attributes of the single valid
  ``Autocrypt`` header (see above), if available.

The update process proceeds as follows:

1. If the message's effective date is older than the
   ``peers[from-addr].autocrypt_timestamp`` value, then no changes are
   required, and the update process terminates.

2. If the message's effective date is more recent than
   ``peers[from-addr].last_seen`` then set
   ``peers[from-addr].last_seen`` to the message's effective date.

3. If the ``Autocrypt`` header is unavailable, no further changes are
   required and the update process terminates.

4. Set ``peers[from-addr].autocrypt_timestamp`` to the message's
   effective date.

5. Set ``peers[from-addr].public_key`` to the corresponding
   ``keydata`` value of the ``Autocrypt`` header.

6. Set ``peers[from-addr].prefer_encrypt`` to the corresponding
   ``prefer-encrypt`` value of the ``Autocrypt`` header.

.. _recommendation:

Provide a recommendation for message encryption
+++++++++++++++++++++++++++++++++++++++++++++++

On message composition, an Autocrypt-capable MUA
can decide whether to try to encrypt the new e-mail
message.  Autocrypt provides a recommendation for the MUA.

Any Autocrypt-capable MUA may have other means for making this
decision outside of Autocrypt (see :doc:`other-crypto-interop`).
Autocrypt provides a recommendation, but there is no
requirement for Autocrypt-capable MUAs to follow this
recommendation.

That said, all Autocrypt-capable MUAs should be able to calculate
the same Autocrypt recommendation.

The Autocrypt recommendation depends on the recipient
addresses of the draft message.  When the user changes the
recipients, the Autocrypt recommendation may change.

The output of the Autocrypt recommendation algorithm has two elements:

 * ``ui-recommendation``: a single state recommending the state of the
   encryption user interface, described below.
 * ``target-keys``: a map of recipient addresses to public keys.

``ui-recommendation`` can take four possible values:

 * ``disable``: Disable or hide any UI that would allow the user to
   choose to encrypt the message.  This happens iff encryption is not
   immediately possible.

 * ``discourage``: Enable UI that would allow the user to choose to
   encrypt the message, but do not default to encryption. If the user
   manually enables encryption, the MUA SHOULD warn that the recipient
   may not be able to read the message. This warning message MAY be
   supplemented using optional counters and user-agent state as
   suggested in :doc:`optional-state`.

 * ``available``: Enable UI that would allow the user to choose to
   encrypt the message, but do not default to encryption.

 * ``encrypt``: Enable UI that would allow the user to choose to send
   the message in cleartext, and default to encryption.

Recommendations for single-recipient messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Autocrypt recommendation for a message composed to a single
recipient with the e-mail address ``to-addr`` depends primarily on the
value stored in :ref:`peers[to-addr] <peers>`.

Determine if encryption is possible
___________________________________

If there is no ``peers[to-addr]``, then set ``ui-recommendation`` to
``disable``, and terminate.

For the purposes of the rest of this recommendation, if either
``public_key`` or ``gossip_key`` is revoked, expired, or otherwise
known to be unusable for encryption, then treat that key as though it
were ``null`` (not present).

If both ``public_key`` and ``gossip_key`` are ``null``, then set
``ui-recommendation`` to ``disable`` and terminate.

Otherwise, we derive the recommendation using a two-phase algorithm.
The first phase computes the ``preliminary-recommendation``.

Preliminary Recommendation
__________________________

If either ``public_key`` is ``null``, or ``autocrypt_timestamp`` is
more than a month older than ``gossip_key_timestamp``, set
``target-keys[to-addr]`` to ``gossip_key`` and set
``preliminary-recommendation`` to ``discourage`` and skip to the
:ref:`final-recommendation-phase`.

Otherwise, set ``target-keys[to-addr]`` to ``public_key``.

If ``autocrypt_timestamp`` is more than a month older than
``last_seen``, set ``preliminary-recommendation`` to ``discourage``.

Otherwise, set ``preliminary-recommendation`` to ``available``.

.. _final-recommendation-phase:


Deciding to Encrypt by Default
______________________________

The final phase turns on encryption by setting ``ui-recommendation`` to
``encrypt`` in two scenarios:

- If ``preliminary-recommendation`` is either ``available`` or
  ``discourage``, and the message is composed as a reply to an
  encrypted message, or
- If the ``preliminary-recommendation`` is ``available`` and both
  ``peers[to-addr].prefer_encrypt`` and
  ``accounts[from-addr].prefer_encrypt`` are ``mutual``.

Otherwise, the ``ui-recommendation`` is set to
``preliminary-recommendation``.

Recommendations for messages to multiple addresses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For level 1 MUAs, the Autocrypt recommendation for a message composed
to multiple recipients, we derive the message's recommendation from
the recommendations for each recipient individually.

The aggregate ``target-keys`` for the message is the merge of all
recipient ``target-keys``.

The aggregate ``ui-recommendation`` for the message is derived as
follows:

1. If any recipient has a ``ui-recommendation`` of ``disable``, then
   the message's ``ui-recommendation`` is ``disable``.
2. If every recipient has a ``ui-recommendation`` of ``encrypt``,
   then the message ``ui-recommendation`` is ``encrypt``.
3. If any recipient has a ``ui-recommendation`` of ``discourage``,
   then the message ``ui-recommendation`` is ``discourage``.

Otherwise, the message ``ui-recommendation`` is ``available``.

While composing a message, a situation might occur where the
``ui-recommendation`` is ``available``, the user has explicitly
enabled encryption, and then modifies the list of recipients in a way
that changes the ``ui-recommendation`` to ``disable``. When this
happens, the MUA should not disable encryption without communicating
this to the user.  A graceful way to handle this situation is to save
the enabled state, and only prompt the user about the issue when they
send the mail.

Mail Encryption
+++++++++++++++

.. note::

   An e-mail that is said to be "encrypted" here will be both signed
   and encrypted in the cryptographic sense.

An outgoing e-mail will be sent encrypted in either of two cases:

- the Autocrypt recommendation for the list of recipients is
  ``encrypt``, and not explicitly overridden by the user, or
- the Autocrypt recommendation is ``available`` or ``discourage``,
  and the user chose to encrypt.

When encrypting, the MUA MUST construct the encrypted message as a
:rfc:`PGP/MIME <3156>` message that is signed by the user's Autocrypt
key, and encrypted to the currently known Autocrypt key of each
recipient, as well as the sender's Autocrypt key.

E-mail Drafts
~~~~~~~~~~~~~

For messages that are going to be encrypted when sent, the MUA MUST
take care to not leak the cleartext of drafts or other
partially composed messages to their e-mail provider (e.g., in the
"Drafts" folder). If there is a chance that a message could be
encrypted, the MUA SHOULD encrypt the draft only to itself before storing
it remotely. The MUA SHOULD NOT sign drafts.


Cleartext replies to encrypted mail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the common case, a reply to an encrypted message will also be
encrypted. Due to Autocrypt's opportunistic approach to key discovery,
however, it is possible that keys for some of the recipients may not
be available, and, as such, a reply can only be sent in the clear.

To avoid leaking cleartext from the original encrypted message in this
case, the MUA MAY prepare the cleartext reply without including any of
the typically quoted and attributed text from the previous message.
Additionally, the MUA MAY include some text in the message body
describing why the usual quoted text is missing.  An example of such
copy can be found in :ref:`_example-cant-encrypt-reply`.

The above recommendations are only "MAY" and not "SHOULD" or "MUST"
because we want to accommodate a user-friendly Level 1 MUA that stays
silent and does not impede the user's ability to reply.  Opportunistic
encryption means we can't guarantee encryption in every case.

.. _key-gossip:

Key Gossip
++++++++++

It is a common use case to send an encrypted mail to a group of
recipients. To ensure that these recipients can encrypt messages when
replying to that same group, the keys of all recipients can be
included in the encrypted payload. This does not include BCC
recipients, which by definition must not be revealed to other
recipients.

The ``Autocrypt-Gossip`` header has the format as the ``Autocrypt``
header (see `autocryptheaderformat`_). Its ``addr`` attribute
indicates the recipient address this header is valid for as usual, but
may relate to any recipient in the ``To`` or ``Cc`` header.

Key Gossip Injection in Outbound Mail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An Autocrypt MUA MAY include ``Autocrypt-Gossip`` headers in messages
with more than one recipient. These headers MUST be placed in the root
MIME part of the encrypted message payload. The encrypted payload in
this case contains one Autocrypt-Gossip header for each recipient,
which MUST include ``addr`` and ``keydata`` attributes with the
corresponding values for the recipient identified by ``gossip-addr``
as stored in ``peers[gossip-addr]``.  It SHOULD NOT contain a
``prefer-encrypt`` attribute.

To avoid leaking metadata about a third party in the clear, an
``Autocrypt-Gossip`` header SHOULD NOT be added outside an encrypted
MIME part.

Updating Autocrypt Peer State from Key Gossip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An incoming message may contain one or more ``Autocrypt-Gossip``
headers in the encrypted payload. Each of these headers may update the
Autocrypt peer state of the gossiped recipient identified by its
``addr`` value (referred to here as ``gossip-addr``) in the following
way:

1. If ``gossip-addr`` does not match any recipient in the mail's
   ``To`` or ``Cc`` header, the update process terminates (i.e.,
   header is ignored).

2. If ``peers[gossip-addr].gossip_timestamp`` is more recent than the
   message's effective date, then the update process terminates.

3. Set ``peers[gossip-addr].gossip_timestamp`` to the message's
   effective date.

4. Set ``peers[gossip-addr].gossip_key`` to the value of the
   ``keydata`` attribute.


.. _account-management:

Managing accounts controlled by the MUA
---------------------------------------

See :ref:`accounts` for a definition of the structure of
information stored about the MUA's own e-mail accounts.


.. _secretkeys:

Secret key generation and storage
+++++++++++++++++++++++++++++++++

The MUA SHOULD generate and store two RSA 3072-bit secret keys for the
user, one for signing and self-certification, and the other for
decrypting.  An MUA with hardware constraints (e.g., one using an external
crypto token) MAY choose to generate and store 2048-bit RSA secret
keys instead.  The MUA MUST be capable of assembling these keys into
an OpenPGP certificate (:rfc:`RFC 4880 "Transferable Public
Key"<4880#section-11.1>`) that indicates these capabilities.

The secret key material should be protected from access by other
applications or co-tenants of the device at least as well as the
passwords the MUA retains for the user's IMAP or SMTP accounts.

Secret key protection at rest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The MUA SHOULD NOT protect the secret key with a password. All
encrypted outgoing messages MUST be signed, which would require the
user to enter the password for both reading and sending mail. This
introduces too much friction to become part of a routine daily workflow.
Protection of the user's keys at rest and other files is achieved more
easily and securely with full-disk encryption.


.. _multiaccounts:

Handling Multiple Accounts and Aliases
++++++++++++++++++++++++++++++++++++++

An MUA that is capable of connecting to multiple e-mail accounts
SHOULD have a separate and distinct Autocrypt ``accounts[from-addr]``
for each e-mail account with the address ``from-addr``.

A multi-account MUA MAY maintain a single ``peers`` table that merges
information from e-mail received across all accounts for the sake of
implementation simplicity.  While this results in some linkability
between accounts (the effect of mails sent to one account can be
observed by activity on the other account), it provides a more uniform
and predictable user experience.  Any linkability concerns introduced by
Autocrypt can be mitigated by using a different client for each e-mail
account.

Sometimes a user may be able to send and receive emails with multiple
distinct e-mail addresses ("aliases") via a single account.  For the
purposes of Autocrypt, the MUA SHOULD treat each specific alias as a
distinct account.


Avoiding MUA Conflicts
++++++++++++++++++++++

If more than one Autocrypt-enabled MUA generates a key and then
distributes it to communication peers, encrypted mail sent to the user
is only readable by the MUA that sent the last message. This can lead
to behavior that is unpredictable and confusing for the user.


See section :ref:`getting_started` for guidance on how to detect and
avoid such a situation.


.. _`setup-message`:

Autocrypt Setup Message
+++++++++++++++++++++++

To avoid "lock-in" of secret key material on a particular MUA,
Autocrypt level 1 includes a way to "export" the user's keys and her
:ref:`prefer-encrypt state <accounts>` for other MUAs to pick up,
asynchronously and with explicitly required user interaction.

The mechanism available is a specially-formatted e-mail message called
the Autocrypt Setup Message.  An already-configured Autocrypt MUA
can generate an Autocrypt Setup Message, and send it to itself.  A
not-yet-configured Autocrypt MUA (a new MUA in a multi-device
case, or recovering from device failure or loss) can import the
Autocrypt Setup Message and recover the ability to read existing
messages.

An Autocrypt Setup Message is protected with a :ref:`Setup Code
<setup-code>`.

Message Structure
~~~~~~~~~~~~~~~~~

The Autocrypt Setup Message itself is an e-mail message with a
specific format. While the message structure is complex, it is
designed to be easy to pack and unpack using common OpenPGP tools,
both programmatically and manually.

- Both the To and From headers MUST be the address of the user account.

- The Autocrypt Setup Message MUST contain an ``Autocrypt-Setup-Message: v1`` header.

- The Autocrypt Setup Message MUST have a ``multipart/mixed`` structure,
  and it MUST have as first part a human-readable description about
  the purpose of the message (e.g. ``text/plain`` or ``text/html`` or
  ``multipart/alternative``).

- The second mime part of the message MUST have the content-type
  ``application/autocrypt-setup``. It consists of the user's
  ASCII-armored secret key, encrypted in an ASCII-armored :rfc:`RFC
  4880 Symmetrically Encrypted Data Packet<4880#section-5.7>`

- There MAY be text above or below the ASCII-armored encrypted data in
  the second MIME part, which MUST be ignored while processing. This
  allows implementations to optionally add another human-readable
  explanation.

- The encrypted payload MUST begin with an ASCII-armored :rfc:`RFC
  4880 Transferable Secret Key<4880#section-11.2>`. All trailing data
  after the ASCII-armor ending delimiter MUST be stripped before
  processing the secret key. The ASCII-armored secret key SHOULD have
  an ``Autocrypt-Prefer-Encrypt`` header that contains the current
  ``accounts[addr].prefer_encrypt`` setting.

- The symmetric encryption algorithm used MUST be AES-128.
  The passphrase MUST be the Setup Code (see below), used
  with :rfc:`OpenPGP's salted+iterated S2K algorithm
  <4880#section-3.7.1.3>`.

.. _setup-code:

Setup Code
~~~~~~~~~~

The Setup Code MUST be generated by the implementation itself using a
`Cryptographically secure pseudorandom number generator (CSPRNG)
<https://en.wikipedia.org/wiki/Cryptographically_secure_pseudorandom_number_generator>`_,
and presented directly to the user for safekeeping. It MUST NOT be
included in the cleartext of the Autocrypt Setup Message, or otherwise
transmitted over e-mail.

An Autocrypt Level 1 MUA MUST generate a Setup Code as UTF-8 string
of 36 numeric characters, divided into nine blocks of four, separated
by dashes. The dashes are part of the secret code and there are no
spaces. This format holds about 119 bits of entropy. It is designed to
be unambiguous, pronounceable, script-independent (chinese, cyrillic
etc.), easily input on a mobile device and split into blocks that are
easily kept in short term memory. For instance::

    9503-1923-2307-
    1980-7833-0983-
    1998-7562-1111

An Autocrypt Setup Message that uses this structure for its Setup Code
SHOULD include a ``Passphrase-Format`` header with value
``numeric9x4`` in the ASCII-armored data. This allows providing a
specialized input form during decryption, with greatly improved
usability.

As a further measure to improve usability, it is RECOMMENDED to reveal
the first two digits of the first block in a ``Passphrase-Begin``
header, sacrificing about 7 bits of entropy. Those digits can be
pre-filled during decryption, which reassures the user that they have
the correct code before typing the full 36 digits. It also helps
mitigate a possible type of phishing attack that asks the user to
input their Setup Code.

The headers might look like this::

    Passphrase-Format: numeric9x4
    Passphrase-Begin: 95

If those digits are included in the headers, they may also
be used in the descriptive text that is part of the Setup Message, to
distinguish different messages.

Setup Message Creation
~~~~~~~~~~~~~~~~~~~~~~

An Autocrypt MUA MUST NOT create an Autocrypt Setup Message without
explicit user interaction.  When the user takes this action for a
specific account, the MUA:

 * Generates a Setup Code.
 * Optionally, displays the Setup Code to the user, prompts the user
   to write it down, and then hides it and asks the user to re-enter
   it before continuing.  This minor annoyance is a recommended
   defense against worse annoyance: it ensures that the code was
   actually written down and the Autocrypt Setup Message is not
   rendered useless.
 * Produces an ASCII-armored, minimized :rfc:`OpenPGP Transferable Secret
   Key <4880#section-11.2>` out of the key associated with that account.
 * Symmetrically encrypts the OpenPGP transferable secret key using
   the Setup Code as the passphrase.
 * Composes a new self-addressed e-mail message that contains the
   payload as a MIME part with the appropriate Content-Type and other
   headers.
 * Sends the generated e-mail message to its own account.
 * Suggests to the user to either back up the message or to import it
   from another Autocrypt-capable MUA.

A Level 1 MUA MUST be able to create an Autocrypt Setup Message, to
preserve users' ability to recover from disaster, and to choose to use
a different Autocrypt-capable MUA in the future.


Setup Message Import
~~~~~~~~~~~~~~~~~~~~

An Autocrypt-capable MUA SHOULD support the ability to wait for and
import an Autocrypt Setup Message when the user has not yet configured
Autocrypt.  This could happen either when a user of an unconfigured
Autocrypt MUA decides to enable Autocrypt, or the MUA could
proactively scan the MUA's mailbox for a message that matches these
characteristics, and it could alert the MUA if it discovers one.

If the MUA finds an Autocrypt Setup Message, it should offer to
import it to enable Autocrypt.  If the user agrees to do so:

 * The MUA prompts the user for their corresponding Setup Code.
   If there is a ``Passphrase-Format`` header in the outer OpenPGP armor and
   its value is ``numeric9x4``, then the MUA MAY present a specialized
   input dialog assisting the user to enter a code in the format described
   above.
   If there is no ``Passphrase-Format`` header, or the value is unknown,
   then the MUA MUST provide a plain UTF-8 string text entry.

 * The MUA should try decrypting the message with the supplied
   Setup Code.  The Code serves both for decryption as well as
   authenticating the message.  Extra care needs to be taken with some
   PGP implementations that the Setup Code is actually used for
   decryption. See :doc:`bad-import` for more explanation and an
   example.

 * If it decrypts, then the MUA SHOULD update ``accounts[addr]``
   according to the contents of the decrypted message, as discussed in
   :ref:`accounts`.

See :ref:`setup-message-example`.


User Interface
--------------

Ideally, Autocrypt users see very little UI.  However, some UI is
inevitable if we want users to be able to interoperate with existing,
non-Autocrypt users.

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
``encrypt``, the MUA SHOULD expose this UI with the :ref:`recommended default <recommendation>` during message composition
to allow the user to make a different decision.

If the Autocrypt recommendation is ``discourage``, then the MUA SHOULD
expose the UI in an unactive state.  But if the user chooses to
activate it (e.g., clicking on the checkbox), then the UI should
display a warning to the user and ask them to confirm the choice to
encrypt.

.. _preference-ui:

Account Preferences
+++++++++++++++++++

Level 1 MUAs MUST allow the user to disable Autocrypt completely for
each account they control (that is, to set ``accounts[addr].enabled``
to ``false``).  For level 1, we expect most MUAs to have Autocrypt
disabled by default.

.. _getting_started:

Helping Users get Started
+++++++++++++++++++++++++

This section provides recommendations for MUA implementations to help
users start Autocrypt immediately after an account (with the address
``addr``) was set up.

The MUA SHOULD scan the mailbox for messages sent by the user
(wherever the messages might be) that show evidence of OpenPGP or
Autocrypt usage. It is likely sufficient to only scan the messages
sent during the last 30 days, as it is unlikely that the user
used Autocrypt or OpenPGP actively if no such message was sent in
the recent past.

From the set of all found sent messages, the MUA should
determine the best action to take from the following list of choices.
Earlier choices are better than later ones.

1. If an Autocrypt Setup Message was found:

   Start a setup process suggesting the user to import the
   setup message. If multiple Autocrypt Setup Messages are
   found, the most recent message should be preferred.

2. If a sent message with an Autocrypt header was found:

   Provide guidance for creating an Autocrypt Setup Message
   on the MUA that created the message.

3. If there is evidence of actively used OpenPGP software
   (for example if a secret key is available, some
   specific software is installed, etc.) or if encrypted
   mails are found:

   Inform the user about Autocrypt on <https://autocrypt.org/pgp-users>.

4. If no evidence for Autocrypt was found:

   Create a key with default settings and without a password in the
   background. Set your ``accounts[addr].prefer_encrypt`` to
   ``nopreference`` and start sending Autocrypt headers.


Appendix
--------

.. _example-headers:

Example Autocrypt headers
+++++++++++++++++++++++++

::

    Delivered-To: <bob@autocrypt.example>
    From: Alice <alice@autocrypt.example>
    To: Bob <bob@autocrypt.example>
    Subject: an Autocrypt header exapmple using RSA 3072 key
    Autocrypt: addr=alice@autocrypt.example; keydata=
     mQGNBFn+L+YBDAC3jsOXmFKwKfUh/WxaOErSMMdL1NJzzFCDf4oo0XD5b4ldfVGP09PsNXg5bzUW
     NP1eGiINWCnQlPYmdFR+mCn/mvG50tCiZ0ij4qiFqTv4easAgKNn0dCvqoLY0tpsMLo2Kv9lM9m5
     Fi9NrK0xNUgw/nX0LgE58VmGhT0tA1VRlnmdu/yKHWLqjOyuueYRVMlT8prGGNsxtplOdjTlFUN+
     QEjc/YcnX+EKXHQmIXOFW82sRB2p9m7dcjhqCjgjaFdZ0YtVZ4y9XJs+9MyzqceUy3WjmHz4YBKv
     F32S34xns3C95kEuH+Qgp+xMQt/7QpFQSgWsddeKeR7lI1nLd5DnOgzlw6vyiiG91JWs2JqFSWxz
     FwIpUctgOayNhce5RWsbewL9m+PuBHPHB6bsTadDWH6o2INRkcCQj1n5fuL9HGA6FSXu7NWNYfJr
     PA+Rxc5gd1/qSYgGFIsSVLnkGoeRnpIv3PndPVe4N0SZLJ/3r18wtNIpWv8Isd3LtLbes50AEQEA
     AbQXYWxpY2VAYXV0b2NyeXB0LmV4YW1wbGWJAdMEEwEKAD0WIQTYxrHIMQydyu0aBH2r8IzzOTtm
     BgUCWf4v5gIbAwUJA8JnAAQLCQgHBRUKCQgLBRYCAwEAAh4BAheAAAoJEKvwjPM5O2YGfl8L/Rew
     fvGqOyDgveMaGZ7m4icDKwAmbDUAdQH6R0vQ9RPezT+PPhLTkYkciIT7weDL4v3YO63lqVgFjuFV
    Date: Sat, 17 Dec 2016 10:07:48 +0100
    Message-ID: <rsa-3072@autocrypt.example>
    MIME-Version: 1.0
    Content-Type: text/plain

    This is an example e-mail with Autocrypt header and RSA 3072 key
    as defined in Level 1.

.. _example-cant-encrypt-reply:

Example Copy when a Reply can't be Encrypted
++++++++++++++++++++++++++++++++++++++++++++

::

    The message this is a reply to was sent encrypted, but this reply is
    unencrypted because I don't yet know how to encrypt to
    ``bob@example.com``.  If ``bob@example.com`` would reply here, my
    future messages in this thread will be encrypted.



Example User Interaction for Setup Message Creation
+++++++++++++++++++++++++++++++++++++++++++++++++++

The Setup Code shown in this example can be used with
:ref:`setup-message-example` below.

::

    You'll need to use this Setup Code in your other e-mail program to
    use the Autocrypt Setup Message:

        1742-0185-6197-
        1303-7016-8412-
        3581-4441-0597


Example User Interaction for Setup Message Receipt
++++++++++++++++++++++++++++++++++++++++++++++++++

To initiate the import of the Autocrypt Setup Message, the MUA
can display a message like the example below:

::

    We detected a message created by one of your other email
    applications that contains the setup information for
    Autocrypt. By importing these settings, you can apply
    the same settings in (your application).

    Please enter the Setup Code displayed by your other email
    application to proceed:

                     17__ - ____ - ____ -
                     ____ - ____ - ____ -
                     ____ - ____ - ____


               [   Cancel   ]     [ Import Settings ]

.. _setup-message-example:

Example Setup Message
+++++++++++++++++++++

::

    Date: Sun, 05 Nov 2017 08:44:38 GMT
    To: alice@autocrypt.example
    From: alice@autocrypt.example
    Autocrypt-Setup-Message: v1
    Subject: Autocrypt Setup Message
    Content-type: multipart/mixed; boundary="Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ"

    --Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ
    Content-Type: text/plain

    This message contains all information to transfer your Autocrypt
    settings along with your secret key securely from your original
    device.

    To set up your new device for Autocrypt, please follow the
    instuctions that should be presented by your new device.

    You can keep this message and use it as a backup for your secret
    key. If you want to do this, you should write down the Setup Code
    and store it securely.
    --Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ
    Content-Type: application/autocrypt-setup
    Content-Disposition: attachment; filename="autocrypt-setup-message.html"

    <html><body>
    <p>
    This is the Autocrypt setup file used to transfer settings and
    keys between clients. You can decrypt it using the Setup Code
    presented on your old device, and then import the contained key
    into your keyring.
    </p>

    <pre>
    -----BEGIN PGP MESSAGE-----
    Passphrase-Format: numeric9x4
    Passphrase-Begin: 17

    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
    mngm1QCMMw2v/j8=
    =9sJE
    -----END PGP MESSAGE-----
    </pre></body></html>
    --Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ--

The encrypted message part contains:

::

    -----BEGIN PGP PRIVATE KEY BLOCK-----
    Autocrypt-Prefer-Encrypt: mutual

    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
    TRzalg==
    =f96/
    -----END PGP PRIVATE KEY BLOCK-----
