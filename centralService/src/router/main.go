package main

//package main

import (
	"centralService/src/base"
	"centralService/src/common"
	Router "centralService/src/router/routerApp"
)

func main() {
	base.Init("routerConf.json", &Router.RouterConfig, func() common.IApp {
		return Router.NewRouterApp()
	})
}
