# git-hq
A remote manager for git

## Use Cases
Have lots of git repos everywhere? Have lots of machines you work on? Have lots of remotes for each repo?

By design, git does not keep track of your remotes, and other assorted information found in its `.git/config` file. Cloning a repo sets up an "origin" remote, but if you want to push to other remotes, these must be added manually, either with different names, or with an additional `url` entry in the origin remote.

`git-hq` references a global config file, `~/.git-hq` to lookup remote information that may not be found in the repository's local config file. All you need do is synchronize `git-hq`'s global config file (if you keep your dotfiles in a repository, this is easy), and any machine you're on can instantly clone known repositories

	 git hq clone [repo-name]

without having to do the usual routine of looking up the remote urls. Any repo known to `git-hq`'s config file can push or pull to all of its listed repositories (or named ones, using a simple name alias), even if they are not in the repo's individual config file

	git hq push
	git hq pull  
	git hq push github bitbucket  
	git hq pull gitorious  

As with git itself, `git-hq` uses a human-readable config file format (parsed using python's configparser library), and also allows remotes/repositories to be added via simple commands:

	git hq remote add github git@github.com:username/{repo}.git
	cd path/to/git/repo/
	git hq init             # git-hq now knows about this repo  
	git hq attach github	# the remote added above is now associated  
	git hq push             # push to the repo above  
	git hq remote commit	# "bake in" the repos in git-hq into git's config file  
	git hq run status -suno # shows modified files in all repos in config file

## Features

Sub commands, just as git uses, control what commands `git-hq` sends to git and how `git-hq` updates its config file with your repository information. Instead of executing `git-hq` directly as `./git-hq [subcommand]`, it is much easier to place the executable on your `$PATH` environment variable with `export PATH=$PATH:/dir/with/git-hq` (or your own shell's equivalent). Not only does this make `git-hq` easier to execute, but git itself will now recognize `git-hq` and allow you just type `git hq [subcommand]` instead.

### Individual Repository

`remote [add,attach,detach,commit]` controls the remotes in `git-hq`'s config file. `remote add {shortname} {repourl}` will add a new, remote (that is initially unattached to any specific repo). `remote attach {shortname}` will add the remote to the current repo (whatever repository you're in). `remote detach {shortname}` will remote a remove from the current repo (but it will still remain available to be attached to other repositories). `remote commit` will add the repositories to git's local config file for the current repo.

`clone {projectname}` clones a repository known to `git-hq` into the current directory.

`init [remotes]*` adds the current git repository to `git-hq`'s known list of repositories, and optionally attaches one or more remotes to this repository listing as well.

`purge [reponame]` removes the current repo (or the specified repo) from `git-hq`'s known list of repositories.

`pull [remotename]*` does a git pull on all the remotes (or only the remotes listed). An optional `-o` option pulls from only the first listed remote.

`push [remotename]*` does a git push on all the remotes (or only the remotes listed). An optional `-o` option pushes from only the first listed remote.

### Multiple Repository

`path [pathname]` sets the pathname for the current repo. If no pathname is specified, simply prints the current path. A path is a "cannonical" location for a repo, and lets `git-hq` know where to find the repo when running commands on all repositories.  

`run [command]` runs a command on all repos listed in `git-hq`'s config file (that have valid paths). Prints a header that includes the repo name before running the command on the repo.

## Details

`git-hq` is written in python, using a brittle wrapper (subprocess) around a few token git commands (future work should bind to [libgit2](http://libgit2.github.com/) ). Since git has no straightforward way to identify a repository, `git-hq ` uses the first commit's sha-1 to identify the repository.

Testing has been done with both Python 2.7 and Python 3, though `configparser` (aka `ConfigParser`) differs in parsing config files slightly (e.g. tabbed properties will break 2.7 but not 3), but most basic functionality is the same regardless of version.

For remote names, the special `{repo}` string will always be substituted with the name of the repository, which is found by the top-level directory name of the project. If you have a repo that has a different remote name than the director in which it is stored, you can simply omit the `{repo}` and include the full remote string, but this remote will not work with other repositories. `{repo}` will always be downcased, while `{Repo}` will retain case and `{REPO}` will uppercase the repo name. Many hosts differ in how they handle reponame case, so these options should provide enough flexibility in this regard. In addition, `configparser` provides a `$(variablename)s` syntax (note the "s" at the end) that will substitute a variable declared either in the same section, or in the [DEFAULT] section. This can be used for user names or host names to reduce the amount of typing.

## License

Copyright 2011 Jarrell Waggoner. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY JARRELL WAGGONER ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL JARRELL WAGGONER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

---

Jarrell Waggoner  
/-/ [malloc47.com](http://www.malloc47.com)
