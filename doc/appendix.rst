Appendix
=========

.. _autocrypt_example_message:

Autocrypt example message
-------------------------
::

    Delivered-To: <bob@testsuite.autocrypt.org>
    From: Alice <alice@testsuite.autocrypt.org>
    To: Bob <bob@testsuite.autocrypt.org>
    Subject: an Autocrypt RSA test
    Autocrypt: addr=alice@testsuite.autocrypt.org; keydata=
    mQENBFhVF+ABCAD...

    Date: Sat, 17 Dec 2016 10:07:48 +0100
    Message-ID: <rsa2048-simple@testsuite.autocrypt.org>
    MIME-Version: 1.0
    Content-Type: text/plain

    This is an example e-mail with Autocrypt header as defined in Level 1.

Key Gossip Example Message
--------------------------

::

   From: Me <me@example.com>
   To: Them <them@example.org>
   Cc: Other <other@example.org>, Odder <odder@example.org>
   Content-type: multipart/encrypted; protocol="application/pgp-encrypted"; boundary="==break=="

   --==break==
   Content-Type: application/pgp-encrypted

   Version: 1

   --==break==
   Content-Type: application/octet-stream

   -----BEGIN PGP MESSAGE-----

   hQIMAxC7JraDy7DVAQ//SK1NltM+r6uRf2BJEg+rnpmiwfAEIiopU0LeOQ6ysmZ0
   CLlfUKAcryaxndj4sBsxLllXWzlNiFDHWw4OOUEZAZd8YRbOPfVq2I8+W4jO3Moe
   ...
   -----END PGP MESSAGE-----
   --==break==--

The encrypted message part contains:

::
   Content-Type: text/plain
   Autocrypt-Gossip: addr=them@example.org; keydata=
        SK1NltMhQIMAxC7JraDy7DVAQ//+r6uRf2BJEg+rnpmiwfAEIiopU0LeOQ6ysmZ0
        ...
   Autocrypt-Gossip: addr=other@example.org; keydata=
        zlNiFDHWw4OOUEZAZd8YRbOPfVq2I8CLlfUKAcryaxndj4sBsxLllXW+W4jO3Moe
        ...
   Autocrypt-Gossip: addr=otter@example.org; keydata=
        W4jO3MoezlNiFDHWw4OOUEZAZd8YRbOPfVq2I8CLlfUKAcryaxndj4sBsxLllXW+
        ...

   Encrypted text message
