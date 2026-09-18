package Router

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"encoding/json"
	"strconv"
	"time"

	"github.com/gomodule/redigo/redis"
)

// Redis 中只维护一份数据：单个 Hash，field 是 routerId，value 是该 router 的 meta JSON。
// router 进程只在 ClusterSyncTick 中写这个 hash；不在转发热路径上访问 Redis。
const (
	routerClusterKey        = "routerCluster:routers"
	routerClusterKeyTTL     = 15 * time.Second
	clusterSyncTickInterval = 5 * time.Second
)

// routerMetaStaleTTL: 路由 meta 中 LastTickMs 距今超过该阈值时，认为该 meta 不可信，
// 在计算 serverId→routerId 路由表、调整 cluster 连接时均忽略。
const routerMetaStaleTTL = 1 * time.Minute

func doWithConn(pool *redis.Pool, fn func(redis.Conn) error) error {
	conn, err := common.GetRedisConn(pool, "router.cluster.tick")
	if err != nil {
		return err
	}
	defer conn.Close()
	return fn(conn)
}

// routerMetaPayload 是写入 Redis 的 JSON 序列化格式。
type routerMetaPayload struct {
	ClusterAddr   string   `json:"clusterAddr"`
	GameServerIds []uint32 `json:"gameServerIds"`
	LastTickMs    int64    `json:"lastTickMs"`
}

func writeAllRouters(pool *redis.Pool, myId uint32, myPayload string) error {
	return doWithConn(pool, func(c redis.Conn) error {
		if _, err := c.Do("HSET", routerClusterKey, myId, myPayload); err != nil {
			return err
		}
		_, err := c.Do("PEXPIRE", routerClusterKey, int64(routerClusterKeyTTL/time.Millisecond))
		return err
	})
}

func readAllRouters(pool *redis.Pool) (map[uint32]*routerMetaPayload, error) {
	result := make(map[uint32]*routerMetaPayload)
	nowMs := time.Now().UnixMilli()
	staleMs := int64(routerMetaStaleTTL / time.Millisecond)
	err := doWithConn(pool, func(c redis.Conn) error {
		vals, err := redis.Values(c.Do("HGETALL", routerClusterKey))
		if err != nil {
			return err
		}
		for i := 0; i+1 < len(vals); i += 2 {
			field, _ := redis.String(vals[i], nil)
			value, _ := redis.String(vals[i+1], nil)
			id, perr := strconv.ParseUint(field, 10, 32)
			if perr != nil {
				continue
			}
			var p routerMetaPayload
			if jerr := json.Unmarshal([]byte(value), &p); jerr != nil {
				appLog.Warnf("routerCluster: invalid meta payload for routerId=%d: %s", id, jerr.Error())
				continue
			}
			// LastTickMs 超过 routerMetaStaleTTL 的 meta 视为不可信，直接跳过
			if p.LastTickMs > 0 && nowMs-p.LastTickMs > staleMs {
				// appLog.Warnf("routerCluster: skip stale meta, routerId=%d lastTickMs=%d age=%dms",
				// 	id, p.LastTickMs, nowMs-p.LastTickMs)
				continue
			}
			result[uint32(id)] = &p
		}
		return nil
	})
	return result, err
}

// collectLocalServerIdsAndJSON: 把本节点 gameServerIds 与 clusterAddr 序列化成 JSON 字符串。
// caller 负责把游戏服列表（去重 serverId）传入。
func buildMyMetaJSON(clusterAddr string, ids []uint32, lastTickMs int64) (string, error) {
	p := routerMetaPayload{
		ClusterAddr:   clusterAddr,
		GameServerIds: ids,
		LastTickMs:    lastTickMs,
	}
	b, err := json.Marshal(p)
	if err != nil {
		return "", err
	}
	return string(b), nil
}
