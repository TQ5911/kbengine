package main

import (
	"centralService/src/base"
	"centralService/src/common"
	crossTeamApp "centralService/src/crossTeamServer/crossTeamApp"
)

func main() {
	base.Init(&crossTeamApp.CrossTeamConfig, func() common.IApp {
		return crossTeamApp.NewCrossTeamApp()
	})
}
