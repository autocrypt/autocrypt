Key Formats for INBOME
======================

``p`` - OpenPGP Based
-----------------

INBOME requires keys of a certain format to reduce the requirements for implementations.

If OpenPGP key format is used, the message also uses OpenPGP Message encoding (pgp/mime)

**For New Users**

We are standardizing on eliptic curve crypto based on ed25519 for the primary key and cv25519 for the encryption-capable subkey.
We only include a minimum key in the headers that has:

* a ed25519 primary key ``Kp``

  * a uid that is the email address
  * a self signature

* one cv25519 encryption subkey ``Ke``

  * a signature for the subkey by the primary key

**Reasoning**

*Why ed25519+cv25519*

short keys for short header lines
  
*why email address as uid*

 Possibilities for uid we considered:
 
 ======= == == == === ==
 Option  SC BC VO RvK SR
 ======= == == == === ==
 no uid            x  x
 email   x  x   x  x   
 fixed         x   x  x
 hash    x      x   x x
 ======= == == == === ==
 
SC: self-claim. This was very important to us for usability reasons. This restricted us to either use the email directly or hashed.

BC: backwards compatibility

VO: valid OpenPGP

RvK: allows revocations using keyservers

SR: Spam resistant/publicly list email addresses

Using a salted hash of the email address for the uid to not list them on keyservers
would prevent the privacy issue of public mail addresses but the key should not be
uploaded in the first place.
Accidental or malicious uploading of keys with associated email addresses should be
prevented by introducing a flag at the keys that says that keyservers shouldn't accept it.
See `issue #7 <https://github.com/mailencrypt/inbome/issues/7>`_.


**For current OpenPGP users**

* What about other keys, that i have been using with other properties? (smart-card, RSA, ...)

  * You can still create a compatible header with a tool we will provide. We are targeting users who have not used pgp before. Never the less most clients will still support other key formats. But they are not required to.
