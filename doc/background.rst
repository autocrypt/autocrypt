Background
==================================================

.. contents::

Motivation
----------

**If users ask how they can secure their e-mail the answer
should be as simple as: use an Autocrypt-enabled mail app!**

**Why improve e-mail?** E-Mail has been declared dead many times but
refuses to die. It remains the largest open federated identity and
messaging ecosystem, anchors the web and mobile phones. E-Mail continues to relay
sensitive information between people and organisations. It has
problems but do you prefer the proprietary, easy-to-track mobile phone
number system to become the single source of digital identification?

**Why a new approach to e-mail encryption?**  Encrypted e-mail has been
around for decades, but has failed to see wide adoption outside of
specialist communities, in large part because of difficulties with user
experience and certification models.  Autocrypt first aims to provide
convenient encryption that is neither perfect nor as secure as
traditional e-mail encryption, but is convenient enough for
much wider adoption.

The Social Autocrypt Approach
------------------------------

The Autocrypt project is driven by a diverse group of mail app developers,
hackers and researchers who are willing to take fresh approaches, learn from
past mistakes, and collectively aim to increase the overall encryption
of E-Mail in the net.  The group effort was born and named "Autocrypt"
on December 17th 2016 by ~20 people during a 5-day meeting at the
OnionSpace in Berlin. Follow up meetings took place in March 2017 around the
Internet Freedom festival and during a subsequent gathering in Freiburg, Germany.
It remains a dynamic, fun process which is open to new people, influences and
contributions.  See :doc:`contact channels and upcoming events <contact>` on
how you may talk with us and who "we" are currently.


The Technical Autocrypt Approach
--------------------------------------

Autocrypt uses regular E-Mail messages between people to piggyback
necessary information to allow encrypting subsequent messages; it adds
a new :mailheader:`Autocrypt` E-Mail header for transferring public
keys and driving encryption behaviour. By default, key management is
not visible to users. See :doc:`features` for more technical and UI
cornerstones.

We are following this approach step-by-step using different "Levels"
of implementation compliance.  Driven by usability concerns, we are
refining and implementing :doc:`Level 1 <level1>` in several mail apps
during summer 2017, aiming for a release party during autumn 2017 which
marks the first `real-life implementation milestone <https://github.com/autocrypt/autocrypt/milestone/1>`_.
If you are interested to learn more or want to help please :doc:`join our channels and look at
where we meet next <contact>`.

See :doc:`contents` for an index of all docs and discussion results so far.


Design Differences To Previous Approaches
-----------------------------------------

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
