package common

import (
	"centralService/src/appLog"
	"context"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"sort"
	"sync"
	"sync/atomic"
	"time"

	"github.com/gomodule/redigo/redis"
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

// RedisGetConnTimeout 是业务调用方从池中获取连接的超时。
// 沿用 RedisOpTimeout。设得太短会在池子偶发排队时误杀请求；
// 设得太长又会让泄漏路径下的 goroutine 长时间占着 RPC 通道。
// 5s 是经验值，覆盖了大部分正常 redis 抖动场景。
const RedisGetConnTimeout = RedisOpTimeout

const (
	// redisMetricsWindowSize 是平均连接持有时长的统计窗口长度。
	redisMetricsWindowSize = 60 * time.Second
	// redisMetricsBucketSize 是滑动窗口里单个 bucket 的时间跨度。
	// bucketNum = WindowSize / BucketSize 必须能被整除。
	redisMetricsBucketSize = 10 * time.Second
	// redisMetricsBucketNum 是滑动窗口里 bucket 的数量。
	redisMetricsBucketNum = 6

	// slowHoldThreshold 是慢持有记录的判定门槛。Close 时若发现持有时长
	// 超过这个值就尝试挤进 Top5 排名，进程级持久。
	slowHoldThreshold = 500 * time.Millisecond
	// slowHoldTopN 是慢持有保留的数量。
	slowHoldTopN = 5
)

var (
	tracedConnIDCounter uint64

	tracedConnsMu sync.Mutex
	tracedConns   = map[uint64]*tracedConn{}

	poolRegistryMu sync.RWMutex
	poolRegistry   = map[*redis.Pool]string{}

	redisMetricsMu sync.RWMutex
	redisMetrics   = map[string]*redisPoolMetrics{}
)

// redisPoolBucket 记录一个 bucket 周期内的累计持有时长与次数。
type redisPoolBucket struct {
	holdNanos uint64
	holdCount uint64
}

// slowHoldRecord 记录一次持有时长 > slowHoldThreshold 的借出，进程级 Top5 用。
type slowHoldRecord struct {
	id         uint64
	poolName   string
	borrower   string
	hold       time.Duration
	borrowedAt time.Time
}

// redisPoolMetrics 用环形 bucket 数组实现"最近 60 秒"的滑动窗口平均。
// 每次写入前先按需 rotate，把过期 bucket 清零，避免无限增长。
// slowHolds 是进程级 Top5，按 hold 降序维护，slowCount 标记已填充槽位。
type redisPoolMetrics struct {
	poolName       string
	mu             sync.Mutex
	buckets        [redisMetricsBucketNum]redisPoolBucket
	curIdx         int
	lastRotateTime time.Time

	slowHolds [slowHoldTopN]*slowHoldRecord
	slowCount int
}

// recordHold 把一次连接持有时长写入当前 bucket。
func (m *redisPoolMetrics) recordHold(d time.Duration) {
	if d < 0 {
		d = 0
	}
	m.mu.Lock()
	m.rotateLocked(time.Now())
	m.buckets[m.curIdx].holdNanos += uint64(d.Nanoseconds())
	m.buckets[m.curIdx].holdCount++
	m.mu.Unlock()
}

// recordSlowHold 尝试把一条慢持有记录挤入 Top5（按 hold 降序，进程级持久）。
// 只有超过 slowHoldThreshold 的借出才会进来；满了之后只有更大的才能顶替。
// K=5，插入排序开销可忽略。
func (m *redisPoolMetrics) recordSlowHold(rec *slowHoldRecord) {
	if rec.hold < slowHoldThreshold {
		return
	}
	m.mu.Lock()
	defer m.mu.Unlock()
	if rec.borrower == "" {
		return
	}
	if m.slowCount >= slowHoldTopN {
		// 找最弱者
		minIdx := 0
		for i := 1; i < slowHoldTopN; i++ {
			if m.slowHolds[i].hold < m.slowHolds[minIdx].hold {
				minIdx = i
			}
		}
		if rec.hold <= m.slowHolds[minIdx].hold {
			return
		}
		m.slowHolds[minIdx] = rec
	} else {
		m.slowHolds[m.slowCount] = rec
		m.slowCount++
	}
	// 简单插入排序，保持降序。
	for i := 1; i < m.slowCount; i++ {
		for j := i; j > 0 && m.slowHolds[j].hold > m.slowHolds[j-1].hold; j-- {
			m.slowHolds[j], m.slowHolds[j-1] = m.slowHolds[j-1], m.slowHolds[j]
		}
	}
}

// SnapshotSlowHolds 返回当前 Top5 的副本（按 hold 降序），供日志输出。
func (m *redisPoolMetrics) SnapshotSlowHolds() []*slowHoldRecord {
	m.mu.Lock()
	defer m.mu.Unlock()
	out := make([]*slowHoldRecord, 0, m.slowCount)
	for i := 0; i < m.slowCount; i++ {
		if m.slowHolds[i] != nil {
			out = append(out, m.slowHolds[i])
		}
	}
	return out
}

// Snapshot 返回当前滑动窗口内的累计 hold 次数与总纳秒。
// 调用方用 holdNanos/holdCount 计算平均持有时长。
func (m *redisPoolMetrics) Snapshot() (count uint64, nanos uint64) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.rotateLocked(time.Now())
	var totalNanos, totalCount uint64
	for _, b := range m.buckets {
		totalNanos += b.holdNanos
		totalCount += b.holdCount
	}
	return totalCount, totalNanos
}

// rotateLocked 在持锁状态下推进 curIdx 并清零被覆盖的 bucket。
// 处理"步进 >= bucketNum"（长时间静默后一次性清空整个窗口）的边界情况。
func (m *redisPoolMetrics) rotateLocked(now time.Time) {
	if m.lastRotateTime.IsZero() {
		m.lastRotateTime = now.Truncate(redisMetricsBucketSize)
		return
	}
	elapsed := now.Sub(m.lastRotateTime)
	if elapsed < redisMetricsBucketSize {
		return
	}
	steps := int(elapsed / redisMetricsBucketSize)
	if steps > redisMetricsBucketNum {
		steps = redisMetricsBucketNum
	}
	for i := 0; i < steps; i++ {
		m.curIdx = (m.curIdx + 1) % redisMetricsBucketNum
		m.buckets[m.curIdx] = redisPoolBucket{}
	}
	m.lastRotateTime = m.lastRotateTime.Add(time.Duration(steps) * redisMetricsBucketSize)
}

// newRedisPoolMetrics 创建一个新的 per-pool 滑动窗口指标，并注册到全局 map。
func newRedisPoolMetrics(poolName string) *redisPoolMetrics {
	m := &redisPoolMetrics{
		poolName:       poolName,
		lastRotateTime: time.Now().Truncate(redisMetricsBucketSize),
	}
	redisMetricsMu.Lock()
	redisMetrics[poolName] = m
	redisMetricsMu.Unlock()
	return m
}

// tracedConn wraps whatever Pool.GetContext returns (typically *activeConn
// from redigo's pool.go) so we can record hold time on Close (for sliding-window
// metrics) and keep an entry in the global registry for the stuck-detector.
//
// All redis.Conn methods except Close are auto-forwarded through the embedded
// interface; Close is overridden to record metrics before delegating.
//
// 注意：redigo v1.9.3 的 Pool.GetContext 返回的是 *activeConn（redigo 自己的
// 内部包装，把用户 Dial 返回的 conn 埋在 activeConn.pc.c 里）。所以这个 wrapper
// 必须裹在 Pool.GetContext 之后、包在用户业务代码之前，Close 才能被触发。
type tracedConn struct {
	redis.Conn
	id         uint64
	poolName   string
	metrics    *redisPoolMetrics
	borrower   string
	borrowedAt time.Time
}

// Close 是连接生命周期的终点（被业务 defer conn.Close() 调用）：
//   1. 记一次持有时长到所属 pool 的滑动窗口；
//   2. 从全局注册表摘掉自己，避免长时间运行后 map 无限增长；
//   3. 调内层 *activeConn.Close() 把连接还回 redigo 池。
//
// setBorrower/Close 共同构成"set once / clear once"配对，期间无并发写，
// 不需要锁。snapshotBorrower 在 stuck-detector 里被并发读，存在读撕裂风险，
// 但只影响诊断日志，不影响功能。
func (c *tracedConn) Close() error {
	if !c.borrowedAt.IsZero() {
		d := time.Since(c.borrowedAt)
		if c.metrics != nil {
			c.metrics.recordHold(d)
			if d >= slowHoldThreshold {
				c.metrics.recordSlowHold(&slowHoldRecord{
					id:         c.id,
					poolName:   c.poolName,
					borrower:   c.borrower,
					hold:       d,
					borrowedAt: c.borrowedAt,
				})
			}
		}
		c.borrower = ""
		c.borrowedAt = time.Time{}
	}
	tracedConnsMu.Lock()
	delete(tracedConns, c.id)
	tracedConnsMu.Unlock()
	return c.Conn.Close()
}

func (c *tracedConn) setBorrower(b string, t time.Time) {
	c.borrower = b
	c.borrowedAt = t
}

func (c *tracedConn) snapshotBorrower() (string, time.Time) {
	return c.borrower, c.borrowedAt
}

func newTracedConn(inner redis.Conn, poolName string, metrics *redisPoolMetrics) *tracedConn {
	id := atomic.AddUint64(&tracedConnIDCounter, 1)
	tc := &tracedConn{
		Conn:     inner,
		id:       id,
		poolName: poolName,
		metrics:  metrics,
	}
	tracedConnsMu.Lock()
	tracedConns[id] = tc
	tracedConnsMu.Unlock()
	return tc
}

type borrowInfo struct {
	id         uint64
	poolName   string
	borrower   string
	borrowedAt time.Time
}

// topOldestBorrows 扫描所有 tracedConn，按 borrowedAt 升序取前 n 个"当前被持有"的连接。
func topOldestBorrows(n int) []borrowInfo {
	tracedConnsMu.Lock()
	snap := make([]borrowInfo, 0, len(tracedConns))
	for _, tc := range tracedConns {
		b, t := tc.snapshotBorrower()
		if b == "" {
			continue
		}
		snap = append(snap, borrowInfo{
			id:         tc.id,
			poolName:   tc.poolName,
			borrower:   b,
			borrowedAt: t,
		})
	}
	tracedConnsMu.Unlock()
	sort.Slice(snap, func(i, j int) bool { return snap[i].borrowedAt.Before(snap[j].borrowedAt) })
	if len(snap) > n {
		snap = snap[:n]
	}
	return snap
}

func registerPool(pool *redis.Pool, name string) {
	poolRegistryMu.Lock()
	poolRegistry[pool] = name
	poolRegistryMu.Unlock()
}

func poolNameOf(pool *redis.Pool) string {
	poolRegistryMu.RLock()
	defer poolRegistryMu.RUnlock()
	if name, ok := poolRegistry[pool]; ok {
		return name
	}
	return "<unknown>"
}

// callerInfo 保留但不再被 GetRedisConn 使用：tag 化之后，慢持有 Top5
// 直接显示业务方传入的 tag，比 runtime.Caller 拿到的栈帧更稳定可控。
// 这里保留一个空实现，避免被无意义代码误删。
func callerInfo(skip int) string {
	pc, file, line, ok := runtime.Caller(skip + 1)
	if !ok {
		return "unknown"
	}
	fn := runtime.FuncForPC(pc)
	name := "?"
	if fn != nil {
		name = fn.Name()
	}
	return fmt.Sprintf("%s:%d [%s]", filepath.Base(file), line, name)
}

func NewRedisPool(opts RedisPoolOptions) *redis.Pool {
	if opts.MaxIdle <= 0 {
		opts.MaxIdle = 16
	}
	if opts.MaxActive <= 0 {
		opts.MaxActive = 500
	}
	if opts.IdleTimeout <= 0 {
		opts.IdleTimeout = 100
	}

	metrics := newRedisPoolMetrics(opts.ServerName)

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
		// 不在 TestOnBorrow 里做 PING：PING 会阻塞调用方最长 ReadTimeout 秒，
		// 慢 Redis 下容易把业务请求拖到 10s。改由 IdleTimeout 主动回收老连接。
		TestOnBorrow: nil,
	}

	registerPool(pool, opts.ServerName)

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
			// 滑动窗口内的平均连接持有时长：每次成功健康检查都打印，便于实时观察。
			holdCount, holdNanos := metrics.Snapshot()
			if holdCount > 0 {
				avgMs := float64(holdNanos) / float64(holdCount) / 1e6
				appLog.Infof("[%s] [slow-hold] redis avg conn hold over last %ds: %.2fms (%d borrows)",
					opts.ServerName, int64(redisMetricsWindowSize/time.Second), avgMs, holdCount)
			}
			// 进程级慢持有 Top5：>slowHoldThreshold 的最慢 N 条借出，便于定位
			// "为什么平均时长被拉这么高"的具体持有点。所有行均带 [slow-hold] tag，
			// 运维可用 grep '\[slow-hold\]' 直接过滤。
			slows := metrics.SnapshotSlowHolds()
			if len(slows) > 0 {
				appLog.Infof("[%s] [slow-hold] top %d borrows (>%dms):",
					opts.ServerName, len(slows), slowHoldThreshold/time.Millisecond)
				for i, s := range slows {
					appLog.Infof("[%s]   [slow-hold] [#%d] id=%d hold=%.2fms since=%s by %s",
						opts.ServerName, i+1, s.id,
						float64(s.hold)/float64(time.Millisecond),
						s.borrowedAt.Format("15:04:05.000"), s.borrower)
				}
			}
			if okTicks%60 == 0 {
				stats := pool.Stats()
				appLog.Infof("[%s] redis health check ok, addr=%s, active=%d/%d idle=%d",
					opts.ServerName, opts.Addr, stats.ActiveCount, opts.MaxActive, stats.IdleCount)
			}
		}
	}()

	startRedisPoolStuckDetector(pool, opts)

	return pool
}

// GetRedisConn 从 redis 池中获取一个连接，带 RedisGetConnTimeout 超时。
// 业务调用方应使用本函数而不是直接 pool.Get()，避免池子被占满时 goroutine 长时间阻塞。
// 调用方需自行 defer conn.Close() 归还连接；本函数会返回 *tracedConn，
// 业务 Close 时会自动记录持有时长到所属 pool 的滑动窗口指标。
//
// tag 用来标识调用方（"哪个业务点借的连接"），在慢持有 Top5 / stuck-detector
// 日志里直接显示出来。强烈建议按 包名.函数名[子场景] 命名，方便按 tag 聚合。
// 不要再用 runtime.Caller 拿栈帧了：内联 / 编译器优化会让 skip 计数漂移。
func GetRedisConn(pool *redis.Pool, tag string) (redis.Conn, error) {
	if tag == "" {
		tag = "untagged"
	}
	ctx, cancel := context.WithTimeout(context.Background(), RedisGetConnTimeout)
	defer cancel()
	rawConn, err := pool.GetContext(ctx)
	if err != nil {
		return nil, err
	}
	poolName := poolNameOf(pool)
	tc := newTracedConn(rawConn, poolName, poolMetricsFor(poolName))
	tc.setBorrower(tag, time.Now())
	appLog.Debugf("[redis] acquire id=%d pool=%s by %s", tc.id, tc.poolName, tag)
	return tc, nil
}

// poolMetricsFor 通过 pool 名查找所属的滑动窗口指标。
// pool 名不在 NewRedisPool 注册表里时返回 nil（recordHold 内部对此做了安全跳过）。
func poolMetricsFor(poolName string) *redisPoolMetrics {
	redisMetricsMu.RLock()
	defer redisMetricsMu.RUnlock()
	return redisMetrics[poolName]
}

// startRedisPoolStuckDetector 监控 redis 池：若连续多轮都处于"满载"状态，
// 输出 WARN + 写一份 goroutine dump 到临时目录，便于事后定位泄漏点。
// opts.MaxActive 为 0 时退化为 100。
func startRedisPoolStuckDetector(pool *redis.Pool, opts RedisPoolOptions) {
	maxActive := opts.MaxActive
	if maxActive <= 0 {
		maxActive = 100
	}
	const (
		checkInterval    = 60 * time.Second
		stuckThreshold   = 5 // 连续 5 * 60s = 5 分钟满载
		recoverThreshold = 3 // 恢复后至少 3 轮稳定才视为真恢复
	)
	go func() {
		ticker := time.NewTicker(checkInterval)
		defer ticker.Stop()
		var stuckCount, recoverStable int
		for range ticker.C {
			stats := pool.Stats()
			if stats.ActiveCount >= maxActive {
				stuckCount++
				recoverStable = 0
				if stuckCount == stuckThreshold {
					appLog.Warnf("[%s] redis pool stuck for %d minutes, active=%d/%d idle=%d goroutines=%d",
						opts.ServerName, stuckCount, stats.ActiveCount, maxActive,
						stats.IdleCount, runtime.NumGoroutine())
					for i, b := range topOldestBorrows(5) {
						appLog.Warnf("  [#%d] id=%d borrowedAt=%s duration=%s by %s",
							i+1, b.id, b.borrowedAt.Format(time.RFC3339),
							time.Since(b.borrowedAt).Truncate(time.Second), b.borrower)
					}
					buf := make([]byte, 1<<20)
					n := runtime.Stack(buf, true)
					dumpPath := filepath.Join(os.TempDir(),
						fmt.Sprintf("redis_pool_stuck_%s_%d.dump", opts.ServerName, time.Now().Unix()))
					if err := os.WriteFile(dumpPath, buf[:n], 0644); err != nil {
						appLog.Errorf("[%s] write goroutine dump failed: %s", opts.ServerName, err.Error())
					} else {
						appLog.Warnf("[%s] goroutine dump written to %s", opts.ServerName, dumpPath)
					}
				}
				continue
			}
			if stuckCount > 0 {
				recoverStable++
				if recoverStable >= recoverThreshold {
					appLog.Infof("[%s] redis pool recovered, was stuck for %d minutes, active=%d/%d idle=%d",
						opts.ServerName, stuckCount, stats.ActiveCount, maxActive, stats.IdleCount)
					stuckCount = 0
				}
			}
		}
	}()
}
