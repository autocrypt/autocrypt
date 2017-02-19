
Autocrypt command line and library Python code
==============================================

This README is intended to help contributors to get setup
with running tests and using the code and "autocrypt"
command line.

testing
+++++++

To use the code and run tests you need to have installed:

- the command line client "gpg", optionally "gpg2",
  available through "gnupg" and "gnugp2" on debian.

- something to speed up gpg key creation, e.g.
  by installing "rng-tools" on debian.

- python2.7 and python3.5 if you can.
  If python3.5 is not present tests for it
  will be skipped.

- tox either installed via "pip install tox"
  or via the "python-tox" debian package.

If this is all there simply issue:

    tox

to run all the tests against the autocrypt classes
and the command line.


installation
++++++++++++

You'll need the command line client "gpg", optionally "gpg2",
available through "gnupg" and "gnugp2" on debian.

To install the autocrypt command line tool you can install
the "autocrypt" python package into your virtual environment
of choice.  If you don't know about python's virtual environments
you may just install the debian package "python-pip" and then
use "pip" to install the autocrypt library and command line too::

    $ sudo pip install autocrypt

This will install the required dependency "click", a python
framework for writing command line clients.


installation for development
++++++++++++++++++++++++++++

If you plan to work/modify the sources and have
a github checkout we strongly recommend to create
and activate a python virtualenv and then once use
**pip without sudo in edit mode**::

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -e .

Changes you subsequently make to the sources will be
available without further installing the autocrypt
package again.


running the command line
++++++++++++++++++++++++

After _installation simply run the main command::

    autocrypt

to see available sub commands and options.  Start by
initializing an Autocrypt account which will maintain
its own keyring and not interfere with your possibly
existing gpg default keyring::

    $ autocrypt init

Afterwards you can create an autocrypt header
for an email address::

    $ autocrypt make-header x@example.org

You can process and integrate peer's Autocrypt
keys by specifying an email message filename::

    $ autocrypt process-incoming EMAIL_MESSAGE_FILE

At any point you can show the status of your autocrypt
account::

    $ autocrypt show
