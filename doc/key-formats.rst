Key Formats for INBOME
======================


p - OpenPGP based
-----------------

INBOME requires keys of a certain format to reduce the requirements for implementations.
We are standardizing on eliptic curve crytpo based on ed25519.
We only include a minimum key in the headers that has:
* a long term identity key S,C
** a uid ?
** a self signature
* one encryption key
** a signature for the encryption key by the identity key

What about other keys, that i have been using with other properties?
(smart-card, RSA, ...)
You can still create a compatible header with a tool we will provide. We are
targeting users who have not used pgp before. Never the less most clients will
still support other key formats. But they are not required to.
