Optional per-peer state
=======================

An Autocrypt-capable client must store some specific state about each
of its peers.

This document attempts to describe additional optional state that can
improve the user experience in some corner cases.

Unlike the standard Autocrypt level 0 state management, some of these
rules depend on a client being able to keep track of whether it has
seen a given message before or not, and these guidelines may cause
non-deterministic results depending on the order that messages are
encountered.

Additional state
----------------

Optionally, an agent MAY store and maintain the following data in
order to provide clearer feedback to the user:

* ``counting_since``: The UTC timestamp of when we started counting
* ``count_have_ach``: A count of parsed AutoCrypt headers
* ``count_no_ach``: A count of messages without AutoCrypt headers
* ``bad_user_agent``: The apparent user-agent (if known) of the last
  message seen without AutoCrypt headers.

.. note::

     These attributes are all optional, and are presented here as a
     recommendation of the type of data an AutoCrypt capable user-agent
     might record in order to provide the user with more detailed
     feedback and guidance when we detect a potential conflict.

     The theory is that a message of the form "The recipient may not be
     able to read encrypted mail" could be augmented with reasons such
     as "The last 5 messages we saw from them all came from a
     non-AutoCrypt capable e-mail application", or "Their most recent
     message was sent on April 5th using Apple Mail on an iPad."

Managing additional state
-------------------------

When processing a message from the peer:

 - OPTIONAL: If ``counting_since`` is unset, set it to the current time.
   Otherwise, if ``message_date`` is greater than ``counting_since``:

   - If ``pah`` is ``null``, increment ``count_no_ac``.
   - If ``pah`` is not ``null`` increment ``count_have_ac``.


After message processng, in the case where the message processed
causes a *reset*:

 - OPTIONAL in the case of a **reset**:

   - set ``autocrypt_peer_state[A].bad_user_agent`` to the apparent
     user-agent of the message

 - OPTIONAL in the case of a **reset** AND ``counting_since`` is more
   than a month older than ``message_date``:

   - set ``autocrypt_peer_state[A].counting_since`` to ``last_seen``
   - set ``autocrypt_peer_state[A].count_have_ach`` to zero
   - set ``autocrypt_peer_state[A].count_no_ach`` to one


Using additional state
----------------------

During message composition, if the Autocrypt recommendation is
``discourage`` this state can be used to craft a more-informative
warning message for the user.
