Autocrypt - E-mail Encryption for Everyone
==========================================

**The Autocrypt project aims to ease end-to-end email encryption 
such that it eventually happens automatically.**

E-mail has been declared dead many times but refuses to die.  And that 
despite the constant drag of apps who want to lure us to
in-app-only communication.  E-mail remains the largest open federated 
identity and messaging eco-system, anchors the web, mobiles and continues 
to relay sensitive information between citizens and organisations. 

The autocrypt project is driven by mail app developers, hackers 
and researchers who are willing to take fresh approaches, learn from
past mistakes, and collectively aim to increase the overall encryption
of E-Mail in the net.  The group effort was born and named "autocrypt"
on December 17th 2016 by ~20 people during a 5-day meeting at the 
OnionSpace in Berlin. It's a dynamic, fun process which is open to 
new people, influences and contributions. No need to tweet but
we have :ref:`contact channels` and :ref:`upcoming events`
where you may talk with us.


Current docs (work-in-progress)
-------------------------------

The following in-progress documents are written for software developers
and privacy enthusiasts.

:doc:`features`
     discusses how the Autocrypt efforts is different from past 
     e2e encryption efforts.

:doc:`Autocrypt key discovery <key-discovery>`
     discusses how mail programs negotiate encryption with each other.

:doc:`Autocrypt MUA internals <mua-internals>`
     discusses requirements, operations and the state MUAs need to
     keep in order to implement the Autocrypt protocols.

:doc:`ecosystem-dangers`
     some documented risks and dangers to the mail ecosystem,
     related to Autocrypt.


unsorted collection of docs and fragments
+++++++++++++++++++++++++++++++++++++++++++++++

The following docs need refinement and incorporation into
our sorted, maintained collection.

:doc:`Autocrypt levels <levels>`

:doc:`muaa-state` 

:doc:`multi-device`

:doc:`lockout`

:doc:`message-encryption`

:doc:`pgp-interop`

:doc:`user-experience`


.. _`contact channels`:

Channels
--------

If you want to help, including offering constructive criticism, 
you may:

- join the `autocrypt mailing list`_

- join chats at **#nextleap on freenode or matrix.org**.

- collaborate through PRs, issues and edits on our
  `github autocrypt repo <https://github.com/autocrypt/autocrypt>`_

.. _`autocrypt mailing list`: https://lists.mayfirst.org/mailman/listinfo/autocrypt


.. _`upcoming events`:

Upcoming events
----------------

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
