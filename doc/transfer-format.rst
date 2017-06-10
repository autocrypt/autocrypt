Autocrypt Setup Message Transfer Format
=======================================

This document describes a format recommendation for the Autocrypt
Setup Message payload. The Autocrypt Setup Message payload is an
attachment in a mail client that can be handled automatically by
Autocrypt clients, but also strives for usability when saved as a file
in agnostic clients.

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

An exemplary Autocrypt Setup Message's MIME part would look like the
text below.  This Autocrypt Setup Message can be unlocked with the
Setup Code ``D9VN-RD7A-7T3B-BWG7-LEPY-3NYT``.

.. code-block:: html

  Content-Type: application/pgp-key-backup; name="Autocrypt-Key for name-at-example.org.html"
  Content-Description: OpenPGP Digital Signature
  Content-Disposition: attachment; filename="Autocrypt-Key for name-at-example.org.html"

  <html><body><h1>Autocrypt Key for <tt>example.org</tt></h1><p>

  This is an Autocrypt Key file. When imported into an Autocrypt capable E-Mail
  client with its backup code, it can be used to read encrypted E-Mail sent to
  <tt>name@example.org</tt>.

  </p><pre>
  -----BEGIN PGP MESSAGE-----
  Autocrypt-Setup-Message: v1

  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
  xUbOVydoyTLaP9bQScqv4WBqVcw5k8v4i+I=
  =k6Rc
  -----END PGP MESSAGE-----
  </pre><hr><i><a href="http://example.org/">Generated by Autocrypt-capable Client</a>.</i></body></html>
