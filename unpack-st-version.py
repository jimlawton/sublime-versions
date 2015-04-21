#!/usr/bin/env python
#
# Simple script to unpack a Sublime-Text 3 install kit into a tree structure 
# that can be committed to Git, so that different versions of Sublime Text 
# can be compared.
#
# Jim Lawton, April 21st, 2015.

import sys
import os
import os.path
import shutil
import zipfile
import tarfile


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
    args = sys.argv
    if len(args) <= 1:
        sys.exit("ERROR: please supply a tar file!")
    if not os.path.isfile(sys.argv[1]):
        sys.exit("ERROR: file %s does not exist!" % sys.argv[1])
    if os.path.exists("sublime_text_3"):
        shutil.rmtree("sublime_text_3", ignore_errors=True)
    with tarfile.open(sys.argv[1], "r") as tar:
        tar.extractall()
    for pkg in getPackages(os.getcwd()):
        pkgroot = os.path.dirname(pkg)
        pkgname = os.path.basename(pkg).replace(".sublime-package", "")
        pkgdir = os.path.join(pkgroot, pkgname)
        if os.path.exists(pkgdir):
            shutil.rmtree(pkgdir, ignore_errors=True)
        os.makedirs(pkgdir)
        with zipfile.ZipFile(pkg, 'r') as pkgzip:
            pkgzip.extractall(pkgdir)


if __name__ == '__main__':
    main()

