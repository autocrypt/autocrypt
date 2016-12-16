Why are you using headers rather than attached keys?
-----------------------------------------------------

Attachments are visible to users of non INBOME compatible MUAs.


Why are you sending keys in all the mails and not just announcing capabilities?
-----------------------------------------------------------------------------------

We did this in a previous version. We decided against it because it requires the MUA to keep
the information who announced INBOME and who they requested keys from.


Why are we using IMAP folders rather than self send messages for multi device?
------------------------------------------------------------------------------

Self send messages end up in your inbox and might be confusing to users. They
are likely also processed by your spam protection and might look like spam.


Why do you aim to use ed25519 - it's not supported by X?
---------------------------------------------------------

They give us much smaller keys that lead to smaller headers and make it easier
to include them. You can even write them down as a backup code.
We want to support implementation where needed.


So you say you care about header size... but then you type out prefer-encrypt?
----------------------------------------------------------------------------------

An ECC key is roughly 500 bytes formated in Base64 and RSA 2048 key is 1750 bytes.
The Length of attribute name does not matter so much. So we opted for readability.


Why do you drop all headers if there is more than one?

Because of multi-agent usage we may have to handle an inconsistent stream of
headers already. Making this an inconsistent stream of multiple keys with
priorities sounds like a lot of pain.

What if I want two different keys announced?

If you really care about supporting other keys than what we use in
INBOME there is the OpenPGP header that could use some standardization and
automatic client support. Feel free to innovate there.

If we want to enable multiple headers in the future we can still add INBOME
headers with a critical attribute 'priority'. Versions that do not support it
yet will drop these headers and fall back to the one without priority.


Why do you use the 'to' attribute rather than the uid from the key?

We need to store state about the key to use for a given email address. Just
importing the key into a keyring won't cut it.
We want to be able to handle the header without having to parse the key first.
We believe that using the 'to' attribute will be more forward compatible. For
example we discussed hashing the uid in the keys so in case they leak
to pgp keyservers they do not leak the email address. This would not be
compatible with requiring the email address as the uid.

