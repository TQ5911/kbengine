package merger_test

import (
	"context"
	"testing"

	"github.com/DATA-DOG/go-sqlmock"

	"gamemerge/internal/merger"
)

func TestCursorSourceReadsInBatches(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	meta := merger.NewTableMeta("kbe_accountinfos", []string{"accountName", "entityDBID"})
	src := merger.NewCursorSource(db, "kbe_accountinfos", "accountName", meta.Columns, 2)

	rows1 := sqlmock.NewRows([]string{"accountName", "entityDBID"}).
		AddRow("alice", int64(10)).
		AddRow("bob", int64(20))
	mock.ExpectQuery("SELECT `accountName`, `entityDBID` FROM `kbe_accountinfos` ORDER BY `accountName` LIMIT 2").
		WillReturnRows(rows1)

	rows2 := sqlmock.NewRows([]string{"accountName", "entityDBID"}).
		AddRow("carol", int64(30))
	mock.ExpectQuery("SELECT `accountName`, `entityDBID` FROM `kbe_accountinfos` WHERE `accountName` > ? ORDER BY `accountName` LIMIT 2").
		WithArgs("bob").
		WillReturnRows(rows2)

	mock.ExpectQuery("SELECT `accountName`, `entityDBID` FROM `kbe_accountinfos` WHERE `accountName` > ? ORDER BY `accountName` LIMIT 2").
		WithArgs("carol").
		WillReturnRows(sqlmock.NewRows([]string{"accountName", "entityDBID"}))

	want := []struct {
		name string
		dbid int64
	}{
		{"alice", 10}, {"carol", 30},
	}
	for i, w := range want {
		batch, err := src.Next(context.Background())
		if err != nil {
			t.Fatalf("Next #%d: %v", i, err)
		}
		if len(batch) == 0 {
			t.Fatalf("batch %d empty", i)
		}
		first := batch[0]
		if first[0] != w.name {
			t.Fatalf("batch %d first name = %v, want %s", i, first[0], w.name)
		}
	}

	if _, err := src.Next(context.Background()); err != merger.ErrSourceDone {
		t.Fatalf("expected ErrSourceDone, got %v", err)
	}
	if err := mock.ExpectationsWereMet(); err != nil {
		t.Fatalf("expectations: %v", err)
	}
}

func TestBulkSinkInsertsBatchedRows(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectExec("INSERT INTO `t` (`id`, `name`) VALUES (?, ?), (?, ?), (?, ?)").
		WithArgs(int64(1), "a", int64(2), "b", int64(3), "c").
		WillReturnResult(sqlmock.NewResult(3, 3))

	sink := merger.NewBulkSink(db, "t", []string{"id", "name"}, []int{0, 1}, 10)
	err = sink.Submit(context.Background(), []merger.Row{
		{int64(1), "a"},
		{int64(2), "b"},
		{int64(3), "c"},
	})
	if err != nil {
		t.Fatalf("Submit: %v", err)
	}
	if err := mock.ExpectationsWereMet(); err != nil {
		t.Fatalf("expectations: %v", err)
	}
}

func TestBulkSinkRespectsColIdxs(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectExec("INSERT INTO `t` (`name`) VALUES (?), (?)").
		WithArgs("a", "b").
		WillReturnResult(sqlmock.NewResult(2, 2))

	sink := merger.NewBulkSink(db, "t", []string{"name"}, []int{1}, 10)
	err = sink.Submit(context.Background(), []merger.Row{
		{int64(101), "a"},
		{int64(102), "b"},
	})
	if err != nil {
		t.Fatalf("Submit: %v", err)
	}
	if err := mock.ExpectationsWereMet(); err != nil {
		t.Fatalf("expectations: %v", err)
	}
}