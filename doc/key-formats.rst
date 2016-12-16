Key Formats for INBOME
======================


p - OpenPGP based
-----------------

INBOME requires keys of a certain format to reduce the requirements for implementations.
We are standardizing on:
* eliptic curve crytpo based on ed25519
* a long term identity key
* one encryption key
* a signature for the encryption key by the identity key

