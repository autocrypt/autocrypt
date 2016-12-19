
Known Open questions / notes 
-----------------------------

- Instead of transporting keysdata through Autocrypt headers we could
  also add attachments, e.g. application/pgp-keys ones and put Autocrypt
  headers into it.

- We don't currently address signatures at all -- how does Autocrypt
  interact with message signing?

- The actual encryption/signing mechanism are not defined by Autocrypt.
  For now we assume the practical implementation uses OpenPGP keys and
  either a separate or the default user's keyrings to store keys
  coming over Autocrypt.

- We can allow peers to gossip keys for all participating parties in an
  email conversation to speed up key discovery among them.  If a peer
  got two different keys for a target address (which can happen
  because of group gossiping and upgraded/regenerated keys) the peer
  shall encrypt to both keys if possible and request a key from the
  peer so that it can resolve the conflict.  FIXME: how are we
  encouraging key gossip in a group?

- We assume that an MUA only sends a key to a peer if the peer's last
  message indicated Autocrypt abilities/requests.  If a peer has sent a
  non Autocrypt mail, an MUA shall by default send a cleartext mail
  (unless explicitly requested by its user to continue sending
  encrypted).

- how does Autocrypt interact with today's mailing list managers?  This
  might not be relevant except for encrypted mailing lists.

- under what circumstances precisely do you downgrade from encryption
  to cleartext?  Could we consider the ``User-Agent`` header which
  often will indicate if the other side is using multiple
  devices/MUAs?  can we otherwise practically distinguish different
  MUAs from parsing messages/headers?  There's an ongoing push to drop
  User-Agent headers from most MUAs, in an attempt to minimize
  published metadata, so relying on User-Agent isn't a reasonable
  approach.  However, each MUA could select and publish a UUID as part
  of its Autocrypt header, if we find it's important for one peer to know
  when the other is using multiple clients.

- how to deal with spammers downgrade encryption by using a fake from?
  (it's not their intention, just a side effect).  How much can we
  rely on DKIM?
