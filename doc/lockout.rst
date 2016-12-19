Account Lockout for Autocrypt
=============================

Autocrypt-enabled MUAs are aware that encrypted messages can only be
read directly on the Autocrypt-enabled agent that connects to the
e-mail accout.

Problem statement
-----------------

In the event that two Autocrypt-enabled agents operate a single
e-mail account, they could clash and cause serious usability problems.
In particular, if they each manage their own secret key material,
communicating peers might arbitrarily choose one key or another to
encrypt to, and then certain mails will be unreadable with certain
agents, in an apparently-arbitrary pattern based on the origin of the
remote peer's last-received message.

So we need either synchronization between Autocrypt agents on a single
account, or there needs to be only one such agent on a given account.

For level 1 and higher, we aim to provide a synchronization mechanism
so that all Autocrypt-enabled MUAs connected to a single account are
capable of reading encrypted mail.

For simplicitly, level 0 does not require or define synchronization
mechanisms, but instead allows an Autocrypt-enable client to "lock"
the account so that multiple Autocrypt-enabled clients don't end up
sending different keys.

Account Locking Mechanism
-------------------------

A Level 0 Autocrypt-enabled client can claim an e-mail account by
dropping a customized message in a well-known IMAP folder.

FIXME: describe the lockout message in specific detail

FIXME: declare the name of the well-known folder

FIXME: describe the tradeoffs and workflow for level-0 agents sharing
an account with future level-1 clients, or failure modes (e.g. lockout
by an agent you no longer use)

