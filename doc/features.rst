
Autocrypt features
==================

End-to-end encrypted e-mail has been around for decades, but has failed
to see wide adoption outside of specialist communities, in large part
because of difficulties with user experience and certification models.
To better understand how the Autocrypt effort is different
from previous ones here are some of its features:

- **Protect first against passive data-collecting adversaries**,
  resist the temptation to early-add complexity which aim to prevent
  active attacks.  See :rfc:`RFC7435 A New Perspective
  <7435#section-1.2>` for some motivation of this and the next points.

- **Focus on incremental deployment**, always consider that there
  will be both Autocrypt-enabled mail apps and traditional plain ones,
  interacting with each other.

- **Don't ask users anything about keys, ever.** Minimize and
  usability-test what needs to be decided by users and include
  resulting UI guidance in the specs. Minimize friction for people
  using multiple mail apps with their accounts.

- **Go for mail app changes only**, don't require changes from mail
  providers or don't depend on third party services, allowing fluid
  development of deployable code and specs. Ensure mail implementors
  can actually implement and influence the spec.

- **Use decentralized, in-band key discovery.**  Make mail apps
  tell each other how and when to encrypt to each other. Send this
  information in a way that is hidden from users of non-autocrypt mail
  clients to avoid confusing them.
