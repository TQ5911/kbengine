package transformer

import (
	"context"

	"gamemerge/internal/merger"
)

// EntityTransformer 处理一张"实体子表"的"按父 id join → 重写 → 落 dst"过程。
//
// 触发条件：当一个 root 表通过 tablelevel.Tree 自动发现出它的子表时（典型前缀
// tbl_Avatar_* / tbl_Guild_* 等），每张子表都会各自跑一遍本 transformer。配
// BuildEntityPipeline 工厂一起用；父 pipeline 必须先 Sink.Close，子表才能起，
// 保证 join 父 idmap 一定能命中。
//
// 适用表特征：
//   - 有 parentID 列（指向某个父实体的 id，约定列名 parentID）；
//   - id 列是可选的（auto_increment 时 dst 自动分配，不需要我们改）；
//   - 子表之间可能互相 join（多层级），传 idMap 让 level=N 查 level=N-1 的 id。
//
// 字段语义：
//   - parentIDCol：子表中指向父实体 id 的列名（约定列名 parentID）。
//   - IDCol/IDBase：子表自有的 id 列与起始偏移（dst.subTable.max(id)+1）。
//     如果 idBase 为 0 或 IDCol 为空，表示不重写 id（dst 用 auto_increment）。
//   - parentMap：查父表的 old→new 映射；找不到映射的行直接 drop（父不存在）。
//   - idMap：可选；用于子表之间互相 join（如 level=3 查 level=2 的 id）。
//
// 不要手动构造 EntityTransformer 处理非子表场景——tbl_Account 这种 root 表由
// KBE + AccountConsumer 处理，game_account_characters 这种角色表由 GameAccountCharacters
// 自己处理。
type EntityTransformer struct {
	Meta        merger.TableMeta
	ParentIDCol string
	IDCol       string
	IDBase      int64
	ParentIDMap interface {
		Get(oldID int64) (int64, bool)
	}
	IDMap interface {
		Put(oldID, newID int64)
	}
}

// Process：单行处理。
//
//   1. 读子表 parentID 的原值；
//   2. 在父 idmap 里查新值；找不到 → 父没合并进来，安全 drop；
//   3. 改写 parentID 列为新值；
//   4. 如果配置了 IDCol + IDBase，按 base 偏移 id 并可选写进 idMap。
func (t *EntityTransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
	parentOld, ok := t.Meta.GetInt64(row, t.ParentIDCol)
	if !ok {
		// 列缺失或非 int64 视为不需要 join（与 Python 把"父不存在"等价处理）。
		return nil, nil
	}
	parentNew, found := t.ParentIDMap.Get(parentOld)
	if !found {
		// 父表没合进来 → 这条子行没意义（孤儿），丢弃。
		return nil, nil
	}
	t.Meta.Set(row, t.ParentIDCol, parentNew)

	if t.IDCol != "" {
		if oldID, ok := t.Meta.GetInt64(row, t.IDCol); ok {
			newID := oldID + t.IDBase
			if t.IDMap != nil {
				t.IDMap.Put(oldID, newID)
			}
			t.Meta.Set(row, t.IDCol, newID)
		}
	}
	return row, nil
}