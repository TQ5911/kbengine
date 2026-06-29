package Queue

import (
	"centralService/src/appLog"
	"errors"
	"strconv"
	"sync"
	"time"

	"github.com/garyburd/redigo/redis"
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
	WaitMapCacheTTL          = 30 * time.Second
)

type WaitMapServerMgr struct {
	app           *QueueApp
	cachedServers map[string]int
	lastQueryTime time.Time
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
// 5 秒内重复查询会返回缓存数据，减少对 Redis 的压力
// key 为 serverId 字符串，value 为空闲人数
func (self *WaitMapServerMgr) GetAliveFreeServers() (map[string]int, error) {
	self.mu.RLock()
	if len(self.cachedServers) > 0 && time.Since(self.lastQueryTime) < WaitMapCacheTTL {
		cached := self.copyCachedServersLocked()
		self.mu.RUnlock()
		return cached, nil
	}
	self.mu.RUnlock()

	self.mu.Lock()
	defer self.mu.Unlock()

	// 双重检查，避免并发请求重复查询 Redis
	if len(self.cachedServers) > 0 && time.Since(self.lastQueryTime) < WaitMapCacheTTL {
		return self.copyCachedServersLocked(), nil
	}

	conn := self.app.redisPool.Get()
	defer conn.Close()

	// 读取所有等待服的心跳
	members, err := redis.Strings(conn.Do("ZRANGE", WaitMapHeartbeatKey, 0, -1, "WITHSCORES"))
	if err != nil {
		appLog.Error("WaitMapServerMgr GetAliveFreeServers zrange failed", err.Error())
		// Redis 异常时，如果有缓存则返回过期缓存作为兜底
		if len(self.cachedServers) > 0 {
			return self.copyCachedServersLocked(), nil
		}
		return nil, err
	}

	self.cachedServers = make(map[string]int, 4)
	nowTs := time.Now().Unix()

	for i := 0; i+1 < len(members); i += 2 {
		serverIdStr := members[i]
		scoreStr := members[i+1]

		_, err := strconv.ParseUint(serverIdStr, 10, 32)
		if err != nil {
			appLog.Warnw("WaitMapServerMgr GetAliveFreeServers invalid serverId", "serverId", serverIdStr, "error", err.Error())
			continue
		}
		score, err := strconv.ParseInt(scoreStr, 10, 64)
		if err != nil {
			appLog.Warnw("WaitMapServerMgr GetAliveFreeServers invalid score", "serverId", serverIdStr, "score", scoreStr, "error", err.Error())
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

		self.cachedServers[serverIdStr] = freeNum
		appLog.Debugw("WaitMapServerMgr GetAliveFreeServers alive server", "serverId", serverIdStr, "freeNum", freeNum)
	}

	self.lastQueryTime = time.Now()

	if len(self.cachedServers) == 0 {
		return nil, errors.New("no alive wait map server")
	}

	return self.copyCachedServersLocked(), nil
}

// copyCachedServersLocked 在已加锁的前提下拷贝缓存数据
func (self *WaitMapServerMgr) copyCachedServersLocked() map[string]int {
	result := make(map[string]int, len(self.cachedServers))
	for k, v := range self.cachedServers {
		result[k] = v
	}
	return result
}
