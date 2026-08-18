package config

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestLoad(t *testing.T) {
	path := writeConfig(t, `
databases:
  game1:
    host: 127.0.0.1
    port: 3306
    username: a
    password: b
    db: src_db
    server_id: 1
  game2:
    host: 10.0.0.2
    port: 3307
    username: c
    password: d
    db: dst_db
    server_id: 2
  game3:
    host: 10.0.0.3
    port: 3306
    username: e
    password: f
    db: src2_db
    server_id: 3
merge:
  read_batch: 500
  write_batch: 100
  jobs:
    - src: game1
      dst: game2
    - src: game3
      dst: game2
`)

	cfg, err := Load(path)
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}

	if len(cfg.Databases) != 3 {
		t.Fatalf("expected 3 databases, got %d", len(cfg.Databases))
	}
	if cfg.Databases["game1"].Host != "127.0.0.1" || cfg.Databases["game1"].ServerID != 1 {
		t.Fatalf("unexpected game1: %+v", cfg.Databases["game1"])
	}
	if cfg.Databases["game2"].Port != 3307 {
		t.Fatalf("unexpected game2: %+v", cfg.Databases["game2"])
	}
	if cfg.Merge.ReadBatch != 500 || cfg.Merge.WriteBatch != 100 {
		t.Fatalf("unexpected merge batch: %+v", cfg.Merge)
	}
	if len(cfg.Merge.Jobs) != 2 {
		t.Fatalf("expected 2 jobs, got %d", len(cfg.Merge.Jobs))
	}
}

func TestLoadAppliesDefaults(t *testing.T) {
	path := writeConfig(t, `
databases:
  game1:
    host: 127.0.0.1
    port: 3306
    username: a
    password: b
    db: src
  game2:
    host: 127.0.0.1
    port: 3306
    username: a
    password: b
    db: dst
merge:
  jobs:
    - src: game1
      dst: game2
`)
	cfg, err := Load(path)
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if cfg.Merge.ReadBatch != 1000 || cfg.Merge.WriteBatch != 400 {
		t.Fatalf("defaults not applied: %+v", cfg.Merge)
	}
}

func TestLoadRejectsUnknownJobRef(t *testing.T) {
	path := writeConfig(t, `
databases:
  game1:
    host: 127.0.0.1
    port: 3306
    username: a
    password: b
    db: src
merge:
  jobs:
    - src: game1
      dst: missing
`)
	_, err := Load(path)
	if err == nil || !strings.Contains(err.Error(), "missing") {
		t.Fatalf("expected missing reference error, got %v", err)
	}
}

func TestLoadRejectsSameSrcDst(t *testing.T) {
	path := writeConfig(t, `
databases:
  game1:
    host: 127.0.0.1
    port: 3306
    username: a
    password: b
    db: src
merge:
  jobs:
    - src: game1
      dst: game1
`)
	_, err := Load(path)
	if err == nil || !strings.Contains(err.Error(), "cannot be the same") {
		t.Fatalf("expected same src/dst error, got %v", err)
	}
}

func TestLoadRequiresDatabases(t *testing.T) {
	path := writeConfig(t, `
merge:
  jobs:
    - src: a
      dst: b
`)
	_, err := Load(path)
	if err == nil || !strings.Contains(err.Error(), "databases") {
		t.Fatalf("expected databases required error, got %v", err)
	}
}

func TestLoadRequiresJobs(t *testing.T) {
	path := writeConfig(t, `
databases:
  game1:
    host: 127.0.0.1
    port: 3306
    username: a
    password: b
    db: src
`)
	_, err := Load(path)
	if err == nil || !strings.Contains(err.Error(), "merge.jobs must contain") {
		t.Fatalf("expected jobs required error, got %v", err)
	}
}

func TestLoadAppliesRootDefault(t *testing.T) {
	path := writeConfig(t, `
databases:
  game1:
    host: 127.0.0.1
    port: 3306
    username: a
    password: b
    db: src
  game2:
    host: 127.0.0.1
    port: 3306
    username: a
    password: b
    db: dst
merge:
  jobs:
    - src: game1
      dst: game2
`)
	cfg, err := Load(path)
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if cfg.Merge.Root != "Avatar" {
		t.Fatalf("Root default not applied: %q", cfg.Merge.Root)
	}
}

func TestResolve(t *testing.T) {
	cfg := &Config{
		Databases: map[string]MySQL{
			"game1": {Host: "127.0.0.1", Port: 3306, ServerID: 1},
			"game2": {Host: "10.0.0.2", Port: 3307, ServerID: 2},
		},
	}
	rj, err := cfg.Resolve(ServerPair{Src: "game1", Dst: "game2"})
	if err != nil {
		t.Fatalf("Resolve: %v", err)
	}
	if rj.SrcConfig.Host != "127.0.0.1" || rj.DstConfig.Host != "10.0.0.2" {
		t.Fatalf("unexpected resolve: %+v", rj)
	}
	if _, err := cfg.Resolve(ServerPair{Src: "x", Dst: "game2"}); err == nil {
		t.Fatal("expected error for unknown src")
	}
}

func TestLoadRejectsUnknownField(t *testing.T) {
	path := writeConfig(t, `
databases:
  game1:
    host: 127.0.0.1
    port: 3306
    username: a
    password: b
    db: src
    bogus: value
merge:
  jobs:
    - src: game1
      dst: game2
  unknown_field: 1
databases_unknown: 1
`)
	_, err := Load(path)
	if err == nil {
		t.Fatal("expected unknown field error")
	}
	if !strings.Contains(err.Error(), "bogus") && !strings.Contains(err.Error(), "unknown_field") && !strings.Contains(err.Error(), "databases_unknown") {
		t.Fatalf("error did not mention any unknown field: %v", err)
	}
}

func writeConfig(t *testing.T, content string) string {
	t.Helper()

	path := filepath.Join(t.TempDir(), "config.yaml")
	if err := os.WriteFile(path, []byte(content), 0o600); err != nil {
		t.Fatalf("write config: %v", err)
	}
	return path
}