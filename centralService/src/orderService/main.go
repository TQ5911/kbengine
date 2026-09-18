package main

import (
	"centralService/src/base"
	"centralService/src/common"
	OrderApp "centralService/src/orderService/app"
)

func main() {
	base.Init(&OrderApp.OrderServiceConfig, func() common.IApp {
		return OrderApp.NewOrderApp()
	})
}
