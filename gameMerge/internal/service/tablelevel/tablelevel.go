package tablelevel

import (
	"context"
	"database/sql"
	"fmt"
	"io"
	"sort"
	"strings"
)

const TablePrefix = "tbl_"

type Node struct {
	Name     string
	Level    int
	Children []*Node
}

type Tree struct {
	Root    *Node
	ByName  map[string]*Node
	ByLevel map[int][]*Node
}

func Load(ctx context.Context, db *sql.DB, entTableName string) (*Tree, error) {
	if db == nil {
		return nil, fmt.Errorf("tablelevel: nil db")
	}
	if strings.TrimSpace(entTableName) == "" {
		return nil, fmt.Errorf("tablelevel: entTableName is empty")
	}

	keyName := entTableName
	if !strings.HasPrefix(keyName, TablePrefix) {
		keyName = TablePrefix + keyName
	}

	pattern := escapeLike(keyName) + "%"
	rows, err := db.QueryContext(ctx, fmt.Sprintf("SHOW TABLES LIKE '%s'", pattern))
	if err != nil {
		return nil, fmt.Errorf("tablelevel: query tables for %q: %w", keyName, err)
	}
	defer rows.Close()

	allTables := make([]string, 0, 16)
	for rows.Next() {
		var name string
		if err := rows.Scan(&name); err != nil {
			return nil, fmt.Errorf("tablelevel: scan table name: %w", err)
		}
		allTables = append(allTables, name)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("tablelevel: iterate tables: %w", err)
	}

	filtered := make([]string, 0, len(allTables))
	hasRoot := false
	for _, t := range allTables {
		if t == keyName {
			hasRoot = true
			filtered = append(filtered, t)
			continue
		}
		if strings.HasPrefix(t, keyName+"_") {
			filtered = append(filtered, t)
		}
	}
	if !hasRoot {
		return nil, fmt.Errorf("tablelevel: root table %q not found", keyName)
	}
	if len(filtered) == 0 {
		return nil, fmt.Errorf("tablelevel: no tables found for %q", keyName)
	}

	levels := make(map[string]int, len(filtered))
	for _, t := range filtered {
		levels[t] = ComputeLevel(t, filtered)
	}

	sort.SliceStable(filtered, func(i, j int) bool {
		li, lj := levels[filtered[i]], levels[filtered[j]]
		if li != lj {
			return li < lj
		}
		return filtered[i] < filtered[j]
	})

	byName := make(map[string]*Node, len(filtered))
	byLevel := make(map[int][]*Node, len(filtered))
	var root *Node
	for _, t := range filtered {
		node := &Node{Name: t, Level: levels[t]}
		byName[t] = node
		byLevel[levels[t]] = append(byLevel[levels[t]], node)
		if t == keyName {
			root = node
			continue
		}
		if parent := FindParent(t, byName); parent != nil {
			parent.Children = append(parent.Children, node)
		}
	}

	return &Tree{Root: root, ByName: byName, ByLevel: byLevel}, nil
}

func ComputeLevel(table string, all []string) int {
	lv := 1
	for _, other := range all {
		if other != table && strings.Contains(table, other+"_") {
			lv++
		}
	}
	return lv
}

func FindParent(table string, byName map[string]*Node) *Node {
	var best *Node
	for name, n := range byName {
		if name == table {
			continue
		}
		if !strings.HasPrefix(table, name+"_") {
			continue
		}
		if best == nil || len(name) > len(best.Name) {
			best = n
		}
	}
	return best
}

func escapeLike(s string) string {
	return strings.NewReplacer(
		`\`, `\\`,
		`%`, `\%`,
		`_`, `\_`,
	).Replace(s)
}

// ChildTableNames 返回 root 之外所有节点的物理表名（按 Level 升序、同 Level 按字典序）。
// 主要给合服侧用于"枚举所有要跑的子表"。
func (t *Tree) ChildTableNames() []string {
	if t == nil {
		return nil
	}
	names := make([]string, 0, len(t.ByName))
	for name, node := range t.ByName {
		if t.Root == nil || node == t.Root {
			continue
		}
		names = append(names, name)
	}
	sort.SliceStable(names, func(i, j int) bool {
		li := t.ByName[names[i]].Level
		lj := t.ByName[names[j]].Level
		if li != lj {
			return li < lj
		}
		return names[i] < names[j]
	})
	return names
}

func (t *Tree) Print(w io.Writer) {
	if t == nil || w == nil {
		return
	}
	if t.Root == nil {
		fmt.Fprintln(w, "(empty)")
		return
	}
	printNode(w, t.Root, "", true)
}

func printNode(w io.Writer, n *Node, prefix string, isLast bool) {
	connector := "├── "
	childPrefix := prefix + "│   "
	if isLast {
		connector = "└── "
		childPrefix = prefix + "    "
	}
	fmt.Fprintf(w, "%s%s%s (level=%d)\n", prefix, connector, n.Name, n.Level)
	for i, c := range n.Children {
		printNode(w, c, childPrefix, i == len(n.Children)-1)
	}
}
