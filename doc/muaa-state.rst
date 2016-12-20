Autocrypt state for Mail User Agent Accounts
============================================

The Autocrypt header offers a key discovery mechanism to support
encrypted mail.

However, inferring what key to use from messages seen over time is
non-obvious.  This document provides guidance for implementors who
need to use these headers to infer key use and encryption preferences,
and will serve as a baseline input to multi-agent synchronization
work.


Internal state
--------------

Agents capable of Autocrypt level 0 MUST store some state about the
capabilities of their remote peers.

Conceptually, we represent this state as a table named
`autocrypt_peer_state` indexed by e-mail address and type.  (in level
0, there is only one type, "p", so level 0 agents can implement this
by indexing only the e-mail address).

For each e-mail and type, an Agent MUST store the following
attributes:

 * `pah`: Parsed Autocrypt header, which could be `null`
 * `changed`: Timestamp when `pah` was last changed
 * `last_seen`: Most recent time that `pah` was confirmed

Agents MAY also store other attributes and other information gathered
for heuristic purposes, or for other cryptographic schemes.  However,
In order to support future syncing of Autocrypt state between agents, it
is critical that Autocrypt-capable agents store and update the state
specified here.

Parsed Autocrypt header
-----------------------

Please see mua-key-discovery.rst for details about the wire format of
the Autocrypt header.  Autocrypt-compatible agents SHOULD track and
store in `autocrypt_peer_state` a parsed interpretation `pah`, which
is not necessarily the literal header.  The `pah` MUST contain the
following fields:

 * `key` -- the raw key material, after base64 decoding
 * `prefer_encrypted` -- a tri-state: `nopreference`, `yes`, or `no`

Note that `nopreference` can only be indirectly sent in a raw Autocrypt
header (by omitting the `prefer-encrypted` attribute entirely).

Upon message receipt
--------------------

When first encountering an incoming e-mail from a e-mail address `A`,
the user agent should determine the `selected_date` and parse the
e-mail for Autocrypt headers.

NOTE: this implies that Autocrypt clients keep track of whether they
have encountered a given message before, but does not provide them
with guidance on how to do so.  Message-ID?  Digest of full message
body?  The consequences of re-triggering the message receipt process
should only matter for messages that are erroneously marked with a
future date. Another approach that would not require keeping track of
the message would be to simply ignore messages whose `Date:` header is
in the future.

NOTE: the spec currently doesn't say how to integrate Autocrypt
processing on message receipt with spam filtering.  Should we say
something about not doing Autocrypt processing on message receipt if
the message is believed to be spam?

the `message_date` is the *earlier* of:

 * the `Date:` header of the e-mail
 * the current timestamp (e.g. the output of `time()`)

(this is to avoid an a sender who mis-generates a `Date:` stamp in the
future)
   
When parsing the e-mail message for the Autocrypt header, the
resulting `message_pah` is either a Parsed Autocrypt header, or NULL.

if `message_pah` is NULL, then we replace it with a `synthesized_pah`
generated from the message itself:

 * If the message is not cryptographically signed, or there is an
   unverifiable or invalid message signature, `synthesized_pah` is
   NULL.

 * Alternately, the message is cryptographically signed, and the
   signature is verified and comes from a known OpenPGP certificate
   `K`: If `K` is not encryption-capable (i.e. if the primary key has
   no encryption-capabilities marked, and no valid subkeys are
   encryption-capable), or if K does not have an OpenPGP User ID which
   contains the e-mail address in the message's `From:`, then
   `synthesized_pah` is also NULL.  Otherwise, with an
   encryption-capable `K`, the `key` element of `synthesized_pah` is
   set to `K`.  In this case, the `prefer_encrypted` element of
   `synthesized_pah` is set based on whether the message is also
   encrypted in addition to being signed.  If the message is
   encrypted, then `prefer_encrypted` is set to `yes`.  If it is not
   encrypted, then `prefer_encrypted` is set to `nopreference`.

NOTE: We do *not* synthesize the Autocrypt header from any
`application/pgp-keys` message parts.  This is because it's possible
that an attached OpenPGP key is not intended to be the sender's
OpenPGP key.  For example, Alice might send Bob Carol's OpenPGP key in
an attachment, but Bob should not interpret it as Carol's key.

   
The agent continues this message receipt process even in the case that
`message_pah` is NULL, since updating the stored state with NULL is
sometimes the correct action.
   
Next, the agent compares the `message_pah` with the `pah` stored in
`autocrypt_peer_state[A]`.

If `autocrypt_peer_state` has no record at all for address `A`, the
agent sets `autocrypt_peer_state[A]` such that `pah` is `message_pah`
and `changed` and `last_seen` are both `message_date`, and then
terminates this receipt process.

If `autocrypt_peer_state[A]` has `last_seen` greater than or equal to
`message_date`, then the agent stores `message_pah` and terminates
this receipt process, since it already knows about something more
recent.  For example, this might be if mail is delivered out of order,
or if an inbox is scanned from newest to oldest.

If `autocrypt_peer_state[A]` has a `last_seen` less than
`message_date`, then we compare `message_pah` with the `pah` currently
stored in `autocrypt_peer_state[A]`.

This is done as a literal comparison using only the `key` and
`prefer_encrypt` fields, even if the Agent stores additional fields as
an augmentation -- if `key` is bytewise different, or if
`prefer_encrypted` has a different value, then this is an update.  If
`key` and `prefer_encrypted` match exactly, then it is considered a
match.  If both `pah` and `message_pah` are NULL, it is a match.  If
one is NULL and the other is not NULL, it is a update.

In the case of a match, set `autocrypt_peer_state[A].last_seen` to
`message_date`.

In the case of an update, set `autocrypt_peer_state[A].pah` to
`message_pah` and `autocrypt_peer_state[A].last_seen` and
`autocrypt_peer_state[A].changed` to `message_date`.

NOTE: the above algorithm results in a non-deterministic
`autocrypt_peer_state` if two Autocrypt headers are processed using
the same `message_date` (depending on which message is encountered
first).  For consistency and predictability across implementations, it
would be better to have a strict ordering between parsed Autocrypt
headers, and to always select the lower header in case of equal values
of `message_date`.

NOTE: OpenPGP's composable certificate format suggests that there
could be alternate ways to compare `key` values besides strict
bytewise comparison.  For example, this could be done by comparing
only the fingerprint of the OpenPGP primary key instead of the
keydata.  However, this would miss updates of the encryption-capable
subkey, or updates to the capabilities advertised in the OpenPGP
self-signature.  Alternately, the message receipt process could
incorporate fancier date comparisons by integrating the timestamps
within the OpenPGP messages during the date comparison step.  For
simplicity and ease of implementation, level 0 Autocrypt-capable
agents are expected to avoid these approaches and to do full
bytestring comparisons of `key` data instead.


Generating an Autocrypt header upon message composition
-------------------------------------------------------

During message composition where the message will be marked as `From:`
an e-mail address that the Autocrypt-capable agent knows the secret
key material for, it should always include an Autocrypt header with
the associated public key material as the `key=` attribute, and it
should include the `to=` attribute for recipients to match on.

If the `From:` address changes during message composition (e.g. if the
user selects a different outbound identity, the Autocrypt-capable
client MUST change the Autocrypt header.

NOTE: we need documentation about key expiry -- Autocrypt-capable
clients that choose to have an expiry policy on their secret key
material should use message composition as an opportunity to refresh
their secret key material or update the expiration dates in their
public certificate.


Choosing encryption and UI during message composition
-----------------------------------------------------

On message composition, an Autocrypt-capable agent also has an
opportunity to decide whether to try to encrypt an e-mail.  Autocrypt
aims to provide a reasonable recommendation for the agent.

Any Autocrypt-capable agent may have other means for making this
decision outside of Autocrypt.  Autocrypt provides a recommendation to
this process, but there is no requirement for Autocrypt-capable agents
to always follow the Autocrypt recommendation.  For example, an
Autocrypt-capable agent that also incorporates the OpenPGP "Web of
Trust" might already know about a non-Autocrypt public key that it
considers to be correctly bound to the recipient e-mail address.  It
may wish to prefer such a key, and to decide to use for a given
outbound message over any recommendations provided by Autocrypt.

That said, all Autocrypt-capable agents should be able to calculate
the same Autocrypt recommendation due to their internal state.

Autocrypt can produce three possible recommendations to the agent
during message composition:

 * `disable` : Disable or hide any UI that would allow the user to
    choose to encrypt the message.  Prepare the message in cleartext.

 * `available` : Enable UI that would allow the user to choose to
   encrypt the message, but do not default to encryption.  Prepare the
   message in cleartext.

 * `encrypt` : Enable UI that would allow the user to choose to send
   the message in cleartext, and default to encryption.  Prepare the
   message as an encrypted message.

NOTE: The Autocrypt recommendation should probably change depending on
whether the mail is a reply to an encrypted e-mail or not.
   
Single recipient messages
-------------------------
   
For level 0 agents, the Autocrypt recommendation for message composed
to a single recipient with e-mail address `A` is derived from the
value stored in `autocrypt_peer_state[A]`.

If the `pah` is NULL, or if `pah.key` is known to be unusable for
encryption (e.g. it is otherwise known to be revoked or expired), then
the recommendation is `disable`.

If the `pah` is not NULL, and `prefer-encrypted` is `yes`, then the
recommendation is `encrypt`.

If `pah` is not NULL, and `prefer-encrypted` is either `no` or
`nopreference`, then the recommendation is `available`.

Message composition to multiple addresses
-----------------------------------------

For level 0 agents, the Autocrypt recommendation for a message
composed to multiple recipients is derived from the recommendations
for each recipient individually.

If any recipient has a recommendation of `disable` then the message
recommendation is `disable`.

If every recipient other than "myself" (the e-mail address that the
message is `From:`) has a recommendation of `encrypt` then the message
recommendation is `encrypt`.

Otherwise, the message recommendation is `available`.

Future Work for level > 0
-------------------------

We need to specify how to sync these state updates between clients.
We want to be able to sync the state without sending sync data for
every message processed, while we also want all synced peers to have
the same internal state as much as possible.  We currently believe
that syncing updates to `pah` and `changed` should be sufficient, and
that peers do not need to sync `last_seen`.  This has not been proved
in practice.

how to deal with multiple types (at least when a new type is
specified).  When we support types other than `p`, it's possible that
users will have multiple keys available, each with a different type.
That seems likely to introduce some awkward choices during message
composition time, particularly for multi-recipient messages.
