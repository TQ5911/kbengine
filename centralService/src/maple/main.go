package main

import (
	"centralService/src/base"
	"centralService/src/common"
	mapleApp "centralService/src/maple/mapleApp"
)

func main() {
	base.Init("mapleConf.json", &mapleApp.MapleConfig, func() common.IApp {
		return mapleApp.NewMapleApp()
	})
}
