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


Why are we using IMAP folders rather than self-sent messages for multi device?
------------------------------------------------------------------------------

Self-sent messages end up in your inbox and might be confusing to
users who use multiple MUAs. They are also likely also processed by
your spam filters and might look like spam.

IMAP folders are more a stable and reliable transport, as well as
being conceptually simpler to look for.


Why not use IMAP METADATA instead of specially-named folders?
-------------------------------------------------------------

We ultimately want Autocrypt to be more generic than IMAP, to make it
clear how other mail-checking protocols could work (e.g. MAPI, webmail
interfaces) as long as they offer some sort of namespaced shared
storage.  Using `IMAP METADATA <https://tools.ietf.org/html/rfc5464>`_
would tie Autocrypt more tightly to IMAP, and would also limit the
number of IMAP implementations that Autocrypt-enabled clients could
connect to (METADATA is `not widely supported by today's IMAP server
implementations <http://www.imapwiki.org/Specs>`_).

If we wanted Autocrypt to use METADATA where it was available on the
server, but allow for fallback to normal folders for IMAP servers that
don't support METADATA, then we'd be adding an implementation
requirement for clients that might not already know how to use the
METADATA extension, which makes adoption harder.

And without initially requiring it for clients, we don't see a way to
transition once non-METADATA capable clients exist in the wild,
either, since lockout and sync become difficult to do.  So we don't
see a good story for METADATA deployment, sadly, despite it targeting
our use case fairly neatly.

See also `earlier discussion about IMAP METADATA
<https://github.com/autocrypt/autocrypt/issues/12>`_.


Why do you aim to use ed25519 - it's not supported by X?
--------------------------------------------------------

They give us much smaller keys that lead to smaller headers and make
it easier to include them. You can even write them down as a backup
code.  We want to support implementation where needed.


So you say you care about header size... but then you type out prefer-encrypt?
------------------------------------------------------------------------------

An ECC key is roughly 500 bytes formated in Base64 and RSA 2048 key is
1750 bytes.  The Length of attribute name does not matter so much. So
we opted for readability.


Why do you drop all headers if there is more than one?
------------------------------------------------------

Because of multi-agent usage we may have to handle an inconsistent stream of
headers already. Making this an inconsistent stream of multiple keys with
priorities sounds like a lot of pain.

What if I want two different keys announced?
--------------------------------------------

If you really care about supporting other keys than what we use in
Autocrypt there is the OpenPGP header that could use some standardization and
automatic client support. Feel free to innovate there.

If we want to enable multiple headers in the future we can still add Autocrypt
headers with a critical attribute 'priority'. Versions that do not support it
yet will drop these headers and fall back to the one without priority.


Why do you use the ``to=`` attribute rather than the uid from the key?
----------------------------------------------------------------------

We need to store state about the key to use for a given e-mail
address. Just importing the key into a keyring won't cut it.

We want to be able to handle the header without having to parse the
key first.  We believe that using the 'to' attribute will be more
forward compatible. For example we discussed hashing the uid in the
keys so in case they leak to pgp keyservers they do not leak the e-mail
address. This would not be compatible with requiring the e-mail address
as the uid.

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

We picked a commonly-understood and implemented mail encryption
technology so that implementers wouldn't need to start from scratch.

Future levels of the Autocrypt specification may support different
encryption technologies, but the main immediate goal is to get wider
adoption, not to re-invent the encryption mechanism itself.

Please see `key-formats` for more discussion.

Why don't you use the ``User-Agent`` header to detect different mail apps?
--------------------------------------------------------------------------

Not all mail apps implement the ``User-Agent`` header (and there is an
ongoing effort to discourage its use as a way to reduce metadata
leakage).  Also, some mail apps are used only to read mail, and are
not used to send at all, so the remote peer can't see anything about
those specific apps.

We could encourage each MUA to publish a UUID to inform the remote
peer that multiple mail apps are in use, but it's not clear that this
offers much benefit, and it leaks information that we don't need to
leak.

What about spammers accidentally downgrading encryption?
--------------------------------------------------------

A spammer who forges mail from a given address could potentially
downgrade encryption for that person as a side effect.  Please see
`level0/public-key-management` for details about expected interaction
with spam filters.

How does Autocrypt interact with today's mailing list managers?
---------------------------------------------------------------

Mailing lists that distribute cleartext (unencrypted) mail may end up
distributing their user's public key material in the ``Autocrypt:``
headers of the distributed mail.  For mailing lists that rewrite
``From:`` headers, these ``Autocrypt:`` headers will be dropped by
recipients, which is fine.

For encrypted mailing lists like `schleuder
<http://schleuder2.nadir.org/>`_, we haven't done a full analysis yet.
Suggestions welcome!

Why don't you encourage gossiping keys of other users?
------------------------------------------------------

This is a plausible future improvement for Autocrypt.  But being
willing to accept gossiped keys for other users presents a more
complicated and risky public-key state management situation for the
receiving client.  For example, what if one client gets multiple
different keys for a target address from different gossiping peers --
should the client encrypt to all keys or just some?  How should those
keys interact with keys received from the end peer directly? Because
of these complications, we're sidestepping this problem for level 0.

We welcome drafts proposing sensible ways to manage key gossip in
group e-mail communication for future levels of Autocrypt.

Why can only one Level 0 MUA to "claim" an e-mail account for Autocrypt?
------------------------------------------------------------------------

In the event that two Autocrypt-enabled agents operate a single
e-mail account, they could clash and cause serious usability problems.
In particular, if they each manage their own secret key material,
communicating peers might arbitrarily choose one key or another to
encrypt to, and then certain mails will be unreadable with certain
agents, in an apparently-arbitrary pattern based on the origin of the
remote peer's last-received message.

So we need either synchronization between Autocrypt agents on a single
account, or there needs to be only one such agent on a given account.

For level 1 and higher, we aim to provide a synchronization mechanism
so that all Autocrypt-enabled MUAs connected to a single account are
capable of reading encrypted mail.

For simplicitly, level 0 does not require or define synchronization
mechanisms, but instead allows an Autocrypt-enable client to "lock"
the account so that multiple Autocrypt-enabled clients don't end up
sending different keys.

.. todo::

   Describe the tradeoffs and workflow for level-0 agents sharing an
   account with future level-1 clients, or failure modes (e.g. lockout
   by an agent you no longer use)


Why do you clamp ``Date:`` to the current time?
-----------------------------------------------

E-mail messages with ``Date:`` in the future could destroy the ability
to update the internal state.

However, since different MUAs view messages at different times,
future-dated e-mails could result in state de-synchronization.

.. todo::

   deeper analysis of this state de-sync issue with future-dated
   e-mails, or alternate, more-stable approaches to dealing with wrong
   ``Date:`` headers.

Why do you always encrypt-to-self?
----------------------------------

Users expect to be able to read their outbox or Sent Messages folders.
Autocrypt should not get in the way of that.


Why did you choose the raw e-mail address for the user ID?
----------------------------------------------------------

Possibilities for uid we considered:

 ======= == == == === ==
 Option  SC BC VO RvK SR
 ======= == == == === ==
 no uid            x  x
 e-mail  x  x   x  x
 fixed         x   x  x
 hash    x      x   x x
 ======= == == == === ==

SC: self-claim. This was very important to us for usability
reasons. This restricted us to either use the e-mail directly or
hashed.

BC: backwards compatibility

VO: valid OpenPGP

RvK: allows revocations using keyservers

SR: Spam resistant/publicly list e-mail addresses

Using a salted hash of the e-mail address for the uid to not list them
on keyservers would prevent the privacy issue of public mail addresses
but the key should not be uploaded in the first place.

Accidental or malicious uploading of keys with associated e-mail
addresses should be prevented by introducing a flag at the keys that
says that keyservers shouldn't accept it.  See `issue #1
<https://github.com/autocrypt/autocrypt/issues/1>`_.


Why RSA2048 and not 25519?
--------------------------

Curve 25519 keys are shorter, cheaper to compute on, and likely to be
stronger than RSA 2048 against non-quantum attackers.  However, we
want level 0 to be implementable in late 2016, and more toolkits
support RSA 2048 than 25519.  Future versions are likely to encourage
25519 over RSA 2048.
