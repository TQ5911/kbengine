package merger_test

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"sync/atomic"
	"testing"
	"time"

	"gamemerge/internal/merger"
)

type fakeSource struct {
	meta    merger.TableMeta
	batches [][]merger.Row
	calls   atomic.Int32
}

func (s *fakeSource) Meta() merger.TableMeta { return s.meta }

func (s *fakeSource) Next(ctx context.Context) ([]merger.Row, error) {
	i := int(s.calls.Add(1)) - 1
	if i >= len(s.batches) {
		return nil, merger.ErrSourceDone
	}
	return s.batches[i], nil
}

type fakeTransformer struct {
	drop func(merger.Row) bool
	mu   atomic.Int32
}

func (t *fakeTransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
	t.mu.Add(1)
	if t.drop != nil && t.drop(row) {
		return nil, nil
	}
	return row, nil
}

type fakeSink struct {
	mu      sync.Mutex
	batches [][]merger.Row
	closed  bool
	calls   atomic.Int32
}

func (s *fakeSink) Submit(ctx context.Context, rows []merger.Row) error {
	s.calls.Add(1)
	s.mu.Lock()
	defer s.mu.Unlock()
	cp := make([]merger.Row, len(rows))
	copy(cp, rows)
	s.batches = append(s.batches, cp)
	return nil
}

func (s *fakeSink) Close() error {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.closed = true
	return nil
}

func TestPipelineRunsThreeStages(t *testing.T) {
	meta := merger.NewTableMeta("t", []string{"id", "name"})
	src := &fakeSource{meta: meta, batches: [][]merger.Row{
		{{int64(1), "a"}, {int64(2), "b"}},
		{{int64(3), "c"}},
	}}
	sink := &fakeSink{}
	p := &merger.Pipeline{
		Name:    "test",
		Source:  src,
		Process: &fakeTransformer{},
		Sink:    sink,
		Config:  merger.PipelineConfig{ReadBuf: 2, ProcessBuf: 4, WriteBatch: 2},
	}

	if err := p.Run(context.Background()); err != nil {
		t.Fatalf("Run: %v", err)
	}

	if got := p.Metrics.RowsIn.Load(); got != 3 {
		t.Fatalf("RowsIn = %d, want 3", got)
	}
	if got := p.Metrics.RowsOut.Load(); got != 3 {
		t.Fatalf("RowsOut = %d, want 3", got)
	}
	if got := p.Metrics.Batches.Load(); got != 2 {
		t.Fatalf("Batches = %d, want 2", got)
	}
	if !sink.closed {
		t.Fatal("sink not closed")
	}
}

func TestPipelineDropsRows(t *testing.T) {
	meta := merger.NewTableMeta("t", []string{"id"})
	src := &fakeSource{meta: meta, batches: [][]merger.Row{
		{{int64(1)}, {int64(2)}, {int64(3)}},
	}}
	sink := &fakeSink{}
	p := &merger.Pipeline{
		Name:    "test",
		Source:  src,
		Process: &fakeTransformer{drop: func(r merger.Row) bool { return r[0].(int64) == 2 }},
		Sink:    sink,
		Config:  merger.PipelineConfig{ReadBuf: 1, ProcessBuf: 8, WriteBatch: 10},
	}
	if err := p.Run(context.Background()); err != nil {
		t.Fatalf("Run: %v", err)
	}
	if got := p.Metrics.RowsDrop.Load(); got != 1 {
		t.Fatalf("RowsDrop = %d, want 1", got)
	}
	if got := p.Metrics.RowsOut.Load(); got != 2 {
		t.Fatalf("RowsOut = %d, want 2", got)
	}
}

type failingSource struct{ fakeSource }

func (s *failingSource) Next(ctx context.Context) ([]merger.Row, error) {
	return nil, errors.New("boom")
}

func TestPipelinePropagatesSourceError(t *testing.T) {
	meta := merger.NewTableMeta("t", []string{"id"})
	p := &merger.Pipeline{
		Name:    "test",
		Source:  &failingSource{fakeSource: fakeSource{meta: meta}},
		Process: &fakeTransformer{},
		Sink:    &fakeSink{},
		Config:  merger.PipelineConfig{WriteBatch: 1},
	}
	err := p.Run(context.Background())
	if err == nil || !contains(err.Error(), "load") {
		t.Fatalf("expected load error, got %v", err)
	}
}

type cancelSource struct {
	fakeSource
}

func (s *cancelSource) Next(ctx context.Context) ([]merger.Row, error) {
	select {
	case <-ctx.Done():
		return nil, ctx.Err()
	case <-time.After(50 * time.Millisecond):
	}
	return []merger.Row{{int64(1)}}, nil
}

func TestPipelineRespectsContextCancel(t *testing.T) {
	meta := merger.NewTableMeta("t", []string{"id"})
	src := &cancelSource{fakeSource: fakeSource{meta: meta}}
	p := &merger.Pipeline{
		Name:    "test",
		Source:  src,
		Process: &fakeTransformer{},
		Sink:    &fakeSink{},
		Config:  merger.PipelineConfig{ReadBuf: 1, ProcessBuf: 1, WriteBatch: 1},
	}
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Millisecond)
	defer cancel()
	err := p.Run(ctx)
	if err == nil {
		t.Fatal("expected context error")
	}
}

func TestTableMetaGetSet(t *testing.T) {
	meta := merger.NewTableMeta("t", []string{"id", "name"})
	row := merger.Row{int64(1), "a"}

	v, ok := meta.Get(row, "name")
	if !ok || v != "a" {
		t.Fatalf("Get(name) = %v, %v", v, ok)
	}
	if !meta.Set(row, "name", "b") {
		t.Fatal("Set failed")
	}
	if row[1] != "b" {
		t.Fatalf("row[1] = %v, want b", row[1])
	}
	if _, ok := meta.Get(row, "missing"); ok {
		t.Fatal("expected missing to fail")
	}
}

func TestBulkInsertSQL(t *testing.T) {
	sql, ph := merger.BulkInsertSQL("tbl_Account", []string{"id", "name"})
	if sql != "INSERT INTO `tbl_Account` (`id`, `name`) VALUES " {
		t.Fatalf("unexpected sql: %s", sql)
	}
	if ph != "(?, ?)" {
		t.Fatalf("unexpected placeholder: %q", ph)
	}
}

func TestPipelineRunsProcessConcurrently(t *testing.T) {
	meta := merger.NewTableMeta("t", []string{"id"})
	src := &fakeSource{meta: meta, batches: [][]merger.Row{
		{{int64(1)}, {int64(2)}, {int64(3)}, {int64(4)}, {int64(5)}},
	}}
	slow := &slowTransformer{}
	sink := &fakeSink{}
	p := &merger.Pipeline{
		Name:    "test",
		Source:  src,
		Process: slow,
		Sink:    sink,
		Config:  merger.PipelineConfig{ReadBuf: 1, ProcessBuf: 8, WriteBatch: 5},
	}
	if err := p.Run(context.Background()); err != nil {
		t.Fatalf("Run: %v", err)
	}
	if got := p.Metrics.RowsIn.Load(); got != 5 {
		t.Fatalf("RowsIn = %d", got)
	}
}

type slowTransformer struct{}

func (s *slowTransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
	time.Sleep(5 * time.Millisecond)
	return row, nil
}

func contains(s, sub string) bool {
	return len(sub) == 0 || (len(s) >= len(sub) && (func() bool {
		for i := 0; i+len(sub) <= len(s); i++ {
			if s[i:i+len(sub)] == sub {
				return true
			}
		}
		return false
	})())
}

func TestMetricsSnapshot(t *testing.T) {
	m := &merger.Metrics{}
	m.RowsIn.Add(10)
	m.RowsOut.Add(8)
	m.RowsDrop.Add(2)
	snap := m.Snapshot()
	if snap["rows_in"] != 10 || snap["rows_out"] != 8 || snap["rows_drop"] != 2 {
		t.Fatalf("unexpected snapshot: %+v", snap)
	}
	if (*merger.Metrics)(nil).Snapshot() != nil {
		t.Fatal("nil Metrics should return nil")
	}
	if fmt.Sprintf("%v", snap["rows_in"]) != "10" {
		t.Fatalf("rows_in = %v", snap["rows_in"])
	}
}