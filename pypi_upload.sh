#!/bin/bash
# Build the library and sends it to PyPI with Twine.
# Takes one parameter: PyPI repo name from pypirc.
# Requires one environment variable: password to PyPI repo.

set -ev

COMMIT_ACTION_SCRIPT=$(dirname $0)/get_commit_action.sh
COMMIT_ACTION=$($COMMIT_ACTION_SCRIPT)

if [ $COMMIT_ACTION == build_code ]; then
    python3 setup.py sdist bdist_wheel
    TWINE_ACTION=upload
else
    python3 setup.py sdist
    TWINE_ACTION=register
fi

PYPIRC=$(dirname $0)/pypirc
twine $TWINE_ACTION -r $1 -p $PYPI_PASSWORD --config-file $PYPIRC dist/*

