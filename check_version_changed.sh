#!/bin/bash
# Checks if the version of a library has changed between the current and previous commit.
# It is assumed that the version has changed when the line containing setting a version is setup.py
# (either as parameter of "setup" function or as an independent variable)
# has been changed in the last commit, when the previous commit doesn't contain setup.py
# or when there's only one commit.
#
# This won't tell if the version was changed properly (feat commits should increment minor,
# not patch version number), but can identify when the programmer skipped version bumping.
set -e

COMMIT_COUNT=$(git rev-list --count HEAD)
if [ $((COMMIT_COUNT)) -le 1 ]; then
    exit 0
fi

PREVIOUS_COMMIT_FILES=$(git ls-tree -r --name-only HEAD~1)
if ! echo -e $PREVIOUS_COMMIT_FILES | grep setup.py > /dev/null; then
    exit 0
fi

DIFF_OUTPUT=$(git diff -G"^\ *version\ ?=" HEAD~1:setup.py HEAD:setup.py)
if [ -n "$DIFF_OUTPUT" ]; then
    exit 0
else
    exit 1
fi
