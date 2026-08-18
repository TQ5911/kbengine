package merge

import (
	"context"
	"strings"
	"testing"

	"github.com/DATA-DOG/go-sqlmock"
)

func TestAnalyzeEntityRequiresIDColumn(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectQuery("SHOW COLUMNS FROM `tbl_Avatar`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("name", "varchar(64)", "NO", "", nil, ""))

	_, err = AnalyzeEntity(context.Background(), db, "Avatar")
	if err == nil || !strings.Contains(err.Error(), "missing") {
		t.Fatalf("expected missing id error, got %v", err)
	}
}

func TestAnalyzeEntityInfersAvatarSpec(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectQuery("SHOW COLUMNS FROM `tbl_Avatar`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment").
			AddRow("sm_accountDBID", "bigint unsigned", "NO", "MUL", "0", "").
			AddRow("name", "varchar(64)", "NO", "", "", ""))

	mock.ExpectQuery("SELECT max(id) FROM `tbl_Avatar`").
		WillReturnRows(sqlmock.NewRows([]string{"max"}).AddRow(nil))

	mock.ExpectQuery("SHOW TABLES LIKE 'tbl\\_Avatar%'").
		WillReturnRows(sqlmock.NewRows([]string{"Tables_in_db"}).
			AddRow("tbl_Avatar").
			AddRow("tbl_Avatar_subA"))

	mock.ExpectQuery("SHOW COLUMNS FROM `tbl_Avatar_subA`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment").
			AddRow("parentID", "bigint unsigned", "NO", "MUL", "0", ""))

	mock.ExpectQuery("SELECT max(id) FROM `tbl_Avatar_subA`").
		WillReturnRows(sqlmock.NewRows([]string{"max"}).AddRow(nil))

	spec, err := AnalyzeEntity(context.Background(), db, "Avatar")
	if err != nil {
		t.Fatalf("AnalyzeEntity: %v", err)
	}

	if spec.Root.Name != "tbl_Avatar" {
		t.Fatalf("unexpected root name: %s", spec.Root.Name)
	}
	if spec.Root.IDCol != "id" || spec.Root.ParentCol != "sm_accountDBID" {
		t.Fatalf("unexpected root spec: %+v", spec.Root)
	}

	if len(spec.Subs) != 1 {
		t.Fatalf("expected 1 sub, got %d (%+v)", len(spec.Subs), spec.Subs)
	}
	if spec.Subs[0].Name != "tbl_Avatar_subA" {
		t.Fatalf("unexpected sub: %+v", spec.Subs[0])
	}
	if spec.Subs[0].ParentIDCol != "parentID" || spec.Subs[0].IDCol != "id" {
		t.Fatalf("unexpected sub cols: %+v", spec.Subs[0])
	}
}

func TestAnalyzeEntityNoParentColStaysEmpty(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectQuery("SHOW COLUMNS FROM `tbl_Guild`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment").
			AddRow("name", "varchar(64)", "NO", "", "", ""))

	mock.ExpectQuery("SELECT max(id) FROM `tbl_Guild`").
		WillReturnRows(sqlmock.NewRows([]string{"max"}).AddRow(int64(99)))

	spec, err := AnalyzeEntity(context.Background(), db, "Guild")
	if err != nil {
		t.Fatalf("AnalyzeEntity: %v", err)
	}
	if spec.Root.ParentCol != "" {
		t.Fatalf("expected no parentCol, got %q", spec.Root.ParentCol)
	}
	if spec.Root.IDBase != 100 {
		t.Fatalf("expected base=100, got %d", spec.Root.IDBase)
	}
	if len(spec.Subs) != 0 {
		t.Fatalf("expected 0 subs, got %d", len(spec.Subs))
	}
}

func TestAnalyzeEntityGuildWithSubs(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectQuery("SHOW COLUMNS FROM `tbl_Guild`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment").
			AddRow("name", "varchar(64)", "NO", "", "", "").
			AddRow("level", "int unsigned", "NO", "", "0", ""))

	mock.ExpectQuery("SELECT max(id) FROM `tbl_Guild`").
		WillReturnRows(sqlmock.NewRows([]string{"max"}).AddRow(int64(200)))

	mock.ExpectQuery("SHOW TABLES LIKE 'tbl\\_Guild%'").
		WillReturnRows(sqlmock.NewRows([]string{"Tables_in_db"}).
			AddRow("tbl_Guild").
			AddRow("tbl_Guild_members_members").
			AddRow("tbl_Guild_applyJoins_applyJoins").
			AddRow("tbl_Guild_orphanA"))

	mock.ExpectQuery("SHOW COLUMNS FROM `tbl_Guild_applyJoins_applyJoins`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment").
			AddRow("parentID", "bigint unsigned", "NO", "MUL", "0", ""))

	mock.ExpectQuery("SELECT max(id) FROM `tbl_Guild_applyJoins_applyJoins`").
		WillReturnRows(sqlmock.NewRows([]string{"max"}).AddRow(nil))

	mock.ExpectQuery("SHOW COLUMNS FROM `tbl_Guild_members_members`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment").
			AddRow("parentID", "bigint unsigned", "NO", "MUL", "0", "").
			AddRow("gbId", "bigint unsigned", "NO", "MUL", "0", ""))

	mock.ExpectQuery("SELECT max(id) FROM `tbl_Guild_members_members`").
		WillReturnRows(sqlmock.NewRows([]string{"max"}).AddRow(int64(5000)))

	mock.ExpectQuery("SHOW COLUMNS FROM `tbl_Guild_orphanA`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment"))

	spec, err := AnalyzeEntity(context.Background(), db, "Guild")
	if err != nil {
		t.Fatalf("AnalyzeEntity: %v", err)
	}

	if spec.Root.ParentCol != "" {
		t.Fatalf("Guild has no sm_accountDBID, ParentCol should be empty, got %q", spec.Root.ParentCol)
	}
	if spec.Root.IDBase != 201 {
		t.Fatalf("expected base=201, got %d", spec.Root.IDBase)
	}
	if len(spec.Subs) != 2 {
		t.Fatalf("expected 2 valid subs (orphanA skipped), got %d (%+v)", len(spec.Subs), spec.Subs)
	}

	names := []string{spec.Subs[0].Name, spec.Subs[1].Name}
	if !containsAll(names, "tbl_Guild_applyJoins_applyJoins", "tbl_Guild_members_members") {
		t.Fatalf("unexpected sub names: %v", names)
	}

	for _, s := range spec.Subs {
		if s.ParentIDCol != "parentID" {
			t.Fatalf("sub %s: ParentIDCol = %q", s.Name, s.ParentIDCol)
		}
		if s.IDCol != "id" {
			t.Fatalf("sub %s: IDCol = %q", s.Name, s.IDCol)
		}
	}

	var members ChildSpec
	for _, s := range spec.Subs {
		if s.Name == "tbl_Guild_members_members" {
			members = s
		}
	}
	if members.IDBase != 5001 {
		t.Fatalf("expected members IDBase=5001, got %d", members.IDBase)
	}
}

func containsAll(haystack []string, needles ...string) bool {
	set := make(map[string]bool, len(haystack))
	for _, s := range haystack {
		set[s] = true
	}
	for _, n := range needles {
		if !set[n] {
			return false
		}
	}
	return true
}

func TestAnalyzeEntityRejectsEmptyName(t *testing.T) {
	db, _, err := sqlmock.New()
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	_, err = AnalyzeEntity(context.Background(), db, "")
	if err == nil {
		t.Fatal("expected error for empty name")
	}
}

func TestAnalyzeEntitySkipsChildrenWithoutParentID(t *testing.T) {
	db, mock, err := sqlmock.New(sqlmock.QueryMatcherOption(sqlmock.QueryMatcherEqual))
	if err != nil {
		t.Fatalf("sqlmock.New: %v", err)
	}
	defer db.Close()

	mock.ExpectQuery("SHOW COLUMNS FROM `tbl_Avatar`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment"))

	mock.ExpectQuery("SELECT max(id) FROM `tbl_Avatar`").
		WillReturnRows(sqlmock.NewRows([]string{"max"}).AddRow(nil))

	mock.ExpectQuery("SHOW TABLES LIKE 'tbl\\_Avatar%'").
		WillReturnRows(sqlmock.NewRows([]string{"Tables_in_db"}).
			AddRow("tbl_Avatar").
			AddRow("tbl_Avatar_orphanA"))

	mock.ExpectQuery("SHOW COLUMNS FROM `tbl_Avatar_orphanA`").
		WillReturnRows(sqlmock.NewRows([]string{"Field", "Type", "Null", "Key", "Default", "Extra"}).
			AddRow("id", "bigint unsigned", "NO", "PRI", nil, "auto_increment"))

	spec, err := AnalyzeEntity(context.Background(), db, "Avatar")
	if err != nil {
		t.Fatalf("AnalyzeEntity: %v", err)
	}
	if len(spec.Subs) != 0 {
		t.Fatalf("orphan sub should be skipped, got %d", len(spec.Subs))
	}
}