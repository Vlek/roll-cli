Roll-cli
====

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

|Asciinema|

.. |PyPI| image:: https://img.shields.io/pypi/v/roll-cli.svg
   :target: https://pypi.org/project/roll-cli/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/roll-cli.svg
   :target: https://pypi.org/project/roll-cli/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/roll-cli
   :target: https://pypi.org/project/roll-cli
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/roll-cli
   :target: https://opensource.org/licenses/GPL-3.0
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/roll-cli/latest.svg?label=Read%20the%20Docs
   :target: https://roll-cli.readthedocs.io/
   :alt: Read the documentation at https://roll-cli.readthedocs.io/
.. |Tests| image:: https://github.com/vlek/roll-cli/workflows/Tests/badge.svg
   :target: https://github.com/vlek/roll-cli/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/vlek/roll-cli/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/vlek/roll-cli
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black
.. |Asciinema| image:: https://asciinema.org/a/URGcrvqF0ahiBSHWXx5ZcLwBS.svg
   :target: https://asciinema.org/a/URGcrvqF0ahiBSHWXx5ZcLwBS
   :alt: Asciinema usage example


Features
--------

Dice roller CLI Script

Makes it easy to roll dice via command line and is able handle the basic math functions, including parens!

Feature-packed, including:

- Basic math functions
- Dice rolling with variable sides and number of dice
- Correct order of operations (with some liberty taken for where to put dice notation)
- Verbose printing to see what each individual dice roll was
- Ability to roll the minimum or maximum for each roll
- Keep notation, specify the number of dice whose value you would like to keep, discarding the rest


Requirements
------------

- Python >=3.7
- While not required, Pipx helps manage package dependencies and ensure that they do not conflict.


Installation
------------

You can install *Roll* via pipx_ from PyPI_:

.. code:: console

   $ pipx install roll-cli


Usage
-----

After installation, the `roll` command is then made globally available.

.. code:: console

   $ roll
   8

   $ roll 4d6
   14

   $ roll 10d6K3 -v
   Rolled: 10d6: [2, 5, 5, 4, 2, 4, 3, 5, 3, 6]
   Keeping highest: 3: [5, 5, 6]
   16

Please see the `Command-line Reference <Usage_>`_ for further details.


Contributing
------------

This is just a fun learning project for me, so I am trying to do all the work myself.
If you believe that there are features that I should incorporate, please do not hesitate to create a feature request.

To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `GPL 3.0 license`_,
*Roll* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

.. image:: https://avatars.githubusercontent.com/u/15008772?v=4
   :target: https://github.com/vlek
   :alt: Vlek
   :width: 100

All coding is done by `@vlek`_.

This project uses `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@vlek: https://github.com/vlek
.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _GPL 3.0 license: https://opensource.org/licenses/GPL-3.0
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/vlek/roll-cli/issues
.. _pipx: https://pypa.github.io/pipx/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://roll-cli.readthedocs.io/en/latest/usage.html
