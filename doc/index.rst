Autocrypt - E-mail Encryption for Everyone
==========================================

**STATUS of all docs here**:
 needs full review after after many changes and flesh outs 
 which happened during the "automatic mail 
 encryption" unconference in Berlin Dec 14-18th <https://github.com/mailencrypt/ame2016>`_

Autocrypt is a project to opportunistically replace cleartext mail
with encrypted mail as much as humanly possible.
 

Current work-in-progress specs:

:doc:`Autocrypt key discovery <mua-keydiscovery>`
     presents and discusses how mail programs negotiate encryption
     with each other.

:doc:`Autocrypt key format <key-formats>`
     discusses the precise header and key format.

:doc:`Autocrypt levels <levels>`
     discusses level0 and level1 support.

:doc:`Autocrypt MUA internals <mua-internals>`
     discusses requirements, operations and the state MUAs need to
     keep in order to implement the Autocrypt protocols.

:doc:`Autocrypt multi-device management <multi-device>`
     discusses how to make several MUAs share secret key material,
     also involving questions of key backup. Autocrypt-supporting MUAs
     communicate via mail with each other in order to synchronize
     secrets.

.. 
    :doc:`Autocrypt reasons <reasons>` lists reasons and frequent questions. 

.. toctree::
   :hidden:

   mua-keydiscovery
   key-formats
   levels
   mua-internals
   multi-device
