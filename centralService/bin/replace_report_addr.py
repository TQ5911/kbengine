#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="批量修改所有 JSON 配置文件顶层的 reportAddr")
    parser.add_argument("report_addr", help="新的 reportAddr")
    args = parser.parse_args()

    bin_dir = Path(__file__).resolve().parent
    changed_files = []

    for path in sorted(bin_dir.rglob("*.json")):
        try:
            with path.open("r", encoding="utf-8-sig") as file:
                config = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            print(f"[跳过] {path.relative_to(bin_dir)}: {error}")
            continue

        if not isinstance(config, dict) or "reportAddr" not in config:
            continue

        old_addr = config["reportAddr"]
        if old_addr == args.report_addr:
            continue

        config["reportAddr"] = args.report_addr
        with path.open("w", encoding="utf-8", newline="\n") as file:
            json.dump(config, file, ensure_ascii=False, indent=4)
            file.write("\n")

        print(f"[已修改] {path.relative_to(bin_dir)}: {old_addr!r} -> {args.report_addr!r}")
        changed_files.append(path.relative_to(bin_dir))

    print("\n成功检测并修改的文件：")
    if changed_files:
        for path in changed_files:
            print(f"  {path}")
    else:
        print("  无")
    print(f"共修改 {len(changed_files)} 个文件")


if __name__ == "__main__":
    main()
