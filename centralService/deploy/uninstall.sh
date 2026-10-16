#!/usr/bin/env bash
# ============================================================================
#  centralService 卸载
#
#  默认只移除 systemd 单元与程序文件，保留数据目录与备份，
#  避免误删业务日志和回滚用的二进制。
#
#  用法：
#      sudo ./deploy/uninstall.sh                # 停服务 + 删单元 + 删程序文件
#      sudo ./deploy/uninstall.sh --purge        # 连数据目录和备份一起删（不可恢复）
#      sudo ./deploy/uninstall.sh --keep-files   # 只停服务和删单元，文件原样保留
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "$SCRIPT_DIR/lib/common.sh"

ENV_FILE="$DEPLOY_DIR/deploy.env"
INSTANCES_FILE="$DEPLOY_DIR/instances.conf"
PURGE=0
KEEP_FILES=0

while [ $# -gt 0 ]; do
    case "$1" in
        -e|--env)       ENV_FILE="$2"; shift 2 ;;
        -i|--instances) INSTANCES_FILE="$2"; shift 2 ;;
        --purge)        PURGE=1; shift ;;
        --keep-files)   KEEP_FILES=1; shift ;;
        -h|--help)      sed -n '2,14p' "$0"; exit 0 ;;
        *)              die "未知参数: $1" ;;
    esac
done

[ "$(id -u)" -eq 0 ] || die "需要 root 权限，请用 sudo $0"

INSTALL_ROOT="/home/fengyan/Server/centralService/bin"
UNIT_PREFIX="centralsvc"
if [ -f "$ENV_FILE" ]; then
    load_env_file "$ENV_FILE"
    INSTALL_ROOT="${INSTALL_ROOT:-/home/fengyan/Server/centralService/bin}"
    UNIT_PREFIX="${UNIT_PREFIX:-centralsvc}"
fi
read_instances "$INSTANCES_FILE"

log_step "停止服务"
for svc in "${INSTANCE_NAMES[@]}"; do
    unit="$(unit_name "$svc")"
    if systemctl list-unit-files "$unit" --no-legend 2>/dev/null | grep -q "$unit"; then
        systemctl disable --now "$unit" >/dev/null 2>&1 || true
        log_ok "已停止并取消自启: $unit"
    else
        log_dim "$svc 未安装，跳过"
    fi
done

log_step "移除 systemd 单元"
for svc in "${INSTANCE_NAMES[@]}"; do
    unit="$(unit_name "$svc")"
    rm -f "/etc/systemd/system/$unit"
    log_dim "已删除 $unit"
done
systemctl daemon-reload

if [ "$KEEP_FILES" -eq 1 ]; then
    log_ok "已保留程序文件: $INSTALL_ROOT"
    exit 0
fi

log_step "移除程序文件"
for svc in "${INSTANCE_NAMES[@]}"; do
    if [ -d "$INSTALL_ROOT/$svc" ]; then
        rm -rf "$INSTALL_ROOT/$svc"
        log_ok "已删除 $INSTALL_ROOT/$svc"
    fi
done
rm -f /etc/nginx/conf.d/centralsvc-admin.conf

if [ "$PURGE" -eq 1 ]; then
    rm -rf "$INSTALL_ROOT"
    log_warn "已删除整个安装目录 $INSTALL_ROOT（含日志与回滚备份）"
else
    # 只删共享数据目录，保留 .rollback 便于回溯
    if [ -d "$INSTALL_ROOT/data" ]; then
        rm -rf "$INSTALL_ROOT/data"
        log_ok "已删除共享数据目录 $INSTALL_ROOT/data"
    fi
    if [ -d "$INSTALL_ROOT/.rollback" ]; then
        log_info "保留回滚备份: $INSTALL_ROOT/.rollback（加 --purge 可一并删除）"
    fi
fi

if id -u "${SERVICE_USER:-fengyan}" >/dev/null 2>&1; then
    log_info "运行用户 ${SERVICE_USER:-fengyan} 仍保留，如需删除请手动 userdel"
fi

echo
log_ok "卸载完成"