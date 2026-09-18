#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""admin /getAvatarServerId 接口测试脚本"""
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request

# === 配置项 (按需修改) ===
BASE_URL    = "http://127.0.0.1:8080"
SIGN_KEY    = "3Pi0ZsIoRha8h0MG6jfHdxG1WLcE7XplB0kzhFitVIZzUNIbKc871DMEZnHGygno"
KNOWN_GBID  = "2815091073934967903"   # 测试环境的玩家 gbId
KNOWN_SID   = 20223                   # 上述 gbId 对应的 serverId

# admin 错误码 (与 HttpApiService.go 一致)
RESULT_OK                  = 0
RESULT_SIGN_ERR            = -213
RESULT_ARGS_ERR            = -218
RESULT_PARTITION_NOT_FOUND = -206


def sign(body: bytes, key: str) -> str:
    h = hashlib.md5()
    h.update(body)
    h.update(key.encode())
    return h.hexdigest()


def post(args_value: str, sign_value: str = None) -> tuple:
    """POST /getAvatarServerId?sign=<md5>. admin 端读的是 req.URL.Query()[\"sign\"],
    不是 header,sign 必须放在 URL 上。"""
    body_bytes = json.dumps({"args": args_value}).encode()
    url = BASE_URL + "/getAvatarServerId"
    if sign_value is not None:
        # sign 是 hex 串, 不会有特殊字符, 不做 url-encoding 也安全
        url += "?sign=" + sign_value
    req = urllib.request.Request(url, data=body_bytes,
                                  headers={"Content-Type": "application/json"},
                                  method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def get(url: str) -> tuple:
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


passed = failed = 0


def check(name: str, ok: bool, detail: str = ""):
    global passed, failed
    if ok:
        passed += 1
        print(f"  PASS  {name}" + (f" — {detail}" if detail else ""))
    else:
        failed += 1
        print(f"  FAIL  {name}" + (f" — {detail}" if detail else ""))


def call(gbId: str, *, no_sign=False, bad_sign=False) -> tuple:
    args_hex = gbId.encode().hex()
    body_bytes = json.dumps({"args": args_hex}).encode()
    sign_value = None if no_sign else ("deadbeef" * 8 if bad_sign else sign(body_bytes, SIGN_KEY))
    return post(args_hex, sign_value)


# 1) 已知玩家
print(f"\n[1] 已知玩家 gbId={KNOWN_GBID} 期望 serverId={KNOWN_SID}")
status, body = call(KNOWN_GBID)
data = json.loads(body) if body else {}
ok = status == 200 and data.get("result") == RESULT_OK \
     and (data.get("body") or {}).get("serverId") == KNOWN_SID
check("status=200 result=0 serverId 匹配", ok,
      f"status={status} body={body[:200] if body else ''}")

# 2) 不存在的玩家
fake_gb = f"9999{int(time.time()) % 1000000}"
print(f"\n[2] 不存在 gbId={fake_gb}")
status, body = call(fake_gb)
data = json.loads(body) if body else {}
check("result == -206",
      status == 200 and data.get("result") == RESULT_PARTITION_NOT_FOUND,
      f"body={body[:200] if body else ''}")

# 3) 缺 sign
print(f"\n[3] 缺 sign header")
status, body = call(KNOWN_GBID, no_sign=True)
data = json.loads(body) if body else {}
check("result == -213",
      status == 200 and data.get("result") == RESULT_SIGN_ERR,
      f"body={body[:200] if body else ''}")

# 4) sign 错
print(f"\n[4] sign 错")
status, body = call(KNOWN_GBID, bad_sign=True)
data = json.loads(body) if body else {}
check("result == -213",
      status == 200 and data.get("result") == RESULT_SIGN_ERR,
      f"body={body[:200] if body else ''}")

# 5) args 非 hex
print(f"\n[5] args 非 hex")
status, body = post("not-hex-zzz")
data = json.loads(body) if body else {}
check("result == -218",
      status == 200 and data.get("result") == RESULT_ARGS_ERR,
      f"body={body[:200] if body else ''}")

# 6) args 空
print(f"\n[6] args 空字符串")
status, body = post("")
data = json.loads(body) if body else {}
check("result == -218",
      status == 200 and data.get("result") == RESULT_ARGS_ERR,
      f"body={body[:200] if body else ''}")

# 7) GET
print(f"\n[7] 用 GET 打 POST 接口")
status, _ = get(BASE_URL + "/getAvatarServerId")
check("status == 405", status == 405, f"status={status}")

print(f"\n{'-' * 40}\n{passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
