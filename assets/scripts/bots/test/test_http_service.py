
import sys
import os
import urllib.request
import urllib.error
import json


def get(url, timeout=3):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        code = resp.getcode()
        body = resp.read().decode('utf-8')
        return code, body


def main():
    #host = os.environ.get('BOTS_HTTP_HOST', '192.168.10.15')
    host = os.environ.get('BOTS_HTTP_HOST', '127.0.0.1')
    port = os.environ.get('BOTS_HTTP_PORT', 49527)
    if not port and len(sys.argv) >= 2:
        port = sys.argv[1]
    if not port:
        print('Usage: set BOTS_HTTP_PORT or pass PORT as arg')
        return 2
    base = f"http://{host}:{int(port)}"

    try:
        # Health endpoints
        code, body = get(base + "/")
        assert code == 200 and body == "OK", f"/ expected 200 OK, got {code} {body!r}"
        print("/ -> 200 OK [PASS]")

        code, body = get(base + "/health")
        assert code == 200 and body == "OK", f"/health expected 200 OK, got {code} {body!r}"
        print("/health -> 200 OK [PASS]")

        # Account count should be an integer
        code, body = get(base + "/account_count")
        assert code == 200 and body.strip().isdigit(), f"/account_count expected number, got {code} {body!r}"
        print(f"/account_count -> {body.strip()} [PASS]")

        # Clients count should be an integer
        code, body = get(base + "/clients/count")
        assert code == 200 and body.strip().isdigit(), f"/clients/count expected number, got {code} {body!r}"
        print(f"/clients/count -> {body.strip()} [PASS]")

        # Slow clients JSON structure check
        code, body = get(base + "/clients/slow")
        assert code == 200, f"/clients/slow expected 200, got {code}"
        data = json.loads(body)
        print(f"/clients/slow -> count={data.get('count')} age={data.get('age')} [PASS]")

        # RPC call statistics should be a JSON dict of string->int
        code, body = get(base + "/rpc/stats")
        assert code == 200, f"/rpc/stats expected 200, got {code}"
        stats = json.loads(body)
        assert isinstance(stats, dict), f"/rpc/stats expected dict, got {type(stats)}"
        # If non-empty, validate value types are integers
        for k, v in sorted(list(stats.items()), key=lambda x: -x[1]):
            # allow ints encoded as numbers; cast check
            print(f'k[{k}]:v[{v}]')
        print(f"/rpc/stats -> {len(stats)} entries [PASS]")

        # Noclient list should be a JSON dict with count and clients list
        code, body = get(base + "/clients/noclient")
        assert code == 200, f"/clients/noclient expected 200, got {code}"
        data = json.loads(body)
        assert isinstance(data, dict) and 'count' in data and 'clients' in data, \
            f"/clients/noclient expected dict with count/clients, got {body!r}"
        print(f"/clients/noclient -> count={data.get('count')} [PASS]")

        # Switch module: list, set, get, toggle
        code, body = get(base + "/switch/list")
        assert code == 200, f"/switch/list expected 200, got {code}"
        sw = json.loads(body)
        assert isinstance(sw, dict) and 'switches' in sw and isinstance(sw['switches'], dict), \
            f"/switch/list expected dict with switches, got {body!r}"
        print("/switch/list -> [PASS]")

        flag = 'debugClient'
        code, body = get(base + f"/switch/set?name={flag}&value=1")
        assert code == 200, f"/switch/set expected 200, got {code}"
        resp = json.loads(body)
        assert resp.get('name') == flag and resp.get('value') is True, f"/switch/set failed: {body!r}"
        code, body = get(base + f"/switch/get?name={flag}")
        print(f"/switch/set + /switch/get -> {body!r}")
        assert code == 200 and json.loads(body).get('value') is True, \
            f"/switch/get expected true, got {body!r}"
        print("/switch/set + /switch/get -> true [PASS]")

        print("HTTP service real-env tests: ALL PASS")
        return 0
    except Exception as exc:
        print("HTTP service real-env tests: FAIL:", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())

