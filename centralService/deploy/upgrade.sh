#!/usr/bin/env bash
# ============================================================================
#  centralService 灰度升级（失败自动回滚）
#
#  逐服务执行：停 → 备份现有二进制 → 换新 → 起 → 探活
#  任一服务探活失败，立刻把该服务回滚到升级前的二进制并重新拉起，
#  已经升级成功的服务保持新版本（不回滚），由人工决定是否继续。
#
#  只处理二进制。配置变更请走 install.sh --skip-build，
#  两者混在一起会让回滚语义变模糊。
#
#  用法：
#      sudo ./deploy/upgrade.sh                      # 编译并升级全部
#      sudo ./deploy/upgrade.sh maple router         # 只升这两个
#      sudo ./deploy/upgrade.sh --no-build           # 用 bin/ 下已有的二进制
#      sudo ./deploy/upgrade.sh --timeout 120        # 探活等待更久
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "$SCRIPT_DIR/lib/common.sh"

export PYTHONIOENCODING=utf-8

ENV_FILE="$DEPLOY_DIR/deploy.env"
INSTANCES_FILE="$DEPLOY_DIR/instances.conf"
REPO_ROOT_OPT=""
DIST_DIR=""
TIMEOUT=60
KEEP_BACKUPS=5
DO_BUILD=1
ONLY=()

while [ $# -gt 0 ]; do
    case "$1" in
        -e|--env)       ENV_FILE="$2"; shift 2 ;;
        -i|--instances) INSTANCES_FILE="$2"; shift 2 ;;
        -r|--repo-root) REPO_ROOT_OPT="$2"; shift 2 ;;
        -d|--dist-dir)  DIST_DIR="$2"; shift 2 ;;
        -t|--timeout)   TIMEOUT="$2"; shift 2 ;;
        --no-build)     DO_BUILD=0; shift ;;
        --keep)         KEEP_BACKUPS="$2"; shift 2 ;;
        -h|--help)      sed -n '2,22p' "$0"; exit 0 ;;
        -*)             die "未知参数: $1" ;;
        *)              ONLY+=("$1"); shift ;;
    esac
done

[ "$(id -u)" -eq 0 ] || die "需要 root 权限，请用 sudo $0"
[ -f "$ENV_FILE" ] || die "找不到 $ENV_FILE"
load_env_file "$ENV_FILE"

set_repo_root "$REPO_ROOT_OPT"
[ -n "$DIST_DIR" ] || DIST_DIR="$(resolve_dist_dir "$REPO_ROOT")"
log_info "仓库根目录: $REPO_ROOT"
log_info "二进制来源: $DIST_DIR"

INSTALL_ROOT="${INSTALL_ROOT:-/home/fengyan/Server/centralService/bin}"
UNIT_PREFIX="${UNIT_PREFIX:-centralsvc}"
SERVICE_USER="${SERVICE_USER:-fengyan}"
SERVICE_GROUP="${SERVICE_GROUP:-$SERVICE_USER}"
export SERVICE_USER SERVICE_GROUP
read_instances "$INSTANCES_FILE"

targets=("${INSTANCE_NAMES[@]}")
if [ ${#ONLY[@]} -gt 0 ]; then
    targets=()
    for want in "${ONLY[@]}"; do
        found=0
        for svc in "${INSTANCE_NAMES[@]}"; do
            if [ "$svc" = "$want" ]; then targets+=("$svc"); found=1; fi
        done
        [ "$found" -eq 1 ] || die "服务清单里没有: $want"
    done
fi

# ---------------------------------------------------------------------------
#  编译
# ---------------------------------------------------------------------------
if [ "$DO_BUILD" -eq 1 ]; then
    log_step "编译 Linux 二进制"
    "$DEPLOY_DIR/build_linux.sh" --out-dir "$DIST_DIR" "${targets[@]}"
else
    log_step "跳过编译，使用 $DIST_DIR 下已有二进制"
fi

# ---------------------------------------------------------------------------
#  校验产物：格式、架构、有没有比源码旧
# ---------------------------------------------------------------------------
log_step "校验待升级二进制"
require_python
"$PYTHON" "$DEPLOY_DIR/lib/verify_artifact.py" \
    --repo-root "$REPO_ROOT" \
    --dist-dir "$DIST_DIR" \
    --instances "$INSTANCES_FILE" \
    --strict-fresh \
    || die "二进制校验未通过，拒绝升级（详见上方输出）"

STAMP="$(date +%Y%m%d%H%M%S)"
BACKUP_ROOT="$INSTALL_ROOT/.rollback/$STAMP"
mkdir -p "$BACKUP_ROOT"
log_info "本次二进制备份目录: $BACKUP_ROOT"

# ---------------------------------------------------------------------------
#  单服务升级
# ---------------------------------------------------------------------------
upgrade_one() {
    local svc="$1"
    local unit="$(unit_name "$svc")"
    local live="$INSTALL_ROOT/$svc/$svc"
    local incoming="$DIST_DIR/$svc/$svc"
    local backup="$BACKUP_ROOT/$svc"

    [ -f "$live" ] || die "$svc 尚未部署过（$live 不存在），请先跑 install.sh"

    log_info "升级 $svc ..."

    systemctl stop "$unit" || true

    if [ -f "$live" ]; then
        mkdir -p "$backup"
        cp -p "$live" "$backup"
    fi

    if ! install -m 0755 "$incoming" "$live"; then
        log_err "$svc 替换二进制失败，尝试还原"
        if [ -f "$backup" ]; then
            cp -p "$backup" "$live"
        fi
        systemctl start "$unit" || true
        return 1
    fi
    chown "$SERVICE_USER":"$SERVICE_GROUP" "$live" 2>/dev/null || true

    if ! systemctl start "$unit"; then
        log_err "$svc 启动失败"
        journalctl -u "$unit" -n 20 --no-pager 2>/dev/null | sed 's/^/        /' >&2 || true
        rollback_one "$svc" "$backup"
        return 1
    fi

    # 端口探活
    local ports p failed_port=""
    ports="${INSTANCE_PORTS[$svc]}"
    for p in ${ports//,/ }; do
        [ -n "$p" ] || continue
        if ! wait_for_port 127.0.0.1 "$p" "$TIMEOUT"; then
            failed_port="$p"
            break
        fi
    done

    if [ -n "$failed_port" ]; then
        log_err "$svc 端口 :$failed_port 探活超时"
        rollback_one "$svc" "$backup"
        return 1
    fi

    log_ok "$svc 升级成功"
    return 0
}

rollback_one() {
    local svc="$1" backup="$2"
    local unit="$(unit_name "$svc")"
    if [ ! -f "$backup" ]; then
        log_err "$svc 没有可用备份，无法自动回滚，请人工介入"
        return 1
    fi
    log_warn "$svc 正在回滚到升级前版本 ..."
    systemctl stop "$unit" || true
    cp -p "$backup" "$INSTALL_ROOT/$svc/$svc"
    systemctl start "$unit" || true
    if wait_for_port 127.0.0.1 "${INSTANCE_PORTS[$svc]%%,*}" "$TIMEOUT"; then
        log_ok "$svc 已回滚并恢复运行"
    else
        log_err "$svc 回滚后仍未就绪，请人工排查"
        return 1
    fi
    return 0
}

# ---------------------------------------------------------------------------
#  主流程
# ---------------------------------------------------------------------------
log_step "开始升级 ${#targets[@]} 个服务（探活超时 ${TIMEOUT}s）"

succeeded=()
failed=()
for svc in "${targets[@]}"; do
    if upgrade_one "$svc"; then
        succeeded+=("$svc")
    else
        failed+=("$svc")
        log_warn "后续服务不再继续升级，已升级: ${succeeded[*]:-无}"
        break
    fi
done

# 清理过期的历史备份
if [ -d "$INSTALL_ROOT/.rollback" ]; then
    mapfile -t old_backups < <(ls -1d "$INSTALL_ROOT/.rollback"/*/ 2>/dev/null | sort -r)
    if [ ${#old_backups[@]} -gt "$KEEP_BACKUPS" ]; then
        for ((i = KEEP_BACKUPS; i < ${#old_backups[@]}; i++)); do
            rm -rf "${old_backups[$i]}"
            log_dim "清理旧备份: ${old_backups[$i]}"
        done
    fi
fi

echo
if [ ${#failed[@]} -eq 0 ]; then
    log_ok "全部 ${#succeeded[@]} 个服务升级完成（备份保留在 $BACKUP_ROOT）"
    exit 0
fi

log_err "升级中断，失败服务: ${failed[*]}"
log_info "已升级: ${succeeded[*]:-无}"
log_info "备份目录: $BACKUP_ROOT"
exit 1