package transformer

import (
	"context"
	"log/slog"
	"sync/atomic"

	"gamemerge/internal/merger"
)

// StateKeepTransformer 是装饰型 transformer：仅当行内指定列的值落在白名单
// 内时才交给内层 transformer 处理，否则直接 drop。
//
// 触发场景：合服合并 tbl_BountyStub_bountyInfoData_bountyList 时，sm_state 为
// PRE_PUBLISH(1)/PRE_ACCEPT(3) 的行是"冻结占位、等扣款确认"的中间态（状态枚举
// 见游戏侧 server_common/gameconst.py BountyState），其确认定时器（60s）是运行
// 时定时器、不随库持久化。若把这类行合入 dst，合并服重启重建索引后它们会永久
// 占住猎物/猎人槽位（猎物不能再被悬赏、猎人不能再接单），因此只保留
// PUBLISHED(2)/ACCEPTED(4) 的有效单；被 drop 的行打 WARN 留痕（含 uuid 与双方
// gbid），已扣款项由运营按日志人工处理。
type StateKeepTransformer struct {
	Inner merger.Transformer
	Meta  merger.TableMeta
	Col   string
	Keep  map[int64]bool

	drops atomic.Int64
}

// Drops 返回累计 drop 的行数，供调用方打总结日志。
func (t *StateKeepTransformer) Drops() int64 {
	return t.drops.Load()
}

// Process：先按 Col 过滤，再交 Inner。列缺失或值取不到时按不命中处理（drop）。
func (t *StateKeepTransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
	state, ok := t.Meta.GetInt64(row, t.Col)
	if !ok || !t.Keep[state] {
		t.drops.Add(1)
		uuid, _ := t.Meta.GetInt64(row, "sm_uuid")
		gbid, _ := t.Meta.GetInt64(row, "sm_gbid")
		preyGbID, _ := t.Meta.GetInt64(row, "sm_preyGbId")
		hunterGbID, _ := t.Meta.GetInt64(row, "sm_hunterGbId")
		slog.Warn("drop non-final bounty row",
			"table", t.Meta.Name,
			"sm_state", state,
			"sm_uuid", uuid,
			"sm_gbid", gbid,
			"sm_preyGbId", preyGbID,
			"sm_hunterGbId", hunterGbID,
		)
		return nil, nil
	}
	return t.Inner.Process(ctx, row)
}
