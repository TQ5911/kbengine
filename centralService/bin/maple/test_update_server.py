#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maple /updateServer 增量更新功能测试

被测接口:
  POST /updateServer     (要鉴权: HMAC-SHA256(secret, method+ts+nc))
  POST /removeServer     (清理用)
  POST /removeZone       (清理用)
  GET  /getAllServer     (读回校验, 不需要鉴权)

覆盖点:
  1. 只传部分字段也能建服 (未传字段按零值, server_sub_group 取 DDL 默认 1)
  2. 全量字段更新
  3. 增量更新只改传了的字段, 其余列保持原值            <-- 本功能核心
  4. 显式传零值 ("", 0) 能覆盖成零值, 与"没传"区分
  5. 只传 zone_name 时能用库里现有 zone_id 定位 maple_zone
  6. 不传 zone_name 时不会把 maple_zone 里的名字清空
  7. zone_id + zone_name 一起改, 分区跟着换
  8. 只传主键 = 空更新, 返回 200 且不改任何数据
  9. 主键缺失 / id<=0 -> 400
 10. 非法 JSON -> 400
 11. 主键兼容 server_id 写法
 12. id 与 server_id 同时给且不一致时以 id 为准
 13. 签名错误 -> 401

用法:
  python test_update_server.py --url http://127.0.0.1:9527 --secret "hello world"
  或
  MAPLE_URL=http://127.0.0.1:9527 MAPLE_SECRET="hello world" python test_update_server.py

测试数据用时间派生的 id (880000 起), 不跟历史数据冲突;
跑完默认通过 /removeServer /removeZone 自动清理, 加 --keep 保留现场并打印清理 SQL。

注意: 这个脚本会真的往 maple / maple_zone 写数据, 只在测试库或低峰期跑。
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Optional, Tuple


def sign(method: str, ts: str, nc: str, secret: str) -> str:
    """对齐 maple handleAuth: HMAC-SHA256(secret, method+ts+nc)."""
    msg = f"{method}{ts}{nc}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()


# maple 表里由 updateServer 负责的列, 断言"没变"时逐列比对
SERVER_FIELDS = (
    "server_name", "zone_id", "zone_name", "game_server", "queue_server",
    "central_login", "server_group", "server_sub_group", "server_state",
    "server_flag_state", "alias", "start_time",
)


class MapleClient:
    def __init__(self, base_url: str, secret: str):
        self.base_url = base_url.rstrip("/")
        self.secret = secret

    def _request(self, method: str, path: str,
                 body: Optional[dict] = None,
                 raw: Optional[str] = None,
                 bad_sign: bool = False) -> Tuple[int, str]:
        url = self.base_url + path
        if raw is not None:
            data = raw.encode("utf-8")
        elif body is not None:
            data = json.dumps(body).encode("utf-8")
        else:
            data = None

        headers = {}
        if method != "GET":
            ts = str(int(time.time()))
            nc = "test-nonce"
            headers["ts"] = ts
            headers["nc"] = nc
            headers["sign"] = "deadbeef" * 8 if bad_sign else sign(method, ts, nc, self.secret)
        if data is not None:
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status, resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8")

    # ---- 被测接口 ----

    def update_server(self, payload: dict) -> Tuple[int, str]:
        return self._request("POST", "/updateServer", body=payload)

    def update_server_raw(self, raw: str) -> Tuple[int, str]:
        return self._request("POST", "/updateServer", raw=raw)

    def update_server_bad_sign(self, payload: dict) -> Tuple[int, str]:
        return self._request("POST", "/updateServer", body=payload, bad_sign=True)

    def remove_server(self, server_id: int) -> Tuple[int, str]:
        return self._request("POST", "/removeServer", body={"id": server_id})

    def remove_zone(self, zone_id: int) -> Tuple[int, str]:
        return self._request("POST", "/removeZone", body={"zone_id": zone_id})

    # ---- 读回 ----

    def get_all_server(self) -> dict:
        status, body = self._request("GET", "/getAllServer")
        if status != 200:
            raise RuntimeError(f"getAllServer status={status} body={body}")
        return json.loads(body)

    def get_server(self, server_id: int) -> Optional[dict]:
        for s in self.get_all_server().get("servers") or []:
            if s.get("id") == server_id:
                return s
        return None

    def get_zone(self, zone_id: int) -> Optional[dict]:
        for z in self.get_all_server().get("zones") or []:
            if z.get("zone_id") == zone_id:
                return z
        return None


class TestRunner:
    def __init__(self, client: MapleClient):
        self.client = client
        self.passed = 0
        self.failed = 0

        # 时间派生一组 id, 避免和历史脏数据/其他测试撞车;
        # 撞到上一轮残留 (--keep) 就整体往后挪, 防止互相干扰。
        data = client.get_all_server()
        used_ids = {s.get("id") for s in (data.get("servers") or [])}
        used_zids = {z.get("zone_id") for z in (data.get("zones") or [])}

        base = 880000 + int(time.time()) % 1000
        for _ in range(20):
            if not ({base, base + 1} & used_ids) and not ({base + 500, base + 501} & used_zids):
                break
            base += 7

        self.S1 = base
        self.S2 = base + 1
        self.Z1 = base + 500
        self.Z2 = base + 501

    # ---- 断言 ----

    def _ok(self, name: str, msg: str = ""):
        self.passed += 1
        print(f"  PASS  {name}" + (f" — {msg}" if msg else ""))

    def _fail(self, name: str, msg: str = ""):
        self.failed += 1
        print(f"  FAIL  {name}" + (f" — {msg}" if msg else ""))

    def _expect(self, name: str, cond: bool, detail: str = ""):
        if cond:
            self._ok(name, detail)
        else:
            self._fail(name, detail)
        return cond

    def _expect_eq(self, name: str, got, want):
        return self._expect(name, got == want, f"got={got!r} want={want!r}")

    def _expect_200(self, name: str, status: int, body: str) -> bool:
        return self._expect(name, status == 200, f"status={status} body={body}")

    def _expect_400(self, name: str, status: int, body: str) -> bool:
        return self._expect(name, status == 400, f"status={status} body={body}")

    def _diff(self, before: dict, after: dict, exclude=()) -> dict:
        """返回两快照之间有差异的字段: {字段: (旧, 新)}"""
        keys = set(before) | set(after) | set(SERVER_FIELDS)
        return {k: (before.get(k), after.get(k))
                for k in keys
                if k not in exclude and before.get(k) != after.get(k)}

    def _set(self, name: str, payload: dict, check: str = "") -> Optional[dict]:
        """发一次 updateServer 并读回, 返回读回的 server 快照"""
        status, body = self.client.update_server(payload)
        self._expect_200(name, status, body)
        if status != 200:
            return None
        return self.client.get_server(payload.get("id") or payload.get("server_id") or 0)

    # ---- 用例 ----

    def test_create_partial(self):
        """部分字段建服: 没传的列为零值, server_sub_group 走 DDL 默认 1"""
        print(f"\n[Test 1] 部分字段建服 id={self.S1} zone={self.Z1}")
        payload = {
            "id": self.S1,
            "server_name": "incr-test",
            "zone_id": self.Z1,
            "zone_name": "incr-zone-1",
            "server_state": 1,
        }
        s = self._set("create partial -> 200", payload)
        if not s:
            self._fail("create partial 后能读回", "server 不存在")
            return
        self._expect_eq("server_name", s.get("server_name"), "incr-test")
        self._expect_eq("zone_id", s.get("zone_id"), self.Z1)
        self._expect_eq("zone_name", s.get("zone_name"), "incr-zone-1")
        self._expect_eq("server_state", s.get("server_state"), 1)
        # 没传的字段
        self._expect_eq("server_group 未传=0", s.get("server_group"), 0)
        self._expect_eq("alias 未传=''", s.get("alias"), "")
        self._expect_eq("start_time 未传=0", s.get("start_time"), 0)
        self._expect_eq("game_server 未传=''", s.get("game_server"), "")
        self._expect_eq("server_sub_group 未传=DDL 默认 1", s.get("server_sub_group"), 1)

    def test_full_update(self):
        """全量字段更新: 每个字段都按传入值落库"""
        print(f"\n[Test 2] 全量更新 id={self.S1}")
        payload = {
            "id": self.S1,
            "server_name": "incr-full",
            "zone_id": self.Z1,
            "zone_name": "incr-zone-1",
            "game_server": "gs-1:9001",
            "queue_server": "qs-1:9002",
            "central_login": "cl-1:9003",
            "server_group": 3,
            "server_sub_group": 2,
            "server_state": 5,
            "server_flag_state": 1,
            "alias": "al-1",
            "start_time": 1700000000,
        }
        s = self._set("full update -> 200", payload)
        if not s:
            return
        for k, v in payload.items():
            if k == "id":
                continue
            self._expect_eq(f"全量 {k}", s.get(k), v)

    def test_incremental_keeps_others(self):
        """核心: 只传 server_state, 其他 11 列必须原封不动"""
        print(f"\n[Test 3] 增量更新只改 server_state (核心用例)")
        before = self.client.get_server(self.S1)
        if not before:
            self._fail("增量更新前置数据", "server 不存在")
            return

        s = self._set("只传 server_state -> 200", {"id": self.S1, "server_state": 9})
        if not s:
            return
        self._expect_eq("server_state 变成 9", s.get("server_state"), 9)

        d = self._diff(before, s, exclude={"server_state"})
        self._expect("其他字段全部保持原值", not d, f"被误改的字段: {d}" if d else "")

    def test_explicit_zero_values(self):
        """显式传空串/0 要真的写进去, 不能被当成缺字段"""
        print(f"\n[Test 4] 显式零值: alias='' start_time=0 server_group=0")
        before = self.client.get_server(self.S1)
        if not before:
            self._fail("零值前置数据", "server 不存在")
            return

        s = self._set("显式零值 -> 200",
                      {"id": self.S1, "alias": "", "start_time": 0, "server_group": 0})
        if not s:
            return
        self._expect_eq("alias 被清空", s.get("alias"), "")
        self._expect_eq("start_time 归零", s.get("start_time"), 0)
        self._expect_eq("server_group 归零", s.get("server_group"), 0)
        # 这三个字段本来有值, 说明确实写进去了; 其它字段不变
        self._expect("alias 之前非空(证明是写入而非未传)",
                     before.get("alias") == "al-1", f"before={before.get('alias')!r}")
        d = self._diff(before, s, exclude={"alias", "start_time", "server_group"})
        self._expect("其余字段保持原值", not d, f"被误改的字段: {d}" if d else "")

    def test_zone_name_only(self):
        """只传 zone_name, 用库里现有 zone_id 定位 maple_zone"""
        print(f"\n[Test 5] 只传 zone_name, 不传 zone_id")
        before = self.client.get_server(self.S1)
        if not before:
            self._fail("zone_name 前置数据", "server 不存在")
            return

        s = self._set("只传 zone_name -> 200", {"id": self.S1, "zone_name": "incr-zone-1b"})
        if not s:
            return
        self._expect_eq("zone_name 已更新", s.get("zone_name"), "incr-zone-1b")
        self._expect_eq("zone_id 没被改动", s.get("zone_id"), before.get("zone_id"))
        d = self._diff(before, s, exclude={"zone_name"})
        self._expect("其余字段保持原值", not d, f"被误改的字段: {d}" if d else "")

    def test_no_zone_name_keeps_zone(self):
        """不传 zone_name 时, 不能把 maple_zone 里的名字清空"""
        print(f"\n[Test 6] 不传 zone_name 时分区名不受影响")
        before = self.client.get_server(self.S1)
        if not before:
            self._fail("分区保护前置数据", "server 不存在")
            return

        s = self._set("只传 server_flag_state -> 200",
                      {"id": self.S1, "server_flag_state": 2})
        if not s:
            return
        self._expect_eq("zone_name 仍是 incr-zone-1b", s.get("zone_name"), "incr-zone-1b")
        z = self.client.get_zone(self.Z1)
        self._expect_eq("maple_zone 里分区名未变",
                        (z or {}).get("zone_name"), "incr-zone-1b")

    def test_zone_id_and_name_together(self):
        """zone_id + zone_name 一起改: 分区跟着换, 新分区要落 maple_zone"""
        print(f"\n[Test 7] zone_id+zone_name 一起改到 {self.Z2}")
        s = self._set("同时改 zone_id/zone_name -> 200",
                      {"id": self.S1, "zone_id": self.Z2, "zone_name": "incr-zone-2"})
        if not s:
            return
        self._expect_eq("server.zone_id", s.get("zone_id"), self.Z2)
        self._expect_eq("server.zone_name", s.get("zone_name"), "incr-zone-2")
        z = self.client.get_zone(self.Z2)
        self._expect("新分区已写入 maple_zone", z is not None, f"zone={z}")
        self._expect_eq("新分区名", (z or {}).get("zone_name"), "incr-zone-2")
        old = self.client.get_zone(self.Z1)
        self._expect_eq("旧分区名没被改", (old or {}).get("zone_name"), "incr-zone-1b")

    def test_empty_patch(self):
        """只传主键: 200 但一条数据都不改"""
        print(f"\n[Test 8] 只传主键 = 空更新")
        before = self.client.get_server(self.S1)
        if not before:
            self._fail("空更新前置数据", "server 不存在")
            return

        status, body = self.client.update_server({"id": self.S1})
        self._expect_200("空更新 -> 200", status, body)
        after = self.client.get_server(self.S1)
        d = self._diff(before or {}, after or {})
        self._expect("空更新不改任何字段", not d, f"被改的字段: {d}" if d else "")

    def test_bad_requests(self):
        """主键问题 / 非法 JSON 都应该是 400"""
        print(f"\n[Test 9] 非法请求 -> 400")
        status, body = self.client.update_server({"server_name": "no-id"})
        self._expect_400("缺主键 -> 400", status, body)

        status, body = self.client.update_server({"id": 0, "alias": "x"})
        self._expect_400("id=0 -> 400", status, body)

        status, body = self.client.update_server({"id": -1, "alias": "x"})
        self._expect_400("id=-1 -> 400", status, body)

        status, body = self.client.update_server_raw('{"id": ')
        self._expect_400("非法 JSON -> 400", status, body)

    def test_server_id_alias(self):
        """主键兼容 server_id 写法 (等同 id)"""
        print(f"\n[Test 10] 用 server_id 当主键建服 {self.S2}")
        status, body = self.client.update_server({
            "server_id": self.S2,
            "server_name": "alias-test",
            "zone_id": self.Z2,
        })
        self._expect_200("server_id 建服 -> 200", status, body)
        s = self.client.get_server(self.S2)
        self._expect("能按 id 读回", s is not None, f"server={s}")
        if s:
            self._expect_eq("server_name", s.get("server_name"), "alias-test")
            self._expect_eq("server_sub_group 默认 1", s.get("server_sub_group"), 1)

    def test_id_precedence(self):
        """id 与 server_id 同时给且不一致时, 以 id 为准, 不能误改另一条"""
        print(f"\n[Test 11] id 与 server_id 冲突时以 id 为准")
        s2_before = self.client.get_server(self.S2)
        status, body = self.client.update_server({
            "id": self.S1, "server_id": self.S2, "alias": "precedence",
        })
        self._expect_200("id+server_id 同时给 -> 200", status, body)

        s1 = self.client.get_server(self.S1)
        self._expect_eq("S1 被改", (s1 or {}).get("alias"), "precedence")
        s2 = self.client.get_server(self.S2)
        self._expect_eq("S2 没被动", (s2 or {}).get("alias"), (s2_before or {}).get("alias"))

    def test_bad_auth(self):
        """签名错 -> 401"""
        print(f"\n[Test 12] 签名错误 -> 401")
        status, body = self.client.update_server_bad_sign({"id": self.S1, "alias": "hack"})
        self._expect("bad sign -> 401", status == 401, f"status={status} body={body}")

    # ---- driver ----

    def cleanup(self):
        print("\n[清理]")
        for sid in (self.S1, self.S2):
            status, body = self.client.remove_server(sid)
            print(f"  removeServer {sid}: {status} {body}")
        for zid in (self.Z1, self.Z2):
            status, body = self.client.remove_zone(zid)
            print(f"  removeZone {zid}: {status} {body}")

    def run(self, keep: bool = False) -> bool:
        print(f"本次使用 id: S1={self.S1} S2={self.S2} Z1={self.Z1} Z2={self.Z2}")
        try:
            self.test_create_partial()
            self.test_full_update()
            self.test_incremental_keeps_others()
            self.test_explicit_zero_values()
            self.test_zone_name_only()
            self.test_no_zone_name_keeps_zone()
            self.test_zone_id_and_name_together()
            self.test_empty_patch()
            self.test_bad_requests()
            self.test_server_id_alias()
            self.test_id_precedence()
            self.test_bad_auth()
        finally:
            if keep:
                print("\n[保留现场] 手动清理:")
                print(f"  DELETE FROM `maple` WHERE `server_id` IN ({self.S1}, {self.S2});")
                print(f"  DELETE FROM `maple_zone` WHERE `zone_id` IN ({self.Z1}, {self.Z2});")
            else:
                self.cleanup()

        total = self.passed + self.failed
        print(f"\n{'-' * 40}\n{self.passed}/{total} passed, {self.failed} failed")
        if self.failed == 0:
            print("All green.")
        return self.failed == 0


def main():
    parser = argparse.ArgumentParser(description="Maple updateServer 增量更新测试")
    parser.add_argument("--url", default=os.environ.get("MAPLE_URL", "http://127.0.0.1:9527"))
    parser.add_argument("--secret", default=os.environ.get("MAPLE_SECRET", ""))
    parser.add_argument("--keep", action="store_true", help="跑完不自动清理, 打印清理 SQL")
    args = parser.parse_args()

    if not args.secret:
        print("ERROR: --secret 或环境变量 MAPLE_SECRET 必须设置", file=sys.stderr)
        sys.exit(2)

    client = MapleClient(args.url, args.secret)

    # 探活
    try:
        n = len(client.get_all_server().get("servers") or [])
        print(f"Connected to {args.url} (现有服务器 {n} 条)")
    except Exception as e:
        print(f"ERROR: 连不上 {args.url}: {e}", file=sys.stderr)
        sys.exit(3)

    runner = TestRunner(client)
    sys.exit(0 if runner.run(keep=args.keep) else 1)


if __name__ == "__main__":
    main()
