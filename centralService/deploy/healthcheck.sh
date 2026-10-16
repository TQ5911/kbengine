#!/usr/bin/env bash
# ============================================================================
#  centralService 健康检查
#
#  对每个服务同时验证三件事：
#    1. systemd 单元处于 active
#    2. pid 文件存在（程序启动时会写 <服务名>_0.pid，见 src/common/Pidfile.go）
#    3. 配置里声明的监听端口可以建立 TCP 连接
#
#  端口连不上通常意味着：配置没渲染对、依赖的 MySQL/Redis 不通、
#  或程序在初始化阶段就退出了。
#
#  用法：
#      ./deploy/healthcheck.sh                # 全量
#      ./deploy/healthcheck.sh maple router   # 只查指定服务
#      ./deploy/healthcheck.sh --timeout 60   # 启动后等待端口的最长时间
# ============================================================================
set -uo pipefail   # 故意不加 -e：检查失败要继续跑完并汇总

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "$SCRIPT_DIR/lib/common.sh"

ENV_FILE="$DEPLOY_DIR/deploy.env"
INSTANCES_FILE="$DEPLOY_DIR/instances.conf"
TIMEOUT=5
ONLY=()

while [ $# -gt 0 ]; do
    case "$1" in
        -e|--env)       ENV_FILE="$2"; shift 2 ;;
        -i|--instances) INSTANCES_FILE="$2"; shift 2 ;;
        -t|--timeout)   TIMEOUT="$2"; shift 2 ;;
        -h|--help)      sed -n '2,25p' "$0"; exit 0 ;;
        -*)             die "未知参数: $1" ;;
        *)              ONLY+=("$1"); shift ;;
    esac
done

[ -f "$ENV_FILE" ] || die "找不到 $ENV_FILE"
load_env_file "$ENV_FILE"
INSTALL_ROOT="${INSTALL_ROOT:-/home/fengyan/Server/centralService/bin}"
UNIT_PREFIX="${UNIT_PREFIX:-centralsvc}"
read_instances "$INSTANCES_FILE"

targets=("${INSTANCE_NAMES[@]}")
if [ ${#ONLY[@]} -gt 0 ]; then
    targets=()
    for want in "${ONLY[@]}"; do
        found=0
        for svc in "${INSTANCE_NAMES[@]}"; do
            if [ "$svc" = "$want" ]; then
                targets+=("$svc")
                found=1
            fi
        done
        [ "$found" -eq 1 ] || die "服务清单里没有: $want"
    done
fi

printf '\n%-18s %-8s %-9s %s\n' "SERVICE" "UNIT" "PID" "PORTS"
printf '%s\n' "----------------------------------------------------------------------"

fail_services=()
total=0

for svc in "${targets[@]}"; do
    total=$((total + 1))
    unit="$(unit_name "$svc")"

    # 1) systemd
    if systemctl is-active --quiet "$unit" 2>/dev/null; then
        unit_state="$(systemctl is-active "$unit" 2>/dev/null || echo unknown)"
        if [ "$unit_state" = "active" ]; then
            unit_mark="active"
        else
            unit_mark="$unit_state"
        fi
    else
        unit_state="$(systemctl is-active "$unit" 2>/dev/null || echo inactive)"
        unit_mark="${unit_state:-inactive}"
        fail_services+=("$svc(unit)")
        # 203/EXEC 这类「进程没起来」的失败在日志里什么都没有，
        # 不点破的话会一直往「服务崩溃」的方向查。
        explain_unit_failure "$svc"
    fi

    # 2) pid 文件
    pidfile="$INSTALL_ROOT/$svc/${svc}_0.pid"
    if [ -f "$pidfile" ]; then
        pid="$(cat "$pidfile" 2>/dev/null)"
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            pid_mark="$pid"
        else
            pid_mark="stale"
            fail_services+=("$svc(pid)")
        fi
    else
        pid_mark="-"
        fail_services+=("$svc(pid)")
    fi

    # 3) 端口探测
    ports="${INSTANCE_PORTS[$svc]}"
    port_marks=()
    for p in ${ports//,/ }; do
        [ -n "$p" ] || continue
        ok=no
        waited=0
        while [ "$waited" -le "$TIMEOUT" ]; do
            if tcp_probe 127.0.0.1 "$p"; then
                ok=yes
                break
            fi
            sleep 1
            waited=$((waited + 1))
        done
        if [ "$ok" = "yes" ]; then
            port_marks+=("$p${C_GRN}✓${C_RST}")
        else
            port_marks+=("$p${C_RED}✗${C_RST}")
            fail_services+=("$svc(:$p)")
        fi
    done
    port_str="$(printf '%s ' "${port_marks[@]}")"

    printf '%-18s %-8s %-9s %s\n' "$svc" "$unit_mark" "$pid_mark" "$port_str"
done

printf '%s\n' "----------------------------------------------------------------------"

if [ ${#fail_services[@]} -eq 0 ]; then
    printf '%s全部 %d 个服务健康%s\n\n' "$C_GRN" "$total" "$C_RST"
    exit 0
fi

printf '%s%d/%d 项异常：%s%s\n\n' "$C_RED" "${#fail_services[@]}" "$((total * 2))" \
    "${fail_services[*]}" "$C_RST"
cat <<'EOF'
排查顺序：
  1. systemctl status <单元>        看退出码
     status=203/EXEC 表示二进制压根没被执行（不是崩溃），
     先 ls -l / file / 手动跑一次；其余 200+ 也是这个意思
  2. tail -50 $INSTALL_ROOT/<服务名>/<服务名>.out.log   进程 stdout/stderr
  3. tail -50 $INSTALL_ROOT/<服务名>/<服务名>.log       业务日志
  4. journalctl -u <单元> -n 50     只有 systemd 自己的消息
     （LOG_STDOUT_MODE=file 时业务输出不进 journald）
  5. 确认配置在 $INSTALL_ROOT/<服务名>/<服务名>.json
     （文件名必须等于服务名，程序靠可执行文件所在目录名去找它）

EOF
exit 1