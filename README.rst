Autocrypt -- E-Mail Encryption for Everyone
===========================================

This is the source repository from which
the https://autocrypt.org website and Autocrypt specficiations are generated.

The Autocrypt Level 1 spec was created in 2019
and subsequently implemented in various MUAs
and enjoys wide active use.

The following was agreed during the OpenPGP Summit 2024 by rough consensus:

- For 2024/2025 multiple parties in the OpenPGP space are interested
  to evolve the Autofcrypt spec towards a Level 2 version.

- We close all historic issues and PRs (they remain accessible in the search).

- We implement a strict new issue/PR-creation policy (see below).


Strict Issue/PR creation policy
---------------------------------

As of June 2024, there is only a loose set of people paying attention
and caring for the Autocrypt repository.
Therefore, this respository does not invite feature suggestions
or bug reports and roughly has the following issue and PR creation policy:

**Both Issues and PRs should typically only be opened
if two parties agree on it before-hand
and assign themselves
which indicates
they are committing to caring for resolving/merging.**

You are however always warmly welcome to submit PRs
to update the website, documentation and development-status pages,
as well as the continous-integration machinery.


Working on a checkout of the autocrypt spec/pages
-------------------------------------------------

If you want to read and work on the docs locally checkout the `doc
<doc>`_ directory which contains a ``sphinx`` documentation project.
You can `install sphinx
<https://www.sphinx-doc.org/en/stable/install.html>`_ and then run
``make html`` in the ``doc`` directory to regenerate docs locally.


Implementation development repositories
---------------------------------------

For implementation development repos, see https://autocrypt.org/dev-status.html


Copyright 2016-2024, the Autocrypt team, CC0 license.
