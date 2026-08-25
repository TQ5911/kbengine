package merge

import (
	"context"
	"database/sql"
	"fmt"
	"log/slog"
	"sort"
	"sync/atomic"

	"gamemerge/internal/domain"
	mysqlinfra "gamemerge/internal/infrastructure/mysql"
	"gamemerge/internal/merger"
	"gamemerge/internal/merger/transformer"
	"gamemerge/internal/service/cache"
	"gamemerge/internal/service/idmap"
)

// autoIncrementIDTbls 是"主键 id 自增、其它列透传"的流水表清单。
// 所有表都走 IDAutoIncrementTransformer，无依赖、可并发跑。
// 加新表：在下面加一行即可，不用改 Job.Run。
var autoIncrementIDTbls = []string{
	"game_account_mails",
	"game_account_offline_callbacks",
	"game_admin_cmds",
	"game_avatar_offline_callbacks",
	"game_friends",
	"game_modify_currency",
	"game_player_mails",
	"game_safe_box",
	"game_safe_box_idempotent",
}

// passthroughTbl 是 passthrough 表的元组：只需要表名，PK 列由
// mergePassthroughTbl 内部 SHOW COLUMNS 自动查（避免每个调用方硬编码 PK 列名）。
type passthroughTbl struct {
	name string
}

// passthroughTbls 是"整行透传、不做改写"的纯映射表清单。
// 走 PassthroughTransformer，无依赖、可并发跑。
// 加新表：在下面加一行（只填 name），不用改 Job.Run。
var passthroughTbls = []passthroughTbl{
	{"game_guild_avatar"},
	{"game_last_global_mail_info"},
}

// autoIncrementIDSteps 把表名批量转成 DAG step。Go 1.22+ loop 变量按迭代作用域，
// 所以闭包里直接引用 tbl 不用额外捕获。
func autoIncrementIDSteps(j *Job, tbls []string) []merger.Step {
	out := make([]merger.Step, 0, len(tbls))
	for _, tbl := range tbls {
		out = append(out, merger.Step{
			Name: tbl, Deps: nil,
			Fn: func(ctx context.Context) error {
				return j.mergeAutoIncrementIDTbl(ctx, tbl)
			},
		})
	}
	return out
}

// passthroughSteps 同上，但走 mergePassthroughTbl。PK 列由 mergePassthroughTbl
// 内部自动查。
func passthroughSteps(j *Job, tbls []passthroughTbl) []merger.Step {
	out := make([]merger.Step, 0, len(tbls))
	for _, pt := range tbls {
		name := pt.name
		out = append(out, merger.Step{
			Name: name, Deps: nil,
			Fn: func(ctx context.Context) error {
				return j.mergePassthroughTbl(ctx, name)
			},
		})
	}
	return out
}

// Job 代表一对 (src, dst) 数据库的一次合服操作；把工作委托给 EntityMerger.Merge。
// rootName 由调用方传入（如 cfg.Merge.Root）。parentMap 仅供 root 含指向父实体的
// 列时使用，目前通常传 nil。
type Job struct {
	Src        *sql.DB
	Dst        *sql.DB
	ReadBatch  int
	WriteBatch int
}

func (j *Job) mergeTbl(ctx context.Context, rootTbl string, parentMap interface {
	Get(oldID int64) (int64, bool)
}) (*idmap.IDMap, error) {
	slog.Info("entity merge start", "root", rootTbl)
	merger := &EntityMerger{
		Src:        j.Src,
		Dst:        j.Dst,
		ReadBatch:  j.ReadBatch,
		WriteBatch: j.WriteBatch,
		Name:       rootTbl,
		ParentMap:  parentMap,
	}
	if err := merger.Merge(ctx); err != nil {
		slog.Error("entity merge failed", "root", rootTbl, "err", err)
		return nil, fmt.Errorf("root %s: %w", rootTbl, err)
	}
	slog.Info("entity merge done", "root", rootTbl,
		"idmap_size", merger.RootIDMap.Len())
	return merger.RootIDMap, nil
}

// mergePassthroughTbl 处理像 game_guild_avatar 这类无需 ID 改写、无需做
// 冲突检测的纯映射表：cursor 顺序读 src → PassthroughTransformer → BulkSink。
//
// PK 列由 SHOW COLUMNS 自动查（避免硬编码 PK 列名），所以调用方只需要传表名。
// 复合 PK 会报错——CursorSource 是单列游标扫描。
func (j *Job) mergePassthroughTbl(ctx context.Context, table string) error {
	slog.Info("passthrough merge start", "table", table)
	pk, err := mysqlinfra.PrimaryKeyColumn(ctx, j.Dst, table)
	if err != nil {
		slog.Error("passthrough merge failed", "table", table, "err", err)
		return fmt.Errorf("passthrough %s: %w", table, err)
	}
	allCols, err := mysqlinfra.ColumnsEx(ctx, j.Dst, table)
	if err != nil {
		slog.Error("passthrough merge failed", "table", table, "err", err)
		return fmt.Errorf("passthrough %s: columns: %w", table, err)
	}
	allNames := make([]string, len(allCols))
	for i, c := range allCols {
		allNames[i] = c.Name
	}
	writeCols := mysqlinfra.WriteColumns(allCols)

	src := merger.NewCursorSource(j.Src, table, pk, allNames, j.ReadBatch)

	colIdxs := make([]int, len(writeCols))
	for i, c := range writeCols {
		if idx, ok := src.Meta().Index(c); ok {
			colIdxs[i] = idx
		} else {
			colIdxs[i] = -1
		}
	}
	sink := merger.NewBulkSink(j.Dst, table, writeCols, colIdxs, j.WriteBatch)
	pipe := &merger.Pipeline{
		Name:    table,
		Source:  src,
		Process: &transformer.PassthroughTransformer{Meta: src.Meta()},
		Sink:    sink,
		Config: merger.PipelineConfig{
			ReadBuf:    4,
			ProcessBuf: 4,
			WriteBatch: j.WriteBatch,
		},
	}
	if err := pipe.Run(ctx); err != nil {
		slog.Error("passthrough merge failed", "table", table, "err", err)
		return fmt.Errorf("passthrough %s: %w", table, err)
	}
	slog.Info("passthrough merge done", "table", table)
	return nil
}

// mergeKBEAccountInfosTbl 是合服链路第一步：处理 kbe_accountinfos 这张"账号字典表"。
//
// 流程：
//   1. 加载 dst 已有账号到 DstAccountCache（accountName → id）；
//   2. 读取 dst.tbl_Account 最大 id 作为 Base（命中时 dst.id 直接用，未命中用 oldDBID+Base 偏移）；
//   3. 跑 KBETransformer pipeline：命中 dst name → drop 行但记录
//      src.entityDBID → dst.id 到 Duplicated（供后续 tbl_Account 跳过）；
//      未命中 → oldDBID+Base 改写 row.entityDBID 并把 src.entityDBID → newDBID 记入 IDMap。
//
// 返回：
//   - idMap：完整的 src.entityDBID → dst.entityDBID 映射（含命中与未命中），供 Avatar 父 join。
//   - duplicated：命中的 src.entityDBID 集合，供 tbl_Account merge 也 drop 这些行。
func (j *Job) mergeKBEAccountInfosTbl(ctx context.Context) (
	idMap *idmap.IDMap, duplicated *transformer.DuplicatedSet, err error,
) {
	const table = "kbe_accountinfos"
	const nameCol = "accountName"
	const entityDBCol = "entityDBID"
	slog.Info("kbe_accountinfos merge start", "table", table)

	// 1. 加载 dst.kbe_accountinfos 已有账号到 DstAccountCache（用 accountName 做业务键）。
	// ⚠️ 必须查 kbe_accountinfos 而不是 tbl_Account：两个表的 account 数据可能不一致
	// （典型场景：dst.kbe_accountinfos 已经有数据但 tbl_Account 还没建好/被清过）；
	// 主键冲突也只可能发生在 kbe_accountinfos 上，所以去重查询要和 INSERT 目标表一致。
	dstAccounts, err := loadDstKBEAccounts(ctx, j.Dst)
	if err != nil {
		return nil, nil, fmt.Errorf("kbe: load dst: %w", err)
	}

	// 2. 取 dst.tbl_Account 最大 id 作为 Base（KBE 未命中时 entityDBID = oldDBID + Base）
	var maxID sql.NullInt64
	if err := j.Dst.QueryRowContext(ctx,
		"SELECT max(`id`) FROM `tbl_Account`").Scan(&maxID); err != nil {
		return nil, nil, fmt.Errorf("kbe: max id: %w", err)
	}
	var base int64
	if maxID.Valid {
		base = maxID.Int64 + 1
	}

	// 3. 构造 pipeline（列/Sink 与 mergePassthroughTbl 一致）
	allCols, err := mysqlinfra.ColumnsEx(ctx, j.Dst, table)
	if err != nil {
		return nil, nil, fmt.Errorf("kbe: columns: %w", err)
	}
	allNames := make([]string, len(allCols))
	for i, c := range allCols {
		allNames[i] = c.Name
	}
	writeCols := mysqlinfra.WriteColumns(allCols)

	src := merger.NewCursorSource(j.Src, table, nameCol, allNames, j.ReadBatch)
	colIdxs := make([]int, len(writeCols))
	for i, c := range writeCols {
		if idx, ok := src.Meta().Index(c); ok {
			colIdxs[i] = idx
		} else {
			colIdxs[i] = -1
		}
	}
	sink := merger.NewBulkSink(j.Dst, table, writeCols, colIdxs, j.WriteBatch)

	idMap = idmap.New(0)
	duplicated = transformer.NewDuplicatedSet()
	pipe := &merger.Pipeline{
		Name:    table,
		Source:  src,
		Process: &transformer.KBETransformer{
			Meta:        src.Meta(),
			DstAccount:  dstAccounts,
			Duplicated:  duplicated,
			IDMap:       idMap,
			Base:        base,
			NameCol:     nameCol,
			EntityDBCol: entityDBCol,
		},
		Sink: sink,
		Config: merger.PipelineConfig{
			ReadBuf:    4,
			ProcessBuf: 4,
			WriteBatch: j.WriteBatch,
		},
	}
	if err := pipe.Run(ctx); err != nil {
		return nil, nil, fmt.Errorf("kbe: %w", err)
	}
	slog.Info("kbe_accountinfos merge done",
		"table", table,
		"idmap_size", idMap.Len(),
		"duplicated_size", duplicated.Len(),
		"dst_preloaded", dstAccounts.Len(),
		"base", base,
	)
	return idMap, duplicated, nil
}

// mergeAccountTbl 处理 tbl_Account 这张 root 表。注意：与之前版本不同，
// 现在不再自己生成 idmap/dedup——直接消费 mergeKBEAccountInfosTbl 产出的 accMap
// 与 duplicated 集合：
//   - 命中 duplicated → drop（dst 已有此账号的 tbl_Account 行）；
//   - 未命中 → 从 accMap 取 new id（来自 KBE 的 oldDBID+Base 偏移）改写 row.id 并写入 dst；
//   - 不在 accMap 里 → drop（说明 src 这条账号在 kbe 里没有授权迁移）。
func (j *Job) mergeAccountTbl(ctx context.Context,
	accMap interface {
		Get(oldID int64) (int64, bool)
	},
	duplicated interface {
		Contains(oldID int64) bool
	},
) error {
	const table = "tbl_Account"
	const nameCol = "sm_accountName"
	const idCol = "id"
	slog.Info("account merge start", "table", table)

	allCols, err := mysqlinfra.ColumnsEx(ctx, j.Dst, table)
	if err != nil {
		return fmt.Errorf("account: columns: %w", err)
	}
	allNames := make([]string, len(allCols))
	for i, c := range allCols {
		allNames[i] = c.Name
	}
	writeCols := mysqlinfra.WriteColumns(allCols)

	src := merger.NewCursorSource(j.Src, table, idCol, allNames, j.ReadBatch)
	colIdxs := make([]int, len(writeCols))
	for i, c := range writeCols {
		if idx, ok := src.Meta().Index(c); ok {
			colIdxs[i] = idx
		} else {
			colIdxs[i] = -1
		}
	}
	sink := merger.NewBulkSink(j.Dst, table, writeCols, colIdxs, j.WriteBatch)

	pipe := &merger.Pipeline{
		Name:   table,
		Source: src,
		Process: &transformer.AccountConsumerTransformer{
			Meta:       src.Meta(),
			AccMap:     accMap,
			Duplicated: duplicated,
			IDCol:      idCol,
		},
		Sink: sink,
		Config: merger.PipelineConfig{
			ReadBuf:    4,
			ProcessBuf: 4,
			WriteBatch: j.WriteBatch,
		},
	}
	if err := pipe.Run(ctx); err != nil {
		return fmt.Errorf("account: %w", err)
	}
	slog.Info("account merge done", "table", table)
	return nil
}

// mergeGameAccountCharactersTbl 处理 game_account_characters 这张"角色表"。
//
// 依赖：必须先合 KBE 与 tbl_Avatar 才能拿到 accMap / avatarMap。
//   - parentID、authDbId 走 accMap（authDbId=0 时不改写，未命中保留 src 值）；
//   - dbId 走 avatarMap；
//   - id 自增（起点 = max(dst.id)+1）；
//   - 命中失败 drop + WARN（避免 dangling reference；正常情况下极少发生：
//     KBE 命中也写 IDMap 后 accMap 完整覆盖，avatarMap 来自 RootTransformer 也完整）。
func (j *Job) mergeGameAccountCharactersTbl(ctx context.Context, accMap, avatarMap interface {
	Get(oldID int64) (int64, bool)
}) error {
	const table = "game_account_characters"
	slog.Info("game_account_characters merge start", "table", table)

	var maxID sql.NullInt64
	if err := j.Dst.QueryRowContext(ctx,
		fmt.Sprintf("SELECT max(`id`) FROM `%s`", table)).Scan(&maxID); err != nil {
		return fmt.Errorf("game_account_characters: max id: %w", err)
	}
	var next int64
	if maxID.Valid {
		next = maxID.Int64 + 1
	}
	nextIDFn := func() int64 {
		n := next
		next++
		return n
	}

	allCols, err := mysqlinfra.ColumnsEx(ctx, j.Dst, table)
	if err != nil {
		return fmt.Errorf("game_account_characters: columns: %w", err)
	}
	allNames := make([]string, len(allCols))
	for i, c := range allCols {
		allNames[i] = c.Name
	}
	writeCols := mysqlinfra.WriteColumns(allCols)

	src := merger.NewCursorSource(j.Src, table, "id", allNames, j.ReadBatch)
	colIdxs := make([]int, len(writeCols))
	for i, c := range writeCols {
		if idx, ok := src.Meta().Index(c); ok {
			colIdxs[i] = idx
		} else {
			colIdxs[i] = -1
		}
	}
	sink := merger.NewBulkSink(j.Dst, table, writeCols, colIdxs, j.WriteBatch)

	t := &transformer.GameAccountCharactersTransformer{
		Meta:         src.Meta(),
		AccountMap:   accMap,
		AvatarMap:    avatarMap,
		NextID:       nextIDFn,
		IDCol:        "id",
		ParentIDCol:  "parentID",
		AuthDbIDCol:  "authDbId",
		DbIDCol:      "dbId",
		DropsByReason: make(map[string]*atomic.Int64),
	}
	pipe := &merger.Pipeline{
		Name:    table,
		Source:  src,
		Process: t,
		Sink:    sink,
		Config: merger.PipelineConfig{
			ReadBuf:    4,
			ProcessBuf: 4,
			WriteBatch: j.WriteBatch,
		},
	}
	if err := pipe.Run(ctx); err != nil {
		return fmt.Errorf("game_account_characters: %w", err)
	}

	// Drop 汇总：每个 reason 一个计数字段；total > 0 时打 WARN（不替换原 INFO，
	// 保留 Pipeline 的 rows_in/out/drop/batches 一起对照看）
	if total, byReason := t.DropSnapshot(); total > 0 {
		attrs := []any{"total_drops", total}
		keys := make([]string, 0, len(byReason))
		for k := range byReason {
			keys = append(keys, k)
		}
		sort.Strings(keys)
		keysAttr := make([]any, 0, len(keys))
		for _, k := range keys {
			attrs = append(attrs, "count_"+k, byReason[k])
			keysAttr = append(keysAttr, k)
		}
		attrs = append(attrs, "by_reason_order", keysAttr)
		slog.Warn("game_account_characters: drop summary", attrs...)
	}

	slog.Info("game_account_characters merge done", "table", table)
	return nil
}

// loadDstKBEAccounts 把 dst.kbe_accountinfos 全量读到 cache.DstAccountCache。
// 用作 KBE 的去重缓存（accountName → dst.entityDBID）。
// ⚠️ 不要改成查 tbl_Account：两表 account 数据可能不一致，且 INSERT 撞主键的目标是 kbe_accountinfos。
func loadDstKBEAccounts(ctx context.Context, dst *sql.DB) (*cache.DstAccountCache, error) {
	rows, err := dst.QueryContext(ctx,
		"SELECT `accountName`, `entityDBID` FROM `kbe_accountinfos`")
	if err != nil {
		return nil, fmt.Errorf("load dst kbe accounts: %w", err)
	}
	defer rows.Close()
	c := cache.NewDstAccount()
	for rows.Next() {
		var name string
		var entityDBID int64
		if err := rows.Scan(&name, &entityDBID); err != nil {
			return nil, fmt.Errorf("scan dst kbe accounts: %w", err)
		}
		c.Put(name, domain.AccountInfo{DBID: entityDBID})
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("iterate dst kbe accounts: %w", err)
	}
	return c, nil
}

func (j *Job) Run(ctx context.Context, parentMap interface {
	Get(oldID int64) (int64, bool)
}) error {
	// Job.Run 按 DAG 驱动合服：每步显式声明依赖，无依赖的立即并发启动；上游一完成
	// 下游立即启动——不必等其他无关 step 跑完（这正是之前 layer 模型踩的坑）。
	// 跨 step 状态由闭包/外层 var 传递，RunDAG 用 mutex + wg.Wait() 保证
	// happens-before，下游一定能读到上游写完的结果。
	//
	// 依赖图：
	//   kbe_accountinfos ─→ tbl_Account
	//   kbe_accountinfos ─┐
	//   tbl_Avatar ───────┴─→ game_account_characters
	//   （其它表无任何上游依赖，从头并发）
	//
	// 注意 tbl_BountyStub 虽无依赖，但语义特殊：它是归档全局单例，只做
	// "子表追加到 dst 既有 root 行下"，不走 EntityMerger 整树合并（否则
	// 会向 dst 插入第二个 root 行，起服加载出两个单例）。
	//
	// 表清单管理：
	//   - autoIncrementIDTbls / passthroughTbls 在文件顶部包级 var，列出走相同
	//     transformer 的表。Run 通过 autoIncrementIDSteps / passthroughSteps
	//     helper 批量展开。加新表 → 在列表里加一行，不用改 Run。
	//   - KBE / tbl_Avatar / tbl_Account / game_account_characters 因为各自有 deps 或
	//     副作用（捕获到外层 var），仍在 Run 里手写。

	var (
		kbeResult struct {
			accMap     *idmap.IDMap
			duplicated *transformer.DuplicatedSet
		}
		avatarMap *idmap.IDMap
	)

	steps := []merger.Step{
		// === 起点：源头 KBE（产出 accMap + duplicated） ===
		{Name: "kbe_accountinfos", Deps: nil, Fn: func(ctx context.Context) error {
			m, d, err := j.mergeKBEAccountInfosTbl(ctx)
			if err != nil {
				return err
			}
			kbeResult.accMap, kbeResult.duplicated = m, d
			return nil
		}},

		// === 独立 entity 树：dst schema 无 sm_accountDBID 列，不需要 accMap ===
		{Name: "tbl_Guild", Deps: nil, Fn: func(ctx context.Context) error {
			_, err := j.mergeTbl(ctx, "Guild", nil)
			return err
		}},
		{Name: "tbl_Avatar", Deps: nil, Fn: func(ctx context.Context) error {
			m, err := j.mergeTbl(ctx, "Avatar", nil)
			if err != nil {
				return err
			}
			avatarMap = m
			return nil
		}},

		// === 归档单例：src 子表行追加到 dst 既有 root 行下，不动 dst root ===
		{Name: "tbl_BountyStub", Deps: nil, Fn: func(ctx context.Context) error {
			return j.mergeBountyStubTbl(ctx)
		}},
		{Name: "tbl_RedBagStub", Deps: nil, Fn: func(ctx context.Context) error {
			return j.mergeRedBagStubTbl(ctx)
		}},

		// === 等 KBE 完：tbl_Account 消费 accMap + duplicated ===
		{Name: "tbl_Account", Deps: []string{"kbe_accountinfos"}, Fn: func(ctx context.Context) error {
			return j.mergeAccountTbl(ctx, kbeResult.accMap, kbeResult.duplicated)
		}},

		// === 同时等 KBE + tbl_Avatar：game_account_characters 消费两份映射 ===
		{Name: "game_account_characters", Deps: []string{"kbe_accountinfos", "tbl_Avatar"}, Fn: func(ctx context.Context) error {
			return j.mergeGameAccountCharactersTbl(ctx, kbeResult.accMap, avatarMap)
		}},
	}

	// === Bulk：从包级列表展开无依赖表 ===
	steps = append(steps, autoIncrementIDSteps(j, autoIncrementIDTbls)...)
	steps = append(steps, passthroughSteps(j, passthroughTbls)...)

	return merger.RunDAG(ctx, steps)
}

// mergeAutoIncrementIDTbl 处理 game_account_mails / game_account_offline_callbacks /
// game_admin_cmds / game_avatar_offline_callbacks / game_friends /
// game_modify_currency / game_player_mails / game_safe_box /
// game_safe_box_idempotent 这类"主键自动分配新 id、其它列透传"的流水表。
//
// 依赖：none。不需要 accMap / avatarMap / duplicated；账号名是字符串业务键
// （src/dst 相同），不需要改写。
//
// 流程：
//   - SHOW COLUMNS 自动查 PK 列名（避免硬编码 "id"）；
//   - CursorSource 按 PK 列游标读 src；
//   - IDAutoIncrementTransformer 把 row[PK] 置 nil（让 dst auto_increment 分配）；
//   - BulkSink 写 INSERT(PK=NULL)，其他列原样落 dst。
func (j *Job) mergeAutoIncrementIDTbl(ctx context.Context, table string) error {
	slog.Info("auto-increment-id merge start", "table", table)

	pk, err := mysqlinfra.PrimaryKeyColumn(ctx, j.Dst, table)
	if err != nil {
		return fmt.Errorf("auto-increment %s: %w", table, err)
	}
	allCols, err := mysqlinfra.ColumnsEx(ctx, j.Dst, table)
	if err != nil {
		return fmt.Errorf("auto-increment %s: columns: %w", table, err)
	}
	allNames := make([]string, len(allCols))
	for i, c := range allCols {
		allNames[i] = c.Name
	}
	writeCols := mysqlinfra.WriteColumns(allCols)

	src := merger.NewCursorSource(j.Src, table, pk, allNames, j.ReadBatch)
	colIdxs := make([]int, len(writeCols))
	for i, c := range writeCols {
		if idx, ok := src.Meta().Index(c); ok {
			colIdxs[i] = idx
		} else {
			colIdxs[i] = -1
		}
	}
	sink := merger.NewBulkSink(j.Dst, table, writeCols, colIdxs, j.WriteBatch)

	pipe := &merger.Pipeline{
		Name:   table,
		Source: src,
		Process: &transformer.IDAutoIncrementTransformer{
			Meta:  src.Meta(),
			IDCol: pk,
		},
		Sink: sink,
		Config: merger.PipelineConfig{
			ReadBuf:    4,
			ProcessBuf: 4,
			WriteBatch: j.WriteBatch,
		},
	}
	if err := pipe.Run(ctx); err != nil {
		return fmt.Errorf("auto-increment %s: %w", table, err)
	}
	slog.Info("auto-increment-id merge done", "table", table)
	return nil
}

func (j *Job) mergeRedBagStubTbl(ctx context.Context) (error) {
	slog.Info("red stub merge start")
	merger := &RedBagEntityMerger{
		Src:        j.Src,
		Dst:        j.Dst,
		ReadBatch:  j.ReadBatch,
		WriteBatch: j.WriteBatch,
		Name:     	"RedBagStub",
	}
	if err := merger.Merge(ctx); err != nil {
		slog.Error("red bag stub merge", "err", err)
		return fmt.Errorf("red bag stub merge error: %w", err)
	}
	slog.Info("red bag stub merge done")
	return nil
}