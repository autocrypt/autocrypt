Why Autocrypt?
==============

Email has been declared dead many times but refuses to die. It remains
the largest open federated identity and messaging system, anchors the
web and mobile phones and continues to relay sensitive information
between citizens and organisations.

End-to-end encrypted e-mail has been around for several decades, but
has failed to see wide adoption outside of specialist communities, in
large part because of difficulties user experience and certification
models.

The result is that most e-mails sent on the Internet today are still
as transparent as a postcard: a passive attacker who observes them in
transit can see their contents.

The Autocrypt effort aims to develop opportunistic mail encryption
drafts and working code that normal people can use with a minimum of
interruption to their everyday e-mail workflow. To ease adoption, it
restricts itself to only require changes from mail programs (MUAs) but
no changes whatsoever from mail providers.

Autocrypt follows recommendations from `RFC 7435 "Opportunistic
security" <https://tools.ietf.org/html/rfc7435>`_ and specifically
avoids talking to users about keys without them having asked for it
first. **The overall goal of Autocrypt is to help massively increase
the overall number of encrypted mails world wide**.

Autocrypt does not aim to defend against active attackers, and is
*not* a replacement for strongly-authenticated encrypted e-mail.  It
is a replacement for cleartext e-mail.

You may also be interested in the :doc:`Autocrypt User Experience
<user-experience>`.

Increasing the adoption of encrypted mail globally isn't without
:doc:`risks of its own, but we are trying to document those risks and
plan mitigations for them<ecosystem-dangers>`.
