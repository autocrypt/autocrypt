Best Practices for E-mail Service Providers
===========================================

Autocrypt is designed to provide end-to-end encrypted e-mail with *no*
assistance from the user's e-mail service provider.  It should work
fine as long as the provider offers the user simple,
standards-compliant e-mail.

However, e-mail service providers may be sympathetic to the goals of
Autocrypt, and may want to facilitate it for their users.  This
document describes best practices for operating an Autocrypt-friendly
mail service.

Baseline Requirements
---------------------

As noted in :ref:`provider-requirements`, the service provider MUST
offer the user's MUA the ability to:

- Control the contents of outgoing e-mail including the ability to set
  custom e-mail headers;

- Send e-mail on its own (required by the :ref:`setup-message`);

- Read whole, raw e-mails including message headers

Typically the first two (outbound) mechanisms are provided by
:rfc:`SMTP Submission <6409>`, and the final (inbound) mechanism is
provided by :rfc:`IMAP <3501>` or :rfc:`POP3 <1939>`, which are widely
supported by many MUAs.

However, the provider may offer any protocol(s) that it expects its
users' MUAs to implement which meet the guidelines above.

Allow Easy Search by Top-Level MIME Headers
-------------------------------------------

A MUA that enables Autocrypt for an account typically requires
searching for a :ref:`setup-message`

For example, a provider that offers the :rfc:`IMAP SEARCH command
<3501#section-6.4.4>` can facilitate this search from the server side:

    C: A123 SEARCH HEADER Autocrypt-Setup-Message "v1" FROM "alice@example.org" TO "alice@example.org"
    S: * SEARCH 452
    S: A123 OK SEARCH completed

Do Not Tamper With Existing Autocrypt Headers
---------------------------------------------

DKIM-sign the user-provided Autocrypt header
--------------------------------------------

Case-insensitive e-mail addresses
---------------------------------
