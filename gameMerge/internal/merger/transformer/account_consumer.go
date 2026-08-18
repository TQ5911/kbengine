package transformer

import (
	"context"
	"fmt"

	"gamemerge/internal/merger"
)

// AccountConsumerTransformer 是 tbl_Account 专用 transformer，专门"消费"KBE 阶段的决策。
//
// 触发条件：紧跟在 KBETransformer 之后跑（在 Job.Run 里顺序是
// mergeKBEAccountInfosTbl → mergeAccountTbl）。它没有自己的"生产"逻辑——
// 纯消费 KBE 已经构造好的两份数据：
//   - KBE 的 idMap（src.entityDBID → dst.entityDBID，未命中+命中都填）；
//   - KBE 的 duplicated（命中的 src.entityDBID 集合，供本表也 drop）。
//
// 适用表特征：tbl_Account 这张表的 id 跟 kbe_accountinfos.entityDBID 是同一概念
// （同一个账号的 dbid 在两张表里指向同一逻辑实体），所以这张表没必要自己再去重 /
// 自增——直接照搬 KBE 的判定结果。
//
// 处理流程：
//   - src.id ∈ duplicated → drop（dst 已有此账号的 tbl_Account 行）；
//   - src.id ∈ idMap → 用映射值改写 row.id 后落 dst；
//   - 不在 idMap 里 → drop（说明 src 这条账号在 kbe 里没被授权迁移，不能瞎写）。
//
// 不要把它复用到 tbl_Account 之外——其他 root 表（tbl_Avatar / tbl_Guild）有自己的
// 偏移逻辑（见 RootTransformer），本 transformer 没有"自增 / 自偏移"的能力。
type AccountConsumerTransformer struct {
	Meta       merger.TableMeta
	AccMap     interface {
		Get(oldID int64) (int64, bool)
	}
	Duplicated interface {
		Contains(oldID int64) bool
	}
	IDCol string
}

func (t *AccountConsumerTransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
	oldID, ok := t.Meta.GetInt64(row, t.IDCol)
	if !ok {
		return nil, fmt.Errorf("account consumer: missing %s", t.IDCol)
	}
	if t.Duplicated.Contains(oldID) {
		return nil, nil
	}
	newID, found := t.AccMap.Get(oldID)
	if !found {
		return nil, nil
	}
	t.Meta.Set(row, t.IDCol, newID)
	return row, nil
}