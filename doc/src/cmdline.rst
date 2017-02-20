
Autocrypt command line docs
===========================

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
    /tmp/home/.config/autocrypt: account ccf4c0fe6cc9429c87bf28b9a6945793 created

This created a secret key and assigns a UUID to your
account.  Autocrypt maintains all its state and does
all its file system modifications inside an application
default directory, on linux often ``~/.config/autocrypt``.

Let's check out account status::

    $ autocrypt status
    account-dir: /tmp/home/.config/autocrypt
    uuid: ccf4c0fe6cc9429c87bf28b9a6945793
    own-keyhandle: 9DCB7DC93829FDCE
    prefer-encrypt: notset

This shows our own keyhandle of our Autocrypt OpenPGP key.

Let's generate a static email Autocrypt header which
you can add to your email configuration (substitute
``a@example.org`` with your email address)::

    $ autocrypt make-header a@example.org
    Autocrypt: to=a@example.org; key=mQENBFiq1kYBCAC7UHdpZcyNAftWQEievO76d5cNg0q7sFhaI5nC0hqRp4V31coKgWOV+TJhPoITnnUiwP8z3eRovq+mDbDWA0BDoQfgm6gvfxQXcY6WBcRjYrj7ZtIJQHbjazzATCkrApcFEHqeXHCiCNmPajMDxadFncB6Sii3I/SK8uNg/mU5Qk6nM8gqI8DXQloOWCyEU1RsaAQR21mEbOp83feCpX7pIHSJqpDD85VLo1J+FIj5Hj+4BGtWOsVVVJOzMv9qrjByw0upIGnn7G3DFp420R3pxWf6kz62Z7TNKJgx7vaq7xJb492yDdZCWCle4xinK6cA+xiXBuYfAfgQerGk9opdABEBAAG0IyA8Y2NmNGMwZmU2Y2M5NDI5Yzg3YmYyOGI5YTY5NDU3OTM+iQE4BBMBAgAiBQJYqtZGAhsDBgsJCAcDAgYVCAIJCgsEFgIDAQIeAQIXgAAKCRCdy33JOCn9zjjDB/0QQkaTykC/qcTKnarhZuz2nWdLuBEmwJqBs/pNEyPu32v7TBhLk+jbShZhaphnCvyWYTL5bZ44+5EyPI+HQnCAMSbydsXk97o8Sin7IzMuDU5PoD4SyXYTBtiDupb+sypPAXz8pLaK6tM6BbXWFGecu3FSSg6f+eE5rjPaRHX6Ogx89W3viVkSESbcVWIelP8Ms0VCNnEoCtqGgoJZfskDukevUC8bkndSZii+6/+rCu9kl1LazO61VhrevIxrnLQIShqmDGKi0a5rzAm6CpHeXSkBpHouRjx9w+WtyJNeJ+2mx0bKJFha/GggDmcgeOpAHX1Jd4D1CVTxmzIuJgGuuQENBFiq1kYBCADKlqC1odX1qFO0iU4SBcsZ/MBxIJ4fMagaZ+RVYY/o2AocQs5g7Y5unntAScl6jPmBKLHH8CGrnudMDSVxvyJ+4N/2SGiH2UMKMWePORR5MDq/Gt4H93aUI+G+EvDWnbF2IMEEMmhvv9vgqTqqFDM7QSNThcvwWlHB/rW0C6WoZ2NqqCEjUZdLDQ0a9BXErJK+nf8hVOCMuJL79DSU27GfPoXUvkIUCO219OXLlH5toOcSAkxeFy2qe5bLD22QzxJtZiKymQEEii+RNE2aPzzcGvCBl3D7GRTZIAFT0849WUXQJsNz5JowhFiOAjKjdxcn0HvECGA4M7XyvfktR1s7ABEBAAGJAR8EGAECAAkFAliq1kYCGwwACgkQnct9yTgp/c44igf+LGqL00unwoh4wMnXMGC55C4lDQ54YKDAf0MQhxT09UMCsCLkFle4C2PWGH6CeJhE1x7sz0oDlPYlqn+A7Op03pgPwEbBWrY0eH9IhcyYUZD9xN6VeH5kHID8OwJxGAejCeaWWt3eS+kEm5KkTjO9RvgMMkNtBAwuhge/AdDj6WHQXahiDfXrZJNyN01Dp2mWXH6Xu3NCN0CapVOpPvyWD/aV04Lkrv9pKddaBRAAj8T9pW2omc2tHgbteOgylh9L7YUj6ZMgQtpML7AEg3R17ydBiA7vqtp/LAW3trJBvRmc1TPq7N/RzdSfHecpuorSZa2QSLCccVDPA9EVU3j3gA==

Getting our own public encryption key in armored format::

    $ autocrypt export-public-key
    -----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v1
    
    mQENBFiq1kYBCAC7UHdpZcyNAftWQEievO76d5cNg0q7sFhaI5nC0hqRp4V31coK
    gWOV+TJhPoITnnUiwP8z3eRovq+mDbDWA0BDoQfgm6gvfxQXcY6WBcRjYrj7ZtIJ
    QHbjazzATCkrApcFEHqeXHCiCNmPajMDxadFncB6Sii3I/SK8uNg/mU5Qk6nM8gq
    I8DXQloOWCyEU1RsaAQR21mEbOp83feCpX7pIHSJqpDD85VLo1J+FIj5Hj+4BGtW
    OsVVVJOzMv9qrjByw0upIGnn7G3DFp420R3pxWf6kz62Z7TNKJgx7vaq7xJb492y
    DdZCWCle4xinK6cA+xiXBuYfAfgQerGk9opdABEBAAG0IyA8Y2NmNGMwZmU2Y2M5
    NDI5Yzg3YmYyOGI5YTY5NDU3OTM+iQE4BBMBAgAiBQJYqtZGAhsDBgsJCAcDAgYV
    CAIJCgsEFgIDAQIeAQIXgAAKCRCdy33JOCn9zjjDB/0QQkaTykC/qcTKnarhZuz2
    nWdLuBEmwJqBs/pNEyPu32v7TBhLk+jbShZhaphnCvyWYTL5bZ44+5EyPI+HQnCA
    MSbydsXk97o8Sin7IzMuDU5PoD4SyXYTBtiDupb+sypPAXz8pLaK6tM6BbXWFGec
    u3FSSg6f+eE5rjPaRHX6Ogx89W3viVkSESbcVWIelP8Ms0VCNnEoCtqGgoJZfskD
    ukevUC8bkndSZii+6/+rCu9kl1LazO61VhrevIxrnLQIShqmDGKi0a5rzAm6CpHe
    XSkBpHouRjx9w+WtyJNeJ+2mx0bKJFha/GggDmcgeOpAHX1Jd4D1CVTxmzIuJgGu
    uQENBFiq1kYBCADKlqC1odX1qFO0iU4SBcsZ/MBxIJ4fMagaZ+RVYY/o2AocQs5g
    7Y5unntAScl6jPmBKLHH8CGrnudMDSVxvyJ+4N/2SGiH2UMKMWePORR5MDq/Gt4H
    93aUI+G+EvDWnbF2IMEEMmhvv9vgqTqqFDM7QSNThcvwWlHB/rW0C6WoZ2NqqCEj
    UZdLDQ0a9BXErJK+nf8hVOCMuJL79DSU27GfPoXUvkIUCO219OXLlH5toOcSAkxe
    Fy2qe5bLD22QzxJtZiKymQEEii+RNE2aPzzcGvCBl3D7GRTZIAFT0849WUXQJsNz
    5JowhFiOAjKjdxcn0HvECGA4M7XyvfktR1s7ABEBAAGJAR8EGAECAAkFAliq1kYC
    GwwACgkQnct9yTgp/c44igf+LGqL00unwoh4wMnXMGC55C4lDQ54YKDAf0MQhxT0
    9UMCsCLkFle4C2PWGH6CeJhE1x7sz0oDlPYlqn+A7Op03pgPwEbBWrY0eH9IhcyY
    UZD9xN6VeH5kHID8OwJxGAejCeaWWt3eS+kEm5KkTjO9RvgMMkNtBAwuhge/AdDj
    6WHQXahiDfXrZJNyN01Dp2mWXH6Xu3NCN0CapVOpPvyWD/aV04Lkrv9pKddaBRAA
    j8T9pW2omc2tHgbteOgylh9L7YUj6ZMgQtpML7AEg3R17ydBiA7vqtp/LAW3trJB
    vRmc1TPq7N/RzdSfHecpuorSZa2QSLCccVDPA9EVU3j3gA==
    =wwk8
    -----END PGP PUBLIC KEY BLOCK-----
    
