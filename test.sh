#!/bin/sh

if [ ! -d venv/ ]
then
    virtualenv venv
fi

# What follows is equivalent to "source venv/bin/activate"
# See https://gist.github.com/datagrok/2199506
# The deactivate happens automatically when the script ends
export VIRTUAL_ENV=./venv
export PATH="$VIRTUAL_ENV/bin:$PATH"
unset PYTHON_HOME

if [ ! -d venv/lib/python2.7/site-packages/pytest_cov ]
then
    pip install -r requirements.txt
fi

py.test $@
