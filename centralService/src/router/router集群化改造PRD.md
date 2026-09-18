# Router 集群化改造 PRD

## 一、背景与目标

### 1.1 背景
当前 router 是单点部署，所有游戏服注册到同一个 router 上，router 之间没有任何协同能力。随着在线规模扩张，存在以下问题：

- **单点瓶颈**：所有跨服消息转发都集中在单台 router 上，连接数与吞吐有上限
- **故障域过大**：router 一旦宕机，全网跨服消息转发中断，恢复期间业务受损
- **扩展性差**：横向扩容 router 没办法协同，等于多份互不相通的单点

### 1.2 目标
把 router 改造成一个**无主节点的对等集群**：

1. 任意一个 router 节点都能接收游戏服注册
2. 任意一个 router 节点都能接收跨服转发请求，本地能命中就直接转发，本地命中不了就走集群转发
3. router 节点之间对等，**不存在主从**，任何节点宕机不影响集群继续服务
4. 集群元数据（节点地址、游戏服注册信息）通过 **Redis 共享**，不依赖任何单点的协调进程
5. router 之间的连接遵循"小 ID 主动连大 ID"规则，**保证任意两个 router 之间只有一条连接**

### 1.3 非目标
- 不引入 etcd/zookeeper/raft 等额外协调组件
- 不做动态主从选举（节点完全对等，不需要主）
- 不改变游戏服侧的 RPC 协议与调用方式（游戏服视角仍只连一个 router）
- 不重写底层 trpc 框架，沿用现有的 protobuf + 自定义 RpcChannel

---

## 二、总体架构

### 2.1 集群形态

```
           ┌─────────────────────────────────────────────┐
           │                  Redis                       │
           │  (共享集群元数据，5 秒一个 tick 读写)        │
           └─────────────────────────────────────────────┘
                          ▲               ▲
                          │读/写          │读/写
        ┌─────────────────┴──┐      ┌──────┴────────────────┐
        │                    │      │                       │
   ┌────┴─────┐         ┌────┴─────┴──┐               ┌────┴─────┐
   │ Router 1 │◄───────►│   Router 2  │◄─────────────►│ Router 3 │
   │ id=1     │         │   id=2     │               │ id=3     │
   │ :2060    │         │   :2060    │               │ :2060    │
   │ :2061    │         │   :2061    │               │   :2061  │
   └────┬─────┘         └────┬───────┘               └────┬─────┘
        │                    │                            │
   游戏服注册            游戏服注册                    游戏服注册
   (serverId=10,         (serverId=11,                (serverId=12,
    componentId=1)       componentId=1)               componentId=1)
```

### 2.2 节点内部组件

每个 router 节点内部职责划分：

| 组件 | 职责 |
| --- | --- |
| `GameServerService` | 对游戏服提供 RPC（注册、转发），保留现有协议不变 |
| `RouterNodeService` | 对其他 router 节点提供 RPC（集群转发、心跳） |
| `ClusterSyncTick` | 5 秒一次的定时任务：写自己的元数据到 Redis + 读全集群元数据 |
| `ClusterTopology` | 根据元数据 + 小连大规则，维护到其他 router 的连接集合 |
| `ForwardRouter` | DoOnOthersBase 入口，先查本地、再查路由表、最后走集群转发 |

### 2.3 端口规划

每个 router 节点监听两个端口：

| 端口 | 用途 |
| --- | --- |
| `GameServerServiceAddr`（已有，例如 :2060） | 接受游戏服连接，跑 `RouterServer` 服务 |
| `RouterClusterAddr`（新增，例如 :2061） | 接受其他 router 节点连接，跑 `RouterNodeService` |

---

## 三、Redis 数据模型

### 3.1 Key 设计

统一加前缀 `routerCluster:`，避免与其他业务 key 冲突。

#### 3.1.1 router 节点元数据

- Key: `routerCluster:router:<routerId>`
- Type: `Hash`
- 字段：
  - `routerId` (string, 数字)
  - `clusterAddr` (string, 形如 `host:2061`)
  - `gameServerAddr` (string, 形如 `host:2060`, 冗余便于排查)
  - `lastTick` (string, 毫秒时间戳)
- TTL: **15 秒**（连续 3 个 tick 没刷新即视为掉线）
- 写入时机：每个 tick 覆盖写一次

#### 3.1.2 router 节点游戏服注册表

- Key: `routerCluster:routerServers:<routerId>`
- Type: `Hash`
- 字段：`<serverId>:<componentId>` → `1`（值无意义，仅作为存在性标记；元信息已在游戏服注册阶段维护到全局表）
- TTL: **15 秒**，每个 tick 刷新

#### 3.1.3 全局游戏服注册表

- Key: `routerCluster:gameServers`
- Type: `Hash`
- 字段：`<serverId>:<componentId>` → `<routerId>`
- TTL: 不设（仅在删除时显式 DEL），由 router 在游戏服断开时 DEL
- 写入时机：
  - 游戏服成功注册到本地 router 时，写入（值 = 本 router id）
  - 通过同步 tick 发现其他 router 上线时**不需要**回写（仅读取）

### 3.2 Redis 读写约束

1. **写操作**：只在 `ClusterSyncTick` 中批量执行，**业务路径（DoOnOthersBase、RegisterBaseapp 等）不直接写 Redis**，避免热路径上拖慢转发
2. **读操作**：`ClusterSyncTick` 周期读取，缓存在内存的 `globalServerTable` 与 `routerNodesTable` 里，业务路径读内存表
3. **失败容忍**：Redis 抖动/短暂不可用时：
   - 写入失败：下一个 tick 重试，不影响本地服务
   - 读取失败：保留上一份缓存继续服务，报警

---

## 四、配置变更

### 4.1 路由节点配置 (`routerConf.json`)

```json
{
    "serverName": "routerServer",
    "routerId": 1,
    "gameServerServiceAddr": "0.0.0.0:2060",
    "routerClusterAddr": "0.0.0.0:2061",
    "addressForDebug": "localhost:8989",
    "logPath": "router.log",
    "logLevel": 0,
    "logRotateSize": 500,
    "reportAddr": "https://...",
    "redisServer": {
        "addr": "127.0.0.1:6379",
        "username": "",
        "passwd": "",
        "db": "0",
        "maxIdle": 16,
        "maxActive": 16,
        "idleTimeout": 100
    }
}
```

新增字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `routerId` | uint32 | **集群内唯一**，不允许重复，重复则进程直接 panic 退出 |
| `routerClusterAddr` | string | 集群内部监听地址（接其他 router） |
| `redisServer` | object | Redis 连接配置，与 admin/queueServer 等保持结构一致 |

`AppConfig` 结构体扩展（`src/router/routerApp/config.go`）：

```go
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
    GameServerServiceAddr string
    RouterClusterAddr     string
    RouterId              uint32
    AddressForDebug       string
    LogPath               string
    LogLevel              string
    LogRotateSize         string
    RedisServer           RedisServerConfig
}
```

---

## 五、核心流程

### 5.1 启动流程

```
RouterApp.Start()
  ├─ 校验 RouterId 已被配置且非 0
  ├─ 初始化 redis 连接池
  ├─ 启动 GameServerServiceAddr 监听（已存在）
  ├─ 启动 RouterClusterAddr 监听（新增）
  ├─ 启动 ClusterSyncTick（5s）
  ├─ 启动 debug http 服务
  └─ 注册信号处理
```

### 5.2 集群同步 Tick（每 5 秒一次）

```
ClusterSyncTick.Run():
  1. 写自己:
     HSET routerCluster:router:<myRouterId>
       routerId=<myRouterId>
       clusterAddr=<myClusterAddr>
       gameServerAddr=<myGameServerAddr>
       lastTick=<now_ms>
     EXPIRE routerCluster:router:<myRouterId> 15

  2. 写自己当前注册的所有游戏服:
     HSET routerCluster:routerServers:<myRouterId> "<sid>:<cid>" 1
     EXPIRE routerCluster:routerServers:<myRouterId> 15

  3. 写自己在 globalServerTable 里属于自己的条目 (本地游戏服):
     HSET routerCluster:gameServers "<sid>:<cid>" <myRouterId>

  4. 读全集群:
     KEYS/SCAN routerCluster:router:*       → 拿到所有在线 router 元数据
     HGETALL routerCluster:gameServers      → 拿到所有游戏服→router 映射
     每个 router 上线后 HGETALL routerCluster:routerServers:<routerId> → 该 router 上挂的游戏服

  5. 更新内存表:
     routerNodesTable[routerId] = { clusterAddr, lastTick, ... }
     globalServerTable["<sid>:<cid>"] = routerId

  6. 清理过期:
     globalServerTable 中指向已经不在 routerNodesTable 的 routerId → 视为该 router 掉线，
       同步把该 router 上的游戏服从 globalServerTable 中移除（让其他 router 在下个 tick
       能重新登记；不会出现孤儿条目，因为同 serverId+componentId 不会被两个 router 同时登记）

  7. 调整集群拓扑（详见 5.3）

  8. 清理本节点已断开的旧连接（详见 5.4）
```

### 5.3 拓扑建立规则 —— 小 ID 主动连大 ID

```
对 routerNodesTable 里每个 otherRouterId:
  if otherRouterId == myRouterId: continue
  if otherRouterId < myRouterId:
    // 我是大 ID，等对方连我，不要主动连
    // 如果连接不存在（对方刚上线 / 重启），什么都不做
    // 检查 ServerEndPoint 是否还在监听即可（不需要业务动作）
    continue
  if otherRouterId > myRouterId:
    // 我是小 ID，我应该连对方
    if 已经有到 otherRouterId 的连接:
      if 连接健康: 保持
      else:        关闭旧的，触发重连
    else:
      主动 Dial 其他节点的 clusterAddr，建立新连接
```

**结果**：任意两个 router A、B 之间恰好只有一条 TCP 连接，由 `min(A,B)` 那一端发起。

### 5.4 连接生命周期

| 场景 | 处理 |
| --- | --- |
| tick 检测到对方 router 15 秒内未刷新 | 关闭到该 router 的连接、从 `routerNodesTable` 删除 |
| tick 检测到对方 router 重新出现 | 主动重新建立连接（小端） |
| TCP 断开（小端发起重连） | 关闭 `RpcChannel`，下个 tick 触发重连 |
| TCP 断开（大端被动接收连接丢失） | 等小端在下一个 tick 里重连即可 |
| 重连退避 | 简单固定 5s（与 tick 对齐），不引入额外退避，避免复杂度 |

### 5.5 游戏服注册流程（保持原协议不变）

```
GameServerA (sid=10, cid=1) → GameServerServiceAddr → Router#2 (routerId=2)
  Router#2.RegisterBaseapp()
    1. addGameServer 到本地 gameServers map
    2. serversLock 保护下追加到 gameBaseAppsList
    // 注意：这里不再触发任何 Redis 写入，由 5.2 的 tick 异步写入
```

### 5.6 跨服转发流程（核心改动）

```
GameServerA (sid=10) 在 Router#2 上要发消息给 GameServerB (sid=11, cid=1)：

Router#2.DoOnOthersBase(req):
  dstCid := req.componentId
  dstSid := req.dstServerId

  // 1. 本地优先
  if dst := getGameServer(dstSid, dstCid); dst != nil:
      dst.OnRemoteCallFromOthersBase(req)
      recordTraffic(...)
      return

  // 2. 查集群路由表
  routerId := globalServerTable["<dstSid>:<dstCid>"]
  if routerId == 0 || routerId == myRouterId:
      log("目标不存在或不可达")
      return

  // 3. 走集群转发
  node := routerNodesTable[routerId]
  if node == nil || !node.connected:
      log("目标 router 不在线")
      return

  node.client.ForwardToGameServer({
    dstServerId, dstComponentId,
    srcServerId, srcComponentId,
    memoryStream,
  })

  recordTraffic(mySide=sid, dstRouterSide=routerId, ...)
```

```
Router#N (收到 ForwardToGameServer):
  // 把请求原样转给本节点上对应的游戏服
  dst := localGameServers["<sid>:<cid>"]
  if dst == nil:
      // 极小概率：目标游戏服刚断开 / 跨 tick 边界
      log("cluster forward miss", sid, cid)
      return
  dst.OnRemoteCallFromOthersBase(req)
```

### 5.7 游戏服断开

```
RouterApp.removeGameServer():
  // 保留原有的本地清理
  delete gameServers[serviceKey]
  delete channelToHost[uuid]
  remove from gameBaseAppsList

  // 新增：本地表清理后立即从 Redis 全局表中删除对应条目，
  //       避免其他 router 还按老路由转发过来
  //       （下一个 tick 也会因为本地 routerServers hash 里没有该 key 而被覆盖清除，这里做主动删以提速）
  redis.HDEL routerCluster:gameServers "<sid>:<cid>"
```

---

## 六、proto 与 RPC 协议

### 6.1 新增 `routerCluster.proto`

在 `src/router/routerApp/routerCluster/` 下新增 proto 与生成的 rpc/pb 代码。

```proto
syntax = "proto3";
package RouterCluster;
option go_package = "../routerCluster";

// 由转发端发出，目标 router 节点收到后把 payload 转交给本地游戏服
message ClusterForwardRequest {
    uint32 dstServerId     = 1;
    uint32 dstComponentId  = 2;
    uint32 srcServerId     = 3;
    uint32 srcComponentId  = 4;
    bytes  memoryStream    = 5;
}

// 心跳 / 健康检查（小端连上来之后可选调用，目前用 TCP 连接存活作为心跳）
message ClusterPing {
    uint32 fromRouterId = 1;
    uint64 timestamp    = 2;
}

message ClusterPong {
    uint32 fromRouterId = 1;
    uint64 timestamp    = 2;
}

message Void {}

// Router 节点间服务
service RouterNodeService {
    rpc forwardToGameServer(ClusterForwardRequest) returns (Void);
    rpc ping(ClusterPing) returns (ClusterPong);
}
```

### 6.2 不变的部分

- `RouterServer` 服务（游戏服看到的协议）完全不动
- `GameServer` 客户端回调协议完全不动
- 底层 `trpc.RpcChannel` / `ServerEndPoint` / `ClientEndPoint` 完全不动

---

## 七、并发与一致性

### 7.1 锁策略

| 表 | 锁 |
| --- | --- |
| `gameServers` / `channelToHost` / `gameBaseAppsList`（已存在） | `serversLock` RWMutex |
| `globalServerTable` map[string]uint32 | 新增 `globalTableLock` RWMutex |
| `routerNodesTable` map[uint32]*RouterNodeInfo | 新增 `routerNodesLock` RWMutex |
| `trafficStats`（已存在） | 无锁 atomic（保持不变） |

### 7.2 一致性取舍

- **最终一致**：tick 周期是 5 秒，最坏情况一个游戏服掉线后 5 秒内其他 router 还可能转发到老 router，由老 router 上的 `forwardToGameServer` 处理时发现本地没有，丢弃并记日志
- **不接受**：把 Redis 当强一致 KV 在转发路径上同步读写

### 7.3 幂等性

- `RegisterBaseapp` 仍然要求同一个 `(serverId, componentId)` 只能注册一次（已实现）
- 集群转发 `forwardToGameServer` 不要求幂等（业务侧已有自己的去重机制；如果上层的 `OthersBaseRequest` 已经带 seq，由业务负责）

---

## 八、容错

| 故障 | 处理 |
| --- | --- |
| 单个 router 宕机 | 该 router 上的游戏服连接断开，15 秒后其他 router 从 Redis 看到 TTL 过期，清理路由表 |
| Redis 抖动 | tick 写失败下个 tick 重试；读失败保留旧缓存；Redis 长时间不可用时集群退化为"各自为战"，但仍能服务本地游戏服 |
| router 重复启动同 routerId | 启动时校验本地内存表 `globalServerTable`，若已存在本 routerId 但 clusterAddr 不同，记 ERROR 并 panic 退出（避免脑裂） |
| 跨节点转发时对方连接断开 | 在 `forwardToGameServer` 入口发现连接断开 → 丢弃并记日志；调用方路由失败由业务重试 |
| 集群转发 RPC 超时 | 走现有 RpcChannel 10 秒读超时；超时不重试 |

---

## 九、性能影响评估

- 转发热路径 (`DoOnOthersBase`) 增加两次内存查表 (`globalServerTable` + `routerNodesTable`)，均为 RWMutex 读锁，无 Redis 调用，单次增加 < 1µs
- 跨节点转发增加一跳 RpcChannel 调用，沿用现有 RPC 框架，无额外序列化开销
- Tick 路径每秒最多触发一次 Redis 写入（合并后），连接数 N ≤ 32 时单次写开销可忽略

---

## 十、上线步骤

1. 编写 `routerCluster.proto` 并生成 `rpc.go` / `pb.go`
2. 扩展 `AppConfig` 与 `routerConf.json` schema
3. 实现 `ClusterSyncTick`、`ClusterTopology`、`RouterNodeService` 三个新组件
4. 修改 `RouterApp`：
   - 启动时多监听一个端口
   - `DoOnOthersBase` 加集群转发分支
   - `removeGameServer` 增加 Redis HDEL
5. 单 router 启动 → Redis 中能查到自己的元数据 → 与不集群化前行为一致
6. 双 router 启动（小 ID 一端主动连大 ID 一端）→ DoOnOthersBase 跨节点转发跑通
7. 模拟某 router kill -9 → 15 秒后另一端清理掉对应路由，老连接断开
8. 恢复后重新加入集群

---

## 十一、未来可扩展项（不在本次范围内）

- 基于 Redis Stream / pub-sub 实现秒级事件推送，替代 5s tick
- router 节点动态扩缩容时由中心服下发新配置
- 集群级流量统计聚合
- 多机房部署时按机房做 router 分组，避免跨机房转发

