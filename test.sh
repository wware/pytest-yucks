#!/bin/sh

if [ ! -d venv/ ]
then
    virtualenv venv
fi

# What follows is equivalent to "source venv/bin/activate"
# See https://gist.github.com/datagrok/2199506
# The deactivate happens automatically when the script ends
export VIRTUAL_ENV=$(readlink -f venv)
export PATH="$VIRTUAL_ENV/bin:$PATH"
unset PYTHON_HOME

if [ ! -d venv/lib/python2.7/site-packages/pytest_cov ]
then
    pip install -r requirements.txt
fi

maybe_die() {
    if [ "$?" != "0" ]
    then
        echo
        echo "***OUCH*** $1"
        exit 1
    fi
}

(cd pytest_; py.test)
maybe_die "pytest tests failed"

(cd unittest_; python hack_ut.py)
maybe_die "unittest tests failed"

(cd doctest_; python foo.py)
maybe_die "doctest tests failed"

echo
echo "All tests ran OK"