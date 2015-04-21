#!/usr/bin/env python
#
# Simple script to pack a tree structure back into a Sublime Text 3 install 
# package.
#
# Jim Lawton, April 21st, 2015.

import sys
import os
import os.path
import shutil
import zipfile
import tarfile


def main():
    if not os.path.exists("sublime_text_3"):
        sys.exit("ERROR: no sublime_text_3 directory!")
    # Make tempdir for archive.
    tempdir = tempfile.mkdtemp()
    print tempdir
    # Copy sublime_text_3 tree to tempdir.
    stroot = os.path.join(os.getcwd(), "sublime_text_3")
    shutil.copytree(stroot, tempdir)
    pkgroot = os.path.join(tempdir, "sublime_text_3", "Packages")
    pkgs = []
    for fname in os.listdir(pkgroot):
        path = os.path.join(pkgroot, fname)
        if not os.path.isdir(path):
            continue
        pkgs.append(fname)
    for pkg in pkgs:
        pkgfile = pkg + ".sublime-package"
        pkgdir = os.path.join(pkgroot, pkg)
        if not os.path.exists(pkgdir):
            sys.exit("ERROR: package %s does not exist!" % pkgdir)
        shutil.make_archive(pkgfile, "zip", pkgdir)
        shutil.rmtree(pkgdir, ignore_errors=True)
    with tarfile.open("sublime_text_3_SNAPSHOT.tar.bz2", "w") as tar:
        tar.add(tempdir)

if __name__ == '__main__':
    main()

