Why Autocrypt?
==============

*by Valodim, 19.02.2017*

In the past couple of months, I had conversations about Autocrypt with many
people, on various conferences and other occasions. In this blog post, I will
try to reflect on these conversations, and try to answer the typical questions
that came up.

First off, let me say that OpenPGP is an old standard, and thus comes with a lot
of tradition. It has lived through various periods, from the crypto wars to the
Cryptoparty hype after the Snowden revelations. GnuPG, suite of tools. This
tends to attract "power users", who feel right at home with a complex system
that gives them a huge amount of options and learning opportunities behind every
corner.

The core question that people have is "PGP has been around for 20 years, what
are you doing differently?" When a technically well-versed user skims our spec,
they are often left with the impression that Autocrypt is "just keys in
headers". And this is true, in a way - for the core Autocrypt mechanism, there
is little more to it technically than "keys in headers".

The Autocrypt spec tries to provide a basis for a coherent user experience for
encrypted e-mail. Towards this overarching goal, the spec includes a couple of
technical mechanisms, but no single one of these "is" Autocrypt on its own.

For the single use case of encrypted e-mail, we tried to pinpoint the set of
required workflows, and designed the spec to support these with as little
friction as possible for the user. Secondary design criteria were keeping
implementation complexity to a minimum, leaving room for future extensions,
while retaining some backwards compatibility with the existing OpenPGP
ecosystem.

The workflows we want to support are as follows:

1) Encryption between Autocrypt clients. This should typically be single click
   opt-in, no questions asked.
2) "Reply to all" to encrypted mail should always just work.
3) There should be a simple way for transferring the user's key setup from one
   client to another.

I'm going to stick to the first one in this blog post.

The part that took us the longest to figure out is actually a social aspect: For
every encrypted e-mail, the decision to encrypt must lie with a human. Given the
e-mail infrastructure, encrypted e-mails are inherently less convenient than
plaintext.
