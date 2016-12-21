

Interoperability with existing PGP practises
-------------------------------------------------

should Autocrypt keys appear on key servers?

- no!

should i add rcvd Autocrypt keys into my PGP keyring? (if my mua already supports PGP)

- yes

should my own Autocrypt keys appear in my keyring?

- no
  (why not?  how else can we do encrypt-to-self, or message signing?)

can I put my regular pgp keys into Autocrypt?

- MUAs should not provide UI for importing keys for Level 1
- allowed for Level 0 to get traction early on (as replacement for keyservers)

can I use someone's pgp key that i have for encrypting mail to that person?

- This would work like without Autocrypt

if i have for a person an non-Autocrypt pgp key and an Autocrypt key, which one do
i use to encrypt mails for that person?

- Look up email address in pgp keyring
- if there is a key that has better user ID validity for the matching address than "unknown", use that one
- else look up a key from the Autocrypt state (which is also in the keyring)

two target audiences:

- end-users
- mail software devs
