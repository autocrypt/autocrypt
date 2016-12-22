
Autocrypt features
--------------------------------

**If users ask how they can secure their e-mail the answer
should be as simple as: use an autocrypt-enabled mail app.**

End-to-end encrypted e-mail has been around for decades, but has failed
to see wide adoption outside of specialist communities, in large part
because of difficulties user experience and certification models.
To better understand how the fresh Autocrypt effort is different 
from previous ones here are some of its features:

- **Protect first against passive data-collecting adversaries**,
  resist the temptation to early-add complexity which aim to 
  prevent active attacks.  See `RFC7435 A New Perspective
  <https://tools.ietf.org/html/rfc7435#section-1.2>`_ for some
  motivation of this and the next points.
 
- **Focus on incremental deployment**, always consider that there
  will be both Autocrypt-enabled mail apps and traditional plain ones,
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

- **Implement and specify "Level 0" support in several mail apps in spring
  2017.** Keep Level 0 minimal enough that it's easy for developers to
  adopt it and we can start to drive efforts from real-life experiences.
  Please see :doc:`level0`.
  Currently involved are developers from `K9/Android`_, `Enigmail`_,
  `Mailpile`_, `Bitmask/LEAP`_ and others who are interested to add
  support for OSX or write reference "bots" in `Python`_ or `Go`_.

.. _`K9/Android`: https://k9mail.github.io/
.. _`Enigmail`: https://enigmail.net/
.. _`Mailpile`: https://mailpile.is/
.. _`Bitmask/LEAP`: https://leap.se/en/docs/client

.. _`Python`: https://www.python.org/
.. _`Go`: https://golang.org/
