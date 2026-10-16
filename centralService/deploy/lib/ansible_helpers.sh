#!/usr/bin/env bash
# ============================================================================
#  centralService Ansible 远程操作辅助库
#
#  被 install.sh / upgrade.sh / uninstall.sh 通过 source 引入。
#  本文件只定义函数，不执行任何动作。
# ============================================================================

# ----------------------------------------------------------------------------
#  Ansible 连接参数（由调用方在调用前设置）
# ----------------------------------------------------------------------------
# ANSIBLE_HOSTS      : Ansible 主机组或 host pattern（默认 "tmp"）
# ANSIBLE_USER       : 远程 SSH 用户（默认 fengyan）
# ANSIBLE_BECOME     : 是否使用 sudo（默认 yes）
# ANSIBLE_INVENTORY  : inventory 文件路径；为空时按下面的规则自动判定

_ansible_defaults() {
    : "${ANSIBLE_HOSTS:=tmp}"
    : "${ANSIBLE_USER:=fengyan}"
    : "${ANSIBLE_BECOME:=yes}"
    : "${ANSIBLE_INVENTORY:=}"
    # 只有命令行显式 --ansible-user 才强制覆盖 inventory 里的 ansible_user
    : "${ANSIBLE_USER_OPT:=}"
    : "${ANSIBLE_BECOME_PASSWORD_FILE:=}"
}

# ----------------------------------------------------------------------------
#  inventory 解析
# ----------------------------------------------------------------------------
# Ansible ad-hoc 的 host pattern 必须能在 inventory 里解析出主机，
# 直接写 IP 也会报 "Could not match supplied host pattern"。
# 所以：
#   1) 显式给了 ANSIBLE_INVENTORY 就用它
#   2) ANSIBLE_HOSTS 看起来是一台具体主机（纯 IP 或带点的域名）时，
#      用 "<主机>," 这种内联 inventory 兜底 —— 末尾逗号是必须的，
#      否则 ansible 会把它当文件名。
#   3) 其余情况（组名如 tmp）交给 ansible 默认 inventory，由 ansible_check 报错
_ansible_inventory() {
    if [ -n "${ANSIBLE_INVENTORY:-}" ]; then
        printf '%s' "$ANSIBLE_INVENTORY"
        return 0
    fi
    if printf '%s' "$ANSIBLE_HOSTS" | grep -qE \
        '^[0-9]{1,3}(\.[0-9]{1,3}){3}$|^[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$'; then
        printf '%s,' "$ANSIBLE_HOSTS"
    fi
    return 0
}

# ----------------------------------------------------------------------------
#  内部：拼装 ansible 命令行
# ----------------------------------------------------------------------------
# 四个坑，都踩过：
#   1) ad-hoc 的 -o 是 --one-line（不带参数）。写 `-o StrictHostKeyChecking=no`
#      时那串会变成第二个 host pattern，报 "Could not match supplied host pattern"。
#      SSH 参数不能从这里传，改由 install.sh 导出 ANSIBLE_HOST_KEY_CHECKING=False。
#   2) -b/--become 是开关，不接受参数。写 `--become=yes` 会直接报
#      "argument -b/--become: ignored explicit argument 'yes'" 然后退出，
#      跟连不连通一点关系都没有 —— 所以只能按布尔值决定加不加这个 flag。
#   3) 不能无条件 -u $ANSIBLE_USER。inventory 里常常已经写了 ansible_user=xxx，
#      命令行 -u 的优先级高于它，盲目覆盖会以错误的用户连过去，
#      表现正是 "Permission denied (publickey,password)"。
#      所以：只有 inventory 没声明 ansible_user 时才用 ANSIBLE_USER 兜底，
#      命令行 --ansible-user 则始终最高优先级。
#   4) ANSIBLE_INVENTORY 为空时不要 export。空字符串会被 abspath 解析成当前目录，
#      ansible 于是把 CWD（也就是 deploy/）当 inventory 目录，
#      把里面每个 .sh/.py/.conf 都试着当 inventory 解析，刷出上百行 WARNING。
# 结果缓存：ansible-inventory --list 要解析整个 inventory，
# 而每次 _ansible_cmd 都会调一次，一轮部署几十次调用不能每次都重跑。
_ANSIBLE_USER_CACHE=""
_ANSIBLE_USER_CACHE_SET=0

_ansible_user_arg() {
    if [ -n "${ANSIBLE_USER_OPT:-}" ]; then
        printf '%s' "$ANSIBLE_USER_OPT"
        return 0
    fi
    if [ "$_ANSIBLE_USER_CACHE_SET" -eq 1 ]; then
        printf '%s' "$_ANSIBLE_USER_CACHE"
        return 0
    fi

    local inv resolved=""
    local -a inv_args=()
    inv="$(_ansible_inventory)"
    [ -n "$inv" ] && inv_args=(-i "$inv")
    if ! ansible-inventory --list "${inv_args[@]}" 2>/dev/null \
            | grep -q '"ansible_user"'; then
        # inventory 没声明 ansible_user，才用配置里的 ANSIBLE_USER 兜底
        resolved="$ANSIBLE_USER"
    fi

    _ANSIBLE_USER_CACHE="$resolved"
    _ANSIBLE_USER_CACHE_SET=1
    printf '%s' "$resolved"
}

_ansible_cmd() {
    _ansible_defaults
    ANSIBLE_CMD=(ansible "$ANSIBLE_HOSTS")
    local inv ssh_user
    inv="$(_ansible_inventory)"
    if [ -n "$inv" ]; then
        ANSIBLE_CMD+=(-i "$inv")
    fi
    ssh_user="$(_ansible_user_arg)"
    if [ -n "$ssh_user" ]; then
        ANSIBLE_CMD+=(-u "$ssh_user")
    fi
    if [ "${_ANSIBLE_NO_BECOME:-0}" -eq 1 ]; then
        :   # 只探测 SSH/python 这一层，不提权（ansible_check 的第一级探测用）
    else
    case "${ANSIBLE_BECOME}" in
        1|y|Y|yes|YES|Yes|true|TRUE|True|on|ON)
            ANSIBLE_CMD+=(--become --become-user=root --become-method=sudo)
            # sudo 要密码时用口令文件。不能用 -K：本脚本一轮要调几十次 ansible，
            # -K 每次都会重新提示，根本没法用。
            if [ -n "${ANSIBLE_BECOME_PASSWORD_FILE:-}" ]; then
                ANSIBLE_CMD+=(--become-password-file "$ANSIBLE_BECOME_PASSWORD_FILE")
            fi
            ;;
        0|n|N|no|NO|No|false|FALSE|False|off|OFF|"")
            : ;;
        *)
            die "ANSIBLE_BECOME 只能是 yes/no（当前: $ANSIBLE_BECOME）" ;;
    esac
    fi
    # 排障用：ANSIBLE_VERBOSE=1 时给每次调用加 -v
    if [ "${ANSIBLE_VERBOSE:-0}" = "1" ]; then
        ANSIBLE_CMD+=(-v)
    fi
}

# 打印当前拼出来的完整命令行，供用户手工复现（带必要引号）
# 用法：_ansible_cmdline [-m ping]  —— 带上你这次实际传给 ansible 的参数，
# 否则打出来的是一条不完整的命令，粘到终端复现不出同样的问题。
_ansible_cmdline() {
    _ansible_cmd
    local out="" arg
    for arg in "${ANSIBLE_CMD[@]}" "$@"; do
        case "$arg" in
            ""|*[" 	"]*) out="$out '$arg'" ;;
            *)             out="$out $arg" ;;
        esac
    done
    printf '%s' "${out# }"
}

# 单次 ansible 调用：打印并执行
_ansible() {
    _ansible_cmd
    log_info "ansible $ANSIBLE_HOSTS $*"
    "${ANSIBLE_CMD[@]}" "$@"
}

# 同上，但把输出缩进后打到日志里（不看返回码）
_ansible_ok() {
    _ansible_cmd
    log_info "ansible $ANSIBLE_HOSTS $*"
    "${ANSIBLE_CMD[@]}" "$@" 2>&1 | while IFS= read -r line; do
        log_dim "  $line"
    done
}

# 同上，但不打日志、不吞输出，供调用方捕获原始结果做判断
_ansible_capture() {
    _ansible_cmd
    "${ANSIBLE_CMD[@]}" "$@" 2>&1
}

# 同上，但这次调用不提权（--become 全去掉），用来区分「连不上」和「sudo 不行」
_ansible_capture_nobecome() {
    _ANSIBLE_NO_BECOME=1
    _ansible_cmd
    _ANSIBLE_NO_BECOME=0
    "${ANSIBLE_CMD[@]}" "$@" 2>&1
}

# ----------------------------------------------------------------------------
#  内部：把 ansible 原始输出裁成能看的样子
# ----------------------------------------------------------------------------
# 三类噪音要处理，但一条都不能误删真实错误：
#   a) ansible 把某个目录当 inventory 时，对每个文件刷 "Failed to parse ..." WARNING
#   b) 参数错误时几十行 usage
#   c) 输出为空 —— 以前这里用 sed -n '1,/^usage: /p' | sed '$d'，
#      没有 usage 时第一段会一路打到文件尾，紧跟着的 sed '$d' 就把最后一行给删了；
#      只剩一行的输出（比如单行 FAILED/单行 WARNING）会被删成空，
#      于是屏幕上啥也看不到。现在只在真出现 usage 时才截断。
_ansible_dump_raw() {
    local out="$1" filtered
    filtered="$(printf '%s\n' "$out" \
        | grep -v 'Failed to parse .* with \(script\|ini\) plugin' \
        | grep -v 'Unable to parse .* as an inventory source' \
        || true)"
    if printf '%s\n' "$filtered" | grep -q '^usage: '; then
        filtered="$(printf '%s\n' "$filtered" | awk '/^usage: /{exit} {print}' || true)"
    fi
    if [ -z "$(printf '%s' "$filtered" | tr -d '[:space:]')" ]; then
        printf '        (ansible 没有产生任何输出 —— 退出码非 0 且无 stderr)\n'
    else
        printf '%s\n' "$filtered" | head -40 | sed 's/^/        /'
    fi
}

# ----------------------------------------------------------------------------
#  前置检查
# ----------------------------------------------------------------------------
ansible_check() {
    log_step "Ansible 远程前置检查"

    _ansible_defaults
    require_cmd ansible

    local inv out ssh_user
    inv="$(_ansible_inventory)"
    ssh_user="$(_ansible_user_arg)"

    # 两级探测。以前只探一次（带 sudo），于是「SSH 根本没连上」和
    # 「连上了但 sudo 提权失败」混成同一句报错 —— 两者的排查方向完全不同。
    #   第一级：不带 --become，只验 SSH 密钥 + 远程 python
    #   第二级：带 --become，验 sudo（装 systemd 单元 / chown 都要 root）
    #
    # 必须 || true：ansible 失败时命令替换的返回码会传导到赋值语句，
    # 在 set -e 下直接把脚本打断，原始错误反而看不到了。
    local stage=""
    out="$(_ansible_capture_nobecome -m ping || true)"
    if printf '%s' "$out" | grep -q 'SUCCESS\|pong'; then
        log_ok "SSH 连通 ($ANSIBLE_HOSTS，用户: ${ssh_user:-<inventory 或当前用户>})"

        local need_become=0
        case "${ANSIBLE_BECOME}" in
            1|y|Y|yes|YES|Yes|true|TRUE|True|on|ON) need_become=1 ;;
        esac

        if [ "$need_become" -eq 1 ]; then
            out="$(_ansible_capture -m ping || true)"
            if printf '%s' "$out" | grep -q 'SUCCESS\|pong'; then
                log_ok "Ansible 连接就绪 ($ANSIBLE_HOSTS → sudo root)"
                return 0
            fi
            stage="sudo 提权"
            # 直接问 sudo 本人，比 ansible 转述的那句准得多
            local sudo_out
            sudo_out="$(_ansible_capture_nobecome -m command -a "sudo -n true" || true)"
            if [ -n "$sudo_out" ]; then
                log_dim "远程执行 sudo -n true 的原始输出："
                _ansible_dump_raw "$sudo_out"
            fi
        else
            log_ok "Ansible 连接就绪（未启用 sudo，后续需要 root 的步骤会失败）"
            return 0
        fi
    else
        stage="SSH 连接 / 远程 python"
    fi

    # 失败时一定要把原始输出打出来。之前是 >/dev/null 2>&1 全吞掉，
    # 只剩一句"无法连接"，根本分不清是 host 没匹配、SSH 被拒还是 sudo 失败。
    log_err "Ansible 无法连接 $ANSIBLE_HOSTS（失败层级: $stage），原始输出："
    _ansible_dump_raw "$out" >&2

    # 按错误类型给不同的排查方向。一股脑都推 inventory 会把真问题盖住：
    # 参数写错 / sudo 失败的表现跟 host 没匹配完全不是一回事。
    #
    # 顺序很重要：ansible 的 WARNING 里可能夹杂别的命令的 usage（比如把
    # deploy/ 下当 inventory 解析时会打印 render_config.py 的 usage），
    # 所以「主机不可达 / 认证失败」必须排在「参数错误」之前判断，
    # 而且参数错误只认 ansible 自己的那行 "ansible: error:"。
    if printf '%s' "$out" | grep -q 'UNREACHABLE\|Failed to connect to the host'; then
        cat >&2 <<EOF

  inventory 已经解析到主机了，是 SSH 连接/认证环节失败。依次查：
    1) SSH 用户 —— 命令行 -u 会覆盖 inventory 里的 ansible_user。
       手工跑一次同样的命令看用的是谁：
         ansible $ANSIBLE_HOSTS -m ping            # 不带 -u，用 inventory/当前用户
         ansible $ANSIBLE_HOSTS -u $ANSIBLE_USER -m ping   # 带 -u，复现本脚本的行为
       两边结果不一样，说明 inventory 里另有 ansible_user，
       这时不要传 --ansible-user，或把它改成 inventory 里的那个。
    2) 密钥：ssh-copy-id <用户>@<目标机IP>
    3) known_hosts 首次连接被拦：ssh -o StrictHostKeyChecking=no <用户>@<目标机IP>
EOF
    elif printf '%s' "$out" | grep -q 'Missing sudo password\|sudo: a password is required\|Incorrect sudo password\|requiretty\|a terminal is required\|may not run sudo'; then
        cat >&2 <<EOF

  SSH 那一层是通的，挂在 sudo 提权。ansible 走的是非交互 sudo（sudo -n），
  问不了密码，也不会有 tty。

  如果已经配过 NOPASSWD 还是这样，先确认 sudoers 真的生效：
    ssh -t $ANSIBLE_USER@<目标机IP> sudo -n true      # 不该问密码、不该报错
    ssh -t $ANSIBLE_USER@<目标机IP> sudo -l -U $ANSIBLE_USER   # 看实际授权了什么
  最常见的三种「配了还是不行」：
    · sudoers 条目没被加载 —— 必须放 /etc/sudoers.d/ 且 /etc/sudoers 里有
      #includedir /etc/sudoers.d；直接追加到 /etc/sudoers 末尾可能被后面的
      %sudo/%wheel 规则覆盖
    · Defaults requiretty —— ansible 没有 tty，有这条一定失败，改成
      Defaults!$ANSIBLE_USER !requiretty 或直接删掉
    · NOPASSWD 只授权了单条命令 —— ansible 要跑 /bin/sh -c，必须是 NOPASSWD: ALL

  三种解法，按推荐顺序：

    1) 目标机上给 $ANSIBLE_USER 配免密 sudo（本脚本一轮要调几十次 ansible，
       带密码的方式都很别扭）：
         ssh -t $ANSIBLE_USER@<目标机IP> \\
           "echo '$ANSIBLE_USER ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/$ANSIBLE_USER && sudo chmod 440 /etc/sudoers.d/$ANSIBLE_USER"

    2) 用口令文件（口令落盘，注意权限）：
         echo 'sudo口令' > ~/.ansible-become-pass && chmod 600 ~/.ansible-become-pass
         ./deploy/install.sh --ansible --ansible-become-pass-file ~/.ansible-become-pass

    3) 直接用 root 连（需目标机允许 root SSH 登录）：
         ./deploy/install.sh --ansible --ansible-user root

  只想先验证 SSH 那一层（跳过 sudo 检查）：
         ./deploy/install.sh --ansible --no-become
EOF
    elif printf '%s' "$out" | grep -q 'password script'; then
        cat >&2 <<EOF

  这是「口令文件」被解析成了目录/不可执行文件，ansible 想把它当脚本跑。
  典型原因是环境里有个**值为空的** ANSIBLE_*_PASSWORD_FILE：
  ansible 对 path 型配置拿到空串会 unfrackpath('')，结果就是当前目录，
  而目录的 x 位为 1（算「可执行」），于是被当成口令脚本去执行 → Permission denied。
  （和 ANSIBLE_INVENTORY="" 被解析成 CWD 是同一个坑。）

    1) 找出值为空的那些：env | grep '^ANSIBLE_'
    2) 临时绕过：unset ANSIBLE_BECOME_PASSWORD_FILE 后重跑
    3) 确认生效：ansible $ANSIBLE_HOSTS -m ping    # 不该再提 password script

  如果指向的是个真实文件，那是它有可执行位：chmod -x <该文件>
EOF
    elif printf '%s' "$out" | grep -q 'Could not match supplied host pattern\|No hosts matched\|does not match any hosts'; then
        cat >&2 <<EOF

  这是 host pattern 在 inventory 里解析不出主机。两条路任选其一：

    A) 直接给 IP（不需要 inventory 文件）：
         ./deploy/install.sh --ansible --ansible-hosts <目标机IP> --ansible-user $ANSIBLE_USER

    B) 写 inventory：cp deploy/ansible/hosts.example deploy/ansible/hosts 后改 IP，
         再 ./deploy/install.sh --ansible --ansible-inventory deploy/ansible/hosts
       看当前 inventory 里有哪些主机：
         ansible-inventory --list -i ${inv:-/etc/ansible/hosts}
EOF
    elif printf '%s' "$out" | grep -q '^ansible: error:\|ansible: error: argument'; then
        cat >&2 <<EOF

  这是 ansible 命令行参数本身不合法，跟网络无关。
  典型的是给开关型选项传了值（--become=yes、-o xxx 都是错的：
  -b/--become 不接受参数，-o 是 --one-line 也不接受参数）。
  手工复现：
    ansible $ANSIBLE_HOSTS -u $ANSIBLE_USER --become --become-user=root \\
            --become-method=sudo -m ping
EOF
    else
        cat >&2 <<EOF

  host pattern 解析到了主机，但连接/提权环节失败，且不属于上面任何一类。依次查：
    ssh $ANSIBLE_USER@<目标机IP>                   # SSH 密钥已授权
    ssh -t $ANSIBLE_USER@<目标机IP> sudo -n true   # 免密 sudo（装服务要写 /etc/systemd）
    ssh $ANSIBLE_USER@<目标机IP> which python3     # 需要 /usr/bin/python3

  如果上面「原始输出」是空的（ansible 一声不吭就退出），通常是：
    · ansible 被信号中断（SSH 卡死 / 超时 / known_hosts 交互提示被吞）
    · 输出全是 inventory 解析 WARNING，被本脚本过滤掉了
  加 verbose 重跑看真实过程：
    ANSIBLE_VERBOSE=1 ./deploy/install.sh --ansible --ansible-user $ANSIBLE_USER
EOF
    fi

    # 无论哪一类失败，都把本脚本真正执行的那条命令给出来，
    # 用户可以直接粘到终端复现，不用猜我们到底传了什么参数。
    printf '\n  本脚本实际执行的命令（可直接粘贴复现）:\n    ' >&2
    _ansible_cmdline -m ping >&2
    printf '\n' >&2
    die "Ansible 连接检查未通过"
}

# ----------------------------------------------------------------------------
#  远程：创建服务用户和用户组
# ----------------------------------------------------------------------------
ansible_ensure_user() {
    local user="$1" group="$2" home_dir="$3"
    log_step "远程创建用户/用户组"

    # 用户组
    if ! _ansible -m shell -a "getent group $group" >/dev/null 2>&1; then
        log_info "创建用户组: $group"
        _ansible -m group -a "name=$group state=present system=yes"
    else
        log_dim "用户组已存在: $group"
    fi

    # 用户
    if ! _ansible -m shell -a "id -u $user" >/dev/null 2>&1; then
        log_info "创建用户: $user"
        _ansible -m user -a \
            "name=$user group=$group home=$home_dir shell=/usr/sbin/nologin \
             create_home=no state=present system=yes"
    else
        log_dim "用户已存在: $user"
    fi

    log_ok "远程用户就绪: $user"
}

# ----------------------------------------------------------------------------
#  远程：确保目录存在且归属正确
# ----------------------------------------------------------------------------
ansible_mkdir() {
    local path="$1" user="$2" group="$3"
    log_info "远程创建目录: $path"
    _ansible -m file -a \
        "path=$path state=directory owner=$user group=$group mode=0755 recurse=yes"
}

# ----------------------------------------------------------------------------
#  远程：递归修正属主
#  synchronize 推上去的文件属主是 ANSIBLE_USER，而服务以 SERVICE_USER 运行，
#  配置又是 0600，属主不对服务就读不到配置。推完必须 chown 一次。
# ----------------------------------------------------------------------------
ansible_chown() {
    local path="$1" user="$2" group="$3"
    log_info "远程修正属主: $path -> $user:$group"
    _ansible -m file -a \
        "path=$path state=directory owner=$user group=$group recurse=yes"
}

# ----------------------------------------------------------------------------
#  推送：把本地渲染好的 staging 目录同步到远程
#  用法：ansible_push_staging <本地staging> <远程根目录>
#  示例：ansible_push_staging /tmp/centralService-staging.123 /home/fengyan/Server/centralService/bin
# ----------------------------------------------------------------------------
ansible_push_staging() {
    local stage="$1"
    local remote_root="$2"
    local user="$ANSIBLE_USER"

    log_step "同步渲染产物到远程"

    # staging 里每个服务一个子目录，内容已经是 install_service_files 的产物
    # 目录结构: <stage>/<svc>/{svc, *.json, *.sql, up.sh, ...}
    # 共享数据: <stage>/data/

    # 先同步各服务目录
    local svc
    for svc in "${INSTANCE_NAMES[@]}"; do
        if [ ! -d "$stage/$svc" ]; then
            log_warn "staging 缺少 $svc，跳过"
            continue
        fi
        log_info "同步 $svc -> $remote_root/$svc/"
        # 使用 rsync 风格同步，保持权限
        _ansible -m synchronize -a \
            "src=$stage/$svc/ dest=$remote_root/$svc/ delete=yes recursive=yes times=yes"
    done

    # 同步共享数据目录（如果有）
    if [ -d "$stage/data" ]; then
        log_info "同步 data/ -> $remote_root/data/"
        _ansible -m synchronize -a \
            "src=$stage/data/ dest=$remote_root/data/ delete=yes recursive=yes times=yes"
    fi

    log_ok "渲染产物已推送"
}

# ----------------------------------------------------------------------------
#  推送：把本地二进制目录同步到远程
#  用法：ansible_push_binaries <本地dist_dir> <远程根目录>
# ----------------------------------------------------------------------------
ansible_push_binaries() {
    local dist="$1"
    local remote_root="$2"

    log_step "同步 Linux 二进制到远程"

    local svc
    for svc in "${INSTANCE_NAMES[@]}"; do
        if [ ! -f "$dist/$svc/$svc" ]; then
            log_warn "缺少二进制 $dist/$svc/$svc，跳过"
            continue
        fi
        log_info "同步二进制 $svc -> $remote_root/$svc/"
        _ansible -m synchronize -a \
            "src=$dist/$svc/$svc dest=$remote_root/$svc/$svc delete=yes recursive=yes times=yes"
    done

    log_ok "二进制已推送"
}

# ----------------------------------------------------------------------------
#  推送：systemd 单元文件到远程
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
#  远程：推单个文件（logrotate 这类小文件，copy 比 synchronize 省事）
# ----------------------------------------------------------------------------
ansible_copy_file() {
    local src="$1" dest="$2" mode="${3:-0644}"
    if [ ! -f "$src" ]; then
        die "要推送的文件不存在: $src"
    fi
    _ansible -m copy -a "src=$src dest=$dest mode=$mode owner=root group=root"
}

ansible_push_units() {
    local unit_dir="$1"   # 本地临时目录，包含生成的 .service 文件
    local remote_unit_dir="/etc/systemd/system"

    log_step "推送 systemd 单元到远程"

    if [ ! -d "$unit_dir" ] || [ -z "$(ls -A "$unit_dir" 2>/dev/null)" ]; then
        log_warn "本地单元目录为空，跳过"
        return 0
    fi

    _ansible -m synchronize -a \
        "src=$unit_dir/ dest=$remote_unit_dir/ delete=no recursive=yes times=yes"

    # 立即 daemon-reload
    log_info "远程 reload-daemon"
    _ansible -m systemd -a "daemon_reload=yes"

    log_ok "systemd 单元已推送并 reload"
}

# ----------------------------------------------------------------------------
#  远程：启用并启动服务
# ----------------------------------------------------------------------------
ansible_service_restart() {
    local svc="$1"
    local unit_name
    unit_name="$(unit_name "$svc")"
    log_info "远程 restart $unit_name"
    _ansible -m systemd -a \
        "name=$unit_name state=restarted enabled=yes daemon_reload=yes"
}

ansible_service_stop() {
    local svc="$1"
    local unit_name
    unit_name="$(unit_name "$svc")"
    log_info "远程 stop $unit_name"
    _ansible -m systemd -a "name=$unit_name state=stopped" || true
}

# ----------------------------------------------------------------------------
#  远程：执行数据库初始化（up.sh）
# ----------------------------------------------------------------------------
ansible_db_init() {
    local svc="$1" prefix="$2"
    local up="$prefix/$svc/up.sh"

    log_info "远程执行 $svc up.sh"
    _ansible -m shell -a \
        "cd $prefix/$svc && sh ./up.sh"
}

# ----------------------------------------------------------------------------
#  远程：健康检查（调用远程的 healthcheck.sh）
# ----------------------------------------------------------------------------
ansible_healthcheck() {
    local env_file="$1" instances_file="$2"
    local remote_deploy_dir="$3"   # 远程 deploy/ 路径（与仓库结构对应）

    log_step "远程健康检查"
    # 在远程以 root 身份执行 healthcheck
    _ansible -m script -a \
        "$DEPLOY_DIR/healthcheck.sh --env $env_file --instances $instances_file"
}

# ----------------------------------------------------------------------------
#  远程：查询已安装服务列表（用于 upgrade / uninstall）
# ----------------------------------------------------------------------------
ansible_list_installed() {
    local prefix="$1"
    _ansible -m shell -a \
        "systemctl list-units --type=service --no-legend | \
         grep 'centralsvc-' | awk '{print \$1}' | sed 's/centralsvc-//;s/.service//'"
}
