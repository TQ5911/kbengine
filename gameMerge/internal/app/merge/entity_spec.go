package merge

import (
	"context"
	"database/sql"
	"fmt"
	"log/slog"
	"strings"

	mysqlinfra "gamemerge/internal/infrastructure/mysql"
	"gamemerge/internal/service/tablelevel"
)

const (
	DefaultIDCol      = "id"
	DefaultParentCol  = "parentID"
	AccountIDCol      = "sm_accountDBID"
)

// EntitySpec 是 Run 一个 root 表（含其子表）所需的全部 schema 描述。
//
// 设计目标：tbl_Avatar / tbl_Account / tbl_Guild 等根表共用同一套构建与执行
// 逻辑；差异仅来源于 dst schema（列名、是否有指向 Account 的列等）。
//
// 调用方通过 AnalyzeEntity 从 dst schema 推断得到一个 Spec；
// 之后用同一个 Spec 构造并执行 Pipeline。
type EntitySpec struct {
	Name string // 用户传入的 entity 名（不带 tbl_ 前缀，会自动补上）
	Root RootSpec
	Subs []ChildSpec
}

type RootSpec struct {
	Name      string // 物理表名，含 tbl_ 前缀
	IDCol     string
	IDBase    int64
	ParentCol string // 可选：指向父表（典型 tbl_Avatar.sm_accountDBID），空表示不重写父列
}

type ChildSpec struct {
	Name        string
	ParentIDCol string
	IDCol       string
	IDBase      int64
}

// AnalyzeEntity 通过 dst schema 推断 EntitySpec。
//
// 推断规则：
//   - root 表必须存在，且有 IDCol（默认 "id"）。
//   - IDBase = max(dst.Root.id) + 1；不存在任何行时取 0。
//   - 如果 root 存在 AccountIDCol（"sm_accountDBID"），Root.ParentCol = "sm_accountDBCol"，
//     表示 tbl_Avatar 这类带"指向 Account 的 dbId 列"的根表。
//   - 子表通过 tablelevel.Load 发现（基于 dst schema），约定 ParentIDCol = "parentID"，
//     IDCol = "id"。child.IDBase 同样取 max(dst.child.id) + 1；
//     如果子表没有 ParentIDCol 列，整个子表被跳过（视为非子树）。
func AnalyzeEntity(ctx context.Context, dst *sql.DB, name string) (*EntitySpec, error) {
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

	if _, ok := findCol(rootAllNames, DefaultIDCol); !ok {
		return nil, fmt.Errorf("analyze: root %s missing %q", rootTable, DefaultIDCol)
	}

	rootBase, err := maxID(ctx, dst, rootTable)
	if err != nil {
		return nil, fmt.Errorf("analyze: root base %s: %w", rootTable, err)
	}

	parentCol := ""
	if _, ok := findCol(rootAllNames, AccountIDCol); ok {
		parentCol = AccountIDCol
	}

	spec := &EntitySpec{
		Name: name,
		Root: RootSpec{
			Name:      rootTable,
			IDCol:     DefaultIDCol,
			IDBase:    rootBase,
			ParentCol: parentCol,
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
		if _, ok := findCol(childNames, DefaultParentCol); !ok {
			continue
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
		spec.Subs = append(spec.Subs, ChildSpec{
			Name:        childName,
			ParentIDCol: DefaultParentCol,
			IDCol:       idCol,
			IDBase:      childBase,
		})
	}

	slog.Info("analyze done",
		"root", spec.Root.Name,
		"id_base", spec.Root.IDBase,
		"parent_col", spec.Root.ParentCol,
		"subs", len(spec.Subs),
	)
	return spec, nil
}

func maxID(ctx context.Context, db *sql.DB, table string) (int64, error) {
	var v sql.NullInt64
	row := db.QueryRowContext(ctx, fmt.Sprintf("SELECT max(id) FROM `%s`", table))
	if err := row.Scan(&v); err != nil {
		return 0, fmt.Errorf("max id %s: %w", table, err)
	}
	if !v.Valid {
		return 0, nil
	}
	return v.Int64 + 1, nil
}

func findCol(cols []string, name string) (int, bool) {
	for i, c := range cols {
		if c == name {
			return i, true
		}
	}
	return 0, false
}
