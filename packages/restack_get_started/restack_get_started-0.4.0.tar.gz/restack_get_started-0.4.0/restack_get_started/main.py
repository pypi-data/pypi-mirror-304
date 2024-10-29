# /// script
# dependencies = ["../get-started.sh"]
# ///

import subprocess

def _run(bash_script):
    try:
        return subprocess.call(bash_script, shell=True)
    except Exception as e:
        print(f"Error executing script: {e}")
        return 1

def restack_get_started():
    return _run("../get-started.sh")

if __name__ == "__main__":
    restack_get_started()
