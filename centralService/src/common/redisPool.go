package common

import (
	"centralService/src/appLog"
	"context"
	"time"

	"github.com/garyburd/redigo/redis"
)

type RedisPoolOptions struct {
	ServerName  string
	Addr        string
	Username    string
	Password    string
	Db          string
	MaxIdle     int
	MaxActive   int
	IdleTimeout int
}

func NewRedisPool(opts RedisPoolOptions) *redis.Pool {
	if opts.MaxIdle <= 0 {
		opts.MaxIdle = 16
	}
	if opts.MaxActive <= 0 {
		opts.MaxActive = 100
	}
	if opts.IdleTimeout <= 0 {
		opts.IdleTimeout = 100
	}

	pool := &redis.Pool{
		MaxIdle:     opts.MaxIdle,
		MaxActive:   opts.MaxActive,
		IdleTimeout: time.Duration(opts.IdleTimeout) * time.Second,
		Wait:        true,
		Dial: func() (redis.Conn, error) {
			c, err := redis.Dial("tcp", opts.Addr,
				redis.DialConnectTimeout(RedisDialTimeout),
				redis.DialReadTimeout(RedisReadTimeout),
				redis.DialWriteTimeout(RedisWriteTimeout),
			)
			if err != nil {
				appLog.Errorf("[%s] redis dial failed, addr=%s, err=%s", opts.ServerName, opts.Addr, err.Error())
				return nil, err
			}
			if opts.Username != "" && opts.Password != "" {
				if _, err := c.Do("AUTH", opts.Username, opts.Password); err != nil {
					appLog.Errorf("[%s] redis auth failed, addr=%s, user=%s, err=%s", opts.ServerName, opts.Addr, opts.Username, err.Error())
					c.Close()
					return nil, err
				}
			} else if opts.Password != "" {
				if _, err := c.Do("AUTH", opts.Password); err != nil {
					appLog.Errorf("[%s] redis auth failed, addr=%s, err=%s", opts.ServerName, opts.Addr, err.Error())
					c.Close()
					return nil, err
				}
			}
			if opts.Db != "" {
				if _, err := c.Do("SELECT", opts.Db); err != nil {
					appLog.Errorf("[%s] redis select db failed, addr=%s, db=%s, err=%s", opts.ServerName, opts.Addr, opts.Db, err.Error())
					c.Close()
					return nil, err
				}
			}
			appLog.Infof("[%s] redis connected, addr=%s", opts.ServerName, opts.Addr)
			return c, nil
		},
		TestOnBorrow: func(c redis.Conn, t time.Time) error {
			if time.Since(t) < 30*time.Second {
				return nil
			}
			_, err := c.Do("PING")
			if err != nil {
				appLog.Warnf("[%s] redis idle conn probe failed, will redial, err=%s", opts.ServerName, err.Error())
			}
			return err
		},
	}

	go func() {
		ticker := time.NewTicker(30 * time.Second)
		defer ticker.Stop()
		var okTicks int
		for range ticker.C {
			ctx, cancel := context.WithTimeout(context.Background(), RedisDialTimeout)
			getStart := time.Now()
			conn, err := pool.GetContext(ctx)
			getCost := time.Since(getStart)
			cancel()
			if err != nil {
				stats := pool.Stats()
				appLog.Errorf("[%s] redis health check failed (get conn), addr=%s, cost=%v, active=%d/%d idle=%d, err=%s",
					opts.ServerName, opts.Addr, getCost,
					stats.ActiveCount, opts.MaxActive, stats.IdleCount,
					err.Error())
				continue
			}
			_, pingErr := conn.Do("PING")
			conn.Close()
			if pingErr != nil {
				appLog.Errorf("[%s] redis health check failed, addr=%s, err=%s", opts.ServerName, opts.Addr, pingErr.Error())
				continue
			}
			okTicks++
			if okTicks%60 == 0 {
				stats := pool.Stats()
				appLog.Infof("[%s] redis health check ok, addr=%s, active=%d/%d idle=%d",
					opts.ServerName, opts.Addr, stats.ActiveCount, opts.MaxActive, stats.IdleCount)
			}
		}
	}()

	return pool
}
