# GameMerge

GameMerge 是一个使用 Go 编写的 MySQL 游戏数据合服工具。程序以 `(src, dst)` 为一个合服任务，通过 DAG 调度多张表，并在每张表内部使用 `Source -> Transformer -> Sink` 三阶段 Pipeline 完成批量读取、数据改写和批量写入。

本文重点说明如何接入新表、增加新的 Transformer，以及通常需要同步修改的代码。

## 目录结构

```text
cmd/gamemerge/                         程序入口
configs/                               配置模板
internal/app/merge/                    合服任务编排、DAG 注册
internal/merger/                       Pipeline、DAG、Source、Sink 等基础能力
internal/merger/transformer/           Transformer 实现
internal/service/idmap/                新旧 ID 映射
internal/service/tablelevel/           Entity 子表自动发现
scripts/build.sh                       构建脚本
docs/implementation.md                早期设计文档，仅供参考
```

`gameMerge/gameMerge/` 是 Python 旧实现，只用于参考，不参与 Go 项目的构建。

## 核心处理流程

### Pipeline

每张表通常对应一条 Pipeline：

```text
CursorSource -> Transformer.Process -> BulkSink
```

相关接口定义在 `internal/merger/pipeline.go`：

```go
type Transformer interface {
    Process(ctx context.Context, row Row) (Row, error)
}
```

Transformer 的返回值约定：

- `return row, nil`：保留并写入该行；
- `return nil, nil`：丢弃该行，不视为错误，Pipeline 会增加 `rows_drop`；
- `return nil, err`：终止当前 Pipeline，并通过 `context` 通知上下游退出。

`Row` 的实际类型是 `[]any`。不要直接依赖固定下标，优先使用 `merger.TableMeta`：

```go
oldID, ok := t.Meta.GetInt64(row, t.IDCol)
name, ok := t.Meta.String(row, t.NameCol)
t.Meta.Set(row, t.IDCol, newID)
```

### DAG

表之间的依赖由 `internal/app/merge/job.go` 中的 `merger.Step` 声明，执行器位于 `internal/merger/stage.go`。

当前主要依赖关系为：

```text
kbe_accountinfos ───────────────→ tbl_Account
kbe_accountinfos ─┐
tbl_Avatar ───────┴────────────→ game_account_characters

其他表无上游依赖，从任务开始时并发执行。
```

无依赖节点会立即启动；一个节点完成后，其依赖计数归零的下游会立即启动，不需要等待无关表完成。任一节点失败后，DAG 会取消其他节点。

## 现有 Transformer

| Transformer | 文件 | 用途 |
| --- | --- | --- |
| `KBETransformer` | `internal/merger/transformer/kbe.go` | 合并 KBE 账号字典，处理账号去重并生成账号 ID 映射 |
| `AccountConsumerTransformer` | `internal/merger/transformer/account_consumer.go` | 消费 KBE 映射，改写 `tbl_Account.id` |
| `RootTransformer` | `internal/merger/transformer/root.go` | 合并 Avatar、Guild 等 Entity 根表并生成 ID 映射 |
| `EntityTransformer` | `internal/merger/transformer/entity.go` | 合并 Entity 子表，改写 `parentID` 和子表 ID |
| `PassthroughTransformer` | `internal/merger/transformer/passthrough.go` | 整行透传，不改写字段 |
| `IDAutoIncrementTransformer` | `internal/merger/transformer/id_auto_increment.go` | 清空源主键，让目标库的 `auto_increment` 分配新 ID |
| `GameAccountCharactersTransformer` | `internal/merger/transformer/game_account_characters.go` | 同时消费账号和 Avatar 映射，改写角色表多个外键 |

## 接入新表前先判断类型

很多新表不需要新增 Transformer。先按以下规则判断：

| 新表需求 | 推荐方式 | 需要修改的位置 |
| --- | --- | --- |
| 主键由目标库自增，其他字段原样保留 | 复用 `IDAutoIncrementTransformer` | 把表名加入 `job.go` 的 `autoIncrementIDTbls` |
| 所有字段原样写入，不改 ID | 复用 `PassthroughTransformer` | 把表名加入 `job.go` 的 `passthroughTbls` |
| 新增标准 Entity 根表及其子表 | 复用 `RootTransformer`、`EntityTransformer` | 在 `Job.Run` 增加 root Step，必要时调整 `entity_spec.go` |
| 需要特殊去重、ID 生成、外键映射或过滤规则 | 新增自定义 Transformer | Transformer、Job helper、DAG Step，必要时增加映射状态 |

### 增加自增 ID 表

如果表的主键需要由目标库重新分配，其他列不改写，只需修改：

```go
var autoIncrementIDTbls = []string{
    "game_account_mails",
    "your_new_table",
}
```

程序会自动查找目标表主键、构建 Pipeline，并使用 `IDAutoIncrementTransformer` 将主键设为 `nil`。

### 增加纯透传表

如果源表数据可以直接写入目标表，只需修改：

```go
var passthroughTbls = []passthroughTbl{
    {"game_guild_avatar"},
    {"your_new_table"},
}
```

纯透传表必须有单列主键，主键由 `SHOW COLUMNS` 自动发现。复合主键不受支持。

## 如何新增自定义 Transformer

以下以 `ExampleTransformer` 为例。

### 1. 新建 Transformer 文件

在 `internal/merger/transformer/` 下创建一个独立文件，例如：

```text
internal/merger/transformer/example.go
```

基础结构：

```go
package transformer

import (
    "context"
    "fmt"

    "gamemerge/internal/merger"
)

type ExampleTransformer struct {
    Meta merger.TableMeta

    IDMap interface {
        Get(oldID int64) (int64, bool)
    }

    ForeignIDCol string
}

func (t *ExampleTransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
    oldID, ok := t.Meta.GetInt64(row, t.ForeignIDCol)
    if !ok {
        return nil, fmt.Errorf("column %s is not int64", t.ForeignIDCol)
    }

    newID, found := t.IDMap.Get(oldID)
    if !found {
        return nil, nil
    }

    if !t.Meta.Set(row, t.ForeignIDCol, newID) {
        return nil, fmt.Errorf("missing column %s", t.ForeignIDCol)
    }
    return row, nil
}
```

实现时遵循以下约定：

1. `Meta` 使用 `merger.TableMeta` 值类型；
2. 列读写使用 `Meta.Get`、`GetInt64`、`String` 和 `Set`；
3. 依赖 ID 映射时优先声明最小接口，不直接依赖具体实现，方便替换和测试；
4. 可预期的业务过滤返回 `(nil, nil)`；真正的数据结构错误或执行错误返回 `error`；
5. Transformer 不直接执行 SQL，读取与写入分别交给 Source 和 Sink；
6. Transformer 可能在 Pipeline 的 goroutine 中执行，共享状态必须保证并发安全。

### 2. 在 Job 中装配 Pipeline

在 `internal/app/merge/job.go` 中新增 helper，例如：

```go
func (j *Job) mergeExampleTbl(ctx context.Context, idMap interface {
    Get(oldID int64) (int64, bool)
}) error {
    const table = "your_new_table"
    const cursorCol = "id"

    allCols, err := mysqlinfra.ColumnsEx(ctx, j.Dst, table)
    if err != nil {
        return fmt.Errorf("%s: columns: %w", table, err)
    }

    allNames := make([]string, len(allCols))
    for i, col := range allCols {
        allNames[i] = col.Name
    }
    writeCols := mysqlinfra.WriteColumns(allCols)

    src := merger.NewCursorSource(j.Src, table, cursorCol, allNames, j.ReadBatch)
    colIdxs := make([]int, len(writeCols))
    for i, col := range writeCols {
        if idx, ok := src.Meta().Index(col); ok {
            colIdxs[i] = idx
        } else {
            colIdxs[i] = -1
        }
    }

    sink := merger.NewBulkSink(j.Dst, table, writeCols, colIdxs, j.WriteBatch)
    pipe := &merger.Pipeline{
        Name:   table,
        Source: src,
        Process: &transformer.ExampleTransformer{
            Meta:         src.Meta(),
            IDMap:        idMap,
            ForeignIDCol: "parentID",
        },
        Sink: sink,
        Config: merger.PipelineConfig{
            ReadBuf:    4,
            ProcessBuf: 4,
            WriteBatch: j.WriteBatch,
        },
    }

    if err := pipe.Run(ctx); err != nil {
        return fmt.Errorf("%s: %w", table, err)
    }
    return nil
}
```

装配流程通常是：

1. 使用 `mysqlinfra.ColumnsEx` 获取目标表列定义；
2. 使用 `mysqlinfra.WriteColumns` 排除不应直接写入的列；
3. 创建 `CursorSource`；
4. 根据 Source 的 `TableMeta` 生成 `colIdxs`；
5. 创建 `BulkSink`；
6. 创建 Transformer 并注入列名、IDMap 等依赖；
7. 创建并执行 `merger.Pipeline`。

`colIdxs` 表示目标写入列对应源 Row 中的下标。源列不存在时必须填 `-1`。如果某列需要保留源值，应让它指向 Source 中的真实列下标，不能误设为 `-1`。

如果多张表共享完全相同的装配规则，可以像 `autoIncrementIDSteps` 一样维护表清单并批量生成 Step，避免复制多个 helper。

### 3. 注册 DAG Step

在 `Job.Run` 的 `steps` 中注册新表：

```go
{Name: "your_new_table", Deps: []string{"upstream_table"}, Fn: func(ctx context.Context) error {
    return j.mergeExampleTbl(ctx, upstreamMap)
}},
```

无依赖表不需要映射参数时，可以直接注册独立 helper：

```go
{Name: "your_independent_table", Deps: nil, Fn: func(ctx context.Context) error {
    return j.mergeIndependentTbl(ctx)
}},
```

DAG 注册需要注意：

- `Name` 在同一组 Step 中必须唯一；
- `Deps` 中的名称必须与已注册 Step 的 `Name` 完全一致；
- 不要遗漏实际依赖，否则下游可能在 IDMap 尚未生成时启动；
- 当前 `RunDAG` 会校验未知依赖，但不会检测循环依赖，禁止形成环；
- 跨 Step 的 IDMap 应由上游生成，下游通过闭包读取；
- 如果下游同时依赖多个映射，必须在 `Deps` 中列出所有上游。

例如 `game_account_characters` 同时读取账号映射和 Avatar 映射，因此必须同时依赖 `kbe_accountinfos` 和 `tbl_Avatar`。

### 4. 跨 Step 传递映射

标准 ID 映射使用 `internal/service/idmap.IDMap`：

```go
var exampleMap *idmap.IDMap

steps := []merger.Step{
    {Name: "upstream", Deps: nil, Fn: func(ctx context.Context) error {
        m, err := j.mergeUpstreamTbl(ctx)
        if err != nil {
            return err
        }
        exampleMap = m
        return nil
    }},
    {Name: "downstream", Deps: []string{"upstream"}, Fn: func(ctx context.Context) error {
        return j.mergeExampleTbl(ctx, exampleMap)
    }},
}
```

上游负责完整写入映射，下游只在上游 Step 完成后读取。不要把存在写入竞争的普通 `map` 直接暴露给并发 Step。

### 5. 装配逻辑复杂时增加工厂函数

当新 Transformer 需要列校验、多个映射或特殊 Source/Sink 时，可以把装配逻辑封装为工厂。参考：

```text
internal/merger/transformer/entity_pipeline.go
```

建议使用 Options 结构体：

```go
type BuildExampleOptions struct {
    Src        *sql.DB
    Dst        *sql.DB
    Table      string
    CursorCol  string
    ReadBatch  int
    WriteBatch int
}

func BuildExamplePipeline(
    ctx context.Context,
    opts BuildExampleOptions,
    idMap interface {
        Get(oldID int64) (int64, bool)
    },
) (*merger.Pipeline, error) {
    return nil, nil
}
```

工厂应只负责校验和组装；实际执行仍由 Job helper 调用 `pipe.Run(ctx)`。

### 6. 需要统计丢弃原因时

普通 Pipeline 已统计总 `rows_drop`。如果还要按原因统计，可以参考 `GameAccountCharactersTransformer`：

- 总数使用 `atomic.Int64`；
- 原因映射本身使用 `sync.Mutex` 保护；
- 每个原因的计数器使用 `atomic.Int64`；
- 只采样输出少量逐行 WARN；
- Pipeline 完成后由 Job 输出汇总日志。

不要对每一条异常数据无限制打印日志，否则大表合并时会产生大量 I/O。

## 新增 Entity 根表

标准 Entity 表通常不需要编写新 Transformer。`EntityMerger` 会：

1. 分析根表结构；
2. 使用 `RootTransformer` 合并根表并产生 Root IDMap；
3. 通过 `internal/service/tablelevel` 自动发现子表；
4. 在根表 Sink 关闭后，按层处理子表；
5. 使用 `EntityTransformer` 改写子表 `parentID`。

在 `Job.Run` 中增加根表 Step：

```go
{Name: "tbl_NewRoot", Deps: nil, Fn: func(ctx context.Context) error {
    _, err := j.mergeTbl(ctx, "NewRoot", nil)
    return err
}},
```

命名通常应符合：

```text
根表：tbl_NewRoot
子表：tbl_NewRoot_*
```

如果表结构不符合现有 `AnalyzeEntity` 规则，需要同步修改 `internal/app/merge/entity_spec.go`。不要手工枚举标准 Entity 子表。

## Source 和 Sink 注意事项

### CursorSource

`CursorSource` 使用以下思路分页：

```sql
WHERE cursor_column > ? ORDER BY cursor_column
```

因此游标列应满足：

- 单列；
- 值可稳定比较；
- 最好是递增的大整数；
- 不支持复合主键。

字符串主键、非唯一游标或排序规则复杂的字段不要直接套用，必要时实现专用 Source。自定义 Source 的循环和阻塞发送必须响应 `ctx.Done()`。

### BulkSink

SQL 必须使用 `database/sql` 参数占位符，不允许把值拼接进 SQL。

`mysqlinfra.WriteColumns` 返回可写列，`colIdxs` 决定每个目标列从源 Row 的哪个位置取值。处理 auto-increment 列时，应明确区分：

- 由 Transformer 将值设为 `nil`，让目标库分配；
- 目标写入列在源 Row 中不存在，使用 `colIdxs[i] = -1`；
- 保留源值，使用 Source 中对应列的真实下标。

## 检查清单

新增 Transformer 或接入新表后，至少确认：

- [ ] 是否真的需要新增 Transformer，能否复用现有类型；
- [ ] Transformer 位于 `internal/merger/transformer/`，一个文件一个主要 Transformer；
- [ ] 必需列在运行前完成校验；
- [ ] 列读写使用 `TableMeta`，没有依赖不稳定的 Row 下标；
- [ ] `(nil, nil)` 只用于明确允许丢弃的业务场景；
- [ ] IDMap 对命中和未命中场景的覆盖符合下游要求；
- [ ] Pipeline 的 Source、Sink 和 `colIdxs` 正确；
- [ ] 新表已经加入列表或注册到 `Job.Run`；
- [ ] DAG 声明了全部上游依赖，且没有环；
- [ ] 父表完成并关闭 Sink 后才处理依赖其 IDMap 的子表；
- [ ] 日志使用 `log/slog`，不记录密码、DSN 等敏感信息；
- [ ] SQL 使用 `?` 占位符；
- [ ] 已运行测试、vet 和构建检查。

## 构建与校验

```bash
# 全量测试
go test ./...

# merger 相关测试
go test ./internal/merger_test/ -v

# 静态检查
go vet ./...

# release 构建
bash scripts/build.sh

# debug 构建
bash scripts/build.sh -c debug
```

项目约定：除非任务明确要求，不要新增单元测试；已有测试必须保持通过。如果确实需要增加 merger 测试，统一放在 `internal/merger_test/`，包名使用 `merger_test`，不要在 `internal/merger/` 下新增 `_test.go`。

## 配置与运行

复制配置模板并填写本地数据库连接：

```bash
cp configs/config.example.yaml configs/config.yaml
bash scripts/build.sh
./bin/gamemerge-linux-amd64 --config configs/config.yaml
```

`configs/config.yaml` 已被忽略，不要把真实 DSN 或密码提交到仓库。当前 `--dry-run` 参数不会阻止数据库写入，不要把它当作安全演练模式。
