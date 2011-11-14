import subprocess as sp

def hashes():
    return sp.check_output(["git","log","--pretty=format:%H"]).decode("utf-8").split('\n')

def last_hash():
    return sp.check_output("git log --pretty=format:%H | tail -n 1",shell=True).decode("utf-8").strip()

def name():
    return sp.check_output("basename $(git rev-parse --show-toplevel)",shell=True).decode("utf-8").strip()

def cmd(cmd,source):
    sp.check_call(["git",cmd,source])
