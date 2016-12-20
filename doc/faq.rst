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


Why are we using IMAP folders rather than self send messages for multi device?
------------------------------------------------------------------------------

Self send messages end up in your inbox and might be confusing to
users. They are likely also processed by your spam protection and
might look like spam.


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

We need to store state about the key to use for a given email
address. Just importing the key into a keyring won't cut it.

We want to be able to handle the header without having to parse the
key first.  We believe that using the 'to' attribute will be more
forward compatible. For example we discussed hashing the uid in the
keys so in case they leak to pgp keyservers they do not leak the email
address. This would not be compatible with requiring the email address
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
