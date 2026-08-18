package transformer

import (
	"context"
	"fmt"

	"gamemerge/internal/merger"
)

// KBETransformer 处理 kbe_accountinfos 这张"KBE 账号字典表"。
//
// 触发条件：合服链路的最开始跑这一张，因为后续所有的账号相关 id（tbl_Account.id、
// game_account_characters.parentID/authDbId 等）都要从这里产出的映射回填。
// 具体由 Job.mergeKBEAccountInfosTbl 构造并跑。
//
// 适用表特征：
//   - 业务键（business key）是字符串（如 accountName varchar(128)）；
//   - 主键即业务键，不需要 auto_increment id；
//   - 含 entityDBID 列指向 tbl_Account.id。
//
// 处理流程：
//   - 命中 DstAccount（账号名重复）→ 视为 dst 已存在账号，drop 当前 kbe 行。
//   - 未命中 → 按 Base 偏移 oldDBID 作为 newDBID 写入 row。
//
// 同步写两份映射给下游消费，语义不同不要混用：
//   - IDMap：完整 src.entityDBID → dst.entityDBID（命中与未命中都填），给"需要 remap
//     FK 列"的下游用（典型如 game_account_characters.parentID / authDbId remap）。
//     命中时值 = dst 已有 id（不是新分配）。
//   - Duplicated：仅命中 src.entityDBID 集合（KBE 已 drop 的行），给"自己也要 drop
//     同 id 行"的下游用（典型如 AccountConsumerTransformer 的 tbl_Account merge）。
//
// 历史上命中分支只写 Duplicated 不写 IDMap，导致 game_account_characters 拿到
// 不完整的 accMap，命中账号的所有角色行被静默 drop。现在两个 map 都写，保证 accMap
// 全量覆盖。
//
// 不要把它复用到非 KBE 账号字典的表——它的去重键是字符串业务名、id 生成是简单
// `oldID + Base` 偏移，跟 Numeric PK 表的语义完全不同。
type KBETransformer struct {
	Meta       merger.TableMeta
	DstAccount interface {
		Lookup(name string) (DBID int64, ok bool)
	}
	Duplicated interface {
		Put(srcDBID, dstDBID int64)
	}
	IDMap interface {
		Put(oldID, newID int64)
	}
	Base        int64
	NameCol     string
	EntityDBCol string
}

func (t *KBETransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
	name, ok := t.Meta.String(row, t.NameCol)
	if !ok {
		return nil, fmt.Errorf("kbe: missing or non-string %s", t.NameCol)
	}
	oldDBID, ok := t.Meta.GetInt64(row, t.EntityDBCol)
	if !ok {
		return nil, fmt.Errorf("kbe: missing %s", t.EntityDBCol)
	}

	if dst, found := t.DstAccount.Lookup(name); found {
		// 命中：drop 当前 kbe 行，映射同时写 Duplicated 和 IDMap。
		//   - Duplicated: 供 tbl_Account 的 AccountConsumerTransformer drop 同 id 行
		//   - IDMap:      供 game_account_characters 等 remap parentID / authDbId
		// 命中时 dst 已有该账号，IDMap 值 = dst.id（不是新分配）。
		t.Duplicated.Put(oldDBID, dst)
		t.IDMap.Put(oldDBID, dst)
		return nil, nil
	}

	// 未命中：按 Base 偏移生成 new id，写入 row 与 IDMap
	newDBID := oldDBID + t.Base
	t.IDMap.Put(oldDBID, newDBID)
	t.Meta.Set(row, t.EntityDBCol, newDBID)
	return row, nil
}

// DuplicatedSet 记录 KBE 命中的 src.entityDBID，供 tbl_Account merge 时一起 drop。
// 不导出方法集（只暴露 Put/Contains），避免与 idmap.IDMap 混淆。
type DuplicatedSet struct {
	m map[int64]struct{}
}

func NewDuplicatedSet() *DuplicatedSet {
	return &DuplicatedSet{m: make(map[int64]struct{})}
}

func (s *DuplicatedSet) Put(srcDBID, _ int64) {
	s.m[srcDBID] = struct{}{}
}

func (s *DuplicatedSet) Contains(srcDBID int64) bool {
	_, ok := s.m[srcDBID]
	return ok
}

func (s *DuplicatedSet) Len() int { return len(s.m) }