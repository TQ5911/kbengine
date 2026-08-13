package crossDataApp

type MYSQLConfig struct {
	Addr   string
	User   string
	Passwd string
	Db     string
}

type AppConfig struct {
	Mysql               MYSQLConfig
	LogPath             string
	LogLevel            string
	LogRotateSize       string
	CrossDataServerAddr string
	AddressForDebug     string
}
