package common

import (
	"centralService/src/appLog"
	"context"
	"fmt"
	"os"
	"path/filepath"
	"sync"
	"sync/atomic"
	"testing"
	"time"

	"github.com/gomodule/redigo/redis"
)

// >>> 改成你的实际目标地址 <<<
const (
	demoRedisAddr = "192.168.11.138:7617"
	demoRedisUser = ""
	demoRedisPass = ""
	demoRedisDB   = "0"

	demoDialTimeout = 5 * time.Second
	demoBurstSize   = 32
)

func TestMain(m *testing.M) {
	logDir, err := os.MkdirTemp("", "redisDemo-log-")
	if err == nil {
		logPath := filepath.Join(logDir, "demo.log")
		appLog.LogInit(logPath, 0, 10)
	}
	os.Exit(m.Run())
}

func newDemoPool() *redis.Pool {
	return NewRedisPool(RedisPoolOptions{
		ServerName:  "demo",
		Addr:        demoRedisAddr,
		Username:    demoRedisUser,
		Password:    demoRedisPass,
		Db:          demoRedisDB,
		MaxIdle:     8,
		MaxActive:   16,
		IdleTimeout: 60,
	})
}

func TestRedisDemo_Ping(t *testing.T) {
	pool := newDemoPool()
	defer pool.Close()

	ctx, cancel := context.WithTimeout(context.Background(), demoDialTimeout)
	defer cancel()

	start := time.Now()
	conn, err := pool.GetContext(ctx)
	if err != nil {
		t.Fatalf("get conn failed in %v: %v", time.Since(start), err)
	}
	defer conn.Close()

	reply, err := conn.Do("PING")
	if err != nil {
		t.Fatalf("PING failed in %v: %v", time.Since(start), err)
	}
	t.Logf("[PING]        ok in %v  reply=%v", time.Since(start), reply)
}

func TestRedisDemo_SetGet(t *testing.T) {
	pool := newDemoPool()
	defer pool.Close()

	ctx, cancel := context.WithTimeout(context.Background(), demoDialTimeout)
	defer cancel()
	conn, err := pool.GetContext(ctx)
	if err != nil {
		t.Fatalf("get conn failed: %v", err)
	}
	defer conn.Close()

	key := fmt.Sprintf("redisDemo:%d", time.Now().UnixNano())
	start := time.Now()
	if _, err := conn.Do("SET", key, "hello-redis", "EX", 30); err != nil {
		t.Fatalf("SET failed in %v: %v", time.Since(start), err)
	}
	got, err := redis.String(conn.Do("GET", key))
	if err != nil {
		t.Fatalf("GET failed in %v: %v", time.Since(start), err)
	}
	if got != "hello-redis" {
		t.Fatalf("GET mismatch, got %q", got)
	}
	t.Logf("[SET/GET]     ok in %v  key=%s value=%s", time.Since(start), key, got)

	if _, err := conn.Do("DEL", key); err != nil {
		t.Logf("[DEL]         warn: %v", err)
	}
}

func TestRedisDemo_ConcurrentBurst(t *testing.T) {
	pool := newDemoPool()
	defer pool.Close()

	var ok, fail int64
	var wg sync.WaitGroup
	wg.Add(demoBurstSize)
	start := time.Now()
	for i := 0; i < demoBurstSize; i++ {
		go func(idx int) {
			defer wg.Done()
			ctx, cancel := context.WithTimeout(context.Background(), demoDialTimeout)
			defer cancel()
			conn, err := pool.GetContext(ctx)
			if err != nil {
				atomic.AddInt64(&fail, 1)
				t.Logf("  goroutine %d get failed: %v", idx, err)
				return
			}
			defer conn.Close()
			if _, err := conn.Do("PING"); err != nil {
				atomic.AddInt64(&fail, 1)
				t.Logf("  goroutine %d ping failed: %v", idx, err)
				return
			}
			atomic.AddInt64(&ok, 1)
		}(i)
	}
	wg.Wait()
	t.Logf("[BURST x%d]  done in %v  ok=%d fail=%d", demoBurstSize, time.Since(start), ok, fail)
}

func TestRedisDemo_QuickTimeoutProbe(t *testing.T) {
	short := 500 * time.Millisecond
	start := time.Now()
	conn, err := redis.Dial("tcp", demoRedisAddr,
		redis.DialConnectTimeout(short),
		redis.DialReadTimeout(short),
		redis.DialWriteTimeout(short),
	)
	if err != nil {
		t.Logf("[FAST DIAL]   fail in %v: %v  -> 大概率 网络/端口不通 或 Redis 没监听", time.Since(start), err)
		return
	}
	defer conn.Close()

	ctx, cancel := context.WithTimeout(context.Background(), short)
	defer cancel()
	start = time.Now()
	pingConn, err := (&redis.Pool{
		Dial: func() (redis.Conn, error) { return conn, nil },
		MaxIdle: 1,
	}).GetContext(ctx)
	if err != nil {
		t.Logf("[FAST PING]   fail in %v: %v  -> 端口通,但服务卡死/慢", time.Since(start), err)
		return
	}
	defer pingConn.Close()
	reply, err := pingConn.Do("PING")
	dialCost := time.Since(start)
	if err != nil {
		t.Logf("[FAST PING]   fail in %v: %v  -> 端口通,但服务卡死/慢", dialCost, err)
		return
	}
	t.Logf("[FAST PING]   ok in %v  reply=%v  -> 网络与服务都健康", dialCost, reply)
}
