package adminApp

import "strconv"

type REDISConfig struct {
	Addr     string
	Username string
	Passwd   string
	Db       string
}

type AdminConfig struct {
	AddressForGameServer     string
	AddressForGMT            string
	AddreesForGRPC           string
	HttpAPIAddress           string
	AddressForDebug          string
	MachinePort              uint16
	TransferAvatarSignSecret string
	HttpCmdSignKey           string
	CentralLoginCmdAddress   string
	LogPath                  string
	LogLevel                 string
	LogRotateSize            string
	IDIPMergeMap             map[string]uint32
	NeteaseMusicRedirect     string
	HttpSDKAddress           string
	RedisServer              REDISConfig
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
