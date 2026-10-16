#!/usr/bin/env bash
# ============================================================================
#  centralService 一键部署（systemd / Ansible）
#
#  流程（本地模式）：preflight → build → render → install → db-init → unit → start → verify
#  流程（Ansible 模式）：preflight → build → render → ansible_deploy → verify
#
#  Ansible 模式：开发机编译+渲染，通过 Ansible 推送到远程部署机执行。
#  适合"开发机 build → 部署机跑服务"的场景。
#
#  典型用法（Ansible 模式）：
#      cp deploy/deploy.env.example deploy/deploy.env        # 填好口令
#      cp deploy/overrides.conf.example deploy/overrides.conf
#      ./deploy/install.sh --ansible                         # 开发机打包+远程部署
#      ./deploy/install.sh --ansible --skip-build             # 只改配置并重启
#      ./deploy/install.sh --ansible --dry-run                # 先看看要做什么
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "$SCRIPT_DIR/lib/common.sh"
# shellcheck source=lib/ansible_helpers.sh
. "$SCRIPT_DIR/lib/ansible_helpers.sh"

# python3 输出中文，统一强制 UTF-8，避免在非 UTF-8 locale 下报错
export PYTHONIOENCODING=utf-8
export LC_ALL="${LC_ALL:-C.UTF-8}"

# 首次 SSH 连新机器时不弹 known_hosts 确认。
# 注意不能写成 `ansible ... -o StrictHostKeyChecking=no`：
# ad-hoc 的 -o 是 --one-line（不带参数），那串会被当成第二个 host pattern。
export ANSIBLE_HOST_KEY_CHECKING=False

# ============================================================================
#  参数
# ============================================================================
ENV_FILE="$DEPLOY_DIR/deploy.env"
OVERRIDES_FILE="$DEPLOY_DIR/overrides.conf"
INSTANCES_FILE="$DEPLOY_DIR/instances.conf"

# 下面两个在解析完参数、定位到仓库之后再定
REPO_ROOT_OPT=""
SRC_BIN_DIR=""
DIST_DIR=""

PREFIX=""
# 命令行显式指定的远程安装根目录。必须在 load_env_file 之后再套用，
# 否则会被 deploy.env 里的 ANSIBLE_REMOTE_PREFIX 覆盖掉。
REMOTE_PREFIX_OPT=""
DO_BUILD=1
DB_INIT=""
DO_START=1
DO_NGINX=0
DRY_RUN=0
STRICT_IPS=0
STRICT_FRESH=0

# Ansible 模式参数
DO_ANSIBLE=0
ANSIBLE_HOSTS="${ANSIBLE_HOSTS:-}"
ANSIBLE_USER="${ANSIBLE_USER:-}"
ANSIBLE_REMOTE_PREFIX="${ANSIBLE_REMOTE_PREFIX:-/home/fengyan/Server/centralService/bin}"
# Ansible inventory 文件。为空时：host pattern 是具体 IP/域名就用内联 inventory，
# 是组名（如 tmp）就交给 ansible 默认 inventory。
# 注意：绝不能把空字符串 export 出去 —— ansible 会把空 inventory 解析成当前目录，
# 然后把 CWD（deploy/）下每个文件都当 inventory 解析，刷出上百行 WARNING。
ANSIBLE_INVENTORY="${ANSIBLE_INVENTORY:-}"
INVENTORY_OPT=""
# 命令行显式 --ansible-user。只有它非空时才强制 -u，
# 否则让 inventory 里的 ansible_user 说了算。
ANSIBLE_USER_OPT=""
# sudo 口令文件（目标机的 sudo 需要密码时用）。不要用 -K 交互输入：
# 本脚本一轮要调几十次 ansible，-K 每次都会重新提示。
ANSIBLE_BECOME_PASSWORD_FILE="${ANSIBLE_BECOME_PASSWORD_FILE:-}"
ANSIBLE_BECOME="${ANSIBLE_BECOME:-yes}"
# 排障：ANSIBLE_VERBOSE=1 给每次 ansible 调用加 -v
ANSIBLE_VERBOSE="${ANSIBLE_VERBOSE:-0}"

usage() {
    cat <<'EOF'
用法: sudo ./deploy/install.sh [选项]

选项:
  -e, --env FILE          环境变量文件          (默认 deploy/deploy.env)
  -o, --overrides FILE    逐服务覆盖文件        (默认 deploy/overrides.conf)
  -i, --instances FILE    服务清单              (默认 deploy/instances.conf)
  -r, --repo-root DIR     仓库根目录            (默认自动探测，见下)
  -b, --bin-dir DIR       配置基线目录          (默认 <仓库>/bin)
  -d, --dist-dir DIR      二进制来源目录        (默认 <仓库>/dist，没有则退回 bin/)
  -p, --prefix DIR        安装根目录            (默认取 deploy.env 的 INSTALL_ROOT)
      --skip-build        跳过编译，直接用 --dist-dir 下已有的二进制
      --db-init / --no-db-init
                          是否执行各服务 up.sh 建库导表
                          (默认: 清单中 db_init=yes 的服务执行)
      --no-start          只安装不启动
      --install-nginx     额外部署 admin 的 nginx 反代到 /etc/nginx/conf.d
      --strict-ips        配置里仍有 192.168/10.x/172.16-31.x 地址时直接中止部署
      --strict-fresh      二进制比源码旧时直接中止部署
      --dry-run           只演练，不改动系统
  -h, --help              显示本帮助

Ansible 模式（开发机 → 部署机）:
      --ansible           启用 Ansible 部署模式（跳过本地 systemd，只做编译+渲染）
      --ansible-hosts HOSTS
                          Ansible 主机组或 host pattern（默认从 deploy.env 的 ANSIBLE_HOSTS 读取，
                          也没有时默认 tmp）
      --ansible-user USER SSH 连接用户（默认 fengyan）
      --ansible-inventory FILE
                          Ansible inventory 文件（默认 deploy/ansible/hosts，不存在则留空）
      --ansible-become-pass-file FILE
                          sudo 口令文件（目标机 sudo 需要密码时用，chmod 600）
      --no-become          不用 sudo（只用来确认 SSH 那一层是否通；
                            后续建用户/装 systemd 仍需 root，会失败）
      --ansible-verbose    给每次 ansible 调用加 -v（排障用）
      --remote-prefix DIR  远程安装根目录（默认 /home/fengyan/Server/centralService/bin）

仓库根目录怎么找（deploy/ 单独拷到别处时也能用）：
  1) --repo-root 显式指定
  2) 环境变量 CENTRAL_REPO_ROOT
  3) 从 deploy/ 往上找带 go.mod + src/ 的目录（标准布局）
  4) 常见位置 $HOME/Server/centralService 等

示例（本地直接部署到本机）：
  sudo ./deploy/install.sh --dry-run
  sudo ./deploy/install.sh
  sudo ./deploy/install.sh --skip-build --strict-ips --strict-fresh

示例（Ansible 模式：开发机 → 部署机）：
  ./deploy/install.sh --ansible --dry-run              # 先演练
  ./deploy/install.sh --ansible                         # 全新部署
  ./deploy/install.sh --ansible --skip-build            # 只改配置并重启服务
  ./deploy/install.sh --ansible -e /path/to/env --ansible-hosts "172.16.41.49"
EOF
}

while [ $# -gt 0 ]; do
    case "$1" in
        -e|--env)           ENV_FILE="$2"; shift 2 ;;
        -o|--overrides)     OVERRIDES_FILE="$2"; shift 2 ;;
        -i|--instances)     INSTANCES_FILE="$2"; shift 2 ;;
        -r|--repo-root)     REPO_ROOT_OPT="$2"; shift 2 ;;
        -b|--bin-dir)       SRC_BIN_DIR="$2"; shift 2 ;;
        -d|--dist-dir)      DIST_DIR="$2"; shift 2 ;;
        -p|--prefix)        PREFIX="$2"; shift 2 ;;
        --skip-build)       DO_BUILD=0; shift ;;
        --db-init)          DB_INIT=yes; shift ;;
        --no-db-init)       DB_INIT=no; shift ;;
        --no-start)          DO_START=0; shift ;;
        --install-nginx)    DO_NGINX=1; shift ;;
        --strict-ips)       STRICT_IPS=1; shift ;;
        --strict-fresh)     STRICT_FRESH=1; shift ;;
        --dry-run)          DRY_RUN=1; shift ;;
        --ansible)          DO_ANSIBLE=1; shift ;;
        --ansible-hosts)    ANSIBLE_HOSTS="$2"; shift 2 ;;
        --ansible-user)     ANSIBLE_USER="$2"; ANSIBLE_USER_OPT="$2"; shift 2 ;;
        --ansible-become-pass-file) ANSIBLE_BECOME_PASSWORD_FILE="$2"; shift 2 ;;
        --no-become)        ANSIBLE_BECOME=no; shift ;;
        --ansible-verbose)  ANSIBLE_VERBOSE=1; shift ;;
        --ansible-inventory) INVENTORY_OPT="$2"
                            ANSIBLE_INVENTORY="$2"; shift 2 ;;
        --remote-prefix)    REMOTE_PREFIX_OPT="$2"
                            ANSIBLE_REMOTE_PREFIX="$2"; shift 2 ;;
        -h|--help)          usage; exit 0 ;;
        *)                  die "未知参数: $1（用 --help 看用法）" ;;
    esac
done

# ============================================================================
#  步骤实现
# ============================================================================

step_preflight() {
    log_step "1/8 前置检查"

    if [ "$DO_ANSIBLE" -eq 1 ]; then
        # Ansible 模式：本地只检查工具链，远程 systemd 由 ansible 验证
        require_python
        require_cmd ansible
        require_cmd rsync

        set_repo_root "$REPO_ROOT_OPT"
        log_ok "ansible / rsync / $PYTHON 就绪"
        log_info "仓库根目录: $REPO_ROOT"
    else
        # 本地模式：需要完整 systemd 环境
        require_cmd systemctl install
        require_systemd
        require_python
        require_cmd go
        set_repo_root "$REPO_ROOT_OPT"
        log_ok "systemd / $PYTHON / go 就绪"
        log_info "仓库根目录: $REPO_ROOT"
    fi

    [ -n "$SRC_BIN_DIR" ] || SRC_BIN_DIR="$REPO_ROOT/bin"
    [ -n "$DIST_DIR" ] || DIST_DIR="$(resolve_dist_dir "$REPO_ROOT")"
    if [ "$DIST_DIR" = "$SRC_BIN_DIR" ] && [ ! -d "$REPO_ROOT/dist" ]; then
        log_warn "没有 $REPO_ROOT/dist，退回使用 $SRC_BIN_DIR 下的同名二进制。
       这些文件可能很旧，下面的新鲜度校验会逐个比对 src/ 的时间。"
    fi

    if [ -f "$ENV_FILE" ]; then
        load_env_file "$ENV_FILE"
    else
        die "找不到 $ENV_FILE
       先执行: cp $DEPLOY_DIR/deploy.env.example $ENV_FILE 并填入数据库口令"
    fi

    # Ansible 模式参数：从 env 文件继承未显式指定的值。
    # 命令行 --remote-prefix 优先级最高，load_env_file 之后要重新盖回去。
    if [ "$DO_ANSIBLE" -eq 1 ]; then
        # load_env_file 用的是 `set -a` + source，会把 deploy.env 里的变量全部 export，
        # **包括值为空的那些**。ansible 对 path 型配置（inventory / *_password_file /
        # private_key_file 等）拿到空串时会做 unfrackpath('')，结果就是当前目录，
        # 而目录算「可执行」—— 于是 ansible 把 deploy/ 当口令脚本去执行：
        #   ERROR! Problem occured when trying to run the password script
        #   /…/deploy ([Errno 13] Permission denied)
        # 跟 ANSIBLE_INVENTORY 是同一个坑。空的 ANSIBLE_* 一律 unset。
        local avar
        for avar in $(compgen -e | grep '^ANSIBLE_' || true); do
            if [ -z "${!avar:-}" ]; then
                unset "$avar"
            fi
        done

        # unset 之后变量就「不存在」了，脚本是 set -u，后面再 $ANSIBLE_XXX 会
        # 直接 "unbound variable"。所以凡后面还要引用的，都重新置成空值
        # （注意是赋空值，不是再 unset：赋空值不带 export 属性，不会重新踩坑）。
        : "${ANSIBLE_BECOME:=yes}"
        : "${ANSIBLE_VERBOSE:=0}"
        : "${ANSIBLE_INVENTORY:=}"
        : "${ANSIBLE_BECOME_PASSWORD_FILE:=}"

        : "${ANSIBLE_HOSTS:=${ANSIBLE_HOSTS:-tmp}}"
        : "${ANSIBLE_USER:=${ANSIBLE_USER:-fengyan}}"
        if [ -n "$REMOTE_PREFIX_OPT" ]; then
            ANSIBLE_REMOTE_PREFIX="$REMOTE_PREFIX_OPT"
        fi
        # inventory 同理：命令行 > deploy.env > 默认的 deploy/ansible/hosts
        if [ -n "$INVENTORY_OPT" ]; then
            ANSIBLE_INVENTORY="$INVENTORY_OPT"
        elif [ -z "$ANSIBLE_INVENTORY" ] && [ -f "$DEPLOY_DIR/ansible/hosts" ]; then
            ANSIBLE_INVENTORY="$DEPLOY_DIR/ansible/hosts"
        fi
        if [ -n "$ANSIBLE_INVENTORY" ] && [ ! -e "$ANSIBLE_INVENTORY" ]; then
            die "inventory 文件不存在: $ANSIBLE_INVENTORY"
        fi
        # 空值一律不 export：ANSIBLE_INVENTORY="" 会被 ansible 解析成当前目录，
        # 于是 deploy/ 下每个文件都被当成 inventory 去解析。
        export ANSIBLE_HOSTS ANSIBLE_USER ANSIBLE_REMOTE_PREFIX ANSIBLE_USER_OPT
        export ANSIBLE_BECOME ANSIBLE_VERBOSE
        if [ -n "$ANSIBLE_BECOME_PASSWORD_FILE" ]; then
            [ -f "$ANSIBLE_BECOME_PASSWORD_FILE" ] \
                || die "sudo 口令文件不存在: $ANSIBLE_BECOME_PASSWORD_FILE"
            local pmode
            pmode="$(stat -c '%a' "$ANSIBLE_BECOME_PASSWORD_FILE" 2>/dev/null || echo 644)"
            case "$pmode" in
                6[0-7][0-7]|4[0-7][0-7]) : ;;
                *) log_warn "$ANSIBLE_BECOME_PASSWORD_FILE 权限是 $pmode，含 sudo 口令，建议 chmod 600" ;;
            esac
            export ANSIBLE_BECOME_PASSWORD_FILE
        fi
        if [ -n "$ANSIBLE_INVENTORY" ]; then
            export ANSIBLE_INVENTORY
        else
            unset ANSIBLE_INVENTORY
        fi
    fi

    # 安装根目录。
    # Ansible 模式下 PREFIX 是「远程机器上」的路径，本机可能压根不存在
    # （/home/fengyan/... 属于另一个用户），拿它当本地目录建会直接 Permission denied。
    # 所以远程模式走 ANSIBLE_REMOTE_PREFIX，本地模式才走 INSTALL_ROOT。
    if [ -n "$PREFIX" ]; then
        :
    elif [ "$DO_ANSIBLE" -eq 1 ]; then
        PREFIX="${ANSIBLE_REMOTE_PREFIX:-${INSTALL_ROOT:-/home/fengyan/Server/centralService/bin}}"
    else
        PREFIX="${INSTALL_ROOT:-/home/fengyan/Server/centralService/bin}"
    fi
    UNIT_PREFIX="${UNIT_PREFIX:-centralsvc}"
    # 默认与部署账号一致：更新二进制、改配置、跑服务都是同一身份，
    # 不会出现「文件属主是 ANSIBLE_USER、服务以另一账号跑」导致的读不到配置。
    SERVICE_USER="${SERVICE_USER:-fengyan}"
    SERVICE_GROUP="${SERVICE_GROUP:-$SERVICE_USER}"
    TIMEZONE="${TIMEZONE:-Asia/Shanghai}"
    GOTRACEBACK="${GOTRACEBACK:-crash}"
    START_TIMEOUT="${START_TIMEOUT:-90}"
    STOP_TIMEOUT="${STOP_TIMEOUT:-30}"
    RESTART_SEC="${RESTART_SEC:-3}"
    LOG_IN_SERVICE_DIR="${LOG_IN_SERVICE_DIR:-1}"
    LOG_STDOUT_MODE="${LOG_STDOUT_MODE:-file}"
    LOG_ROTATE_KEEP="${LOG_ROTATE_KEEP:-7}"
    export PREFIX UNIT_PREFIX SERVICE_USER SERVICE_GROUP LOG_IN_SERVICE_DIR

    # deploy.env 必须以 root 可读、他人不可读的方式存放
    local mode
    mode="$(stat -c '%a' "$ENV_FILE" 2>/dev/null || echo 644)"
    case "$mode" in
        6[0-7][0-7]|4[0-7][0-7]|7[0-7][0-7]) : ;;
        *) log_warn "$ENV_FILE 权限是 $mode，含数据库口令，建议 chmod 600" ;;
    esac

    read_instances "$INSTANCES_FILE"
    log_ok "服务清单: ${#INSTANCE_NAMES[@]} 个（$(printf '%s ' "${INSTANCE_NAMES[@]}")）"
    log_info "安装根目录: $PREFIX    运行用户: $SERVICE_USER"

    if [ ! -d "$SRC_BIN_DIR" ]; then
        log_err "找不到配置基线目录: $SRC_BIN_DIR"
        cat >&2 <<EOF

  它应当包含各服务的 <服务名>.json、*.sql、up.sh，以及共享的 data/。
  查找过：
    --bin-dir 指定值 : ${SRC_BIN_DIR}
    仓库根目录      : $REPO_ROOT

  用 --bin-dir 或 -r 指定正确的位置，例如：
    sudo bash install.sh -r /home/fengyan/Server/centralService/bin --skip-build
EOF
        exit 1
    fi
    log_ok "配置基线: $SRC_BIN_DIR"

    if [ "$DB_INIT" = "yes" ]; then
        require_cmd mysql
        log_ok "mysql 客户端就绪（将执行建库导表）"
    fi

    if [ "$DO_ANSIBLE" -eq 0 ]; then
        # 本地模式：端口冲突检查
        local svc ports p busy=()
        for svc in "${INSTANCE_NAMES[@]}"; do
            if unit_is_active "$svc"; then
                continue
            fi
            ports="${INSTANCE_PORTS[$svc]}"
            for p in ${ports//,/ }; do
                [ -n "$p" ] || continue
                if port_in_use "$p"; then
                    busy+=("$svc:$p")
                fi
            done
        done
        if [ ${#busy[@]} -gt 0 ]; then
            log_warn "以下端口已被其它进程占用，部署前请先排查: ${busy[*]}"
        else
            log_ok "监听端口无冲突"
        fi
    fi

    # 目标机不编译时，装的是构建机传过来的二进制，必须先验一遍
    if [ "$DO_BUILD" -eq 0 ]; then
        step_verify_artifacts
    fi
}

# 校验待装二进制：是不是 Linux ELF、架构对不对、比源码新不新
step_verify_artifacts() {
    log_dim "校验交付二进制: $DIST_DIR"

    local extra=()
    if [ "$STRICT_FRESH" -eq 1 ]; then
        extra+=(--strict-fresh)
    fi

    if [ ! -f "$DEPLOY_DIR/lib/verify_artifact.py" ]; then
        log_dim "verify_artifact.py 不存在，跳过二进制校验"
        return 0
    fi

    "$PYTHON" "$DEPLOY_DIR/lib/verify_artifact.py" \
        --repo-root "$REPO_ROOT" \
        --dist-dir "$DIST_DIR" \
        --instances "$INSTANCES_FILE" \
        "${extra[@]+"${extra[@]}"}" \
        || die "二进制校验未通过（详见上方输出）
       目标机不编译时，二进制必须由构建机的 ./deploy/build_linux.sh 产出到 dist/。
       bin/ 下躺着的可能是几周前编译的旧文件，装上去不会有任何提示。"
}

step_build() {
    if [ "$DO_BUILD" -eq 0 ]; then
        log_step "2/8 编译（跳过，使用 $DIST_DIR 下已有二进制）"
        return 0
    fi
    log_step "2/8 编译 Linux 二进制"
    require_cmd go
    "$DEPLOY_DIR/build_linux.sh" --out-dir "$DIST_DIR"
    step_verify_artifacts
}

# 把「二进制 + 渲染好的配置 + SQL + up.sh + 共享 data」拼成一个完整的
# 安装目录镜像，供 Ansible 整体推送。
#
# render_config.py 只产出 *.json。如果 staging 里只有 JSON，
# ansible_push_staging 的 delete=yes 会把远程目录里的二进制、up.sh、SQL
# 当成「多余文件」删掉，服务随后必然起不来。
# 这里刻意与 install_service_files（本地模式）保持一致的目录布局，
# 两条部署路径的产物才不会分叉。
stage_service_files() {
    local svc="$1" src="$SRC_BIN_DIR/$1" dst="$STAGE/$1" f
    mkdir -p "$dst"

    # 二进制来自 dist/（构建产物），不是 bin/（配置与本地杂项的混合目录）
    [ -f "$DIST_DIR/$svc/$svc" ] || die "缺少可执行文件: $DIST_DIR/$svc/$svc"
    install -m 0755 "$DIST_DIR/$svc/$svc" "$dst/$svc"

    for f in "$src"/*.sql "$src"/*.pem "$src"/*.crt; do
        if [ -e "$f" ]; then install -m 0640 "$f" "$dst/"; fi
    done
    for f in "$src"/up.sh "$src"/down.sh "$src"/game.sh; do
        if [ -e "$f" ]; then install -m 0750 "$f" "$dst/"; fi
    done
    return 0
}

step_render() {
    log_step "3/8 渲染配置"

    if [ "$DO_ANSIBLE" -eq 1 ]; then
        # 远程模式：PREFIX 是远程机器上的路径，本地不要碰它，
        # staging 一律落在本机临时目录，再由 ansible synchronize 推上去。
        STAGE="$(mktemp -d "${TMPDIR:-/tmp}/centralService-staging.XXXXXX")"
    else
        # 本地模式：staging 放在安装根目录内，保证和最终位置同一文件系统，
        # 后面 cp -a 是同盘拷贝，不会因为跨 fs 半途失败留下残缺配置。
        mkdir -p "$PREFIX"
        STAGE="$PREFIX/.staging.$$"
    fi
    trap 'rm -rf "${STAGE:-}"' EXIT
    mkdir -p "$STAGE"
    log_dim "渲染暂存目录: $STAGE"

    local extra=()
    if [ -f "$OVERRIDES_FILE" ]; then
        extra+=(--overrides "$OVERRIDES_FILE")
    fi
    if [ "$STRICT_IPS" -eq 1 ]; then
        extra+=(--strict)
    fi

    "$PYTHON" "$DEPLOY_DIR/lib/render_config.py" \
        --src-dir "$SRC_BIN_DIR" \
        --out-dir "$STAGE" \
        --env "$ENV_FILE" \
        --instances "$INSTANCES_FILE" \
        "${extra[@]+"${extra[@]}"}" \
        || die "配置渲染失败或未通过 --strict-ips 检查（详见上方输出）"

    # 远程模式要把整个服务目录推上去，这里补齐二进制/SQL/脚本/共享数据
    if [ "$DO_ANSIBLE" -eq 1 ]; then
        local svc
        for svc in "${INSTANCE_NAMES[@]}"; do
            stage_service_files "$svc"
        done

        local datadir="$SRC_BIN_DIR/data"
        if [ -d "$datadir" ]; then
            mkdir -p "$STAGE/data"
            cp -a "$datadir/." "$STAGE/data/"
        else
            log_warn "缺少 $datadir，依赖 ../data 的服务会因读不到配置表而启动失败"
        fi
    fi

    log_ok "配置已渲染到 $STAGE"
}

# ============================================================================
#  本地模式步骤
# ============================================================================

install_service_files() {
    local svc="$1" src="$SRC_BIN_DIR/$svc" dst="$PREFIX/$svc" f
    [ -d "$src" ] || die "缺少服务配置目录: $src"
    mkdir -p "$dst"

    # 二进制来自 dist/（构建产物），不是 bin/（配置与本地杂项的混合目录）
    [ -f "$DIST_DIR/$svc/$svc" ] || die "缺少可执行文件: $DIST_DIR/$svc/$svc"
    install -m 0755 "$DIST_DIR/$svc/$svc" "$dst/$svc"

    # 渲染后的配置
    cp -a "$STAGE/$svc/." "$dst/"
    chmod 0640 "$dst"/*.json

    # 数据库初始化脚本与证书
    local f
    for f in "$src"/*.sql "$src"/*.pem "$src"/*.crt; do
        if [ -e "$f" ]; then install -m 0640 "$f" "$dst/"; fi
    done
    for f in "$src"/up.sh "$src"/down.sh "$src"/game.sh; do
        if [ -e "$f" ]; then install -m 0750 "$f" "$dst/"; fi
    done

    chown -R "$SERVICE_USER:$SERVICE_GROUP" "$dst"
    log_ok "已安装 $svc"
}

step_install() {
    log_step "4/8 安装文件"

    ensure_service_user "$SERVICE_USER" "$SERVICE_GROUP"
    mkdir -p "$PREFIX"

    local svc
    for svc in "${INSTANCE_NAMES[@]}"; do
        install_service_files "$svc"
    done

    # 共享数据目录：centralLogin / auction / orderService /
    # allianceService / leaseServer 以 ../data/ 相对路径读取
    local datadir="$SRC_BIN_DIR/data"
    if [ -d "$datadir" ]; then
        mkdir -p "$PREFIX/data"
        cp -a "$datadir/." "$PREFIX/data/"
        chown -R "$SERVICE_USER:$SERVICE_GROUP" "$PREFIX/data"
        log_ok "已安装共享数据目录 $PREFIX/data"
    else
        log_warn "缺少 $datadir，依赖 ../data 的服务会因读不到配置表而启动失败"
    fi

    log_ok "全部文件就位：$PREFIX"
}

step_db_init() {
    local run="$DB_INIT"
    if [ -z "$run" ]; then
        local has_yes=0 svc
        for svc in "${INSTANCE_NAMES[@]}"; do
            if [ "${INSTANCE_DB_INIT[$svc]}" = "yes" ]; then
                has_yes=1
                break
            fi
        done
        if [ "$has_yes" -eq 1 ]; then run=yes; else run=no; fi
    fi

    log_step "5/8 数据库初始化"
    if [ "$run" != "yes" ]; then
        log_dim "已跳过（--no-db-init 或清单中无 db_init=yes 的服务）"
        return 0
    fi

    require_cmd mysql
    local svc up failed=()
    for svc in "${INSTANCE_NAMES[@]}"; do
        [ "${INSTANCE_DB_INIT[$svc]}" = "yes" ] || continue
        up="$PREFIX/$svc/up.sh"
        if [ ! -f "$up" ]; then
            log_warn "$svc 没有 up.sh，跳过"
            continue
        fi
        log_info "$svc -> 建库并导入表结构"
        if ! ( cd "$PREFIX/$svc" && sh ./up.sh ); then
            failed+=("$svc")
        fi
    done

    if [ ${#failed[@]} -gt 0 ]; then
        log_warn "以下服务建库/导表返回失败（表已存在时属正常，请人工确认）: ${failed[*]}"
    else
        log_ok "数据库初始化完成"
    fi
}

step_units() {
    log_step "6/8 安装 systemd 单元"

    local tpl="$DEPLOY_DIR/templates/centralsvc.service.template"
    [ -f "$tpl" ] || die "单元模板不存在: $tpl"

    UNIT_DIR="/etc/systemd/system"
    mkdir -p "$UNIT_DIR"

    local svc out
    for svc in "${INSTANCE_NAMES[@]}"; do
        tpl_clear
        tpl_set SERVICE       "$svc"
        tpl_set DESCRIPTION   "${INSTANCE_DESC[$svc]:-$svc}"
        tpl_set INSTALL_ROOT  "$PREFIX"
        tpl_set SERVICE_USER  "$SERVICE_USER"
        tpl_set SERVICE_GROUP "$SERVICE_GROUP"
        tpl_set TIMEZONE      "$TIMEZONE"
        tpl_set GOTRACEBACK   "$GOTRACEBACK"
        tpl_set START_TIMEOUT "$START_TIMEOUT"
        tpl_set STOP_TIMEOUT  "$STOP_TIMEOUT"
        tpl_set RESTART_SEC   "$RESTART_SEC"
        tpl_set PROTECT_HOME  "$(protect_home_value)"
        tpl_set STDOUT_TARGET "$(stdout_target "$svc")"
        tpl_set STDERR_TARGET "$(stdout_target "$svc")"

        out="$UNIT_DIR/$(unit_name "$svc")"
        render_template "$tpl" "$out"
        tpl_assert_no_leftover "$out"
        chmod 0644 "$out"
    done

    log_info "ProtectHome=$(protect_home_value)（安装根目录 $PREFIX 在受保护路径下时自动关闭）"
    systemctl daemon-reload
    log_ok "已生成 ${#INSTANCE_NAMES[@]} 个单元（$(printf '%s ' "${INSTANCE_NAMES[@]}")）"
}

# 日志全落在服务目录里，不轮转会撑爆磁盘：
#   <服务名>.log      lumberjack 按大小轮转，但默认不限制备份份数和天数
#   <服务名>.out.log  systemd 一直持有 fd，重启也不清空（用的 append:）
step_logrotate() {
    local tpl="$DEPLOY_DIR/templates/logrotate.conf.template"
    [ -f "$tpl" ] || { log_warn "没有 logrotate 模板，跳过"; return 0; }
    log_step "配置日志轮转"

    tpl_clear
    tpl_set INSTALL_ROOT    "$PREFIX"
    tpl_set SERVICE_USER    "$SERVICE_USER"
    tpl_set SERVICE_GROUP   "$SERVICE_GROUP"
    tpl_set LOG_ROTATE_KEEP "$LOG_ROTATE_KEEP"

    local out="/etc/logrotate.d/centralsvc"
    mkdir -p /etc/logrotate.d
    render_template "$tpl" "$out"
    tpl_assert_no_leftover "$out"
    chmod 0644 "$out"
    log_ok "logrotate 配置已生成: $out（保留 $LOG_ROTATE_KEEP 份）"
}

step_nginx() {
    local tpl="$DEPLOY_DIR/templates/nginx-admin.conf.template"
    [ -f "$tpl" ] || { log_warn "没有 nginx 模板，跳过"; return 0; }

    local ports gmt_port http_port sdk_port
    ports="$("$PYTHON" - "$STAGE/admin/admin.json" <<'PY'
import json, sys
cfg = json.load(open(sys.argv[1], encoding="utf-8"))
def port(key, default):
    val = cfg.get(key, "")
    return val.rsplit(":", 1)[-1] if ":" in str(val) else default
print(port("addressForGMT", "2050"),
      port("httpAPIAddress", "8080"),
      port("httpSDKAddress", "8081"))
PY
)" || die "读取 admin.json 端口失败"
    read -r gmt_port http_port sdk_port <<< "$ports"

    tpl_clear
    tpl_set ADMIN_HOSTNAME "${ADMIN_HOSTNAME:-localhost}"
    tpl_set ADMIN_GMT_PORT "$gmt_port"
    tpl_set ADMIN_HTTP_PORT "$http_port"
    tpl_set ADMIN_SDK_PORT "$sdk_port"
    tpl_set SSL_CERT "${SSL_CERT:-/etc/letsencrypt/live/localhost/fullchain.pem}"
    tpl_set SSL_KEY  "${SSL_KEY:-/etc/letsencrypt/live/localhost/privkey.pem}"

    local out="/etc/nginx/conf.d/centralsvc-admin.conf"
    render_template "$tpl" "$out"
    tpl_assert_no_leftover "$out"
    log_ok "nginx 配置已生成: $out"
    log_dim "生成的是 http/https server 块，请按需挂到主配置并 reload"
}

step_start() {
    if [ "$DO_START" -eq 0 ]; then
        log_step "7/8 启动服务（--no-start 已跳过）"
        return 0
    fi

    log_step "7/8 启动服务"

    local svc unit failed=()
    for svc in "${INSTANCE_NAMES[@]}"; do
        unit="$(unit_name "$svc")"
        log_info "启动 $svc ..."
        systemctl enable "$unit" >/dev/null 2>&1 || log_warn "$unit 开机自启设置失败"
        if systemctl restart "$unit"; then
            :
        else
            failed+=("$svc")
            log_err "$svc 启动失败"
            # 203/EXEC 这类是「进程没起来」，日志里什么都不会有，
            # 必须先说清楚是哪一类失败，否则会被当成崩溃一直查错方向。
            explain_unit_failure "$svc"
            # stdout/stderr 默认不进 journald，先看服务目录里的 out.log
            local out_log="$PREFIX/$svc/$svc.out.log"
            if [ -f "$out_log" ]; then
                log_dim "---- 尾部 $out_log ----"
                tail -n 20 "$out_log" 2>/dev/null | sed 's/^/        /' >&2 || true
            else
                journalctl -u "$unit" -n 20 --no-pager 2>/dev/null \
                    | sed 's/^/        /' >&2 || true
            fi
        fi
    done

    if [ ${#failed[@]} -gt 0 ]; then
        local first="${failed[0]}"
        die "以下服务启动失败: ${failed[*]}
       排查（日志都在服务目录里）:
         tail -f $PREFIX/$first/$first.out.log     # 进程的 stdout/stderr
         tail -f $PREFIX/$first/$first.log         # 业务日志
       配置错误最常见的原因是 <服务名>.json 没放在 /同服务名/ 目录下"
    fi
    log_ok "全部服务已启动"
}

step_verify() {
    if [ "$DO_START" -eq 0 ]; then
        return 0
    fi
    log_step "部署校验"
    "$DEPLOY_DIR/healthcheck.sh" --env "$ENV_FILE" --instances "$INSTANCES_FILE" \
        || log_warn "健康检查未全绿，请查看上面的明细"
}

# ============================================================================
#  Ansible 模式步骤
# ============================================================================

step_ansible_deploy() {
    log_step "Ansible 远程部署"

    # 前置：确认能连通远程
    ansible_check

    # 1. 远程创建用户/用户组
    ansible_ensure_user "$SERVICE_USER" "$SERVICE_GROUP" "$PREFIX"

    # 2. 远程创建安装根目录
    ansible_mkdir "$PREFIX" "$SERVICE_USER" "$SERVICE_GROUP"

    # 3. 同步整个服务目录（staging 是「最终安装目录」的完整镜像：
    #    二进制 + 渲染好的 *.json + *.sql + up.sh + data/）。
    #    不再单独推二进制：那会在 push_staging 之前落一份，
    #    紧接着被 delete=yes 判定为多余文件而删掉，等于白推一趟。
    ansible_push_staging "$STAGE" "$PREFIX"

    # 4. synchronize 推上去的文件属主是 ANSIBLE_USER，
    #    而进程以 SERVICE_USER 运行；配置是 0600，属主不对就读不到。
    ansible_chown "$PREFIX" "$SERVICE_USER" "$SERVICE_GROUP"

    # 5. 生成并推送 systemd 单元
    local tmp_unit_dir
    tmp_unit_dir="$(mktemp -d)"
    # 注意带上 STAGE：trap 是覆盖式的，这里只写 tmp_unit_dir 会把
    # step_render 注册的 staging 清理动作顶掉，留下一个临时目录。
    trap "rm -rf '${tmp_unit_dir}' '${STAGE:-}'" EXIT

    local tpl="$DEPLOY_DIR/templates/centralsvc.service.template"
    local svc out
    for svc in "${INSTANCE_NAMES[@]}"; do
        tpl_clear
        tpl_set SERVICE       "$svc"
        tpl_set DESCRIPTION   "${INSTANCE_DESC[$svc]:-$svc}"
        tpl_set INSTALL_ROOT  "$PREFIX"
        tpl_set SERVICE_USER  "$SERVICE_USER"
        tpl_set SERVICE_GROUP "$SERVICE_GROUP"
        tpl_set TIMEZONE      "$TIMEZONE"
        tpl_set GOTRACEBACK   "$GOTRACEBACK"
        tpl_set START_TIMEOUT "$START_TIMEOUT"
        tpl_set STOP_TIMEOUT  "$STOP_TIMEOUT"
        tpl_set RESTART_SEC   "$RESTART_SEC"
        tpl_set PROTECT_HOME  "$(protect_home_value)"
        tpl_set STDOUT_TARGET "$(stdout_target "$svc")"
        tpl_set STDERR_TARGET "$(stdout_target "$svc")"

        out="$tmp_unit_dir/$(unit_name "$svc")"
        render_template "$tpl" "$out"
        tpl_assert_no_leftover "$out"
        chmod 0644 "$out"
    done
    log_info "ProtectHome=$(protect_home_value)（安装根目录 $PREFIX 在受保护路径下时自动关闭）"
    log_ok "本地生成 ${#INSTANCE_NAMES[@]} 个 systemd 单元"

    ansible_push_units "$tmp_unit_dir"

    # 5b. 日志轮转。日志全落在服务目录里，lumberjack 默认不限制备份份数，
    #     systemd 也一直持有 out.log 的 fd，不轮转会撑爆磁盘。
    local tpl_lr="$DEPLOY_DIR/templates/logrotate.conf.template"
    if [ -f "$tpl_lr" ]; then
        log_step "推送日志轮转配置"
        local lr_out="$tmp_unit_dir/centralsvc-logrotate"
        tpl_clear
        tpl_set INSTALL_ROOT    "$PREFIX"
        tpl_set SERVICE_USER    "$SERVICE_USER"
        tpl_set SERVICE_GROUP   "$SERVICE_GROUP"
        tpl_set LOG_ROTATE_KEEP "$LOG_ROTATE_KEEP"
        render_template "$tpl_lr" "$lr_out"
        tpl_assert_no_leftover "$lr_out"
        chmod 0644 "$lr_out"
        ansible_copy_file "$lr_out" "/etc/logrotate.d/centralsvc" 0644
        log_ok "logrotate 配置已推送（保留 $LOG_ROTATE_KEEP 份）"
    fi

    # 6. 数据库初始化
    local run="$DB_INIT"
    if [ -z "$run" ]; then
        local has_yes=0 svc2
        for svc2 in "${INSTANCE_NAMES[@]}"; do
            if [ "${INSTANCE_DB_INIT[$svc2]}" = "yes" ]; then
                has_yes=1
                break
            fi
        done
        if [ "$has_yes" -eq 1 ]; then run=yes; else run=no; fi
    fi

    if [ "$run" = "yes" ]; then
        log_step "远程数据库初始化"
        local svc2 up failed=()
        for svc2 in "${INSTANCE_NAMES[@]}"; do
            [ "${INSTANCE_DB_INIT[$svc2]}" = "yes" ] || continue
            up="$PREFIX/$svc2/up.sh"
            # 检查远程是否有 up.sh
            if ! _ansible -m shell -a "test -f $up" >/dev/null 2>&1; then
                log_warn "$svc2 没有 up.sh，跳过"
                continue
            fi
            log_info "$svc2 -> 建库并导入表结构"
            if ! ansible_db_init "$svc2" "$PREFIX"; then
                failed+=("$svc2")
            fi
        done
        if [ ${#failed[@]} -gt 0 ]; then
            log_warn "以下服务建库/导表返回失败: ${failed[*]}"
        else
            log_ok "数据库初始化完成"
        fi
    fi

    # 7. 启动服务
    if [ "$DO_START" -eq 1 ]; then
        log_step "远程启动服务"
        local svc3 failed=()
        for svc3 in "${INSTANCE_NAMES[@]}"; do
            if ! ansible_service_restart "$svc3"; then
                failed+=("$svc3")
            fi
        done
        if [ ${#failed[@]} -gt 0 ]; then
            log_warn "以下服务启动失败: ${failed[*]}"
        else
            log_ok "全部服务已启动"
        fi
    else
        log_step "启动服务（--no-start 已跳过）"
    fi

    # 8. 健康检查（本地调用远程 healthcheck.sh）
    if [ "$DO_START" -eq 1 ]; then
        log_step "远程健康检查"
        # 把 deploy/ 同步到远程（healthcheck.sh 需要用到）
        local remote_deploy_dir="/home/$ANSIBLE_USER/deploy"
        log_info "同步 deploy/ 到远程 $remote_deploy_dir"
        _ansible -m synchronize -a \
            "src=$DEPLOY_DIR/ dest=$remote_deploy_dir/ delete=no recursive=yes times=yes"

        # 注意两点：
        #  1) 必须用远程的 deploy.env 路径。$ENV_FILE 是本机路径
        #     （如 /mnt/hgfs/.../deploy/deploy.env），远程根本不存在，
        #     healthcheck.sh 会直接以「找不到环境文件」退出。
        #  2) 用 shell 模块而不是 script 模块：script 的第一个参数是本机脚本路径，
        #     把 "cd ... && bash ..." 整串喂给它会被当成文件名。
        _ansible -m shell -a \
            "cd $remote_deploy_dir && bash healthcheck.sh \
             --env $remote_deploy_dir/deploy.env \
             --instances $remote_deploy_dir/instances.conf" \
            2>&1 | while IFS= read -r line; do
                log_dim "  $line"
            done
    fi

    log_ok "Ansible 远程部署完成"
}

# ============================================================================
#  主流程
# ============================================================================
main() {
    # Ansible 模式不需要 root（SSH 走密钥，远程操作靠 sudo）
    # 本地模式需要 root
    if [ "$DO_ANSIBLE" -eq 0 ]; then
        require_root "$@"
    fi

    step_preflight

    if [ "$DRY_RUN" -eq 1 ]; then
        log_step "[dry-run] 演练模式，不改动系统"

        if [ "$DO_ANSIBLE" -eq 1 ]; then
            # Ansible 模式演练：检查连接 + 渲染配置
            log_info "Ansible 主机组: $ANSIBLE_HOSTS"
            log_info "远程用户    : ${ANSIBLE_USER_OPT:-$ANSIBLE_USER（inventory 里另有 ansible_user 时以它为准）}"
            log_info "inventory   : ${ANSIBLE_INVENTORY:-（未指定，host pattern 是具体主机时用内联 inventory）}"
            log_info "远程安装路径: $PREFIX"
            log_info "本地仓库    : $REPO_ROOT"
            log_info "二进制目录  : $DIST_DIR"
            log_info "配置基线    : $SRC_BIN_DIR"

            # 直接复用 ansible_check，别在演练里另写一套连接检查：
            # 参数（inventory / -u / become）稍有出入，演练通过而实际部署失败。
            # 它内部是只读的 ping，演练跑它不会改动远程机器。
            ansible_check

            DO_BUILD=0
            step_build
            if [ -d "$DIST_DIR" ]; then
                "$PYTHON" "$DEPLOY_DIR/lib/verify_artifact.py" \
                    --repo-root "$REPO_ROOT" --dist-dir "$DIST_DIR" \
                    --instances "$INSTANCES_FILE" \
                    --skip-elf --skip-arch \
                    2>&1 | head -5 || true
            fi

            STAGE="/tmp/centralService-dryrun.$$"
            mkdir -p "$STAGE"
            trap "rm -rf '$STAGE'" EXIT
            local extra=()
            if [ -f "$OVERRIDES_FILE" ]; then
                extra+=(--overrides "$OVERRIDES_FILE")
            fi
            log_step "配置渲染演练"
            "$PYTHON" "$DEPLOY_DIR/lib/render_config.py" \
                --src-dir "$SRC_BIN_DIR" --out-dir "$STAGE" \
                --env "$ENV_FILE" --instances "$INSTANCES_FILE" \
                "${extra[@]+"${extra[@]}"}" || true

            log_step "将要执行的变更（Ansible 模式）"
            log_info "远程用户      : $ANSIBLE_USER@$ANSIBLE_HOSTS"
            log_info "远程安装路径  : $PREFIX"
            log_info "运行用户      : $SERVICE_USER:$SERVICE_GROUP"
            log_info "远程操作      : useradd / systemctl / file sync"
            log_info "二进制来源    : $DIST_DIR"
            local s dbs=""
            for s in "${INSTANCE_NAMES[@]}"; do
                if [ "${INSTANCE_DB_INIT[$s]}" = yes ]; then
                    dbs="$dbs $s"
                fi
            done
            if [ "$DB_INIT" != "no" ] && [ -n "$dbs" ]; then
                log_info "建库导表      :$dbs"
            fi
            log_ok "演练完成，去掉 --dry-run 即可真正部署"
        else
            # 本地模式演练
            DO_BUILD=0
            step_build
            if [ -d "$DIST_DIR" ]; then
                "$PYTHON" "$DEPLOY_DIR/lib/verify_artifact.py" \
                    --repo-root "$REPO_ROOT" --dist-dir "$DIST_DIR" \
                    --instances "$INSTANCES_FILE" || \
                    log_warn "二进制未就绪，去掉 --dry-run 前请先在构建机跑 ./deploy/build_linux.sh"
            else
                log_warn "没有 $DIST_DIR：目标机不编译时必须先由构建机产出二进制"
            fi
            STAGE="/tmp/centralService-dryrun.$$"
            mkdir -p "$STAGE"
            trap "rm -rf '$STAGE'" EXIT
            local extra=()
            if [ -f "$OVERRIDES_FILE" ]; then
                extra+=(--overrides "$OVERRIDES_FILE")
            fi
            log_step "配置渲染演练"
            "$PYTHON" "$DEPLOY_DIR/lib/render_config.py" \
                --src-dir "$SRC_BIN_DIR" --out-dir "$STAGE" \
                --env "$ENV_FILE" --instances "$INSTANCES_FILE" \
                "${extra[@]+"${extra[@]}"}" || true
            log_step "将要执行的变更"
            log_info "创建用户      : $SERVICE_USER:$SERVICE_GROUP"
            log_info "安装目录      : $PREFIX/<服务名>/{二进制,配置,SQL}"
            log_info "二进制来源    : $DIST_DIR"
            log_info "共享数据      : $PREFIX/data"
            log_info "systemd 单元  : /etc/systemd/system/$UNIT_PREFIX-<服务名>.service"
            local s
            local dbs=""
            for s in "${INSTANCE_NAMES[@]}"; do
                if [ "${INSTANCE_DB_INIT[$s]}" = yes ]; then
                    dbs="$dbs $s"
                fi
            done
            if [ "$DB_INIT" != "no" ] && [ -n "$dbs" ]; then
                log_info "建库导表      :$dbs"
            fi
            log_ok "演练完成，去掉 --dry-run 即可真正部署"
        fi
        return 0
    fi

    # 实际部署
    step_build
    step_render

    if [ "$DO_ANSIBLE" -eq 1 ]; then
        step_ansible_deploy
    else
        step_install
        step_db_init
        step_units
        step_logrotate
        if [ "$DO_NGINX" -eq 1 ]; then
            step_nginx
        fi
        step_start
    fi

    step_verify

    echo
    if [ "$DO_ANSIBLE" -eq 1 ]; then
        log_ok "部署完成（Ansible 模式）"
        cat <<EOF

  常用运维命令（Ansible 模式）：
    ansible $ANSIBLE_HOSTS -b -m systemd -a "name=$UNIT_PREFIX-<服务名> state=restarted"
                                              # 重启远程服务
    ansible $ANSIBLE_HOSTS -b -m shell -a "tail -n 50 $PREFIX/<服务名>/<服务名>.out.log"
                                              # 看远程进程 stdout/stderr
    ./deploy/upgrade.sh --ansible             # 升级（自动回滚）
    ./deploy/uninstall.sh --ansible            # 卸载

  日志都在服务自己的目录里：
    $PREFIX/<服务名>/<服务名>.log       业务日志（lumberjack 按大小轮转）
    $PREFIX/<服务名>/<服务名>.out.log   进程 stdout/stderr
    logrotate 配置在 /etc/logrotate.d/centralsvc

EOF
    else
        log_ok "部署完成"
        cat <<EOF

  常用运维命令：
    systemctl status $UNIT_PREFIX-<服务名>      查看状态
    ./deploy/healthcheck.sh                     全量健康检查
    ./deploy/upgrade.sh                         升级（自动回滚）
    ./deploy/uninstall.sh                       卸载

  日志都在服务自己的目录里：
    $PREFIX/<服务名>/<服务名>.log       业务日志（lumberjack 按大小轮转）
    $PREFIX/<服务名>/<服务名>.out.log   进程 stdout/stderr
    logrotate 配置在 /etc/logrotate.d/centralsvc

EOF
    fi
}

main "$@"
