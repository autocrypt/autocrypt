
Autocrypt features
--------------------------------

End-to-end encrypted e-mail has been around for decades, but has failed
to see wide adoption outside of specialist communities, in large part
because of difficulties with user experience and certification models.
To better understand how the Autocrypt effort is different
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
  usability-test what needs to be decided by users and include
  resulting UI guidance in the specs.  Minimize friction for people
  using multiple mail apps with their accounts.

- **Go for mail app changes only**, don't require changes from mail
  providers or depend on third party services, allowing fluid development
  of deployable code and specs.

- **Use decentralized, in-band key discovery.**  Make mail apps
  tell each other how and when to encrypt to each other
  by attaching necessary information along with mails.

- **Implement and specify "Level 0" support in several mail apps in spring
  2017.** Keep Level 0 minimal enough that it's easy for developers to
  adopt it and we can start to drive efforts from real-life experiences.
  Please see :doc:`level0`.
