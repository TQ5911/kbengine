package main

import (
	"centralService/src/base"
	"centralService/src/common"
	allianceApp "centralService/src/allianceService/allianceApp"
)

func main() {
	base.Init(&allianceApp.AllianceConfig, func() common.IApp {
		return allianceApp.NewAllianceApp()
	})
}
