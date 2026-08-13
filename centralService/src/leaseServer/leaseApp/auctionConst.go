package LeaseApp

import (
	"encoding/json"
	"os"
)

// AuctionConstConfig 拍卖行常量配置（租赁服务复用）
// 租赁费率（rentalProp01/02）不在此处：由游戏服在 LeaseItemPrepare 请求中透传，支持热更
type AuctionConstConfig struct {
	RentalTimelimit    int `json:"rentalTimelimit"`
	RentalAutoUnlist   int `json:"rentalAutoUnlist"`   // 租赁上架自动下架时长（小时）
	RentalInitShelfNum int `json:"rentalInitShelfNum"` // 玩家默认租赁货架数量
}

func loadAuctionConst(path string) (*AuctionConstConfig, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var cfg AuctionConstConfig
	if err := json.Unmarshal(data, &cfg); err != nil {
		return nil, err
	}
	return &cfg, nil
}
