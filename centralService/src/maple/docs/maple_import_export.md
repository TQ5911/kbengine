# Maple 服务 Import / Export API（简版）

本文件面向客户端开发，涵盖 `/import` 与 `/export` 两个接口的最小必需信息：鉴权、请求格式、示例与返回值。

## 鉴权（所有接口必需）
- 头部参数：
  - `ts`: 秒级 Unix 时间戳（与服务端时间允许 ±10 秒）
  - `nc`: 随机字符串（nonce）
  - `sign`: HMAC-SHA256 签名的十六进制小写字符串
- 签名算法：`sign = hex( HMAC_SHA256(secret, method + ts + nc) )`
  - `method` 使用大写 HTTP 方法，如 `POST` / `GET`
  - `secret` 为双方约定的密钥
- 失败时返回 `401 Unauthorized`

---

## Import 全量导入
- 方法：`POST`
- 路径：`/import`
- 头部：`Content-Type: application/json`，以及鉴权头 `ts` `nc` `sign`
- 语义：全量替换。服务端会清空 `maple` 与 `maple_zone` 后，按请求体插入全部数据。
- 请求体示例：
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
      "server_group": 1,
      "server_state": 1,
      "server_flag_state": 0,
      "alias": "s1-a"
    },
    {
      "id": 2,
      "server_name": "S2",
      "zone_id": 100,
      "zone_name": "一区",
      "game_server": "10.0.0.3:7001",
      "queue_server": "10.0.0.4:8001",
      "server_group": 1,
      "server_state": 1,
      "server_flag_state": 0,
      "alias": "s2-a"
    }
  ]
}
```
- 成功返回：`200 OK`，文本：`success`
- 失败返回：
  - `401 Unauthorized`（鉴权失败）
  - `500 Internal Server Error`（解析或数据库错误）

---

## Export 导出（全量）
- 方法：`GET`
- 路径：`/export`
- 头部：鉴权头 `ts` `nc` `sign`
- 响应：`application/json`，结构如下：
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
      "server_group": 1,
      "server_state": 1,
      "server_flag_state": 0,
      "alias": "s1-a"
    }
  ]
}
```
- 失败返回：
  - `401 Unauthorized`（鉴权失败）
  - `500 Internal Server Error`

---

## 字段说明（Server）
- `id`：服务器唯一 ID（int）
- `server_name`：服务器名（string）
- `zone_id`：区 ID（int）
- `zone_name`：区名（string）
- `game_server`：游戏服地址（string）
- `queue_server`：排队服地址（string）
- `server_group`：分组（int）
- `server_state`：状态（int）
- `server_flag_state`：标志位状态（int）
- `alias`：别名（string）

---

## 签名示例（伪代码）
```text
method = "POST"           // 调用 /import 用 POST，/export 用 GET
ts = now_unix_seconds()
nc = random_string()
plain = method + ts + nc
sign = hex( HMAC_SHA256(secret, plain) )
```

将 `ts`、`nc`、`sign` 作为请求头发送。注意 `ts` 与服务端时间相差不可超过 ±10 秒。
