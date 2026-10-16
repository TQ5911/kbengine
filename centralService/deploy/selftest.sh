#!/usr/bin/env bash
# 临时冒烟测试：只验证不依赖 root/systemd 的纯逻辑部分
set -uo pipefail

DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$DEPLOY_DIR/.." && pwd)"
export PYTHONIOENCODING=utf-8
fails=0

# 本地是 Windows + Git Bash，python3 只是 Microsoft Store 的占位符；
# 目标环境是 Linux，python3 一定存在。这里只为本地自测兜底。
if ! python3 -c 'pass' >/dev/null 2>&1; then
    python3() { python "$@"; }
fi

ok()   { printf '  \033[32mOK\033[0m    %s\n' "$*"; }
bad()  { printf '  \033[31mFAIL\033[0m  %s\n' "$*"; fails=$((fails+1)); }

. "$DEPLOY_DIR/lib/common.sh"
set_repo_root ""
require_python
PY="$PYTHON"

echo "== 1. instances.conf 解析 =="
if read_instances "$DEPLOY_DIR/instances.conf"; then
    ok "解析出 ${#INSTANCE_NAMES[@]} 个服务: ${INSTANCE_NAMES[*]}"
    [ "${INSTANCE_PORTS[admin]}" = "8080,8081,2040,2050,2051" ] \
        && ok "admin 端口表正确" || bad "admin 端口表异常: ${INSTANCE_PORTS[admin]}"
    [ "${INSTANCE_DB_INIT[router]}" = "no" ] \
        && ok "router db_init=no" || bad "router db_init 异常"
    [ "${INSTANCE_NAMES[0]}" = "centralLogin" ] \
        && ok "启动顺序首项为 centralLogin" || bad "启动顺序异常"
    [ "${#INSTANCE_NAMES[@]}" -eq 12 ] \
        && ok "服务总数 12" || bad "服务总数为 ${#INSTANCE_NAMES[@]}，期望 12"
else
    bad "instances.conf 解析失败"
fi

echo "== 2. 服务名与目录/二进制命名一致性 =="
missing=""
for svc in "${INSTANCE_NAMES[@]}"; do
    [ -d "$REPO_ROOT/src/$svc" ] || missing="$missing src/$svc"
    [ -d "$REPO_ROOT/bin/$svc" ] || missing="$missing bin/$svc"
    [ -f "$REPO_ROOT/bin/$svc/$svc.json" ] || missing="$missing bin/$svc/$svc.json"
done
[ -z "$missing" ] && ok "12 个服务的源码目录、产物目录、主配置齐全" \
    || bad "缺失:$missing"

echo "== 3. systemd 单元模板渲染 =="
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
tpl_clear
tpl_set SERVICE maple; tpl_set DESCRIPTION 大区服务; tpl_set INSTALL_ROOT /opt/centralService
tpl_set SERVICE_USER fengyan; tpl_set SERVICE_GROUP fengyan
tpl_set TIMEZONE Asia/Shanghai; tpl_set GOTRACEBACK crash
tpl_set START_TIMEOUT 90; tpl_set STOP_TIMEOUT 30; tpl_set RESTART_SEC 3
tpl_set PROTECT_HOME "$(protect_home_value)"
tpl_set STDOUT_TARGET "append:/opt/centralService/maple/maple.out.log"
tpl_set STDERR_TARGET "append:/opt/centralService/maple/maple.out.log"
render_template "$DEPLOY_DIR/templates/centralsvc.service.template" "$tmp/centralsvc-maple.service"
tpl_assert_no_leftover "$tmp/centralsvc-maple.service" \
    && ok "模板渲染无残留占位符" || bad "模板渲染有残留占位符"
grep -q '^WorkingDirectory=/opt/centralService/maple$' "$tmp/centralsvc-maple.service" \
    && ok "WorkingDirectory 指向同名目录" || bad "WorkingDirectory 不正确"
grep -q '^ExecStart=/opt/centralService/maple/maple --instid=0$' "$tmp/centralsvc-maple.service" \
    && ok "ExecStart 路径与目录同名" || bad "ExecStart 不正确"
grep -vE '^[[:space:]]*#' "$tmp/centralsvc-maple.service" | grep -q '%i' \
    && bad "具体单元的有效配置行里残留 %i 占位符（systemd 会报错）" \
    || ok "有效配置行无 %i 实例占位符残留"
grep -q '^ExecStartPre=-/bin/sh -c .*maple_0\.pid' "$tmp/centralsvc-maple.service" \
    && ok "ExecStartPre 清理残留 pid 文件（带 - 容错前缀）" || bad "缺/错 ExecStartPre pid 清理"
# 单元里 systemd 会把 $$ 还原成 $，还原后的片段必须是合法 shell
awk '/^ExecStartPre=-\/bin\/sh -c /{sub(/^ExecStartPre=-\/bin\/sh -c .?/,"");sub(/.$/,"");gsub(/\$\$/,"$");print}' \
    "$tmp/centralsvc-maple.service" > "$tmp/pre.sh"
bash -n "$tmp/pre.sh" 2>/dev/null \
    && ok "ExecStartPre 的 shell 片段语法正确" || bad "ExecStartPre 的 shell 片段有语法错误"
grep -q '^Restart=always$' "$tmp/centralsvc-maple.service" && ok "Restart=always" || bad "缺 Restart"
grep -q '^KillSignal=SIGTERM$' "$tmp/centralsvc-maple.service" && ok "KillSignal=SIGTERM" || bad "缺 KillSignal"
grep -q '^StandardOutput=append:/opt/centralService/maple/maple.out.log$' "$tmp/centralsvc-maple.service" \
    && ok "stdout 落在服务目录内" || bad "stdout 没有落到服务目录"

# 日志去向：file 模式给 append: 路径，journal 模式给 journal
PREFIX=/opt/centralService
[ "$(LOG_STDOUT_MODE=file stdout_target maple)" = "append:/opt/centralService/maple/maple.out.log" ] \
    && ok "stdout_target file 模式" || bad "stdout_target file 模式不对: $(LOG_STDOUT_MODE=file stdout_target maple)"
[ "$(LOG_STDOUT_MODE=journal stdout_target maple)" = "journal" ] \
    && ok "stdout_target journal 模式" || bad "stdout_target journal 模式不对"

# ProtectHome：装到 /home 下必须关掉，否则 systemd 把 /home 挂成空 tmpfs，
# execve 找不到二进制 → 203/EXEC
[ "$(PREFIX=/home/fengyan/Server/centralService; protect_home_value)" = "no" ] \
    && ok "安装目录在 /home 下时 ProtectHome=no" || bad "/home 下 ProtectHome 没关掉"
[ "$(PREFIX=/opt/centralService; protect_home_value)" = "true" ] \
    && ok "安装目录在 /opt 下时 ProtectHome=true" || bad "/opt 下 ProtectHome 应为 true"
[ "$(SYSTEMD_PROTECT_HOME=read-only; protect_home_value)" = "read-only" ] \
    && ok "SYSTEMD_PROTECT_HOME 可覆盖" || bad "SYSTEMD_PROTECT_HOME 覆盖失效"
grep -q '^ProtectHome=true$' "$tmp/centralsvc-maple.service" \
    && ok "渲染出的 ProtectHome 值正确" || bad "渲染出的 ProtectHome 值不对"

echo "== 3b. logrotate 模板渲染 =="
tpl_clear
tpl_set INSTALL_ROOT /opt/centralService; tpl_set SERVICE_USER fengyan
tpl_set SERVICE_GROUP fengyan; tpl_set LOG_ROTATE_KEEP 7
render_template "$DEPLOY_DIR/templates/logrotate.conf.template" "$tmp/logrotate.conf"
tpl_assert_no_leftover "$tmp/logrotate.conf" \
    && ok "logrotate 模板渲染无残留占位符" || bad "logrotate 模板有残留占位符"
grep -q '^/opt/centralService/\*/\*\.log {$' "$tmp/logrotate.conf" \
    && ok "logrotate 覆盖各服务目录下的日志" || bad "logrotate 匹配路径不对"
grep -q '^    copytruncate$' "$tmp/logrotate.conf" \
    && ok "logrotate 用 copytruncate（进程持有 fd）" || bad "缺 copytruncate"

echo "== 4. nginx 模板渲染 =="
tpl_clear
tpl_set ADMIN_HOSTNAME gm.example.com; tpl_set ADMIN_GMT_PORT 2050
tpl_set ADMIN_HTTP_PORT 8080; tpl_set ADMIN_SDK_PORT 8081
tpl_set SSL_CERT /etc/ssl/a.pem; tpl_set SSL_KEY /etc/ssl/a.key
render_template "$DEPLOY_DIR/templates/nginx-admin.conf.template" "$tmp/nginx.conf"
tpl_assert_no_leftover "$tmp/nginx.conf" && ok "nginx 模板渲染无残留" || bad "nginx 模板有残留"
grep -q '127.0.0.1:2050' "$tmp/nginx.conf" && ok "grpc-web 端口取自 admin.json" || bad "nginx 端口不对"

echo "== 5. 配置渲染器端到端 =="
printf 'MYSQL_ADDR=10.0.0.1\nMYSQL_USER=prod\nMYSQL_PASSWD=pw\nREDIS_ADDR=10.0.0.2:6380\nREDIS_PASSWD=rp\nREPORT_ADDR=https://hook\n' > "$tmp/env"
printf 'router:routerClusterAdvertiseAddr="10.0.0.5:2061"\ncentralLogin/serverList.json:gameServerList.20001="10.0.0.9:20013"\n' > "$tmp/ovr"
if python3 "$DEPLOY_DIR/lib/render_config.py" --src-dir "$REPO_ROOT/bin" --out-dir "$tmp/out" \
      --env "$tmp/env" --overrides "$tmp/ovr" --instances "$DEPLOY_DIR/instances.conf" >"$tmp/render.log" 2>&1; then
    ok "渲染成功"
else
    bad "渲染失败"; sed 's/^/        /' "$tmp/render.log"
fi
python3 - "$tmp/out" <<'PY'
import json, os, sys
out = sys.argv[1]
bad = []
def check(cond, msg):
    if not cond: bad.append(msg)

# 无端口的 MYSQL_ADDR 应补全端口
m = json.load(open(os.path.join(out, "maple", "maple.json"), encoding="utf-8"))
check(m["mysql"]["addr"] == "10.0.0.1:3306", "maple mysql.addr 未补端口: %s" % m["mysql"]["addr"])
check(m["mysql"]["user"] == "prod", "maple mysql.user 未覆盖")
# orderService 的异名键 password
o = json.load(open(os.path.join(out, "orderService", "orderService.json"), encoding="utf-8"))
check("passwd" not in o["mysql"], "orderService 不应被塞进 passwd 键")
check(o["mysql"]["password"] == "pw", "orderService mysql.password 未覆盖: %s" % o["mysql"])
# auction 用的是 redis 块名 + user 键名
a = json.load(open(os.path.join(out, "auction", "auction.json"), encoding="utf-8"))
check(a["redis"]["addr"] == "10.0.0.2:6380", "auction redis.addr 未覆盖")
check(a["redis"]["user"] == "", "auction redis.user 键名异常")
# leaseServer 用的是大写 RedisServer / Mysql
l = json.load(open(os.path.join(out, "leaseServer", "leaseServer.json"), encoding="utf-8"))
check(l["RedisServer"]["addr"] == "10.0.0.2:6380", "leaseServer RedisServer 未覆盖")
check(l["Mysql"]["passwd"] == "pw", "leaseServer Mysql.passwd 未覆盖")
# 跨文件覆盖：只作用于显式指定的文件
c = json.load(open(os.path.join(out, "centralLogin", "centralLogin.json"), encoding="utf-8"))
check("redisServer" in c and "maxIdle" not in c["redisServer"],
      "centralLogin.json 不该被塞 maxIdle: %s" % c.get("redisServer"))
sl = json.load(open(os.path.join(out, "centralLogin", "serverList.json"), encoding="utf-8"))
check(sl["gameServerList"]["20001"] == "10.0.0.9:20013", "serverList 覆盖未生效")
check("redisServer" not in sl, "serverList.json 被误塞 redisServer")
# 权限：Windows/NTFS 不映射 POSIX 权限位，os.chmod 形同虚设，只在 posix 上断言
if os.name == "posix":
    mode = oct(os.stat(os.path.join(out, "maple", "maple.json")).st_mode)[-3:]
    check(mode == "600", "渲染产物权限应为 600，实际 %s" % mode)
else:
    print("        (跳过权限断言：当前非 POSIX 平台)")
for b in bad: print("        - " + b)
sys.exit(1 if bad else 0)
PY
if [ $? -eq 0 ]; then ok "渲染结果校验通过（键名异名/端口补全/跨文件隔离/权限）"; else bad "渲染结果校验未通过"; fi

echo "== 6. 遗留内网地址扫描 =="
scan_out="$(python3 "$DEPLOY_DIR/lib/render_config.py" --src-dir "$REPO_ROOT/bin" \
    --out-dir "$tmp/scan" --env "$tmp/env" --instances "$DEPLOY_DIR/instances.conf" 2>&1)"
if printf '%s' "$scan_out" | grep -q '高危'; then
    ok "检出开发机残留地址（无 overrides 时应报警）"
    printf '%s\n' "$scan_out" | grep -E '192\.168|10\.[0-9]|172\.(1[6-9]|2[0-9]|3[01])' \
        | head -3 | sed 's/^/        /'
else
    bad "未检出开发机残留地址"
fi
if printf '%s' "$scan_out" | grep -q '提示：以下指向本机'; then
    ok "loopback 地址被单独归为提示档，不与高危混在一起"
else
    bad "未做 loopback / rfc1918 分档"
fi
# deploy.env 里声明的地址不该被当成残留
if printf '%s' "$scan_out" | grep -q '10\.20\.30\.40'; then
    bad "deploy.env 声明的 MYSQL_ADDR 被误报为残留"
else
    ok "deploy.env 声明的 MYSQL/Redis 地址已排除，不误报"
fi
# --strict 应以非零码卡住
python3 "$DEPLOY_DIR/lib/render_config.py" --src-dir "$REPO_ROOT/bin" \
    --out-dir "$tmp/scan2" --env "$tmp/env" --instances "$DEPLOY_DIR/instances.conf" \
    --strict >/dev/null 2>&1
if [ $? -ne 0 ]; then ok "--strict 在有残留地址时返回非零码"; else bad "--strict 未卡住"; fi
# 补齐 overrides 后应放行
printf 'router:routerClusterAdvertiseAddr="10.0.0.5:2061"\nadmin:mapleHttpAddr="10.0.0.5:9527"\nleaseServer:mapleHttpAddr="10.0.0.5:9527"\ncentralLogin/serverList.json:gameServerList.20001="10.0.0.9:20013"\ncentralLogin/serverList.json:queueServerList.20001="10.0.0.9:7999"\n' > "$tmp/ovr2"
python3 "$DEPLOY_DIR/lib/render_config.py" --src-dir "$REPO_ROOT/bin" \
    --out-dir "$tmp/scan3" --env "$tmp/env" --overrides "$tmp/ovr2" \
    --instances "$DEPLOY_DIR/instances.conf" --strict >/dev/null 2>&1
if [ $? -eq 0 ]; then ok "补齐 overrides 后 --strict 放行"; else bad "补齐 overrides 后仍被卡住"; fi

echo "== 7. game.sh 语法与 ps 兼容性 =="
for f in "$REPO_ROOT"/bin/*/game.sh; do
    if ! bash -n "$f" 2>/dev/null; then bad "语法错误: $f"; fi
done
if grep -vE '^[[:space:]]*#' "$REPO_ROOT"/bin/*/game.sh | grep -q 'ps -A'; then
    bad "仍有文件在实际执行 ps -A + awk 解析"
else
    ok "12 个 game.sh 语法正确，实际执行语句里已无 ps -A 列解析"
fi

echo "== 8. set -e 下的行为（模拟 install.sh 的 shell 选项）==="
# install.sh / upgrade.sh 都是 set -euo pipefail。函数里的
# `cond && cmd` 在 cond 为假时会让整条语句返回 1 并触发退出，
# 自测本身若不开 -e 就发现不了这类问题，所以这里显式在 -e 下跑一遍。
if bash -c "
    set -euo pipefail
    . '$DEPLOY_DIR/lib/common.sh'
    read_instances '$DEPLOY_DIR/instances.conf'
    [ \${#INSTANCE_NAMES[@]} -eq 12 ] || exit 1
    tpl_clear
    tpl_set SERVICE smoke; tpl_set DESCRIPTION 冒烟; tpl_set INSTALL_ROOT /opt/centralService
    tpl_set SERVICE_USER u; tpl_set SERVICE_GROUP g; tpl_set TIMEZONE UTC
    tpl_set GOTRACEBACK crash; tpl_set START_TIMEOUT 90; tpl_set STOP_TIMEOUT 30; tpl_set RESTART_SEC 3
    tpl_set PROTECT_HOME \$(protect_home_value)
    tpl_set STDOUT_TARGET journal; tpl_set STDERR_TARGET journal
    render_template '$DEPLOY_DIR/templates/centralsvc.service.template' '$tmp/smoke.service'
    tpl_assert_no_leftover '$tmp/smoke.service'
    load_env_file '$tmp/env'
    unit_name smoke >/dev/null
    is_true 1
    if is_true 0; then exit 1; fi
" 2>"$tmp/errexit.log"; then
    ok "read_instances / render_template / tpl_assert / load_env / is_true 在 set -e 下均正常"
else
    bad "set -e 下函数异常退出："
    sed 's/^/        /' "$tmp/errexit.log"
fi

# build_linux.sh 不带参数时必须正常进入编译流程，而不是被 && 短路吃掉
if grep -n '^\s*\[[^]]*\]\s*||\s*\[[^]]*\]\s*&&' "$DEPLOY_DIR/build_linux.sh" >/dev/null 2>&1; then
    bad "build_linux.sh 仍存在 A || B && C 写法"
else
    ok "build_linux.sh 无 A || B && C 写法"
fi

echo "== 9. 交付二进制校验 =="
DIST_DIR_REAL="$REPO_ROOT/dist"
if [ ! -d "$DIST_DIR_REAL" ]; then
    bad "缺少 dist/，请先执行 ./deploy/build_linux.sh（交付路径依赖它）"
else
    # abspath：相对路径必须在 cd 之前转绝对，否则 go build 会写歪
    cd "$REPO_ROOT" || exit 1
    if [ "$(abspath dist)" = "$REPO_ROOT/dist" ]; then
        ok "abspath 能把相对路径转绝对"
    else
        bad "abspath 结果异常: $(abspath dist)"
    fi

    # 真实产物应全部通过
    if "$PY" "$DEPLOY_DIR/lib/verify_artifact.py" --repo-root "$REPO_ROOT" \
        --dist-dir "$DIST_DIR_REAL" --instances "$DEPLOY_DIR/instances.conf" \
        --strict-fresh >"$tmp/verify.log" 2>&1; then
        ok "dist/ 下 12 个产物全部通过格式+架构+新鲜度校验"
    else
        bad "dist/ 产物未通过校验"
        sed 's/^/        /' "$tmp/verify.log"
    fi

    # 造三种坏产物，逐一确认能被抓出来
    fake="$tmp/fakedist"
    mkdir -p "$fake/maple"
    cp "$DIST_DIR_REAL/maple/maple" "$fake/maple/maple"

    cp "$DIST_DIR_REAL/maple/maple" "$fake/maple/maple"
    touch -d '30 days ago' "$fake/maple/maple"
    "$PY" "$DEPLOY_DIR/lib/verify_artifact.py" --repo-root "$REPO_ROOT" \
        --dist-dir "$fake" --instances "$DEPLOY_DIR/instances.conf" \
        --strict-fresh >/dev/null 2>&1
    if [ $? -ne 0 ]; then ok "过期二进制被 --strict-fresh 拦下"; else bad "过期二进制未被拦截"; fi

    if [ -f "$REPO_ROOT/bin/maple/maple.exe" ]; then
        cp "$REPO_ROOT/bin/maple/maple.exe" "$fake/maple/maple"
        out="$("$PY" "$DEPLOY_DIR/lib/verify_artifact.py" --repo-root "$REPO_ROOT" \
            --dist-dir "$fake" --instances "$DEPLOY_DIR/instances.conf" 2>&1)"
        if printf '%s' "$out" | grep -q '非ELF'; then
            ok "拷错成 Windows .exe 会被识别出来"
        else
            bad "非 ELF 文件未被识别"
        fi
    fi

    rm -f "$fake/maple/maple"
    out="$("$PY" "$DEPLOY_DIR/lib/verify_artifact.py" --repo-root "$REPO_ROOT" \
        --dist-dir "$fake" --instances "$DEPLOY_DIR/instances.conf" 2>&1)"
    if printf '%s' "$out" | grep -q '缺失'; then
        ok "缺失的二进制会被报出来"
    else
        bad "缺失的二进制未被报出"
    fi
fi

echo "== 10. 仓库根目录定位（deploy/ 被单独拷走时）=="
# 复现实际场景：deploy/ 拷到别处，仓库在 ~/Server/centralService
if [ "$(resolve_repo_root "")" = "$REPO_ROOT" ]; then
    ok "deploy/ 在仓库内时，向上查找能定位到 $REPO_ROOT"
else
    bad "向上查找失败: $(resolve_repo_root "")"
fi

# 把 deploy/ 复制到别处，模拟只拷脚本上机的情形
away="$tmp/elsewhere/deploy"
mkdir -p "$tmp/elsewhere"
cp -r "$DEPLOY_DIR" "$away"

# 不带任何提示时，向上找不到，应返回非零
if ( . "$away/lib/common.sh"; resolve_repo_root "" >/dev/null 2>&1 ); then
    bad "deploy/ 脱离仓库后不该凭空找到仓库根"
else
    ok "deploy/ 脱离仓库时向上查找正确失败"
fi

# CENTRAL_REPO_ROOT 环境变量
got="$( CENTRAL_REPO_ROOT="$REPO_ROOT" bash -c ". '$away/lib/common.sh'; resolve_repo_root ''" 2>/dev/null )"
if [ "$got" = "$REPO_ROOT" ]; then
    ok "CENTRAL_REPO_ROOT 环境变量可用"
else
    bad "CENTRAL_REPO_ROOT 未生效（得到: $got）"
fi

# 显式传参
got="$( bash -c ". '$away/lib/common.sh'; resolve_repo_root '$REPO_ROOT'" 2>/dev/null )"
if [ "$got" = "$REPO_ROOT" ]; then
    ok "--repo-root 显式指定可用"
else
    bad "--repo-root 未生效（得到: $got）"
fi

# 指向无效目录时应报错而不是静默通过
if ( . "$away/lib/common.sh"; resolve_repo_root "/tmp/not-a-repo" >/dev/null 2>&1 ); then
    bad "无效的 --repo-root 被静默接受"
else
    ok "无效的 --repo-root 会被拒绝"
fi

# dist/ 优先，没有才退回 bin/
d="$(resolve_dist_dir "$REPO_ROOT")"
if [ -d "$REPO_ROOT/dist" ]; then
    if [ "$d" = "$REPO_ROOT/dist" ]; then ok "有 dist/ 时优先用 dist/"; else bad "dist/ 优先级不对: $d"; fi
else
    if [ "$d" = "$REPO_ROOT/bin" ]; then ok "没有 dist/ 时退回 bin/"; else bad "回退逻辑不对: $d"; fi
fi

echo
if [ "$fails" -eq 0 ]; then printf '\033[32m全部通过\033[0m\n'; else printf '\033[31m%d 项失败\033[0m\n' "$fails"; fi
exit "$fails"