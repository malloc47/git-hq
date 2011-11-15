import subprocess as sp

def hashes():
    try:
        return sp.check_output(["git","log","--pretty=format:%H"]).decode("utf-8").split('\n')
    except sp.CalledProcessError:
        return []

def last_hash():
    try:
        return sp.check_output("git log --pretty=format:%H | tail -n 1",shell=True).decode("utf-8").strip()
    except:
        return None

def name():
    try:
        return sp.check_output("basename $(git rev-parse --show-toplevel)",shell=True).decode("utf-8").strip()
    except:
        return None

def exists():
    return not sp.call("git rev-parse --git-dir &>/dev/null",shell=True)

def cmd(cmd,source):
    sp.call(["git",cmd,source])
