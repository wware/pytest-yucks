Pytest
======

The py.test framework is very very cool. This repo is a very brief overview of py.test. I am not familiar
with its full range of features, but I like what I've seen so far.

There are [thorough docs](http://pytest.org/latest/contents.html).
One of the most powerful things about py.test is [fixtures](http://pytest.org/latest/fixture.html).
Mocking is done with [monkeypatch](http://pytest.org/latest/monkeypatch.html) (but you can still use the
`mock` module if you want). Installation is easy:
```bash
pip install pytest
```

Here are some links with general info about py.test.

* http://pythontesting.net/framework/pytest/pytest-introduction/
* http://programeveryday.com/post/pytest-more-advanced-features-for-easier-testing/
* http://thesoftjaguar.com/pres_pytest.html


Test discovery
--------------

Py.test will look for tests in modules, files, or functions whose names start with `test_`, and in classes
whose names start with `Test`, where the tests are methods whose names start with `test_`. Packages that
include tests should always have a `__init__.py` file at each directory level.

Command line options
--------------------

When a test fails, py.test can pop you into a debugger with the `--pdb` command line option.

You can also temporarily put this statement in your functional code with similar effect.
```python
    import pdb; pdb.set_trace()
```
For extra special cleverness points, put asserts in your functional code, then run `pytest --pdb` to pop
into the debugger immediately after a fault is detected to query the variables.

You can include doctests with the normal tests using the `--doctest-modules` option.

You can select tests within a file or module using `-k`, for instance

```python
py.test foo/bar/test_baz.py -k test_specific_1
```

which would run only `test_specific_1` in the `test_baz.py` file, ignoring `test_specific_2` or any other
tests in the same file. It is frequently useful to select a single test and run it repeatedly while working
on the code that it tests.

You can check the coverage of your tests using [pytest-cov](https://pytest-cov.readthedocs.org/en/latest/),
First pip-install `pytest-cov` and then using the `--cov` command line option. There are some
[useful variations](https://pytest-cov.readthedocs.org/en/latest/readme.html#usage) of this option
that you can read about.

