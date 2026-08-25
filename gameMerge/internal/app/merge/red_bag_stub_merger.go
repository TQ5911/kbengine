package merge

import (
	"context"
	"database/sql"
	"fmt"
	"log/slog"
	"strings"

	mysqlinfra "gamemerge/internal/infrastructure/mysql"
	"gamemerge/internal/merger"
	"gamemerge/internal/merger/transformer"
	"gamemerge/internal/service/idmap"
	"gamemerge/internal/service/tablelevel"
)

const (
	RedBagLastReleaseTimeCol  = "sm_lastReleaseTime"
)

type RedBagStubSpec struct {
	Name	string
	Root  	RedBagRootSpec
	Subs 	[]RedBagChildSpec
}

type RedBagRootSpec struct {
	Name      				string
	IDCol     				string
	LastReleaseTimeCol   	string
}

type RedBagChildSpec struct {
	Name        string
	IDCol       string
	IDBase      int64
}

// RedBagEntityMerger 是RedStub的一次合服封装：包含 RedBagStub 和 其子表
type RedBagEntityMerger struct {
	Src        *sql.DB
	Dst        *sql.DB
	ReadBatch  int
	WriteBatch int

	Name string			// RedBagStub
	ParentMap 			*idmap.IDMap
	LastReleaseTimeMap	*idmap.IDMap
}

func (e *RedBagEntityMerger) Merge(ctx context.Context) error {
	if e.Src == nil || e.Dst == nil {
		return fmt.Errorf("stub merger %q: nil src/dst", e.Name)
	}

	var err error
	e.ParentMap, err= e.GetParentMap(ctx, e.Name)
	if err != nil {
		slog.Error("get parent map error")
		return err
	}
	e.LastReleaseTimeMap, err = e.GetLastReleaseTime(ctx, e.Dst, e.Name)
	if err != nil {
		slog.Error("get time map error")
		return err
	}

	spec, err := e.AnalyzeRedBagStub(ctx, e.Dst, e.Name)
	if err != nil {
		slog.Error("analyze failed", "name", e.Name, "err", err)
		return fmt.Errorf("analyze %s: %w", e.Name, err)
	}

	rootPipe, err := e.buildRedBagRootPipeline(ctx, spec.Root)
	if err != nil {
		e.LastReleaseTimeMap = nil
		return fmt.Errorf("root pipeline %s: %w", spec.Root.Name, err)
	}

	runners := []merger.Runner{rootPipe}
	if len(spec.Subs) > 0 {
		subPipes, err := e.buildRedStubSubPipelines(ctx, spec.Subs)
		if err != nil {
			e.LastReleaseTimeMap = nil
			return fmt.Errorf("sub pipelines %s: %w", e.Name, err)
		}
		runners = append(runners, &merger.Stage{
			Name:  fmt.Sprintf("%s.children[%d]", spec.Root.Name, len(subPipes)),
			Items: subPipes,
		})
	}

	for _, r := range runners {
		if err := r.Run(ctx); err != nil {
			e.LastReleaseTimeMap = nil
			e.ParentMap = nil
			return err
		}
	}
	return nil
}

func (e *RedBagEntityMerger) buildRedBagRootPipeline(ctx context.Context, root RedBagRootSpec) (*merger.Pipeline, error) {
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
	sink := merger.NewRedBagStubBulkSink(e.Dst, root.Name, writeCols, colIdxs, e.WriteBatch)
	t := &transformer.RedStubRootTransformer{
		Meta:      src.Meta(),
		IDCol:		root.IDCol,
		LastReleaseTimeCol: RedBagLastReleaseTimeCol,
		LastReleaseTimeMap: e.LastReleaseTimeMap,
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

func (e *RedBagEntityMerger) buildRedStubSubPipelines(ctx context.Context, subs []RedBagChildSpec) ([]merger.Runner, error) {
	out := make([]merger.Runner, 0, len(subs))
	for _, sub := range subs {
		childIDMap := idmap.New(sub.IDBase)
		pipe, err := transformer.BuildEntityPipeline(ctx, transformer.BuildEntityOptions {
			Src:         e.Src,
			Dst:         e.Dst,
			Table:       sub.Name,
			ParentIDCol: DefaultParentCol,
			IDCol:       DefaultIDCol,
			IDBase:      sub.IDBase,
			ReadBatch:   e.ReadBatch,
			WriteBatch:  e.WriteBatch,
		}, e.ParentMap, childIDMap)
		if err != nil {
			slog.Warn("skip sub table", "table", sub.Name, "err", err)
			continue
		}
		out = append(out, pipe)
	}
	return out, nil
}

func (e *RedBagEntityMerger) AnalyzeRedBagStub(ctx context.Context, dst *sql.DB, name string) (*RedBagStubSpec, error) {
	if strings.TrimSpace(name) == "" {
		return nil, fmt.Errorf("analyze: empty entity name")
	}

	slog.Info("analyze start", "name", name)

	rootTable := tablelevel.TablePrefix + name
	rootCols, err := mysqlinfra.ColumnsEx(ctx, dst, rootTable)
	if err != nil {
		return nil, fmt.Errorf("analyze: root columns %s: %w", rootTable, err)
	}

	rootAllNames := make([]string, len(rootCols))
	for i, c := range rootCols {
		rootAllNames[i] = c.Name
	}

	if _, ok := findCol(rootAllNames, RedBagLastReleaseTimeCol); !ok {
		return nil, fmt.Errorf("analyze: root %s missing %q", rootTable, RedBagLastReleaseTimeCol)
	}

	spec := &RedBagStubSpec{
		Name: name,
		Root: RedBagRootSpec{
			Name:      rootTable,
			IDCol:     DefaultIDCol,
			LastReleaseTimeCol: RedBagLastReleaseTimeCol,
		},
	}

	tree, err := tablelevel.Load(ctx, dst, name)
	if err != nil {
		return spec, nil
	}

	for _, childName := range tree.ChildTableNames() {
		childCols, err := mysqlinfra.ColumnsEx(ctx, dst, childName)
		if err != nil {
			slog.Warn("child columns failed, skip", "table", childName, "err", err)
			continue
		}
		childNames := make([]string, len(childCols))
		for i, c := range childCols {
			childNames[i] = c.Name
		}
		idCol := ""
		if _, ok := findCol(childNames, DefaultIDCol); ok {
			idCol = DefaultIDCol
		}
		childBase, err := maxID(ctx, dst, childName)
		if err != nil {
			slog.Warn("child max id failed, skip", "table", childName, "err", err)
			continue
		}
		spec.Subs = append(spec.Subs, RedBagChildSpec{
			Name:        childName,
			IDCol:       idCol,
			IDBase:      childBase,
		})
	}

	slog.Info("analyze done",
		"time", e.LastReleaseTimeMap,
		"stub ", spec.Root.Name,
		"subs", len(spec.Subs),
	)
	return spec, nil
}

func (e *RedBagEntityMerger) GetLastReleaseTime(ctx context.Context, db *sql.DB, table string) (timeMap *idmap.IDMap, err error) {
	rootTable := tablelevel.TablePrefix + table
	rows, err:= db.QueryContext(ctx, fmt.Sprintf("SELECT id, %s FROM `%s`", RedBagLastReleaseTimeCol, rootTable))
	if err != nil {
		return nil, fmt.Errorf("stub: query %s err: %w", table, err)
	}
	defer rows.Close()

	timeMap = idmap.New(0)
	for rows.Next() {
		var (
			id   int64
			time int64
		)
		if err := rows.Scan(&id, &time); err != nil {
			return nil, fmt.Errorf("stub: scan %s err: %w", table, err)
		}
		timeMap.Put(id, time)
	}

	return timeMap, nil
}

func (e *RedBagEntityMerger) GetParentMap(ctx context.Context, table string) (parentMap *idmap.IDMap, err error) {
	dstRootID, err := e.RedStubRootID(ctx, e.Dst, table, "dst")
	if err != nil {
		return nil, err
	}
	srcRootID, err := e.RedStubRootID(ctx, e.Src, table, "src")
	if err != nil {
		return nil, err
	}
	if srcRootID == 0 {
		slog.Info("red stub: src has no root row, skip")
		return nil, err
	}
	parentMap = idmap.New(0)
	parentMap.Put(srcRootID, dstRootID)
	return parentMap, nil
}

func (e *RedBagEntityMerger) RedStubRootID(ctx context.Context, db *sql.DB, name string, which string) (int64, error) {
	rootTable := tablelevel.TablePrefix + name
	rows, err := db.QueryContext(ctx, fmt.Sprintf("SELECT id FROM `%s`", rootTable))
	if err != nil {
		return 0, fmt.Errorf("red bag stub: query %s root: %w", which, err)
	}
	defer rows.Close()

	ids := make([]int64, 0, 2)
	for rows.Next() {
		var id int64
		if err := rows.Scan(&id); err != nil {
			return 0, fmt.Errorf("red bag stub: scan %s root id: %w", which, err)
		}
		ids = append(ids, id)
	}
	if err := rows.Err(); err != nil {
		return 0, fmt.Errorf("red bag stub: iterate %s root: %w", which, err)
	}

	switch {
	case len(ids) == 0:
		if which == "dst" {
			return 0, fmt.Errorf("red bag stub: dst tbl_BountyStub is empty (server never ran?)")
		}
		return 0, nil
	case len(ids) > 1:
		return 0, fmt.Errorf("red bag stub: %s tbl_BountyStub has %d root rows, expect exactly 1", which, len(ids))
	}

	return ids[0], nil
}
