#!/bin/bash
set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$SCRIPT_DIR/src"

if [ ! -d "$SRC_DIR" ]; then
    echo "src directory not found: $SRC_DIR" >&2
    exit 1
fi

ran=0
failed=0
for dir in "$SRC_DIR"/*/; do
    if [ -x "$dir/build.sh" ]; then
        ran=$((ran + 1))
        name=$(basename "$dir")
        echo "==> building $name"
        if (cd "$dir" && ./build.sh); then
            echo "    OK"
        else
            echo "    FAILED ($name)"
            failed=$((failed + 1))
        fi
    fi
done

if [ "$ran" -eq 0 ]; then
    echo "no build.sh found under $SRC_DIR" >&2
    exit 1
fi

if [ "$failed" -gt 0 ]; then
    echo "$failed/$ran build(s) failed"
    exit 1
fi

echo "All $ran build processes are successfully"