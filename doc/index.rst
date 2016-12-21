Autocrypt - E-mail Encryption for Everyone
==========================================

**The Autocrypt project aims to ease end-to-end email encryption 
such that it eventually happens automatically.**

E-mail has been declared dead many times but refuses to die. It remains
the largest open federated identity and messaging system, anchors the
web, mobiles and continues to relay sensitive information between
citizens and organisations. And that despite the constant drag of
apps who want to lure us into in-app-only communication.

The autocrypt project is driven by various mail app developers, hackers 
and researchers who are willing to take fresh approaches, learn from
past mistakes, and collectively aim to increase the overall encryption
of E-Mail in the net.  The group effort was born and named "autocrypt"
on December 17th 2016 by ~20 people during a 5-day meeting at the 
OnionSpace in berlin. It's a dynamic, fun process which is open to 
new influences, contributions and people. No need to tweet btw but
please do join our `autocrypt mailing list`_ :)

Features of the Autocrypt effort
--------------------------------

End-to-end encrypted e-mail has been around for decades, but has failed
to see wide adoption outside of specialist communities, in large part
because of difficulties user experience and certification models.
To better understand how the fresh autocrypt effort is different 
from previous ones here are some of its features:

- **Protect first against passive data-collecting adversaries**,
  resist the temptation to early-add complexity which aim to 
  prevent active attacks.  See `RFC7435 A New Perspective
  <https://tools.ietf.org/html/rfc7435#section-1.2>`_ for some
  motivation of this and the next points.
 
- **Focus on incremental deployment**, always consider that there
  will be both autocrypt-enabled MUAs and traditional plain ones,
  interacting with each other. 

- **Don't ask users anything about keys, ever.** And minimize and 
  useability-test what needs to be decided by users and include 
  resulting UI guidance in the specs.  Minimize friction for people 
  using multiple mail apps with their accounts.

- **Go for mail app changes, don't require changes from mail providers**, 
  allowing fluid development of deployable code and specs.

- **Use decentralized, in-band key discovery.**  Make mail apps
  tell each other how and when to encrypt to each other
  by attaching neccessary information along with mails.

- **Implement and specify "level0" support in several MUAs in spring
  2017.**  Keep level0 minimal enough that it's easy for developers to
  adopt it and we can start to drive efforts from real-life experiences.
  Currently involved are developers from K9/Android, Enigmail, Mailpile, 
  Bitmask/LEAP and others who are interested to add support for OSX 
  or write reference "MUA bots" in Python or Go.


Current docs (work-in-progress)
-------------------------------

The following in-progress documents are written for software developers
and privacy enthusiasts.

:doc:`Autocrypt key discovery <mua-keydiscovery>`
     presents and discusses how mail programs negotiate encryption
     with each other.

:doc:`Autocrypt key format <key-formats>`
     discusses the precise header and key format.

:doc:`Autocrypt levels <levels>`
     discusses level0 and level1 support.

:doc:`Autocrypt MUA internals <mua-internals>`
     discusses requirements, operations and the state MUAs need to
     keep in order to implement the Autocrypt protocols.

:doc:`ecosystem-dangers`
     some documented risks and dangers to the mail ecosystem,
     related to Autocrypt.


unsorted collection of docs and fragments
+++++++++++++++++++++++++++++++++++++++++++++++

:doc:`muaa-state` 

:doc:`multi-device`

:doc:`lockout`

:doc:`message-encryption`

:doc:`pgp-interop`

:doc:`user-experience`


Contact points
----------------------

If you want to help, including offering constructive criticism, 
you may:

- join the `autocrypt mailing list`_

- join chats at **#nextleap on freenode or matrix.org**.

- collaborate through PRs, issues and edits on our
  `github autocrypt repo <https://github.com/autocrypt/autocrypt>`_

.. _`autocrypt mailing list`: https://lists.mayfirst.org/mailman/listinfo/autocrypt

Next events
-------------

- Dec 2016: at 33c3, Hamburg, scheduled talk at the 
  "we fix the net session" and probably a separate one.

- Jan 2017: a prospective lightning talk from dkg at 
  real-world-crypto the week after in New york

- Mar 2017: autocrypt sessions at the Internet Freedom Festival
  with hackers and users, several autocrypt-people there.

- April/May 2017: next autocrypt unconf-hackathon planned
  roughly around DE/NL/CH



.. 
    :doc:`Autocrypt reasons <reasons>` lists reasons and frequent questions. 

.. toctree::
   :hidden:

   mua-keydiscovery
   key-formats
   mua-internals
   levels
   multi-device
