package main

import (
	"centralService/src/base"
	"centralService/src/common"
	allianceApp "centralService/src/allianceService/allianceApp"
)

func main() {
	base.Init("allianceServiceConfig.json", &allianceApp.AllianceConfig, func() common.IApp {
		return allianceApp.NewAllianceApp()
	})
}
