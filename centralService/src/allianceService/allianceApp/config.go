package allianceApp

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
	AllianceServiceAddr string
	AddressForDebug     string
	ServerName          string
	ServerId            int
}

type BizConstCfg struct {
	MaxEventsPerAlliance int
	UnionNameMinLength   int
	UnionNameMaxLength   int
	UnionCreedMaxLength  int
}
