should inbome keys appear on key servers?

- no!

should i add rcvd inbome keys into my pgp keyring? (if my mua supports pgp)

- unclear:

  - in the long run we want to have seperate keyrings

    - the keyring is *explicit* key management
    - inbome is the exact opposite
    - prevents accidental upload of keys to keyservers

  - for moving fast we could have a lvl0 client that just puts all inbome
      keys into the existing pgp keyring
  - problem with that is when migrating lvl1 it would prefer the existing pgp
      keys from the keyring but those are in fact old inbome keys. x(

should my own inbome keys appear in my keyring?

- no

can I put my regular pgp keys into inbome?

- MUAs should not provide UI for importing keys for level1
- allowed for level0 to get traction early on (as replacement for keyservers)

can I use someone's pgp key that i have for encrypting mail to that person?

- This would work like without inbome
- yes, it even takes precedence!

if i have an non-inbome pgp key and an inbome key, which one do i use to
encrypt mails for that person?

- If there is a usable traditional pgp key according to current heuristics
  use that.
- If all traditional pgp keys are unusable (expired) the MUA MUST still alert
  the user about it even when an INBOME key is available.
  We want to ensure INBOME does not weaken traditional pgp usage.

two target audiences:

- end-users
- mail software devs
