package app

import "fmt"

const (
	_ = iota
	SERVICE_CLIENT_AUTH
	SERVICE_GAME_SERVER
)

const (
	ServiceStatus_None         = 0
	ServiceStatus_Connected    = 1
	ServiceStatus_Disconnected = 2
)

const (
	// 充值
	Recharge = 1
	// 重试
	Retry = 2
)

const (
	// 订单锁时间
	Order_Lock_Time = 60
)

func GetOrderLockKey(orderNo string) string {
	return fmt.Sprintf("order_add_lock_%v", orderNo)
}

const (
	CFG_TYPE_ITEM_DATA = "1"
)

// 设置配置数据
func GetCfgFiles() map[string]string {
	datas := map[string]string{
		CFG_TYPE_ITEM_DATA: "../data/itemData.itemData.txt",
	}
	return datas
}

var ConfigStore *CfgData
