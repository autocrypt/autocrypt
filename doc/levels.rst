Levels of Support
=================

We want to enable working on INBOME for projects that currently cannot support ECC right now. Therefore we define levels of support for INBOME compatible agents.

Here's what we expect to be mandatory to implement at a certain level of support.

Level 0
-------

MUST generate: RSA 2048
MUST accept: RSA 2048
SHOULD accept: 25519

When receiving a key the uid MUST be treated as ornamental.
When sending an email the uid on the cert SHOULD match the 'to' field in the
header.

If you see more than one valid header you MUST drop them all.

Level 1
-------

MUST generate: 25519
MUST accept: RSA 2048, 25519

We are standardizing on eliptic curve crypto based on ed25519 for the primary key and cv25519 for the encryption-capable subkey.




Critical and non-critical attributes
------------------------------------

Attributes starting with _ are non critical and can be dropped if the agent does not understand them.
If the agent does not understand an attribute that does not start with _ it MUST ignore the header.
