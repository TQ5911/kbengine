package merger_test

import (
	"context"
	"errors"
	"testing"

	"github.com/DATA-DOG/go-sqlmock"

	"gamemerge/internal/merger"
	"gamemerge/internal/merger/transformer"
)

func TestEntityTransformerDropsMissingParent(t *testing.T) {
	meta := merger.NewTableMeta("tbl_Avatar_xxx", []string{"id", "parentID", "val"})
	parentMap := &stubIDMapGet{m: map[int64]int64{1: 1001}}
	t1 := &transformer.EntityTransformer{
		Meta: meta, ParentIDCol: "parentID", IDCol: "id", IDBase: 5000,
		ParentIDMap: parentMap,
	}

	out, err := t1.Process(context.Background(), merger.Row{int64(99), int64(1), "x"})
	if err != nil || out == nil {
		t.Fatalf("expected kept row, got %v err=%v", out, err)
	}
	if out[0].(int64) != 5099 || out[1].(int64) != 1001 {
		t.Fatalf("unexpected rewrite: %v", out)
	}

	out2, err := t1.Process(context.Background(), merger.Row{int64(99), int64(999), "x"})
	if err != nil || out2 != nil {
		t.Fatalf("missing parent should drop, got %v err=%v", out2, err)
	}
}

func TestEntityTransformerRecordsSubIDMap(t *testing.T) {
	meta := merger.NewTableMeta("tbl_Avatar_xxx", []string{"id", "parentID"})
	parentMap := &stubIDMapGet{m: map[int64]int64{1: 1001}}
	idm := &stubIDMapPut{}
	t1 := &transformer.EntityTransformer{
		Meta: meta, ParentIDCol: "parentID", IDCol: "id", IDBase: 5000,
		ParentIDMap: parentMap, IDMap: idm,
	}
	out, err := t1.Process(context.Background(), merger.Row{int64(50), int64(1)})
	if err != nil {
		t.Fatalf("Process: %v", err)
	}
	if idm.m[50] != 5050 {
		t.Fatalf("sub idmap not recorded: %+v", idm.m)
	}
	if out[0].(int64) != 5050 {
		t.Fatalf("id not rewritten: %v", out)
	}
}

func TestBuildEntityPipelineRejectsTableMissingColumns(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectQuery("SHOW COLUMNS FROM `weird`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint(20) unsigned", "NO", "PRI", nil, "auto_increment"))

	_, err = transformer.BuildEntityPipeline(context.Background(), transformer.BuildEntityOptions{
		Src: db, Dst: db, Table: "weird", ParentIDCol: "parentID", IDCol: "id",
	}, &stubIDMapGet{}, nil)
	if err == nil {
		t.Fatal("expected missing parentID column error")
	}
}

func TestBuildEntityPipelineRequiresMatchingColumns(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectQuery("SHOW COLUMNS FROM `good`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint(20) unsigned", "NO", "PRI", nil, "").
			AddRow("parentID", "bigint(20) unsigned", "NO", "MUL", "0", ""))

	parentMap := &stubIDMapGet{m: map[int64]int64{1: 1001}}

	p, err := transformer.BuildEntityPipeline(context.Background(), transformer.BuildEntityOptions{
		Src: db, Dst: db, Table: "good", ParentIDCol: "parentID", IDCol: "id", IDBase: 5000,
		ReadBatch: 10, WriteBatch: 10,
	}, parentMap, nil)
	if err != nil {
		t.Fatalf("BuildEntityPipeline: %v", err)
	}

	if p.Name != "good" {
		t.Fatalf("unexpected pipeline name: %s", p.Name)
	}
	if err := mock.ExpectationsWereMet(); err != nil {
		t.Fatalf("expectations: %v", err)
	}
}

var _ = errors.New