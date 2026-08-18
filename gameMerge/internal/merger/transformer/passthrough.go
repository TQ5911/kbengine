package transformer

import (
	"context"

	"gamemerge/internal/merger"
)

// PassthroughTransformer 直接把行透传给 Sink，不做任何改写，也不做冲突检测。
//
// 触发条件：在 Job.Run 末尾用（mergePassthroughTbl），处理那些不属于任何 entity 树
// 的、纯映射类表。它不是 entity 链路的一部分，所以也不会出现在 tablelevel.Tree
// 自动发现结果里。
//
// 适用表特征：
//   - 表内容是简单的"主键 + 外键"映射（如 game_guild_avatar: gbId PK + guildUUID）；
//   - 不需要重写任何 id（外键列的指向 dst 那边已经存在）；
//   - 不存在冲突——目标表在 dst 是空的或允许重复插入。
//
// 不要拿它处理以下场景：
//   - 任何包含 src → dst id 改写需求的表（用 RootTransformer / EntityTransformer）；
//   - 需要按业务键去重的表（用 KBETransformer）；
//   - 需要 join 上游映射的表（用 AccountConsumerTransformer / GameAccountCharacters）。
type PassthroughTransformer struct {
	Meta merger.TableMeta
}

func (t *PassthroughTransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
	return row, nil
}