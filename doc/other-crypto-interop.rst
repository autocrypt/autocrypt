Interoperability With Other Cryptographic E-mail Mechanisms
===========================================================

Many MUAs that aim to become Autocrypt-compatible will already have
implementations of other e-mail encryption mechanisms.

We have concrete guidance for those MUAs that we hope is useful.

Message encryption recommendations
----------------------------------

An Autocrypt-capable MUA that also incorporates the OpenPGP "Web of
Trust" might already know about a non-Autocrypt public key that it
considers to be correctly bound to the recipient e-mail address.  It
may wish to prefer such a key, and to decide to use for a given
outbound message over any recommendations provided by Autocrypt.


For current OpenPGP users
-------------------------

* What about other keys, that i have been using with other properties?
  (smart-card, RSA, ...)

  * You can still create a compatible header with a tool we will
    provide. We are targeting users who have not used pgp
    before. Nevertheless most clients will still support other key
    formats. But they are not required to.


.. todo::

   More guidance here!





Interoperability with existing PGP practises
-------------------------------------------------

should Autocrypt keys appear on key servers?

- no!

should i add rcvd Autocrypt keys into my PGP keyring? (if my mua already supports PGP)

- yes

should my own Autocrypt keys appear in my keyring?

- no
  (why not?  how else can we do encrypt-to-self, or message signing?)

can I put my regular pgp keys into Autocrypt?

- MUAs should not provide UI for importing keys for Level 1
- allowed for Level 1 to get traction early on (as replacement for keyservers)

can I use someone's pgp key that i have for encrypting mail to that person?

- This would work like without Autocrypt

if i have for a person an non-Autocrypt pgp key and an Autocrypt key, which one do
i use to encrypt mails for that person?

- Look up e-mail address in pgp keyring
- if there is a key that has better user ID validity for the matching address than "unknown", use that one
- else look up a key from the Autocrypt state (which is also in the keyring)

two target audiences:

- end-users
- mail software devs
