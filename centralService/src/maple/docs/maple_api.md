# Maple 服务 HTTP API 完整文档

> 源码位置：`src/maple/mapleApp/mapleHttpService.go`（路由注册见 `start()`，第 754-772 行）
> 配置文件：`bin/maple/maple.json`（`httpAddr` 默认 `0.0.0.0:9527`，`secret` 为签名密钥）

---

## 一、服务概述

Maple 是游戏服/分区（zone）基础数据的中心存储服务，数据落 MySQL（库名 `maple`），对外只提供 HTTP JSON 接口。

| 项目 | 说明 |
|---|---|
| 协议 | HTTP/1.1，JSON（`application/json; charset=utf-8`） |
| 默认监听 | `0.0.0.0:9527`（配置项 `httpAddr`） |
| 鉴权 | HMAC-SHA256 签名（仅写接口与 `/export` 需要） |
| CORS | 全部接口支持，`OPTIONS` 预检由 `corsMiddleware` 统一返回 200 |
| 存储 | MySQL：`maple` / `maple_zone` / `maple_kv` / `maple_merge_server` |

### 数据表结构（`bin/maple/up.sql`）

| 表 | 主键 | 用途 |
|---|---|---|
| `maple` | `id` 自增，`server_id` 唯一 | 游戏服列表 |
| `maple_zone` | `id` 自增，`zone_id` 唯一 | 分区列表 |
| `maple_kv` | `key` | 自定义键值对 |
| `maple_merge_server` | `from_server_id` | 和服映射（from 被合入服 → to 目标服），每服最多一条出边 |

---

## 二、通用鉴权（仅部分接口）

需要鉴权的接口：`/import` `/export` `/addZone` `/removeZone` `/updateZone` `/updateServer` `/removeServer` `/updateKV` `/addMergeServer` `/removeMergeServer`
无需鉴权的接口：`/getAllServer` `/getAllZoneData` `/getAllMergeServer`

### 请求头

| Header | 必填 | 说明 |
|---|---|---|
| `ts` | 是 | 当前 UNIX 秒级时间戳，与服务端偏差必须在 **±10 秒** 内，否则 401 |
| `nc` | 是 | 随机数/随机串（nonce），建议 6 位随机数 |
| `sign` | 是 | 签名，见下 |
| `Content-Type` | 有 body 时 | `application/json` |

### 签名算法

```
plain = method + ts + nc          // method 为实际 HTTP 方法，大写，如 "POST"、"GET"
sign  = hex( HMAC_SHA256(secret, plain) )   // 小写十六进制
```

- `secret` 来自服务端配置 `maple.json` 的 `secret`（示例为 `hello world`），客户端必须一致。
- `method` 必须与实际请求方法一致（服务端用 `r.Method` 参与验签）。
- 验签失败 / `ts` 非法 → `401 Unauthorized`，body 为 `unauthorized`（`handleAuth`，`mapleHttpService.go:32`）。

### 签名示例

**bash（cURL）：**

```bash
SECRET="hello world"
METHOD="POST"
TS=$(date +%s)
NC=$RANDOM
PLAIN="${METHOD}${TS}${NC}"
SIGN=$(printf "%s" "$PLAIN" | openssl dgst -sha256 -hmac "$SECRET" -binary | xxd -p -c 256)

curl -X POST "http://<host>:9527/addZone" \
  -H "Content-Type: application/json" \
  -H "ts: ${TS}" -H "nc: ${NC}" -H "sign: ${SIGN}" \
  -d '{"zone_id":1001,"zone_name":"一服-天穹"}'
```

**Python：**

```python
import time, random, hmac, hashlib, requests

def auth_headers(method: str, secret: str = "hello world"):
    ts = str(int(time.time()))
    nc = str(random.randint(100000, 999999))
    sign = hmac.new(secret.encode(), (method + ts + nc).encode(), hashlib.sha256).hexdigest()
    return {"Content-Type": "application/json", "ts": ts, "nc": nc, "sign": sign}
```

### CORS 响应头

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: *
（写接口另附）Access-Control-Allow-Headers: Authorization, ts, nc, sign, Content-Type
```

---

## 三、公共数据模型

### Server（游戏服对象）

```json
{
  "id": 1,
  "server_name": "S1",
  "zone_id": 100,
  "zone_name": "一区",
  "game_server": "10.0.0.1:7001",
  "queue_server": "10.0.0.2:8001",
  "central_login": "10.0.0.5:9001",
  "server_group": 1,
  "server_state": 1,
  "server_flag_state": 3,
  "alias": "s1-a",
  "start_time": 1700000000
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | int | 游戏服唯一 ID（对应 `maple.server_id`，唯一键） |
| `server_name` | string | 服务器名 |
| `zone_id` | int | 所属分区 ID |
| `zone_name` | string | 分区名（服务端由 `maple_zone` 关联填充；写接口也接受此字段并会插入 zone） |
| `game_server` | string | 游戏服地址 `ip:port` |
| `queue_server` | string | 排队服地址 `ip:port` |
| `central_login` | string | 中央登录服地址 `ip:port` |
| `server_group` | int | 逻辑组别（跨组校验/货架过滤依据） |
| `server_state` | int | 服务器状态 |
| `server_flag_state` | int | 状态标志位，**位掩码**（第 n 位代表第 n 个 flag，导入脚本用 `1 << n` 组装） |
| `alias` | string | 别名 |
| `start_time` | int64 | 开服时间（秒级时间戳，缺省 0） |

### ZoneData（分区对象）

```json
{ "zone_id": 1001, "zone_name": "一服-天穹" }
```

### AddMergeRequest（和服映射请求）

```json
{ "from_server_id": 10002, "to_server_id": 10001 }
```

- `from_server_id`：被合入（被合并掉）的服
- `to_server_id`：合入目标服
- 每服最多一条出边（DB 主键 `from_server_id` 保证）

---

## 四、接口清单总览

| # | 方法 | 路径 | 鉴权 | 功能 | 返回 |
|---|---|---|---|---|---|
| 1 | GET | `/getAllServer` | 否 | 全量拉取 服务器+分区+KV | JSON |
| 2 | GET | `/getAllZoneData` | 否 | 拉取全部分区 | JSON |
| 3 | GET | `/getAllMergeServer` | 否 | 拉取折叠后的和服映射 | JSON |
| 4 | POST | `/export` | 是 | 导出全量服务器数据 | JSON |
| 5 | POST* | `/import` | 是 | 全量导入（清空后重写） | 文本 |
| 6 | POST | `/addZone` | 是 | 新增分区 | 文本 |
| 7 | POST | `/removeZone` | 是 | 删除分区 | 文本 |
| 8 | POST | `/updateZone` | 是 | 更新分区名 | 文本 |
| 9 | POST | `/updateServer` | 是 | 新增/更新游戏服（upsert） | 文本 |
| 10 | POST | `/removeServer` | 是 | 删除游戏服 | 文本 |
| 11 | POST | `/updateKV` | 是 | 批量写入 KV | 文本 |
| 12 | POST | `/addMergeServer` | 是 | 新增/更新和服映射（带环检测） | 文本 |
| 13 | POST | `/removeMergeServer` | 是 | 删除和服映射（按 from_server_id 主键） | 文本 |

> \* `/export` 推荐 GET（测试脚本用 GET，签名 method 传 `GET`）；服务端不强制方法校验，但**签名中的 method 必须与实际请求方法一致**。`/import` 惯例用 POST。

---

## 五、接口详情

### 1. GET /getAllServer — 全量数据（服务器 + 分区 + KV）

供各微服务定时轮询（`src/common/gameServerData.go` 每 5s 拉取一次，超时 3s）。

- **方法**：`GET`（不校验方法）
- **鉴权**：无
- **入参**：无
- **出参**（`200 OK`，`application/json`）：

```json
{
  "servers": [ { /* Server 对象，见第三节 */ } ],
  "zones":   [ { "zone_id": 100, "zone_name": "一区" } ],
  "kv":      { "someKey": "someValue" }
}
```

- **失败**：`500`（DB/序列化错误）
- **备注**：每个 server 的 `zone_name` 由 `maple_zone` 关联填充；`kv` 为 `maple_kv` 全表。

---

### 2. GET /getAllZoneData — 全部分区

- **方法**：`GET`
- **鉴权**：无
- **入参**：无
- **出参**（`200 OK`）：JSON 对象，**key 为 zone_id 的字符串形式**：

```json
{ "100": "一区", "1001": "一服-天穹" }
```

- **失败**：`500`

---

### 3. GET /getAllMergeServer — 折叠后的和服映射

- **方法**：`GET`
- **鉴权**：无
- **入参**：无
- **出参**（`200 OK`，`Content-Type: application/json`）：

```json
{ "merge_map": { "10002": 10001, "10003": 10001 } }
```

- **折叠语义**：沿链追溯到没有出边的根服。
  - 原始链 `10002→10003→10001` 折叠为 `10002→10001`、`10003→10001`（`foldMergeMap`，`mapleHttpService.go:702`）
- **备注**：未参与合服的服不会出现在 map 中；被 `gameServerData.go` 用于 `GetGameServerMergeRoot`。
- **失败**：`500 internal server error`

---

### 4. GET/POST /export — 导出全量服务器数据

- **方法**：`GET`（签名 method 传 `GET`）
- **鉴权**：**需要**
- **入参**：无
- **出参**（`200 OK`，`Content-Type: application/json`）：

```json
{
  "servers": [
    {
      "id": 1, "server_name": "S1",
      "zone_id": 100, "zone_name": "一区",
      "game_server": "10.0.0.1:7001",
      "queue_server": "10.0.0.2:8001",
      "central_login": "10.0.0.5:9001",
      "server_group": 1, "server_state": 1, "server_flag_state": 0,
      "alias": "s1-a", "start_time": 1700000000
    }
  ]
}
```

> 注意：**只返回 `servers`，不返回 zones 与 kv**（与 `/getAllServer` 不同）。

- **失败**：`401 unauthorized`、`500 internal server error`

---

### 5. POST /import — 全量导入（危险：清空重写）

- **方法**：`POST`
- **鉴权**：**需要**
- **入参**（body，JSON）：

```json
{
  "servers": [
    {
      "id": 1,
      "server_name": "S1",
      "zone_id": 100,
      "zone_name": "一区",
      "game_server": "10.0.0.1:7001",
      "queue_server": "10.0.0.2:8001",
      "central_login": "10.0.0.5:9001",
      "server_group": 1,
      "server_state": 1,
      "server_flag_state": 3,
      "alias": "s1-a",
      "start_time": 1700000000
    }
  ]
}
```

- **处理逻辑**（单事务）：
  1. `DELETE FROM maple`、`DELETE FROM maple_zone`（全量清空）
  2. 逐条 `INSERT ... ON DUPLICATE KEY UPDATE` 写 `maple_zone`
  3. 逐条 `INSERT` 写 `maple`
  4. 任一步失败 → `ROLLBACK`
- **出参**：
  - 成功：`200 OK`，body `success`
  - `401 unauthorized`（鉴权失败）
  - `500` + 文本：`unauthorized` / `internal server error` / `unmarshal body error` / `begin tx error` / `clear maple error` / `clear maple_zone error` / `insert zone error` / `insert server error` / `commit tx error`
- **备注**：**不影响** `maple_kv` 与 `maple_merge_server`。

---

### 6. POST /addZone — 新增分区

- **方法**：`POST`
- **鉴权**：**需要**
- **入参**：

```json
{ "zone_id": 1001, "zone_name": "一服-天穹" }
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `zone_id` | int | 是 | 分区 ID（唯一键） |
| `zone_name` | string | 是 | 分区名 |

- **处理**：`INSERT INTO maple_zone (zone_id, zone_name) VALUES (?, ?)`
- **出参**：`200 OK`，body `success`；`401 unauthorized`
- **备注/已知限制**：
  - **无去重校验**，重复 `zone_id` 会触发 DB 唯一键错误，但错误只打日志，**接口仍返回 200 success**。
  - body 解析失败同样只打日志，仍返回 200。

---

### 7. POST /removeZone — 删除分区

- **方法**：`POST`
- **鉴权**：**需要**
- **入参**：

```json
{ "zone_id": 1001 }
```

- **处理**：`DELETE FROM maple_zone WHERE zone_id = ?`（不校验是否还有游戏服引用该分区）
- **出参**：`200 success`；`401 unauthorized`
- **备注**：SQL 错误仅打日志，仍返回 200。

---

### 8. POST /updateZone — 更新分区名

- **方法**：`POST`
- **鉴权**：**需要**
- **入参**：

```json
{ "zone_id": 1001, "zone_name": "新名字" }
```

- **处理**：`UPDATE maple_zone SET zone_name = ? WHERE zone_id = ?`（zone 不存在时是空更新，仍返回 200）
- **出参**：`200 success`；`401 unauthorized`

---

### 9. POST /updateServer — 新增/更新游戏服（upsert）

- **方法**：`POST`
- **鉴权**：**需要**
- **入参**：完整 Server 对象（字段说明见第三节）

```json
{
  "id": 1,
  "server_name": "S1",
  "zone_id": 100,
  "zone_name": "一区",
  "game_server": "10.0.0.1:7001",
  "queue_server": "10.0.0.2:8001",
  "central_login": "10.0.0.5:9001",
  "server_group": 1,
  "server_state": 1,
  "server_flag_state": 0,
  "alias": "s1-a",
  "start_time": 1700000000
}
```

- **处理逻辑**：
  1. `SELECT COUNT(*) FROM maple WHERE server_id = ?`
  2. **不存在** → `INSERT maple` + `INSERT maple_zone(zone_id, zone_name)`（顺带补分区）
  3. **已存在** → `UPDATE maple SET server_name, zone_id, game_server, queue_server, server_group, server_state, server_flag_state, alias, start_time, central_login WHERE server_id = ?`
- **出参**：`200 success`；`401 unauthorized`
- **备注**：SQL 错误仅打日志，仍返回 200；**非事务**（insert server 与 insert zone 不在同一事务）。

---

### 10. POST /removeServer — 删除游戏服

- **方法**：`POST`
- **鉴权**：**需要**
- **入参**：

```json
{ "id": 1 }
```

> 注意 key 是 **`id`**（不是 `server_id`），对应 `RemoveServerRequest.Id`。

- **处理**：`DELETE FROM maple WHERE server_id = ?`
- **出参**：`200 success`；`401 unauthorized`

---

### 11. POST /updateKV — 批量写入 KV

- **方法**：`POST`
- **鉴权**：**需要**
- **入参**：**任意 `map[string]string` 对象**（非结构体）：

```json
{
  "maintain_notice": "今晚 22:00 维护",
  "activity_open": "1"
}
```

- **处理逻辑**（单事务）：对每个键执行
  `INSERT INTO maple_kv (key, value) VALUES (?, ?) ON DUPLICATE KEY UPDATE value = VALUES(value)`
- **出参**：
  - `200 success`
  - `401 unauthorized`
  - `500` + `internal server error` / `unmarshal body error` / `begin tx error` / `insert kv error` / `commit tx error`
- **备注**：**只增/改，不删除**——请求中未包含的旧 key 会保留。

---

### 12. POST /addMergeServer — 新增/更新和服映射（带环检测）

- **方法**：`POST`
- **鉴权**：**需要**
- **入参**：

```json
{ "from_server_id": 10002, "to_server_id": 10001 }
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `from_server_id` | int | 是 | 被合入的服（源） |
| `to_server_id` | int | 是 | 合入目标服 |

- **处理逻辑**（`mapleHttpService.go:632`）：
  1. body 解析失败 → `400 invalid request`
  2. `from == to` → `400 from and to cannot be the same`（自环拒绝）
  3. 加载全表映射到内存 `loadMergeMap()`
  4. 若已有 `curMap[from] == to` → 直接 `200 success`（**幂等**）
  5. 从图中摘掉 `from` 的旧出边后做 BFS 环检测：若 `to` 能走回 `from` → `400 cycle detected`
  6. 通过则 `INSERT ... ON DUPLICATE KEY UPDATE to_server_id = VALUES(to_server_id)`（**覆盖旧目标**）
- **出参**：
  - `200 success`
  - `401 unauthorized`
  - `400` + `invalid request` / `from and to cannot be the same` / `cycle detected`
  - `500 internal server error`
- **行为示例**（来自 `bin/maple/test_merge_server.py`）：
  - `A→B`、`B→C` 成功；查询折叠结果 `A→C`、`B→C`
  - 再加 `C→A` 被拒（成环）
  - `A→B` 改为 `A→E` 成功（换目标不算环），`B→C` 不受影响

---

### 13. POST /removeMergeServer — 删除和服映射

用于修正 `/addMergeServer` 时填错的映射。按主键 `from_server_id` 精确删除，不影响其他服的链路。

- **方法**：`POST`
- **鉴权**：**需要**
- **入参**：

```json
{ "from_server_id": 10002 }
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `from_server_id` | int | 是 | 被合入服（源）的主键 |

- **处理逻辑**（`mapleHttpService.go:728`）：
  1. body 解析失败 → `400 invalid request`
  2. `DELETE FROM maple_merge_server WHERE from_server_id = ?`（SQL 错误 → `500 internal server error`）
  3. 删完之后该 `from` 服在 `foldMergeMap` 中没有出边，会被视作根服，不再出现在 `/getAllMergeServer` 的折叠结果里
- **出参**：
  - 成功：`200 OK`，body `success`
  - `401 unauthorized`
  - `400 invalid request`
  - `500 internal server error`
- **幂等性**：不存在的 `from_server_id` 也返回 `200 success`（`DELETE` 影响 0 行不报错）。

---

## 六、通用返回约定

| 状态码 | 含义 | Body |
|---|---|---|
| `200` | 成功 | 查询接口为 JSON；写接口为文本 `success` |
| `400` | 参数非法/和服成环 | 文本错误描述（仅 `/addMergeServer`） |
| `401` | 鉴权失败（sign 不符 / ts 超 ±10s） | `unauthorized` |
| `500` | 服务端错误 | 文本错误描述 |

**已知实现特性（调用方需注意）**：
1. `/addZone` `/removeZone` `/updateZone` `/updateServer` `/removeServer` 的数据库错误**只打日志，仍返回 200 success**，不能以 200 判定落库成功；需要强一致请走 `/import`（事务 + 真实 500）。
2. 所有接口**不校验 HTTP 方法**（验签除外——签名里的 method 必须等于实际 method），建议按本文档推荐方法调用。
3. 查询类接口 `/getAllServer` `/getAllZoneData` `/getAllMergeServer` **无鉴权**，任何内网客户端可直接读。
4. 写接口无速率限制、无幂等键（`/addMergeServer` 除外，其天然幂等）。

---

## 七、消费方接入（供参考）

各微服务通过配置 `mapleHttpAddr`（如 `192.168.10.13:9527`）自动接入（`src/base/init.go:80`），后台每 5s 拉取：

- `/getAllServer` → 缓存 `serverId → server_group`
- `/getAllMergeServer` → 缓存 `serverId → 合并组根服`

查询 API（`src/common/gameServerData.go`）：

```go
GetGameServerGroup(serverId)        // 先做和服折叠再查组别
GetGameServerMergeRoot(serverId)    // 查询所属合并组根服
GetAllGameServerGroups()            // 全量快照
GetAllGameServerMergeMap()          // 全量和服映射（仅含参与合服的服）
```

---

## 八、相关测试脚本

| 脚本 | 覆盖接口 |
|---|---|
| `src/maple/py_test/test.py` | `/import` `/export` `/getAllServer` `/getAllZoneData` `/addZone`（xlsx 导入、导出 JSON） |
| `bin/maple/test_merge_server.py` | `/addMergeServer` `/getAllMergeServer` `/removeMergeServer`（环检测、幂等、鉴权失败用例） |
