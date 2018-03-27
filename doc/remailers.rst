Autocrypt and Mailing Lists
====

General Considerations
----

"Mailing lists" are a special use case of e-mail, where some address is managed
not as an inbox that stores e-mail for retrieval, but instead forwards all
messages to a configurable list of subscribers. For the case of end-to-end
encryption, the introduction of a relaying agent brings up the question of what
constitutes an "Endpoint".

For users with a typical intuition of end-to-end encryption, the expected end
points of end-to-end encrypted mailing lists will likely be the individual
subscribers. This is very difficult to achieve on top of existing e-mail
infrastructure, since it requires either negotiation between all endpoints, or
use of experimental encryption techniques such as homomorphic or attribute-based
encryption.

A compromise solution is to encrypt from the sender only to the remailer, which
then decrypts the message and individually encrypts to all subscribers. This
method violates strict end-to-end confidentiality, since the remailer can access
to the forwarded plaintext. However, the remailer will only need to handle
sensitive data transiently, which means messages are secure as long as the
remailer is honest at the time of sending.

This document focuses on seamless support for re-encryption based end-to-end
security in existing remailers, in keeping with the more general Autocrypt
approach.

Autocrypt-enabled Remailer
----

An Autocrypt-enabled remailer maintains an Autocrypt key of its own. During
regular operation, it collects Autocrypt-headers of all list participants via
incoming mail, to keep track of their keys. Then, depending on the availability
of encryption keys for participants, the remailer injects its own
Autocrypt-headers into outgoing mail to signal availability of encryption.

More specifically, an Autocrypt-enabled mailing list adds three behaviors to its
remailing logic:

1) For all incoming messages, keep track of Autocrypt-headers. This mechanism is
   the same that is used by clients, and requires no modifications.
2) Inject an Autocrypt-header into outgoing messages. This header serves the
   same purpose as usual, but adds some details for the mailing list use case.
   The header might only be injected under certain conditions, e.g. if
   encryption keys are available for a certain number of subscribers.
3) When receiving an encrypted message, decrypt it and re-encrypt for individual
   delivery to each Autocrypt-enabled subscriber. Subscribers for whom no keys
   are available do not receive the message, but optionally a notification of
   this circumstance (see below).

The presented mechanism works well for relatively small groups of mostly active
and Autocrypt-enabled subscribers, but becomes increasingly ineffective with
larger numbers of passive or non Autocrypt-enabled subscribers. As with any
encrypted group communication, the benefits of end-to-end encryption also dilute
with larger numbers of recipients.

For compatibility with clients that are not Autocrypt-capable, the remailer
software might want to offer manual configuration of keys, e.g. via a web
interface.

Injecting Reamiler Autocrypt-Headers
~~~~~

To inform subscribers of its key, the remailer injects an Autocrypt-header into
outgoing messages. The header format is the same as usual, where the ``addr``
attribute is the address of the list, and ``keydata`` is the list's Autocrypt
key.

In addition to those two attributes, the remailer SHOULD add the
``_list-recommendation`` attribute, and MAY add ``_list-recipients`` attribute.
Both of these attributes are exclusive for use by remailers, and MUST NOT be
used by regular mailbox addresses. Both of these attributes are non-critical
(starting with an underscore), which will cause an Autocrypt-capable client that
does not handle these attributes to skip over them, falling back to the usual
Autocrypt behavior.

Example of Autocrypt header for remailer with opt-in encryption::

    Autocrypt: addr=post@list.example; _list-recommendation=available; _list-recipients=7/15; keydata=XXX

Example of Autocrypt header for remailer with mandatory encrypytion::

    Autocrypt: addr=post@list.example; _list-recommendation=mandatory; keydata=XXX

The ``_list-recommendation`` attribute SHOULD be included in an Autocrypt header
sent by a remailer. Its value may be either ``available`` or ``mandatory``. If
the value is set to ``mandatory``, the remailer requires encryption of every
message, and will reject plaintext messages. If the value is ``available``,
encryption is offered as an opt-in mechanism and plaintext messages will be
handled as usual. In either case, encrypted messages will be delivered
exclusively to subscribers for whom an encryption key is available.

To inform the decision of whether to encrypt or not, the remailer MAY include a
``_list-recipients`` attribute. This attribute contains the current number of
subscribers for which an encryption key is available, and the total number of
subscribers, separated by a slash character ('/'). This attribute is only useful
if the ``_list-recommendation`` attribute is set to ``available``.

Administrative Considerations
----

Graceful Up- and Downgrade
~~~

To allow graceful up- and downgrade of lists with no intervention by the list
administrator, a remailer software distribution could automatically include
Autocrypt-headers with outgoing mail depending on the number of
Autocrypt-enabled subscribers. For example, a remailer software distribution may
choose to inject Autocrypt headers only if encryption keys are available for a
majority of subscribers. Note that obviously, end-to-end encryption is
unsuitable for lists that are publicly archived.

Missed Message Notifications
~~~

A remailer MAY send notifications to recipients that were unable to receive an
encrypted message, if their key was unavailable or unusable for some reason. If
available, a digest mechanism can be used to aggregate this information and
avoid redundant notifications.

Limiting Plaintext Exposure
~~~

An honest remailer SHOULD limit exposure to the plaintext data by re-using the
session key of the original message and re-encrypting it directly, to avoid
having the actual plaintext in memory at any time.
