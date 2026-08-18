package transformer

import (
	"context"

	"gamemerge/internal/merger"
)

// IDAutoIncrementTransformer 处理"主键是 id、merge 时让 dst.auto_increment 自行分配"的表。
//
// 触发条件：src 表的主键是数字 id（int / bigint + auto_increment），但 dst 已经有数据
// 或不希望沿用 src.id——典型场景是 game_account_mails 这种每服各发一条 id 的"流水 /
// 玩家数据"表。具体由 Job.mergeGameAccountMailsTbl 用，未来有同类表（流水 / 日志 /
// 玩家私有数据等）可以复用。
//
// 适用表特征：
//   - PK 是数字 id（auto_increment）；
//   - merge 时不要把 src.id 写进 dst（避免主键冲突 / 业务语义里 id 应该 per-server 独立）；
//   - 其余列都是 src → dst 1:1 透传，没有跨表外键需要重写（accountName、字符串属性等）。
//
// 处理逻辑：把 row 的 IDCol 置 nil 透传，BulkSink 写 INSERT(id=NULL)，由 dst 的
// auto_increment 分配新 id。其它列原样。若日后想换成"在 Sink 层把 colIdxs[id] = -1"
// 的等价实现，把本文件的 nil-set 删掉并在 Job helper 里设置 colIdxs 即可。
type IDAutoIncrementTransformer struct {
	Meta  merger.TableMeta
	IDCol string
}

func (t *IDAutoIncrementTransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
	t.Meta.Set(row, t.IDCol, nil)
	return row, nil
}