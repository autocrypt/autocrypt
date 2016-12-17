
INBOME - in-band opportunistic mail encryption  (WIP)
-----------------------------------------------------

**STATUS of all docs here**: early stages, under discussion before and at the `AME2016 meetup in Berlin Dec 14-18th <https://github.com/mailencrypt/ame2016>`_

Email has been declared dead many times but refuses to die. It remains the largest open federated identity and messaging system, anchors the web and mobile phones and continues to relay sensitive information between citizens and organisations.  However, bringing pervasive end-to-end encryption to this infrastructure has failed so far. The INBOME effort aims to develop opportunistic mail encryption drafts and working code. To ease adoption, it restricts itself to only require changes from mail programs (MUAs) but no changes whatsoever from mail providers. It follows recommendations from RFC7435 "Opportunistic security" and specifically avoids talking to users about keys without them having asked for it first. **The overall goal of INBOME is to help massively increase the overall number of encrypted mails world wide**.  

Current work-in-progress specs:

:doc:`INBOME key discovery <mua-keydiscovery>` presents and discusses how mail programs negotiate encryption with each other. 

:doc:`INBOME key format <key-formats>` discusses the precise header and key format.

:doc:`INBOME levels <levels>` discusses level0 and level1 support.

:doc:`INBOME MUA internals <mua-internals>` discusses requirements, operations and the state MUAs need to keep in order to implement the INBOME protocols.

:doc:`INBOME multi-device management <multi-device>` discusses how to make several MUAs share secret key material, also involving questions of key backup. INBOME-supporting MUAs communicate via mail with each other in order to synchronize secrets.

.. 
    :doc:`INBOME reasons <reasons>` lists reasons and frequent questions. 

.. toctree::
   :hidden:

   mua-keydiscovery
   key-formats
   levels
   mua-internals
   multi-device
