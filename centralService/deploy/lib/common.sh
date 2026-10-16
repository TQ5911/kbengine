#!/usr/bin/env bash
# ============================================================================
#  centralService 部署工具公共库
#
#  被 install.sh / upgrade.sh / healthcheck.sh / uninstall.sh 通过 source 引入。
#  本文件只定义函数和常量，不执行任何动作。
#
#  依赖：bash 4+（关联数组）、python3（配置渲染）
# ============================================================================

# 让 source 进来的脚本也能拿到路径
DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ----------------------------------------------------------------------------
#  仓库根目录定位
#
#  deploy/ 目录常常被单独拷到别处（比如只拷 deploy/ 到 /tmp/deploy），
#  这时「deploy 的上一级」根本不是仓库。定位顺序：
#    1. 命令行 --repo-root
#    2. 环境变量 CENTRAL_REPO_ROOT
#    3. 从 deploy/ 往上找带 go.mod + src/ 的目录（标准布局）
#    4. 常见的自建目录
#  判据用 go.mod + src/，因为 bin/ 可能整个缺失（新 clone 出来就是这样）。
# ----------------------------------------------------------------------------
REPO_ROOT_HINT="$(cd "$DEPLOY_DIR/.." && pwd)"
REPO_ROOT="$REPO_ROOT_HINT"

_is_repo_root() {
    [ -n "${1:-}" ] && [ -d "$1" ] && [ -f "$1/go.mod" ] && [ -d "$1/src" ]
}

resolve_repo_root() {
    local explicit="${1:-}" dir

    if [ -n "$explicit" ]; then
        _is_repo_root "$explicit" && { printf '%s' "$explicit"; return 0; }
        die "指定的仓库目录无效: $explicit
       判据是该目录下同时存在 go.mod 和 src/"
    fi

    if [ -n "${CENTRAL_REPO_ROOT:-}" ]; then
        _is_repo_root "$CENTRAL_REPO_ROOT" && { printf '%s' "$CENTRAL_REPO_ROOT"; return 0; }
        die "CENTRAL_REPO_ROOT 无效: $CENTRAL_REPO_ROOT（该目录下应有 go.mod 和 src/）"
    fi

    # 3. 从 deploy/ 往上找
    dir="$DEPLOY_DIR"
    while :; do
        if _is_repo_root "$dir"; then
            printf '%s' "$dir"
            return 0
        fi
        [ "$dir" = "/" ] || [ -z "$dir" ] && break
        dir="$(dirname "$dir")"
    done

    # 4. 常见自建目录。sudo 运行时 $HOME 常常被换成 /root，
    #    所以把发起 sudo 的那个用户的家目录也算进来。
    local candidates=() sudo_home=""
    candidates+=("$HOME/Server/centralService" "$HOME/centralService"
                 "$HOME/src/centralService" "/data/centralService")
    if [ -n "${SUDO_USER:-}" ] && [ "$SUDO_USER" != "root" ]; then
        sudo_home="$(getent passwd "$SUDO_USER" 2>/dev/null | cut -d: -f6)"
        if [ -n "$sudo_home" ]; then
            candidates+=("$sudo_home/Server/centralService" "$sudo_home/centralService")
        fi
    fi
    for dir in "${candidates[@]}"; do
        if _is_repo_root "$dir"; then
            printf '%s' "$dir"
            return 0
        fi
    done

    return 1
}

# 解析并导出，失败时把排查方法一并打出来
set_repo_root() {
    if ! REPO_ROOT="$(resolve_repo_root "${1:-}")"; then
        log_err "找不到仓库根目录（该目录下需要同时有 go.mod 和 src/）"
        cat >&2 <<EOF

  脚本当前在: $DEPLOY_DIR
  向上找到的: $REPO_ROOT_HINT（这里没有 go.mod）

  三种指定方式，任选其一：
    1) 把整个仓库连同 deploy/ 一起拷贝，保持 deploy/ 在仓库内
    2) 传参:         sudo bash install.sh --repo-root /path/to/centralService ...
    3) 传环境变量:   CENTRAL_REPO_ROOT=/path/to/centralService sudo bash install.sh ...
EOF
        exit 1
    fi
    export REPO_ROOT
    return 0
}

# 可执行文件来源目录。优先 dist/（交付产物），
# 没有时退回 bin/ 并提醒一句——退回是可接受的，因为
# verify_artifact.py 会拿它跟 src/ 比时间，过期照样会被拦下。
resolve_dist_dir() {
    local repo="$1" explicit="${2:-}"
    if [ -n "$explicit" ]; then
        printf '%s' "$explicit"
        return 0
    fi
    if [ -d "$repo/dist" ]; then
        printf '%s' "$repo/dist"
        return 0
    fi
    printf '%s' "$repo/bin"
    return 0
}

# ============================================================================
#  日志
# ============================================================================
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
    C_RED=$'\033[31m'; C_YEL=$'\033[33m'; C_GRN=$'\033[32m'
    C_BLU=$'\033[34m'; C_DIM=$'\033[2m'; C_BLD=$'\033[1m'; C_RST=$'\033[0m'
else
    C_RED=''; C_YEL=''; C_GRN=''; C_BLU=''; C_DIM=''; C_BLD=''; C_RST=''
fi

log_step() { printf '%s==>%s %s%s%s\n'      "$C_BLU" "$C_RST" "$C_BLD" "$*" "$C_RST"; }
log_info() { printf '    %s\n'              "$*"; }
log_ok()   { printf '    %s✔%s %s\n'       "$C_GRN" "$C_RST" "$*"; }
log_warn() { printf '    %s! %s%s\n'        "$C_YEL" "$*" "$C_RST" >&2; }
log_err()  { printf '    %s�’%s %s\n'      "$C_RED" "$C_RST" "$*" >&2; }
log_dim()  { printf '    %s%s%s\n'          "$C_DIM" "$*" "$C_RST"; }
die()      { log_err "$*"; exit 1; }

# ============================================================================
#  环境与前置检查
# ============================================================================
require_root() {
    [ "$(id -u)" -eq 0 ] || die "需要 root 权限，请用 sudo $0 $*"
}

require_cmd() {
    local missing=() c
    for c in "$@"; do
        command -v "$c" >/dev/null 2>&1 || missing+=("$c")
    done
    [ ${#missing[@]} -eq 0 ] || die "缺少命令: ${missing[*]}"
}

require_systemd() {
    [ -d /run/systemd/system ] || die "当前环境未运行 systemd，本方案只支持 systemd 发行版"
    command -v systemctl >/dev/null 2>&1 || die "找不到 systemctl"
}

# 找一个真正能用的 python。Linux 上就是 python3；
# 但开发机在 Windows Git Bash 里跑时，python3 可能只是 Microsoft Store 的
# 占位符（存在但一执行就报错），这时退回 python。
PYTHON=""
require_python() {
    if [ -n "$PYTHON" ]; then
        return 0
    fi
    if command -v python3 >/dev/null 2>&1 && python3 -c 'pass' >/dev/null 2>&1; then
        PYTHON=python3
    elif command -v python >/dev/null 2>&1 && python -c 'pass' >/dev/null 2>&1; then
        PYTHON=python
    else
        die "找不到可用的 python3（Debian/RHEL 装 python3，Alpine 装 python3）"
    fi
    return 0
}

# 加载 KEY=VALUE 形式的 env 文件
load_env_file() {
    local file="$1"
    [ -f "$file" ] || die "找不到环境文件: $file（可从 deploy.env.example 复制）"
    set -a
    # shellcheck disable=SC1090
    . "$file"
    set +a
}

# ============================================================================
#  服务清单（instances.conf）
# ============================================================================
INSTANCE_NAMES=()
declare -A INSTANCE_PORTS=()      # 服务名 -> 探活端口，逗号分隔
declare -A INSTANCE_DB_INIT=()    # 服务名 -> yes/no
declare -A INSTANCE_DESC=()       # 服务名 -> 说明

read_instances() {
    local file="$1" line name ports dbi desc
    [ -f "$file" ] || die "找不到服务清单: $file"

    INSTANCE_NAMES=()
    local -A seen_ports=()
    local -A seen_dbinit=()
    local -A seen_desc=()
    local lineno=0

    while IFS= read -r line || [ -n "$line" ]; do
        lineno=$((lineno + 1))
        line="${line%$'\r'}"                 # 去掉 Windows 换行符
        line="${line%%#*}"                  # 去掉注释（注意：值里不能带 #）
        line="${line#"${line%%[![:space:]]*}"}"   # ltrim
        line="${line%"${line##*[![:space:]]}"}"   # rtrim
        # 注意：这里必须用 if 而不能用 [ -z "$line" ] && continue。
        # 条件为假时整条 && 语句返回 1，调用方若开了 set -e 会直接退出。
        if [ -z "$line" ]; then
            continue
        fi

        IFS='|' read -r name ports dbi desc <<< "$line"
        name="${name// /}"
        if [ -z "$name" ]; then
            continue
        fi

        case "$name" in
            *[!a-zA-Z0-9_]*)
                die "instances.conf 第 $lineno 行：服务名非法 [$name]，只允许字母数字下划线" ;;
        esac

        seen_ports[$name]="${ports// /}"
        seen_dbinit[$name]="${dbi// /}"
        seen_desc[$name]="${desc#"${desc%%[![:space:]]*}"}"
        INSTANCE_NAMES+=("$name")
    done < "$file"

    [ ${#INSTANCE_NAMES[@]} -gt 0 ] || die "服务清单为空: $file"

    # 去重
    local -A dup=()
    for name in "${INSTANCE_NAMES[@]}"; do
        if [ -n "${dup[$name]:-}" ]; then
            die "instances.conf 中服务重复: $name"
        fi
        dup[$name]=1
    done

    local n
    for n in "${INSTANCE_NAMES[@]}"; do
        INSTANCE_PORTS[$n]="${seen_ports[$n]}"
        INSTANCE_DB_INIT[$n]="${seen_dbinit[$n]:-no}"
        INSTANCE_DESC[$n]="${seen_desc[$n]}"
        [ "${INSTANCE_DB_INIT[$n]}" = "yes" ] || [ "${INSTANCE_DB_INIT[$n]}" = "no" ] \
            || die "instances.conf 中 $n 的 db_init 只能是 yes/no（当前: ${INSTANCE_DB_INIT[$n]}）"
    done
}

# ============================================================================
#  端口探测
# ============================================================================

# 端口是否已被任何进程监听（用于部署前的冲突检查）
port_in_use() {
    local port="$1"
    if command -v ss >/dev/null 2>&1; then
        ss -ltn 2>/dev/null | awk -v p=":$port\$" 'NR>1 && $4 ~ p {found=1} END {exit found?0:1}'
    elif command -v netstat >/dev/null 2>&1; then
        netstat -ltn 2>/dev/null | awk -v p=":$port\$" 'NR>2 && $4 ~ p {found=1} END {exit found?0:1}'
    else
        return 2   # 无探测手段
    fi
}

# TCP 连接探测（用于服务启动后的存活检查）
tcp_probe() {
    local host="$1" port="$2"
    (exec 3<>"/dev/tcp/${host}/${port}") >/dev/null 2>&1
}

# 等待端口可连接；成功返回 0
wait_for_port() {
    local host="$1" port="$2" timeout="${3:-30}" waited=0
    while [ "$waited" -lt "$timeout" ]; do
        if tcp_probe "$host" "$port"; then
            return 0
        fi
        sleep 1
        waited=$((waited + 1))
    done
    return 1
}

# ============================================================================
#  systemd 单元
# ============================================================================
unit_name() { printf '%s-%s.service' "${UNIT_PREFIX:-centralsvc}" "$1"; }

unit_is_active() {
    systemctl is-active --quiet "$(unit_name "$1")" 2>/dev/null
}

# ---- 启动失败原因解读 ------------------------------------------------------
# systemd 用 200+ 的退出码表示「进程压根没起来」，跟程序自己 return 的码
# 不是一个意思。这些码在 systemctl status 里显示为 status=203/EXEC 这种形式，
# 光看数字完全不知道发生了什么，而 Restart=always 会把它刷成一串重启记录，
# 很容易被误读成「服务起来又崩了」——实际上一次都没成功启动过。
explain_unit_failure() {
    local svc="$1" unit st root
    unit="$(unit_name "$svc")"
    st="$(systemctl show "$unit" -p ExecMainStatus --value 2>/dev/null || echo "")"
    [ -n "$st" ] || return 0
    root="${PREFIX:-${INSTALL_ROOT:-/home/fengyan/Server/centralService/bin}}/$svc"

    case "$st" in
        203)    # EXIT_EXEC：execve() 失败，二进制根本没被执行
            cat >&2 <<EOF

  $svc 的退出码是 203/EXEC —— systemd 执行 ${root}/$svc 失败，
  进程一次都没启动成功（不是起来后崩溃）。按这个顺序查：

    namei -l ${root}/$svc
      最该先看的一条：它把路径上每一级的权限和属主都列出来。
      只要有任何一级是 750/700 且属主不是服务用户，进程就走不到二进制，
      典型是安装目录放在某个用户的家目录下（/home/<某人>/...），
      而服务以另一个账号运行 —— 上一层目录没有 x 权限，execve 直接 EACCES。

    ls -l ${root}/$svc                       # 有没有可执行位
    file ${root}/$svc                        # 是不是 linux/amd64 的 ELF
    cd ${root} && ./$svc --instid=0          # 绕开 systemd 直接跑，看真实报错

    systemctl cat $unit | grep -E 'ProtectHome|ProtectSystem'
      安装目录在 /home 下时，ProtectHome=true 会把 /home 挂成空 tmpfs，
      systemd 先 chdir 成功、再 execve，于是二进制"不见了"→ ENOENT/203。
      本脚本已按安装路径自动决定这个值，手工改过单元的话要留意这一条。

    sudo journalctl -u $unit -n 50 --no-pager
      失败原因是 systemd（root）自己打的，普通用户看不到，会显示
      "-- No entries --"，必须加 sudo。想免 sudo 就把自己加进组：
      sudo usermod -aG systemd-journal \$USER（重新登录生效）。

  其余常见原因：二进制没有 +x；拷成了 Windows 的 .exe 或别的架构；
  ExecStart 路径与目录名不同名；挂载选项带 noexec。
EOF
            ;;
        217) cat >&2 <<EOF

  $svc 的退出码是 217/SELINUX_CONTEXT —— SELinux 拒绝了这次启动。
  排查: ausearch -m avc -ts recent | grep $svc
EOF
            ;;
        226) cat >&2 <<EOF

  $svc 的退出码是 226/CGROUP —— 创建 cgroup 失败，检查 cgroup v2 与
  MemoryAccounting/CPUAccounting 相关设置。
EOF
            ;;
        200|201|202|204|205|206|207|208|209|210|211|212|213|214|215|216|218|219|220|221|222|223|224|225|227)
            log_dim "$svc 退出码 $st 是 systemd 保留码（进程未成功启动，不是崩溃），详见 systemd.exec(5) 的 Process Exit Codes"
            ;;
        *) : ;;   # 程序自己的退出码，交给业务日志
    esac
}

# ---- 日志去向 --------------------------------------------------------------
# 业务日志由程序自己写在 WorkingDirectory 下（<服务名>.log，见 render_config.py
# 的 LOG_IN_SERVICE_DIR）。这里决定的是 stdout/stderr：
#   file    -> <服务目录>/<服务名>.out.log
#   journal -> journald
# 用 append: 而不是 file:，后者每次启动都会清空，崩溃重启时等于把上一次的
# 退出原因抹掉了。
stdout_target() {
    local svc="$1"
    case "${LOG_STDOUT_MODE:-file}" in
        file)     printf 'append:%s' "${PREFIX:-/home/fengyan/Server/centralService/bin}/$svc/$svc.out.log" ;;
        journal)  printf 'journal' ;;
        *) die "LOG_STDOUT_MODE 只能是 file 或 journal（当前: ${LOG_STDOUT_MODE:-file}）" ;;
    esac
}

# ---- systemd 加固：ProtectHome -------------------------------------------
# ProtectHome=true 会把 /home、/root、/run/user 整体挂成一个空 tmpfs。
# 安装目录在 /home/<用户>/... 下面时，systemd 的执行顺序是
#   chdir(WorkingDirectory)  →  搭 mount namespace  →  execve(ExecStart)
# chdir 发生在命名空间搭好之前，走到的是真实 /home，所以能成功；
# 之后 /home 被空 tmpfs 盖住，execve 一个"看不见"的路径 → ENOENT，
# 表现就是 systemctl status 里的 status=203/EXEC，而 journal 里一个字都没有
# （进程压根没起来，也没有 stdout），查起来极其费劲。
# 所以安装根目录落在受保护路径下时必须关掉它。
protect_home_value() {
    if [ -n "${SYSTEMD_PROTECT_HOME:-}" ]; then
        printf '%s' "$SYSTEMD_PROTECT_HOME"
        return 0
    fi
    case "${PREFIX:-${INSTALL_ROOT:-}}" in
        /home|/home/*|/root|/root/*|/run/user|/run/user/*) printf 'no' ;;
        *) printf 'true' ;;
    esac
}

# 把 --status/-n 等开关规整成布尔
is_true() {
    case "${1,,}" in
        1|y|yes|true|on)   return 0 ;;
        0|n|no|false|off)  return 1 ;;
        *) die "无法识别的布尔值: $1" ;;
    esac
}

# ============================================================================
#  模板渲染（@KEY@ 占位符，纯 bash 实现，无外部依赖）
# ============================================================================
declare -A TPL_VARS=()

tpl_set() { TPL_VARS["$1"]="${2:-}"; }

tpl_clear() { TPL_VARS=(); }

# render_template <模板路径> <输出路径>
# 输出路径不会自动创建目录以外的权限，权限由调用方设置。
render_template() {
    local src="$1" dst="$2" key line
    [ -f "$src" ] || die "模板不存在: $src"
    mkdir -p "$(dirname "$dst")"
    : > "$dst"
    while IFS= read -r line || [ -n "$line" ]; do
        for key in "${!TPL_VARS[@]}"; do
            line="${line//@${key}@/${TPL_VARS[$key]}}"
        done
        printf '%s\n' "$line" >> "$dst"
    done < "$src"
}

# 把路径转成绝对路径。
# 必须这么做：构建脚本会 cd 到 src/<服务名>/ 再执行 go build，
# 相对输出路径在 cd 之后会指向完全不同的位置，产物会被悄悄写到
# src/<服务名>/dist/ 下，而校验读的是仓库根的 dist/，于是"构建成功"但文件没更新。
abspath() {
    local p="${1:-.}"
    case "$p" in
        /*|[A-Za-z]:[\\/]*) printf '%s' "$p" ;;
        *)                  printf '%s/%s' "${PWD%/}" "$p" ;;
    esac
}

# 校验模板渲染结果是否还有没被替换的占位符，避免装出一个带 @FOO@ 的配置
# 只看有效配置行：注释里出现 @XXX@ 只是说明文字，不算残留。
tpl_assert_no_leftover() {
    local file="$1" leftover
    leftover="$( { grep -vE '^[[:space:]]*#' "$file" 2>/dev/null || true; } \
                 | { grep -oE '@[A-Z0-9_]+@' || true; } \
                 | sort -u | tr '\n' ' ' )"
    [ -z "${leftover// /}" ] || die "渲染结果 $file 仍有未替换的占位符: $leftover"
    return 0
}

# ============================================================================
#  服务用户
# ============================================================================
ensure_service_user() {
    local user="$1" group="$2"
    if getent group "$group" >/dev/null 2>&1; then
        log_dim "用户组已存在: $group"
    else
        groupadd --system "$group"
        log_ok "创建用户组: $group"
    fi
    if id -u "$user" >/dev/null 2>&1; then
        log_dim "用户已存在: $user"
    else
        useradd --system --gid "$group" --home-dir "$INSTALL_ROOT" \
                --shell /usr/sbin/nologin --no-create-home "$user"
        log_ok "创建用户: $user"
    fi
}