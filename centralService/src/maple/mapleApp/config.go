package MapleApp

type MYSQLConfig struct {
	Addr   string
	User   string
	Passwd string
	Db     string
}

type AppConfig struct {
	HttpAddr        string
	AddressForDebug string
	LogPath         string
	LogLevel        string
	LogRotateSize   string
	Mysql           MYSQLConfig
	Secret          string
}

var MapleConfig AppConfig
