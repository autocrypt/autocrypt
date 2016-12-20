Cleanup needed
--------------

doc/_templates/globaltoc.html points to several docs that don't yet
exist.  Much of the information throughout that intended layout are
currently in several other unindexed pages.  Merging the existing .rst
files into the proposed structure would be very helpful.

RFC 2231 talks about the elements of a MIME header as "parameters"
instead of "attributes".  RFC 2045 specifies the same vocab.  We
should normalize.

Let's use "cert" where we mean "cert" and "key" where we mean "key"

need a tight document for what is expected of level 0 clients
(level0.rst).

user-facing material probably should use "app" -- for technical
documentation, we need to settle internally on "agent" or "client" or
"MUA" or "MUAA"

glossary for technical documentation.

we should use "email" or "e-mail" consistently in these docs

rst markup probably needs cleanup.

