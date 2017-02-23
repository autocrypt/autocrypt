
Autocrypt command line docs
===========================


getting started, playing around
-------------------------------

After :ref:`installation` let's see what sub commands we have::

    $ autocrypt
    Usage: autocrypt [OPTIONS] COMMAND [ARGS]...

      access and manage Autocrypt keys, options, headers.

    Options:
      --basedir PATH  directory where autocrypt account state is stored
      --version       Show the version and exit.
      -h, --help      Show this message and exit.

    Commands:
      init                init autocrypt account state.
      status              print account state including those of peers.
      make-header         print autocrypt header for an emailadr.
      set-prefer-encrypt  print or set prefer-encrypted setting.
      process-incoming    process incoming mail from file/stdin.
      export-public-key   print public key of own or peer account.
      export-secret-key   print secret key of own autocrypt account.

initializing an autocrypt account::

    $ autocrypt init
    /tmp/home/.config/autocrypt: account 89a7329750454bbe9f319a77b64f6acb created
    account-dir: /tmp/home/.config/autocrypt
    uuid: 89a7329750454bbe9f319a77b64f6acb
    own-keyhandle: 38D055C7FC7EB7A8
    prefer-encrypt: notset
    gpgbin: gpg [currently resolves to: /usr/bin/gpg]
    gpgmode: own

This created a secret key and assigns a UUID to your
account.  With this setup Autocrypt maintains all its state
and does all its file system modifications inside an application
default directory, on linux often ``~/.config/autocrypt``. If you
rather like autocrypt to use your system keyring so that all incoming
keys are available there, see init_system_.

Let's check out account status::

    $ autocrypt status
    account-dir: /tmp/home/.config/autocrypt
    uuid: 89a7329750454bbe9f319a77b64f6acb
    own-keyhandle: 38D055C7FC7EB7A8
    prefer-encrypt: notset
    gpgbin: gpg [currently resolves to: /usr/bin/gpg]
    gpgmode: own

This shows our own keyhandle of our Autocrypt OpenPGP key.

Let's generate a static email Autocrypt header which
you could add to your email configuration (substitute
``a@example.org`` with your email address)::

    $ autocrypt make-header a@example.org
    Autocrypt: to=a@example.org; key=mQENBFiut7QBCADiop7dDa2FVesj3LMlozunBul1IEN/QASAfVR7qM5V6tS8O70Yp5QQEhToDY2JMfWVrRfezbhzvHkbWeMSe8F29wWpCZSyqE9YRuVzoLIooZlHAq732us0HuXeZDVrQbjjRX1RNZUiOAnFZM+ztit/k57G1eOXE3ZLKMuxrpSnsNPa1RaCGPdm4f/NmhSbTRKzVDLOIXCFIun1/JECZtf+h6vdA6Vti/+G63VC4fV5xnrG2UKfUr9dF/ztJvEkmWUJiJm+3ghqd/W9S6EC3ugMH+HaG3K9EwAdai6ORCXj2piMELTK4zIPpjXaTqNroGRAeuXQvMLNRO//JyMx/O7HABEBAAG0IyA8ODlhNzMyOTc1MDQ1NGJiZTlmMzE5YTc3YjY0ZjZhY2I+iQE4BBMBAgAiBQJYrre0AhsDBgsJCAcDAgYVCAIJCgsEFgIDAQIeAQIXgAAKCRA40FXH/H63qLejB/9PayniQNI9Z1ibcHkRt4IOEvGfUslkv8WCv8wC7po07IKPAOGbo5NPH5zE+0NUdhxDzpRi7zmuZya27GmBM3wokvw8HEziWAQNrIqJZMr+u3C3SQ05IfOpY4Zc1yLc7J6/YKyJQnAFUYoRvJuTwOIV24VmW41iIfm6dyXWp6Wp9l2GHamrTGzkTyRKmmCDG1XlWUhKqDQ3PTySyJvxZwJc34wOfSHgtysQKB4rO88QvMBi4pfz1IhTzMgd1GxbK0IQIS0BFjZaG8siCqvxGGtIZXEeZa4pyu7DJrtoMtX4qYrKbEb7Y5cT51OoyejVn0ncw+BVinfpwv8uzY0l2gh4uQENBFiut7QBCADbJ6B0eMWArox2JtiTwLoB+METoWDLFFNXHV4VXRhyXE1ymfp8m8gIFwcpH+UDjf1wZrkwloI19yrF1Hk6RrmHq4Rm2oA1HCzBcn6jpCKdkKLCR1cbUAQuKXygQ85beY5/NAupgKSbLXHtNXnGZqY8XoEY8U4G7Abp1EoWxLfuReSz+eIhLNoh1UdR6WSDP8MSJ1EKNNTK+s+zTl68Xx1futR6lGKpM7C/uYlnHHzSJKE+JIezBTcxSmq7Iyf81NxHCIZ35mIRztploYPYBl+KHgdUs3bSg6keZtHXACLG1AQBsuJtj76AiVSxTOxjXuNmWtf71jl79rlKfeEBc5npABEBAAGJAR8EGAECAAkFAliut7QCGwwACgkQONBVx/x+t6i32wgAzoDO8XEgfoMYw7jja3VvoW9sKP+G3KxbAOXYryZCcRoP/js9eb7VwOreHzULaDWxsaJTJcVUQDaAqEb09yjQNWP+cmYG4furzsJNi4pO4scAYEUKH+S6eGVlg1crcXr4jI4kr3v871MsIgaRnOmi1ok0DQ55/w65moYM9ql1vmWxS/vAZA34QAQs8dQu1Fnat4WUOv/Wry5DdAVAREkfpwsagzLMGJTPL1GNCmJPIF2ReOaFk8HUTxQGAOSNpsiR0cjIXlbMV3ygWLk90uLOcxy1f5Kiw5kXwRoNP3nZaUNmGmhIF25BFYl3LKma6DksW+ggNbsP2a8D6+kyGUFtHA==

Getting our own public encryption key in armored format::

    $ autocrypt export-public-key
    -----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v1

    mQENBFiut7QBCADiop7dDa2FVesj3LMlozunBul1IEN/QASAfVR7qM5V6tS8O70Y
    p5QQEhToDY2JMfWVrRfezbhzvHkbWeMSe8F29wWpCZSyqE9YRuVzoLIooZlHAq73
    2us0HuXeZDVrQbjjRX1RNZUiOAnFZM+ztit/k57G1eOXE3ZLKMuxrpSnsNPa1RaC
    GPdm4f/NmhSbTRKzVDLOIXCFIun1/JECZtf+h6vdA6Vti/+G63VC4fV5xnrG2UKf
    Ur9dF/ztJvEkmWUJiJm+3ghqd/W9S6EC3ugMH+HaG3K9EwAdai6ORCXj2piMELTK
    4zIPpjXaTqNroGRAeuXQvMLNRO//JyMx/O7HABEBAAG0IyA8ODlhNzMyOTc1MDQ1
    NGJiZTlmMzE5YTc3YjY0ZjZhY2I+iQE4BBMBAgAiBQJYrre0AhsDBgsJCAcDAgYV
    CAIJCgsEFgIDAQIeAQIXgAAKCRA40FXH/H63qLejB/9PayniQNI9Z1ibcHkRt4IO
    EvGfUslkv8WCv8wC7po07IKPAOGbo5NPH5zE+0NUdhxDzpRi7zmuZya27GmBM3wo
    kvw8HEziWAQNrIqJZMr+u3C3SQ05IfOpY4Zc1yLc7J6/YKyJQnAFUYoRvJuTwOIV
    24VmW41iIfm6dyXWp6Wp9l2GHamrTGzkTyRKmmCDG1XlWUhKqDQ3PTySyJvxZwJc
    34wOfSHgtysQKB4rO88QvMBi4pfz1IhTzMgd1GxbK0IQIS0BFjZaG8siCqvxGGtI
    ZXEeZa4pyu7DJrtoMtX4qYrKbEb7Y5cT51OoyejVn0ncw+BVinfpwv8uzY0l2gh4
    uQENBFiut7QBCADbJ6B0eMWArox2JtiTwLoB+METoWDLFFNXHV4VXRhyXE1ymfp8
    m8gIFwcpH+UDjf1wZrkwloI19yrF1Hk6RrmHq4Rm2oA1HCzBcn6jpCKdkKLCR1cb
    UAQuKXygQ85beY5/NAupgKSbLXHtNXnGZqY8XoEY8U4G7Abp1EoWxLfuReSz+eIh
    LNoh1UdR6WSDP8MSJ1EKNNTK+s+zTl68Xx1futR6lGKpM7C/uYlnHHzSJKE+JIez
    BTcxSmq7Iyf81NxHCIZ35mIRztploYPYBl+KHgdUs3bSg6keZtHXACLG1AQBsuJt
    j76AiVSxTOxjXuNmWtf71jl79rlKfeEBc5npABEBAAGJAR8EGAECAAkFAliut7QC
    GwwACgkQONBVx/x+t6i32wgAzoDO8XEgfoMYw7jja3VvoW9sKP+G3KxbAOXYryZC
    cRoP/js9eb7VwOreHzULaDWxsaJTJcVUQDaAqEb09yjQNWP+cmYG4furzsJNi4pO
    4scAYEUKH+S6eGVlg1crcXr4jI4kr3v871MsIgaRnOmi1ok0DQ55/w65moYM9ql1
    vmWxS/vAZA34QAQs8dQu1Fnat4WUOv/Wry5DdAVAREkfpwsagzLMGJTPL1GNCmJP
    IF2ReOaFk8HUTxQGAOSNpsiR0cjIXlbMV3ygWLk90uLOcxy1f5Kiw5kXwRoNP3nZ
    aUNmGmhIF25BFYl3LKma6DksW+ggNbsP2a8D6+kyGUFtHA==
    =/gWy
    -----END PGP PUBLIC KEY BLOCK-----


.. _init_system:

initializing with key in system key ring
----------------------------------------

If you want to use autocrypt with an existing mail setup you
can initialize by specifying an existing key in your system
gpg or gpg2 key ring.  To present a fully self-contained example
let's create a standard autocrypt key with gpg::

    # content of autocrypt_key.spec

    Key-Type: RSA
    Key-Length: 2048
    Key-Usage: sign
    Subkey-Type: RSA
    Subkey-Length: 2048
    Subkey-Usage: encrypt
    Name-Email: test@autocrypt.org
    Expire-Date: 0

Let's run gpg to create the key::

    $ gpg --batch --gen-key autocrypt_key.spec
    gpg: keyring `/tmp/home/.gnupg/secring.gpg' created
    gpg: keyring `/tmp/home/.gnupg/pubring.gpg' created
    +++++
    .....+++++
    ..+++++
    ...............+++++
    gpg: /tmp/home/.gnupg/trustdb.gpg: trustdb created
    gpg: key FE8447A5 marked as ultimately trusted

We can now try initialize autocrypt using the just generated key::

    $ autocrypt init --use-existing-key test@autocrypt.org
    account 89a7329750454bbe9f319a77b64f6acb exists at /tmp/home/.config/autocrypt and --replace was not specified

Oh, the previous autocrypt init state is still there.  Let's replace it::

    $ autocrypt init --replace --use-existing-key test@autocrypt.org
    deleting account directory: /tmp/home/.config/autocrypt
    /tmp/home/.config/autocrypt: account 1fee5e74d6a643f5962d649489150171 created
    account-dir: /tmp/home/.config/autocrypt
    uuid: 1fee5e74d6a643f5962d649489150171
    own-keyhandle: 66AE5A5DFE8447A5
    prefer-encrypt: notset
    gpgbin: gpg [currently resolves to: /usr/bin/gpg]
    gpgmode: system

Success! We now have an initialized autocrypt account which will store
Autocrypt keys from incoming mails in the system key ring.
