Appendix
=========

.. _own_state:

``own_state``
--------------

.. code-block:: none

    own_state
        secret_key
        public_key
        prefer_encrypt

.. code-block:: none

    prefer_encrypt = {mutual, nopreference}

``peer_state``
--------------

.. code-block:: none

    autocrypt_peer_state
        last_seen
        last_seen_autocrypt
        public_key
        state

.. code-block:: none

    state = {nopreference, mutual, reset, gossip}

``certificate``
---------------

.. code-block:: none

    certificate
        Kp
        user id
        self signature
        Ke
        binding signature Ke by Kp

``recommendation``
-------------------

.. code-block:: none

    recommendation =
