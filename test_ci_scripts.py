import os
import shutil
import subprocess
import uuid

import pytest

REPO_DIR = 'repodir'
BUILD_CODE_OUT = b'build_code'
BUILD_DOCS_OUT = b'build_docs'


@pytest.yield_fixture
def repo():
    subprocess.check_call(['git', 'init', REPO_DIR])
    os.chdir(REPO_DIR)

    _create_commit('Initial commit')
    yield
    os.chdir('..')
    shutil.rmtree(REPO_DIR)


@pytest.mark.parametrize('commit_message, action', [
    ('feat(something): Added some feature.', BUILD_CODE_OUT),
    ('fix(something): Fixed some code.', BUILD_CODE_OUT),
    ('refactor(something): Refactored some code.', BUILD_CODE_OUT),
    ('perf(something): Increased performance somewhere.', BUILD_CODE_OUT),
    ('docs(something): Changed the readme.', BUILD_DOCS_OUT),
    ('style(something): Changed styling somewhere.', BUILD_DOCS_OUT),
    ('test(something): Refactored some tests.', BUILD_DOCS_OUT),
    ('chore(something): Did some CI stuff.', BUILD_DOCS_OUT),
])
def test_get_commit_action_for_proper_commit(repo, commit_message, action):
    _create_commit(commit_message)
    assert _get_commit_action() == action


def test_get_commit_action_for_invalid_commit(repo):
    _create_commit('fix of something')
    with pytest.raises(subprocess.CalledProcessError):
        _get_commit_action()


def _create_commit(message, with_file=None):
    if with_file is None:
        file_name = str(uuid.uuid4())
        subprocess.check_call(['touch', file_name])
    else:
        file_name = with_file
    subprocess.check_call(['git', 'add', file_name])
    subprocess.check_call(['git', 'commit', '-m', message])


def _get_commit_action():
    return subprocess.check_output('../get_commit_action.sh')


def test_detect_version_changed(repo):
    _commit_setup_py('0.0.1')
    _commit_setup_py('0.0.2')

    assert _check_version_changed()


def test_detect_nothing_when_version_not_changed(repo):
    _commit_setup_py()
    _create_commit('docs(bla): bla2')
    
    assert not _check_version_changed()


def test_detect_version_changed_single_commit(repo):
    assert _check_version_changed()


def test_previous_commit_without_setup(repo):
    _commit_setup_py()
    assert _check_version_changed()


def _check_version_changed():
    try:
        subprocess.check_call('../check_version_changed.sh')
        return True
    except subprocess.CalledProcessError as ex:
        if ex.returncode == 1:
            print('sraka')
            return False
        else:
            raise


def _commit_setup_py(version='0.0.1'):
    setup_content = """
from setuptools import setup

setup(
    name='blbla'
    version={version}
)
"""
    setup_filename = 'setup.py'
    with open(setup_filename, 'w') as setup_file:
        setup_file.write(setup_content.format(version=version))
    _create_commit('fix(bla): Blah, blah', setup_filename)

