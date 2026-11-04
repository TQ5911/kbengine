# 中心服统一启动日志 TAG 与告警接入

## 1. 这套东西解决什么

线上 12 个中心服由 systemd 托管（`Restart=always`）。服务挂掉后会被自动拉起，
但"被拉起了"这个事实原先只能靠人工翻日志发现 —— 每个服务的启动日志措辞都不一样
（`server is running`、各种中文串），没法写一条通用告警规则。

现在所有中心服在启动/失败/退出时会输出**同一格式的一行日志**，共用同一个 TAG：

```
CENTRALSVC_BOOT
```

采集侧匹配这一个词就能覆盖全部服务，不用逐服务配置。

## 2. 一行日志长什么样

```
2026-11-02T17:05:12.345+0800 INFO CENTRALSVC_BOOT phase=ready service=maple serverName=mapleServer serverId=1 instid=0 pid=12345 host=ip-172-16-41-49 boot=3 prev=unclean
```

字段顺序固定（`serverName`/`serverId` 只在配置读到后出现），可以直接写正则。

| 字段 | 含义 |
| --- | --- |
| `phase` | `starting` / `ready` / `failed` / `exit`，见第 3 节 |
| `service` | 服务名，取**可执行文件所在目录名**，与 `deploy/instances.conf` 的 `name` 列一致 |
| `serverName` | 配置里的 `serverName`（如 `mapleServer`） |
| `serverId` | 配置里的 `serverId` |
| `instid` | 启动参数 `--instid`，systemd 下固定为 `0` |
| `pid` | 进程号 |
| `host` | 主机名，多机部署用来区分机器 |
| `boot` | 本机本实例累计第几次启动，`>1` 即发生过重启 |
| `prev` | 上次退出的干净程度：`clean` / `unclean` / `none`（首次启动） |
| `reason` | 仅 `failed` / `exit` 有，失败原因短名 |
| `code` | 仅 `exit` 有，退出码 |

## 3. 四个 phase

| phase | 触发时机 | 用途 |
| --- | --- | --- |
| `starting` | `main` 进入初始化流程的最开头（`centralLogin` / `queueServer` 是 `main` 第一行，其余是 `base.Init` 开头） | 证明"进程确实被拉起来了"。配置完全丢失时，这是唯一能看到的行 |
| `ready` | TCP 类：所有监听端口 `Listen` 成功；HTTP 类：进入 HTTP 服务循环 | **告警主匹配点**，代表服务真的可用 |
| `failed` | 任一初始化阶段失败 | 服务起不来，比"重启了"更需要处理 |
| `exit` | 进程退出 | 和下一次 `starting` 配对，能算出"挂了多久才被拉起" |

### 两类服务的 ready 判定不一样

中心服有两种形态，`common.Run` 对它们走不同分支：

| 形态 | 服务 | ready 判定 |
| --- | --- | --- |
| TCP 类 | `centralLogin` `router` `auction` `admin` `allianceService` `leaseServer` `dropServer` `orderService` `crossDataServer` `crossTeamServer` | `GetServices()` 返回端口清单，全部 `Listen` 成功才打 `ready`；任一失败打 `failed`（带 `addr=` / `err=`） |
| HTTP 类 | `maple` `queueServer` | `GetServices()` 返回 `nil`，`Start()` 自己同步阻塞在 `ListenAndServe` 上。因此 `Start` 跑在独立协程里，端口绑定成功、进入服务循环后打 `ready`；绑定失败会 panic，由协程内 recover 转成 `failed` |

`failed` 的 `reason` 取值：

| reason | 含义 |
| --- | --- |
| `init_config` | 读不到 `<服务名>.json`，或工作目录不对 |
| `init_log` | `logPath` 无效 / 日志级别配置非法 |
| `write_pid_file` | pid 文件已存在（多半是上一个进程没清干净） |
| `init_report` | 企微上报初始化失败 |
| `init_common` | 公共初始化失败 |
| `app_init_return_nil` | 服务的 NewXxxApp 返回 nil，配置校验没过 |
| `app_is_nil` / `app_is_typed_nil` | `common.Run` 拿到的 app 是 nil / typed-nil（防御分支） |
| `listen` | 端口监听失败，附带 `addr=` / `err=` / `fail_count=` |
| `start_returned` | HTTP 类服务的 `Start()` 直接返回了，没进入服务循环 |
| `panic` | panic。附带 `stage=`：`main`（base.Init 之前）/ `start`（HTTP 类启动）/ `run`（运行期） |

`exit` 的 `reason` 取值：`sigterm` / `sigint` / `sighup` / `sigquit` / `panic` / `run_returned` / `unspecified`。

> `centralLogin` 和 `queueServer` 会在 `base.Init` 之前读 `serverList.json`，读不到直接
> `log.Panicf`。为了不让这种"拉起即崩"变成日志里一片空白，它们的 `main` 第一行加了
> `defer appLog.BootFatalRecover()`，panic 时同样输出 `starting` + `failed` + `exit` 三条。

## 4. 日志落在哪

同一行会写三处中的两处，采集走任一路都能匹配：

| 位置 | 内容 | 何时有 |
| --- | --- | --- |
| `<安装根>/<服务名>/<服务名>.log` | 业务日志（lumberjack 写） | `init_log` 成功之后的所有 phase |
| `<安装根>/<服务名>/<服务名>.out.log` | stdout | 全部 phase（`LOG_STDOUT_MODE=file` 时） |
| `journalctl -u centralsvc-<服务名>` | stdout | 全部 phase（`LOG_STDOUT_MODE=journal` 时） |

`starting` 发生在日志系统初始化之前，所以**只走 stdout**，不在业务日志文件里。
这是刻意的：配置读不到时业务日志根本没建立，只能靠 stdout。

## 5. 告警规则建议

按优先级从高到低，四条就能覆盖绝大多数故障：

### P1 服务起不来

```
CENTRALSVC_BOOT .*phase=failed
```

任意服务出现 `failed` 立即告警，把 `reason=` 一起带到通知里，能直接定位是配置、
端口还是依赖问题。

### P1 崩溃后被拉起（核心场景）

```
CENTRALSVC_BOOT .*phase=ready .*prev=unclean
```

`prev=unclean` 表示**上一次进程没走优雅退出** —— panic、OOM、被 `SIGKILL`，
或者上次也是启动失败。这是"中心服挂了又被拉起来"最准确的信号，比只看
`phase=ready` 干净得多（正常 `systemctl restart` 的 `prev` 是 `clean`）。

### P2 反复重启

统计时间窗口内同一 `service` 出现的 `phase=ready` 次数，例如 10 分钟内 ≥3 次。
配合 `boot=` 字段可直接看出累计重启次数，防止"起来又挂"的抖动被单条告警淹没。

### P2 异常退出码

```
CENTRALSVC_BOOT .*phase=exit .*code=(?!0\b)(?!130\b)\d+
```

`code=0`（正常停止）和 `code=130`（`SIGINT`）是预期内的，其余都值得看一眼。

## 6. 现场排查命令

```bash
# 看某个服务最近的启动记录（业务日志 + stdout 两路都在，sort -u 去重）
grep -h CENTRALSVC_BOOT <安装根>/maple/maple.log <安装根>/maple/maple.out.log | sort -u | tail -20

# journal 模式
sudo journalctl -u centralsvc-maple --since "1 hour ago" | grep CENTRALSVC_BOOT

# 全量：谁在重启、第几次、上次干不干净
grep -h CENTRALSVC_BOOT <安装根>/*/*.log | grep 'phase=ready' | sort -u | \
  awk '{for(i=1;i<=NF;i++) if($i ~ /^(service|boot|prev)=/) printf "%s ", $i; print ""}'

# 只看启动失败
grep -h CENTRALSVC_BOOT <安装根>/*/*.log | grep 'phase=failed' | sort -u
```

`fengyan` 不在 `adm` 组，查 journal 必须带 `sudo`，否则只会输出 `-- No entries --`。

## 7. 可调项

| 环境变量 | 作用 | 默认 |
| --- | --- | --- |
| `CENTRALSVC_BOOT_TAG` | 覆盖 TAG 名，灰度期可单独抓某批服务 | `CENTRALSVC_BOOT` |
| `CENTRALSVC_SERVICE` | 覆盖 `service` 字段。仅当二进制不在 `<服务名>/` 目录下才需要 | 按可执行文件目录名推导 |

改 systemd 环境变量：在 `deploy/deploy.env` 里加 `Environment=` 或直接改单元后
`systemctl daemon-reload`。

## 8. 状态文件

`boot` / `prev` 依赖服务工作目录下两个小文件（与 pid 文件同目录）：

| 文件 | 作用 |
| --- | --- |
| `<服务名>_<instid>.boot` | 累计启动次数，每次启动自增 |
| `<服务名>_<instid>.clean` | 优雅退出标记，被下次启动读取后立即删除 |

- 两个文件读写失败都**不会**影响服务启动，只会让 `boot=0` 或 `prev` 退化成保守值。
- 已加入 `.gitignore`（`*.boot` / `*.clean`），不会污染版本库。
- 想重置"第几次启动"的计数，停服后删掉 `.boot` 文件即可。

`clean` 标记的写入时机：只有 `ExitProgram(0)` / `ExitProgram(130)` 才会写。
`panic`、OOM、`SIGKILL` 都到不了那里，因此下次启动的 `prev` 必然是 `unclean`。

## 9. 实现位置

| 文件 | 职责 |
| --- | --- |
| `src/appLog/BootTag.go` | TAG 常量、字段组装、双路输出、boot/clean 状态文件、main 级 panic 兜底 |
| `src/base/init.go` | `starting` 打点；各初始化阶段失败时打 `failed`；`Run` 返回时补 `exit` |
| `src/common/App.go` | TCP 类：收集所有端口的 `Listen` 结果，全成功才打 `ready`；HTTP 类：`runHttpOnlyApp` 独立协程启动并判定 `ready` |
| `src/common/Pidfile.go` | `exit` 打点、`clean` 标记写入、信号名传递 |
| `src/queueServer/main.go`、`src/centralLogin/main.go` | `main` 第一行的 panic 兜底，覆盖 `base.Init` 之前的前置配置读取 |
| `src/appLog/BootTag_test.go` | 生命周期回归测试（`go test ./src/appLog/ -run TestBootTag`） |

## 10. 变更影响面

- 只在启动/退出路径加日志，不改变任何服务原有的启动顺序、监听方式与退出码。
- `common.Run` 里 `GetServices()` 的调用时机从「`Start()` 之后」提前到「`Start()` 之前」。
  各服务的 `GetServices()` 都只读全局配置、不依赖 `Start()` 的副作用，已逐个确认。
- `ExitProgram` 的 `reason` 是可变参数，原有的 `ExitProgram(1)` 调用无需改动。
- 启动路径多两个文件读写（`.boot` / `.clean`），失败时静默降级，不影响服务。
- HTTP 类服务的 `ready` 判定引入 300ms 观察窗口，即这两个服务启动多 0.3 秒才打 `ready`，
  不影响对外提供服务的时间（端口在此之前已绑定）。
