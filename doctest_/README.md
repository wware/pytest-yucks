Doctest
=======

The doctest module searches for pieces of text that look like interactive
Python sessions in docstrings, and then executes those sessions to verify that
they work exactly as shown.

Doctests have a different use case than proper unit tests: they are usually
less detailed and don’t catch special cases or obscure regression bugs. They
are useful as an expressive documentation of the main use cases of a module and
its components. However, doctests should run automatically each time the full
test suite runs.
