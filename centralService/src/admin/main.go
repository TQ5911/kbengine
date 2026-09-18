package main

import (
	"centralService/src/admin/adminApp"
	"centralService/src/base"
	"centralService/src/common"
)

var app *adminApp.AdminApp = nil
var adminConfig adminApp.AdminConfig = adminApp.AdminConfig{}

func main() {
	base.Init(&adminConfig, func() common.IApp {
		return adminApp.NewAdminApp()
	})
}
