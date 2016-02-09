import datetime
import os
import warnings

import pytest


def multiply(x, y):
    """
    Start with a trivial function to test.
    """
    return x * y


def test_mult_3_4():
    """
    Some trivial tests
    """
    assert multiply(3, 4) == 12
    assert multiply(2, 19) != 12


@pytest.mark.xfail    # comment this line out to try the pdb hack
def test_known_failure():
    """
    This test will intentionally fail. If you run "py.test --pdb", you'll
    pop into a PDB session where you can examine the variables x and y and
    see that they are unequal.
    """
    x = multiply(3, 4)
    y = 19
    assert x == y, "Expected failure because 3 * 4 is not 19"


#############################################################
#                                                           #
#             Exceptions and expected failures              #
#                                                           #
#############################################################


def divide(x, y):
    """
    We can get in trouble here with a zero denominator.
    """
    return x / y


def test_division():
    """
    Be sure to test what happens with a zero denominator.
    """
    assert divide(42, 6) == 7
    assert divide(3.0, 4) == 0.75
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_recursion_depth():
    """
    Another example of an expected failure.
    """
    with pytest.raises(RuntimeError) as excinfo:
        def f():
            f()
        f()
    assert str(excinfo.value) == 'maximum recursion depth exceeded'


@pytest.mark.xfail(raises=NameError)
def test_never_defined():
    """
    One of the built-in fixtures is pytest.mark.xfail, which is used to
    indicate an expected failure that we want to ignore. We can optionally
    say what kind of failure we expect.
    """
    never_defined()


def test_warning():
    """
    We can also say we expect a warning. Warnings are new to me.
    """
    x = 1
    with pytest.warns(UserWarning):
        warnings.warn("The owls are not what they seem.", UserWarning)
        """
        warnings.warn is not raise, so we continue to run code afterwards.
        """
        x = 2
    assert x == 2


#############################################################
#                                                           #
#                      Py.test fixtures                     #
#                                                           #
#############################################################


def do_stuff_with_file(fileobj):
    """
    Text processing (even trivial) is a good example to show how fixtures
    can mock things that may be slow or may fail.
    """
    return 'py.test' in fileobj.read()


def test_with_file():
    assert do_stuff_with_file(open('README.md')) is True


def test_with_non_existent_file():
    with pytest.raises(IOError) as excinfo:
        assert do_stuff_with_file(open('Mahabharata.md')) is True
    assert "No such file or directory" in str(excinfo.value)


@pytest.fixture
def mock_open():
    """
    A mock for pretending to open an ordinary text file.
    """
    class Foo(object):
        def __call__(self, filename):
            return self

        def read(self):
            return 'Everybody loves py.test just heaps and heaps!'
    return Foo()


def test_with_mock_open(mock_open):
    """
    Let's use the open-file mock in a test.
    """
    assert do_stuff_with_file(mock_open("README.md")) is True


@pytest.fixture
def mock_open_missing():
    """
    A mock for pretending to try to open a non-existent file.
    """
    class Foo(object):
        def __call__(self, filename):
            raise IOError("[Errno 2] No such file or directory: 'Mahabharata.md'")
    return Foo()


def test_with_missing_mock(mock_open_missing):
    """
    Let's use the open-missing-file mock in a test.
    """
    with pytest.raises(IOError) as excinfo:
        assert do_stuff_with_file(mock_open_missing("Mahabharata.md")) is True
    assert "No such file or directory" in str(excinfo.value)


@pytest.fixture(scope='module')
def some_dumb_resource(request):
    """
    Because of the scope='module' argument, this setup is done only once for each
    module being tested. If you omit it, the setup-teardown will be done for each
    test case. Scope can be by session, module, class, or function, the default being
    function.

    The request argument uses one of py.test's built-in fixtures to set up the teardown.
    """
    print "Set up some dumb resource"   # do some stuff
    """
    If you don't need a teardown, you can skip the rest of this, and remove the
    request argument above.
    """
    def some_dumb_resource_teardown():
        """
        This finalizer will perform the teardown operation matchine the setup
        operation above.
        """
        print "Tear down some dumb resource"     # undo some stuff
    request.addfinalizer(some_dumb_resource_teardown)


def test_setup_and_teardown(some_dumb_resource):
    assert some_dumb_resource is None


#############################################################
#                                                           #
#                   Parameterized fixtures                  #
#                                                           #
#############################################################


@pytest.fixture(params=[
    # tuple with (input, expectedOutput)
    (3, 4, 5, True),    # legitimate Pythagorean triplets
    (5, 12, 13, True),
    (8, 15, 17, True),
    (7, 24, 25, True),
    (1, 2, 3, False),    # bogus Pythagorean triplets
    (6, 7, 10, False),
    (105, 110, 130, False),
    (600, 800, 1001, False)
])
def test_data(request):
    return request.param


def valid_pythagorean_triplet(a, b, c):
    return (a ** 2 + b ** 2) == c ** 2


def test_pythagorean(test_data):
    a, b, c, legit = test_data
    assert valid_pythagorean_triplet(a, b, c) == legit


@pytest.mark.parametrize('input, expected, legit', [
    ('2 + 3', 5, True),
    ('6 - 4', 2, True),
    ('5 + 2', 8, False)    # 5 + 2 != 8
])
def test_python_eval1(input, expected, legit):
    assert (eval(input) == expected) == legit


@pytest.mark.parametrize('input, expected', [
    ('2 + 3', 5),
    ('6 - 4', 2),
    pytest.mark.xfail(('5 + 2', 8))
])
def test_python_eval2(input, expected):
    """Another approach"""
    assert eval(input) == expected


#############################################################
#                                                           #
#                         Monkeypatch                       #
#                                                           #
#############################################################


def getssh():
    return os.path.join(os.path.expanduser("~admin"), '.ssh')


def test_mytest(monkeypatch):
    """
    If you have multiple arguments to your test, monkeypatch should always
    be the last arg. Also see
    http://pytest.org/latest/monkeypatch.html
    """
    def mockreturn(path):
        return '/abc'
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)
    x = getssh()
    assert x == '/abc/.ssh'


FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 05, 55)


@pytest.fixture
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME
    monkeypatch.setattr(datetime, 'datetime', mydatetime)


def test_patch_datetime(patch_datetime_now):
    assert datetime.datetime.now() == FAKE_TIME
