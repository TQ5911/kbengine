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
	AppSecret             string
	Mysql                 MYSQLConfig
	EnablePasswdLogin     bool
	NeedCDKey             bool
	CdKeyServer           string
	CentralServerId       uint32
	AddressForDebug       string
	IdipHttpServer        string
	LogPath               string
	LogLevel              string
	LogRotateSize         string
	HttpServerListDir     map[string]interface{}
	MapleServer           map[string]interface{}
	RedisServer           REDISConfig
	AccountTypes          []uint8
	YidunCaptcha          uint8
	YidunCaptchaID        string
	YidunSecurityID       string
	YidunSecurityKey      string
	TapTap				  map[string]interface{}
	Official			  map[string]interface{}
}

type ServerListConfig struct {
	ServerList     map[string]interface{}
	ServerGroup    map[string]interface{}
	ProvinceServer map[string]interface{}
}
