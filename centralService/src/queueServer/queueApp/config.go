package Queue

type REDISConfig struct {
	Addr   string
	Passwd string
	Db     string
}

type AppConfig struct {
	ClientServiceAddr     string
	GameServerServiceAddr string
	AddressForDebug       string
	LogPath               string
	LogLevel              string
	LogRotateSize         string
	HttpServer            string
	RedisServer           REDISConfig
}
