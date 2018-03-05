How to Fix E-mail: making communication encrypted and decentralized with Autocrypt
==================================================================================

`Email has been declared dead many times but refuses to die. There is a new effort towards making encrypted end-to-end email communication as automatic as possible. It is part of a diverse set of efforts to re-invigorate the email ecosystem, which remains a crucial cornerstone of a functioning, open Internet.`

The email server network forms the largest open, socially federated
messaging system in human history. Federated email servers relay messages
for around 3 billion users, based on open protocols and the freedom to
operate and integrate your own server. Despite not changing much from its
original specification over 50 years ago, it remains the largest open federated
identity system by anchoring the web with two-factor authentication and account
recovery.

Emails continue to relay sensitive information between people and
organisations, unencrypted and vulnerable. Even five years after Snowden, most
email is being sent without end-to-end encryption. Even though there have been
massive improvements in transport encryption via TLS, the mail servers remain
a big attack surface for malicious hackers and surveillance.

To try to bridge this gap, WhatsApp and other centralized messaging platforms
have claimed to provide usable end-to-end encryption. However, WhatsApp and
other massively used messengers (3.5 billion users between Facebook
messenger, WhatsApp, and WeChat alone) are hidden behind proprietary source
code, encryption techniques, and algorithms that are impossible to
independently verify. Furthermore, these centralized messengers have been
censored and blocked in some countries, having raised serious concerns
regarding human rights and freedom of expression. It is a socially dangerous
development if fundamental human communication is controlled and exploited by
a few commercial entities.

End-to-end encrypted email, on the other hand, is resilient to such attacks,
such as spying and censorship, due to its decentralized nature. It's federated,
not dependent on a single company, and relies on open standards. Attempts have been made to
make the PGP the de facto standard for secure communication.  However, PGP has
failed to see wide adoption outside of specialist communities, in large part
because of difficulties with user experience. In PGP, we already have
end-to-end encrypted email that is decentralized, just no one is using it.
A lesson to take from the failed project of widespread encrypted email is that
even a perfectly secure technology can't protect anyone if it doesn't reach a critical mass of
users. This leaves email in a fragile position, despite its widespread usage.

The Social Approach
--------------------

In December 2016, a diverse group of email application developers, 
hackers, and researchers met to fix encrypted email. They were willing 
to consider new, innovative approaches, learn from past mistakes, and collectively 
aim to increase the overall encryption of email in the Internet. After
a few months, they reselased a 12 page specification for email 
applications called Autocrypt. This specification builds upon the existing (and broken) Internet email
infrastructure and doesn't involve any new companies, tools, or servers.
A primary goal of Autocrypt is to protect against passive data-collecting
adversaries, focusing on fixing this broken piece of the Internet. RFC7435
A New Perspective is an influential document that motivated this focus. In
other words, Autocrypt primarily aims to provide convenient encryption that is
neither perfect nor as secure as traditional email encryption, but is
convenient enough for much wider adoption. 

Autocrypt goes beyond IETF or W3C practices by working from a strong "usability
first" perspective and specifying not only wire formats but also user
experiences and internal application state. Autocrypt is decentralized in that
it does not require a key server or special support from email servers. It
rather transmits cryptographic information along with normal email messages and
lets applications automatically process and interpret this information in
order to offer a uniform user experience. It automates key management and
distribution, and adds necessary encryption information, such as a public
OpenPGP key, to unencrypted email to allow encrypting subsequent messages.  By
default, key management is not visible to users, but users can setup other
devices as well as encrypted group e-mails. Despite Autocrypt's efforts to make
encryption easy, there will always be cleartext emails in the same system as
encrypted emails if the other party doesn't use Autocrypt. With Autocrypt,
end-to-end encryption is opportunistic while still prioritizing usability. 

Autocrypt has released its first specification, code-named "Level 1", on
December 21st 2017. In early 2018, the Enigmail Mozilla Thunderbird extension
and the K-9 Mail Android application released support for Autocrypt. Moreover, DeltaChat is
a new application that uses the email server network but offers a
IM style of chat interface. It fully implements the Autocrypt specification
and allows users to send end-to-end encrypted messages between the messaging
interface and traditional email clients. Several email application developers
have worked closely together to ensure their implementations of the
specification are mutually compatible. Autocrypt is a specification intended to keep
different email applications interoperable, encrypted, and easy to use. 

The Benefits of Email
------------------------

Most messengers are not only centralized systems, they also use a phone number to identify users. Managing people's identity over a phone number is ethically questionable, as it can lead to human rights violations, censorship, and unwarranted tracking. Email as an identity provider is better for a variety of reasons. It's an open standard, which means that everyone can provide email, and doesn't have to trust one of the few monopolistic telephone providers. Also, creating an email account is free, while mobile phone numbers can be unattainably expensive in some parts of the world.

In decentralized systems, such as email, users are free to choose and switch providers and platforms (e.g., Thunderbird to Outlook, or Gmail to ProtonMail). You can leave a central hub and move to another, and still be able to communicate with the same people. If an adversarial government or ISP wanted to block Autocrypt, it would require the censor to block all encrypted email, including those that government and business rely on, thus resulting in a much higher political and economic cost for the censoring party. In those cases, decentralized systems -- such as email --  are more resilient by design and still operate as intended -- fault tolerant and interoperable. This is why we should not just give up on email, but instead make a concerted effort to improve its broken parts.

How to Make Encryption Easy Enough for Everyone
---------------------------------------------

There are reasons why encryption has not been widely adopted yet, despite the threats to everyone's privacy. For many users, it has never been convenient enough to encrypt emails. PGP is a very complex tool, which can be used for various purposes. Encrypted communication is just one of them, while software signing, document signature validity, and online authentication are others.

To fulfill all those use cases, users have to know which keys they are using, trusting, and what exactly they are doing. They need to know the difference between a public and a private key. What signatures are related to encryption. But do they have to know that if they only want simple encrypted messages? If you had to think about security before each message is sent, would you still want to message securely? The answer has proven to be a resounding no, as only a small percent of email is sent encrypted and the effort to saturate manual PGP encryption has largely only been used within specialized communities of developers, security experts, journalists, and some organizations.

Because of these issues, one thing was clear: Users should not have to know that they are using OpenPGP keys when they send an email. This is the benefit of attaching public keys to every email users send, while they are using the Autocrypt specification. Autocrypt tries to give recommendations on user experience, depending on the internal state of key exchanges, while not forcing email applications to adopt a unified approach. Different Autocrypt-enabled email applications do things their own way, and there are a variety of applications that implement the specification. One of these includes an increasingly popular instant messenger inspired from Telegram, called DeltaChat.

Another point where this is important is key discovery. Keys should be hidden from users, but there should still be a decentralized way to distribute keys. Identity is an important part of user autonomy and should not be left to a centralized key server. On the other hand, to remain plain and simple, we can't rely on other channels for verification. If users had to do an out-of-band verification with everyone they want to write to, encryption would not be convenient anymore.
That's why we trust on first use and distribute public keys in the email header. It is hidden, but decentralized, and leaves the users in control of their keys, without them necessarily knowing it. And if they want to do an out-of-band verification with their associates, there will always be user-friendly options, e.g. with a QR code comparison.

Technically, Autocrypt is not much more than a set of some reasonable configuration decisions. But together, the decisions made by Autocrypt can streamline the complex PGP system to be usable for encrypted communication between everyone. What encrypted communication needs is simple, measured steps of improvement. That's the only way to bring people together while maintaining the original intent of the architecture. 

The Internet: A Little Less Broken
-----------------------------------

Technology takes a stance on societal problems. There is no neutral technology, as there is no neutral engineer. This places a lot of responsibility on engineers. While we are using and creating technology, remember that many problems will not be solved by technical means. Often, problems will require a social approach, with the internet organizations, committees, consortiums, task forces, and groups like Autocrypt that try hard to make the current Internet a little less broken. 

What humans need, and how we can achieve it, is not up to technology - it is up to us. We will not find out through scientific discovery, but through communication and discussion. When the spaces are controlled and monitored, a chilling effect leads to the absence of the critical questions required in a functional society. Encryption can create space for this by providing the same privacy and security on the Internet that people have in real life. Decentralization also helps here - if there is no centralized control, censorship and surveillance don't threaten to silence the critics. In the best case, email would be a communication system that is both encrypted and decentralized.

All in all: we want to build technology which actually improves society, which contributes to a decentralized and free Internet. We can't do it alone. But fortunately there are others out there who empower humans in the same way: Mastodon is a decentralized social network, which focuses on meaningful and empathetic discussions. Matrix is building a decentralized and secure messenger network. ownCloud is a decentralized, open source file sharing cloud, capable of replacing Google Drive and Google Docs. There are thousands more projects like these.

Right now, we want to help implementors of mail applications to add Autocrypt support.
In the next steps, we want to find solutions on how to protect users against active adversaries.
We also want to play with new approaches for opportunistically encrypted mailing lists.
Together with the mail application developers, the Autocrypt specification will be further improved.
It is a social effort to keep up interoperability.
We are awaiting new testers to come see the current state of the Autocrypt clients, find bugs, and give feedback on the user experience and development. 



