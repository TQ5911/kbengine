# AGENTS.md — gamemerge

面向 OpenCode / agent 的紧凑指南。每条都回答"agent 不靠这个会踩坑吗"。能读 README / go.mod / `docs/implementation.md` 直接得到的就不重复。

## 硬性规则

- **不要新增单元测试**（除非用户明确要求）。改 `transformers.go` / `pipeline.go` / `entity_pipeline.go` 时不要再补 `_test.go`，已存在的测试保持原样。
- **`internal/merger/` 下不放测试文件**。merger 的测试统一放在 `internal/merger_test/`，包名为 `merger_test`（外部测试包）。新增 transformer / pipeline 辅助方法时若需要测试，往 `merger_test/` 加，类型引用要带 `merger.` 前缀；若代码引用了不导出的类型，得先把对应类型改成导出（同名首字母大写）再写测试。
- 不要把真实 DSN / 密码写进任何被提交的文件。`configs/config.yaml` 已被 `.gitignore` 排除；提交前用 `configs/config.example.yaml` 校验。
- 不要把 Python 旧实现（`gameMerge/gameMerge/`）当作 Go 源码的一部分——它只作参考，不会被 `go build` 编译。

## 架构速览

- 入口：`cmd/gamemerge/main.go` → `merge.Orchestrator.Run` → `Job.Run`（`internal/app/merge/`）。
- `Job.Run` 当前按 **DAG** 驱动（`job.go:380`）：每步显式声明依赖（`merger.Step.Deps`），无依赖的立即并发启动；上游一完成下游立即启动——**不等其他无关 step**。这是之前 layer 模型的修正（layer 强制对齐，KBE 跑完后 tbl_Account 必须等 Guild 等无关表完成才能启动）。

  依赖图：

  ```
  kbe_accountinfos ─→ tbl_Account

  kbe_accountinfos ─┐
  tbl_Avatar ───────┴─→ game_account_characters

  （其它表无任何上游依赖，从头并发）：
    tbl_Guild / tbl_Avatar (dst schema 已删 sm_accountDBID 列，不再消费 accMap)
    game_guild_avatar / game_last_global_mail_info
    game_account_mails / game_account_offline_callbacks / game_admin_cmds
    game_avatar_offline_callbacks / game_friends / game_modify_currency
    game_player_mails / game_safe_box / game_safe_box_idempotent
    tbl_BountyStub（特例：归档全局单例，只做子表追加到 dst 既有 root 行之下，
    不走 EntityMerger 整树合并；见 internal/app/merge/bounty_stub.go）
  ```

  注意 `game_account_characters` 的 deps 必须**同时**声明 `kbe_accountinfos` 和 `tbl_Avatar`——前者产 accMap（KBE 命中也写 IDMap，所以完整覆盖所有 src.entityDBID），后者产 avatarMap，缺一个会读到 nil/空映射导致 join 失效。tbl_Avatar 本身已从 KBE 链路解绑（dst 不再需要按 src account id 改写 sm_accountDBID），所以 KBE 和 tbl_Avatar 是并行跑的。

  执行工具：`merger.RunDAG(ctx, []merger.Step)`（在 `merger/stage.go`）。每个 step 完成时递减下游的 remaining 计数，归零立刻 spawn；第一个 error 时 `cancel()` 子 ctx 让兄弟 Pipeline 立刻停。新增无依赖表 → `Deps: nil` 加进 steps 即可；新增依赖表 → `Deps: []string{"上游名"}` 写清楚。
- Pipeline 三阶段框架在 `internal/merger/pipeline.go`：reader → processor → writer，靠 `ctx` 串/并行。
- **新增 transformer** 统一放在 `internal/merger/transformer/<name>.go`（包名 `transformer`），引用 `Row` / `TableMeta` 等基础类型时通过 `merger` 包，import 别名 `merger`。每个 transformer 一个文件，含类型定义 + `Process` 方法；工厂函数（如 `BuildEntityPipeline`）跟其配套 transformer 同文件。已存在的 transformer 触发场景速查：`KBETransformer` = kbe 字典表（合服起点；命中 / 未命中都写 IDMap，保证 accMap 完整覆盖）；`AccountConsumerTransformer` = tbl_Account（消费 KBE 映射）；`RootTransformer` = 通用 root 表（Avatar / Guild）；`EntityTransformer` = 子表（tablelevel 自动发现）；`GameAccountCharactersTransformer` = 角色表（同时消费 AccountMap + AvatarMap 改写 parentID / authDbId / dbId，drop 时 WARN + 计数）；`PassthroughTransformer` = 纯映射表（保留 src id）；`IDAutoIncrementTransformer` = id 列由 dst.auto_increment 自行分配（流水 / 玩家私有数据）；`StateKeepTransformer` = 装饰器，按指定列白名单过滤行（当前用于 tbl_BountyStub_bountyInfoData_bountyList 只保留 PUBLISHED/ACCEPTED 悬赏单）。
- 实体树自动发现：`AnalyzeEntity` (`entity_spec.go`) + `service/tablelevel.Tree`，不要手动枚举 `tbl_Avatar_*` / `tbl_Guild_*` 子表。
- 父表与子表顺序：父 pipeline `Sink.Close()` 之后才起子 pipeline；不要并发同一 root 的父子表，否则子表 join 父 idmap 会丢命中。

依赖方向：`cmd` → `app` → `service` ↔ `merger` → `infrastructure`；`internal/domain` 不依赖任何其他包。

## 命令

- 构建：`bash scripts/build.sh`（默认 release，产物 `bin/gamemerge-${GOOS}-${GOARCH}`，注入 version/commit/buildTime/goVersion）
  - debug：`bash scripts/build.sh -c debug`
  - 交叉：`bash scripts/build.sh -t linux/amd64`
- 运行：`./bin/gamemerge-linux-amd64 --config configs/config.yaml`
- 测试：`go test ./...`（SQL mock 用 `go-sqlmock`；`docs/implementation.md` 提到的 dockertest 集成测试在本仓库未配置）
- merger 的测试现在在 `./internal/merger_test/`，例如：`go test ./internal/merger_test/ -run TestKBETransformer -v`
- vet：`go vet ./...`

## 配置 (`configs/`)

- `config.example.yaml` 是模板，已 gitignored `config.yaml`，本地复制后再改。
- `merge.jobs` 是 `(src, dst)` 对，每项引用 `databases` 里的 key；多 src 合到同一 dst 写多条。
- `merge.read_batch` / `merge.write_batch` 控制 Pipeline 批大小。
- `merge.root` 字段当前实现不读取（`Orchestrator` 不依赖），保留无害。

## 约定

- `Transformer.Process(ctx, row) (Row, error)`：返回 `(nil, nil)` 表示丢弃行（不是错误）。
- 纯透传表（无 ID 重写、无冲突）→ `PassthroughTransformer` + `Job.mergePassthroughTbl`，不要复用 `EntityMerger`。
- SQL 用 `database/sql` + `?` 占位，禁止字符串拼值（参考 `internal/merger/sql_source.go`）。
- 日志走 `log/slog`（main 里 `slog.SetDefault`），每 stage 起止打 INFO。

## 容易踩的坑

- `internal/merger/pipeline.go:298` `flush` 函数里 `}` 缩进只有两个 tab，语义 OK 但与上下文不齐；无关 PR 不要顺手改格式。
- `CursorSource` 按 `id > ? ORDER BY id` 游标扫描，**id 列必须是可比较大整数**；纯 string 主键的表（如 `kbe_accountinfos` 用 `accountName`）不能直接套，需要参考 `CursorSource` 自己实现。同理，游标列若**非唯一**，单个取值的行数超过 ReadBatch 时 `WHERE col > ?` 会跳过跨批边界的剩余行（静默丢数据）——`BuildEntityPipeline` 因此固定用 `id` 列做子表游标（parentID 只用于 join 改写，不再当游标）。
- `BulkSink` 调 `mysqlinfra.WriteColumns` 返回全部列名（含 auto_increment）；真正跳过某列靠 `colIdxs[i] = -1`（来自 `src.Meta().Index(c)` 查不到时的 fallback）。若想让 src 原值原样写入（比如保留 `gbId`），需要让 `colIdxs[i]` 指向 src 行里那一列。
- Pipeline 任一阶段报错都通过 `ctx` 取消上下游；写自定义 `Source` / `Transformer` 时，每个 `for` 入口和阻塞发送前都要 `select { case <-ctx.Done(): ... }`。
- `--dry-run` 已在 main 里接收，但当前是 no-op（`_ = dryRun`），不要假设它真的不写库。