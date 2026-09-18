# maple 接口文档

maple 是 centralService 的运营配置服务,统一管理服列表、Zone、和服映射、KV 配置。
本文档面向需要"接入 maple 拉取/写入数据"的下游调用方,聚焦**和服映射**相关的接口,顺带列出其余常用 HTTP 接口。

- 服务地址: `http://<maple_host>:<http_addr>`(默认 `0.0.0.0:9527`)
- 鉴权: HMAC-SHA256 头签,窗口 ±10 秒
- 数据格式: JSON,UTF-8

---

## 1. 鉴权说明

写接口(`/import`、`/addZone`、`/addMergeServer` 等)需要在 HTTP 头里带签名,读接口(`/getAllServer`、`/getAllMergeServer`)无需鉴权。

签名算法:

```
plainText = method + ts + nc                     # 直接拼接,无分隔符
sign       = HMAC_SHA256(secret, plainText)      # 十六进制小写
```

必填请求头:

| 头 | 说明 |
|----|------|
| `ts`    | 当前 Unix 秒级时间戳,服务端只接受 `[now-10, now+10]` |
| `nc`    | nonce 字符串,任意可重复,通常用随机串 |
| `sign`  | 按上述算法算出的十六进制串 |
| `Content-Type` | POST 请求固定 `application/json` |

示例 (Python):

```python
import hashlib, hmac, time, json, urllib.request

secret = "hello world"
ts  = str(int(time.time()))
nc  = "abc"
method = "POST"
plain = f"{method}{ts}{nc}".encode("utf-8")
sign  = hmac.new(secret.encode("utf-8"), plain, hashlib.sha256).hexdigest()

req = urllib.request.Request(
    "http://127.0.0.1:9527/addMergeServer",
    data=json.dumps({"from_server_id": 10002, "to_server_id": 10001}).encode("utf-8"),
    headers={"Content-Type": "application/json", "ts": ts, "nc": nc, "sign": sign},
    method="POST",
)
urllib.request.urlopen(req)
```

签名错误或 ts 越界统一返回 `401 Unauthorized`。

---

## 2. 和服映射接口 (核心)

和服过程结束,需要把"哪个服被合入到哪个服"写入 maple,客户端拉到的结果始终是**折叠到根服**的最终映射。

### 2.1 数据模型

```
原始边表 (DB)                 折叠后 (API 返回)
{10002: 10003,                 {10002: 10001,
 10003: 10001}                  10003: 10001}
```

- 每服最多一条出边 (`from_server_id` 主键)。
- 不允许环 (`from -> ... -> from`)。
- 折叠时,沿出边链追溯到没有出边的节点 = 根服。

### 2.2 POST /addMergeServer  ——  新增/替换一条映射

写一条 `from_server_id -> to_server_id` 的和服映射,**每次添加前自动做环形检测**,若成环则该次请求失败,DB 不会被改动。

请求体:

```json
{
  "from_server_id": 10002,
  "to_server_id":   10001
}
```

字段约束:

| 字段 | 类型 | 说明 |
|------|------|------|
| `from_server_id` | int | 被合入的服,**全局唯一出边**,已有 `from` 的旧目标会被新目标覆盖 |
| `to_server_id`   | int | 合入目标 |

响应:

| 状态码 | 含义 |
|--------|------|
| 200    | 写入成功 (新增或覆盖) |
| 400    | `from == to`,或会形成环,响应体是文字描述 (`cycle detected` 等) |
| 401    | 鉴权失败 |
| 500    | 数据库异常 |

环形检测语义: 假设当前 DB 中已经有边集 `E`,加入 `from -> to` 之前:

1. 若 `from -> to` 与某条 `from -> to'` 等价,直接视为成功(幂等);
2. 否则把 `from` 的旧出边 (如果有) 从 `E` 中摘掉 (因为它会被新边替换),得到 `E'`;
3. 在 `E'` 上从 `to` 出发能否走到 `from`:能走通就拒绝,走不通就接受。

也就是说,**允许把一个服的合入目标从 A 改成 B**,只要改动不破坏无环性。

### 2.3 GET /getAllMergeServer  ——  拉取折叠后的全量映射

无需鉴权。

响应:

```json
{
  "merge_map": {
    "10001": 10001,
    "10002": 10001,
    "10003": 10001,
    "20001": 20002
  }
}
```

- `merge_map` 的每个 key 都是**被合入的服**;
- 每个 value 都是该服**沿链追溯到的根服**;
- 没出现在 `merge_map` 中的服 = 它不是任何服的"被合入者" = 它本身就是根服(或独立服);
- 不主动返回 "谁是独立服" 这种列表,如需请额外调用 `/getAllServer`。

客户端拿到的就是**可直接使用的最终映射**,无需再在本地做折叠。

### 2.4 整体调用示例

```python
import hashlib, hmac, time, json, urllib.request

SECRET = "hello world"
BASE   = "http://maple.example.com:9527"

def sign(method, ts, nc):
    return hmac.new(SECRET.encode(), f"{method}{ts}{nc}".encode(), hashlib.sha256).hexdigest()

def add_merge(from_id, to_id):
    ts = str(int(time.time()))
    body = json.dumps({"from_server_id": from_id, "to_server_id": to_id}).encode()
    req = urllib.request.Request(f"{BASE}/addMergeServer", data=body, headers={
        "Content-Type": "application/json",
        "ts": ts, "nc": "x", "sign": sign("POST", ts, "x"),
    }, method="POST")
    with urllib.request.urlopen(req) as r:
        return r.status, r.read().decode()

def get_merge_map():
    with urllib.request.urlopen(f"{BASE}/getAllMergeServer") as r:
        return json.loads(r.read())["merge_map"]

# 把 10002 合入 10003, 再把 10003 合入 10001
print(add_merge(10002, 10001))
print(get_merge_map())
# 期望: {10002: 10001, 10003: 10001}
```

---

## 3. 其他常用接口(简表)

所有写接口都需要 §1 的鉴权,读接口免鉴权。

| Method | Path | 用途 |
|--------|------|------|
| GET    | `/getAllServer`     | 拉取全量服 + 全部 zone + 全量 KV |
| GET    | `/getAllZoneData`   | 仅拉取 zone 列表 |
| GET    | `/export`           | 导出服列表 JSON (需要鉴权) |
| POST   | `/import`           | 全量导入服和 zone (会先清空原数据) |
| POST   | `/addZone`          | 新增一个 zone |
| POST   | `/removeZone`       | 删除一个 zone |
| POST   | `/updateZone`       | 更新 zone 名称 |
| POST   | `/updateServer`     | 新增或更新一个服 |
| POST   | `/removeServer`     | 删除一个服 |
| POST   | `/updateKV`         | 批量写入 KV (整段 map,按 key 覆盖) |

`/getAllServer` 响应体结构 (供下游解包参考):

```json
{
  "servers": [
    {
      "id": 10001,
      "server_name": "...",
      "zone_id": 1,
      "zone_name": "...",
      "game_server":   "...",
      "queue_server":  "...",
      "central_login": "...",
      "server_group": 0,
      "server_state": 0,
      "server_flag_state": 0,
      "alias": "",
      "start_time": 1700000000
    }
  ],
  "zones": [{"zone_id": 1, "zone_name": "..."}],
  "kv":   {"someKey": "someValue"}
}
```

---

## 4. 错误码与排查

| 现象 | 原因 | 处理 |
|------|------|------|
| 401 `unauthorized` | 签名错,或 `secret` 不一致,或 ts 越界 | 比对服务端 `secret`,确认 ts 在 ±10s 内 |
| 400 `cycle detected` | 加边会形成环 | 检查 `from`、`to`,确认调用方上游逻辑无误 |
| 400 `from and to cannot be the same` | `from == to` | 修正参数 |
| 400 `invalid request` | body 不是合法 JSON | 检查 body |
| 500 `internal server error` | DB 异常 | 查 maple 日志 (`maple.log`) |

---

## 5. 部署与依赖

- 服务端需提前建表 (`bin/maple/up.sql`):

  ```sql
  CREATE TABLE IF NOT EXISTS `maple_merge_server` (
      `from_server_id` INT NOT NULL,
      `to_server_id`   INT NOT NULL,
      PRIMARY KEY (`from_server_id`),
      INDEX `idx_to` (`to_server_id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
  ```

- 端口与 `secret` 在 `bin/maple/mapleConf.json` 中配置:

  ```json
  {
      "httpAddr": "0.0.0.0:9527",
      "secret":   "hello world",
      "mysql":    { "addr":"...", "user":"...", "passwd":"...", "db":"maple" }
  }
  ```

- 仅和服映射相关变更:不破坏已有 `maple` / `maple_zone` / `maple_kv` 表的 schema,老调用方升级 maple 服务即可,不需要改动自己侧逻辑。
