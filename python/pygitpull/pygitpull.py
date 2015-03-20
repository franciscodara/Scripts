#!/usr/bin/python

import re
import os
import sys

HOME = os.getenv("HOME")
rgxp_motor = re.compile(r"\* \w+")
search = rgxp_motor.search

try:
    import git as _git
except ImportError:
    print "You need to installl python-git"
    sys.exit(1)


def get_branch(git):
    branches = git.branch()
    branches = branches if branches else 'None'
    result = search(branches)
    branch = result.group() if result else None
    return branch.split('*')[1] if branch else 'no branch'


def exec_pulls(dirs):
    for dir in dirs:
        primary_path = HOME+'/'+dir
        for gitrepo in os.listdir(primary_path):
            full_path = primary_path+'/'+gitrepo
            if os.path.isdir(full_path):
                if '.git' in os.listdir(full_path):
                    try:
                        git = _git.cmd.Git(full_path)
                        branch = get_branch(git)
                        print "git pull in %s in branch %s" % (full_path,
                                                               branch)
                        git.pull()
                    except _git.GitCommandError:
                        print "Error not a git repository or a valid remote"
    print "done"

if __name__ == '__main__':
    dirs = sys.argv[1:]
    exec_pulls(dirs)
