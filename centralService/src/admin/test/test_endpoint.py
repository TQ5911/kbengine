#!/usr/bin/env python3
import sys
import requests

ADMIN_HTTP_API = "http://127.0.0.1:8080"


def call_test():
    url = ADMIN_HTTP_API + "/test"
    resp = requests.get(url, timeout=5)
    print(f"status={resp.status_code}")
    print(f"body={resp.text}")
    resp.raise_for_status()
    return resp.text


if __name__ == "__main__":
    try:
        call_test()
    except Exception as e:
        print(f"call /test failed: {e}", file=sys.stderr)
        sys.exit(1)
