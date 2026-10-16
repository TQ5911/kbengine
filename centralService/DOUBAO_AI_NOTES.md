# DOUBAO_AI_NOTES.md
> 本文件为豆包 AI 对本项目的首轮架构理解笔记，基于只读代码走查生成，后续随任务迭代补充。
> 技术栈：Go 1.21 游戏中心（中心服）微服务群；自研 trpc RPC（裸 TCP + protobuf）；MySQL + Redis；viper 配置 + fsnotify 热更；systemd 部署。

## 1. 项目简介
一句话描述项目：
游戏中心服务器（centralService），一组用 Go 写的独立微服务，承载客户端登录接入、排队限流、游戏服间路由转发、大区/地图数据、拍卖行、订单支付、公会、装备租赁、掉落结算、跨服数据与跨服组队，以及 GMT 后台；游戏服（外部进程）通过自研 trpc 长连接接入这些中心服。

## 2. 模块划分
> 只写顶层模块，`src/` 下每个目录一个条目。

- **base**：服务启动骨架。`base.Init(config, serverInstance)` 统一完成配置加载、日志初始化、serverName/serverId 设置、pid 文件写入、信号监听、企微上报初始化，最后 `common.Run(app)`。
- **common**：公共库。`IApp` 接口与 TCP listener 主循环、Redis 连接池、配置读取（按可执行文件目录名推导 `<服务名>.json`）、游戏服分组数据缓存（每 5s 拉 maple HTTP）、并发 map、任务队列/协程池、企微上报。
- **trpc**：自研 RPC 框架。RpcChannel 负责粘包拆包与方法分发，ServiceDesc/MethodDesc 描述服务；wire 格式 `[4字节LE长度][2字节LE methodIndex][protobuf body]`。
- **appLog**：zap + lumberjack 滚动日志封装。
- **yidunSDK**：网易易盾（验证码/认证）SDK 封装，被 centralLogin 等接入。
- **centralLogin**（端口 2020/2030/8999）：登录网关。两个 TCP 监听：客户端认证连接 + 游戏服连接；校验登录 token（内存在线表 + Redis `login:accountinfo:{type}:{name}` 兜底），账号库 account/account_characters，支持踢人、查账号所在游戏服。
- **queueServer**（4396）：排队与限流。按游戏服维护普通队列/VIP 队列，`golang.org/x/time/rate` 令牌桶限流，参数 maxOnlineNum/limitPerSecond 热更。
- **router**（2060/2061）：游戏服间消息路由转发。按 serverId+componentId 索引在线游戏服连接；集群模式下多 router 节点互联（routerCluster 服务），经 Redis 同步全局 serverId→routerId 表，支持跨节点转发与流量统计。
- **maple**（9527）：大区/地图数据服务。纯 HTTP，无 TCP trpc 监听；是所有服务查询"游戏服分组(server_group)/合服根服映射"的数据源，接口 `/getAllServer`、`/getAllMergeServer`；也负责大区增删、合服导入导出。
- **auction**（2010）：拍卖行。trpc 接游戏服，MySQL 持久化，业务 JSON 配置文件 fsnotify 热更，含 GM 购买拦截计数。
- **orderService**（2011/8888）：订单与支付。trpc 接游戏服 + HTTP 支付回调（PayNotifyApi/Secret），Redis + MySQL。
- **allianceService**（2150）：公会。trpc 接游戏服，内存加载公会数据后提供服务。
- **leaseServer**（2015）：装备租赁。按逻辑组（来自 maple 的 server_group）隔离货架，btree/heap 做索引与到期，交易类/查询类分别限流。
- **dropServer**（2120）：掉落结算。trpc 接游戏服，三表内存缓存（cache-aside + write-through）+ 物品分布式锁。
- **crossDataServer**（2140）：跨服数据。trpc 接游戏服，承载跨服公会数据、城战数据。
- **crossTeamServer**（2016）：跨服队伍。trpc 接游戏服，worker 池 dispatcher 分发，匹配池/聊天缓冲，讨伐玩法全局限流与进行中计数。
- **admin**（8080/8081/2040/2050/2051）：GMT 后台。trpc 接游戏服挂起命令（按 key 等回执），对外用 gRPC + grpc-web（2050 入口），另有 HTTP API / HTTP SDK 通道。

## 3. 核心业务规则（重点！AI写代码必须遵守）
> 以下为代码中直接观察到的约定。

1. **命名铁律**：安装目录名 = 可执行文件名 = 服务名 = 配置文件名。`common.GetConfig` 用 `filepath.Base(filepath.Dir(os.Args[0])) + ".json"` 推导配置路径，改目录名/二进制名必须同步改 `deploy/instances.conf` 与 `bin/<服务名>/`。
2. **trpc 协议**：服务端按 `ServiceDesc.Methods[methodIndex]` 分发；新增方法就是在 `.proto` 里加消息并在 `.rpc.go` 注册 handler，methodIndex 由方法切片顺序决定，**插入/删除方法会改变索引，已上线协议不得调整方法顺序**。
3. **游戏服分组数据来源唯一**：各服务不直接维护分组，配置里写了 `mapleHttpAddr` 即由 `common/gameServerData` 每 5s 拉取 maple `/getAllServer`、`/getAllMergeServer`，atomic.Value 整体替换快照，读路径无锁；逻辑组 0 为未知组（未接入 maple 的服），leaseServer 等服务对组 0 有特殊拒绝逻辑。
4. **centralLogin 登录态双层**：客户端登录成功后内存 map（accountType-accountName → LoginClientService）是第一身份，Redis hash `login:accountinfo:{type}:{name}`（TTL 3600s）是游戏服重连校验的兜底；踢人必须同时断开连接、删内存表、删 Redis key，否则旧 token 会被 Redis 兜底命中。
5. **router 路由表约束**：同一 serverId 的所有 componentId 必须注册在同一 router 上；跨节点转发只保证"帧写到对端 router 的 socket"，不保证对端游戏服已消费。
6. **服务自描述启动**：每个服务 main.go 最后调 `base.Init(&XxxConfig, func() common.IApp { return NewXxxApp() })`，新增服务必须带 `main.go` + `build.sh` + `bin/<服务名>/<服务名>.json` + 登记 `deploy/instances.conf`。

## 4. 数据结构关键说明
> 只写核心结构体。

- **common.IApp**：`Start() / Stop() / NewService(net.Conn, serviceType uint8) trpc.IServerEndPoint / GetServices() []*ServiceInfo`。每个服务的 `XxxApp` 内嵌 `common.App` 实现它。
- **common.ServiceInfo**：`{ServiceType uint8, ServiceName string, ServiceListenAddr string}`，一个服务可以监听多个端口（centralLogin 两个、admin 五个）。
- **trpc.RpcChannel**：一条 TCP 连接一个 channel，持有 uuid、net.Conn、当前正在解析的 RpcRequest；`CallMethod` 序列化 proto 并按 wire 格式写出。
- **trpc.ServerEndPoint / IServerEndPoint**：每连接一个服务实例，`Serve()` 即 `channel.Process()` 阻塞读循环，`OnLoseConnection()` 做清理。
- **服务内常见 map 三件套**：`gameServers`（key→服务实例）、`channelToHost`（channelUUID→实例，断连时 O(1) 定位）、对应的 RWMutex。
- **centralLogin.AccountLoginInfo**：Redis hash 结构 `{token, channelId, userId, otherJsonData}`。

## 5. 部署 & 服务信息
- 运行环境：Linux + systemd（deploy/README 要求 systemd、bash 4+、python3；具体发行版未在代码中固定）。
- 数据库：MySQL（go-sql-driver/mysql），8 个服务各自一个库（login / maple / auction / transaction / allianceDB / lease / dropDB / crossDataDB），`install.sh` 按配置里的 `db` 名自动建库导表。
- 缓存：Redis（redigo），admin / router / queueServer / centralLogin / orderService / crossTeamServer / auction / leaseServer 使用。
- 端口：见第 2 节各服务条目；完整清单以 `deploy/instances.conf` 为唯一事实来源。
- 启动脚本：systemd 单元 `centralsvc-<服务名>` 由模板生成；旧方式 `bin/<服务名>/game.sh`、`up.sh` 仍可用。
- 构建命令：`deploy/build_linux.sh`（交叉编译到 dist/）或根目录 `build_all.sh`；目标机现编需 Go 1.21+。
- 配置三层叠加：`bin/<服务名>/<服务名>.json` 基线 + `deploy/deploy.env`（统一 MySQL/Redis）+ `deploy/overrides.conf`（机器相关地址端口），由 `deploy/lib/render_config.py` 渲染。

## 6. 编码约束（强制规则，AI修改代码必须遵守）
1. 配置键名存在历史不一致，渲染器已做兼容：orderService 的 MySQL 口令键是 `password`（别的是 `passwd`）；auction/orderService 的 Redis 块叫 `redis`（别的是 `redisServer`）；auction Redis 用户键叫 `user`；leaseServer 的块名是 `Mysql`/`RedisServer`（首字母大写）。**改这些服务配置结构时不要"顺手统一"键名，会破坏渲染器兼容。**
2. MySQL 连接统一 `SetMaxIdleConns(50) / SetMaxOpenConns(50) / SetConnMaxLifetime(290s)` 的既有模式，新服务照抄。
3. 日志一律走 `appLog`（zap 封装），不要用标准库 log 打业务日志；启动期错误才用 log.Println。
4. 新服务的配置热更用 viper + fsnotify + MD5 比对的既有模式（centralLogin/queueServer/auction 已有范例），MD5 不变直接 return 避免重复 reload。
5. 每个服务的 TCP listener 接受连接后，`NewService` 里必须 `channel.SetEndPoint(service)` 双向绑定，否则 trpc 分发会 nil panic。
6. 重大改动（新增服务、改 trpc 方法顺序、改表结构）先输出方案再写代码。

## 7. 已知坑 & 历史问题（非常关键，避免重复踩坑）
1. **pid 文件残留导致服务无限重启**：崩溃/OOM/SIGKILL 时 `DelPidFile` 不会执行（只在信号触发的 `ExitProgram` 里），残留 `<服务名>_0.pid` 会让新进程 `WritePidFile` 失败直接 `os.Exit(2)`，systemd 拉起再崩，且此时信号处理器还没注册，`systemctl stop` 也清不掉。部署单元已加 `ExecStartPre` 兜底（进程死了就删 pid），手工排查用 `kill -0 $(cat pid)` 判断 stale。
2. **systemd 203/EXEC**：安装目录在 `/home` 下时 `ProtectHome=true` 会把 home 挂成空 tmpfs 导致二进制 ENOENT，且 journal 无任何输出；脚本已按安装根目录自动决定 `ProtectHome=no`，手工改单元时必须留意。
3. **bin/ 与 dist/ 不能混用**：bin/ 是配置基线入库目录，dist/ 才是 `build_linux.sh` 的交付产物；旧二进制混在 bin/ 里曾导致 `--skip-build` 把几周前的旧包装上生产，`--strict-fresh` 会拦这种过期产物。
4. **漏配 overrides 的静默失败**：开发机 `192.168.x.x` 地址如果没在 overrides.conf 覆盖，会原样进生产配置，表现为"服务能起但连不上对端"，日志不报错；部署带 `--strict-ips` 可拦截。
5. **common 反向依赖 centralLogin**：`common/utils.go` 里 `GetAccoutType` 直接 import 了 `centralLogin/centralLoginApp/clientService` 的 AccountType 枚举，改 centralLogin 的 proto 枚举会影响 common，注意编译依赖方向。

## 8. 待办 / 正在开发
- [ ] （暂未梳理，后续任务补充）

## 9. 禁止事项
- ❌ 不要调整 `.proto` 已生成方法在 `Methods` 切片里的注册顺序（会改变 methodIndex 破坏线上协议）
- ❌ 不要擅自统一各服务历史遗留的配置键名变体（见第 6 节第 1 条）
- ❌ 不要把配置模板拆成多份手写，配置必须走三层叠加渲染
- ❌ 不要在没有登记 `deploy/instances.conf` 的情况下新增服务目录（不会被部署脚本发现）
- ❌ 不要提交密钥/数据库密码到仓库（deploy.env、overrides.conf 均为 .example 模板入库）
- ❌ 文件的增删改只限于当前项目根目录（`centralService/`）及其子目录内；任何涉及项目外部文件的改动，都必须先提示并获得用户确认
- ❌ 后续提出的任何需求，在正式修改代码/文档之前，必须先按功能或模块列出解决方案与思路，经用户同意后才允许动手修改
