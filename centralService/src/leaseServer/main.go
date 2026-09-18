package main

import (
	"centralService/src/base"
	"centralService/src/common"
	LeaseApp "centralService/src/leaseServer/leaseApp"
)

func main() {
	base.Init(&LeaseApp.LeaseConfig, func() common.IApp {
		return LeaseApp.NewLeaseApp()
	})
}
