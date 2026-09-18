package adminApp

import (
	"errors"
	"strconv"
)

type REDISConfig struct {
	Addr     string
	Username string
	Passwd   string
	Db       string
}

type AdminConfig struct {
	AddressForGameServer        string
	AddressForGMT               string
	AddreesForGRPC              string
	HttpAPIAddress              string
	AddressForDebug             string
	MachinePort                 uint16
	TransferAvatarSignSecret    string
	HttpCmdSignKey              string
	CentralLoginCmdAddressList  []string
	LogPath                     string
	LogLevel                    string
	LogRotateSize               string
	IDIPMergeMap                map[string]uint32
	NeteaseMusicRedirect        string
	HttpSDKAddress              string
	RedisServer                 REDISConfig
}

func (self AdminConfig) GetNewServerId(origServerId uint32) uint32 {
	serverId := origServerId
	if self.IDIPMergeMap != nil {
		mapToServerId := origServerId
		for {
			ok := false
			mapToServerId, ok = self.IDIPMergeMap[strconv.FormatUint(uint64(mapToServerId), 10)]
			if ok {
				serverId = mapToServerId
			} else {
				break
			}
		}
	}
	return serverId
}

// Validate 校验 AdminConfig 必需字段。任一字段不通过会返回非 nil error；NewAdminApp 在 error 时返回 nil，
// 借此让 base.initServer 走 ExitProgram(1) 的退出分支，避免带着不合法 config 继续起服。
func (self *AdminConfig) Validate() error {
	if self.AddressForGameServer == "" {
		return errors.New("AddressForGameServer is empty")
	}
	if self.HttpAPIAddress == "" {
		return errors.New("HttpAPIAddress is empty")
	}
	if self.MachinePort == 0 {
		return errors.New("MachinePort must be > 0")
	}
	if self.RedisServer.Addr == "" {
		return errors.New("RedisServer.Addr is empty")
	}
	if len(self.CentralLoginCmdAddressList) == 0 {
		return errors.New("CentralLoginCmdAddressList is empty (at least one centralLogin cmd address is required)")
	}
	return nil
}
