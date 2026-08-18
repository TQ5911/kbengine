package transformer

import (
	"context"
	"log/slog"
	"sync"
	"sync/atomic"

	"gamemerge/internal/merger"
)

// GameAccountCharactersTransformer 处理 game_account_characters 这张"角色表"。
//
// 触发条件：Job.mergeGameAccountCharactersTbl 构造并执行，消费两个上游映射：
//   - AccountMap（来自 KBE.IDMap）：给 parentID / authDbId 改写；
//   - AvatarMap（来自 tbl_Avatar.RootTransformer.IDMap）：给 dbId 改写。
//
// 适用表特征：一张游戏的角色表，主键 id 是业务主键，含三类跨表外键：
//   - parentID → tbl_Account.id（角色所属账号）；
//   - authDbId → tbl_Account.id（充值 / 渠道账号，可选）；
//   - dbId → tbl_Avatar.id（角色实体 dbid）。
// 还有 gbId、name、school、sex、level、tLastOnline、authExpire 这些纯属性列，
// 合服时全部原样保留。
//
// 改写规则：
//   1. id 自增（NextID() 由调用方构造，起点 = max(dst.id)+1）；
//   2. parentID 在 AccountMap 查新值；未命中 → drop（孤儿账号）+ WARN；
//   3. authDbId != 0 时在 AccountMap 查新值；命中改写、未命中保留 src 值（不是 drop）；
//   4. dbId 在 AvatarMap 查新值；未命中 → drop（孤儿 avatar）+ WARN；
//   5. parentID / dbId 列读不到 int64 时也 drop + WARN（数据损坏）；
//   6. 其余列（gbId、name、school、sex、level、tLastOnline、authExpire）原样保留。
//
// Drop 可见性：每个 drop 都会：
//   - 增加 Drops 总数；
//   - 增加对应 reason 的 DropsByReason 计数（带 sync.Mutex 保护 map 自身读写）；
//   - 前 10 条 WARN 全量打日志（带 reason + 关键字段），超出只增计数不打日志。
// 调用方在 pipe.Run 之后读 Drops / DropsByReason 决定要不要打汇总 WARN。
//
// 设计权衡：所有数据理想情况下都应合入 dst，drop 应当极少（KBE 命中也写 IDMap
// 后 accMap 完整覆盖；avatarMap 来自 RootTransformer 也完整）。drop 触发主要是
// 数据完整性边界 case（src 端 orphan 引用、列损坏）。保留 drop + 报出来，便于
// 上线时及时发现数据问题，而不是 silently 丢角色。
type GameAccountCharactersTransformer struct {
	Meta       merger.TableMeta
	AccountMap interface {
		Get(oldID int64) (int64, bool)
	}
	AvatarMap interface {
		Get(oldID int64) (int64, bool)
	}
	NextID      func() int64
	IDCol       string // "id"
	ParentIDCol string // "parentID"
	AuthDbIDCol string // "authDbId"
	DbIDCol     string // "dbId"

	// Drops 总数（每个 drop 条件递增 1）
	Drops atomic.Int64
	// DropsByReason 按 drop 原因分桶计数；map 自身用 dropsMu 保护，
	// counter 本身是 *atomic.Int64 避免读侧也抢锁。
	DropsByReason map[string]*atomic.Int64
	dropsMu       sync.Mutex
}

const dropLogSampleLimit = 10

func (t *GameAccountCharactersTransformer) recordDrop(reason string, attrs ...any) {
	counter := t.dropsByReason(reason)
	n := counter.Add(1)
	t.Drops.Add(1)
	if n <= dropLogSampleLimit {
		slog.Warn("game_account_characters: drop",
			append([]any{
				"reason", reason,
				"drop_seq", n,
			}, attrs...)...,
		)
	}
}

func (t *GameAccountCharactersTransformer) dropsByReason(reason string) *atomic.Int64 {
	t.dropsMu.Lock()
	defer t.dropsMu.Unlock()
	c, ok := t.DropsByReason[reason]
	if !ok {
		c = &atomic.Int64{}
		t.DropsByReason[reason] = c
	}
	return c
}

// DropSnapshot 返回 drop 总数 + 按 reason 分桶的计数（线程安全）。
// 调用方在 pipe.Run 之后用：判断是否要打汇总日志。
func (t *GameAccountCharactersTransformer) DropSnapshot() (int64, map[string]int64) {
	out := make(map[string]int64, len(t.DropsByReason))
	t.dropsMu.Lock()
	for k, c := range t.DropsByReason {
		out[k] = c.Load()
	}
	t.dropsMu.Unlock()
	return t.Drops.Load(), out
}

func (t *GameAccountCharactersTransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
	// 2. parentID：必须命中 AccountMap
	parentOld, ok := t.Meta.GetInt64(row, t.ParentIDCol)
	if !ok {
		t.recordDrop("parentID-not-int64",
			"col", t.ParentIDCol,
			"row_id_col", t.IDCol,
		)
		return nil, nil
	}
	parentNew, found := t.AccountMap.Get(parentOld)
	if !found {
		t.recordDrop("parentID-not-in-AccountMap",
			"parentID", parentOld,
		)
		return nil, nil
	}

	// 1. id 自增
	newID := t.NextID()
	t.Meta.Set(row, t.IDCol, newID)

	// parentID 改写
	t.Meta.Set(row, t.ParentIDCol, parentNew)

	// 3. authDbId：非 0 才查；命中改写，未命中保留 src 原值（不是 drop）。
	// 计数归到"info" 类型方便汇总时看到"未命中改写"的次数（不属 drop）。
	if authOld, ok := t.Meta.GetInt64(row, t.AuthDbIDCol); ok && authOld != 0 {
		if authNew, found := t.AccountMap.Get(authOld); found {
			t.Meta.Set(row, t.AuthDbIDCol, authNew)
		} else {
			t.dropsByReason("authDbId-keep-src").Add(1)
		}
	}

	// 4. dbId：必须命中 AvatarMap
	dbOld, ok := t.Meta.GetInt64(row, t.DbIDCol)
	if !ok {
		t.recordDrop("dbId-not-int64",
			"col", t.DbIDCol,
			"row_id", newID,
		)
		return nil, nil
	}
	dbNew, found := t.AvatarMap.Get(dbOld)
	if !found {
		t.recordDrop("dbId-not-in-AvatarMap",
			"dbId", dbOld,
			"row_id", newID,
		)
		return nil, nil
	}
	t.Meta.Set(row, t.DbIDCol, dbNew)

	return row, nil
}