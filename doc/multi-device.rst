Multi-device sharing with INBOME
================================

.. contents::

We expect users to have multiple devices connected to the same
account, because that's a common use case today.

To make this work as easily as possible, we need to have a way that a
user can use their existing configured device to bring another device
online in a reasonably-synchronized way.

There are two main approaches for this: Static State, and Device
Pairing.  In this discussion, we assume that the user has one e-mail
account, and uses two or more INBOME-aware MUAs to connect to that
e-mail account (for both sending and receiving mail).  We work under
the assumption that all used MUAs are INBOME-aware.

FIXME: think more clearly about the case where both devices have some
level of independent INBOME configuration.

Static State
------------

Static State is the simplest approach, but has some serious usability
and security drawbacks.  In this mechanism, one MUA generates a strong
"backup code" and gets the user to write it down somewhere.  Then it
serializes its secret key material into a message encrypted by the the
backup code.  This message is given a custom header and is sent to the
account in question::

    INBOME: backup;key_backup_data=<encrypted_secret_key>
    From: alice@example.net
    To: alice@example

An INBOME-aware MUA scans the incoming mail for a message with this
INBOME header and prompts the user for their backup code if it finds
it.

Note that this mechanism doesn't require both devices to be accessible
simultaneously.

Note also that the backup code MUST be strong -- it is subject to
brute force attacks by anyone who holds a copy.

Device Pairing
--------------

This mechanism requires both devices to be online in order to set up a
new device.

FIXME: complete description of DH handshake and per-device session
establishment.
