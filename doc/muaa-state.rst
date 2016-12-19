INBOME state for Mail User Agent Accounts
=========================================

The INBOME header offers a key discovery mechanism to support
encrypted mail.

However, inferring what key to use from messages seen over time is
non-obvious.  This document provides guidance for implementors who
need to use these headers to infer key use and encryption preferences,
and will serve as a baseline input to multi-agent synchronization
work.


Internal state
--------------

Agents capable of INBOME level 0 MUST store some state about the
capabilities of their remote peers.

Conceptually, we represent this state as a table named `inbome_state`
indexed by e-mail address and type.  (in level 0, there is only one
type, "p", so level 0 agents can implement this by indexing only the
e-mail address).

For each e-mail and type, an Agent MUST store the following
attributes:

 * `pih`: Parsed INBOME header, which could be `null`
 * `changed`: Timestamp when `pih` was last changed
 * `last_seen`: Most recent time that `pih` was confirmed

Agents MAY also store other attributes and other information gathered
for heuristic purposes, or for other cryptographic schemes.  However,
In order to support future syncing of INBOME state between agents, it
is critical that INBOME-capable agents store and update the state
specified here.

Parsed INBOME header
--------------------

Please see mua-key-discovery.rst for details about the wire format of
the INBOME header.  INBOME-compatible agents SHOULD track and store in
`inbome_state` a parsed interpretation `pih`, which is not necessarily
the literal header.  The `pih` MUST contain the following fields:

 * `key` -- the raw key material, after base64 decoding
 * `prefer_encrypted` -- a tri-state: `nopreference`, `yes`, or `no`

Note that `nopreference` can only be indirectly sent in a raw INBOME
header (by omitting the `prefer-encrypted` attribute entirely).

Upon message receipt
--------------------

When first encountering an incoming e-mail from a e-mail address `A`,
the user agent should determine the `selected_date` and parse the
e-mail for INBOME headers.

NOTE: this implies that INBOME clients keep track of whether they have
encountered a given message before, but does not provide them with
guidance on how to do so.  Message-ID?  Digest of full message body?
The consequences of re-triggering the message receipt process should
only matter for messages that are erroneously marked with a future
date. Another approach that would not require keeping track of the
message would be to simply ignore messages whose `Date:` header is in
the future.

NOTE: the spec currently doesn't say how to integrate INBOME
processing on message receipt with spam filtering.  Should we say
something about not doing INBOME processing on message receipt if the
message is believed to be spam?

the `message_date` is the *earlier* of:

 * the `Date:` header of the e-mail
 * the current timestamp (e.g. the output of `time()`)

(this is to avoid an a sender who mis-generates a `Date:` stamp in the
future)
   
When parsing the e-mail message for the INBOME header, the resulting
`message_pih` is either a Parsed INBOME header, or NULL.

if `message_pih` is NULL, then we replace it with a `synthesized_pih`
generated from the message itself:

 * If the message is not cryptographically signed, or there is an
   unverifiable or invalid message signature, `synthesized_pih` is
   NULL.

 * Alternately, the message is cryptographically signed, and the
   signature is verified and comes from a known OpenPGP certificate
   `K`: If `K` is not encryption-capable (i.e. if the primary key has
   no encryption-capabilities marked, and no valid subkeys are
   encryption-capable), then `synthesized_pih` is also NULL.
   Otherwise, with an encryption-capable `K`, the `key` element of
   `synthesized_pih` is set to `K`.  In this case, the
   `prefer_encrypted` element of `synthesized_pih` is set based on
   whether the message is also encrypted in addition to being signed.
   If the message is encrypted, then `prefer_encrypted` is set to
   `yes`.  If it is not encrypted, then `prefer_encrypted` is set to
   `nopreference`.

The agent continues this message receipt process even in the case that
`message_pih` is NULL, since updating the stored state with NULL is
sometimes the correct action.
   
Next, the agent compares the `message_pih` with the `pih` stored in
`inbome_state[A]`.

If `inbome_state` has no record at all for address `A`, the agent sets
`inbome_state[A]` such that `pih` is `message_pih` and `changed` and
`last_seen` are both `message_date`, and then terminates this receipt
process.

If `inbome_state[A]` has `last_seen` greater than or equal to
`message_date`, then the agent stores `message_pih` and terminates this
receipt process, since it already knows about something more recent.
For example, this might be if mail is delivered out of order, or if an
inbox is scanned from newest to oldest.

If `inbome_state[A]` has a `last_seen` less than `message_date`, then
we compare `message_pih` with the `pih` currently stored in
`inbome_state[A]`.

This is done as a literal comparison using only the `key` and
`prefer_encrypt` fields, even if the Agent stores additional fields as
an augmentation -- if `key` is bytewise different, or if
`prefer_encrypted` has a different value, then this is an update.  If
`key` and `prefer_encrypted` match exactly, then it is considered a
match.  If both `pih` and `message_pih` are NULL, it is a match.  If
one is NULL and the other is not NULL, it is a update.

In the case of a match, set `inbome_state[A].last_seen` to
`message_date`.

In the case of an update, set `inbome_state[A].pih` to `message_pih`
and `inbome_state[A].last_seen` and `inbome_state[A].changed` to
`message_date`.

NOTE: the above algorithm results in a non-deterministic
`inbome_state` if two INBOME headers are processed using the same
`message_date` (depending on which message is encountered first).  For
consistency and predictability across implementations, it would be
better to have a strict ordering between parsed INBOME headers, and to
always select the lower header in case of equal values of
`message_date`.

NOTE: OpenPGP's composable certificate format suggests that there
could be alternate ways to compare `key` values besides strict
bytewise comparison.  For example, this could be done by comparing
only the fingerprint of the OpenPGP primary key instead of the
keydata.  However, this would miss updates of the encryption-capable
subkey, or updates to the capabilities advertised in the OpenPGP
self-signature.  Alternately, the message receipt process could
incorporate fancier date comparisons by integrating the timestamps
within the OpenPGP messages during the date comparison step.  For
simplicity and ease of implementation, level 0 INBOME-capable agents
are expected to avoid these approaches and to do full bytestring
comparisons of `key` data instead.


Generating an INBOME header upon message composition
----------------------------------------------------

During message composition where the message will be marked as `From:`
an e-mail address that the INBOME-capable agent knows the secret key
material for, it should always include an INBOME header with the
associated public key material as the `key=` attribute, and it should
include the `to=` attribute for recipients to match on.

If the `From:` address changes during message composition (e.g. if the
user selects a different outbound identity, the INBOME-capable client
MUST change the INBOME header.

NOTE: we need documentation about key expiry -- INBOME-capable clients
that choose to have an expiry policy on their secret key material
should use message composition as an opportunity to refresh their
secret key material or update the expiration dates in their public
certificate.


Choosing encryption and UI during message composition
-----------------------------------------------------

On message composition, an INBOME-capable agent also has an
opportunity to decide whether to try to encrypt an e-mail.  INBOME
aims to provide a reasonable recommendation for the agent.

Any INBOME-capable agent may have other means for making this decision
outside of INBOME.  INBOME provides a recommendation to this process,
but there is no requirement for INBOME-capable agents to always follow
the INBOME recommendation.  For example, an INBOME-capable agent that
also incorporates the OpenPGP "Web of Trust" might already know about
a non-INBOME public key that it considers to be correctly bound to the
recipient e-mail address.  It may wish to prefer such a key, and to
decide to use for a given outbound message over any recommendations
provided by INBOME.

That said, all INBOME-capable agents should be able to calculate the
same INBOME recommendation due to their internal state.

INBOME can produce three possible recommendations to the agent during
message composition:

 * `disable` : Disable or hide any UI that would allow the user to
    choose to encrypt the message.  Prepare the message in cleartext.

 * `available` : Enable UI that would allow the user to choose to
   encrypt the message, but do not default to encryption.  Prepare the
   message in cleartext.

 * `encrypt` : Enable UI that would allow the user to choose to send
   the message in cleartext, and default to encryption.  Prepare the
   message as an encrypted message.

Single recipient messages
-------------------------
   
For level 0 agents, the INBOME recommendation for message composed to
a single recipient with e-mail address `A` is derived from the value
stored in `inbome_state[A]`.

If the `pih` is NULL, or if `pih.key` is known to be unusable for
encryption (e.g. it is otherwise known to be revoked or expired), then
the recommendation is `disable`.

If the `pih` is not NULL, and `prefer-encrypted` is `yes`, then the
recommendation is `encrypt`.

If `pih` is not NULL, and `prefer-encrypted` is either `no` or
`nopreference`, then the recommendation is `available`.

Message composition to multiple addresses
-----------------------------------------

For level 0 agents, the INBOME recommendation for a message composed
to multiple recipients is derived from the recommendations for each
recipient individually.

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
that syncing updates to `pih` and `changed` should be sufficient, and
that peers do not need to sync `last_seen`.  This has not been proved
in practice.

how to deal with multiple types (at least when a new type is
specified).  When we support types other than `p`, it's possible that
users will have multiple keys available, each with a different type.
That seems likely to introduce some awkward choices during message
composition time, particularly for multi-recipient messages.
