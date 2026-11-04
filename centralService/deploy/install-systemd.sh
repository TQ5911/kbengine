#!/usr/bin/env bash
# ============================================================================
#  只给 centralService 安装 systemd 单元（薄封装）
#
#  与 install.sh 的关系：
#    install.sh        = 全量部署（编译 + 渲染 + 推文件 + 建库 + 装单元 + 启动）
#    本脚本            = 只装单元，前提是远程的起服文件（二进制、<服务名>.json、
#                        up.sh、data/）已经在位
#  两者共用同一份单元模板，不会各写一套。
#
#  典型用法：
#    ./deploy/install-systemd.sh --only maple                # 只给 maple 装单元
#    ./deploy/install-systemd.sh --only maple,admin          # 多个服务
#    ./deploy/install-systemd.sh                             # instances.conf 里的全部
#    ./deploy/install-systemd.sh --only maple --no-restart   # 只落单元，不动服务状态
#    ./deploy/install-systemd.sh --only maple --check        # 演练
#    ./deploy/install-systemd.sh --only maple --check-ports  # 装完等探活端口
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "$SCRIPT_DIR/lib/common.sh"
# shellcheck source=lib/ansible_helpers.sh
. "$SCRIPT_DIR/lib/ansible_helpers.sh"

export PYTHONIOENCODING=utf-8
export LC_ALL="${LC_ALL:-C.UTF-8}"
# 不能写成 ansible 的 -o：ad-hoc 的 -o 是 --one-line（不带参数）
export ANSIBLE_HOST_KEY_CHECKING=False

ENV_FILE="$DEPLOY_DIR/deploy.env"
INSTANCES_FILE="$DEPLOY_DIR/instances.conf"
PLAYBOOK="$DEPLOY_DIR/ansible/systemd-only.yml"

ONLY=""
PREFIX_OPT=""
SVC_STATE=""
ENABLE="true"
CHECK_PORTS="false"
PORT_TIMEOUT="60"
ENSURE_USER="true"
FIX_OWNER="false"
UNIT_BACKUP="true"
DO_CHECK=0
TAGS_OPT=""
LIMIT_OPT=""
VERBOSE=0

usage() {
    cat <<'EOF'
用法: ./deploy/install-systemd.sh [选项]

只做「安装 systemd 单元」这一件事，远程的起服文件必须已经就位。

选项:
  -s, --only NAME[,NAME]   只处理指定服务（默认 instances.conf 里的全部）
  -e, --env FILE           环境变量文件          (默认 deploy/deploy.env)
  -i, --instances FILE     服务清单              (默认 deploy/instances.conf)
  -p, --prefix DIR         远程服务文件所在根目录（默认取 deploy.env 的
                           ANSIBLE_REMOTE_PREFIX / INSTALL_ROOT）
      --no-restart         只生成单元，不改服务状态
      --start-only         只保证处于 started（已运行的不重启）
      --stop               装完单元后停掉服务
      --no-enable          不动开机自启设置
      --check-ports        装完等服务探活端口就绪
      --port-timeout SEC   探活超时（默认 60）
      --fix-owner          顺带递归修正安装根目录属主（默认不动已有文件）
      --no-backup          覆盖已有单元时不备份
      --check              ansible-playbook --check，只演练不落盘
      --tags TAGS         只跑 playbook 的某一段（validate/user/unit/reload/
                           service/verify/status）
      --limit PATTERN     传给 ansible-playbook 的 --limit
      --ansible-hosts H   覆盖 deploy.env 的 ANSIBLE_HOSTS
      --ansible-user U    覆盖 SSH 用户
      --ansible-inventory F
                          inventory 文件
  -v, --verbose          给 ansible-playbook 加 -v
  -h, --help             显示本帮助

示例:
  ./deploy/install-systemd.sh --only maple
  ./deploy/install-systemd.sh --only maple --check
  ./deploy/install-systemd.sh --only maple --no-restart --tags unit
EOF
}

while [ $# -gt 0 ]; do
    case "$1" in
        -s|--only)            ONLY="$2"; shift 2 ;;
        -e|--env)             ENV_FILE="$2"; shift 2 ;;
        -i|--instances)       INSTANCES_FILE="$2"; shift 2 ;;
        -p|--prefix)          PREFIX_OPT="$2"; shift 2 ;;
        --no-restart)         SVC_STATE=none; shift ;;
        --start-only)         SVC_STATE=started; shift ;;
        --stop)               SVC_STATE=stopped; shift ;;
        --no-enable)          ENABLE=false; shift ;;
        --check-ports)        CHECK_PORTS=true; shift ;;
        --port-timeout)       PORT_TIMEOUT="$2"; shift 2 ;;
        --fix-owner)          FIX_OWNER=true; shift ;;
        --no-backup)          UNIT_BACKUP=false; shift ;;
        --check)              DO_CHECK=1; shift ;;
        --tags)               TAGS_OPT="$2"; shift 2 ;;
        --limit)              LIMIT_OPT="$2"; shift 2 ;;
        --ansible-hosts)      ANSIBLE_HOSTS="$2"; shift 2 ;;
        --ansible-user)       ANSIBLE_USER="$2"; ANSIBLE_USER_OPT="$2"; shift 2 ;;
        --ansible-inventory)  ANSIBLE_INVENTORY="$2"; shift 2 ;;
        -v|--verbose)         VERBOSE=1; shift ;;
        -h|--help)            usage; exit 0 ;;
        *)                    die "未知参数: $1（用 --help 看用法）" ;;
    esac
done

# ---- 前置检查 --------------------------------------------------------------
require_python
require_cmd ansible-playbook
[ -f "$PLAYBOOK" ] || die "找不到 playbook: $PLAYBOOK"

[ -f "$ENV_FILE" ] || die "找不到 $ENV_FILE（先 cp deploy.env.example deploy.env）"
load_env_file "$ENV_FILE"

# 与 install.sh 同一个坑：deploy.env 用 set -a + source，会把值为空的
# ANSIBLE_* 也 export 出去；ansible 对 path 型配置（inventory、*_password_file）
# 拿到空串会 unfrackpath('') 解析成当前目录，然后把 deploy/ 当 inventory/口令脚本
# 去执行。空的 ANSIBLE_* 一律 unset，再重新赋空值（赋空值不带 export 属性）。
local_avar=""
for local_avar in $(compgen -e | grep '^ANSIBLE_' || true); do
    if [ -z "${!local_avar:-}" ]; then unset "$local_avar"; fi
done
: "${ANSIBLE_HOSTS:=tmp}"
: "${ANSIBLE_USER:=fengyan}"
: "${ANSIBLE_BECOME:=yes}"
: "${ANSIBLE_INVENTORY:=}"
: "${ANSIBLE_BECOME_PASSWORD_FILE:=}"
: "${ANSIBLE_VERBOSE:=0}"
[ "$VERBOSE" = "1" ] && ANSIBLE_VERBOSE=1

if [ -z "$ANSIBLE_INVENTORY" ] && [ -f "$DEPLOY_DIR/ansible/hosts" ]; then
    ANSIBLE_INVENTORY="$DEPLOY_DIR/ansible/hosts"
fi
_ansible_defaults

read_instances "$INSTANCES_FILE"
[ ${#INSTANCE_NAMES[@]} -gt 0 ] || die "服务清单为空: $INSTANCES_FILE"

# 安装根目录：命令行 > ANSIBLE_REMOTE_PREFIX > INSTALL_ROOT
if [ -n "$PREFIX_OPT" ]; then
    PREFIX="$PREFIX_OPT"
else
    PREFIX="${ANSIBLE_REMOTE_PREFIX:-${INSTALL_ROOT:-/home/fengyan/Server/centralService/bin}}"
fi
UNIT_PREFIX="${UNIT_PREFIX:-centralsvc}"
SERVICE_USER="${SERVICE_USER:-fengyan}"
SERVICE_GROUP="${SERVICE_GROUP:-$SERVICE_USER}"
TIMEZONE="${TIMEZONE:-Asia/Shanghai}"
GOTRACEBACK="${GOTRACEBACK:-crash}"
START_TIMEOUT="${START_TIMEOUT:-90}"
STOP_TIMEOUT="${STOP_TIMEOUT:-30}"
RESTART_SEC="${RESTART_SEC:-3}"
LOG_STDOUT_MODE="${LOG_STDOUT_MODE:-file}"
[ -n "$SVC_STATE" ] || SVC_STATE=restarted

# 值为空的口令文件不要 export（同上，会被当成要执行的脚本）
if [ -n "$ANSIBLE_BECOME_PASSWORD_FILE" ]; then
    [ -f "$ANSIBLE_BECOME_PASSWORD_FILE" ] \
        || die "sudo 口令文件不存在: $ANSIBLE_BECOME_PASSWORD_FILE"
    export ANSIBLE_BECOME_PASSWORD_FILE
else
    unset ANSIBLE_BECOME_PASSWORD_FILE
fi

# ---- 生成 playbook 变量 ----------------------------------------------------
# 参数写进一个 key=value 文件再交给 python，而不是用 argv / 环境变量传。
# 原因：Git Bash(MSYS) 会把「看起来像 POSIX 路径」的 argv 和环境变量悄悄转成
# Windows 路径 —— /home/fengyan/Server/centralService/bin 会被拼成
# D:/.../PortableGit/home/fengyan/...。install_root 是**远程机器上的路径**，
# 本机并不存在，一旦被转换就全错。写盘再传路径就没这个问题：
# MSYS 对「已存在的文件」做的是等价映射，内容不会被改。
# （另见 lib/gen_systemd_vars.py 的说明）
VARS_FILE="$(mktemp "${TMPDIR:-/tmp}/cs-systemd-vars.XXXXXX.json")"
PARAMS_FILE="$(mktemp "${TMPDIR:-/tmp}/cs-systemd-params.XXXXXX.conf")"
trap 'rm -f "$VARS_FILE" "$PARAMS_FILE"' EXIT

{
    printf 'only=%s\n'        "$ONLY"
    printf 'prefix=%s\n'      "$PREFIX"
    printf 'unit_prefix=%s\n' "$UNIT_PREFIX"
    printf 'user=%s\n'        "$SERVICE_USER"
    printf 'group=%s\n'       "$SERVICE_GROUP"
    printf 'timezone=%s\n'    "$TIMEZONE"
    printf 'gotraceback=%s\n' "$GOTRACEBACK"
    printf 'start_timeout=%s\n' "$START_TIMEOUT"
    printf 'stop_timeout=%s\n'  "$STOP_TIMEOUT"
    printf 'restart_sec=%s\n'   "$RESTART_SEC"
    printf 'log_mode=%s\n'      "$LOG_STDOUT_MODE"
    printf 'protect_home=%s\n'  "${SYSTEMD_PROTECT_HOME:-}"
    printf 'svc_state=%s\n'     "$SVC_STATE"
    printf 'enable=%s\n'        "$ENABLE"
    printf 'check_ports=%s\n'   "$CHECK_PORTS"
    printf 'port_timeout=%s\n'  "$PORT_TIMEOUT"
    printf 'ensure_user=%s\n'   "$ENSURE_USER"
    printf 'fix_owner=%s\n'     "$FIX_OWNER"
    printf 'backup=%s\n'        "$UNIT_BACKUP"
} > "$PARAMS_FILE"

# instances.conf 走 argv：它是本机真实文件，MSYS 的转换是等价映射
"$PYTHON" "$DEPLOY_DIR/lib/gen_systemd_vars.py" "$PARAMS_FILE" "$INSTANCES_FILE" > "$VARS_FILE" \
    || die "生成 playbook 变量失败（见上方输出）"
[ -s "$VARS_FILE" ] || die "生成 playbook 变量失败：输出为空"

# ---- 组装并执行 ------------------------------------------------------------
INV="$(_ansible_inventory)"
SSH_USER="$(_ansible_user_arg)"

PB_CMD=(ansible-playbook)
[ -n "$INV" ] && PB_CMD+=(-i "$INV")
[ -n "$SSH_USER" ] && PB_CMD+=(-u "$SSH_USER")
[ -n "$LIMIT_OPT" ] && PB_CMD+=(--limit "$LIMIT_OPT")
[ "$DO_CHECK" -eq 1 ] && PB_CMD+=(--check)
[ -n "$TAGS_OPT" ] && PB_CMD+=(--tags "$TAGS_OPT")
[ "$ANSIBLE_VERBOSE" = "1" ] && PB_CMD+=(-v)
PB_CMD+=("$PLAYBOOK" -e "@$VARS_FILE")

log_step "只装 systemd 单元"
log_info "playbook    : $PLAYBOOK"
log_info "目标        : $ANSIBLE_HOSTS${LIMIT_OPT:+ (limit: $LIMIT_OPT)}"
log_info "SSH 用户    : ${SSH_USER:-<inventory 或当前用户>}"
log_info "inventory   : ${INV:-（ansible 默认）}"
log_info "服务        : ${ONLY:-<全部 ${#INSTANCE_NAMES[@]} 个>}"
log_info "安装根目录  : $PREFIX"
log_info "运行用户    : $SERVICE_USER:$SERVICE_GROUP"
log_info "服务状态    : $SVC_STATE    开机自启: $ENABLE"
[ "$DO_CHECK" -eq 1 ] && log_warn "演练模式（--check），不会真正写入"
log_dim "等价命令： ${PB_CMD[*]}"

echo
"${PB_CMD[@]}"

echo
log_ok "systemd 单元安装完成"
cat <<EOF

  单元文件： /etc/systemd/system/$UNIT_PREFIX-<服务名>.service
  查看状态： systemctl status $UNIT_PREFIX-<服务名>
  看日志  ： sudo journalctl -u $UNIT_PREFIX-<服务名> -n 50 --no-pager
            tail -f $PREFIX/<服务名>/<服务名>.out.log
EOF
