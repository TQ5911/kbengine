package merge

import (
	"context"
	"database/sql"
	"fmt"
	"log/slog"

	mysqlinfra "gamemerge/internal/infrastructure/mysql"
	"gamemerge/internal/merger/transformer"
	"gamemerge/internal/service/idmap"
	"gamemerge/internal/service/tablelevel"
)

// bountyListTbl 是 BountyStub 悬赏单数组的子表名。BOUNTY_INFO 是 FIXED_DICT，
// 其唯一 key bountyList 为 ARRAY of BOUNTY_ITEM_VAL；KBE 对 ARRAY 无条件建子表，
// 表名 = 父表 + dict 属性名 + array key 名。此处只需精确匹配这一张表来挂状态
// 过滤器，其余子表照常追加。
const bountyListTbl = "tbl_BountyStub_bountyInfoData_bountyList"

// bountyKeepStates 是可以合并的悬赏单状态：PUBLISHED(2) / ACCEPTED(4)。
// 状态枚举见游戏侧 server_common/gameconst.py BountyState。
var bountyKeepStates = map[int64]bool{2: true, 4: true}

// mergeBountyStubTbl 合并归档全局单例 BountyStub 的数据（悬赏单 + 猎人榜）。
//
// 与 Avatar/Guild 的整树合并不同：BountyStub 每服有且只有一行 root（其 dbid
// 登记在 dst 的 game_entity_dbid，该表不随合服改动），绝不能向 dst 的
// tbl_BountyStub 再插第二行（否则起服加载出两个全局单例）。因此这里只把
// src 的子表行追加到 dst 既有 root 行之下：
//
//   - parentID：src 子行的 parentID 恒等于 src root id，构造单条目 idmap
//     {srcRootID: dstRootID} 喂给 EntityTransformer 完成 join 改写；
//   - id：按 max(dst.child.id)+1 偏移；多 src 合同一 dst 时 job 串行，天然错开；
//   - 其余列全部透传（悬赏单 uuid 跨服不撞号、玩家 gbid 含 serverId 不冲突）。
//
// 悬赏单子表额外过一道 StateKeepTransformer：只保留 PUBLISHED/ACCEPTED 的
// 有效单，中间态行合入后会在合并服永久占住玩家槽位（详见该 transformer 注释）。
//
// 合并后的自愈由服务端完成：合并服首启时 BountyStub.__init__ 从子表重建全部
// 内存索引/公开榜/过期堆，玩家上线时 initQueryBountyInfo 重建 Avatar 侧副本。
func (j *Job) mergeBountyStubTbl(ctx context.Context) error {
	slog.Info("bounty stub merge start")

	dstRootID, err := bountyStubRootID(ctx, j.Dst, "dst")
	if err != nil {
		return err
	}
	srcRootID, err := bountyStubRootID(ctx, j.Src, "src")
	if err != nil {
		return err
	}
	if srcRootID == 0 {
		slog.Info("bounty stub: src has no root row, skip")
		return nil
	}

	// 单条目父映射：src 所有子行的 parentID 都是 srcRootID；个别 parentID
	// 不匹配的孤儿行会被 EntityTransformer 自动 drop。
	parentMap := idmap.New(0)
	parentMap.Put(srcRootID, dstRootID)

	// 子表从 dst schema 自动发现（与 AnalyzeEntity 同一哲学，不手写枚举，
	// 未来 BOUNTY_INFO 加新 ARRAY 字段也能自动覆盖）。
	tree, err := tablelevel.Load(ctx, j.Dst, "BountyStub")
	if err != nil {
		return fmt.Errorf("bounty stub: load tables: %w", err)
	}

	for _, child := range tree.ChildTableNames() {
		cols, err := mysqlinfra.ColumnsEx(ctx, j.Dst, child)
		if err != nil {
			slog.Warn("bounty stub child columns failed, skip", "table", child, "err", err)
			continue
		}
		names := make([]string, len(cols))
		for i, c := range cols {
			names[i] = c.Name
		}
		if _, ok := findCol(names, DefaultParentCol); !ok {
			continue
		}
		childBase, err := maxID(ctx, j.Dst, child)
		if err != nil {
			slog.Warn("bounty stub child max id failed, skip", "table", child, "err", err)
			continue
		}

		pipe, err := transformer.BuildEntityPipeline(ctx, transformer.BuildEntityOptions{
			Src:         j.Src,
			Dst:         j.Dst,
			Table:       child,
			ParentIDCol: DefaultParentCol,
			IDCol:       DefaultIDCol,
			IDBase:      childBase,
			ReadBatch:   j.ReadBatch,
			WriteBatch:  j.WriteBatch,
		}, parentMap, nil)
		if err != nil {
			slog.Warn("bounty stub skip sub table", "table", child, "err", err)
			continue
		}

		var filter *transformer.StateKeepTransformer
		if child == bountyListTbl {
			filter = &transformer.StateKeepTransformer{
				Inner: pipe.Process,
				Meta:  pipe.Source.Meta(),
				Col:   "sm_state",
				Keep:  bountyKeepStates,
			}
			pipe.Process = filter
		}

		// 数据量小（两张子表），串行跑即可。
		if err := pipe.Run(ctx); err != nil {
			return fmt.Errorf("bounty stub: merge %s: %w", child, err)
		}
		if filter != nil && filter.Drops() > 0 {
			slog.Warn("bounty stub dropped non-final bounty rows",
				"table", child, "drops", filter.Drops())
		}
	}

	slog.Info("bounty stub merge done", "src_root", srcRootID, "dst_root", dstRootID)
	return nil
}

// bountyStubRootID 返回 tbl_BountyStub 唯一 root 行的 id。which 只用于报错
// 文案（"src"/"dst"）。src 侧允许 0 行（返回 0, nil，表示该服没数据可合）；
// 其余情况（dst 0 行、任意侧多行）都视为异常报错。
func bountyStubRootID(ctx context.Context, db *sql.DB, which string) (int64, error) {
	rows, err := db.QueryContext(ctx, "SELECT id FROM `tbl_BountyStub`")
	if err != nil {
		return 0, fmt.Errorf("bounty stub: query %s root: %w", which, err)
	}
	defer rows.Close()

	ids := make([]int64, 0, 2)
	for rows.Next() {
		var id int64
		if err := rows.Scan(&id); err != nil {
			return 0, fmt.Errorf("bounty stub: scan %s root id: %w", which, err)
		}
		ids = append(ids, id)
	}
	if err := rows.Err(); err != nil {
		return 0, fmt.Errorf("bounty stub: iterate %s root: %w", which, err)
	}

	switch {
	case len(ids) == 0:
		if which == "dst" {
			return 0, fmt.Errorf("bounty stub: dst tbl_BountyStub is empty (server never ran?)")
		}
		return 0, nil
	case len(ids) > 1:
		return 0, fmt.Errorf("bounty stub: %s tbl_BountyStub has %d root rows, expect exactly 1", which, len(ids))
	}
	return ids[0], nil
}
