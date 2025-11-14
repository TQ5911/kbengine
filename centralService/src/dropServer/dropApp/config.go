package DropApp

type MYSQLConfig struct {
	Addr   string
	User   string
	Passwd string
	Db     string
}

type AppConfig struct {
	DropServerAddr  string
	AddressForDebug string
	LogPath         string
	LogLevel        string
	LogRotateSize   string
	Mysql           MYSQLConfig
}
