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

