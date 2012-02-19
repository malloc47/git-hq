""" 
Simple shell-based git binding module

Placeholder until libgit2 is more mature and pervasive
"""

import os
import subprocess as sp

def hashes():
    try:
        output = sp.check_output(["git","log","--pretty=format:%H"]
                                ).decode("utf-8").split('\n')
    except AttributeError:
        #sp.check_output doesn't exist in versions prior to 2.7
        #attribute reference will fail and will raise this error
        #this code gives same result and works in 2.6
        output = sp.Popen(["git","log","--pretty=format:%H"],
                          stdout=sp.PIPE).communicate()[0].decode("utf-8"
                          ).split('\n')
    except sp.CalledProcessError:
        return []

    output.reverse()
    return output

def last_hash():
    try:
        return sp.check_output("git log --pretty=format:%H | tail -n 1",
                                shell=True).decode("utf-8").strip()
    except AttributeError:
        return sp.Popen("git log --pretty=format:%H | tail -n 1", 
                        stdout=sp.PIPE, shell=True).communicate()[0].decode(
                        "utf-8").strip()
    except:
        return None

def name():
    try:
        return sp.check_output("basename $(git rev-parse --show-toplevel)",
                                shell=True).decode("utf-8").strip()
    except AttributeError:
        return sp.Popen("basename $(git rev-parse --show-toplevel)",
                        stdout=sp.PIPE, 
                        shell=True).communicate()[0].decode("utf-8").strip()
    except:
        return None

def path():
    try:
        return sp.check_output("git rev-parse --show-toplevel",
                                shell=True).decode("utf-8").strip()
    except AttributeError:
        return sp.Popen("git rev-parse --show-toplevel",
                        stdout=sp.PIPE, 
                        shell=True).communicate()[0].decode("utf-8").strip()
    except:
        return None

def exists():
    # trick so we don't see output
    fnull = open(os.devnull, 'w')
    output = not sp.call(["git","rev-parse","--git-dir"], stdout = fnull, 
                         stderr = fnull)
    fnull.close()
    return output

def cmd(args,path=None):
    if path is None:
        sp.check_call(["git"]+args)
    else:
        if not os.path.isdir(path):
            raise IOError()
        sp.check_call(["git"]+args,cwd=path)
