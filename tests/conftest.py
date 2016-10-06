import os
import subprocess
import shutil

import pytest

from .common import create_commit

REPO_DIR = 'repodir'


@pytest.yield_fixture
def repo():
    subprocess.check_call(['git', 'init', REPO_DIR])
    os.chdir(REPO_DIR)

    create_commit('Initial commit')
    yield
    os.chdir('..')
    shutil.rmtree(REPO_DIR)

