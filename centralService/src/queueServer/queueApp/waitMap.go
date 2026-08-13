package Queue

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"context"
	"errors"
	"strconv"
	"sync"
	"time"

	"github.com/gomodule/redigo/redis"
)

const (
	WaitMapStateSuccess       = 0
	WaitMapStateNoConfig      = 1
	WaitMapStateInvalidParam  = 2
	WaitMapStateFullOrOffline = 3
)

const (
	WaitMapHeartbeatKey      = "waitmap:heartbeat"
	WaitMapFreeKeyPrefix     = "waitmap:free:"
	WaitMapOfflineTimeoutSec = 20
	WaitMapRefreshInterval   = 5 * time.Second
)

type WaitMapServerMgr struct {
	app           *QueueApp
	cachedServers map[string]int
	mu            sync.RWMutex
}

func NewWaitMapServerMgr(app *QueueApp) *WaitMapServerMgr {
	return &WaitMapServerMgr{
		app:           app,
		cachedServers: make(map[string]int, 4),
	}
}

// GetAliveFreeServers 返回当前存活的等待服及其空闲人数
// 服务发现直接依赖 Redis zset，无需额外配置等待服列表
// 数据由后台定时器每 5 秒从 Redis 刷新到缓存，此处只读缓存，支持高并发
// key 为 serverId 字符串，value 为空闲人数
func (self *WaitMapServerMgr) GetAliveFreeServers() (map[string]int, error) {
	self.mu.RLock()
	defer self.mu.RUnlock()

	if len(self.cachedServers) == 0 {
		return nil, errors.New("no alive wait map server")
	}

	return self.copyCachedServersLocked(), nil
}

// Start 启动后台刷新定时器，先同步刷新一次，避免启动初期缓存为空
func (self *WaitMapServerMgr) Start() {
	self.refreshServers()
	go func() {
		ticker := time.NewTicker(WaitMapRefreshInterval)
		defer ticker.Stop()
		for range ticker.C {
			self.refreshServers()
		}
	}()
}

// refreshServers 从 Redis 查询存活等待服并刷新缓存
// Redis 操作在锁外执行，仅在替换缓存时加写锁；失败时保留旧缓存作为兜底
func (self *WaitMapServerMgr) refreshServers() {
	appLog.Debugw("refresh wait servers.")
	ctx, cancel := context.WithTimeout(context.Background(), common.RedisOpTimeout)
	conn, err := self.app.redisPool.GetContext(ctx)
	cancel()
	if err != nil {
		appLog.Error("WaitMapServerMgr refreshServers get conn failed", err.Error())
		return
	}
	defer conn.Close()

	// 读取所有等待服的心跳
	members, err := redis.Strings(conn.Do("ZRANGE", WaitMapHeartbeatKey, 0, -1, "WITHSCORES"))
	if err != nil {
		appLog.Error("WaitMapServerMgr refreshServers zrange failed", err.Error())
		return
	}

	servers := make(map[string]int, 4)
	nowTs := time.Now().Unix()

	for i := 0; i+1 < len(members); i += 2 {
		serverIdStr := members[i]
		scoreStr := members[i+1]

		_, err := strconv.ParseUint(serverIdStr, 10, 32)
		if err != nil {
			appLog.Warnw("WaitMapServerMgr refreshServers invalid serverId", "serverId", serverIdStr, "error", err.Error())
			continue
		}
		score, err := strconv.ParseInt(scoreStr, 10, 64)
		if err != nil {
			appLog.Warnw("WaitMapServerMgr refreshServers invalid score", "serverId", serverIdStr, "score", scoreStr, "error", err.Error())
			continue
		}
		if nowTs-score > WaitMapOfflineTimeoutSec {
			continue
		}

		freeNum, err := redis.Int(conn.Do("get", WaitMapFreeKeyPrefix+serverIdStr))
		if err != nil {
			// 心跳存在但 free key 不存在，认为空闲人数未知，按 0 处理
			freeNum = 0
		}
		if freeNum < 0 {
			freeNum = 0
		}

		servers[serverIdStr] = freeNum
		appLog.Debugw("WaitMapServerMgr refreshServers alive server", "serverId", serverIdStr, "freeNum", freeNum)
	}

	self.mu.Lock()
	self.cachedServers = servers
	self.mu.Unlock()
}

// copyCachedServersLocked 在已加锁的前提下拷贝缓存数据
func (self *WaitMapServerMgr) copyCachedServersLocked() map[string]int {
	result := make(map[string]int, len(self.cachedServers))
	for k, v := range self.cachedServers {
		result[k] = v
	}
	return result
}
