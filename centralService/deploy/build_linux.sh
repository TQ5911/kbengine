#!/usr/bin/env bash
# ============================================================================
#  构建交付用的 Linux 二进制
#
#  产物落在 dist/<服务名>/<服务名>，与 bin/ 严格分开。
#
#  为什么要分开
#  ------------
#  bin/ 这个目录历史上同时堆着四类东西：配置基线（要入库）、
#  编译出来的二进制、win32 的 .exe 和 vendored 的 protoc（都不要入库），
#  还有本地跑出来的 log / pid / nohup.out。
#  把交付物料也放在这里，--skip-build 就等于「把 bin/ 里躺着的东西直接装上」，
#  而那些二进制可能是几周前编译的，没有任何东西会提醒你。
#
#  dist/ 是干净的：只有 build_linux.sh 写进去的东西，一对一对应。
#  install.sh 从这里取，并且会校验格式、架构和新鲜度
#  （见 lib/verify_artifact.py）。
#
#  可以在 Windows / macOS / Linux 上执行，产出统一的 Linux 可执行文件。
#
#  用法
#  ----
#      ./deploy/build_linux.sh                     # 全部服务
#      ./deploy/build_linux.sh maple router        # 只构建指定服务
#      ./deploy/build_linux.sh --out-dir /tmp/pkg  # 换输出目录
#      GOARCH=arm64 ./deploy/build_linux.sh        # 交叉编译 arm64
#
#  交付时把 dist/ 连同仓库一起拷到目标机，然后：
#      sudo ./deploy/install.sh --skip-build --strict-ips
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR=""
DIST_DIR=""

export GOOS="${GOOS:-linux}"
export GOARCH="${GOARCH:-amd64}"
# 依赖全是纯 Go（go-sql-driver / redigo / grpc / viper / zap / lumberjack），
# 关掉 CGO 才能产出不依赖特定 glibc 版本的二进制。
export CGO_ENABLED="${CGO_ENABLED:-0}"

. "$SCRIPT_DIR/lib/common.sh"

usage() {
    cat <<'EOF'
用法: build_linux.sh [--out-dir DIR] [服务名...]

选项:
  -o, --out-dir DIR   产物目录（默认 <仓库>/dist）

可构建的服务（src/ 下含 main.go 的目录）:
EOF
    for d in "$SRC_DIR"/*/; do
        [ -f "${d}main.go" ] && echo "  $(basename "$d")"
    done
    cat <<'EOF'

环境变量:
  GOOS    目标系统，默认 linux
  GOARCH  目标架构，默认 amd64（可选 arm64）
EOF
}

while [ $# -gt 0 ]; do
    case "$1" in
        -o|--out-dir) DIST_DIR="$2"; shift 2 ;;
        -h|--help)    usage; exit 0 ;;
        -*)           die "未知参数: $1" ;;
        *)            break ;;
    esac
done

set_repo_root ""
SRC_DIR="$REPO_ROOT/src"

require_cmd go
[ -d "$SRC_DIR" ] || die "找不到源码目录: $SRC_DIR"

# 关键：输出目录必须是绝对路径。下面的 go build 是在 cd 到 src/<服务名>/ 之后
# 执行的，相对路径会写到 src/<服务名>/dist/ 下面去，看起来成功实则没更新产物。
[ -n "$DIST_DIR" ] || DIST_DIR="$REPO_ROOT/dist"
DIST_DIR="$(abspath "$DIST_DIR")"

targets=()
if [ $# -gt 0 ]; then
    targets=("$@")
else
    for d in "$SRC_DIR"/*/; do
        [ -f "${d}main.go" ] || continue
        targets+=("$(basename "$d")")
    done
fi
[ ${#targets[@]} -gt 0 ] || die "src/ 下没有找到带 main.go 的服务"

mkdir -p "$DIST_DIR"
log_step "构建 ${#targets[@]} 个服务"
go version | head -1 | sed 's/^/    /'
log_info "目标平台 ${GOOS}/${GOARCH}   CGO_ENABLED=${CGO_ENABLED}   输出 $DIST_DIR"
echo

failed=()
for svc in "${targets[@]}"; do
    dir="$SRC_DIR/$svc"
    if [ ! -f "$dir/main.go" ]; then
        log_err "$svc 没有 main.go，跳过"
        failed+=("$svc")
        continue
    fi

    out_dir="$DIST_DIR/$svc"
    mkdir -p "$out_dir"

    # 先把随行文件（配置、SQL、证书）从 bin/ 拷过来。
    # 注意顺序：必须在 go build 之前。bin/<服务名>/ 下躺着一个同名的旧二进制，
    # 如果先 build 再拷贝，cp -a 会把刚编出来的产物覆盖回那个旧文件。
    if [ -d "$REPO_ROOT/bin/$svc" ]; then
        cp -a "$REPO_ROOT/bin/$svc/." "$out_dir/" 2>/dev/null || true
        rm -f "$out_dir/$svc.exe" "$out_dir/nohup.out" 2>/dev/null || true
        rm -f "$out_dir"/*.log "$out_dir"/*.pid "$out_dir"/*.bak 2>/dev/null || true
    fi

    # 直接调 go build，不复用 src/<服务名>/build.sh：
    # 那份脚本把输出路径硬编码成 ../../bin/<服务名>/，没法控制输出目录。
    if ! ( cd "$dir" && go build -o "$out_dir/$svc" main.go ); then
        log_err "$svc 编译失败"
        failed+=("$svc")
        continue
    fi

    # 兜底：go build 退出码为 0 也可能没写到预期位置（路径被相对化、被 cd 带偏等），
    # 所以显式确认产物真的在那里
    if [ ! -f "$out_dir/$svc" ]; then
        log_err "$svc 编译后找不到产物: $out_dir/$svc"
        failed+=("$svc")
        continue
    fi

    # go build 用 umask 下的默认权限，显式补上可执行位
    chmod 0755 "$out_dir/$svc"

    size="$(du -h "$out_dir/$svc" | cut -f1)"
    log_ok "$(printf '%-18s %6s' "$svc" "$size")"
done

echo
if [ ${#failed[@]} -gt 0 ]; then
    die "以下服务构建失败: ${failed[*]}"
fi

# 交付前自检：格式、架构、有没有比源码旧
log_step "产物校验"
require_python
"$PYTHON" "$SCRIPT_DIR/lib/verify_artifact.py" \
    --repo-root "$REPO_ROOT" \
    --dist-dir "$DIST_DIR" \
    --instances "$SCRIPT_DIR/instances.conf" \
    --arch "$GOARCH" || true

cat <<EOF

交付方式（目标机不需要 Go）：

    # dist/ 连同仓库一起拷过去，然后
    sudo ./deploy/install.sh --skip-build --strict-ips

EOF