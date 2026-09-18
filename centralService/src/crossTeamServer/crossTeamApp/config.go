package crossTeamApp

type AppConfig struct {
	CrossTeamServerAddr        string
	AddressForDebug            string
	LogPath                    string
	LogLevel                   string
	LogRotateSize              string
	GroupId                    int32 // 游戏服组标识：每组部署一个中心单例，组间完全隔离
	WorkerNum                  int   // 队伍 worker 数量（请求按 teamId 取模投入）
	MatchTimeoutSeconds        int   // 散人匹配入池超时（秒），<= 0 时用默认值 300
	CrusadeMaxConcurrent       int   // 全组同时进行中的讨伐上限（检查中+副本中），<= 0 不限（仅跨服模式讨伐占用）
	CrusadeStartLimitPerSecond int   // 全局每秒讨伐发起上限，<= 0 不限
}
