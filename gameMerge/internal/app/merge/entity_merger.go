package merge

import (
	"context"
	"database/sql"
	"fmt"
	"log/slog"

	mysqlinfra "gamemerge/internal/infrastructure/mysql"
	"gamemerge/internal/merger"
	"gamemerge/internal/merger/transformer"
	"gamemerge/internal/service/idmap"
)

// EntityMerger 是一次合服操作的封装：合一个 root 表（含其全部子表），
// 对应 Python 时代为每个 root（tbl_Avatar / tbl_Guild / tbl_Account 等）单独
// 写的 EntityTableMerger 链。
//
// 与 Job 的关系：
//   - Job.Run 负责 ctx、src/dst、batches、parentMap 的获取；
//   - EntityMerger.Merge 只关心 schema 推断 + 构造与执行 pipelines。
//
// 想加新 root 时只需在 cfg.Merge.Root 中改一个字符串，复用同一个 Merger。
type EntityMerger struct {
	Src        *sql.DB
	Dst        *sql.DB
	ReadBatch  int
	WriteBatch int

	// Name 是 entity 名（不带 tbl_ 前缀），例如 "Avatar" / "Guild" / "Account"。
	Name string
	// ParentMap：可选；当 root 含指向父实体的列（如 tbl_Avatar.sm_accountDBID → tbl_Account）
	// 时传入对应 idmap；tbl_Guild 这类没有 parent 列时传 nil。
	ParentMap interface {
		Get(oldID int64) (int64, bool)
	}

	// RootIDMap：Merge 成功后填充，供调用方在后续步骤 join（如
	// game_account_characters.dbId → Avatar map）。
	RootIDMap *idmap.IDMap
}

func (e *EntityMerger) Merge(ctx context.Context) error {
	if e.Src == nil || e.Dst == nil {
		return fmt.Errorf("entity merger %q: nil src/dst", e.Name)
	}

	spec, err := AnalyzeEntity(ctx, e.Dst, e.Name)
	if err != nil {
		slog.Error("analyze failed", "name", e.Name, "err", err)
		return fmt.Errorf("analyze %s: %w", e.Name, err)
	}

	rootIDMap := idmap.New(spec.Root.IDBase)
	e.RootIDMap = rootIDMap
	rootPipe, err := e.buildRootPipeline(ctx, spec.Root, rootIDMap)
	if err != nil {
		e.RootIDMap = nil
		return fmt.Errorf("root pipeline %s: %w", spec.Root.Name, err)
	}

	runners := []merger.Runner{rootPipe}
	if len(spec.Subs) > 0 {
		stages, err := e.buildSubPipelines(ctx, spec.Subs, spec.Root.Name, rootIDMap)
		if err != nil {
			e.RootIDMap = nil
			return fmt.Errorf("sub pipelines %s: %w", e.Name, err)
		}
		runners = append(runners, stages...)
	}

	for _, r := range runners {
		if err := r.Run(ctx); err != nil {
			e.RootIDMap = nil
			return err
		}
	}
	return nil
}

func (e *EntityMerger) buildRootPipeline(ctx context.Context, root RootSpec, rootIDMap *idmap.IDMap) (*merger.Pipeline, error) {
	allCols, err := mysqlinfra.ColumnsEx(ctx, e.Dst, root.Name)
	if err != nil {
		return nil, fmt.Errorf("columns %s: %w", root.Name, err)
	}
	allNames := make([]string, len(allCols))
	for i, c := range allCols {
		allNames[i] = c.Name
	}
	writeCols := mysqlinfra.WriteColumns(allCols)

	src := merger.NewCursorSource(e.Src, root.Name, root.IDCol, allNames, e.ReadBatch)

	colIdxs := make([]int, len(writeCols))
	for i, c := range writeCols {
		if idx, ok := src.Meta().Index(c); ok {
			colIdxs[i] = idx
		} else {
			colIdxs[i] = -1
		}
	}
	sink := merger.NewBulkSink(e.Dst, root.Name, writeCols, colIdxs, e.WriteBatch)
	t := &transformer.RootTransformer{
		Meta:      src.Meta(),
		IDCol:     root.IDCol,
		IDBase:    root.IDBase,
		IDMap:     rootIDMap,
		ParentCol: root.ParentCol,
		ParentMap: e.ParentMap,
	}
	return &merger.Pipeline{
		Name:    root.Name,
		Source:  src,
		Process: t,
		Sink:    sink,
		Config: merger.PipelineConfig{
			ReadBuf:    4,
			ProcessBuf: 4,
			WriteBatch: e.WriteBatch,
		},
	}, nil
}

func (e *EntityMerger) buildSubPipelines(ctx context.Context, subs []ChildSpec, rootName string, rootIDMap *idmap.IDMap) ([]merger.Runner, error) {
	// 按 Level 分组：Level 1 是 root（已在外面跑），子表从 Level 2 开始。
	// 跨 Level 必须顺序：level=N 的 parent 是 level=N-1 中的某张表，
	// 必须等父表的 pipeline 跑完把 idmap 写入 idmaps 才能 join。
	byLevel := make(map[int][]ChildSpec, 4)
	maxLevel := 0
	for _, sub := range subs {
		if sub.Level < 2 {
			slog.Warn("skip child with invalid level", "table", sub.Name, "level", sub.Level)
			continue
		}
		byLevel[sub.Level] = append(byLevel[sub.Level], sub)
		if sub.Level > maxLevel {
			maxLevel = sub.Level
		}
	}
	if len(byLevel) == 0 {
		return nil, nil
	}

	// idmaps 把所有表产出的 idmap 缓存下来：root 先填好，跑完一级就把该级所有
	// 子表的 childIDMap 注册进来，供下一级 join 父表用。
	idmaps := make(map[string]*idmap.IDMap, len(subs)+1)
	idmaps[rootName] = rootIDMap

	stages := make([]merger.Runner, 0, maxLevel-1)
	for level := 2; level <= maxLevel; level++ {
		children := byLevel[level]
		if len(children) == 0 {
			continue
		}
		pipes := make([]merger.Runner, 0, len(children))
		for _, sub := range children {
			parentMap, ok := idmaps[sub.ParentName]
			if !ok || parentMap == nil {
				slog.Warn("skip child with unknown parent",
					"table", sub.Name,
					"level", sub.Level,
					"parent", sub.ParentName,
				)
				continue
			}
			childIDMap := idmap.New(sub.IDBase)
			idmaps[sub.Name] = childIDMap
			pipe, err := transformer.BuildEntityPipeline(ctx, transformer.BuildEntityOptions{
				Src:         e.Src,
				Dst:         e.Dst,
				Table:       sub.Name,
				ParentIDCol: sub.ParentIDCol,
				IDCol:       sub.IDCol,
				IDBase:      sub.IDBase,
				ReadBatch:   e.ReadBatch,
				WriteBatch:  e.WriteBatch,
			}, parentMap, childIDMap)
			if err != nil {
				slog.Warn("skip sub table", "table", sub.Name, "err", err)
				delete(idmaps, sub.Name)
				continue
			}
			pipes = append(pipes, pipe)
		}
		if len(pipes) == 0 {
			continue
		}
		stages = append(stages, &merger.Stage{
			Name:  fmt.Sprintf("%s.level[%d][%d]", e.Name, level, len(pipes)),
			Items: pipes,
		})
	}
	return stages, nil
}