import subprocess
from .common import create_commit


def test_detect_version_changed(repo):
    _commit_setup_py('0.0.1')
    _commit_setup_py('0.0.2')

    assert _check_version_changed()


def test_detect_nothing_when_version_not_changed(repo):
    _commit_setup_py()
    create_commit('docs(bla): bla2')

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
    create_commit('fix(bla): Blah, blah', setup_filename)

