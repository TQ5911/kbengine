package common

import "time"

const (
	RedisDialTimeout  = 10 * time.Second
	RedisReadTimeout  = 10 * time.Second
	RedisWriteTimeout = 10 * time.Second
	RedisOpTimeout    = 5 * time.Second
)
