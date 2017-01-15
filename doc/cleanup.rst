Cleanup needed
--------------

:rfc:`2231` talks about the elements of a MIME header as "parameters"
instead of "attributes".  :rfc:`2045` specifies the same vocab.  We
should normalize.

Let's use "cert" where we mean "cert" and "key" where we mean "key"

user-facing material probably should use "app" -- for technical
documentation, we need to settle internally on "agent" or "client" or
"MUA" or "MUAA"

glossary for technical documentation.
