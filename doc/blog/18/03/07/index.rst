Autocrypt: how Decentralization and Free Software can improve Encrypted Communication
=====================================================================================

`Since Snowden made us aware of every day mass surveillance, there is still too much unencrypted communication. What does encrypted communication for humans need?`

Communication is an ecosystem. Different species coexist peacefully and not-so-peacefully, plants need to be watered every day, progress happens. And sometimes, a new innovation bring a new species along; in this case, messengers.

The flow of creativity only starts here - hundreds of different messengers with different features have evolved of this. Audio messages and end-to-end encryption, timed messages and profile pictures, group chats and QR-code fingerprint verification; many interesting developments came out of messengers.

At the same time, people still send faxes, and all of those means of communication coexist. Because even though messengers have been a revolution to communication, they have many disadvantages and problems.

Most messengers put little value on history, it's hard to separate your private and business communication, and they have been a battlefield of influence for big players like Facebook or Google. All widely used messengers at this point are centralized solutions with no federation, commonly referred to as "silos". This allows great control of the platform and rapid development - but lacks the network effects to truly reach everyone. There is not a single messenger out there which all of my friends use.

When I really want to reach anyone, I still default to E-Mail. And why not? E-Mail is the only actually universal platform. It's federated, and not dependent on a single company, it relies on open standards. And of course, everyone has E-Mail. But there is no innovation in the field, the E-Mail ecosystem moves at glacial pace.

Of course we need progress, but legacy is important. If the progress can't deliver, people will fall back to the legacy options they have, E-Mail, and even faxes. Another lesson is that even a perfectly secure technology can't protect anyone, if it doesn't have users. If you are the only user of a perfectly safe messenger, you can't write confidential messages to anyone. And in the end, culture votes with its feet. Maybe one day people will walk away from E-Mail, maybe messengers will die out. Nobody can stop them.

When we both joined the Autocrypt project, we wanted to decrease the amount of unencrypted Internet traffic. The working title was "Encrypted E-Mail for Humans". Maybe humanity needs more than encrypted communication; but it‘s one of the first steps too many other problems.

Even five years after Snowden there is no easy default way to write securely with whoever they want to (No, Whatsapp doesn't count as secure). Right now, the masses can’t protect themselves from the Internet. Messengers didn't solve this problem.

If you look at all the different messengers and encryption tools, they all have one of three problems. Either they are too complicated to use (PGP), centralized and proprietary (Whatsapp, Threema), or they lack the network effects (Signal, Wire, XMPP, Tox, Briar, ....). Autocrypt chose to improve PGP in terms of ease-of-use, compatibility and user friendliness. Of the three problems, it seemed to be the easiest to fix.

The Autocrypt effort is driven by a diverse group of mail app developers, hackers and researchers who collectively aim to increase the overall end-to-end encryption of E-Mail in the net. Autocrypt is a specification for mail apps. It automates key management and key distribution, so users don't have to do it. Many mail apps implement the Autocrypt standard to allow their users to easily encrypt E-Mails.

The basic concept of Autocrypt is fairly easy. In short: Autocrypt uses regular E-Mail messages between people to piggyback necessary information to allow encrypting subsequent messages; it adds a new Autocrypt E-Mail header for transferring public OpenPGP keys and driving encryption behavior. By default, key management is not visible to users. You can encrypt group conversations by sending the keys of everyone to everyone. And you can setup another device for the same key by sending an E-Mail with the private key to yourself. That's it, the specification is only 12 pages long.

Autocrypt chose the E-Mail network for our new encryption specification. E-Mail is decentralized, widespread, and just won't die. Its network effects are useful, its longevity is ironic, but its decentralization is essential to our goals.



A Different Approach on E-Mails
-------------------------------

Most messengers are not only centralized systems, they also use your phone number to identify you. Managing people's identity over a phone number is ethically difficult though, it takes the control over their identity away from them. The phone number system is proprietary and easy to track. E-Mail as an identity provider is better, because it relies on open standards. Everyone can provide E-Mail, and doesn't have to trust one of the few monopolistic telephone providers. But that's not the only advantage of decentralization.

In the world of platforms, it's not a given that you can reach everyone. While we are used to maneuver within and between platforms, any communication happens on some platform. And the communication providers have power, and usually monopolies.

A centralized platform is a gilded cage. It gives users possibilities, but also erodes their sovereignty. If you want to stay in touch with the others in the platform, you can't leave - even if you know that your data is used against you and that there is another platform which suits you better, but has no users. In decentralized systems, you can at least vote with your feet. You can leave a central hub and move to another, if you don't like it - but if the hubs federate, you can still stay in touch. And if there is no hub you like, go on and host your own. Maybe others with less technical capabilities are only waiting for someone like you.

That's why Autocrypt chose the E-Mail network as a platform. There is Gmail as a provider which reads your mail to sell you stuff, but you can still write to Gmail users from an address at a more privacy-respecting E-Mail provider. This enables you to reach anyone, by still preserving your sovereignty.

One of the specific approaches by Autocrypt is the focus on mail app implementation. To use Autocrypt, you don't require your E-Mail Provider to do anything. Instead, with Autocrypt several mail app developers work closely together. This allows for fluid development, and also the adjustment of the specification.

This form of incremental improvement and deployment is very natural for a simple reason: there will always be cleartext E-Mails in the same system as encrypted E-Mails. Encryption shouldn't get into the way of its users; and if we don't want to break existing workflows, we have to take care of backwards compability and legacy support.


How to Bring Encryption to the Many
-----------------------------------

There are reasons why encryption has not been widely adopted yet, despite the threats to everyone's privacy. For many users, it has never been convenient enough to encrypt E-Mails. PGP is a very complex tool, which can be used for various purposes. Encrypted Communication is just one of them, software signing, document signature validity, or online authentication are others.

To fulfill all those use cases, users have indeed to know which keys they are using, trusting, and what exactly they are doing. What the difference between a public and a private key is. What signatures have to do with encryption. But do they have to know that if they only want encrypted communication? If you had to think about security before each message you send - would you still want to message securely?

Because of these issues, one thing was clear, when Autocrypt was born: Autocrypt users should not have to know that they are using keys when they write encrypted. If everyone you write to receives your public key, you don't have to know how to provide public keys. If you can setup new devices with a simple procedure, you don't have to know what a private key is.

`to do:`

Bringing together decentralization/user autonomy and ease of use

Key discovery should be hidden from users, but still decentralized. To remain uncomplicated, we can't rely on other channels for verification.

Streamlining/Recommening UX for different MUAs

<!--

Pitfalls of Centralization
--------------------------

Most messengers are centralized systems. Their vendor also provides the servers, and usually controls account management and other administrative necessities.

Centralization can lead to a lot of problems. Single points of failure are never a good idea for a system. Centralization also makes Internet censorship easier - you only have to shut down one node to control what people post online. Same with surveillance - to kick in one door with a search warrant is easier than finding the necessary doors a complex system. And of course, centralization usually leads to a lack of pluralism and diversity in a system - this makes it hard to satisfy the needs of all users. All in all, it moves the power to one central place, and everyone else has to take or leave it.

In the world of platforms, it's not a given that you can reach everyone. While we are used to maneuver within and between platforms, any communication happens on some platform. And the communication providers have power, and usually monopolies.

A centralized platform is a gilded cage. It gives users possibilities, but also erodes their sovereignty. If you want to stay in touch with the others in the platform, you can't leave - even if you know that your data is used against you and that there is another platform which suits you better, but has no users. In decentralized systems, you can at least vote with your feet. You can leave a central hub and move to another, if you don't like it - but if the hubs federate, you can still stay in touch. And if there is no hub you like, go on and host your own. Maybe others with less technical capabilities are only waiting for someone like you.

That's why Autocrypt chose the E-Mail network as a platform. There is Gmail as a provider which reads your mail to sell you stuff, but you can still write to Gmail users from an address at a more privacy-respecting E-Mail provider. This enables you to reach anyone, by still preserving your sovereignty.

But decentralized systems need federation to reach everyone, and this is not always working either. It is an effort to keep decentralized systems federated and interoperable - specifications do that. All partners of a federation have to come to an agreement how to treat each other, basically a social contract. Specifications ensure that everyone's rights are secured - if they aren't, the federation will break. It's a network out of consenting partners.

Autocrypt is such a specification, supposed to keep different mail apps interoperable. If Outlook-users could not read E-Mails sent with Thunderbird, the federation would be broken. That's why developers of several Free Software mail apps (e.g. Thunderbird-Enigmail, K9-Mail, DeltaChat) joined Autocrypt to make their implementations of the Autocrypt mechanism interoperable.



Free Software as Technological Advancement
------------------------------------------

An important dimension of software that influences the freedom of its user is the free availability of its source code. A software is commonly referred to as "free" if its source code is available to anyone who owns a copy of the software, with permission to freely modify, extend, repurpose or even integrate it in other software.

The benefits of free software are plentiful: The availability of source code for review is a requirement for any kind of trust that isn't built purely on brand and marketing, since there is no way of saying with confidence what the program actually does or doesn't do. It's also the only way to guarantee continued support and a legacy that isn't tied to the well-being or -meaning of any single person or company. A user is never actually in control of an application if they have no way of modifying its behavior, and while for most users this is a fairly theoretical option, it still ensures their freedom in the bigger picture.

Free Software is a commons. It is available for everyone, and wants to be used by everyone. It's not only free as in free beer, it's also liberating as in libre. And because it is controlled by you, there are no strings attached. No ads, no data tracking.

This is only possible because of another advantage of Free Software: it's improvable. Everyone can contribute to it, making it better. And when you improve a software so it works better for you, it immediately also works better for everyone else. And vice versa.

This means, that as any commons, it needs to be taken care of. There is always a need for maintainers, watching that Free Software remains usable. Communities need to be managed, so everyone gets along. And in the best case, the humans who are building and using the software, talk to each other, and communicate how they want to shape the world with their software.

Availability as free software is a natural evolutionary stage in the technological development of any software concept. It's the step that severs the ties with its origin of creation, shifting ownership from a singular entity to the general public. Most software applications solve a problem, but only when software is free is the problem really solved on a societal level.

In this way, free software is a form of decentralization on a more fundamental level - while decentralization is giving the control of a platform back to the user, free software is giving the control of the software back to the user. This is guaranteeing technology which works for all humans.

-->

What can be solved with Technology, what can't?
-----------------------------------------------

Technology takes its stance on societal problems - making them worse, or enabling humans to overcome them. This places a lot of responsibility on engineers - what kind of technology they build has consequences. Technology shapes the world.

But while we are using and creating technology, we don't think that you can solve every problem by technical means. It can never be a universal remedy. Decentralization and Free software are nice, but they don't make everyone free.

In this situation, we need more critical thinking, both from technology makers and policy makers. Policy as well as technology is often made in hierarchical environments - and hierarchies inhibit critical thinking.

In many non-democratic states it is forbidden to use critical thinking for the "wrong" ideas. In such environments, technology can make problems worse - even if it was built to solve problems. If you are not allowed to ask "is this really a good idea?", then it is probably a very bad idea.

Such environments exist in democratic states, too. Military and intelligence agencies are one example – and their actions led to the mass surveillance today, including all the dangers to democracy. Also most workplaces are a place of hierarchy, with command structures like in the military. Critical thinking is only regarded a good thing if it improves the product, not if it questions the authorities and the status quo.

These issues belong together. You can only make good technology if you are not afraid to answer critical questions. There are two differences which are important here:

The difference between good encryption and bad encryption is whether you listen to bug reports - or just state "works for me”. But that is the criticism that only improves the product. The difference between good encryption and a nuclear rocket comes from the other questions - everyone who questions authorities and the status quo knows, nuclear rockets are a really bad idea.

We want Autocrypt to be used for such questions, especially when they are not to be asked. We want humans to communicate, because some problems can not be solved by technology, but only by questioning, listening, and compassion.



Humans need more than Encrypted E-Mails.
----------------------------------------

What humans need, and how we can achieve it, is not up to technology - it is up to us. We will not find out through scientific discovery, but through communication and discussion.

When the spaces are controlled, and critical questions can't be asked, encryption can create spaces for those questions. Decentralization also helps here - if there is no centralized control, censorship and surveillance don't threaten to silence the critics. The communication can just go to a channel hosted by someone else, e.g. a different mail server. In the best case, you have both a communication system both encrypted and decentralized.

Autocrypt makes PGP encryption easy enough for normal users, so they can encrypt the E-Mails they already send every day. We want to develop encryption mail apps which don't get in the way of their users, which don't leave them puzzled, helpless against the omnipresent surveillance.

All in all: we want to build technology which actually improves society, which contributes to a decentralized and free Internet.

We can't do it alone. But fortunately there are others out there who empower humans in the same way: Mastodon is a decentralized social network, which focuses on meaningful and empathetic discussions. Matrix is building a decentralized and secure messenger network. ownCloud is a decentralized, open source file sharing cloud, capable of replacing Google Drive and Google Docs.

There are thousands more projects like those. Because we all do free software, we can help each other and contribute to each other.

And you can help, too: test the current state of the clients and give us your feedback on the UX & development!

More important than this, though, are the human aspects of our lives. Talk to each other, build trust, build relationships! Question authorities, question the status quo! When you are building the world of tomorrow, you should have the right questions in your heart.


