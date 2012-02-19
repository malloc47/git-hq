try:
    import configparser as cp
except:
    import ConfigParser as cp   # python 2.x

class Repo(object):
    """object to store relevant information about a repo"""
    def __init__(self,name,id,repos,path=None):
        self.name = name
        self.id = id
        self.repos = repos
        self.path = path

def load_config(file):
    c = cp.ConfigParser()
    c.readfp(open(file))

    remotes = dict(c.items('remotes'))
    del remotes['uname']

    sections = c.sections()
    sections.remove('remotes')

    repos = {}

    for s in sections:
        p = dict(c.items(s))    # p=properties
        try:
            remote = [(r,remotes[r]. \
                           replace("{repo}",s.lower()). \
                           replace("{REPO}",s.upper()). \
                           replace("{Repo}",s))
                      for r in p['repos'].split(',')]
        except KeyError:
            remote = []
        try:
            path = p['path']
        except KeyError:
            path = None
        repos[p['id']] = Repo(s,p['id'],remote,path)
    return repos,remotes

def create_config(file):
    defaults = {'uname':'mysername'}
    c = cp.ConfigParser(defaults)
    c.add_section("remotes")
    with open(file, 'w') as f:
        c.write(f)

def ammend_property_config(file,section,data):
    c = cp.ConfigParser()
    c.read(file)
    c.set(section,data[0],data[1])
    with open(file, 'w') as f:
        c.write(f)

def remove_property_config(file,section,data):
    c = cp.ConfigParser()
    c.read(file)
    if not c.remove_option(section,data):
        raise CmdFailed('remove_property',"property not found in config file")
    with open(file, 'w') as f:
        c.write(f)

def ammend_section_config(file,section,data):
    c = cp.ConfigParser()
    c.read(file)
    c.add_section(section)
    for d in data:
        c.set(section,d[0],d[1])
    with open(file, 'w') as f:
        c.write(f)

def remove_section_config(file,section):
    c = cp.ConfigParser()
    c.read(file)
    if not c.remove_section(section):
        raise CmdFailed('remove_section',"section not found in config file")
    with open(file, 'w') as f:
        c.write(f)
