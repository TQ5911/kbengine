# centralService 一键部署（systemd）

把本仓库的 12 个 Go 服务一次性部署成 Linux 上的 systemd 服务，并完成
MySQL 建库导表、配置渲染、启动与健康检查。

## 为什么是这个方案

12 个服务都是纯 Go 静态二进制，程序自带 pid 文件、优雅退出、按大小滚动日志。
这些正好是 systemd 已经做好的事，中间再插一层 supervisord 或容器运行时是额外成本。
单元文件是**生成**出来的，不是手写 12 份。

## 30 秒上手

```bash
# 1. 在开发机上填配置
cp deploy/deploy.env.example deploy/deploy.env
cp deploy/overrides.conf.example deploy/overrides.conf
$EDITOR deploy/deploy.env          # 至少改 MYSQL_PASSWD

# 2. 拷贝到目标机后演练
scp -r deploy deploy.env overrides.conf user@host:/tmp/cs-deploy/
ssh user@host
sudo /tmp/cs-deploy/deploy/install.sh --dry-run     # 只看要做什么，不改系统

# 3. 真正部署
sudo /tmp/cs-deploy/deploy/install.sh
```

`install.sh` 默认会依次完成：前置检查 → 交叉编译 → 渲染配置 → 安装文件 →
建库导表 → 生成并启用单元 → 按顺序启动 → 健康检查。

## 交付到生产：先确认仓库状态

**不要直接 `git clone` 部署。** 至少确认两件事：

```bash
# 1. bin/ 下必须已有配置基线（否则渲染器报「源目录不存在」）
git ls-files bin | head          # 现在是空的，需要先提交

# 2. 工作区不能有未提交的重构（服务改名会让 instances.conf 与 src/ 对不上）
git status --porcelain
```

`instances.conf` 按服务名找 `src/<服务名>/` 和 `bin/<服务名>/`，服务一旦改名或
新增但没提交，clone 出来的代码和清单就对不上，部署会在第一步就失败。

### 两种交付方式

**A. 构建机出包（推荐）** —— 目标机不需要 Go：

```bash
# 构建机（Windows/macOS/Linux 均可）
./deploy/build_linux.sh                        # 产出 dist/<服务名>/<服务名>

# 拷贝「仓库 + dist/」到目标机，然后
sudo ./deploy/install.sh --skip-build --strict-ips --strict-fresh
```

`--skip-build` 只跳过编译，**不会**跳过产物校验。

**B. 目标机现编** —— 需要目标机装 Go 1.21+（约 500MB）+ 网络能拉 module：

```bash
sudo ./deploy/install.sh --strict-ips --strict-fresh
```

### C. Ansible 远程部署（推荐用于"开发机 build → 部署机跑服务"）

**适用场景**：开发机有代码和构建工具，部署机只跑服务，两者通过 SSH 连接。

```bash
# 1. 开发机上配置 Ansible 连接
cp deploy/deploy.env.example deploy/deploy.env
$EDITOR deploy/deploy.env        # 填 MySQL 口令 + ANSIBLE_HOSTS / ANSIBLE_USER
cp deploy/overrides.conf.example deploy/overrides.conf

# 2. 确认 Ansible 能连通目标机
#    inventory 组方式（组名 tmp 必须有 inventory 定义它）
cp deploy/ansible/hosts.example deploy/ansible/hosts
$EDITOR deploy/ansible/hosts      # 把 IP 改成目标机真实地址
ansible tmp -i deploy/ansible/hosts -u fengyan -m ping

#    或者直接给 IP，不建 inventory 文件
ansible -i '172.16.41.49,' -u fengyan -m ping

# 2b. 目标机上给部署用户配免密 sudo（不配的话 ansible 会卡在 "Missing sudo password"）
ssh -t fengyan@<目标机IP> \
  "echo 'fengyan ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/fengyan && sudo chmod 440 /etc/sudoers.d/fengyan"
ssh -t fengyan@<目标机IP> sudo -n true     # 不该再问密码

# 3. 演练（只检查连接 + 渲染配置，不改系统）
./deploy/install.sh --ansible --dry-run

# 4. 真正部署
./deploy/install.sh --ansible
```

**Ansible 模式完整流程**：preflight → build（本地）→ render（本地）→ **远程创建用户** → **远程同步二进制+配置** → **远程安装 systemd 单元** → **远程启动服务** → **健康检查**。

**Ansible 模式下目标机需要的依赖**：

| 依赖 | 必需性 | 说明 |
|---|---|---|
| python3 | 必需 | Ansible 需要 `/usr/bin/python3` |
| SSH 密钥授权 | 必需 | 开发机 `~/.ssh/id_rsa.pub` 已加入目标机 `~/.ssh/authorized_keys` |
| 免密 sudo | 必需 | 写 `/etc/systemd/system`、chown 都要 root。**必须免密**，ansible 是非交互的 |
| rsync | 必需 | `ansible_push_*` 用 rsync 同步文件 |
| systemd | 必需 | 目标机跑服务本身需要 systemd |

关键参数：

```bash
# 用 inventory 组（deploy/ansible/hosts 存在时会被自动发现）
./deploy/install.sh --ansible --ansible-hosts tmp
./deploy/install.sh --ansible --ansible-inventory deploy/ansible/hosts

# 直接指定 IP（不需要 inventory 文件，脚本自动用内联 inventory）
./deploy/install.sh --ansible --ansible-hosts 172.16.41.49 --ansible-user fengyan

# 也可以写在 deploy.env 里（见 deploy.env.example）
```

**`--ansible-hosts` 必须能在 inventory 里解析出主机**，这是最容易踩的坑：
ansible ad-hoc 不会把没在 inventory 里的 IP 当主机用，只会报
`Could not match supplied host pattern`。所以要么写 inventory 文件，
要么用"看起来像主机名"的值（纯 IP 或带点的域名），脚本对后者会自动补 `-i '<值>,'`。
组名（`tmp`、`webservers` 这类不带点的）则必须有 inventory 定义。

**注意**：Ansible 模式下的 `--skip-build` 跳过编译但**不跳过**二进制校验，
因为开发机本地已经有 `dist/` 了。如果 `dist/` 里的二进制比源码旧，
`--strict-fresh` 会直接拒绝推送。

### deploy/ 单独拷到别处也可以

脚本不再假设 `deploy/` 必须在仓库内。仓库根目录按以下顺序定位
（判据是目录下同时有 `go.mod` 和 `src/`）：

1. `--repo-root /path/to/centralService`
2. `CENTRAL_REPO_ROOT=/path/to/centralService`
3. 从 `deploy/` 向上逐级查找
4. 常见自建位置：`~/Server/centralService`、`~/centralService` 等；
   `sudo` 运行时也会用 `SUDO_USER` 的家目录再找一遍

比如只把脚本拷到 `/tmp/deploy`：

```bash
sudo bash /tmp/deploy/install.sh --skip-build --dry-run
# 找不到时会明确告诉你是哪个候选路径不成立，并给出上面三种指定方式
```

### 没有 dist/ 时会退回 bin/

现网的服务器往往只有 `bin/`，没有构建产物目录。这时 `install.sh` 会退回用
`bin/<服务名>/<服务名>`，并打一条告警。**可以接受**，因为产物校验会拿它跟
仓库里的 `src/` 比时间：源码有改动而二进制没跟上，照样会被拦下。

如果连 `src/` 也没有（只拷了 `bin/`），新鲜度检查会如实标记为「跳过」
而不是把 12 个服务全报成过期——此时只能靠你自己保证源码和产物一致。

### 目标机需要什么

| 依赖 | 必需性 | 说明 |
|---|---|---|
| systemd | 必需 | `install.sh` 会拒绝在没有 systemd 的环境执行 |
| python3 | 必需 | 配置渲染器 |
| bash 4+ | 必需 | 脚本用了关联数组 |
| Go 1.21+ | 仅方式 B | 方式 A 不需要 |
| mysql 客户端 | 仅建库导表 | `up.sh` 依赖它；`--no-db-init` 可跳过 |
| MySQL / Redis 服务 | 必需 | 本方案不负责安装，只做前置检查 |

## 目录结构

```
deploy/
├── install.sh          一键部署主入口
├── upgrade.sh          灰度升级，探活失败自动回滚
├── healthcheck.sh      全量健康检查（单元状态 + pid + 端口）
├── uninstall.sh        卸载
├── build_linux.sh      交叉编译 Linux 二进制到 dist/（Windows/macOS/Linux 都能跑）
├── selftest.sh         工具链自测（不碰系统，可在开发机随时跑）
├── instances.conf      服务清单：名字、探活端口、是否建库、启动顺序
├── deploy.env.example  中间件连接与运行时参数（复制成 deploy.env）
├── overrides.conf.example  逐服务地址/端口覆盖（复制成 overrides.conf）
├── lib/
│   ├── common.sh           日志、清单解析、端口探测、模板渲染
│   ├── render_config.py    配置渲染器
│   └── verify_artifact.py  交付二进制校验（格式 / 架构 / 新鲜度）
└── templates/
    ├── centralsvc.service.template   systemd 单元模板
    ├── logrotate.conf.template       日志轮转（安装时写到 /etc/logrotate.d/centralsvc）
    └── nginx-admin.conf.template     admin 的 grpc-web 反代（可选）
```

## 目标机目录结构

```
/home/fengyan/Server/centralService/
└── bin/                        ← INSTALL_ROOT / ANSIBLE_REMOTE_PREFIX
    ├── maple/
    │   ├── maple               二进制（文件名 = 目录名 = 服务名）
    │   ├── maple.json          渲染后的配置
    │   ├── maple.log           业务日志（lumberjack）
    │   ├── maple.out.log       stdout/stderr（systemd append:）
    │   ├── maple_0.pid
    │   └── up.sh / game.sh
    ├── centralLogin/ …
    └── data/                   各服务共享数据，服务里以 ../data 访问
```

末级 `bin` 只是服务的上级目录，不受「目录名 = 服务名」约束；**再下一层才必须同名**。

## `bin/` 和 `dist/` 的分工

这两个目录**不能混用**，混了就会出很难查的问题：

| | `bin/` | `dist/` |
|---|---|---|
| 内容 | 配置基线、SQL、证书、本地跑出来的 log/pid | 只有 `build_linux.sh` 写进去的交付产物 |
| 入库 | 配置类入库，`.exe`/二进制/log 不入库 | 不入库（等同 CI 的 build artifact） |
| 用途 | `render_config.py` 的渲染基线 | `install.sh` 装的就是这里的东西 |

为什么必须分开：`bin/` 长期混着配置、Windows 的 `.exe`、vendored 的 protoc，
以及**几周前编译出来的同名二进制**。如果 `--skip-build` 直接从 `bin/` 取，
等于「把 bin/ 里躺着的东西装到生产上」，而没有任何东西会提醒你那份代码是旧的。

`install.sh` 在装之前会跑 `lib/verify_artifact.py`，逐个检查：

```
SERVICE            SIZE      FORMAT   FRESHNESS   NOTE
----------------------------------------------------------------------------------------
centralLogin       16.9M     ELF/amd64 OK
maple              16.0M     ELF/amd64 OK
...
admin              19.1M     ELF/amd64 OK
```

- **FORMAT** —— 是不是真的 Linux ELF（防止把 `.exe` 拷过来）
- **架构** —— 是不是目标 `GOARCH`（构建机 `GOARCH` 设错时 `go build` 不会报错）
- **FRESHNESS** —— 二进制是否早于 `src/` 下最新的源码

`--strict-fresh` 可以让过期二进制直接阻断部署：
实测拿 `bin/` 里那批旧包当交付物，12 个里 11 个被判为「旧17天」并返回非零码。

## 三条铁律

改这套东西之前必须知道，否则服务会以很难排查的方式起不来。

1. **安装目录名必须等于服务名，二进制文件名也必须等于服务名。**
   配置文件名不是配置里写死的，是从可执行文件路径推导的
   （`src/common/utils.go`：`filepath.Base(filepath.Dir(os.Args[0])) + ".json"`）。
   单元里的 `WorkingDirectory` 决定这个推导的结果。改路径时两个名字要一起改。

2. **`WorkingDirectory` 必须是服务自己的目录。**
   日志路径（`logPath`）是相对路径，pid 文件也写在当前工作目录。
   单元里这一行不能动。

3. **安装目录在 `/home` 下时，单元的 `ProtectHome` 必须是 `no`。**
   `ProtectHome=true` 会把 `/home`、`/root`、`/run/user` 整体挂成一个空 tmpfs。
   systemd 的执行顺序是 `chdir` → 搭 mount namespace → `execve`，
   前一步走的是真实 `/home` 所以能成功，之后二进制就"不见了"，
   于是 `execve` 返回 ENOENT，状态码是 **`203/EXEC`** —— 而且进程压根没起来，
   journal 里一个字都没有，极难定位。
   脚本已按安装根目录自动决定这个值（`lib/common.sh` 的 `protect_home_value`），
   可用 `SYSTEMD_PROTECT_HOME` 覆盖；手工改过单元文件时要留意这一条。

新增服务时要同时改：`src/<服务名>/`（带 build.sh 和 main.go）、
`bin/<服务名>/`、**`deploy/instances.conf`**。漏了最后一项不会被部署，
因为清单是唯一事实来源。

### status=203/EXEC 怎么查

`200+` 的退出码是 systemd 保留码，意思是「进程一次都没启动成功」，不是崩溃。
`Restart=always` 会把它刷成一串重启记录，很容易被误读成"起来又崩了"。

```bash
sudo journalctl -u centralsvc-maple -n 50 --no-pager   # 必须 sudo
#   不加 sudo 会显示 "-- No entries --"：失败原因是 systemd（root）打的，
#   普通用户看不到（提示 not seeing messages from other users）。
#   想免 sudo：sudo usermod -aG systemd-journal $USER，重新登录生效

systemctl cat centralsvc-maple | grep -E 'ProtectHome|ProtectSystem'
namei -l /home/fengyan/Server/centralService/bin/maple/maple   # 路径每一级权限
cd /home/fengyan/Server/centralService/bin/maple && ./maple --instid=0  # 绕开 systemd
```

业务日志另在 `tail -f <服务目录>/<服务名>.log`，stdout 在 `<服务名>.out.log`，
`healthcheck.sh` 会按这个顺序依次展示。

### 崩溃后服务一直起不来：pid 文件残留

日志每 3 秒刷一条 `WritePidFile fail, pidFile already Exist` 就是它（3 秒 = `RestartSec`）：

1. `src/base/init.go` 里 `WritePidFile()` 返回 false 就直接 `os.Exit(2)` —— 不是警告，是立即退出。
2. 崩溃 / panic / OOM / SIGKILL 时 `DelPidFile()` 不会执行（它只在 `ExitProgram()` 里，
   而 `ExitProgram` 仅由信号处理器触发），pid 文件必然残留。
3. systemd 拉起来 → 立刻 `exit 2` → 再拉起，无限循环，**服务一直不可用**。
   而且这次退出发生在 `StartListenKillSignal()` 之前，信号处理器没注册，
   连 `systemctl stop` 也清不掉，只能手工 `rm`。

单元里已经加了兜底（`ExecStartPre=-/bin/sh -c '...'`）：启动前检查 pid 文件里的进程
是否还活着（`/proc/<pid>`），死了或文件为空就删掉，活着的保留（防重复启动语义不丢）。
前缀的 `-` 表示这条失败也不阻断启动。

手工解锁：

```bash
sudo systemctl stop centralsvc-maple
rm -f /home/fengyan/Server/centralService/bin/maple/maple_0.pid
sudo systemctl start centralsvc-maple
```

`healthcheck.sh` 用 `kill -0` 判定，残留的 pid 文件会显示成 `stale` 并计入失败，不会误报成健康。

## 配置怎么来的

不维护 12 份配置模板。配置是三层叠加出来的：

```
bin/<服务名>/<服务名>.json      仓库里的基线，业务同学随时可改
        +
deploy.env                    统一的 MySQL / Redis 连接信息
        +
overrides.conf                跟机器环境相关的地址、端口
        =
/home/fengyan/Server/centralService/bin/<服务名>/<服务名>.json
```

好处是业务新增配置键不需要同步改模板，两边不会漂移。

渲染器顺带修掉了仓库里几处长期存在的键名不一致：

| 服务 | 问题 |
|---|---|
| `orderService` | MySQL 口令键是 `password`，别的是 `passwd` |
| `auction` / `orderService` | Redis 块叫 `redis`，别的是 `redisServer` |
| `auction` | Redis 用户键叫 `user`，别的是 `username` |
| `leaseServer` | 块名是 `Mysql` / `RedisServer`（首字母大写） |

### overrides 语法

```
<服务名>[:<文件名>]:<点分键路径>=<合法 JSON 值>
```

```
# 主配置（centralLogin.json）
router:routerClusterAdvertiseAddr="10.0.0.5:2061"
admin:mapleHttpAddr="10.0.0.5:9527"
admin:centralLoginCmdAddressList=["10.0.0.5:8999"]

# 副配置必须显式写文件名，否则会被当成主配置而静默失效
centralLogin/serverList.json:gameServerList.20001="10.0.0.9:20013"
```

### 漏配了会怎样：渲染器会告诉你

`bin/<服务>/<服务>.json` 是在开发机上写的，里面带着 `192.168.x.x`。
渲染只统一 MySQL / Redis 两处，其余跨服地址、对端地址全靠 overrides。
**漏配的地址会原样进到生产配置**，表现是服务能起但连不上对端，日志里还看不出是配置问题。

所以渲染完会自动扫一遍，分两档提示：

```
!! 高危：以下地址疑似开发机残留，必须确认后处理
   admin/admin.json              mapleHttpAddr              192.168.10.13:9527
   router/router.json            routerClusterAdvertiseAddr 192.168.10.133:2061
   centralLogin/serverList.json  gameServerList.20001       192.168.11.118:20013
   leaseServer/leaseServer.json  mapleHttpAddr              192.168.10.13:9527
   在 overrides.conf 里覆盖，形如：<服务名>:<键路径>="<生产地址>:<端口>"

.. 提示：以下指向本机。单机部署通常正确，分机部署需改
   admin/admin.json              centralLoginCmdAddressList[0]  localhost:8999
   maple/maple.json              addressForDebug            localhost:8989
   ...
```

判据是**有没有人显式配过**，不是「是不是内网」——生产内网本来就是 10.x/192.168.x。
`deploy.env` 和 `overrides.conf` 里声明过的值一律不告警。

正式部署建议加 `--strict-ips`，高危项没清干净就直接中止：

```bash
sudo ./deploy/install.sh --strict-ips
```

## 依赖的外部服务

本方案**不负责**安装这些，只负责连通性前置检查：

- **MySQL** —— 8 个服务各自一个库（login / maple / auction / transaction /
  allianceDB / lease / dropDB / crossDataDB），`install.sh` 按各自配置里的
  `db` 名自动建库导表
- **Redis** —— admin / router / queueServer / centralLogin / orderService /
  crossTeamServer / auction / leaseServer

## 常用运维命令

日志都在服务自己的目录里（`<安装根>/<服务名>/`）：

| 文件 | 内容 | 轮转 |
|---|---|---|
| `<服务名>.log` | 业务日志 | 程序内 lumberjack 按 `logRotateSize` 滚动 |
| `<服务名>.out.log` | 进程 stdout/stderr（启动阶段报错看这个） | logrotate |

```bash
systemctl status centralsvc-maple                    # 单个服务状态
tail -f /home/fengyan/Server/centralService/bin/maple/maple.out.log   # 启动阶段的问题看这里
tail -f /home/fengyan/Server/centralService/bin/maple/maple.log       # 业务日志

# 缺省 LOG_STDOUT_MODE=file，stdout 不进 journald；若改成 journal 则用：
journalctl -u centralsvc-maple -f

./deploy/healthcheck.sh                     # 全量体检，有问题直接列出
./deploy/healthcheck.sh maple router        # 只查指定服务

./deploy/upgrade.sh                         # 编译 + 逐个升级 + 失败自动回滚
./deploy/upgrade.sh --no-build              # 用 dist/ 下已有二进制升级
./deploy/install.sh --skip-build            # 只改配置并重启（不重新编译）

./deploy/uninstall.sh                       # 停服务 + 删单元 + 删程序，保留数据
./deploy/uninstall.sh --purge               # 连数据和回滚备份一起删
```

## 排障

| 现象 | 大概率原因 |
|---|---|
| 服务反复重启，日志报找不到配置文件 | 目录名或二进制名和服务名不一致 |
| 端口探活不通但进程还在 | 中间件连不上，先手工验证 MySQL / Redis 连通性 |
| 改了 `overrides.conf` 没生效 | 忘了 `--skip-build` 重跑，或服务名/文件名写错被静默忽略 |
| pprof 端口被外部访问到 | `addressForDebug` 还是 `0.0.0.0`，生产应在 overrides 里改成 `127.0.0.1` |

健康检查的 pid 判定以 `$INSTALL_ROOT/<服务名>/<服务名>_0.pid` 为准
（`--instid=0` 由单元的 `ExecStart` 传入）。

## 本地自测

```bash
./deploy/selftest.sh
```

覆盖清单解析、命名一致性、模板渲染、配置渲染端到端、game.sh 语法。
不碰系统、不需要 root，开发机上随时可以跑。

## 与旧脚本的关系

- `bin/start_all.sh`、`bin/stop_all.sh`、`bin/check_all.sh`、`bin/*/game.sh`
  是部署 systemd 之前的手工运维方式，仍然可用（`game.sh` 的进程名判断已修正为
  `ps -p -o comm=`，原来的 `ps -A` + awk 在 Linux 上会取到 TIME 列而误判）。
  上了 systemd 后请优先用 `systemctl`。
- `bin/replace_db_config.py` 已被 `deploy/lib/render_config.py` 取代，
  后者覆盖了更多键名变体，且能限定作用文件。
- `bin/build_all_server.sh`（引用了重命名后已不存在的 `src/adminServer/`）已移除，
  统一用根目录的 `build_all.sh` 或 `deploy/build_linux.sh`。
