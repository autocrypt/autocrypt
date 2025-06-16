OpenPGP data in vCard contacts
------------------------------

Format of OpenPGP key-value pairs in vCard
++++++++++++++++++++++++++++++++++++++++++

A vCard which holds OpenPGP data
is expected to be at least version 4.0
according to `RFC 6350 <https://www.rfc-editor.org/rfc/rfc6350>`_.

On a user manually importing a vCard,
MUAs MAY process it
to update the Autocrypt Peer State for the contact.
If the MUA manages encryption recommendations differently
than with the Autocrypt Peer State,
it can anyway make sense to consider this specification
to judge the trust which rests in OpenPGP data
imported from a vCard.

MUAs SHOULD NOT import OpenPGP data
for more than one contact from one .vcf file,
unless they show the user each contact's information individually
and let them approve it.

The following vCard properties are relevant
for updating the Autocrypt Peer State:

* ``EMAIL``, optionally with a ``PREF=1`` parameter (or higher)
* ``KEY``, optionally with a ``PREF=1`` parameter (or higher)
  * The value MUST be a data URL
    with the "application/pgp-keys" MIME type
    and using base64 encoding.
  * The comma in the data URL SHOULD be escaped.
    But implementations MUST parse both escaped and unescaped commas correctly,
    because Section 3.4 and the last example in Section 6.8.1 of RFC 6350
    contradict each other, and both versions exist in the wild.
* ``AUTOCRYPT-PREFER-ENCRYPT``

The update process follows these steps:

1. If an ``EMAIL`` property is present,
   the corresponding ``peers[from-addr]`` entry is updated
   in the Autocrypt Peer State.
   Otherwise the OpenPGP data in the vCard SHOULD be discarded.

2. If more than one ``EMAIL`` property is present,
   they need to be prefixed with ``ITEM1`` (or higher).
   All other properties considered by this spec
   MUST clearly refer to one of them
   by having the same ``ITEMn`` prefix,
   or they will be discarded on import.
   If ``EMAIL`` properties have a ``PREF=n`` parameter,
   MUAs MAY import only the one with the lowest number.

3. MUAs MUST NOT update the Autocrypt Peer State
   if no ``KEY`` property is present in the vCard.

4. If a ``KEY`` property is present,
   set ``peers[from-addr].gossip_key``
   to the value of the vCard's property.
   If more than one ``KEY`` property
   refers to the email address,
   MUAs SHOULD use only the one with the lowest number for encryption.
   MUAs MAY import ``KEY`` propertys with higher numbers
   for the purpose of verifying signatures of old messages.

5. If ``peers[from-address].prefer_encrypt`` is not present,
   but an ``AUTOCRYPT-PREFER-ENCRYPT`` property is present,
   MUAs SHOULD set ``peers[from-address].prefer_encrypt``
   to the value of the vCard's property.
   Otherwise, they should set it to ``nopreference``.


Example vCards with OpenPGP data added to it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To update the Autocrypt Peer State, a vCard needs to contain at minimum:

.. code-block:: vCard

  BEGIN:VCARD
  VERSION:4.0
  FN:Dr. Alice Wise
  EMAIL:alice@protonmail.com
  KEY:data:application/pgp-keys;base64\,xlIEXd6t...ZFn/d2WPx4mOoF2ww0=
  END:VCARD


This is an example of having two keys per contact.
Only the first key should be used for encrypting though,
the second key is only for verifying signatures from old messages:

.. code-block:: vCard

  BEGIN:VCARD
  VERSION:4.0
  FN:Dr. Alice Wise
  EMAIL:alice@protonmail.com
  KEY;PREF=1:data:application/pgp-keys;base64,uiOsGaKn...OWeSlq12lc8LsER1E3=
  KEY;PREF=2:data:application/pgp-keys;base64,xlIEXd6t...ZFn/d2WPx4mOoF2ww0=
  AUTOCRYPT-PREFER-ENCRYPT:mutual
  END:VCARD


In Protonmail, a contact can have multiple email addresses,
which each can have multiple keys:

.. code-block:: vCard

  BEGIN:VCARD
  VERSION:4.0
  FN;PREF=1:Dr. Alice Wise
  N:Wise;Alice;;Dr.;
  UID:example-b7331409-58ce-a207-c978-4bf29585545b
  ITEM1.EMAIL;PREF=1:alice@protonmail.com
  ITEM1.KEY;PREF=1:data:application/pgp-keys;base64,xlIEXd6t...ZFn/d2WPx4mOoF2ww0=
  ITEM1.KEY;PREF=2:data:application/pgp-keys;base64,uiOsGaKn...OWeSlq12lc8LsER1E3=
  ITEM2.EMAIL;PREF=2:alice@nsa.gov
  ITEM2.KEY;PREF=1:data:application/pgp-keys;base64,iaudHUSH...IASDNAJSDNI/97adsd=
  ITEM2.KEY;PREF=2:data:application/pgp-keys;base64,98udsiUS...a8sdZSd/3SDT76sd6G=
  END:VCARD

