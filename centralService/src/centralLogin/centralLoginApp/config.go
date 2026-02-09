package CentralLogin

type MYSQLConfig struct {
	Addr   string
	User   string
	Passwd string
	Db     string
}

type REDISConfig struct {
	Addr   string
	Passwd string
	Db     string
}

type AppConfig struct {
	ClientServiceAddr     string
	GameServerServiceAddr string
	Mysql                 MYSQLConfig
	CentralServerId       uint32
	AddressForDebug       string
	IdipHttpServer        string
	LogPath               string
	LogLevel              string
	LogRotateSize         string
	RedisServer           REDISConfig
	AccountTypes          []uint8
	TapTap				  map[string]interface{}
	Official			  map[string]interface{}
}

type ServerListConfig struct {
	ServerList     map[string]interface{}
	ServerGroup    map[string]interface{}
	ProvinceServer map[string]interface{}
}
