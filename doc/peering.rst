Multi-Device Pairing Considerations
===================================

.. _`sma`:

Shared MUAA Messaging Archive
------------------------------------

characteristics/requirements of of what SMAs need to provide:

- a SMA can be implemented on top of IMAP commands

- is used to synchronize states between MUAAs. We use "MUAAs" to
  indicate a particular MUA/Account combination because synchronization
  happens betweens accounts managed by different MUAs.

- is used to send and receive messages between MUAAs (concurrently),
  for example pairing requests, initial Autocrypt setup (of first MUAA),
  updates to received remote Autocrypt encryption keys.

- A MUAA needs to be able to detect if there is any other MUAA

- messages are not (necessarily) human readable and don't appear in the
  regular inbox.

- probably: size of SMA should not grow linearly with number of
  incoming/outgoing mails, for example messages that have been
  processed by a MUA must be deleted

- there should be a policy/expiry of messages for MUAAs which don't
  exist/are not alive anymore

- we only require from IMAP servers that they handle first level folders
  (subfolders are not necessary)

- there is a header in the messages stored in these folders, indicating
  that the message is an SMA message.

implementation on top of IMAP, pairing happy path
+++++++++++++++++++++++++++++++++++++++++++++++++

Let's suppose we have a first MUAA.  It doesn't find an ``_Autocrypt_SMA``
announcement folder so it will do the following:

- create a random new number "1" which we call MUAA-ID.

- create an ``_Autocrypt_SMA`` "announcements" folder and
  append some MUAA description message, most notably
  the MUAA-ID

- create an inbox folder ``_Autocrypt_SMA_1`` where other
  MUAAs will be able to send/drop messages.

If now another MUAA is added:

- create a random new number "27" as MUAA-ID.

- discover the ``_Autocrypt_SMA`` folder exists and read all
  of its messages, discover that there is an ``1`` MUAA

- create an inbox folder ``_Autocrypt_SMA_27`` where other
  MUAAs will be able to send/drop messages.

- append a new MUAA description message to ``_Autocrypt_SMA``

- append a pairing request message to the "1" inbox (``_Autocrypt_SMA_1``).

The MUAA "1" will then:

- discover "27" from the new message in the announcement folder ``_Autocrypt_SMA``

- read the pairing request message from its own ``_Autocrypt_SMA_1`` inbox

- process the pairing request and send a pairing accept message to "27" by appending
  it to the ``_Autocrypt_SMA_27`` folder.

- delete the pairing request message from its own ``_Autocrypt_SMA_1`` folder.

.. note::

    In this happy path example we are not prescribing the precise pairing procedure,
    merely give an example how bootstrapping into a multi-MUA setting works.
    It is unclear whether a centrally shared keyring as an IMAP folder is viable
    (synchronization between MUAs, "merge conflict" between state, deleting
    message might be a problem, encrypted "broadcast" to all my MUAAs)


.. todo::

    Critically consider how the multiple Autocrypt folders show in user interfaces.
    It might be better to depend on sub folders.

.. todo::

    Crically consider end-to-end encryption for MUAA messages.

.. todo::

    Consider how to force remove devices through IMAP folder deletion or something.

types of inter-MUAA unicast messages
------------------------------------
Difficult to reason about when we don't know what we *really* want to do
(cryptographic protocol wise)

ID announcement
+++++++++++++++

pairing messages
++++++++++++++++
- Some authenticated key exchange so later messages between MUAAs can be encrypted
- Shared private key so messages encrypted to the account's public key
  can be encrypted and outgoing mail can be signed

remote key updates
++++++++++++++++++
- notify other MUAAs that you add to or change an entry to your keyring



.. note::

    Why not use IMAP METADATA instead of specially-named folders?

    We ultimately want Autocrypt to be more generic than IMAP, to make it
    clear how other mail-checking protocols could work (e.g. MAPI, webmail
    interfaces) as long as they offer some sort of namespaced shared
    storage.  Using :rfc:`IMAP METADATA <5464>` would tie Autocrypt more
    tightly to IMAP, and would also limit the number of IMAP
    implementations that Autocrypt-enabled MUAs could connect to
    (METADATA is `not widely supported by today's IMAP server
    implementations <http://www.imapwiki.org/Specs>`_).

    If we wanted Autocrypt to use METADATA where it was available on the
    server, but allow for fallback to normal folders for IMAP servers that
    don't support METADATA, then we'd be adding an implementation
    requirement for MUAs that might not already know how to use the
    METADATA extension, which makes adoption harder.

    And without initially requiring it for MUAs, we don't see a way to
    transition once non-METADATA capable MUAs exist in the wild,
    either, since lockout and sync become difficult to do.  So we don't
    see a good story for METADATA deployment, sadly, despite it targeting
    our use case fairly neatly.

    See also `earlier discussion about IMAP METADATA
    <https://github.com/autocrypt/autocrypt/issues/12>`_.

