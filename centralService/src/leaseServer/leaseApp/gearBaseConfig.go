package LeaseApp

import (
	"encoding/json"
	"os"
	"strconv"
)

// GearBaseItem gearBase 配置单项，用于商店分类过滤
type GearBaseItem struct {
	Type    uint32 `json:"type"`    // 装备大类
	SubType uint32 `json:"subType"` // 装备子类
}

func loadGearBaseMap(path string) (map[uint32]*GearBaseItem, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var raw map[string]*GearBaseItem
	if err := json.Unmarshal(data, &raw); err != nil {
		return nil, err
	}
	result := make(map[uint32]*GearBaseItem, len(raw))
	for k, v := range raw {
		if id, err := strconv.ParseUint(k, 10, 32); err == nil {
			result[uint32(id)] = v
		}
	}
	return result, nil
}
