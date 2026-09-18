#!/bin/sh
binName=$(basename "$PWD")
binPathName=../../bin/$binName
if [ ! -d "$binPathName" ]; then
    mkdir -p "$binPathName"
fi
go build -o $binPathName/$binName main.go
