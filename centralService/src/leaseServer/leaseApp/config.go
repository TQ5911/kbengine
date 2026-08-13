package LeaseApp

// MysqlConfig MySQL 连接配置
type MysqlConfig struct {
	Addr   string // 数据库地址，格式 host:port
	User   string // 用户名
	Passwd string // 密码
	Db     string // 数据库名
}

// RedisConfig Redis 连接配置
type RedisConfig struct {
	Addr     string // Redis 地址，格式 host:port
	Username string // 用户名（为空时走纯密码鉴权）
	Passwd   string // 密码（无密码时为空）
	Db       string // 数据库编号（字符串形式）
}

// RateLimitConfig 限流配置
type RateLimitConfig struct {
	R float64 `json:"r"` // 每秒产生令牌数
	B int     `json:"b"` // 令牌桶容量（突发上限）
}

// AppConfig 租赁服务全局配置
type AppConfig struct {
	GameServerServiceAddr string          // 游戏服接入的 TCP 监听地址
	AddressForDebug       string          // HTTP pprof 调试接口地址
	LogPath               string          // 日志文件路径
	LogLevel              string          // 日志级别
	LogRotateSize         string          // 日志轮转大小（MB）
	Mysql                 MysqlConfig     // MySQL 配置
	RedisServer           RedisConfig     // Redis 配置
	RateLimit             RateLimitConfig // 限流配置
	PendingStatusTimeout  int             // 预上架/预租赁中间状态超时时间（秒），超时由清扫器自动恢复，<=0 时默认 60
	CleanIntervalHours    int             // 数据库历史数据清理间隔（小时），<=0 时默认 6
	CleanBatchSize        int             // 数据库清理每批删除行数，<=0 时默认 100
	CleanGraceDays        int             // 历史数据宽限期（天），CANCELED/已结束 LEASED 行超过该时长才删除，<=0 时默认 14
}
