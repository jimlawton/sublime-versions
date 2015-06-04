#!/bin/sh
STARTVER=3065
ENDVER=3092
URLBASE="http://c758482.r82.cf2.rackcdn.com/"
TARBASE="sublime_text_3_build_"
DEBBASE="sublime-text_build-"
TARSUFFIX="_x64.tar.bz2"
DEBSUFFIX="_amd64.deb"
ver=$STARTVER
while [ $ver -le $ENDVER ]; do
    url="${URLBASE}${TARBASE}${ver}${TARSUFFIX}"
    wget $url
    url="${URLBASE}${DEBBASE}${ver}${DEBSUFFIX}"
    wget $url
    ver=`expr $ver + 1`
done
