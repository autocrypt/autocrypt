Guidance for Implementers of Autocrypt Level 0
==============================================

This document describes the basic capabilities required for a MUA to
be Autocrypt-capable at Level 0.  Some Autocrypt-capable clients may
choose to go beyond these features, and future Levels of Autocrypt may
require more specific control.

Throughout this document, we refer to a Mail User Agent (MUA) as
though it was only capable of controlling a single e-mail account.  A
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

- The ability to receive e-mail where the MUA gets access to 
  the entire message being received, including both message 
  headers and message body.

- Access to a special (IMAP) Shared Message Archive (SMA) folder which
  can be accessed by all MUAs of a user's devices to co-ordinate
  between them.  In Level 0 this is only used for `ensuring that only
  one MUA has Autocrypt enabled for an e-mail account at once
  <lockout>`_.

If a particular e-mail account does not expose these features
(e.g. if it only exposes a javascript-driven web interface for message
composition that does not allow setting of e-mail headers, or if it
only offers POP access to the incoming mail) then the e-mail account
cannot be used with Autocrypt.  An Autocrypt-capable MUA may still
access and control the account, but it will not be able to enable
Autocrypt on it.

.. todo::

    Discuss with webmail developers how to work with, refine 
    the interactions.

Secret key generation and storage
---------------------------------

The MUA MUST be capable of generating and storing two RSA 2048-bit
secret keys, one for signing and self-certification and the other for
decrypting.  It MUST be capable of assembling these keys into an
OpenPGP certificate (RFC 4880 "Transferable Public Key") that
indicates these capabilities.

The secret key material is critical for security as in other end-to-end
applications, and should be protected from access by other applications or
co-tenants of the device, at least as well as the passwords the MUA retains for
the user's IMAP or SMTP accounts.

In Level 0 only one MUA can send and receive encrypted mail through Autocrypt
mechanisms.  When an Autocrypt-enabled MUA configures an e-mail account, it
first tries to "claim" the account, to `lock out <lockout>`_ other MUAs of the
same users.  If the claim was successful, the MUA should proceed to generate
secret keys and store them locally.

.. _lockout:

Claiming the Account
--------------------

Only one Level 0 MUA can have Autocrypt enabled for a given account at
a time.  The Autocrypt-enabled MUA "claims" the account so that others
disable their Autocrypt features.

The Shared Mail Archive MUST contain a named location mechanism that
all other Autocrypt clients can see.  For example, an IMAP mailbox
would have a named folder.  Autocrypt uses the special name
`_autocrypt_sma` to store "claim" announcements.

The MUA looks in the special location for a message whose form matches
the standard claim announcement and is valid.  If such a message is
present, the MUA disables its Autocrypt features for this account.

If the special location does not exist, or it exists, but there are no
valid claim announcements in it, the MUA crafts its own claim
announcement and places it in the special location.

.. todo::

   - Document the claim announcement format and precise location
   - Clarify concerns about race conditions, case-sensitivity, etc.


Header injection in outbound mail
---------------------------------

During message composition, if the ``From`` header of the outgoing e-mail
matches an address that the Autocrypt-capable agent knows the secret key
material for, it SHOULD include an Autocrypt header. This header contains the
associated public key material as ``key=`` attribute, and the same sender
address that is used in the ``From`` header in the ``to=`` attribute to confirm
the association. The most minimal Level 0 MUA will only include these two
attributes.

See :ref:`mua-happypath` for examples of outbound headers and
the following sections for header format definitions and parsing.

..  _autocryptheaderformat:

Deriving a Parsed Autocrypt Header from a Message
-------------------------------------------------

The ``Autocrypt`` header has the following format::

    Autocrypt: to=a@b.example.org; [type=p;] [prefer-encrypted=(yes|no);] key=BASE64

The ``to`` attribute indicates the single recipient address this header is
valid for. In case this address differs from the one the MUA considers the
sender of the e-mail in parsing, which will usually be the one specified in the
``From`` header, the entire header MUST be treated as invalid.

The ``type`` and ``key`` attributes specify the type and data of the key
material.  For now the only supported type is ``p``, which represents a
specific subset of OpenPGP (see the next section), and is also the default.
Headers with an unknown ``type`` MUST be treated as invalid.  The value of the
``key`` attribute is a Base64 representation of the public key material.  For
ease of parsing, the ``key`` attribute MUST be the last attribute in the
header.

The ``prefer-encrypted`` attribute indicates whether agents should default to
encrypting when composing e-mails to this recipient.
If ``prefer-encrypted`` is not set,
the value of ``prefer-encrypted`` is ``nopreference``.
If ``prefer-encrypted`` is set, but neither ``yes`` nor ``no``,
the MUA must skip the header as invalid.

Additional attributes unspecified here are also possible before the ``key``
attribute.  If an attribute name starts with an underscore (``_``), it is a
"non-critical" attribute.  The MUA SHOULD ignore non-critical attributes, but
MUST treat the entire header as invalid if it encounters a "critical" attribute
it doesn't support.

When parsing an incoming message, a MUA MUST examine all ``Autocrypt`` headers,
rather than just the first one.  If there is more than one valid header, this
MUST be treated as an error, and all ``Autocrypt`` headers discarded as
invalid.

.. todo::

   - Document why we skip on more than one valid header?
   - What does (p|_*) mean? It's not a regex, apparently?

``type=p``: OpenPGP Based key data
++++++++++++++++++++++++++++++++++

For maximum interoperability, a certificate sent by an
Autocrypt-enabled Level 0 MUA MUST consist of an OpenPGP "Transferable
Public Key" (see `RFC 4880 §11.1 <https://tools.ietf.org/html/rfc4880#section-11.1>`_) 
containing exactly these five OpenPGP packets:

 - a signing-capable primary key ``Kp``
 - a user id that SHOULD be set to the e-mail address of the account
 - a self signature
 - an encryption-capable subkey ``Ke``
 - a binding signature over ``Ke`` by ``Kp``

The content of the user id packet is only decorative, and MAY contain different
values from the ``to`` attribute, or even the empty string.

These packets MUST be assembled in binary format (not ASCII-armored), and then
base64-encoded.

A Level 0 MUA MUST be capable of processing and handling 2048-bit RSA
keys.  It SHOULD be capable of handling Curve 25519 keys (ed25519 for
``Kp`` and cv25519 for ``Ke``), but some underlying toolkits may not
yet support Curve 25519.  It MAY support other OpenPGP key formats.


Internal state storage
----------------------

.. note::

    You should be familiar with :ref:`mua-happypath` before reading the
    following.  

If a remote peer disables Autocrypt or drops back to using a
non-Autocrypt MUA only we must be able to disable sending encrypted
mails to this peer automatically.  MUAs capable of Autocrypt level 0
therefore MUST store state about the capabilities of their remote peers.  

Agents MAY also store additional
information gathered for heuristic purposes, or for other
cryptographic schemes.  However, in order to support future syncing of
Autocrypt state between agents, it is critical that Autocrypt-capable
agents maintain the state specified here.

Conceptually, we represent this state as a table named
``autocrypt_peer_state`` indexed by the peer's :doc:`canonicalized 
e-mail address <address-canonicalization>` and key type.  In level 0,
there is only one type, ``p``, so level 0 agents can implement this by
indexing only the peer's e-mail address. 

For each e-mail and type, an Agent MUST store the following
attributes:

 * ``pah``: Parsed Autocrypt header, which could be ``null``
 * ``changed``: UTC Timestamp when ``pah`` was last changed
 * ``last_seen``: Most recent UTC time that ``pah`` was confirmed

Autocrypt-compatible agents SHOULD track and store in
``autocrypt_peer_state`` a parsed interpretation ``pah``, which is not
necessarily the literal header emitted (for the literal header, see
next section).  The ``pah`` MUST contain the following fields:

 * ``key`` -- the raw key material, after base64 decoding
 * ``prefer_encrypted`` -- a tri-state: ``nopreference``, ``yes``, or ``no``

   
Updating internal state upon message receipt
--------------------------------------------

When first encountering an incoming e-mail ``M`` from an e-mail address ``A``,
the MUA should follow the following ``autocrypt_update`` algorithm:

 - Set a local ``message_date`` to the ``Date:`` header of ``M``.

 - If ``message_date`` is in the future, set ``message_date`` to the
   current time.

.. todo::

   This implies that Autocrypt clients keep track of whether they have
   encountered a given message before, but does not provide them with
   guidance on how to do so.  Message-ID?  Digest of full message
   body?  The consequences of re-triggering the message receipt
   process should only matter for messages that are erroneously marked
   with a future date. Another approach that would not require keeping
   track of the message would be to simply ignore messages whose
   ```Date:`` header is in the future.

..
   
 - Set a local ``message_pah`` to be the ``Autocrypt:`` header in ``M``.  This is
   either a single Parsed Autocrypt header, or ``null``.

 - If ``message_pah`` is ``null``, and the MUA knows about additional
   OpenPGP keys, then we replace ``message_pah`` with a
   ``synthesized_pah`` generated from the message itself:

   - If the message is not cryptographically signed, or there is an
     unverifiable or invalid message signature, ``synthesized_pah`` is
     ``null``.

   - Alternately, the message is cryptographically signed, and the
     signature is verified and comes from a known OpenPGP certificate
     ``K``: If ``K`` is not encryption-capable (i.e. if the primary
     key has no encryption-capabilities marked, and no valid subkeys
     are encryption-capable), or if K does not have an OpenPGP User ID
     which contains the e-mail address in the message's ``From:``,
     then ``synthesized_pah`` is also ``null``.  Otherwise, with an
     encryption-capable ``K``, the ``key`` element of
     ``synthesized_pah`` is set to ``K``.  In this case, the
     ``prefer_encrypted`` element of ``synthesized_pah`` is set based
     on whether the message is also encrypted in addition to being
     signed.  If the message is encrypted, then ``prefer_encrypted``
     is set to ``yes``.  If it is not encrypted, then
     ``prefer_encrypted`` is set to ``nopreference``.

   .. note::

      We do *not* synthesize the Autocrypt header from any
      ``application/pgp-keys`` message parts.  This is because it's
      possible that an attached OpenPGP key is not intended to be the
      sender's OpenPGP key.  For example, Alice might send Bob Carol's
      OpenPGP key in an attachment, but Bob should not interpret it as
      Carol's key.

.. todo::

   - Maybe move ``synthesized_pah`` into :doc:`other-crypto-interop` ?
   - Can we synthesize from attached keys, e.g. if it has a matching user id?
   
..
   
 - Note: The agent continues this message receipt process even when
   ``message_pah`` is ``null``, since updating the stored state with
   ``null`` is sometimes the correct action.
   
 - Next, the agent compares the ``message_pah`` with the ``pah`` stored in
   ``autocrypt_peer_state[A]``.

 - If ``autocrypt_peer_state`` has no record at all for address ``A``,
   the MUA sets ``autocrypt_peer_state[A]`` such that ``pah`` is
   ``message_pah`` and ``changed`` and ``last_seen`` are both
   ``message_date``, and then terminates this receipt process.

 - If ``autocrypt_peer_state[A]`` has ``last_seen`` greater than or
   equal to ``message_date``, then the agent stores ``message_pah``
   and terminates this receipt process, since it already knows about
   something more recent.  For example, this might be if mail is
   delivered out of order, or if an inbox is scanned from newest to
   oldest.

 - If ``autocrypt_peer_state[A]`` has a ``last_seen`` less than
   ``message_date``, then we compare ``message_pah`` with the ``pah``
   currently stored in ``autocrypt_peer_state[A]``.

   This is done as a literal comparison using only the ``key`` and
   ``prefer_encrypt`` fields, even if the Agent stores additional
   fields as an augmentation, as follows:
   
   - If ``key`` is bytewise different, or if ``prefer_encrypted`` has a different value,
     then this is an *update*. 
   - If ``key`` and ``prefer_encrypted`` match exactly, then it is considered a *match*.
   - If both ``pah`` and ``message_pah`` are ``null``, it is a *match*.
   - If one is ``null`` and the other is not ``null``, it is a *update*.

 - In the case of a **match**,
   set ``autocrypt_peer_state[A].last_seen`` to ``message_date``.

 - In the case of an **update**,
   set ``autocrypt_peer_state[A].pah`` to ``message_pah`` and
   ``autocrypt_peer_state[A].last_seen`` and
   ``autocrypt_peer_state[A].changed`` to ``message_date``.

.. note::

   The above algorithm results in a non-deterministic
   ``autocrypt_peer_state`` if two Autocrypt headers are processed
   using the same ``message_date`` (depending on which message is
   encountered first).  For consistency and predictability across
   implementations, it would be better to have a strict ordering
   between parsed Autocrypt headers, and to always select the lower
   header in case of equal values of ``message_date``.

.. note::

   OpenPGP's composable certificate format suggests that there could
   be alternate ways to compare ``key`` values besides strict bytewise
   comparison.  For example, this could be done by comparing only the
   fingerprint of the OpenPGP primary key instead of the keydata.
   However, this would miss updates of the encryption-capable subkey,
   or updates to the capabilities advertised in the OpenPGP
   self-signature.  Alternately, the message receipt process could
   incorporate fancier date comparisons by integrating the timestamps
   within the OpenPGP messages during the date comparison step.  For
   simplicity and ease of implementation, level 0 Autocrypt-capable
   agents are expected to avoid these approaches and to do full
   bytestring comparisons of ``key`` data instead.
   
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

Autocrypt can produce three possible recommendations to the agent
during message composition:

 * ``disable``: Disable or hide any UI that would allow the user to
   choose to encrypt the message.  Prepare the message in cleartext.

 * ``available``: Enable UI that would allow the user to choose to
   encrypt the message, but do not default to encryption.  Prepare the
   message in cleartext.

 * ``encrypt`` : Enable UI that would allow the user to choose to send
   the message in cleartext, and default to encryption.  Prepare the
   message as an encrypted message.

.. todo::

   The Autocrypt recommendation should probably change depending on
   whether the mail is a reply to an encrypted e-mail or not.

Recommendations for single-recipient messages
+++++++++++++++++++++++++++++++++++++++++++++
   
For level 0 MUAs, the Autocrypt recommendation for message composed to
a single recipient with e-mail address ``A`` is derived from the value
stored in ``autocrypt_peer_state[A]``.

If the ``pah`` is ``null``, or if ``pah.key`` is known to be unusable
for encryption (e.g. it is otherwise known to be revoked or expired),
then the recommendation is ``disable``.

If the ``pah`` is not ``null``, and ``prefer-encrypted`` is ``yes``,
then the recommendation is ``encrypt``.

If ``pah`` is not ``null``, and ``prefer-encrypted`` is either ``no``
or ``nopreference``, then the recommendation is ``available``.

Recommendations for messages to multiple addresses
++++++++++++++++++++++++++++++++++++++++++++++++++

For level 0 agents, the Autocrypt recommendation for a message
composed to multiple recipients is derived from the recommendations
for each recipient individually.

If any recipient has a recommendation of ``disable`` then the message
recommendation is ``disable``.

If every recipient other than "myself" (the e-mail address that the
message is ``From:``) has a recommendation of ``encrypt`` then the
message recommendation is ``encrypt``.

Otherwise, the message recommendation is ``available``.



Encrypt outbound mail as requested
----------------------------------

As the user composes mail, in some circumstances, the MUA may be
instructed by the user to encrypt the message.  If the recipient's
keys are all of ``type=p``, and the sender has keys for all recipients
(as well as themselves), they should construct the encrypted message
as a PGP/MIME (RFC 3156) encrypted+signed message, encrypted to all
recipients and the public key whose secret is controlled by the MUA
itself.

For messages that are going to be encrypted when sent, the MUA MUST
take care not to leak the cleartext of drafts or other partially-composed
messages to the SMA (e.g. in the "Drafts" folder).

If there is any chance that the message could be encrypted, the MUA
SHOULD encrypt drafts only to itself before storing in any Drafts
folder on the SMA.

Specific User Interface Elements
--------------------------------

Ideally, Autocrypt users see very little UI.  They might never see any
UI at all by default.  However, some UI is inevitable, even if only
tucked away in an arcane "preferences pane".

Account Preferences
+++++++++++++++++++

Level 0 MUAs MUST allow the user to disable Autocrypt completely for
each account they control.  

If Autocrypt is enabled for a given account, the MUA SHOULD allow the
user to specify whether they explicitly prefer encryption for inbound
messages, or explicitly prefer cleartext for inbound messages, or
choose to express no preference.  The default SHOULD be "no
preference".

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

   - Should we really recommend hiding the encrypt UI? This reduces UI consistency!
