Key Transfer Format
===================

This document describes a format recommendation for secret key backup
attchments. The Autocrypt Key Transfer Format is designed to work as an
attachment in a mail client that can be handled automatically by Autocrypt
clients, but also strives for usability when saved as a file in agnostic
clients.

This goal is achieved by two mechanisms:

- The MIME part MUST have a Content-Disposition of "attachment". Its filename,
  as specified in Content-Type and Content-Disposition header parameters, MUST
  have an extension of ".html".
- The file MUST be formatted as proper HTML. It SHOULD give a human-readable
  description at the beginning, and MUST include the encrypted key as a
  contiguous block of ASCII-armored data, with no indentation or HTML tags
  inside. This block SHOULD reside inside a <pre> block for readability.

With this technique, the way the attachment is handled when saved to disk by the
user is independent from its handling by clients aware of its Content-Type. HTML
as the actual file content is chosen as a universal and familiar format. It can
be opened in a browser, allowing the file to provide a description of itself "on
double-click" on almost any system.

Since the file contains an easy to locate block of ASCII-armored data, it can
still easily be processed by OpenPGP tools. In particular, GnuPG ignores the
header before the armored data starts, so a regular call to :code:`gpg
--decrypt` still works.

An exemplary secret key backup MIME part would look as such:

.. code-block:: html

  Content-Type: application/pgp-key-backup; name="Autocrypt-Key for name-at-example.org.html"
  Content-Description: OpenPGP Digital Signature
  Content-Disposition: attachment; filename="Autocrypt-Key for name-at-example.org.html"

  <html><body><h1>Autocrypt Key</h1><p>

  This is an Autocrypt Key file. When imported into an Autocrypt capable E-Mail
  client with its backup code, it can be used to read encrypted E-Mail sent to
  name@example.org.

  </p><pre>
  -----BEGIN PGP MESSAGE-----

  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
  =CwOM
  -----END PGP MESSAGE-----
  </pre><hr><i><a href="http://example.org/">Generated by Autocrypt-capable Client™</a>.</i></body></html>
