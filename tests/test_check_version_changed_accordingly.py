import subprocess
import uuid

from .common import create_commit, commit_setup_py


def test_version_should_change_and_did(repo):
    commit_setup_py('0.0.1')
    commit_setup_py('0.0.2')
    assert _check_version_changed_accordingly()


def test_version_should_not_change_and_did_not(repo):
    commit_setup_py('0.0.1')
    create_commit("docs(bla): This commit shouldnt' bump the version")
    assert _check_version_changed_accordingly() 


def test_version_should_change_but_did_not(repo):
    commit_setup_py('0.0.1')
    new_filename = str(uuid.uuid4())
    subprocess.check_call(['touch', new_filename])
    create_commit('fix(bla): This commit should bump the version', new_filename)

    assert not _check_version_changed_accordingly()


def test_version_should_not_change_but_did(repo):
    commit_setup_py('0.0.1')
    commit_setup_py('0.0.2', message='docs(bla): Bad commit type.')
    assert not _check_version_changed_accordingly()


def test_version_change_for_malformed_commit_message(repo):
    create_commit('blablabla')
    assert not _check_version_changed_accordingly()


def _check_version_changed_accordingly():
    try:
        subprocess.check_call('../check_version_changed_accordingly.sh')
        return True
    except subprocess.CalledProcessError as ex:
        if ex.returncode == 1:
            return False
        else:
            raise
