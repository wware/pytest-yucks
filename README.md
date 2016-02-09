Pytest Yucks and Giggles
========================

![Funny picture](https://i1.wp.com/blog.ruberto.com/wp-content/uploads/2013/05/vaderLackofTests.jpg)

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

and about Python testing in general.

* http://docs.python-guide.org/en/latest/writing/tests/
* http://pythontesting.net/start-here/

How to think about testing
--------------------------

* Correctness
  - Tests prove that your code works as claimed.
  - Tests show how the code is to be used, what arguments to supply and what behavior or return values
    to expect back.
  - Tests ideally exercise every line of the code and every possible execution pathway thru the code.
    This is called [coverage](https://en.wikipedia.org/wiki/Code_coverage).
  - Trapeze artists ALWAYS use safety nets. Software engineers should always use tests for the same reason.
  - After your development work is done, your tests give notification if somebody else’s work somehow breaks
    your code. This is called [regression testing](https://en.wikipedia.org/wiki/Regression_testing).
  - Aim to write code that is easy to test - non-testable code is often bad code.
* Process stuff
  - Tests should run fast, so that you can conveniently re-run them constantly as you develop your code.
  - If your tests are so slow that you never want to run them, THEY WILL NOT HELP YOU and the time spent on
    them has been wasted.
  - Tests and code should be developed together: for each little piece of functionality, write a test that fails
    because the functional code isn’t written yet, then write code to satisfy the test.
* Being a team player
  - The tests you write should be a help to the QA person.

[Unit tests](https://en.wikipedia.org/wiki/Unit_testing) are for independently testing something small in
isolation (a class, or a module). Mocks are used to represent other classes, but also things like databases
or network connections or hardware, things that may be slow or unreliable. Unit tests should run very quick
and you should feel free to write LOTS of them.

[Functional](https://en.wikipedia.org/wiki/Functional_testing) or
[integration tests](https://en.wikipedia.org/wiki/Integration_testing) test larger pieces of functionality
spanning multiple classes or modules.

The economics of software testing
---------------------------------

I am a big advocate of extensive developer testing. You probably know the rationale, but just to review,
[bugs are cheaper to fix when they are caught earlier](http://faculty.ksu.edu.sa/ghazy/Cost_MSc/R6.pdf)
and often the earliest quickest way to catch them is while you are developing the code. Some bugs can be
caught while you're still just thinking about how to develop the code, but testing encourages good habits
in that phase as well.

You may be worried that writing tests will chew up valuable time in your schedule. People who do a lot of
testing find that overall, tests save time, because there are far fewer unpleasant time-consuming surprises
later on.

Mocks
-----

Mocks are an important enough topic to merit individual discussion.

They can be implemented with fixtures or with monkeypatch, or with the standard mock module, and are
used to represent anything that you aren't immediately testing. If you're testing a class or module that
ordinarily interacts with others, those others can be mocked out. You'll also want to mock out anything
that is either slow or unreliable, such as a network connection or a database. In cases where reliability
can be an issue, write tests to exercise the possible failures.

Mocks are closely related to a testing pattern called
[Dependency injection](https://en.wikipedia.org/wiki/Dependency_injection)
which ALL the cool kids are doing these days.

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

Examples
--------

The rest of this repository is a collection of simple coding exercises to illustrate various usages and
features of py.test. To run these tests, just type `./test.sh`, which will set up your virtualenv and
run the tests. It takes the same arguments as `py.test` takes.

Initially I'll just steal examples from various sources, then later I'll try to get creative and add a
few of my own.
