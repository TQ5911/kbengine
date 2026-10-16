# removeMergeServer API

简洁规范，供客户端接入使用。仅包含此一个接口。

## 概览

- 方法: `POST`
- 路径: `/removeMergeServer`
- 鉴权: 自定义 HMAC（见"鉴权"）
- 编码: `application/json; charset=utf-8`
- 用途: 按主键 `from_server_id` 删除一条和服映射，用于修正 `/addMergeServer` 时填错的目标服

## 鉴权

请求需在 Header 中携带以下字段：

- `ts`: 当前 UNIX 秒时间戳（与服务端相差不超过 ±10 秒）
- `nc`: 随机数（任意字符串/数字，建议 6 位随机数）
- `sign`: 计算方法如下

签名计算：

```
plain = method + ts + nc            // method 为 HTTP 方法名，如 "POST"
sign  = hex(lowercase(HMAC_SHA256(secret, plain)))
```

其中 `secret` 为服务端配置的密钥（需与客户端保持一致）。

跨域支持：服务端返回以下 CORS 头，便于浏览器使用：

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT, DELETE`
- `Access-Control-Allow-Headers: Authorization, ts, nc, sign, Content-Type`

## 请求体

JSON 对象：

```
{
  "from_server_id": number  // 被合入的服 ID（和服映射主键）
}
```

示例：删除 `10002 → 10001` 的映射

```
{
  "from_server_id": 10002
}
```

## 响应

- 成功：`200 OK`，Body: `"success"`
- 鉴权失败：`401 Unauthorized`，Body: `"unauthorized"`
- 请求体非法：`400 Bad Request`，Body: `"invalid request"`
- 解析/服务异常：`500 Internal Server Error`

## 幂等性

不存在的 `from_server_id` 也返回 `200 success`（`DELETE` 影响 0 行不报错），可放心重试。

删除后该 `from` 服将不再出现在 `/getAllMergeServer` 的折叠结果中（被视作根服，不参与和服）。

## cURL 示例

以下示例演示如何在本地计算签名并发起请求（以 bash 为例）：

```bash
SECRET="hello world"                     # 与服务端保持一致
METHOD="POST"
TS=$(date +%s)
NC=$RANDOM
PLAIN="${METHOD}${TS}${NC}"
SIGN=$(printf "%s" "$PLAIN" | openssl dgst -sha256 -hmac "$SECRET" -binary | xxd -p -c 256)

curl -X POST "http://<host>:<port>/removeMergeServer" \
  -H "Content-Type: application/json" \
  -H "ts: ${TS}" \
  -H "nc: ${NC}" \
  -H "sign: ${SIGN}" \
  -d '{"from_server_id":10002}'
```

## 备注

- `ts` 时间戳与服务端相差超过 ±10 秒会被拒绝。
- 该接口只删除 `maple_merge_server` 表中 `from_server_id` 等于入参的记录，不会影响 `maple` / `maple_zone` / `maple_kv` 等其他表。
- 典型用法：先用 `/getAllMergeServer` 查出现有映射，定位到填错的 `from_server_id`，再用本接口删掉，最后用 `/addMergeServer` 重新添加正确的映射。
