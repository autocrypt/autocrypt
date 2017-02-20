""" helper to generate html and autodoc python docs with a temporary
virtualenv where we install the sources in edit mode.
"""
from __future__ import unicode_literals
import os
import sys
import subprocess


if __name__ == "__main__":
    venvdir = sys.argv[1]
    bindir = os.path.join(venvdir, "bin")
    assert venvdir
    if not os.path.exists(venvdir):
        subprocess.check_call(["virtualenv", venvdir])

        # poor people's virtualenv activate
        os.environ["PATH"] = bindir + os.pathsep + os.environ["PATH"]

        subprocess.check_call(["pip", "install", "-e", "../src"])

    sys.exit(subprocess.call(sys.argv[2:]))
