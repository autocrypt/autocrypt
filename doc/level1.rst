.. raw:: latex

   \pagestyle{plain}
   \cfoot{Autocrypt Specification \autocryptrelease}

Autocrypt Level 1: Enabling encryption, avoiding annoyances
===========================================================

Autocrypt aims to incrementally and carefully replace cleartext e-mail
with end-to-end encrypted e-mail. This differs from the traditional approach
of maximizing the security of individual mail communications.
**Sometimes Autocrypt recommends to send cleartext mail even though
encryption appears technically possible.** This is because we want to
avoid unreadable mail for users. Users may mix both Autocrypt-capable
and traditional mail apps and they may loose devices or otherwise loose
the ability to decrypt in unrecoverable ways. Reverting to cleartext
when we suspect such situations is a key part of our aim to stay out of
the way of users.

Another major difference in approach is that Autocrypt Level 1 only
defends against passive data collection attacks. We share and support
:rfc:`the new perspective stated in RFC7435 ("Opportunistic Security: Some
Protection Most of the Time") <7435#section-1.2>`. Protection against
active adversaries (those which modify messages in transit) is the aim
of future specifications.

**Level 1 makes it easy for users to encrypt, based on an automatic and
decentralized key distribution mechanism. There are no dependencies on
key servers and it is meant to work with existing e-mail providers.**
Level 1 focuses on the use of Autocrypt on a single device. Users get
rudimentary support on using Autocrypt on more than one device or mail app.
This is internally realized through sending and receiving an Autocrypt
Setup Message, secured by manually entering a long number. Improving
usability for maintaining synchronized Autocrypt state on multiple
devices is the aim of future specification efforts.

**Last but not least, Level 1 is meant to be relatively easy for
developers to adopt.** It describes the basic capabilities required for
a mail app to be Autocrypt-capable at Level 1, allowing it to exchange
end-to-end encrypted e-mails with other Autocrypt-capable mail apps. The
spec contains detailed guidance on protocol, internal state and user
interface concerns. We have a good track record of supporting new
implementers. Please don't hesitate to ask back or bring up issues or
pull requests. Autocrypt is a living specification and we envision both
bugfix and backward-compatible feature releases.

.. only:: builder_html

   .. contents::

.. only:: builder_readthedocs

   .. contents::

.. raw:: latex

   \newpage
   \sphinxtableofcontents
   \newpage

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
  (:ref:`definition <effective_date>`) of all messages that the MUA
  has processed from this peer.
* ``autocrypt_timestamp``: The UTC timestamp of the most recent
  effective date (the "youngest") of all messages containing a valid
  ``Autocrypt`` header that the MUA has processed from this peer.
* ``public_key``: The value of the ``keydata`` attribute derived from
  the youngest ``Autocrypt`` header that has ever been seen from the
  peer.
* ``prefer_encrypt``: The ``prefer-encrypt`` value (either
  ``nopreference`` or ``mutual``) derived from the youngest
  ``Autocrypt`` header ever seen from the peer.

Autocrypt-capable MUAs that implement :ref:`Gossip <key-gossip>` should
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

There are three defined attributes:

 * The ``addr`` attribute is mandatory, and contains the single
   recipient address this header is valid for.  If this address
   differs from the one in the ``From`` header, the entire
   ``Autocrypt`` header MUST be treated as invalid.

   :rfc:`The Internet Message Format <5322#section-3.6.2>` documents
   three types of originator fields: ``From``, ``Sender``, and
   ``Reply-To``.  Autocrypt is concerned only with the ``From`` field,
   and ignores the other originator fields.

.. _prefer-encrypt:

 * The ``prefer-encrypt`` attribute is optional and can only occur
   with the value ``mutual``.  Its presence in the ``Autocrypt``
   header indicates an agreement to enable encryption by default with
   other peers who have the same preference.  An Autocrypt Level 1 MUA
   that sees the attribute with any other value (or that does not see
   the attribute at all) should interpret the value as
   ``nopreference``.

 * The ``keydata`` attribute is mandatory, and contains the key data
   for the specified ``addr`` recipient address.  The value of the
   ``keydata`` attribute is a Base64 representation of the binary
   :rfc:`OpenPGP "Transferable Public Key"<4880#section-11.1>`. For
   ease of parsing, the ``keydata`` attribute MUST be the last
   attribute in this header.

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
level 1 MUAs.  Such an update to the specification will also have
to describe how an updated MUA will deal with multiple valid headers.


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

An MUA SHOULD send out the same ``Autocrypt:`` header in all messages
from a given outbound identity.  An MUA SHOULD NOT vary the header
based on the message's recipients. If (for whatever reason) the MUA
needs to update (or discovers an update of) the user's ``keydata`` at
some point, the MUA SHOULD send the updated ``keydata`` in all
subsequent ``Autocrypt`` headers.

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

.. _spam-filters:

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

  .. note::

     A message without a ``Date`` header, or with a ``Date`` that
     seems to be in the far future can cause problems for MUAs that
     encounter the message repeatedly (e.g. re-delivery, subsequent
     scans, etc). An MUA MAY decide to ignore such a message entirely
     for the purposes of Autocrypt processing.  If an MUA is capable
     of associating information with a recieved message, it could
     instead save the ``effective date`` of such a message the first
     time it sees it to avoid accidental re-processing.

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

All Autocrypt-capable MUAs should be able to calculate the same
Autocrypt recommendation.

This recommendation algorithm provides sensible guidance that avoids
many common problems, and Autocrypt-capable MUAs SHOULD follow the
recommendation.  An implementation that deviates from the
recommendation should do so on the basis of specific external evidence
or knowledge, while carefully considering the impact of any variation,
including:

 * does it increase the chance of producing unexpectedly unreadable
   mail (for either the sender or the recipient)?
 * does it leak previously encrypted content in the clear?
 * does it force the user to confront a choice they do not have the
   information or knowledge to make safely?

If an implementation deviates from the Autocrypt recommendation in a
meaningful and useful way, the implementer should describe the
variation publicly so it can be considered for future revisions of
this specification.

Recommendation structure
~~~~~~~~~~~~~~~~~~~~~~~~

The Autocrypt recommendation depends on the recipient addresses of the
draft message, and on whether or not the message is a reply to an
encrypted message.  When the user changes the recipients during
composition, the Autocrypt recommendation may change.

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
more than 35 days older than ``gossip_key_timestamp``, set
``target-keys[to-addr]`` to ``gossip_key`` and set
``preliminary-recommendation`` to ``discourage`` and skip to the
:ref:`final-recommendation-phase`.

Otherwise, set ``target-keys[to-addr]`` to ``public_key``.

If ``autocrypt_timestamp`` is more than 35 days older than
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

The aggregate ``ui-recommendation`` for the message is derived in the
following way (the earliest matching rule encountered below takes
precedence over later rules):

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
copy can be found in :ref:`example-cant-encrypt-reply`.

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
See example in :ref:`autocrypt-gossip-example`

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
Autocrypt can be mitigated by using a different MUA for each e-mail
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

An Autocrypt-capable MUA SHOULD support the ability to find and import
an Autocrypt Setup Message when the user has not yet configured
Autocrypt.  An MUA could look for such a message in several ways,
including:

 * If the user decides to enable Autocrypt for an account, and
   indicates to the MUA that an older MUA has already enabled
   Autocrypt on that account, the new MUA could ask the user to
   generate an Autocrypt Setup Message from the old MUA, and then wait
   (e.g., via :rfc:`IMAP IDLE <2177>`) for such a message to arrive.

 * The MUA could proactively scan the account's mailbox for a message
   that matches these characteristics, and it could alert the user if
   it discovers one.

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

Alice sends Bob a simple, unencrypted e-mail message that lets Bob
write back encrypted if Bob is using an Autocrypt-enabled MUA:

.. literalinclude:: appendix/example-simple-autocrypt.eml
    :language: none


.. _autocrypt-gossip-example:

Example Autocrypt Gossip headers
++++++++++++++++++++++++++++++++

After having received messages with Autocrypt headers from both Bob
and Carol, Alice sends an e-mail to the two of them, with Autocrypt
Gossip headers.

.. literalinclude:: appendix/example-gossip.eml
    :language: none

Since Alice encrypts messages to herself, the above message can be
decrypted by her private key as well (see the
:ref:`setup-message-example` for access to her private key)

When decrypted, the encrypted part contains:

.. literalinclude:: appendix/example-gossip-cleartext.eml
    :language: none

.. _example-cant-encrypt-reply:

Example Copy when a Reply can't be Encrypted
++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: none

    The message this is a reply to was sent encrypted, but this reply is
    unencrypted because I don't yet know how to encrypt to
    ``bob@example.com``.  If ``bob@example.com`` would reply here, my
    future messages in this thread will be encrypted.


.. _example-setup-code:

Example User Interaction for Setup Message Creation
+++++++++++++++++++++++++++++++++++++++++++++++++++

The Setup Code shown in this example can be used with
:ref:`setup-message-example` below.

.. code-block:: none

    You'll need to use this Setup Code in your other e-mail app to use
    the Autocrypt Setup Message:

        1742-0185-6197-
        1303-7016-8412-
        3581-4441-0597


Example User Interaction for Setup Message Receipt
++++++++++++++++++++++++++++++++++++++++++++++++++

To initiate the import of the Autocrypt Setup Message, the MUA
can display a message like the example below:

.. code-block:: none

    ExampleMail has detected an Autocrypt Setup Message created by one
    of the other apps you use to access "alice@autocrypt.example".  By
    importing the settings from this message, you can start using
    Autocrypt here in ExampleMail too!

    Please enter the Setup Code displayed by your other e-mail app to
    proceed:

                     17__ - ____ - ____ -
                     ____ - ____ - ____ -
                     ____ - ____ - ____


               [   Cancel   ]     [ Import Settings ]

.. _setup-message-example:

Example Setup Message
+++++++++++++++++++++

Alice's MUA sends her a Setup Message after showing her a Setup Code
(the code used here is the one from :ref:`example-setup-code`).  The
generated message looks like this:

.. literalinclude:: appendix/example-setup-message.eml
    :language: none

When decrypted with the Setup Code, the encrypted blob at the end
contains:

.. literalinclude:: appendix/example-setup-message-cleartext.key
    :language: none
