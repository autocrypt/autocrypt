
Autocrypt Python Reference tool and implementation
==================================================

.. note::

    The autocrypt reference tool is as much in development
    as the spec itself.  Until we have a 1.0 release
    everything is subject to change.

.. contents::

Installing
----------

You need the python package installer "pip".  If you
don't have it you can install it on Debian systems::

    sudo apt-get install python-pip

And now you can install the autocrypt package::

    pip install --user autocrypt

And then make sure that ``~/.local/bin`` is contained
in your ``PATH`` variable.

Quickstart usage
----------------

To get started you initialize your Autocrypt account::

    $ autocrypt init
    account 94274410e1024c3aabc8dbc221900aab exists at /home/hpk/.config/autocrypt and --replace was not specified

This creates a secret key and assigns a UUID to your
account.  Autocrypt maintains all its state and does
all its file system modifications inside an application
default directory, e.g. ``~/.config/autocrypt``.

If you want to generate a static email Autocrypt header which
you can add to your email configuration, substitute
``a@example.org`` with your email address when typing::

    $ autocrypt make-header a@example.org
    Autocrypt: to=MY_EMAIL_ADDRESS; key=mQENBFinTNMBCADFjy143jmsH0Vfv5gFG2/OcQk2Q1ew6Yrkbx3Hh8L+jYijyBnS4gmUMbCkBFucSA9nBuFilaBYVFGzC+TlDIvS9jehxf8oIRDZ9yRAw7e0d1SdlQ9PqQhsxf2E/Ej2N+5ccKUmh3untG09I50l1RzzbcflaRXyqdpelFzlTn0X8Bnhh0DgRHoPwhuVT3AClx7sq2bvBwH6eYvT3KbWPP1q2aaXjY/VdATQ2W/PbZ2ZRJZLbHXqOlrjwg3EWC/ks5xYIZmrMU0xMMVMvOd1LdBDYyKxZq8XHNHzaF/PMl4ndmSIa4IkCD1ZT9EPheVmf8MnzNecll+sGjWemS7WRN7LABEBAAG0IyA8OTQyNzQ0MTBlMTAyNGMzYWFiYzhkYmMyMjE5MDBhYWI+iQE4BBMBAgAiBQJYp0zTAhsDBgsJCAcDAgYVCAIJCgsEFgIDAQIeAQIXgAAKCRA7A5HNPkxHmp7nCACBtrKPefIKx4xTy4WoQqfpMvqFE9E4hGKlu/FrZfwkEHAu2onLKFkHqjYyXhwWMMFrFRBk/WkYib+XITGt9s0MiKUgxjPfXyNcstXUoQnvQP5a+Nd/k5J+NVejii5xIhE1sVKPYw0Z/PXJ/+8pGXXNWkpsUczyAnsABs3Mn4oUpAXpWmnWsoLZRK/iwUw6GdGDVYfYlAq45zl1K4x20vtDlmSNc+Sg4G0U7dxsjZ0XMjoM0DwSee6+W53uoKuvMcFXvZgQonJJmf9ecACHPQcsVI582QVFwoUmVjgmT9D1EsspbcbL/VSPoqxPuwWUJcwuH9XR1KqhNvLb0Fu9QxCfuQENBFinTNMBCADXPXUc4ArbO841IhsIQv/nRzDqdfxckAFVtZ5hF80nC1TcvVX2IdLCMSPkpULk3ZcBlT2OkHH1E/Z94ob+wucV7AbmJH+ou8Xt5LqnCrp0AYFF4U+7+ogOa+Y0sa0jLjTnacBN9G5u8YOiUDkaxO40J2O56vndz2JXHQXj8G35O1vUDPMlJgd4Z8YgktDExVSvtg12cTUPo4ry4k7iuT+tT34MPIVwic3kFP23s4qjksq7DkKOBhdEeheJg8cYFlLd+KZ33Iit6uWE3N9UuLwQHRhoSn5nrg0WAkZWJT6fYba6AzDNvrYSG8nFxDiNCZETOrhgWuUWelrPESbTe6ZrABEBAAGJAR8EGAECAAkFAlinTNMCGwwACgkQOwORzT5MR5pP/gf8DQzZEpFMIAEmi1Eq8R+KerHhi/rhoGfcZ3QhYtv0JInE8R4P1TeYcqc/8+vOigDJ6uTcmFyy1nqVOGIzbkENIC5FmxH01vswH0Hd9cXCdxlL3ekpLlJ2Q//Euv4LaD7AcBB19HMdRD/Yq68OgawUz9UD7I2tPJsHPDDP+o1MEhy5JV9GK3sPmTYAAOQNWNTgfk8UgGGX9QAnCVXK3CgwUv39twbFuMEvoyr+UiDx8RDgHba78NXE+Fu75a6yx4TqeFglxukCRvvie4LTHBCzdmAFn31E+C2UpaIRHeEAa/iHqB9Mw8zsMNvWO5GA422K2cOjDO7dEcpjIFTLJElwUA==

