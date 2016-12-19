Message Encryption by INBOME-capable agents
===========================================

When a message is sent encrypted by an INBOME-capable agent, there are
several details the agent should be aware of when structuring the
encrypted message itself.  This document details guidance on
construction of encrypted messages.

If the sending user has disabled INBOME entirely, then the agent
should probably not be sending encrypted messages.

Always "encrypt-to-self"
------------------------

The INBOME-capable client SHOULD always encrypt the message to the
sender's public key (the key specified in the outbound INBOME header)
in addition to the recipients' public keys.

This is so that the sender can read any mail stored in their outbox or
"Sent" folder, as the user has come to expect.

Mask Key IDs of Bcc'ed recipients
---------------------------------

If any recipients are in `Bcc:` (rather than `To:` or `Cc:`), and the
key types used are all OpenPGP (`type=p`), then the agent SHOULD mask
the recipient key ID in the generated PKESK packets that correspond to
the Bcc'ed recipents.  It does not need to mask recipient key IDs of
normal recipients.

Masking of Key IDs is done by setting the key ID to all-zeros.  See
the end of section 5.1 RFC 4880 for more details.  Users of GnuPG can
use the `--hidden-recipient` argument to indicate a recipient who will
be masked.

This is so that the message encryption does not leak much additional
metadata beyond what is already found in the headers of the message.
It still leaks the number of additional recipients, but the additional
work and usability issues involved with fixing that metadata leak
suggest that it's better to leave that to a future level.

NOTE: interaction with encrypted headers: if something like memoryhole
ever makes it possible to hide normal `To:` and `Cc:` headers, then we
need to rethink our approach to handling PKESK leakage further.

