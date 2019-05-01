from fabric.api import run
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

"""
Usage:
  from lib import git
  git.init()
"""


def init():
    print yellow("RUN: git init")
    run("git init")

"""
git tree

Usage:

  from lib import git
  git.tree()
"""


def tree():
    run("git config --global alias.tree 'log --oneline --decorate --all --graph'")

    print yellow("RUN: git tree")
    return run("git tree")

"""
git status -s

Usage:

  from lib import git
  git.status()
"""


def status():
    print yellow("RUN: git status -s")
    return run("git status -s")


def branch():
    print yellow("RUN: git branch")
    run("git branch")

"""
Run git command

Usage:

   from lib import git
   git.command('status -s')
   git.command('status', '-s')
"""


def command(*param):
    print yellow("RUN: git %s" % ' '.join(param))
    return run("git %s" % ' '.join(param))
