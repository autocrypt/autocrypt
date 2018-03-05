How to Fix E-mail: making communication encrypted and decentralized with Autocrypt
==================================================================================
Despite the revelations that companies and governments see the finest details of our everyday lives, most communication on the Internet today is still unencrypted. Email, one of the first features of the Internet, remains relatively unchanged and unencrypted over the past 50 years. An email message sent in the early 1970s is as insecure and decentralized as a basic email today. Even so, email is the largest open federated identity system by anchoring the web with two-factor authentication and account recovery. It continues to relay sensitive information between people and organisations, unencrypted and vulnerable. Even five years after Snowden, there is no easy and free way to write securely. 

Developers have attempted to bridge this gap by inventing a wide variety of protocols, tools, and applications for communicating that are easier to use. Messaging applications are arguably the most influential of these innovations. WhatsApp, Facebook messenger, and WeChat together top over 3.5 billion active users worldwide. Signal is growing in popularity, and recently collaborated with WhatsApp to provide end-to-end encryption for free to all WhatsApp users. The centralized ownership of messaging platforms gives usability and further functionality improvements over Email, but at a price. As of now, all massively used messengers are hidden  behind proprietary source code, encryption techniques, and algorithms that are impossible to independently verify. Furthermore, these centralized messengers have been censored and blocked in some countries, having raised serious concerns regarding human rights and freedom of expression. 

Encrypted email, on the other hand, is resilient to such attacks, due to its decentralized nature. It's federated, not dependent on a single company, and relies on open standards. Encrypted email, then, is independently verifiable and secure. Attempts have been made to make encrypted email via PGP the de facto standard for secure communication. However, PGP has failed to see wide adoption outside of specialist communities, in large part because of difficulties with user experience. In short, we already have communication that is decentralized and encrypted, just no one is using it. A lesson to take from the failed project of widespread encrypted email is that even a perfectly secure technology can't protect anyone if it doesn't have users. This leaves email in a fragile position despite its widespread usage.

The Social Approach
--------------------

In December 2016, a diverse group of mail application developers, hackers, and researchers met to fix encrypted email. They were willing to take fresh approaches, learn from past mistakes, and collectively aim to increase the overall encryption of email in the Internet. After a few short months, they produced a 12 page specification for mail applications called Autocrypt. This specification builds upon the existing (and broken) Internet email infrastructure, and does not involve any new companies, tools, or servers. A primary goal of Autocrypt is to protect first against passive data-collecting adversaries, focusing on fixing this broken piece of the Internet. RFC7435 A New Perspective is an influential document that motivated this focus.

The basic concept of Autocrypt is fairly easy. In short: Autocrypt
uses regular email messages between people to piggyback necessary
information to allow encrypting subsequent messages; it adds a new
Autocrypt email header for transferring public OpenPGP keys and 
driving encryption behavior. By default, key management is not visible
to users. You can encrypt group conversations by sending the keys of 
everyone to everyone. And you can setup another device for the same 
key by sending an email with the private key to yourself. That's the
technical side of the coin, but the social approach is equally important.

The state of encrypted email is quite bad, but the federated email
system is actually quite healthy. Intercompability is almost
universal, and the system has coped with the few incremental changes
to the email system quite well. That's a strength of the email
standards, and a healthy offering of email services. The state of
encrypted email is not bad because the email system would not work
- it is totally fine, and moves slowly enough to stay resilient.
Instead, it is a problem of user-facing mail applications.

Autocrypt takes a unique approach to this problem by focusing on mail application implementation. Several mail application developers have worked closely together to ensure their implementations of the specification are compatible. To use Autocrypt, users don't require the email provider to do anything. It automates key management and key distribution, and adds necessary encryption information, such as a public OpenPGP key, to unencrypted email to allow encrypting subsequent messages. Autocrypt is a specification intended to keep different email applications interoperable, encrypted, and easy to use. 

Keeping decentralized systems federated and interoperable, and specifications are the fundamental piece of this effort. All partners have to come to an agreement how to treat each other, in essence, a social contract. Specifications ensure that everyone's rights are secured; if they aren't, interoperability will break. Email is simply this: a network of consenting partners. For example, Gmail is a provider which reads mail and advertises to users, but anyone can write to Gmail users from a more privacy-respecting email provider. Autocrypt follows this approach, enabling users of Autocrypt to still reach anyone using basic unencrypted email. There will always be cleartext emails in the same system as encrypted emails. Encryption shouldn't get into the way of its users; and if we don't want to break existing workflows, we have to take care of backwards compatibility and legacy support.

The Benefits of Email
------------------------

Most messengers are not only centralized systems, they also use a phone number to identify users. Managing people's identity over a phone number is ethically questionable, as it can lead to human rights violations, censorship, and unwarranted tracking. Email as an identity provider is better for a variety of reasons. Email is an open standard, which means that everyone can provide email, and doesn't have to trust one of the few monopolistic telephone providers.  It is also free to create an email, while mobile phone numbers can be unattainably expensive in some parts of the world.

In decentralized systems such as email, users are free to move between providers and platforms (e.g., Thunderbird to Outlook, or Gmail to ProtonMail). You can leave a central hub and move to another, and still be able to communicate with the same people. If an adversarial government or ISP wanted to block Autocrypt, it would require that the censor block all encrypted email, including those that government and business rely on, and so would result in a much higher political and economic cost for the censor. Decentralized systems such as email are then more resilient by design, and still operating as intended -- fault tolerant and interoperable. This is why we should not just give up on email, but instead make a concerted effort to improve it’s broken parts.

How to Make Encryption Easy Enough for Everyone
---------------------------------------------

There are reasons why encryption has not been widely adopted yet, despite the threats to everyone's privacy. For many users, it has never been convenient enough to encrypt emails. PGP is a very complex tool, which can be used for various purposes. Encrypted Communication is just one of them, while software signing, document signature validity, and online authentication are others.

To fulfill all those use cases, users have to know which keys they are using, trusting, and what exactly they are doing. They need to know the difference between a public and a private key. What signatures have to do with encryption. But do they have to know that if they only want simple encrypted messages? If you had to think about security before each message you send - would you still want to message securely? The answer has proven to be a resounding no, as only a small percent of email is sent encrypted, and the effort to saturate manual PGP encryption has been largely only used within specialized circles of developers, security experts, journalists, and some organizations.

Because of these issues, one thing was clear: users should not have to know that they are using OpenPGP keys when they send an email. This is the benefit of attaching public keys to every email users send while they are using the Autocrypt specification. Autocrypt tries to give recommendations on user experience depending on the internal state of key exchanges, while not forcing mail applications to adopt a unified approach. Different Autocrypt-enabled mail applications to do things their own way, and there are a variety of applications that implement the specification. One of these includes an increasingly popular instant messenger inspired from Telegram, called Delta.Chat.

Another point where this is important is key discovery. Keys should be hidden from users, but there should still be a decentralized way to distribute keys. Identity is an important part of user autonomy and should not be left to a centralized key server. On the other hand, to remain uncomplicated, we can't rely on other channels for verification. If users had to do an out-of-band verification with everyone they want to write to, encryption would not be convenient anymore.
That's why we trust on first use, and distribute public keys in the header of the emails. It is hidden, but decentralized, and leaves the control over their keys with the users, without them necessarily knowing it. And if they want to do an out-of-band verification with their associates, there will always be user-friendly options, e.g. with a QR code comparison.

Technically, Autocrypt is not much more than a set of some reasonable configuration decisions. But together, the decisions made by Autocrypt can streamline the complex PGP system to be usable for encrypted communication, between everyone. What encrypted communication needs is simple, measured steps of improvement. That's the only way to bring people together while maintaining the original intent of the architecture. 

The Internet: A Little Less Broken
-----------------------------------

Technology takes a stance on societal problems. There is no neutral technology, as there is no neutral engineer. This places a lot of responsibility on engineers. While we are using and creating technology, remember that many problems will not be solved by technical means. Often, problems will require a social approach, with the internet organizations, committees, consortiums, task forces, and groups like Autocrypt that try hard to make the current Internet a little less broken. 

What humans need, and how we can achieve it, is not up to technology - it is up to us. We will not find out through scientific discovery, but through communication and discussion. When the spaces are controlled and monitored, a chilling effect leads to the absence of the critical questions required in a functional society. Encryption can create space for this by providing the same privacy and security on the Internet that people have in real life. Decentralization also helps here - if there is no centralized control, censorship and surveillance don't threaten to silence the critics. In the best case, email would be a communication system that is both encrypted and decentralized.

All in all: we want to build technology which actually improves society, which contributes to a decentralized and free Internet. We can't do it alone. But fortunately there are others out there who empower humans in the same way: Mastodon is a decentralized social network, which focuses on meaningful and empathetic discussions. Matrix is building a decentralized and secure messenger network. ownCloud is a decentralized, open source file sharing cloud, capable of replacing Google Drive and Google Docs. There are thousands more projects like these.

[WHEN DID AUTOCRYPT 1 GET RELEASED?] [WHEN WILL LEVEL 2 COME OUT?] We are awaiting new testers to come see the current state of the Autocrypt clients, find bugs, and give feedback on the user experience and development. 



