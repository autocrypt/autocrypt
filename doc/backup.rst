Autocrypt Secret Key Backup
===========================

This is for Autocrypt Level 1 or later...

The MUA generates a strong "backup code" and gets the user to write it
down somewhere.  Then it serializes its secret key material into a
message encrypted by the the backup code.  This message is given a
custom header and is sent to the account in question::

    Autocrypt-Secret-Key-Backup: key_backup_data=<encrypted_secret_key>
    From: alice@example.net
    To: alice@example.net

.. todo::

   should the MUA store the message in the SMA, or store it to file or
   what?


Restore
-------

.. todo::

   Fill in here
   
Prompting the user for backup code?

Note also that the backup code MUST be strong -- it is subject to
brute force attacks by anyone who holds a copy.

Backup and Sync
---------------


.. todo::

   say something about the relationship between backup and sync
