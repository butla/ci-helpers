import subprocess
import pytest

from .common import create_commit

BUILD_CODE_OUT = b'build_code'
BUILD_DOCS_OUT = b'build_docs'


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
    create_commit(commit_message)
    assert _get_commit_action() == action


def test_get_commit_action_for_invalid_commit(repo):
    create_commit('fix of something')
    with pytest.raises(subprocess.CalledProcessError):
        _get_commit_action()


def _get_commit_action():
    return subprocess.check_output('../get_commit_action.sh')

