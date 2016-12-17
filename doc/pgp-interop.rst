should inbome keys appear on key servers?

- no!

should i add rcvd inbome keys into my pgp keyring? (if my mua supports pgp)

- yes

should my own inbome keys appear in my keyring?

- no

can I put my regular pgp keys into inbome?

- MUAs should not provide UI for importing keys for level1
- allowed for level0 to get traction early on (as replacement for keyservers)

can I use someone's pgp key that i have for encrypting mail to that person?

- This would work like without inbome

if i have for a person an non-inbome pgp key and an inbome key, which one do
i use to encrypt mails for that person?

- Look up email address in pgp keyring
- if there is a key that has better trust than unknown, use that one
- else look up a key from the inbome state (which is also in the keyring)

two target audiences:

- end-users
- mail software devs
