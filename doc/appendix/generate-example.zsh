#!/bin/zsh

add-header-to-ascii-armor() {
    local file=$1 line=$2
    # GNU sed specific -i
    sed -i "2i$line" $file
}

# this is a quick and dirty script to save time generating examples
# please don't use in production for generating autocrypt keys!
generate-autocrypt-key() {
    local uid=$1
    local tmp=$(mktemp -d)
    ({
        export HOME=$tmp
        gpg --no-auto-check-trustdb --batch --passphrase '' --quick-generate-key $uid ed25519
        fpr="$(gpg --no-auto-check-trustdb  --fingerprint --with-colons | grep fpr | cut -d: -f10)"
        [[ -n $fpr ]] || { echo "Failed generating key, couldn't get fingerprint"; return 1; }
        gpg --no-auto-check-trustdb --batch --passphrase '' --quick-add-key $fpr cv25519

        gpg --armor --export-secret-keys $fpr > $uid.sec.asc
        gpg --armor --export $fpr > $uid.pub.asc

        base64key=( ${(f)"$(gpg --no-auto-check-trustdb  --export $fpr | base64 -w 75)"} )
        base64key=( \ $^base64key )
        base64key=${(F)base64key}
        echo -E - $base64key
    } always {
        rm -r $tmp
    })
}

encrypt-file-to() {
    local tmp=$(mktemp -d)
    local file=$1 from=$2
    local to=( $argv[3,$] )
    ({
        export HOME=$tmp
        gpg --no-auto-check-trustdb --import $from.pub.asc $from.sec.asc ${^to}.pub.asc
        local recips=( --recipient\ ${^to} )
        gpg --batch --trust-model always --armor --sign --encrypt ${=recips} < $file
    } always {
        rm -r $tmp
    })
}

encrypt-file-symmetric() {
    local tmp=$(mktemp -d)
    local file=$1 passphrase=$2
    ({
        export HOME=$tmp
        gpg --batch --armor --symmetric --cipher-algo AES --passphrase $passphrase < $file
    } always {
        rm -r $tmp
    })
}

typeset -A base64keys=(
    alice     "$(generate-autocrypt-key alice@autocrypt.example)"
    bob       "$(generate-autocrypt-key bob@autocrypt.example)"
    carol     "$(generate-autocrypt-key carol@autocrypt.example)"
)

cp alice@autocrypt.example.sec.asc example-setup-message-cleartext.key
add-header-to-ascii-armor example-setup-message-cleartext.key "Autocrypt-Prefer-Encrypt: mutual"

> example-simple-autocrypt.eml << EOF
Delivered-To: <bob@autocrypt.example>
From: Alice <alice@autocrypt.example>
To: Bob <bob@autocrypt.example>
Subject: an Autocrypt header example using Ed25519+Cv25519 key
Autocrypt: addr=alice@autocrypt.example; prefer-encrypt=mutual; keydata=
${base64keys[alice]}
Date: $(date --rfc-email)
Message-ID: <$(uuidgen)@autocrypt.example>
MIME-Version: 1.0
Content-Type: text/plain

This is an example e-mail with Autocrypt header and Ed25519+Cv25519 key (key
fingerprint: ${fpr}) as defined in Level 1 revision 1.1.
EOF

> example-gossip-cleartext.eml << EOF
Autocrypt-Gossip: addr=bob@autocrypt.example; keydata=
${base64keys[bob]}
Autocrypt-Gossip: addr=carol@autocrypt.example; keydata=
${base64keys[carol]}
Content-Type: text/plain

Hi Bob and Carol,

I wanted to introduce the two of you to each other.

I hope you are both doing well!  You can now both "reply all" here,
and the thread will remain encrypted.

Regards,
Alice
EOF

gossipmsgencrypted="$(encrypt-file-to example-gossip-cleartext.eml alice@autocrypt.example bob@autocrypt.example carol@autocrypt.example)"

> example-gossip.eml << EOF
Delivered-To: <bob@autocrypt.example>
From: Alice <alice@autocrypt.example>
To: Bob <bob@autocrypt.example>, Carol <carol@autocrypt.example>
Subject: an Autocrypt Gossip header example
Autocrypt: addr=alice@autocrypt.example; prefer-encrypt=mutual; keydata=
${base64keys[alice]}
Date: $(date --rfc-email)
Message-ID: <$(uuidgen)@autocrypt.example>
MIME-Version: 1.0
Content-Type: multipart/encrypted;
 protocol="application/pgp-encrypted";
 boundary="PLdq3hBodDceBdiavo4rbQeh0u8JfdUHL"

--PLdq3hBodDceBdiavo4rbQeh0u8JfdUHL
Content-Type: application/pgp-encrypted
Content-Description: PGP/MIME version identification

Version: 1

--PLdq3hBodDceBdiavo4rbQeh0u8JfdUHL
Content-Type: application/octet-stream; name="encrypted.asc"
Content-Description: OpenPGP encrypted message
Content-Disposition: inline; filename="encrypted.asc"

${gossipmsgencrypted}

--PLdq3hBodDceBdiavo4rbQeh0u8JfdUHL--
EOF

encryptedsetupmsgtail="$(encrypt-file-symmetric example-setup-message-cleartext.key "1742-0185-6197-1303-7016-8412-3581-4441-0597" | tail -n+3)"

> example-setup-message.eml << EOF
To: alice@autocrypt.example
From: alice@autocrypt.example
Autocrypt-Setup-Message: v1
Subject: Autocrypt Setup Message
Date: $(date --rfc-email)
Content-type: multipart/mixed; boundary="Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ"

--Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ
Content-Type: text/plain

This message contains all information to transfer your Autocrypt
settings along with your secret key securely from your original
device.

To set up your new device for Autocrypt, please follow the
instuctions that should be presented by your new device.

You can keep this message and use it as a backup for your secret
key. If you want to do this, you should write down the Setup Code
and store it securely.
--Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ
Content-Type: application/autocrypt-setup
Content-Disposition: attachment; filename="autocrypt-setup-message.html"

<html><body>
<p>
This is the Autocrypt setup file used to transfer settings and
keys between clients. You can decrypt it using the Setup Code
presented on your old device, and then import the contained key
into your keyring.
</p>

<pre>
-----BEGIN PGP MESSAGE-----
Passphrase-Format: numeric9x4
Passphrase-Begin: 17

${encryptedsetupmsgtail}
</pre></body></html>
--Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ--
EOF
