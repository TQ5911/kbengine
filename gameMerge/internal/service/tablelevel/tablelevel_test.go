package tablelevel

import (
	"bytes"
	"context"
	"errors"
	"strings"
	"testing"

	"github.com/DATA-DOG/go-sqlmock"
)

func TestLoadBuildsTree(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	rows := sqlmock.NewRows([]string{"Tables_in_db"}).
		AddRow("tbl_Account").
		AddRow("tbl_Account_A").
		AddRow("tbl_Account_B").
		AddRow("tbl_Account_A_X").
		AddRow("tbl_Other")

	mock.ExpectQuery("SHOW TABLES LIKE 'tbl\\_Account%'").
		WillReturnRows(rows)

	tree, err := Load(context.Background(), db, "Account")
	if err != nil {
		t.Fatalf("Load: %v", err)
	}
	if err := mock.ExpectationsWereMet(); err != nil {
		t.Fatalf("expectations: %v", err)
	}

	if tree.Root == nil || tree.Root.Name != "tbl_Account" {
		t.Fatalf("unexpected root: %+v", tree.Root)
	}
	if tree.Root.Level != 1 {
		t.Fatalf("root level = %d, want 1", tree.Root.Level)
	}
	if got, want := len(tree.Root.Children), 2; got != want {
		t.Fatalf("root children = %d, want %d", got, want)
	}

	if n := tree.ByName["tbl_Account_A"]; n == nil || n.Level != 2 {
		t.Fatalf("tbl_Account_A node = %+v", n)
	}
	if n := tree.ByName["tbl_Account_A_X"]; n == nil || n.Level != 3 {
		t.Fatalf("tbl_Account_A_X node = %+v", n)
	}
	if n := tree.ByName["tbl_Account_B"]; n == nil || n.Level != 2 {
		t.Fatalf("tbl_Account_B node = %+v", n)
	}
	if _, ok := tree.ByName["tbl_Other"]; ok {
		t.Fatal("tbl_Other should be filtered out")
	}

	if got := len(tree.ByLevel[1]); got != 1 {
		t.Fatalf("level 1 count = %d, want 1", got)
	}
	if got := len(tree.ByLevel[2]); got != 2 {
		t.Fatalf("level 2 count = %d, want 2", got)
	}
	if got := len(tree.ByLevel[3]); got != 1 {
		t.Fatalf("level 3 count = %d, want 1", got)
	}

	if n := tree.ByName["tbl_Account_A_X"]; n == nil || len(n.Children) != 0 {
		t.Fatalf("leaf should have no children, got %+v", n)
	}

	if n := tree.ByName["tbl_Account_A"]; n == nil || len(n.Children) != 1 || n.Children[0].Name != "tbl_Account_A_X" {
		t.Fatalf("tbl_Account_A children = %+v", n)
	}
}

func TestLoadAcceptsPrefixedName(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectQuery("SHOW TABLES LIKE 'tbl\\_Avatar%'").
		WillReturnRows(sqlmock.NewRows([]string{"Tables_in_db"}).AddRow("tbl_Avatar").AddRow("tbl_Avatar_X"))

	tree, err := Load(context.Background(), db, "tbl_Avatar")
	if err != nil {
		t.Fatalf("Load: %v", err)
	}
	if tree.Root.Name != "tbl_Avatar" {
		t.Fatalf("unexpected root: %s", tree.Root.Name)
	}
}

func TestLoadRequiresPrefix(t *testing.T) {
	db, _, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	_, err = Load(context.Background(), db, "")
	if err == nil {
		t.Fatal("expected error for empty entTableName")
	}
}

func TestLoadRejectsNilDB(t *testing.T) {
	_, err := Load(context.Background(), nil, "Account")
	if err == nil {
		t.Fatal("expected error for nil db")
	}
}

func TestLoadErrorsWhenNoTables(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectQuery("SHOW TABLES LIKE 'tbl\\_Account%'").
		WillReturnRows(sqlmock.NewRows([]string{"Tables_in_db"}).AddRow("tbl_Account_X"))

	_, err = Load(context.Background(), db, "Account")
	if err == nil {
		t.Fatal("expected error when entity root table is missing")
	}
}

func TestLoadPropagatesQueryError(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	wantErr := errors.New("boom")
	mock.ExpectQuery("SHOW TABLES LIKE 'tbl\\_Account%'").
		WillReturnError(wantErr)

	_, err = Load(context.Background(), db, "Account")
	if err == nil {
		t.Fatal("expected error")
	}
}

func TestComputeLevel(t *testing.T) {
	all := []string{
		"tbl_Account",
		"tbl_Account_A",
		"tbl_Account_B",
		"tbl_Account_A_X",
		"tbl_Other",
	}
	cases := map[string]int{
		"tbl_Account":     1,
		"tbl_Account_A":   2,
		"tbl_Account_B":   2,
		"tbl_Account_A_X": 3,
		"tbl_Other":       1,
	}
	for table, want := range cases {
		if got := ComputeLevel(table, all); got != want {
			t.Fatalf("ComputeLevel(%q) = %d, want %d", table, got, want)
		}
	}
}

func TestFindParent(t *testing.T) {
	all := []string{"tbl_Account", "tbl_Account_A", "tbl_Account_B", "tbl_Account_A_X"}
	byName := map[string]*Node{}
	for _, n := range all {
		byName[n] = &Node{Name: n}
	}

	cases := []struct {
		table string
		want  string
	}{
		{"tbl_Account_A_X", "tbl_Account_A"},
		{"tbl_Account_A", "tbl_Account"},
		{"tbl_Account_B", "tbl_Account"},
		{"tbl_Account", ""},
	}
	for _, c := range cases {
		got := FindParent(c.table, byName)
		gotName := ""
		if got != nil {
			gotName = got.Name
		}
		if gotName != c.want {
			t.Fatalf("FindParent(%q) = %q, want %q", c.table, gotName, c.want)
		}
	}
}

func TestTablePrefixConstant(t *testing.T) {
	if TablePrefix != "tbl_" {
		t.Fatalf("TablePrefix = %q, want %q", TablePrefix, "tbl_")
	}
}

func TestTreePrint(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectQuery("SHOW TABLES LIKE 'tbl\\_Account%'").
		WillReturnRows(sqlmock.NewRows([]string{"Tables_in_db"}).
			AddRow("tbl_Account").
			AddRow("tbl_Account_A").
			AddRow("tbl_Account_A_X"))

	tree, err := Load(context.Background(), db, "Account")
	if err != nil {
		t.Fatalf("Load: %v", err)
	}

	var buf bytes.Buffer
	tree.Print(&buf)
	out := buf.String()

	for _, want := range []string{
		"tbl_Account (level=1)",
		"tbl_Account_A (level=2)",
		"tbl_Account_A_X (level=3)",
	} {
		if !strings.Contains(out, want) {
			t.Fatalf("Print output missing %q:\n%s", want, out)
		}
	}
	if strings.Count(out, "├──")+strings.Count(out, "└──") != 3 {
		t.Fatalf("expected 3 tree edges, got:\n%s", out)
	}
}