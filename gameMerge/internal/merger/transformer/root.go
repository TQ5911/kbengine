package transformer

import (
	"context"
	"fmt"

	"gamemerge/internal/merger"
)

// RootTransformer 处理一张"通用 root 表"的"按 id 偏移 + 可选 join 父表"过程。
//
// 触发条件：在 EntityMerger.Merge 跑 root 表时自动用（entity_merger.go:106
// buildRootPipeline 内）。tbl_Avatar 和 tbl_Guild 这类"id 即业务主键"的表都走这里。
// 子表通过 tablelevel.Tree 自动发现后跑 EntityTransformer（本包内），与 root 表天然
// 串行（父 Sink.Close 后子表才起）。
//
// 适用表特征：
//   - 主键是数字（id bigint），不是字符串业务键；
//   - src 的 id 和 dst 的 id 不需要做去重，只做偏移（new = old + Base）；
//   - 可选：有指向父实体的列（如 tbl_Avatar.sm_accountDBID → tbl_Account）。
//
// 字段语义：
//   - IDCol + IDBase：必填；按 base 偏移 id 并写进 IDMap，供子表 join。
//   - ParentCol + ParentMap：可选；用于 tbl_Avatar.sm_accountDBID 这种
//     "指向 Account dbId" 的列：命中 ParentMap 才落 dst，未命中 drop。
//
// tbl_Account 不走这里——KBE 是它的 id 来源（见 KBETransformer 与
// AccountConsumerTransformer），Account 表有自己的"按业务名去重"语义，用 RootTransformer
// 会错误地把 src 的 id 直接偏移成 dst 的 id，污染 dst 现有的账号主键。
type RootTransformer struct {
	Meta      merger.TableMeta
	IDCol     string
	IDBase    int64
	IDMap     interface {
		Put(oldID, newID int64)
	}
	ParentCol string
	ParentMap interface {
		Get(oldID int64) (int64, bool)
	}
}

func (t *RootTransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
	oldID, ok := t.Meta.GetInt64(row, t.IDCol)
	if !ok {
		return nil, fmt.Errorf("root: missing %s", t.IDCol)
	}
	newID := oldID + t.IDBase
	if t.IDMap != nil {
		t.IDMap.Put(oldID, newID)
	}
	t.Meta.Set(row, t.IDCol, newID)

	if t.ParentCol != "" && t.ParentMap != nil {
		oldParent, ok := t.Meta.GetInt64(row, t.ParentCol)
		if !ok {
			return nil, nil
		}
		newParent, found := t.ParentMap.Get(oldParent)
		if !found {
			return nil, nil
		}
		t.Meta.Set(row, t.ParentCol, newParent)
	}
	return row, nil
}