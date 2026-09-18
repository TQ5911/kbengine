package main

import (
	"centralService/src/base"
	"centralService/src/common"
	dropApp "centralService/src/dropServer/dropApp"
)

func main() {
	base.Init(&dropApp.DropConfig, func() common.IApp {
		return dropApp.NewDropApp()
	})
}
