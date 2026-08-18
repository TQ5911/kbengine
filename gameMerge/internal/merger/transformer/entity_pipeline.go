package transformer

import (
	"context"
	"database/sql"
	"fmt"

	mysqlinfra "gamemerge/internal/infrastructure/mysql"
	"gamemerge/internal/merger"
)

// BuildEntityOptions 是 BuildEntityPipeline 工厂函数的入参；
// 每个字段意义见 EntityTransformer 上的注释。
type BuildEntityOptions struct {
	Src         *sql.DB
	Dst         *sql.DB
	Table       string
	ParentIDCol string
	IDCol       string
	IDBase      int64
	ReadBatch   int
	WriteBatch  int
}

// BuildEntityPipeline 构造一条可立刻跑的子表 Pipeline：
//
//   1. SHOW COLUMNS 拿到 dst 全量列；
//   2. 校验 ParentIDCol / IDCol 存在；
//   3. Source 读全列；Sink 只写过滤掉 auto_increment 之后的列；
//   4. Transformer 走默认重写逻辑（EntityTransformer）。
//
// 如果 dst 表不存在或 ParentID 列缺失，会返回 error；调用方一般按 WARN 跳过、
// 不阻断整个 job。
func BuildEntityPipeline(ctx context.Context, opts BuildEntityOptions, parentMap interface {
	Get(oldID int64) (int64, bool)
}, idMap interface {
	Put(oldID, newID int64)
}) (*merger.Pipeline, error) {
	allCols, err := mysqlinfra.ColumnsEx(ctx, opts.Dst, opts.Table)
	if err != nil {
		return nil, fmt.Errorf("entity %s: columns: %w", opts.Table, err)
	}
	allNames := make([]string, len(allCols))
	for i, c := range allCols {
		allNames[i] = c.Name
	}
	if _, ok := indexOf(allNames, opts.ParentIDCol); !ok {
		return nil, fmt.Errorf("entity %s: missing required column %q", opts.Table, opts.ParentIDCol)
	}
	if opts.IDCol != "" {
		if _, ok := indexOf(allNames, opts.IDCol); !ok {
			return nil, fmt.Errorf("entity %s: missing required column %q", opts.Table, opts.IDCol)
		}
	}

	writeCols := mysqlinfra.WriteColumns(allCols)

	// 游标列固定用 id（唯一且单调）。parentID 非唯一：同一父实体的子行数
	// 超过 ReadBatch 时 `WHERE parentID > ?` 会跳过跨批边界的剩余行（静默丢
	// 数据），绝不能拿它当游标。仅在表没有 id 列（IDCol 为空）时退回
	// ParentIDCol——此时单行数不可能超过批大小的前提由调用方保证。
	cursorCol := opts.IDCol
	if cursorCol == "" {
		cursorCol = opts.ParentIDCol
	}
	src := merger.NewCursorSource(opts.Src, opts.Table, cursorCol, allNames, opts.ReadBatch)

	colIdxs := make([]int, len(writeCols))
	for i, c := range writeCols {
		if idx, ok := src.Meta().Index(c); ok {
			colIdxs[i] = idx
		} else {
			colIdxs[i] = -1
		}
	}
	sink := merger.NewBulkSink(opts.Dst, opts.Table, writeCols, colIdxs, opts.WriteBatch)
	t := &EntityTransformer{
		Meta:        src.Meta(),
		ParentIDCol: opts.ParentIDCol,
		IDCol:       opts.IDCol,
		IDBase:      opts.IDBase,
		ParentIDMap: parentMap,
		IDMap:       idMap,
	}
	return &merger.Pipeline{
		Name:    opts.Table,
		Source:  src,
		Process: t,
		Sink:    sink,
		Config: merger.PipelineConfig{
			ReadBuf:    4,
			ProcessBuf: 4,
			WriteBatch: opts.WriteBatch,
		},
	}, nil
}

// indexOf 在列名数组里线性查找；TableMeta 自身有同名方法，但 BuildEntityPipeline
// 这里只需要知道在不在，所以用最小实现避免依赖 transformer 的 Schema 视图。
func indexOf(cols []string, name string) (int, bool) {
	for i, c := range cols {
		if c == name {
			return i, true
		}
	}
	return 0, false
}