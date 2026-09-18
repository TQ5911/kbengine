#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maple 和服映射接口测试脚本

覆盖的接口:
  POST /addMergeServer       (要鉴权, HMAC-SHA256, 环形检测)
  GET  /getAllMergeServer    (折叠链, 直接指向根服)

用法:
  python test_merge_server.py --url http://127.0.0.1:9527 --secret "hello world"
  或
  MAPLE_URL=http://127.0.0.1:9527 MAPLE_SECRET="hello world" python test_merge_server.py

注意: 测试会基于 time() 派生一组 server id (99001..99005 范围),每次跑会换一组,
保证不跟历史脏数据冲突。测试运行后会在 maple_merge_server 留下本次的 5 行数据,
需要清理请连 MySQL:  DELETE FROM maple_merge_server WHERE from_server_id >= 99000;
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


class MapleClient:
    def __init__(self, base_url: str, secret: str):
        self.base_url = base_url.rstrip("/")
        self.secret = secret

    def _request(self, method: str, path: str,
                 body: Optional[dict] = None) -> Tuple[int, str]:
        url = self.base_url + path
        data = json.dumps(body).encode("utf-8") if body is not None else None

        headers = {}
        if method != "GET":
            ts = str(int(time.time()))
            nc = "test-nonce"
            headers["ts"] = ts
            headers["nc"] = nc
            headers["sign"] = sign(method, ts, nc, self.secret)
        if data is not None:
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status, resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8")

    def add_merge(self, from_id: int, to_id: int) -> Tuple[int, str]:
        return self._request("POST", "/addMergeServer", {
            "from_server_id": from_id,
            "to_server_id": to_id,
        })

    def get_all_merge(self) -> Tuple[int, dict]:
        status, body = self._request("GET", "/getAllMergeServer")
        if status == 200 and body:
            try:
                return status, json.loads(body)
            except json.JSONDecodeError:
                return status, {"raw": body}
        return status, {"raw": body}

    def get_merge_map(self) -> dict:
        _, payload = self.get_all_merge()
        return payload.get("merge_map", {}) if isinstance(payload, dict) else {}


class TestRunner:
    def __init__(self, client: MapleClient):
        self.client = client
        self.passed = 0
        self.failed = 0

        # 用时间戳 + 固定偏移派生一组 id, 不跟历史冲突
        base = 99000 + (int(time.time()) % 1000)
        self.A = base
        self.B = base + 1
        self.C = base + 2
        self.D = base + 3
        self.E = base + 4
        self.F = base + 5

    def _ok(self, name: str, msg: str = ""):
        self.passed += 1
        suffix = f" — {msg}" if msg else ""
        print(f"  PASS  {name}{suffix}")

    def _fail(self, name: str, msg: str = ""):
        self.failed += 1
        suffix = f" — {msg}" if msg else ""
        print(f"  FAIL  {name}{suffix}")

    def _add_expect_ok(self, from_id: int, to_id: int):
        status, body = self.client.add_merge(from_id, to_id)
        if status == 200:
            self._ok(f"add {from_id}->{to_id}", f"body={body}")
            return True
        self._fail(f"add {from_id}->{to_id}", f"expected 200, got {status} body={body}")
        return False

    def _add_expect_reject(self, from_id: int, to_id: int, hint: str = ""):
        status, body = self.client.add_merge(from_id, to_id)
        if status == 400:
            self._ok(f"reject {from_id}->{to_id}", f"({hint}) body={body}")
            return True
        self._fail(f"reject {from_id}->{to_id}",
                   f"({hint}) expected 400, got {status} body={body}")
        return False

    # ---- tests ----

    def test_basic_chain(self):
        """A->B->C; 折叠后 A->C, B->C"""
        print(f"\n[Test 1] basic chain {self.A}->{self.B}, {self.B}->{self.C}")
        self._add_expect_ok(self.A, self.B)
        self._add_expect_ok(self.B, self.C)
        mm = self.client.get_merge_map()
        self._ok("A folds to C", f"got {mm.get(self.A)}") if mm.get(self.A) == self.C \
            else self._fail("A folds to C", f"got {mm.get(self.A)}, want {self.C}")
        self._ok("B folds to C", f"got {mm.get(self.B)}") if mm.get(self.B) == self.C \
            else self._fail("B folds to C", f"got {mm.get(self.B)}, want {self.C}")

    def test_direct_cycle(self):
        """C->A 应被拒 (现有 A->B->C, 加 C->A 直接成环)"""
        print(f"\n[Test 2] direct cycle {self.C}->{self.A} should be rejected")
        self._add_expect_reject(self.C, self.A, hint="A->B->C + C->A = cycle")

    def test_self_loop(self):
        """from == to 应被拒"""
        print(f"\n[Test 3] self loop {self.E}->{self.E} should be rejected")
        self._add_expect_reject(self.E, self.E, hint="self merge")

    def test_idempotent(self):
        """重复 add 同样映射应被接受 (幂等)"""
        print(f"\n[Test 4] idempotent re-add {self.A}->{self.B}")
        self._add_expect_ok(self.A, self.B)

    def test_change_target(self):
        """把 A 的目标从 B 换成 E: 不应形成环; A 折叠到 E, B 不变"""
        print(f"\n[Test 5] change target {self.A}: B -> E")
        self._add_expect_ok(self.A, self.E)
        mm = self.client.get_merge_map()
        self._ok("A folds to E", f"got {mm.get(self.A)}") if mm.get(self.A) == self.E \
            else self._fail("A folds to E", f"got {mm.get(self.A)}, want {self.E}")
        self._ok("B still folds to C", f"got {mm.get(self.B)}") if mm.get(self.B) == self.C \
            else self._fail("B still folds to C", f"got {mm.get(self.B)}, want {self.C}")

    def test_indirect_cycle_via_change(self):
        """在 [A->E, B->C] 基础上加 E->A: 应被拒 (A->E->A 环)"""
        print(f"\n[Test 6] indirect cycle via change {self.E}->{self.A} should be rejected")
        self._add_expect_reject(self.E, self.A, hint="A->E + E->A = cycle")

    def test_three_node_chain(self):
        """新一组 id, F->A->E; F 折叠到 E"""
        print(f"\n[Test 7] three-node chain {self.F}->{self.A}, expect F to fold to {self.E}")
        self._add_expect_ok(self.F, self.A)
        mm = self.client.get_merge_map()
        self._ok("F folds to E", f"got {mm.get(self.F)}") if mm.get(self.F) == self.E \
            else self._fail("F folds to E", f"got {mm.get(self.F)}, want {self.E}")

    def test_long_chain(self):
        """长链 D->F->A->E (F->A 在 test 7 已加), 加 D->F 后 D 折叠到 E"""
        print(f"\n[Test 8] long chain {self.D}->{self.F}, expect D to fold to {self.E}")
        self._add_expect_ok(self.D, self.F)
        mm = self.client.get_merge_map()
        self._ok("D folds to E", f"got {mm.get(self.D)}") if mm.get(self.D) == self.E \
            else self._fail("D folds to E", f"got {mm.get(self.D)}, want {self.E}")

    def test_unrelated_add(self):
        """新加一个独立分支 (D->C); 不应影响其他"""
        print(f"\n[Test 9] independent branch {self.D}->{self.C} (was {self.D}->{self.F})")
        self._add_expect_ok(self.D, self.C)
        mm = self.client.get_merge_map()
        self._ok("D folds to C now", f"got {mm.get(self.D)}") if mm.get(self.D) == self.C \
            else self._fail("D folds to C now", f"got {mm.get(self.D)}, want {self.C}")

    def test_bad_auth_signature(self):
        """签名错应该被 401"""
        print(f"\n[Test 10] bad signature should be 401")
        url = self.client.base_url + "/addMergeServer"
        body = json.dumps({"from_server_id": self.A, "to_server_id": self.C}).encode("utf-8")
        ts = str(int(time.time()))
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json",
            "ts": ts,
            "nc": "x",
            "sign": "deadbeef" * 8,
        }, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                status, txt = r.status, r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            status, txt = e.code, e.read().decode("utf-8")
        self._ok("bad-sign 401", f"status={status}") if status == 401 \
            else self._fail("bad-sign 401", f"got {status} body={txt}")

    def test_stale_ts(self):
        """ts 超出 ±10s 应该被 401"""
        print(f"\n[Test 11] stale ts should be 401")
        url = self.client.base_url + "/addMergeServer"
        body = json.dumps({"from_server_id": self.A, "to_server_id": self.C}).encode("utf-8")
        old_ts = str(int(time.time()) - 60)
        sign_val = sign("POST", old_ts, "x", self.client.secret)
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json",
            "ts": old_ts,
            "nc": "x",
            "sign": sign_val,
        }, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                status, _ = r.status, r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            status = e.code
        self._ok("stale-ts 401", f"status={status}") if status == 401 \
            else self._fail("stale-ts 401", f"got {status}")

    # ---- driver ----

    def run(self) -> bool:
        print(f"Using ids (this run): A={self.A} B={self.B} C={self.C} D={self.D} "
              f"E={self.E} F={self.F}")
        self.test_basic_chain()
        self.test_direct_cycle()
        self.test_self_loop()
        self.test_idempotent()
        self.test_change_target()
        self.test_indirect_cycle_via_change()
        self.test_three_node_chain()
        self.test_long_chain()
        self.test_unrelated_add()
        self.test_bad_auth_signature()
        self.test_stale_ts()

        total = self.passed + self.failed
        print(f"\n{'-' * 40}\n{self.passed}/{total} passed, {self.failed} failed")
        if self.failed == 0:
            print("All green.")
            print(f"Cleanup: DELETE FROM maple_merge_server WHERE from_server_id >= {self.A};")
        return self.failed == 0


def main():
    parser = argparse.ArgumentParser(description="Maple merge server test")
    parser.add_argument("--url", default=os.environ.get("MAPLE_URL", "http://127.0.0.1:9527"))
    parser.add_argument("--secret", default=os.environ.get("MAPLE_SECRET", ""))
    args = parser.parse_args()

    if not args.secret:
        print("ERROR: --secret 或环境变量 MAPLE_SECRET 必须设置", file=sys.stderr)
        sys.exit(2)

    client = MapleClient(args.url, args.secret)

    # 探活
    try:
        status, _ = client.get_all_merge()
        print(f"Connected to {args.url} (status={status})")
    except Exception as e:
        print(f"ERROR: 连不上 {args.url}: {e}", file=sys.stderr)
        sys.exit(3)

    runner = TestRunner(client)
    sys.exit(0 if runner.run() else 1)


if __name__ == "__main__":
    main()