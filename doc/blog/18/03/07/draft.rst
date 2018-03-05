
Autocrypt: how Decentralization and Free Software can improve Encrypted Communication
=====================================================================================

`Since Snowden made us aware of every day mass surveillance, there is
still too much unencrypted communication. How can we build encrypted 
communication for humans?`

Communication is an ecosystem. Different species coexist peacefully
and not-so-peacefully, plants need to be watered every day, progress
happens. And sometimes, a new innovation bring a new species along;
in this case, messengers.

The flow of creativity only starts here - hundreds of different
messengers with different features have evolved of this. Audio
messages and end-to-end encryption, timed messages and profile
pictures, group chats and QR-code fingerprint verification; many
interesting developments came out of messengers.

At the same time, people still send faxes, and all of those means of
communication coexist. Because even though messengers have been a
revolution to communication, they have many disadvantages and problems.

Most messengers put little value on history, it's hard to separate
your private and business communication, and they have been a
battlefield of influence for big players like Facebook or Google. All
widely used messengers at this point are centralized solutions with
no federation, commonly referred to as "silos". This allows great
control of the platform and rapid development - but lacks the network
effects to truly reach everyone. There is not a single messenger out
there which all of my friends use.

When I really want to reach anyone, I still default to E-Mail. And
why not? E-Mail is the only actually universal platform. It's
federated, and not dependent on a single company, it relies on open
standards. And of course, everyone has E-Mail. But there is no
innovation in the field, the E-Mail ecosystem moves at glacial pace.

Of course we need progress, but legacy is important. If the progress
can't deliver, people will fall back to the legacy options they have,
E-Mail, and even faxes. Another lesson is that even a perfectly secure
technology can't protect anyone, if it doesn't have users. If you are
the only user of a perfectly safe messenger, you can't write
confidential messages to anyone. And in the end, culture votes with
its feet. Maybe one day people will walk away from E-Mail, maybe
messengers will die out. Nobody can stop them.

When we both joined the Autocrypt project, we wanted to decrease the
amount of unencrypted Internet traffic. The working title was
"Encrypted E-Mail for Humans". Maybe humanity needs more than
encrypted communication; but it‘s one of the first steps too many
other problems.

Even five years after Snowden there is no easy default way to write
securely with whoever they want to (No, Whatsapp doesn't count as
secure). Right now, the masses can’t protect themselves from the
Internet. Messengers didn't solve this problem.

If you look at all the different messengers and encryption tools,
they all have one of three problems. Either they are too complicated
to use (PGP), centralized and proprietary (Whatsapp, Threema), or
they lack the network effects (Signal, Wire, XMPP, Tox, Briar, ....).
Autocrypt chose to improve PGP in terms of ease-of-use, compatibility
and user friendliness. Of the three problems, it seemed to be the
easiest to fix.

The Autocrypt effort is driven by a diverse group of mail app
developers, hackers and researchers who collectively aim to increase
the overall end-to-end encryption of E-Mail in the net. Autocrypt is
a specification for mail apps. It automates key management and key 
distribution, so users don't have to do it. Many mail apps implement
the Autocrypt standard to allow their users to easily encrypt E-Mails.

The basic concept of Autocrypt is fairly easy. In short: Autocrypt
uses regular E-Mail messages between people to piggyback necessary
information to allow encrypting subsequent messages; it adds a new
Autocrypt E-Mail header for transferring public OpenPGP keys and 
driving encryption behavior. By default, key management is not visible
to users. You can encrypt group conversations by sending the keys of 
everyone to everyone. And you can setup another device for the same 
key by sending an E-Mail with the private key to yourself. That's it,
the specification is only 12 pages long.

We chose the E-Mail network for our new encryption specification.
E-Mail is decentralized, widespread, and just won't die. Its network
effects are useful, its longevity is ironic, but its decentralization
is essential to our goals.


A Different Approach on E-Mails
-------------------------------

Most messengers are not only centralized systems, they also use your
phone number to identify you. Managing people's identity over a phone 
number is ethically difficult though, it takes the control over their 
identity away from them. The phone number system is proprietary and 
easy to track. E-Mail as an identity provider is better, because it
relies on open standards. Everyone can provide E-Mail, and doesn't
have to trust one of the few monopolistic telephone providers. But
that's not the only advantage of decentralization.

In the world of platforms, it's not a given that you can reach
everyone. While we are used to maneuver within and between platforms,
any communication happens on some platform. And the communication 
providers have power, and usually monopolies.

A centralized platform is a gilded cage. It gives users possibilities,
but also erodes their sovereignty. If you want to stay in touch with 
the others in the platform, you can't leave - even if you know that 
your data is used against you and that there is another platform which 
suits you better, but has no users. In decentralized systems, you can 
at least vote with your feet. You can leave a central hub and move to
another, if you don't like it - but if the hubs federate, you can 
still stay in touch. And if there is no hub you like, go on and host 
your own. Maybe others with less technical capabilities are only 
waiting for someone like you.

That's why Autocrypt chose the E-Mail network as a platform. There is
Gmail as a provider which reads your mail to sell you stuff, but you
can still write to Gmail users from an address at a more 
privacy-respecting E-Mail provider. This enables you to reach anyone,
by still preserving your sovereignty.

One of the specific approaches by Autocrypt is the focus on mail app
implementation. To use Autocrypt, you don't require your E-Mail 
Provider to do anything. Instead, with Autocrypt several mail app 
developers work closely together. This allows for fluid development,
and also the adjustment of the specification.

This form of incremental improvement and deployment is very natural
for a simple reason: there will always be cleartext E-Mails in the
same system as encrypted E-Mails. Encryption shouldn't get into the 
way of its users; and if we don't want to break existing workflows,
we have to take care of backwards compability and legacy support.


How to Make Encryption Easy Enough for Everyone
-----------------------------------------------

There are reasons why encryption has not been widely adopted yet,
despite the threats to everyone's privacy. For many users, it has
never been convenient enough to encrypt E-Mails. PGP is a very 
complex tool, which can be used for various purposes. Encrypted 
Communication is just one of them, software signing, document 
signature validity, or online authentication are others.

To fulfill all those use cases, users have indeed to know which keys 
they are using, trusting, and what exactly they are doing. What the 
difference between a public and a private key is. What signatures 
have to do with encryption. But do they have to know that if they 
only want encrypted communication? If you had to think about security
before each message you send - would you still want to message 
securely?

Because of these issues, one thing was clear, when Autocrypt was born:
Autocrypt users should not have to know that they are using keys when
they write encrypted. If everyone you write to receives your public 
key, you don't have to know how to provide public keys. If you can 
setup new devices with a simple procedure, you don't have to know 
what a private key is.

While we care deeply about decentralization and user autonomy, it is 
always trivial to bring those in line with ease of use. A streamlined
user experience is usually better for usability, it is easier to find
help on some issues and more intuitive. On the other hand, we want to
allow different Autocrypt-enabled mail apps to do things their own
way. Letterbox for example focuses on Bitcoin.de-users, and may have 
other considerations than Delta.Chat, an instant messenger based on 
the E-Mail protocol. That's why Autocrypt tries to give 
recommendations on user experience, while not forcing mail apps to a
unified approach.

Another point where this is important is key discovery. Keys should 
be hidden from users, but there should still be a decentralized way
to distribute keys. Identity is an important part of user autonomy
and should not be left to a centralized key server. On the other hand,
to remain uncomplicated, we can't rely on other channels for 
verification. If users had to do an out-of-band verification with 
everyone they want to write to, encryption would not be convenient
anymore.

That's why we trust on first use, and distribute public keys in the 
header of the E-Mails. It is hidden, but decentralized, and leaves 
the control over their keys with the users, without them necessarily
knowing it. And if they want to do an out-of-band verification with 
their associates, there will always be user-friendly options, e.g. 
with a QR code comparison.

Technically, Autocrypt is not much more than a set of some reasonable
configuration decisions. But together, the decisions made by Autocrypt
can streamline the complex PGP system to be usable for encrypted 
communication, between everyone. It is not a technically complex 
approach which introduces breaking new features - it is rather 
reducing complexity.

This is good, because what encrypted communication needs, is not more 
of the same intricate ideas. Rather it needs some reason and common 
sense. That's the only way to bring people together, and it can't be
done by another technological solution to a social problem. Sometimes
it's rather about the right people at the right place and time, 
coming to an agreement on how they want to interact.


What can be solved with Technology, what can't?
-----------------------------------------------

Technology takes its stance on societal problems - making them worse,
or enabling humans to overcome them. This places a lot of 
responsibility on engineers - what kind of technology they build has
consequences. Technology shapes the world.

But while we are using and creating technology, we don't think that
you can solve every problem by technical means. It can never be a 
universal remedy. Decentralization and Free software are nice, but 
they don't make everyone free.

In this situation, we need more critical thinking, both from 
technology makers and policy makers. Policy as well as technology is 
often made in hierarchical environments - and hierarchies inhibit 
critical thinking.

In many non-democratic states it is forbidden to use critical 
thinking for the "wrong" ideas. In such environments, technology can 
make problems worse - even if it was built to solve problems. If you
are not allowed to ask "is this really a good idea?", then it is 
probably a very bad idea.

Such environments exist in democratic states, too. Military and 
intelligence agencies are one example – and their actions led to the
mass surveillance today, including all the dangers to democracy. Also
most workplaces are a place of hierarchy, with command structures 
like in the military. Critical thinking is only regarded a good thing 
if it improves the product, not if it questions the authorities and 
the status quo.

These issues belong together. You can only make good technology if 
you are not afraid to answer critical questions. There are two 
differences which are important here:

The difference between good encryption and bad encryption is whether 
you listen to bug reports - or just state "works for me”. But that is
the criticism that only improves the product. The difference between
good encryption and a nuclear rocket comes from the other questions
- everyone who questions authorities and the status quo knows, nuclear 
rockets are a really bad idea.

We want Autocrypt to be used for such questions, especially when they
are not to be asked. We want humans to communicate, because some 
problems can not be solved by technology, but only by questioning, 
listening, and compassion.


Humans need more than Encrypted E-Mails.
----------------------------------------

What humans need, and how we can achieve it, is not up to technology 
- it is up to us. We will not find out through scientific discovery,
but through communication and discussion.

When the spaces are controlled, and critical questions can't be asked,
encryption can create spaces for those questions. Decentralization 
also helps here - if there is no centralized control, censorship and
surveillance don't threaten to silence the critics. The communication
can just go to a channel hosted by someone else, e.g. a different 
mail server. In the best case, you have both a communication system
both encrypted and decentralized.

Autocrypt makes PGP encryption easy enough for normal users, so they
can encrypt the E-Mails they already send every day. We want to 
develop encryption mail apps which don't get in the way of their
users, which don't leave them puzzled, helpless against the 
omnipresent surveillance.

All in all: we want to build technology which actually improves 
society, which contributes to a decentralized and free Internet.

We can't do it alone. But fortunately there are others out there who 
empower humans in the same way: Mastodon is a decentralized social 
network, which focuses on meaningful and empathetic discussions. 
Matrix is building a decentralized and secure messenger network. 
ownCloud is a decentralized, open source file sharing cloud, capable 
of replacing Google Drive and Google Docs.

There are thousands more projects like those. Because we all do free
software, we can help each other and contribute to each other.

And you can help, too: test the current state of the clients and give 
us your feedback on the UX & development!

More important than this, though, are the human aspects of our lives.
Talk to each other, build trust, build relationships! Question 
authorities, question the status quo! When you are building the world 
of tomorrow, you should have the right questions in your heart.


