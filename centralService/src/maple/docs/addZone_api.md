# addZone API

简洁规范，供客户端接入使用。仅包含此一个接口。

## 概览

- 方法: `POST`
- 路径: `/addZone`
- 鉴权: 自定义 HMAC（见“鉴权”）
- 编码: `application/json; charset=utf-8`

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
  "zone_id":   number,  // 分区 ID（整数）
  "zone_name": string   // 分区名称
}
```

示例：

```
{
  "zone_id": 1001,
  "zone_name": "一服-天穹"
}
```

## 响应

- 成功：`200 OK`，Body: `"success"`
- 鉴权失败：`401 Unauthorized`，Body: `"unauthorized"`
- 解析/服务异常：`500 Internal Server Error`

## cURL 示例

以下示例演示如何在本地计算签名并发起请求（以 bash 为例）：

```bash
SECRET="hello world"                     # 与服务端保持一致
METHOD="POST"
TS=$(date +%s)
NC=$RANDOM
PLAIN="${METHOD}${TS}${NC}"
SIGN=$(printf "%s" "$PLAIN" | openssl dgst -sha256 -hmac "$SECRET" -binary | xxd -p -c 256)

curl -X POST "http://<host>:<port>/addZone" \
  -H "Content-Type: application/json" \
  -H "ts: ${TS}" \
  -H "nc: ${NC}" \
  -H "sign: ${SIGN}" \
  -d '{"zone_id":1001,"zone_name":"一服-天穹"}'
```

## 备注

- `ts` 时间戳与服务端相差超过 ±10 秒会被拒绝。
- 重复的 `zone_id` 将直接插入（当前无去重校验）；若需要“幂等化/覆盖”请与后端约定具体策略。
