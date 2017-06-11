Preventing against injected private keys ++++

When transferring a secret key, the passphrase authenticates the message.  That
is, the fact that the user knows the passphrase means that the contents are
authentic. This means that to ensure that the message is authentic, the
autocrypt implementation must check that the passphrase is correct.

Unfortunately, GnuPG's --decrypt option doesn't mean that it must decrypt a
packet (and will fail if not), it just means that if GnuPG encounters an
encrypted packet while processing the message, it will try to decrypt it. Thus,
if a message contains just a literal packet, then
GnuPG with the --decrypt option will not fail; it will just emit the contents
of the literal packet.

Another example where something could go wrong is if a key is encrypted with
the user's private key and the passphrase is cached.  In this case, GnuPG will
not use any SK-ESK packet to retrieve the session key, but will use the PK-ESK
packet. In other words, it won't verify
that the passphrase is correct.

There may be other scenarios and other implementations may have other gotchas.

To avoid these issues, it is imperative that the autocrypt implementation
ensure that the OpenPGP implementation actually check that the supplied
passphrase is correct, e.g., by making sure that it decrypts the SK-ESK packet
using the supplied passphrase.

On GnuPG, we recommend using a temporary home directory (using --homedir) when
doing the decryption.  This ensures that the gpg-agent does not have any
passphrases cached.   Furthermore, the --status-fd output should be checked to
make sure that a decryption actually
occured.  This protects against the aforementioned literal data packet attack.

An example of a literal data packet message is provided below. If your
autocrypt implementation imports this private key successfully, then your
implementation is broken.


-----BEGIN PGP MESSAGE-----

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
eRrfNvCvwUu0hP82lv0D
=9WbE
-----END PGP MESSAGE-----
