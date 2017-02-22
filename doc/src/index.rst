
Autocrypt Python Reference tool and implementation
==================================================

.. note::

    The autocrypt reference tool is as much in development
    as the spec itself.  Until we have a 1.0 release
    everything is subject to change.

.. toctree::

   cmdline
   api

.. _installation:

Installation
------------

You need the python package installer "pip".  If you
don't have it you can install it on Debian systems::

    sudo apt-get install python-pip

And now you can install the autocrypt package::

    pip install --user autocrypt

And then make sure that ``~/.local/bin`` is contained
in your ``PATH`` variable.

installation for development
----------------------------

If you plan to work/modify the sources and have
a github checkout we recommend to create and activate
a python virtualenv and issue **once**::

    $ cd src
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -e .

This creates a virtual python environment
in the "src/venv" directory and activates it for your
shell through the ``source venv/bin/activate`` command.

Changes you subsequently make to the sources will be
available without further installing the autocrypt
package again.
