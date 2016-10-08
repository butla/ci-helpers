import subprocess
import uuid


def create_commit(message, with_file=None):
    if with_file is None:
        file_name = str(uuid.uuid4())
        subprocess.check_call(['touch', file_name])
    else:
        file_name = with_file
    subprocess.check_call(['git', 'add', file_name])
    subprocess.check_call(['git', 'commit', '-m', message])


def commit_setup_py(version='0.0.1', message='fix(bla): Some version changing stuff.'):
    setup_py_template = """
from setuptools import setup

setup(
    name='asdasd',
    version='{version}',
)
"""
    setup_filename = 'setup.py'
    with open(setup_filename, 'w') as setup_file:
        setup_file.write(setup_py_template.format(version=version))
    create_commit(message, setup_filename)

