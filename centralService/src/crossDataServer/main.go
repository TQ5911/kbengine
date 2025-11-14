package main

import (
	"centralService/src/base"
	"centralService/src/common"
	crossDataApp "centralService/src/crossDataServer/crossDataApp"
)

func main() {
	base.Init("crossDataServerConfig.json", &crossDataApp.CrossDataConfig, func() common.IApp {
		return crossDataApp.NewCrossDataApp()
	})
}
