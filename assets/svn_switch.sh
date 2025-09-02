#!/bin/bash
rev='HEAD'
if [ $# -gt 0 ]
then
	rev=$1
fi

if [ "$rev" = "HEAD" ] || [ $rev -ne 0 ]
then
    svn up -r $rev --ignore-externals .
    svn up -r $rev --ignore-externals ./scripts/data
    svn up -r $rev --ignore-externals ./res/spaces/airwalls
    svn up -r $rev --ignore-externals ../..
fi
