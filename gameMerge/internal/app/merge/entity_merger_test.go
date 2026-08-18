package merge

import (
	"context"
	"log/slog"
	"testing"

	"github.com/DATA-DOG/go-sqlmock"
)

func TestEntityMergerGuildEndToEnd(t *testing.T) {
	srcDB, srcMock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("src sqlmock: %v", err)
	}
	defer srcDB.Close()

	dstDB, dstMock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("dst sqlmock: %v", err)
	}
	defer dstDB.Close()

	dstMock.ExpectQuery("SHOW COLUMNS FROM `tbl_Guild`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment").
			AddRow("name", "varchar(64)", "NO", "", "", ""))

	dstMock.ExpectQuery("SELECT max(id) FROM `tbl_Guild`").
		WillReturnRows(sqlmock.NewRows([]string{"max"}).AddRow(int64(99)))

	dstMock.ExpectQuery("SHOW TABLES LIKE 'tbl\\_Guild%'").
		WillReturnRows(sqlmock.NewRows([]string{"Tables_in_db"}).
			AddRow("tbl_Guild").
			AddRow("tbl_Guild_members_members"))

	dstMock.ExpectQuery("SHOW COLUMNS FROM `tbl_Guild_members_members`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment").
			AddRow("parentID", "bigint unsigned", "NO", "MUL", "0", "").
			AddRow("gbId", "bigint unsigned", "NO", "MUL", "0", ""))

	dstMock.ExpectQuery("SELECT max(id) FROM `tbl_Guild_members_members`").
		WillReturnRows(sqlmock.NewRows([]string{"max"}).AddRow(int64(200)))

	dstMock.ExpectQuery("SHOW COLUMNS FROM `tbl_Guild`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment").
			AddRow("name", "varchar(64)", "NO", "", "", ""))

	dstMock.ExpectQuery("SHOW COLUMNS FROM `tbl_Guild_members_members`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment").
			AddRow("parentID", "bigint unsigned", "NO", "MUL", "0", "").
			AddRow("gbId", "bigint unsigned", "NO", "MUL", "0", ""))

	orig := slog.Default()
	slog.SetDefault(slog.New(slog.NewJSONHandler(devNull{}, nil)))
	t.Cleanup(func() { slog.SetDefault(orig) })

	m := &EntityMerger{
		Src:        srcDB,
		Dst:        dstDB,
		ReadBatch:  100,
		WriteBatch: 10,
		Name:       "Guild",
	}

	spec, err := AnalyzeEntity(context.Background(), dstDB, "Guild")
	if err != nil {
		t.Fatalf("AnalyzeEntity: %v", err)
	}
	if spec.Root.ParentCol != "" {
		t.Fatalf("Guild should have no parentCol, got %q", spec.Root.ParentCol)
	}
	if len(spec.Subs) != 1 || spec.Subs[0].Name != "tbl_Guild_members_members" {
		t.Fatalf("unexpected subs: %+v", spec.Subs)
	}

	rootIDMap := newIDMapStub()
	rootPipe, err := m.buildRootPipeline(context.Background(), spec.Root, rootIDMap)
	if err != nil {
		t.Fatalf("buildRootPipeline: %v", err)
	}

	subPipes, err := m.buildSubPipelines(context.Background(), spec.Subs, rootIDMap)
	if err != nil {
		t.Fatalf("buildSubPipelines: %v", err)
	}
	if len(subPipes) != 1 {
		t.Fatalf("expected 1 sub pipe, got %d", len(subPipes))
	}

	srcMock.ExpectQuery("SELECT `id`, `name` FROM `tbl_Guild` ORDER BY `id` LIMIT 100").
		WillReturnRows(sqlmock.NewRows([]string{"id", "name"}).
			AddRow(int64(1), "Alpha").
			AddRow(int64(2), "Beta").
			AddRow(int64(3), "Gamma"))

	srcMock.ExpectQuery("SELECT `id`, `name` FROM `tbl_Guild` WHERE `id` > ? ORDER BY `id` LIMIT 100").
		WithArgs(int64(3)).
		WillReturnRows(sqlmock.NewRows([]string{"id", "name"}))

	dstMock.ExpectExec("INSERT INTO `tbl_Guild` (`id`, `name`) VALUES (?, ?), (?, ?), (?, ?)").
		WithArgs(int64(101), "Alpha", int64(102), "Beta", int64(103), "Gamma").
		WillReturnResult(sqlmock.NewResult(3, 3))

	if err := rootPipe.Run(context.Background()); err != nil {
		t.Fatalf("root.Run: %v", err)
	}

	srcMock.ExpectQuery("SELECT `id`, `parentID`, `gbId` FROM `tbl_Guild_members_members` ORDER BY `id` LIMIT 100").
		WillReturnRows(sqlmock.NewRows([]string{"id", "parentID", "gbId"}).
			AddRow(int64(10), int64(1), int64(1001)).
			AddRow(int32(11), int32(1), int32(1002)).
			AddRow(int32(12), int32(2), int32(1003)).
			AddRow(int32(99), int32(999), int32(1004)).
			AddRow(int32(13), int32(3), int32(1005)))

	srcMock.ExpectQuery("SELECT `id`, `parentID`, `gbId` FROM `tbl_Guild_members_members` WHERE `id` > ? ORDER BY `id` LIMIT 100").
		WithArgs(int64(13)).
		WillReturnRows(sqlmock.NewRows([]string{"id", "parentID", "gbId"}))

	dstMock.ExpectExec("INSERT INTO `tbl_Guild_members_members` (`id`, `parentID`, `gbId`) VALUES (?, ?, ?), (?, ?, ?), (?, ?, ?), (?, ?, ?)").
		WithArgs(int64(211), int64(101), int64(1001),
			int64(212), int64(101), int64(1002),
			int64(213), int64(102), int64(1003),
			int64(214), int64(103), int64(1005)).
		WillReturnResult(sqlmock.NewResult(4, 4))

	if err := subPipes[0].Run(context.Background()); err != nil {
		t.Fatalf("sub.Run: %v", err)
	}

	if err := srcMock.ExpectationsWereMet(); err != nil {
		t.Fatalf("src expectations: %v", err)
	}
	if err := dstMock.ExpectationsWereMet(); err != nil {
		t.Fatalf("dst expectations: %v", err)
	}
}

type devNull struct{}

func (devNull) Write(p []byte) (int, error) { return len(p), nil }