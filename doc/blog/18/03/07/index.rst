How to Fix E-mail: making communication encrypted and decentralized with Autocrypt
==================================================================================

`Email has been declared dead many times but refuses to die. There is a new effort towards making encrypted end-to-end email communication as automatic as possible. It is part of a diverse set of efforts to re-invigorate the email ecosystem which remains a crucial cornerstone of a functioning, open Internet.`

The e-mail server network forms the largest open, socially federated
messaging system in human history. Federated e-mail servers relay messages
for around 3 billion users, based on open protocols and on the freedom to
operate and integrate your own server. Despite not changing much from it's
original specification over 50 years ago, it remains the largest open federated
identity system by anchoring the web with two-factor authentication and account
recovery.

Emails continue to relay sensitive information between people and
organisations, unencrypted and vulnerable. Even five years after Snowden, most
email is send without end-to-end encryption. Even though there have been
massive improvements in transport encryption via TLS, the mail servers remain
a big attack surface for malicious hackers and surveillance.

To try to bridge this gap, WhatsApp and other centralized messenging platforms
have claimed to provide usable end-to-end encryption. However, WhatsApp and
other massively used messengers (3.5 billion users between Facebook
messenger, WhatsApp, and WeChat alone) are hidden behind proprietary source
code, encryption techniques, and algorithms that are impossible to
independently verify. Furthermore, these centralized messengers have been
censored and blocked in some countries, having raised serious concerns
regarding human rights and freedom of expression. It is a socially dangerous
development if fundamental human communication are controlled and exploited by
a few commercial entities.

End-to-end encrypted email, on the other hand, is resilient to such attacks
such as spying and censorship, due to its decentralized nature. It's federated,
not dependent on a single company, and relies on open standards. Attempts have been made to
make the PGP de facto standard for secure communication.  However, PGP has
failed to see wide adoption outside of specialist communities, in large part
because of difficulties with user experience. In PGP, we already have
end-to-end encrypted email that is decentralized, just no one is using it.
A lesson to take from the failed project of widespread encrypted email is that
even a perfectly secure technology can't protect anyone if it doesn't have
users. This leaves email in a fragile position despite its widespread usage.

The Social Approach
--------------------

In December 2016, a diverse group of mail application developers, 
hackers, and researchers met to fix encrypted email. They were willing 
to take fresh approaches, learn from past mistakes, and collectively 
aim to increase the overall encryption of email in the Internet. After
a few short months, they produced a 12 page specification for mail 
applications called Autocrypt. This specification builds upon the existing (and broken) Internet email
infrastructure, and does not involve any new companies, tools, or servers.
A primary goal of Autocrypt is to protect first against passive data-collecting
adversaries, focusing on fixing this broken piece of the Internet. RFC7435
A New Perspective is an influential document that motivated this focus.  In
other words, Autocrypt first aims to provide convenient encryption that is
neither perfect nor as secure as traditional e-mail encryption, but is
convenient enough for much wider adoption. 

Autocrypt goes beyond IETF or W3C practises by working from a strong "usability
first" perspective and specifying not only wire-formats but also user
experiences and internal application state. Autocrypt is decentralized in that
it does not require a key server or special support from e-mail servers. It
rather transmits cryptographic information along normal e-mail messages and
lets applicationss automatically process and interpret this information in
order to offer a uniform user experience.  It automates key management and key
distribution, and adds necessary encryption information, such as a public
OpenPGP key, to unencrypted email to allow encrypting subsequent messages.  By
default, key management is not visible to users, but users can setup other
devices as well as encrypted group e-mails. Despite Autocrypt's efforts to make
encryption easy, there will always be cleartext emails in the same system as
encrypted emails, if the other party does not have Autocrypt. With Autocrypt,
end-to-end encryption is opportunistic while still prioritizing usability. 

Autocrypt has released its first specification, code-named "Level 1", on
December 21st 2017. Early 2018, the Enigmail Mozilla Thunderbird extension,
and K-9 Mail on Android released support for Autocrypt. Moreover, DeltaChat is
a new application that uses the e-mail server network but offers a
Telegram-style chat interface. It fully implements the Autocrypt specification
and allows users to send end-to-end encrypted messages between the messenging
interface and traditional e-mail clients. Several mail application developers
have worked closely together to ensure their implementations of the
specification are compatible.  Autocrypt is a specification intended to keep
different email applications interoperable, encrypted, and easy to use. 

Next steps for Autocrypt include helping new implementors add
Autocrypt Level 1 support, researching protection against active attacks
from providers, and discussing new specifications after the first round
of implementations is complete and user feedback is received.

Making E-Mail Encryption Usable
-------------------------------

There are reasons why encryption has not been widely adopted yet, despite the threats to everyone's privacy. For many users, it has never been convenient enough to encrypt emails. PGP is a very complex tool, which can be used for various purposes. Encrypted Communication is just one of them, while software signing, document signature validity, and online authentication are others.

To fulfill all those use cases, users have to know which keys they are using, trusting, and what exactly they are doing. They need to know the difference between a public and a private key. What signatures have to do with encryption. But do they have to know that if they only want simple encrypted messages? If you had to think about security before each message you send - would you still want to message securely? The answer has proven to be a resounding no, as only a small percent of email is sent encrypted, and the effort to saturate manual PGP encryption has been largely only used within specialized circles of developers, security experts, journalists, and some organizations.

Because of these issues, one thing was clear: users should not have to know that they are using OpenPGP keys when they send an email. This is the benefit of attaching public keys to every email users send while they are using the Autocrypt specification. Autocrypt tries to give recommendations on user experience depending on the internal state of key exchanges, while not forcing mail applications to adopt a unified approach. Different Autocrypt-enabled mail applications to do things their own way, and there are a variety of applications that implement the specification. One of these includes an increasingly popular instant messenger inspired from Telegram, called Delta.Chat.

Another point where this is important is key discovery. Keys should be hidden from users, but there should still be a decentralized way to distribute keys. Identity is an important part of user autonomy and should not be left to a centralized key server. On the other hand, to remain uncomplicated, we can't rely on other channels for verification. If users had to do an out-of-band verification with everyone they want to write to, encryption would not be convenient anymore.
That's why we trust on first use, and distribute public keys in the header of the emails. It is hidden, but decentralized, and leaves the control over their keys with the users, without them necessarily knowing it. And if they want to do an out-of-band verification with their associates, there will always be user-friendly options, e.g. with a QR code comparison.

Technically, Autocrypt is not much more than a set of some reasonable configuration decisions. But together, the decisions made by Autocrypt can streamline the complex PGP system to be usable for encrypted communication, between everyone. What encrypted communication needs is simple, measured steps of improvement. That's the only way to bring people together while maintaining the original intent of the architecture.

Strengthening E-Mail strengthens the Open Internet
--------------------------------------------------

It's worthwhile to strengthen the massively federated and diverse e-mail
ecosytem because it provides a better way forward for the Open Internet.
Most messengers are not only centralized systems, but also use a phone number to identify users. Managing people's identity over a phone number is ethically questionable, as it can lead to human rights violations, censorship, and unwarranted tracking. Email as an identity provider is better for a variety of reasons. Email is an open standard, which means that everyone can provide email, and don't have to trust one of the few monopolistic telephone providers.  It is also free to create an email, while mobile phone numbers can be unattainably expensive in some parts of the world.

If the highly proprietary and tracked phone number system becomes the
dominant system for network identification, it will make it easier for
repressive regimes and rising authoriarianisms to target civilians.
You can choose your e-mail provider from a very diverse set of
commercial and not-for-profit organizations, but you can only choose your
mobile phone network from state-vetted providers. As you move from
cell-tower to cell-tower your location is tracked in a fine-grained
manner. 

BY contrast, E-mail providers are an important barrier to aggressive
state tracking and surveillance. Providers often operate outside of an individual's
jurisdiction, rendering one safer from immediate tracking and surveillance. Decentralized systems such as email leaves users free to move between providers (Gmail to Proton Mail) and applications (e.g., Thunderbird to Outlook). You can leave a central hub and move to another, and still be able to communicate with the same people. Moreover, as businesses and organizations continue to depend on e-mail for professional communications, it's difficult to block or censor e-mail without damage to companies and governments themselves, leaving higher political and economic costs. Decentralized systems such as e-mail are then more resilient by design, and still operating as intended -- fault tolerant and interoperable. This is why we should not just give up on email, but instead make a concerted effort to improve it’s broken parts.

Let's enrich the e-mail ecosystem, not only with usable PGP encryption,
but also with new apps and efforts. The autonomy to run standalone and
interoperable e-mail servers is a fundamental benefit for organizations
and people around the world.  Who would bet that Whatsapp and Telegram
will still be there and going strong in 10 years from now? They didn't
exist 10 years ago, which admittedly feels like centuries for the Internet.
Maybe the federated and diverse e-mail system evolves a bit like limetrees:
even if it takes a lot of damage and several parts of it die, they survive, strive,
and some survive for millenias.
