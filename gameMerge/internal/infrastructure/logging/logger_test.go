package logging

import (
	"bytes"
	"context"
	"log/slog"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"
	"time"
)

func TestNewWritesToDailyFile(t *testing.T) {
	dir := t.TempDir()

	logger, err := New(Options{Dir: dir, FilePrefix: "test", Level: LevelInfo})
	if err != nil {
		t.Fatalf("New() error = %v", err)
	}
	t.Cleanup(func() { _ = logger.Close() })

	logger.Info("hello", "k", "v")

	if err := logger.Close(); err != nil {
		t.Fatalf("Close() error = %v", err)
	}

	path, content := readLogFile(t, dir, "test")
	if !strings.Contains(content, `"msg":"hello"`) {
		t.Fatalf("log content missing hello message, got: %s", content)
	}
	if !strings.Contains(content, `"k":"v"`) {
		t.Fatalf("log content missing kv pair, got: %s", content)
	}
	if !strings.Contains(content, `"level":"INFO"`) {
		t.Fatalf("log content missing level, got: %s", content)
	}

	if filepath.Base(path) != "test-"+nowUTCDate()+".log" {
		t.Fatalf("unexpected log filename: %s", path)
	}
}

func TestNewRejectsUnwritableDir(t *testing.T) {
	if os.Getuid() == 0 {
		t.Skip("running as root, permission checks are not effective")
	}
	if skipWindowsPermissionTest() {
		t.Skip("POSIX permission bits are not enforced on Windows for the current user")
	}

	dir := t.TempDir()
	readOnly := filepath.Join(dir, "ro")
	if err := os.Mkdir(readOnly, 0o555); err != nil {
		t.Fatalf("mkdir: %v", err)
	}

	_, err := New(Options{Dir: filepath.Join(readOnly, "nested"), FilePrefix: "x"})
	if err == nil {
		t.Fatal("expected error when log directory is not writable")
	}
}

func TestParseLevel(t *testing.T) {
	cases := []struct {
		in      string
		want    Level
		wantErr bool
	}{
		{"", LevelInfo, false},
		{"INFO", LevelInfo, false},
		{"debug", LevelDebug, false},
		{"warn", LevelWarn, false},
		{"warning", LevelWarn, false},
		{"error", LevelError, false},
		{"trace", LevelInfo, true},
	}
	for _, c := range cases {
		got, err := ParseLevel(c.in)
		if (err != nil) != c.wantErr {
			t.Fatalf("ParseLevel(%q) err = %v, wantErr = %v", c.in, err, c.wantErr)
		}
		if !c.wantErr && got != c.want {
			t.Fatalf("ParseLevel(%q) = %v, want %v", c.in, got, c.want)
		}
	}
}

func TestWithContext(t *testing.T) {
	parent, err := New(Options{Dir: t.TempDir(), FilePrefix: "ctx", Level: LevelInfo})
	if err != nil {
		t.Fatalf("New() error = %v", err)
	}
	t.Cleanup(func() { _ = parent.Close() })

	child := parent.With("component", "merge")
	ctx := ContextWith(context.Background(), child)
	got := child.WithContext(ctx)
	if got != child {
		t.Fatal("WithContext did not return the attached logger")
	}
	if got.WithContext(context.Background()) == nil {
		t.Fatal("WithContext fallback returned nil")
	}
}

func TestNewRespectsLevel(t *testing.T) {
	dir := t.TempDir()
	logger, err := New(Options{Dir: dir, FilePrefix: "lvl", Level: LevelWarn})
	if err != nil {
		t.Fatalf("New() error = %v", err)
	}

	var buf bytes.Buffer
	logger.Logger = slog.New(slog.NewJSONHandler(&buf, &slog.HandlerOptions{Level: slog.LevelWarn}))

	logger.Debug("debug")
	logger.Info("info")
	logger.Warn("warn")
	logger.Error("error")
	if err := logger.Close(); err != nil {
		t.Fatalf("Close() error = %v", err)
	}

	out := buf.String()
	if strings.Contains(out, `"msg":"debug"`) || strings.Contains(out, `"msg":"info"`) {
		t.Fatalf("unexpected low-level message in output: %s", out)
	}
	if !strings.Contains(out, `"msg":"warn"`) || !strings.Contains(out, `"msg":"error"`) {
		t.Fatalf("expected warn and error messages, got: %s", out)
	}
}

func TestCloseIsIdempotent(t *testing.T) {
	dir := t.TempDir()
	logger, err := New(Options{Dir: dir, FilePrefix: "close", Level: LevelInfo})
	if err != nil {
		t.Fatalf("New() error = %v", err)
	}
	if err := logger.Close(); err != nil {
		t.Fatalf("first Close() error = %v", err)
	}
	if err := logger.Close(); err != nil {
		t.Fatalf("second Close() error = %v", err)
	}
}

func readLogFile(t *testing.T, dir, prefix string) (string, string) {
	t.Helper()

	entries, err := os.ReadDir(dir)
	if err != nil {
		t.Fatalf("read dir: %v", err)
	}
	var found string
	for _, e := range entries {
		if strings.HasPrefix(e.Name(), prefix+"-") && strings.HasSuffix(e.Name(), ".log") {
			found = filepath.Join(dir, e.Name())
			break
		}
	}
	if found == "" {
		t.Fatalf("no log file found in %s", dir)
	}

	data, err := os.ReadFile(found)
	if err != nil {
		t.Fatalf("read log: %v", err)
	}
	return found, string(data)
}

func nowUTCDate() string {
	var mu sync.Mutex
	mu.Lock()
	defer mu.Unlock()
	return timeNow().UTC().Format("2006-01-02")
}

// timeNow is overridable so tests do not depend on the wall clock.
var timeNow = func() time.Time { return time.Now() }

func skipWindowsPermissionTest() bool {
	return os.PathSeparator == '\\'
}
