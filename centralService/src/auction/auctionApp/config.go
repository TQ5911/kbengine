package Auction

type MysqlConfig struct {
	Addr   string
	User   string
	Passwd string
	Db     string
}

type AppConfig struct {
	GameServerServiceAddr string
	ActionServerId        uint32
	AddressForDebug       string
	LogPath               string
	LogLevel              int
	LogRotateSize         string
	Mysql                 MysqlConfig
	GmLogServerId         uint32
	GmBuyInterception     uint32
}
