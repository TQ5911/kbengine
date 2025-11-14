package main

import (
	Auction "centralService/src/auction/auctionApp"
	"centralService/src/base"
	"centralService/src/common"
	"runtime/debug"
)

func main() {
	debug.SetGCPercent(1000)
	base.Init("auctionConf.json", &Auction.AuctionAppConfig, func() common.IApp {
		return Auction.NewAuctionApp()
	})
}
