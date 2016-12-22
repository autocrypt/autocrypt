Autocrypt - E-mail Encryption for Everyone
==========================================

**The Autocrypt project aims to ease end-to-end email encryption 
such that it eventually happens automatically.**

E-mail has been declared dead many times but refuses to die.  And that 
despite the constant drag of apps who want to lure us to
in-app-only communication.  E-mail remains the largest open federated 
identity and messaging eco-system, anchors the web, mobiles and continues 
to relay sensitive information between citizens and organisations. 

The Autocrypt project is driven by mail app developers, hackers 
and researchers who are willing to take fresh approaches, learn from
past mistakes, and collectively aim to increase the overall encryption
of E-Mail in the net.  The group effort was born and named "Autocrypt"
on December 17th 2016 by ~20 people during a 5-day meeting at the 
OnionSpace in Berlin. It's a dynamic, fun process which is open to 
new people, influences and contributions. No need to tweet but
we have :ref:`contact channels` and :ref:`upcoming events`
where you may talk with us.


The Autocrypt Approach
----------------------

The main approach is to use the way emails are exchanged to
exchange all necessary informations encrypt these emails if possible.
For this, email headers shall automatically contain all necessary
informations (such as the current key) to send emails back encrypted.
No key management should be visible to the users.

For simplicity, we want to establish this approach step-by-step
using different "levels".
Level 0 shall be provided and supported in spring 2017 by various mailers.

Note that this is an approach to bring opportunistic email encryption to the mass.
We want to force convenient encryption whenever possible as a better approach to send emails.
This approach is neither perfect not safe.
Metadata tracking (who is sending email to whom) or
active attacks (such as man-in-the-middle) are still possible.


Current docs (work-in-progress)
-------------------------------

The following in-progress documents are written for software developers
and privacy enthusiasts.

:doc:`features`
     discusses how the Autocrypt efforts is different from past 
     e2e encryption efforts.

:doc:`examples`
     Example data flows and MUA state transitions.  This may be the
     easiest place to get started with the concrete ideas behind Autocrypt.

:doc:`level0`
     Minimum requirements and implementer guidance for Level 0
     Autocrypt-capable MUAs.

:doc:`other-crypto-interop`
     Guidance for integrating Autocrypt with other e-mail encryption mechanisms
     and UI for existing MUAs.

:doc:`next-steps`
     Future improvements for Autocrypt, beyond Level 0.

:doc:`ecosystem-dangers`
     Some documented risks and dangers to the mail ecosystem,
     related to Autocrypt.

:doc:`faq`

:doc:`glossary`

.. _`contact channels`:

Channels
--------

If you want to help, including offering constructive criticism, 
you may:

- join the `Autocrypt mailing list`_

- join chats at **#autocrypt on freenode or matrix.org**.

- collaborate through PRs, issues and edits on our
  `github Autocrypt repo`_

.. _`Autocrypt mailing list`: https://lists.mayfirst.org/mailman/listinfo/autocrypt

.. _`github Autocrypt repo`: https://github.com/autocrypt/autocrypt

.. _`upcoming events`:

Upcoming events
----------------

- Dec 2016: at `33c3`_, Hamburg, scheduled talk at the 
  `We Fix the Net`_ session and probably a separate one.

- Jan 2017: a prospective lightning talk from dkg at 
  `RealWorldCrypto 2017`_ in New york

- Mar 2017: Autocrypt sessions at the `Internet Freedom Festival`_
  with hackers and users, several Autocrypt-people there.

- April/May 2017: next Autocrypt unconf-hackathon planned roughly
  around DE/NL/CH

.. _`33c3`: https://events.ccc.de/congress/2016/wiki/Main_Page

.. _`We Fix the Net`: https://events.ccc.de/congress/2016/wiki/Session:We_Fix_the_Net
  
.. _`RealWorldCrypto 2017`: http://www.realworldcrypto.com/rwc2017

.. _`Internet Freedom Festival`: https://internetfreedomfestival.org/
