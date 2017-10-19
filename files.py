#!/usr/bin/python
#################
# Author: Gabriel Pimenta
# Email: gamboua@gmail.com
#
# This Hook Script is used to forbidd files by the extension.
# 
#################

import sys
import os

zero = "0000000000000000000000000000000000000000"

# Please, set a list of forbidden extensions
extensions=['.zip']

args=sys.argv

# check if is a new branch
if args[2] == zero:
    # Get the HEAD commit on master
    # When a new branch comes, the old_ref variable is equals to zero and the git diff-tree commmand will failure.
    # If we set just the new_ref variable, the command output could not bring files from older commits.
    # So, if we create a new branch, and push it with 2 commits, if the older commit have a forbidden file, the command
    # won't works.
    master_hash = "git log -n 1 master --pretty=format:\"%H\""
    f = os.popen(master_hash)
    master_hash = f.read()

    # prepare parameters when new branch comes
    parametros="%s %s" % (master_hash, args[3])
else:
    # prepare parameters to an existing branch push
    parametros="%s %s" % (args[2], args[3])

# get the files list from commit
command = "git diff-tree --no-commit-id --name-only -r %s" % parametros
f = os.popen(command)
now = f.read()

for i in now.split("\n"):
    for ex in extensions:
        # check the extension on commit files
        if i[-len(ex):] == ex:
            print "Arquivo %s com extensao %s nao permitido" % (i, ex)
            exit(1)
exit(0)
