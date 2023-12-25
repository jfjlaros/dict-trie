Development
===========

Using a :ref:`virtual environment<source-install>` is recommended.

Setup
-----

Install all dependencies required for testing.

::

    pip install -e .[test]


Tests
-----

All unittests can be run locally with the command:

::

    python -m pytest

A specific test can be run with:

::

    python -m pytest <name>

For example:

::

    python -m pytest tests/test_trie.py::TestTrie::test_empty
