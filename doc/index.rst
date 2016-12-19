Autocrypt - E-mail Encryption for Everyone
==========================================

**STATUS of all docs here**:
 early stages, under discussion before and during the `AME2016 meetup
 in Berlin Dec 14-18th <https://github.com/mailencrypt/ame2016>`_

Autocrypt is a project to opportunistically replace cleartext mail
with encrypted mail in as many places as possible.
 
Email has been declared dead many times but refuses to die. It remains
the largest open federated identity and messaging system, anchors the
web and mobile phones and continues to relay sensitive information
between citizens and organisations.  However, bringing pervasive
end-to-end encryption to this infrastructure has failed so far.

The Autocrypt effort aims to develop opportunistic mail encryption
drafts and working code that normal people can use a minimum of
interruption to their everyday e-mail workflow. To ease adoption, it
restricts itself to only require changes from mail programs (MUAs) but
no changes whatsoever from mail providers.

Autocrypt follows recommendations from RFC7435 "Opportunistic
security" and specifically avoids talking to users about keys without
them having asked for it first. **The overall goal of Autocrypt is to
help massively increase the overall number of encrypted mails world
wide**.

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
