# `install.sh` 到底干了什么

一次执行就完成 **编译 → 渲染配置 → 铺文件 → 建库导表 → 装 systemd 单元 → 启动 → 健康检查**。
两条路径共用前三步（编译、渲染），之后分叉：

- **本地模式**：在本机上直接安装并交由本机 systemd 托管。
- **Ansible 模式**：在开发机上编译+渲染，通过 Ansible 推到远程部署机执行。

---

## 一、两种模式的流程对照

```
本地模式（sudo ./deploy/install.sh）
  1/8 前置检查  →  2/8 编译  →  3/8 渲染配置
    →  4/8 安装文件  →  5/8 建库导表  →  6/8 装 systemd 单元
    →  日志轮转  →  [nginx 反代]  →  7/8 启动服务  →  健康检查

Ansible 模式（./deploy/install.sh --ansible）
  1/8 前置检查  →  2/8 编译  →  3/8 渲染配置
    →  Ansible 远程部署（连通性 → 建用户 → 建目录 → 推文件 → 改属主
                        → 推单元 → 建库导表 → 重启 → 远程健康检查）
    →  健康检查
```

差异的本质：**在本机做不了的动作都挪到远程执行**。两条路径的步骤顺序刻意保持一致，
否则产物会静默分叉（比如远程少了 `data/`）。

---

## 二、输入：它读哪些东西

| 输入 | 路径 | 作用 |
|---|---|---|
| 环境变量 | `deploy/deploy.env`（`-e`） | MySQL/Redis 连接、安装根目录、运行用户、日志方式 |
| 逐服务覆盖 | `deploy/overrides.conf`（`-o`） | 覆盖与机器环境相关的地址/端口 |
| 服务清单 | `deploy/instances.conf`（`-i`） | **编排的唯一事实来源**：12 个服务、探活端口、是否建库、启动顺序 |
| 配置基线 | `<仓库>/bin`（`-b`） | 各服务 `*.json`、`*.sql`、证书、`up.sh`、共享 `data/` |
| 二进制来源 | `<仓库>/dist`（`-d`），没有则退回 `bin/` | 装的就是这里的东西 |
| 单元模板 | `deploy/templates/*.template` | systemd 单元、logrotate、nginx 反代 |

两个目录**不能混用**（README 有详解）：`bin/` 是配置基线 + 本地杂项，`dist/` 只有 `build_linux.sh`
写进去的交付产物。`--skip-build` 从 `bin/` 取等于「把几周前的旧包装到生产上」。

---

## 三、逐步骤拆解

### 1/8 前置检查 `step_preflight`

| 检查项 | 本地模式 | Ansible 模式 |
|---|---|---|
| 工具链 | `systemctl` `install` `go` `python3` | `ansible` `rsync` `python3` |
| `deploy.env` 存在且权限非 644+（含口令要 600） | ✅ | ✅ |
| 配置基线目录存在 | ✅ | ✅ |
| 监听端口无冲突 | ✅ | 跳过（端口在远程） |
| 交付二进制校验（ELF/架构/新鲜度） | `--skip-build` 时 | `--skip-build` 时 |

Ansible 模式在这里额外做了一件关键的事：**把所有值为空的 `ANSIBLE_*` 环境变量 unset**。
ansible 对 path 型配置（`ANSIBLE_INVENTORY`、`*_PASSWORD_FILE`）拿到空串会 `unfrackpath('')`
解析成当前目录，然后把 `deploy/` 当 inventory/口令脚本去执行，刷出上百行 WARNING 甚至
`[Errno 13] Permission denied`。unset 之后再重新赋空值（赋空值不带 export 属性，不会重踩坑），
因为脚本是 `set -u`，后面引用未声明的变量会直接 "unbound variable"。

同时**决定了安装根目录**：Ansible 模式取 `ANSIBLE_REMOTE_PREFIX`，本地模式取 `INSTALL_ROOT`。
这两个必须分开——远程路径在本机可能压根不存在（比如 `/home/fengyan/...` 属于另一个用户），
拿它当本地目录 `mkdir` 直接 Permission denied。

默认值的取法：命令行 > `deploy.env` > 内置默认。当前内置默认：

```
INSTALL_ROOT / ANSIBLE_REMOTE_PREFIX = /home/fengyan/Server/centralService/bin
UNIT_PREFIX    = centralsvc        → 单元名 centralsvc-<服务名>.service
SERVICE_USER   = fengyan           → 运行用户，与部署账号一致
RESTART_SEC    = 3                 → 挂了 3 秒后拉起
LOG_STDOUT_MODE= file              → stdout 追加到服务目录
LOG_ROTATE_KEEP= 7
```

### 2/8 编译 `step_build`

调 `build_linux.sh --out-dir <dist>`（`CGO_ENABLED=0 GOOS=linux GOARCH=amd64`），
产出到 `dist/`，然后跑 `verify_artifact.py` 校验：

- **格式**：必须是 ELF，不能是 Windows 的 `.exe`（拷错文件时最常见）
- **架构**：必须匹配目标 `GOARCH`（构建机设错时 `go build` 不会报错）
- **新鲜度**：二进制必须比 `src/` 下最新源码新（`--strict-fresh` 可直接阻断部署）

`--skip-build` 时跳过编译但仍走一遍校验——不编译目标机时，装的是别人传过来的二进制，必须先验。

### 3/8 渲染配置 `step_render`

调 `render_config.py`，三层叠加：

```
bin/<服务名>/<服务名>.json   仓库基线
      + deploy.env           统一注入 MySQL / Redis 连接信息
      + overrides.conf       逐键覆盖与机器环境相关的地址、端口
      = <staging>/<服务名>/<服务名>.json
```

顺带修掉仓库里长期存在的键名不一致：`mysql`/`Mysql`、`passwd`/`password`、
`redisServer`/`redis`、`username`/`user` 等异名会自动归一。

`--strict-ips` 会扫描渲染结果里是否还有 `192.168.x` / `10.x` / `172.16-31.x`
的开发机残留地址，有就直接中止——漏配的地址能让服务起来但连不上对端，且日志里看不出是配置问题。

渲染结果落到 **staging**：本地模式是 `$PREFIX/.staging.$$`（与目标同盘，`cp -a` 不会跨 fs 半途失败），
Ansible 模式是本机 `mktemp -d`（远程路径本机可能不存在）。

Ansible 模式在这一步还会 **补齐完整目录镜像**（`stage_service_files`）：二进制、`*.sql`、`*.pem`、
`*.crt`、`up.sh`/`down.sh`/`game.sh`、共享 `data/`。这一步不能省——
`ansible_push_staging` 用的是 `delete=yes`，staging 里只有 JSON 的话，
远程的二进制会被当成「多余文件」删掉，服务随后必然起不来。

### 4/8 安装文件 `step_install`（本地模式）

每个服务一个目录，**目录名 = 服务名，二进制名 = 服务名**（程序用「可执行文件所在目录名」推导配置
文件名，`filepath.Base(filepath.Dir(os.Args[0])) + ".json"`，名字不对就读不到配置）：

```
<PREFIX>/<服务名>/
  ├── <服务名>          0755  二进制，来自 dist/
  ├── <服务名>.json     0640  渲染后的配置
  ├── *.sql *.pem *.crt 0640
  ├── up.sh game.sh     0750
  └── chown -R SERVICE_USER:SERVICE_GROUP
```

另外安装共享数据 `<PREFIX>/data/`，`centralLogin`/`auction`/`orderService`/`allianceService`/
`leaseServer` 以 `../data/` 相对路径读取。

Ansible 模式对应的动作：`ansible_ensure_user` → `ansible_mkdir` → `ansible_push_staging`
（rsync 逐服务同步）→ `ansible_chown`。最后一步不能省——synchronize 推上去的属主是 `ANSIBLE_USER`，
但进程以 `SERVICE_USER` 运行，配置是 `0640`，属主不对就读不到。

### 5/8 建库导表 `step_db_init`

只对 `instances.conf` 里 `db_init=yes` 的服务执行 `cd <PREFIX>/<服务名> && sh ./up.sh`。
失败时只 warn 不中断（**表已存在时失败属正常**，需要人工确认）。`--no-db-init` 可整体跳过。

### 6/8 装 systemd 单元 `step_units`

按 `templates/centralsvc.service.template` 给每个服务渲染一份
`/etc/systemd/system/centralsvc-<服务名>.service`，然后 `daemon-reload`。几个关键设定：

| 设定 | 值 | 为什么不能动 |
|---|---|---|
| `WorkingDirectory` | `<PREFIX>/<服务名>` | 配置按 CWD 推导、日志是相对路径、pid 写在 CWD |
| `ExecStart` | `.../<服务名>/<服务名> --instid=0` | 二进制名必须等于目录名 |
| `ExecStartPre` | 清理残留 pid 文件 | 崩溃后 pid 文件残留会让服务永远起不来，见下 |
| `ProtectHome` | 自动决定 | 安装目录在 `/home` 下时必须是 `no`，否则 `203/EXEC` |
| `StandardOutput` | `append:<服务目录>/<服务名>.out.log` | 用 append 而不是 file，重启不会抹掉上次的退出原因 |
| `Restart` / `RestartSec` | `always` / `3` | 挂了自动拉起 |
| `StartLimitIntervalSec` | `0` | 不限流，永不进入 failed 状态 |
| `User`/`Group` | `fengyan` | 与部署账号一致，避免属主与运行身份不一致 |

**两个带血泪的坑，都已内置处理：**

1. **`ProtectHome`**：`true` 会把 `/home`、`/root`、`/run/user` 挂成空 tmpfs。systemd 的顺序是
   `chdir` → 搭 mount namespace → `execve`，chdir 走的是真实 `/home` 所以能成功，
   之后二进制"不见了" → `execve` ENOENT → **`status=203/EXEC`**，journal 里一个字都没有。
   现在由 `protect_home_value()` 按安装根目录自动决定（`/home`、`/root`、`/run/user` → `no`），
   可用 `SYSTEMD_PROTECT_HOME` 覆盖。

2. **`ExecStartPre` 清理 pid 文件**：崩溃/panic/OOM/SIGKILL 时 `DelPidFile()` 不会执行，
   pid 文件残留 → 下次启动 `WritePidFile()` 发现文件存在直接 `os.Exit(2)`
   （`src/base/init.go:72-76`）→ systemd 拉起来立刻又退出，每 3 秒一轮，服务一直不可用。
   而且那次退出发生在注册信号处理器之前，连 `systemctl stop` 都清不掉。
   现在启动前检查 `/proc/<pid>` 是否还在，**死了才删，活着的保留**（防重复启动语义不丢）。

### 日志轮转 `step_logrotate`

写 `/etc/logrotate.d/centralsvc`，覆盖 `<PREFIX>/*/*.log`，保留 `LOG_ROTATE_KEEP` 份。
必须用 **`copytruncate`**——systemd 一直持有 `out.log` 的 fd，普通轮转后进程会往已删除的
inode 里继续写。lumberjack 自己不限制备份份数与天数，不靠 logrotate 兜底迟早撑爆磁盘。

### nginx 反代 `step_nginx`（可选，`--install-nginx`）

从渲染后的 `admin.json` 读出 GMT / HTTP / SDK 端口，生成
`/etc/nginx/conf.d/centralsvc-admin.conf`（http/https server 块）。只生成不 reload，需要自己挂进主配置。

### 7/8 启动服务 `step_start`

按 `instances.conf` 的**行顺序**逐个 `systemctl enable` + `restart`。
单个失败时调 `explain_unit_failure` 解读退出码（`200+` 是 systemd 保留码 = 进程一次都没起来，
不是崩溃），并 tail 服务目录里的 `out.log`。有任一失败就 `die` 中断。

### 健康检查 `step_verify`

调 `healthcheck.sh`，逐服务检查 **systemd 单元状态 + pid 文件里的进程是否活着 + 探活端口**。
pid 判定用 `kill -0`，残留的 pid 文件会显示成 `stale` 并计入失败，不会误报成健康。

Ansible 模式下还会先把 `deploy/` 同步到远程再在远程跑一次 `healthcheck.sh`——
注意必须用**远程的** `deploy.env` 路径，`$ENV_FILE` 是本机路径，远程不存在。

---

## 四、它到底改了哪些地方

**目标机上：**

```
<PREFIX>/<服务名>/{<服务名>, <服务名>.json, *.sql, *.pem, *.crt, up.sh, game.sh}
<PREFIX>/data/
/etc/systemd/system/centralsvc-<服务名>.service       ×12
/etc/logrotate.d/centralsvc
/etc/nginx/conf.d/centralsvc-admin.conf              (--install-nginx 时)
用户/用户组 SERVICE_USER:SERVICE_GROUP                (不存在才创建)
```

运行的 systemd 单元会被 `enable` + `restart`，MySQL 里会建成各服务的表。

**它不做的事：** 不安装 MySQL / Redis / nginx / Go / systemd 本身，不配防火墙，不做回滚
（回滚是 `upgrade.sh` 的活），不清理旧目录。

---

## 五、幂等性与副作用

| 步骤 | 重复跑 | 说明 |
|---|---|---|
| 前置检查、编译、渲染 | 安全 | 渲染每次重来 |
| 安装文件 | 安全 | 覆盖写，属主会被重置成 `SERVICE_USER` |
| 建库导表 | **有副作用** | 重复跑 `up.sh`，表已存在时返回失败（只 warn，需人工看） |
| systemd 单元 | 安全 | 覆盖写 + `daemon-reload` |
| 启动 | 安全 | 每个服务都会 `restart` |
| 健康检查 | 只读 | |

所以 `--skip-build` 重跑是「只改配置并重启」的标准操作；但**不想重跑建库就加 `--no-db-init`**。

---

## 六、常用组合

```bash
./deploy/install.sh --ansible --dry-run        # 先演练（Ansible 模式仍会真连一次 SSH ping）
./deploy/install.sh --ansible                  # 全新部署
./deploy/install.sh --ansible --skip-build     # 只改配置/单元并重启 ← 日常最常用
./deploy/install.sh --ansible --strict-ips --strict-fresh --skip-build
                                               # 带卡口的部署：残留内网地址、过期二进制都会中止
./deploy/install.sh --ansible --no-start       # 只铺文件不启动
sudo ./deploy/install.sh                       # 本地模式（需要 root）
```

> `--dry-run` 在本地模式下仍会先 `require_root`，因为它在 `main()` 里排在前置检查之前。

---

## 七、只装单元：`install-systemd.sh`

`install.sh` 的第 6/8 步（装 systemd 单元）可以单独拿出来跑，适用于
**远程起服文件已经在位、只是单元要重装/刷新**的场景——不用再走编译、渲染、推文件、建库。

```bash
./deploy/install-systemd.sh --only maple              # 单服务
./deploy/install-systemd.sh                            # 全部
./deploy/install-systemd.sh --only maple --check       # 演练
./deploy/install-systemd.sh --only maple --no-restart  # 只落单元
```

它是 `ansible/systemd-only.yml` 的薄封装：读 `deploy.env` 与 `instances.conf`，
生成变量 JSON 后调 `ansible-playbook`。playbook 本身只做：

| 步骤 | 标签 | 说明 |
|---|---|---|
| 校验远程二进制与 `*.json` 在不在 | `validate` | 不在就失败，**不做文件分发** |
| 确保运行用户/组存在 | `user` | 单元里 `User=` 必须是已存在的用户 |
| 渲染并推送单元 | `unit` | 复用同一份 `@KEY@` 模板 |
| `daemon-reload` | `reload` | 仅单元有变化时 |
| `enable` + 应用状态 | `service` | 默认 `restarted` |
| 等探活端口 / 打印状态 | `verify` / `status` | 可选 |

单元里已有 `ExecStartPre` 负责清理残留 pid 文件，所以崩溃过的机器 `restart` 也不会
卡在 `WritePidFile fail` 的循环里。

## 八、排障入口

```bash
tail -f <PREFIX>/<服务名>/<服务名>.out.log      # 进程的 stdout/stderr，启动阶段的问题在这
tail -f <PREFIX>/<服务名>/<服务名>.log          # 业务日志
sudo journalctl -u centralsvc-<服务名> -n 50 --no-pager   # 必须 sudo
./deploy/healthcheck.sh                        # 全量体检
```

`journalctl` 不加 sudo 会显示 `-- No entries --`——失败原因是 systemd（root）打的，
普通用户看不到。想免 sudo：`sudo usermod -aG systemd-journal $USER`（重新登录生效）。

`status=203/EXEC`（进程没起来）与「pid 文件残留导致每 3 秒重启一轮」的排查详见 README。
