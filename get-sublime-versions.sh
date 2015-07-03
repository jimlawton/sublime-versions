#!/bin/sh
STARTVER=0
ENDVER=9999

if [ "$#" -gt 0 ]; then
    STARTVER=$1
    if [ "$#" -gt 1 ]; then
        ENDVER=$2
    fi
fi
URLBASE="http://c758482.r82.cf2.rackcdn.com/"
TARBASE="sublime_text_3_build_"
DEBBASE="sublime-text_build-"
TARSUFFIX="_x64.tar.bz2"
DEBSUFFIX="_amd64.deb"
ver=$STARTVER
while [ $ver -le $ENDVER ]; do
    echo "Getting version ${ver}..."
    url="${URLBASE}${TARBASE}${ver}${TARSUFFIX}"
    wget $url
    if [ $? != 0 ]; then
        break
    fi
    url="${URLBASE}${DEBBASE}${ver}${DEBSUFFIX}"
    wget $url
    ver=`expr $ver + 1`
done
