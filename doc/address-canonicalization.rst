E-mail Address canonicalization
===============================

Domain part (the part after the ``@``):

.. todo::

   We need to choose a canonicalization form for the domain side of
   the e-mail address.  There are risks for user presentation around
   phishing with IDNs, which we should be careful about.

Local part (the part before the ``@``):

SMTP specs say this part is domain-specific, and byte-for-byte
arbitrarily sensitive.  In practice, nearly every e-mail domain treats
the local part of the address as a case-insensitive string.  That is,
while it is permitted by the standards, ``John@example.org`` is very
unlikely to deliver to a different mailbox than ``john@example.org``.
Autocrypt-aware MUAs will canonicalize the local part of an e-mail
address by making it all lower-case.

.. todo::

   some people (and some e-mail domains) have known variations which
   all deliver to the same account.  For example, the mailbox that
   receives ``john@example.org`` might automatically receive all mail
   addressed like ``john-whatever@example.org``.  gmail today supports
   arbitrary dot injection (e.g. ``johndoe@example.org`` delivers to
   the same mailbox as ``john.doe@example.org``).  Do we want to try
   to support these somehow?  It would be simplest to declare anyone
   using aliasing schemes like this as out-of-scope for Autocryptv1.

.. todo::

   do we want to allow sophisticated users to explicitly merge known
   shared aliases as long as the domain side stays the same?  For
   example, if i happen to know that ``jdoe@example.org`` delivers to
   the same mailbox as ``john@example.org``, can i declare that to an
   Autocrypt-aware MUA?  How would such an explicit merge affect state
   management?
