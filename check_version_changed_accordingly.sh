#!/bin/bash
# Returns 0 if the library's version changed (or not) according to the last commit type.
# Returns 1 otherwise.
# Version should change on "feat", "fix", "refactor" and "perf" commits.
#
# This script won't tell if the version was changed properly, though
# (feat commits should increment minor, not patch version number),
# but is useful to identify when the programmer skipped version bumping altogether.

COMMIT_ACTION_SCRIPT=$(dirname $0)/get_commit_action.sh
COMMIT_ACTION=$($COMMIT_ACTION_SCRIPT)
if [ $COMMIT_ACTION == 'build_code' ]; then
    SHOULD_CHANGE_VERSION=0
else
    SHOULD_CHANGE_VERSION=1
fi

VERSION_CHANGED_SCRIPT=$(dirname $0)/get_version_changed.sh
$VERSION_CHANGED_SCRIPT
VERSION_HAS_CHANGED=$?

echo $VERSION_HAS_CHANGED
echo $SHOULD_CHANGE_VERSION

# TODO arithmetic comparison
if [ $VERSION_HAS_CHANGED  == $SHOULD_CHANGE_VERSION ] ; then
    exit 0
else
    exit 1
fi
    
