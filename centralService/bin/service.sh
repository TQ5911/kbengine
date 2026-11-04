#!/bin/bash
# ============================================================================
# service.sh - 按服务名批量执行 start / stop / restart / status
#
# 用法:
#   ./service.sh <服务名> [服务名...] <start|stop|restart|status>
#   ./service.sh <start|stop|restart|status> <服务名> [服务名...]
#   ./service.sh all <start|stop|restart|status>
#
# 示例:
#   ./service.sh maple dropServer restart   # 重启 maple 和 dropServer
#   ./service.sh restart maple dropServer   # 同上（动作放前面也行）
#   ./service.sh all stop                   # 停止所有服务
#   ./service.sh maple status               # 只看 maple 状态
#
# ---------------------------------------------------------------------------
# 两种执行模式（自动选择，逐服务判定）
# ---------------------------------------------------------------------------
#   systemd 模式: 存在 centralsvc-<服务名>.service 时走 systemctl（生产环境）。
#                 必须走 systemctl —— unit 里是 Restart=always，
#                 直接调 game.sh 启停会被 systemd 拉回来，两边互相打架。
#   game.sh 模式: 没有对应 unit 时退化到 <服务名>/game.sh（开发机 / 未纳管服务）。
#
#   强制指定模式: --systemd  /  --no-systemd（等价 --game-sh）
#
# ---------------------------------------------------------------------------
# 说明
# ---------------------------------------------------------------------------
#   1. 动作关键字放最前或最后都可以，脚本会自动识别；
#   2. 服务名必须对应 bin 下的同名目录（systemd 模式下目录只用于校验，
#      game.sh 模式下必须目录里有 game.sh，且会 cd 进去执行 ——
#      game.sh 依赖 $PWD 推导二进制路径）；
#   3. all = 除 data / proto / __pycache__ 外的所有服务，
#      且按 deploy/instances.conf 的依赖顺序处理（stop 时倒序）；
#      手工指定的服务名则按你写的顺序处理，不做重排；
#   4. game.sh 模式下 stop/restart 会等进程真正退出（默认 15s），
#      超时后升级 kill -9 —— game.sh 的 stop 只发信号不等退出，
#      紧跟着 start 会撞上「pid 文件还在」的竞态而失败；
#      systemd 模式下 systemctl stop/restart 本身是同步的，不需要额外等待；
#   5. 任何一个服务失败，脚本最终以非 0 退出。
#
# 环境变量:
#   UNIT_PREFIX    systemd 单元前缀，默认 centralsvc（与 deploy/lib/common.sh 一致）
#   STOP_TIMEOUT   game.sh 模式下等待退出的秒数，默认 15
#   NO_COLOR       非空则关闭颜色输出
# ============================================================================

set -u

# ---------------------------------------------------------------------------
# 基础配置
# ---------------------------------------------------------------------------

# 排除的目录（与 start_all.sh / stop_all.sh 保持一致，另加 __pycache__）
EXCLUDE_DIRS=" data proto __pycache__ "

# game.sh 模式下等待进程退出的超时时间（秒）
STOP_TIMEOUT=${STOP_TIMEOUT:-15}

# systemd 单元前缀，与 deploy/lib/common.sh 的 unit_name() 保持一致
UNIT_PREFIX=${UNIT_PREFIX:-centralsvc}

# 切到脚本所在目录，保证从任何路径调用都能正常工作
SELF_NAME=$(basename "$0")
SELF_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SELF_DIR" || exit 1

# 终端颜色（非 tty 或 NO_COLOR 时自动关闭）
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
    C_RED=$'\033[31m'
    C_GRN=$'\033[32m'
    C_YEL=$'\033[33m'
    C_CYN=$'\033[36m'
    C_DIM=$'\033[2m'
    C_BLD=$'\033[1m'
    C_OFF=$'\033[0m'
else
    C_RED=""; C_GRN=""; C_YEL=""; C_CYN=""; C_DIM=""; C_BLD=""; C_OFF=""
fi

# ---------------------------------------------------------------------------
# 输出辅助
# ---------------------------------------------------------------------------
log_info()  { echo "${C_CYN}[$ACTION]${C_OFF} $*"; }
log_ok()    { echo "${C_GRN}[$ACTION]${C_OFF} $*"; }
log_warn()  { echo "${C_YEL}[$ACTION]${C_OFF} $*" >&2; }
log_err()   { echo "${C_RED}[$ACTION]${C_OFF} $*" >&2; }
log_hint()  { echo "${C_DIM}       $*${C_OFF}"; }

usage() {
    cat <<'EOF'
用法:
  ./service.sh <服务名> [服务名...] <start|stop|restart|status>
  ./service.sh <start|stop|restart|status> <服务名> [服务名...]
  ./service.sh all <start|stop|restart|status>

选项:
  --systemd          强制走 systemctl（缺省会报错，不会静默回退）
  --no-systemd       强制走 <服务名>/game.sh（等价于 --game-sh）
  -h, --help         显示本帮助

示例:
  ./service.sh maple dropServer restart   # 重启 maple 和 dropServer
  ./service.sh restart maple dropServer   # 同上（动作放前面也行）
  ./service.sh all stop                   # 停止所有服务（按依赖倒序）
  ./service.sh maple status               # 只看 maple 状态
  ./service.sh all start --no-systemd     # 全部绕过 systemd，直接 game.sh

可用服务:
EOF
    local d
    for d in */; do
        d=${d%/}
        case "$EXCLUDE_DIRS" in *" $d "*) continue ;; esac
        [ -d "$d" ] || continue
        if [ -f "$d/game.sh" ]; then
            echo "  $d"
        else
            echo "  $d ${C_DIM}(缺少 game.sh)${C_OFF}"
        fi
    done
    echo
    echo "systemd 单元名: $UNIT_PREFIX-<服务名>.service"
}

# ---------------------------------------------------------------------------
# 参数解析
# ---------------------------------------------------------------------------
ACTION=""
FORCE_MODE=""          # 空=自动 / systemd / game
SERVICES=()
USE_ALL=0

for arg in "$@"; do
    case "$arg" in
        start|stop|restart|status)
            if [ -n "$ACTION" ]; then
                ACTION="<none>"
                log_err "检测到多个动作参数，只能指定一个: $*"
                exit 2
            fi
            ACTION=$arg
            ;;
        --systemd)
            FORCE_MODE=systemd
            ;;
        --no-systemd|--game-sh|--game)
            FORCE_MODE=game
            ;;
        -h|--help|help)
            usage
            exit 0
            ;;
        all)
            USE_ALL=1
            ;;
        *)
            SERVICES+=("$arg")
            ;;
    esac
done

if [ -z "$ACTION" ]; then
    ACTION="<none>"
    log_err "缺少动作参数，必须是 start|stop|restart|status 之一"
    echo
    usage
    exit 2
fi

if [ "$USE_ALL" -eq 0 ] && [ ${#SERVICES[@]} -eq 0 ]; then
    log_err "缺少服务名，至少要指定一个服务，或使用 all 表示全部"
    echo
    usage
    exit 2
fi

# ---------------------------------------------------------------------------
# 启动顺序（all 时使用；与 deploy/instances.conf 保持一致）
# ---------------------------------------------------------------------------
SERVICE_ORDER="centralLogin queueServer router maple auction orderService \
allianceService leaseServer dropServer crossDataServer crossTeamServer admin"

# 同机上能读到 instances.conf 就以它为准，避免两处维护产生漂移
for conf in "$SELF_DIR/../deploy/instances.conf" "$SELF_DIR/instances.conf"; do
    if [ -r "$conf" ]; then
        parsed=$(awk -F'|' '
            /^[[:space:]]*#/ { next }
            /^[[:space:]]*$/ { next }
            { gsub(/[ \t\r]/, "", $1); if ($1 != "") print $1 }
        ' "$conf")
        if [ -n "$parsed" ]; then
            SERVICE_ORDER=$(printf '%s' "$parsed" | tr '\n' ' ')
            break
        fi
    fi
done

# 返回服务在启动顺序中的序号，不在清单里的返回 999（排最后）
order_index() {
    local svc=$1 s i=0
    for s in $SERVICE_ORDER; do
        i=$((i + 1))
        if [ "$s" = "$svc" ]; then
            echo $i
            return 0
        fi
    done
    echo 999
}

# 按启动顺序稳定排序（sort -s 保证同序号时保持原有相对顺序）
order_services() {
    local svc indexed="" ordered="" line
    for svc in "$@"; do
        indexed="$indexed$(order_index "$svc") $svc
"
    done
    ordered=$(printf '%s' "$indexed" | sort -s -n -k1,1 | cut -d' ' -f2-)
    while IFS= read -r line; do
        [ -n "$line" ] && echo "$line"
    done <<EOF
$ordered
EOF
}

# ---------------------------------------------------------------------------
# 收集服务列表
# ---------------------------------------------------------------------------
targets=()
if [ "$USE_ALL" -eq 1 ]; then
    if [ ${#SERVICES[@]} -gt 0 ]; then
        log_warn "已指定 all，忽略同时给出的服务名: ${SERVICES[*]}"
    fi
    for d in */; do
        d=${d%/}
        case "$EXCLUDE_DIRS" in *" $d "*) continue ;; esac
        [ -d "$d" ] || continue
        [ -f "$d/game.sh" ] || continue
        targets+=("$d")
    done
    if [ ${#targets[@]} -eq 0 ]; then
        log_err "没有找到任何服务目录（排除目录: $EXCLUDE_DIRS）"
        exit 1
    fi
    # all 按依赖顺序；stop 是倒序
    ordered=()
    while IFS= read -r line; do
        [ -n "$line" ] && ordered+=("$line")
    done <<EOF
$(order_services "${targets[@]}")
EOF
    targets=("${ordered[@]}")
    if [ "$ACTION" = "stop" ]; then
        rev=()
        for ((i = ${#targets[@]} - 1; i >= 0; i--)); do
            rev+=("${targets[i]}")
        done
        targets=("${rev[@]}")
    fi
else
    targets=("${SERVICES[@]}")
fi

# ---------------------------------------------------------------------------
# 服务名校验
# ---------------------------------------------------------------------------
valid_services=()
for svc in "${targets[@]}"; do
    case "$EXCLUDE_DIRS" in
        *" $svc "*)
            log_warn "跳过保留目录: $svc"
            continue
            ;;
    esac
    if [ ! -d "$SELF_DIR/$svc" ]; then
        log_err "服务目录不存在: $SELF_DIR/$svc"
        continue
    fi
    if [ "$FORCE_MODE" != "systemd" ] && [ ! -f "$SELF_DIR/$svc/game.sh" ]; then
        log_err "$svc 目录下没有 game.sh，跳过"
        continue
    fi
    valid_services+=("$svc")
done

if [ ${#valid_services[@]} -eq 0 ]; then
    log_err "没有可操作的服务，退出"
    exit 1
fi

# ---------------------------------------------------------------------------
# systemd 环境探测
# ---------------------------------------------------------------------------
unit_name() { printf '%s-%s.service' "$UNIT_PREFIX" "$1"; }

# systemd 是否可用：不仅要有 systemctl，还得确实是它在管这台机器
SYSTEMD_OK=0
if [ -d /run/systemd/system ] && command -v systemctl >/dev/null 2>&1; then
    SYSTEMD_OK=1
fi

# 非 root 时需要 sudo
if [ "$(id -u)" -eq 0 ]; then
    SUDO=""
elif command -v sudo >/dev/null 2>&1; then
    SUDO=sudo
else
    SUDO=""
fi

unit_exists() {
    systemctl cat "$1" >/dev/null 2>&1 && return 0
    [ -n "$SUDO" ] && $SUDO systemctl cat "$1" >/dev/null 2>&1 && return 0
    return 1
}

# 读取单元属性，输出 "state|sub|pid|execstatus|nrestarts"
sysd_props() {
    local out
    out=$(systemctl show "$1" -p ActiveState -p SubState -p MainPID \
                              -p ExecMainStatus -p NRestarts 2>/dev/null)
    if [ -z "$out" ] && [ -n "$SUDO" ]; then
        out=$($SUDO systemctl show "$1" -p ActiveState -p SubState -p MainPID \
                                        -p ExecMainStatus -p NRestarts 2>/dev/null)
    fi
    printf '%s' "$out" | awk -F= '
        $1 == "ActiveState"    { a = $2 }
        $1 == "SubState"       { s = $2 }
        $1 == "MainPID"        { p = $2 }
        $1 == "ExecMainStatus" { e = $2 }
        $1 == "NRestarts"      { n = $2 }
        END { printf "%s|%s|%s|%s|%s\n", a, s, p, e, n }'
}

sysd_run() {
    # $1=动词(start/stop/restart) $2=unit
    if [ -n "$SUDO" ]; then
        $SUDO systemctl "$1" "$2"
    else
        systemctl "$1" "$2"
    fi
}

# 逐服务判定执行模式，结果写入 MODE_<服务名> 形式太脏，改用平行数组
svc_modes=()
for svc in "${valid_services[@]}"; do
    unit=$(unit_name "$svc")
    case "$FORCE_MODE" in
        systemd)
            if [ "$SYSTEMD_OK" -eq 0 ]; then
                log_err "$svc: 已强制 --systemd，但本机 systemctl 不可用"
                svc_modes+=("systemd-unavailable")
            elif ! unit_exists "$unit"; then
                log_err "$svc: 已强制 --systemd，但找不到单元 $unit"
                svc_modes+=("systemd-missing")
            else
                svc_modes+=("systemd")
            fi
            ;;
        game)
            svc_modes+=("game")
            ;;
        *)
            if [ "$SYSTEMD_OK" -eq 1 ] && unit_exists "$unit"; then
                svc_modes+=("systemd")
            else
                svc_modes+=("game")
            fi
            ;;
    esac
done

# ---------------------------------------------------------------------------
# game.sh 模式的进程工具函数
# ---------------------------------------------------------------------------

# 列出某服务 pid 文件里的 pid（game.sh 命名: <服务名>_<instId>.pid）
svc_pids() {
    local svc=$1 f pid
    for f in "$SELF_DIR/$svc/${svc}_"*.pid; do
        [ -f "$f" ] || continue
        pid=$(cat "$f" 2>/dev/null | tr -d '[:space:]')
        case "$pid" in
            ''|*[!0-9]*) continue ;;
            *) echo "$pid" ;;
        esac
    done
}

svc_alive() {
    local pid
    for pid in $(svc_pids "$1"); do
        kill -0 "$pid" 2>/dev/null && return 0
    done
    return 1
}

# 等待进程退出；$1=服务名 $2=超时秒数
wait_exit() {
    local svc=$1 timeout=$2 waited=0 steps
    steps=$((timeout * 2))
    while [ $waited -lt $steps ]; do
        svc_alive "$svc" || return 0
        sleep 0.5
        waited=$((waited + 1))
    done
    svc_alive "$svc" && return 1
    return 0
}

# ---------------------------------------------------------------------------
# 动作实现
# ---------------------------------------------------------------------------
FAILED=0

call_game_sh() {
    local svc=$1 act=$2
    (
        cd "$SELF_DIR/$svc" || exit 1
        if [ -x ./game.sh ]; then
            ./game.sh "$act"
        else
            # SVN 检出可能没带可执行位，退化成 bash 调用
            bash ./game.sh "$act"
        fi
    )
}

sudo_hint() {
    if [ -n "$SUDO" ] && [ ! -t 0 ]; then
        log_hint "若上面是 sudo 鉴权失败，先在交互终端执行 sudo -v 再重试"
    fi
}

do_systemd_start() {
    local svc=$1 unit=$2 props state sub pid
    props=$(sysd_props "$unit")
    state=${props%%|*}; rest=${props#*|}
    sub=${rest%%|*};    rest=${rest#*|}
    pid=${rest%%|*}
    if [ "$state" = "active" ] && [ "$sub" = "running" ]; then
        log_info "$svc 已在运行（$unit, pid=$pid），跳过启动"
        return 0
    fi

    log_info "启动 $svc（systemctl start $unit）..."
    if ! sysd_run start "$unit"; then
        log_err "$svc 启动失败"
        sudo_hint
        return 1
    fi
    log_ok "$svc 已启动"
    return 0
}

do_systemd_stop() {
    local svc=$1 unit=$2 props state
    props=$(sysd_props "$unit")
    state=${props%%|*}
    if [ "$state" = "inactive" ] || [ "$state" = "unknown" ]; then
        log_info "$svc 当前未运行（$state），跳过停止"
        return 0
    fi

    # systemctl stop 本身是同步的，会一直等到单元停止或超时
    log_info "停止 $svc（systemctl stop $unit）..."
    if ! sysd_run stop "$unit"; then
        log_err "$svc 停止失败"
        sudo_hint
        return 1
    fi
    log_ok "$svc 已停止"
    return 0
}

do_systemd_restart() {
    local svc=$1 unit=$2
    log_info "重启 $svc（systemctl restart $unit）..."
    if ! sysd_run restart "$unit"; then
        log_err "$svc 重启失败"
        sudo_hint
        return 1
    fi
    log_ok "$svc 已重启"
    return 0
}

do_game_start() {
    local svc=$1
    log_info "启动 $svc（game.sh start）..."
    if call_game_sh "$svc" start; then
        log_ok "$svc 启动命令已下发"
    else
        log_err "$svc 启动失败（可能进程已在运行）"
        return 1
    fi
    return 0
}

do_game_stop() {
    local svc=$1
    log_info "停止 $svc（game.sh stop）..."
    call_game_sh "$svc" stop

    if ! svc_alive "$svc"; then
        log_ok "$svc 已停止"
        return 0
    fi

    log_hint "等待 $svc 退出（最多 ${STOP_TIMEOUT}s）..."
    if wait_exit "$svc" "$STOP_TIMEOUT"; then
        log_ok "$svc 已停止"
        return 0
    fi

    log_warn "$svc 在 ${STOP_TIMEOUT}s 内未退出，发送 SIGKILL"
    for pid in $(svc_pids "$svc"); do
        kill -9 "$pid" 2>/dev/null
    done
    if wait_exit "$svc" 5; then
        log_ok "$svc 已强制停止"
        return 0
    fi

    log_err "$svc 停止失败，残留 pid: $(svc_pids "$svc" | tr '\n' ' ')"
    return 1
}

do_game_restart() {
    local svc=$1
    log_info "重启 $svc ..."
    do_game_stop "$svc" || return 1
    sleep 1    # 保险起见，等端口 / pid 文件释放
    do_game_start "$svc" || return 1
    log_ok "$svc 重启完成"
    return 0
}

# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
mode_desc=""
for i in "${!valid_services[@]}"; do
    mode_desc="$mode_desc ${valid_services[i]}(${svc_modes[i]})"
done

echo "=============================================================="
echo " 动作   : ${C_CYN}$ACTION${C_OFF}"
echo " 服务   : ${C_CYN}${valid_services[*]}${C_OFF}"
echo " 模式   : ${C_DIM}${mode_desc# }${C_OFF}"
echo " 目录   : ${C_DIM}$SELF_DIR${C_OFF}"
echo "=============================================================="

for i in "${!valid_services[@]}"; do
    svc=${valid_services[i]}
    mode=${svc_modes[i]}
    unit=$(unit_name "$svc")

    case "$mode" in
        systemd-unavailable|systemd-missing)
            log_err "$svc 无法操作，跳过"
            FAILED=$((FAILED + 1))
            continue
            ;;
    esac

    case "$ACTION" in
        start)
            if [ "$mode" = "systemd" ]; then
                do_systemd_start "$svc" "$unit" || FAILED=$((FAILED + 1))
            else
                do_game_start "$svc" || FAILED=$((FAILED + 1))
            fi
            ;;
        stop)
            if [ "$mode" = "systemd" ]; then
                do_systemd_stop "$svc" "$unit" || FAILED=$((FAILED + 1))
            else
                do_game_stop "$svc" || FAILED=$((FAILED + 1))
            fi
            ;;
        restart)
            if [ "$mode" = "systemd" ]; then
                do_systemd_restart "$svc" "$unit" || FAILED=$((FAILED + 1))
            else
                do_game_restart "$svc" || FAILED=$((FAILED + 1))
            fi
            ;;
        status)
            :    # 纯查询，下面统一输出
            ;;
    esac
done

# ---------------------------------------------------------------------------
# 收尾：状态总览
# ---------------------------------------------------------------------------
echo
echo "-------------------------------- 状态总览 --------------------------------"
# 表头用中文（一个汉字占 2 列），故手工补空格而非 %-18s；
# 数据行都是 ASCII，用 printf 对齐即可
echo "服务$(printf '%15s' '')模式$(printf '%7s' '')状态$(printf '%21s' '')备注"

# 先按纯文本算宽度再上色，否则 ANSI 转义码会被计入 %-24s 的占位
fmt_row() {   # $1=服务 $2=模式 $3=状态纯文本 $4=颜色变量内容 $5=备注
    printf "%-18s %-10s %s %s\n" "$1" "$2" "$4$(printf '%-24s' "$3")${C_OFF}" "$5"
}

for i in "${!valid_services[@]}"; do
    svc=${valid_services[i]}
    mode=${svc_modes[i]}
    unit=$(unit_name "$svc")

    case "$mode" in
        systemd-unavailable|systemd-missing)
            fmt_row "$svc" "-" "不可操作" "$C_RED" "$unit"
            continue
            ;;
    esac

    if [ "$mode" = "systemd" ]; then
        props=$(sysd_props "$unit")
        state=${props%%|*}; rest=${props#*|}
        sub=${rest%%|*};    rest=${rest#*|}
        pid=${rest%%|*};    rest=${rest#*|}
        execst=${rest%%|*}
        case "$state" in
            active)   color=$C_GRN ;;
            inactive) color=$C_DIM ;;
            failed)   color=$C_RED ;;
            *)        color=$C_YEL ;;
        esac
        st="$state"
        [ -n "$sub" ] && st="$st($sub)"
        note="$unit"
        [ -n "$pid" ] && [ "$pid" != "0" ] && note="$note pid=$pid"
        fmt_row "$svc" "systemd" "$st" "$color" "$note"

        # 起不来的典型情况给出排查方向
        if [ "$ACTION" != "stop" ] && [ "$ACTION" != "status" ] && [ "$state" != "active" ]; then
            log_warn "$svc 未处于 active，排查: sudo journalctl -u $unit -n 50 --no-pager"
            [ -n "$execst" ] && [ "$execst" != "0" ] && \
                log_hint "退出码 status=$execst（203/EXEC 通常表示二进制路径或权限问题）"
        fi
    else
        if svc_alive "$svc"; then
            fmt_row "$svc" "game.sh" "运行中" "$C_GRN" "pid=$(svc_pids "$svc" | tr '\n' ' ')"
        else
            fmt_row "$svc" "game.sh" "未运行" "$C_DIM" "无存活进程"
        fi
    fi
done
echo "------------------------------------------------------------------------"

if [ "$FAILED" -ne 0 ]; then
    echo
    log_err "完成，但有 $FAILED 个服务执行失败"
    exit 1
fi

echo
log_ok "全部完成"
exit 0
