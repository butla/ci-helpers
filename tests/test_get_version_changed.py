import subprocess
from .common import create_commit, commit_setup_py


def test_detect_version_changed(repo):
    commit_setup_py('0.0.1')
    commit_setup_py('0.0.2')

    assert _check_version_changed()


def test_detect_nothing_when_version_not_changed(repo):
    commit_setup_py()
    create_commit('docs(bla): bla2')

    assert not _check_version_changed()


def test_detect_version_changed_single_commit(repo):
    assert _check_version_changed()


def test_previous_commit_without_setup(repo):
    commit_setup_py()
    assert _check_version_changed()


def _check_version_changed():
    try:
        subprocess.check_call('../get_version_changed.sh')
        return True
    except subprocess.CalledProcessError as ex:
        if ex.returncode == 1:
            return False
        else:
            raise

