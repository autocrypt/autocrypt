Appendix
=========

.. _own_state:

``own_state``
--------------

.. code-block:: none

    own_state:
        - secret_key     =
        - public_key     =
        - prefer_encrypt = {mutual, nopreference}

.. _peer_state:

``peer_state``
--------------

.. code-block:: none

    autocrypt_peer_state:
        - peer e-mail address:
            - last_seen           = <UTC timestamp>
            - last_seen_autocrypt = <UTC timestamp>
            - public_key          =
            - state               = {nopreference, mutual, reset, gossip}

.. _certificate:

certificate packets

---------------------
.. code-block:: none

    certificate packets (binary base64 encoded)
        Kp
        user id                     = <e-mail address>
        self signature
        Ke
        binding signature Ke by Kp

.. _recommendation:

``recommendation``
-------------------

.. code-block:: none

    recommendation = {disable, discourage, available, encrypt}

.. _autocrypt_headers:

Autocrypt headers
------------------
::

    Autocrypt: addr=<From e-mail address>; [prefer-encrypt=mutual;] keydata=<BASE64 encoded From's public key>

::

    Autocrypt-Gossip: addr=<To e-mail address>; [prefer-encrypt=mutual;] keydata=<BASE64 encoded To's public key>
    ...
    Autocrypt-Gossip: addr=<CC e-mail address>; [prefer-encrypt=mutual;] keydata=<BASE64 encoded CC's public key>
    ...

::

    Autocrypt-Prefer-Encrypt: {mutual, }

::

    Autocrypt-Setup-Message: v1


Autocrypt ``content-type`` s
-------------------------------
::

    application/autocrypt-key-backup

Pseudocode to update Autocrypt Peer State
------------------------------------------
::

    if Header.Autocrypt == NULL and Header.Date > autocrypt_peer_state.last_seen:
        autocrypt_peer_state.last_seen = Header.Date
        autocrypt_peer_state.state = reset

Pseudocode to generate single recipient recommendation
-------------------------------------------------------

Pseudocode to generate multiple recipient recommendation
---------------------------------------------------------

Autocrypt Setup Message
-------------------------
::

    To: <To e-mail address>
    From: <From e-mail address>
    Autcrypt-Setup-Message: v1
    Content-type: multipart/mixed
