Why are you using headers rather than attached keys?

Attachments are visible to users of non INBOME compatible MUAs.


Why are you sending keys in all the mails and not just announcing capabilities?

We used to do this. We decided against it because it requires the MUA to keep
the information who announced INBOME and who they requested keys from.


Why are we using IMAP folders rather than self send messages for multi device?

Self send messages end up in your inbox and might be confusing to users. They
are likely also processed by your spam protection and might look like spam.


Why are you using ed25519 - it's not supported by X?

They give us much smaller keys that lead to smaller headers and make it easier
to include them. You can even write them down as a backup code.
We want to support implementation where needed.
