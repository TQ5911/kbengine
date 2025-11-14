@echo off
go env -w GO111MODULE=on
go build -o ../../bin/login/centralLogin.exe main.go
go build -o ../../bin/login/testLogin.exe test.go
