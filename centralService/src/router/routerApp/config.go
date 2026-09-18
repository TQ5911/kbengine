package Router

type RedisServerConfig struct {
	Addr        string
	Username    string
	Passwd      string
	Db          string
	MaxIdle     int
	MaxActive   int
	IdleTimeout int
}

type AppConfig struct {
	GameServerServiceAddr     string
	RouterClusterAddr         string
	RouterClusterAdvertiseAddr string
	RouterId                  uint32
	AddressForDebug           string
	LogPath                   string
	LogLevel                  string
	LogRotateSize             string
	RedisServer               RedisServerConfig
}

// ClusterAdvertiseAddr 返回写进 Redis meta 的对外地址。
// 优先用 RouterClusterAdvertiseAddr（典型场景：监听 0.0.0.0，对外用具体 IP）；
// 未配置时回退到 RouterClusterAddr。
func (c *AppConfig) ClusterAdvertiseAddr() string {
	if c.RouterClusterAdvertiseAddr != "" {
		return c.RouterClusterAdvertiseAddr
	}
	return c.RouterClusterAddr
}
