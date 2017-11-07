Frequently Asked Questions about Autocrypt
==========================================

Why are you using headers rather than attached keys?
----------------------------------------------------

Attachments are visible to users of non Autocrypt-compatible MUAs,
while headers are not.  We don't want to present distracting or
confusing material to those users.

Why are you sending keys in all the mails and not just announcing capabilities?
-------------------------------------------------------------------------------

We did this in a previous version. We decided against it because it
requires the MUA to keep the information who announced Autocrypt and
who they requested keys from.


Why RSA3072 and 25519 only later?
---------------------------------

Curve 25519 keys are shorter, cheaper to compute on, and likely to be
at least as strong as RSA 3072 against non-quantum attackers.  You can
even write them down as a backup code.  However, we want level 1 to be
implementable in 2017, and more toolkits support RSA 3072 than 25519.
Future versions are likely to encourage 25519 over RSA 3072.


So you say you care about header size... but then you type out prefer-encrypt?
------------------------------------------------------------------------------

An ECC key is roughly 500 bytes formatted in Base64 and RSA 3072 key
is about 2350 bytes.  The Length of attribute name does not matter so
much. So we opted for readability.


Why do you drop all headers if there is more than one?
-------------------------------------------------------------

We could come up with rules on which header to pick. But whatever we
do, it has to be deterministic, clear and agreed upon by all MUAs
so their behaviour is predictable and stable for users who might try
multiple MUAs.

Dropping all headers is the simplest way to avoid an ambiguous state
in level 1. Once we have more experience from the field we'll know how
this fails and at that point we'll be in a position to draft more
complicated rules.

Forcibly rejecting multiple headers deters MUAs from gratiutously
sending conflicting headers which may confuse recipients.


What if I want my MUA to announce two different keys?
-----------------------------------------------------

Level 1 aims to keep the complexity low for MUAs growing Autocrypt
support. If we want to enable multiple headers in the future we can
still add ``Autocrypt`` headers using a new critical attribute.
Versions that do not support it will ignore these headers as invalid and
just use the single valid Autocrypt header.


Why do you use the ``addr`` attribute rather than the uid from the key?
-----------------------------------------------------------------------

We want to be able to handle the header without having to parse the
key first.  We believe that using the 'addr' attribute will be more
forward compatible. For example we discussed hashing the uid in the
Level 1 PGP keys so in case they leak to keyservers they do not leak
the e-mail address. This would not be compatible with requiring
the e-mail address as the uid.


How does Autocrypt interact with message signing?
-------------------------------------------------

In general, Autocrypt assumes that mail is either plaintext mail, or
it is both encrypted and signed.  This assumption makes it possible to
create a simpler user experience.

While there are valid usecases for signed, unencrypted mail, or for
encrypted, unsigned mail, they are not the use case targeted by
Autocrypt.

Why use OpenPGP and PGP/MIME instead of some other encryption tech?
-------------------------------------------------------------------

We picked a commonly-understood and widely used decentralized mail encryption
technology so that implementers wouldn't need to start from scratch.

Future levels of the Autocrypt specification may support different
encryption technologies, but the main immediate goal is to get wider
adoption, not to re-invent the encryption mechanism itself.

Why don't you use the ``User-Agent`` header to detect different mail apps?
------------------------------------------------------------------------------------

Not all mail apps send a ``User-Agent`` header (and there is an ongoing
effort to discourage its use as a way to reduce metadata leakage).
Also, some mail apps are used only to read mail, and are not used to
send at all, so the remote peer can't see anything about those specific
apps.

We could encourage each MUA to publish a UUID to inform the remote
peer that multiple mail apps are in use, but it's not clear that this
offers much benefit, and it leaks information that we may not want to leak.


What about spammers accidentally downgrading encryption?
--------------------------------------------------------

A spammer who forges mail from a given address could potentially
downgrade encryption for that person as a side effect.  Please see
:ref:`the Level 1 documentation <spam-filters>` for details
about expected interaction with spam filters.


How does Autocrypt interact with today's mailing list managers?
---------------------------------------------------------------

Mailing lists that distribute cleartext (unencrypted) mail may end up
distributing their user's public key material in the
``Autocrypt`` headers of the distributed mail.  For mailing
lists that rewrite ``From`` headers, these
``Autocrypt`` headers will be dropped by recipients, which
is fine.

For encrypted mailing lists like `schleuder
<http://schleuder2.nadir.org/>`_, we haven't done a full analysis yet.
Help welcome.


Why do you require MUAs to detect if another is using Autocrypt already?
------------------------------------------------------------------------

In the event that two Autocrypt-enabled MUAs operate a single
e-mail account, they could clash and cause usability problems:
If they each manage their own secret key material, communicating peers
might arbitrarily choose one key or another to encrypt to, and then
certain mails will be unreadable with certain MUAs, in an
apparently-arbitrary pattern based on the origin of the remote peer's
last-received message.

Level 1 therefore defines an Autocrypt setup process which involves sending
and receiving a :ref:`setup message <setup-message>`. This allows two Autocrypt MUAs to share
secret key material so that mails can be decrypted and read on both devices.
This transfer of secret key material currently requires the user to type in
a long :ref:`setup code <setup-code>`.  For level 2, we aim to provide a pairing mechanism
which only uses a short number to secure the peering.


Why do you cap ``Date`` to the current time?
---------------------------------------------------------

E-mail messages with ``Date`` in the future could destroy
the ability to update the internal state.

However, since different MUAs process messages at different times,
future-dated e-mails could result in state de-synchronization.

.. todo::

   deeper analysis of this state de-sync issue with future-dated
   e-mails, or alternate, more-stable approaches to dealing with wrong
   ``Date`` headers.


Why do you always encrypt-to-self?
----------------------------------

Users expect to be able to read their outbox or Sent Messages folders.
Autocrypt should not get in the way of that.


Why ``prefer-encrypt=mutual`` and not more aggressive choices?
--------------------------------------------------------------

We considered and discarded several other designs for
``prefer-encrypt`` before settling on ``prefer-encrypt=mutual``.  The
other designs we considered tended to have a scenario where e-mail was
automatically encrypted with greater frequency.

We opted for the less-aggressive design because we wanted to avoid
annoyances for users who want to be able to get encrypted e-mail when
they need it, but who actually have logistical trouble with handling
encrypted messages (e.g. the user often uses a liimted MUA
that cannot decrypt).  In particular, unpleasant surprises (unwanted
encrypted mail) tended to happen when the communicating peers have
different preferences, which can demotivate the very people for whom
encrypted mail capability is marginal anyway.

We want to broaden the group of people who might be able to use
encrypted mail; to reduce the pressure to uninstall mail encryption
capabilities; and to reduce the human-to-human pushback ("please quit
sending me encrypted mail").  So we only automatically encrypt between
peers who have both opted in.

Why not use a better KDF for symmetric encryption of the Setup Message?
-----------------------------------------------------------------------

Use of a memory-hard KDF like scrypt or argon2 would be desirable in the future.
However, at the point of this writing this is not specified in OpenPGP. It is a
bigger concern to preserve compatibility and avoid friction with presently
deployed OpenPGP software.

Where does the "35 days" limit come from?
-----------------------------------------

The recommendation algorithm uses a duration gap of 35 days to make a
decision in a few places.  This is an arbitrary value, which seemed
plausible to most people who worked on the specification, based on the
idea that for people who you want to communicate with regularly, it's
not uncommon that the user has exchanged e-mails at least once a
month.  It's intended to be slightly more than monthly, so that people
who have scheduled e-mail exchanges (e.g. "please check in on the 1st
of the month") will stay current.

Future revisions to the recommendation algorithm may change this
cutoff.  If you have evidence that there are algorithms that provide
better results, :ref:`please share them <contact channels>`!
