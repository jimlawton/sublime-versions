#!/usr/bin/env python
#
# Simple script to unpack a Sublime-Text 3 install kit into a tree structure 
# that can be committed to Git, so that different versions of Sublime Text 
# can be compared.
#
# Jim Lawton, April 21st, 2015.

import os
import os.path
import shutil


def getPackages(path):
    excludes = [".git"]
    for dirpath, dirnames, filenames in os.walk(path):
        if os.path.dirname(dirpath) in excludes:
            dirnames[:] = []
            filenames[:] = []
            continue
        for x in excludes:
            if x in dirnames:
                del dirnames[dirnames.index(x)]
        for filename in filenames:
            if filename.endswith(".sublime-package"):
                path = os.path.join(dirpath, filename)
                yield path


def main():
    for pkg in getPackages(os.getcwd()):
        print pkg

if __name__ == '__main__':
    main()

