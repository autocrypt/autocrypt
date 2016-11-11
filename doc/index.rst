
INBOME - in-band opportunistic mail encryption  (WIP)
-----------------------------------------------------

**STATUS of all docs here**: early stages, under discussion before and at the `AME2016 meetup in Berlin Dec 14-18th <https://github.com/mailencrypt/ame2016>`_

Email has been declared dead many times but refuses to die. It remains the largest open federated identity and messaging system, anchors the web and mobile phones and continues to relay sensitive information between citizens and organisations.  However, bringing pervasive end-to-end encryption to this infrastructure has failed so far. The INBOME effort aims to develop opportunistic mail encryption drafts and working code. To ease adoption, it restricts itself to only require changes from mail programs (MUAs) but no changes whatsoever from mail providers. It follows recommendations from RFC7435 "Opportunistic security" and specifically avoids talking to users about keys without them having asked for it first. **The overall goal of INBOME is to help massively increase the overall number of encrypted mails world wide**.  

Current work-in-progress specs:

:doc:`INBOME key discovery <mua-keydiscovery>` outlines and prototypes how mail programs negotiate encryption with each other. Similar to TLS's machine to machine handshake, users first have a cleartext mail exchange where their mail programs automatically attach crypto protocol and key information. Subsequent mails will then be encrypted. Mail programs signal encryption-status at "compose-mail" time and otherwise avoid asking for decisions about keys. Passive eavesdroppers will not be able to continue reading mail content. INBOME key discovery requires changes only in mail programs and works with any existing provider, it works fully offline and is only based on the two core abilities every mail program has: sending and receiving mail.

:doc:`INBOME multi-device management <multi-device>` discusses how to make several MUAs share secret key material, also involving questions of key backup. INBOME-supporting MUAs communicate via mail with each other in order to synchronize secrets.

:doc:`INBOME MUA state <mua-state>` discusses the state MUAs need to keep in order to implement the INBOME protocols.

:doc:`INBOME MUA requirements <mua-requirements>` lists what facilities MUAs must offer.


.. toctree::
   :hidden:

   mua-keydiscovery
   multi-device
   mua-state
   mua-requirements
