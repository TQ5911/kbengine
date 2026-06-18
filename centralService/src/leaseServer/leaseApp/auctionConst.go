package LeaseApp

import (
	"encoding/json"
	"os"
)

// RentalProp 租赁概率三元组
type RentalProp [3]float64

// AuctionConstConfig 拍卖行常量配置（租赁服务复用）
type AuctionConstConfig struct {
	RentalProp01    RentalProp `json:"rentalProp01"`
	RentalProp02    RentalProp `json:"rentalProp02"`
	RentalTimelimit int        `json:"rentalTimelimit"`
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
