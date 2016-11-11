MUA requirements
=================



INBOME works for people who use INBOME-aware MUAs.  We expect the MUAs
to have the following capabilities:

- know what account(s) they are associated with, including the
  public-facing e-mail address associated with each account.

- be able to fetch e-mail from the corresponding accounts

- send e-mail to arbitrary e-mail addresses (including its own
  account(s)).

- If the MUA can check multiple e-mail accounts, it should be able to
  distinguish somehow between mail delivered to each of those
  accounts.  That is, if the MUA checks the mailbox for
  ``bob@home.example`` and also for ``robert@work.example``, it should
  know which messages came for which address.  (Inspecting headers may
  be sufficient for this).  This is necessary because some messages
  that affect the state of an INBOME peering don't bear INBOME headers
  at all (e.g. messages from new, non-INBOME-capable MUAs)

- be able to store persistent state about the user's communications
  partners (see mua-state.rst) and about the user's other devices (see
  multi-device.rst)
