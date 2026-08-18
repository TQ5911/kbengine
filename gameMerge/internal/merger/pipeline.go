package merger

import (
	"context"
	"errors"
	"fmt"
	"log/slog"
	"sync/atomic"
	"time"
)

var ErrSourceDone = errors.New("merger: source done")

type Row []any

type TableMeta struct {
	Name    string
	Columns []string
	index   map[string]int
}

func NewTableMeta(name string, columns []string) TableMeta {
	idx := make(map[string]int, len(columns))
	for i, c := range columns {
		idx[c] = i
	}
	return TableMeta{Name: name, Columns: columns, index: idx}
}

func (m TableMeta) Index(name string) (int, bool) {
	i, ok := m.index[name]
	return i, ok
}

func (m TableMeta) Get(row Row, name string) (any, bool) {
	i, ok := m.index[name]
	if !ok {
		return nil, false
	}
	if i >= len(row) {
		return nil, false
	}
	return row[i], true
}

func (m TableMeta) Set(row Row, name string, v any) bool {
	i, ok := m.index[name]
	if !ok {
		return false
	}
	if i >= len(row) {
		return false
	}
	row[i] = v
	return true
}

func (m TableMeta) String(row Row, name string) (string, bool) {
	v, ok := m.Get(row, name)
	if !ok || v == nil {
		return "", false
	}
	switch x := v.(type) {
	case string:
		return x, true
	case []byte:
		return string(x), true
	}
	return "", false
}

func (m TableMeta) GetInt64(row Row, name string) (int64, bool) {
	v, ok := m.Get(row, name)
	if !ok || v == nil {
		return 0, false
	}
	switch x := v.(type) {
	case int64:
		return x, true
	case int:
		return int64(x), true
	case int32:
		return int64(x), true
	case uint64:
		return int64(x), true
	default:
		return 0, false
	}
}

type Source interface {
	Meta() TableMeta
	Next(ctx context.Context) ([]Row, error)
}

type Transformer interface {
	Process(ctx context.Context, row Row) (Row, error)
}

type Sink interface {
	Submit(ctx context.Context, rows []Row) error
	Close() error
}

type Metrics struct {
	RowsIn    atomic.Int64
	RowsOut   atomic.Int64
	RowsDrop  atomic.Int64
	Batches   atomic.Int64
	ErrCount  atomic.Int64
	LoadMs    atomic.Int64
	ProcessMs atomic.Int64
	WriteMs   atomic.Int64
}

func (m *Metrics) Snapshot() map[string]int64 {
	if m == nil {
		return nil
	}
	return map[string]int64{
		"rows_in":    m.RowsIn.Load(),
		"rows_out":   m.RowsOut.Load(),
		"rows_drop":  m.RowsDrop.Load(),
		"batches":    m.Batches.Load(),
		"err_count":  m.ErrCount.Load(),
		"load_ms":    m.LoadMs.Load(),
		"process_ms": m.ProcessMs.Load(),
		"write_ms":   m.WriteMs.Load(),
	}
}

type PipelineConfig struct {
	ReadBuf    int
	ProcessBuf int
	WriteBatch int
}

func (c PipelineConfig) withDefaults() PipelineConfig {
	if c.ReadBuf <= 0 {
		c.ReadBuf = 4
	}
	if c.ProcessBuf <= 0 {
		c.ProcessBuf = 4
	}
	if c.WriteBatch <= 0 {
		c.WriteBatch = 400
	}
	return c
}

type Pipeline struct {
	Name    string
	Source  Source
	Process Transformer
	Sink    Sink
	Config  PipelineConfig
	Metrics *Metrics
}

func (p *Pipeline) Run(ctx context.Context) error {
	start := time.Now()
	err := p.runGuts(ctx)
	elapsed := time.Since(start)

	m := p.Metrics
	if m == nil {
		m = &Metrics{}
		p.Metrics = m
	}

	attrs := []any{
		"table", p.Name,
		"rows_in", m.RowsIn.Load(),
		"rows_out", m.RowsOut.Load(),
		"rows_drop", m.RowsDrop.Load(),
		"batches", m.Batches.Load(),
		"duration_ms", elapsed.Milliseconds(),
	}
	if err != nil {
		slog.Error("table failed", append(attrs, "err", err)...)
		return err
	}
	slog.Info("table merged", attrs...)
	return nil
}

// runGuts 启动三阶段并发流水线:
//   reader   -> readCh  -> processor -> writeCh -> writer -> Sink
// 任一阶段出错都会通过 errCh 通知主协程，主协程等待 writer 关闭 done 后退出。
func (p *Pipeline) runGuts(ctx context.Context) error {
	cfg := p.Config.withDefaults()
	m := p.Metrics
	if m == nil {
		m = &Metrics{}
		p.Metrics = m
	}

	// readCh: reader 推到 processor 的批次缓冲
	// writeCh: processor 推到 writer 的单行缓冲
	// errCh: 任一阶段报错都丢进来，主协程消费，容量 3 避免 reader/processor/writer 同时报错时阻塞
	readCh := make(chan []Row, cfg.ReadBuf)
	writeCh := make(chan Row, cfg.ProcessBuf)
	errCh := make(chan error, 3)

	// writer 退出时关闭 done，用于通知主协程"流水线正常结束"
	done := make(chan struct{})

	// === 阶段 1: reader ===
	// 循环从 Source 拉取批次，写入 readCh；遇到 ErrSourceDone 或空批次视为正常结束。
	go func() {
		defer close(readCh)
		t := time.Now()
		for {
			// 进入下一轮拉取前先看 ctx 是否已取消
			select {
			case <-ctx.Done():
				errCh <- ctx.Err()
				return
			default:
			}
			batch, err := p.Source.Next(ctx)
			if err != nil {
				// ErrSourceDone 是约定的"读完"信号，累加耗时后正常退出
				if errors.Is(err, ErrSourceDone) {
					m.LoadMs.Add(time.Since(t).Milliseconds())
					return
				}
				m.LoadMs.Add(time.Since(t).Milliseconds())
				errCh <- fmt.Errorf("%s: load: %w", p.Name, err)
				return
			}
			// 空批次也视为读完，避免下游无限等待
			if len(batch) == 0 {
				m.LoadMs.Add(time.Since(t).Milliseconds())
				return
			}
			m.RowsIn.Add(int64(len(batch)))
			// 发送批次时也要响应 ctx 取消，防止 reader 在满缓冲上死等
			select {
			case readCh <- batch:
			case <-ctx.Done():
				errCh <- ctx.Err()
				return
			}
		}
	}()

	// === 阶段 2: processor ===
	// 逐行调用 Transformer，把结果行（或 nil 表示丢弃）写入 writeCh。
	go func() {
		defer close(writeCh)
		t := time.Now()
		for batch := range readCh {
			for _, row := range batch {
				// 每行处理前检查 ctx，便于快速响应取消
				select {
				case <-ctx.Done():
					errCh <- ctx.Err()
					return
				default:
				}
				out, err := p.Process.Process(ctx, row)
				if err != nil {
					errCh <- fmt.Errorf("%s: process: %w", p.Name, err)
					return
				}
				if out == nil {
					// Transformer 返回 nil 表示该行被过滤掉
					m.RowsDrop.Add(1)
					continue
				}
				m.RowsOut.Add(1)
				select {
				case writeCh <- out:
				case <-ctx.Done():
					errCh <- ctx.Err()
					return
				}
			}
		}
		m.ProcessMs.Add(time.Since(t).Milliseconds())
	}()

	// === 阶段 3: writer ===
	// 把单行聚合成 cfg.WriteBatch 大小的批次后一次性提交给 Sink，
	// 最后做一次 flush 并关闭 Sink。
	go func() {
		defer close(done)
		t := time.Now()
		buf := make([]Row, 0, cfg.WriteBatch)
		// flush 把当前缓冲一次性提交，成功后清空缓冲并累加批次计数
		flush := func() error {
			if len(buf) == 0 {
				return nil
			}
			if err := p.Sink.Submit(ctx, buf); err != nil {
				return err
		}
		m.Batches.Add(1)
		buf = make([]Row, 0, cfg.WriteBatch)
		return nil
	}

	for row := range writeCh {
			buf = append(buf, row)
			if len(buf) >= cfg.WriteBatch {
				if err := flush(); err != nil {
					errCh <- fmt.Errorf("%s: write: %w", p.Name, err)
					return
				}
			}
		}
		// writeCh 被关闭后，再 flush 一次尾部残留数据
		if err := flush(); err != nil {
			errCh <- fmt.Errorf("%s: write: %w", p.Name, err)
			return
		}
		m.WriteMs.Add(time.Since(t).Milliseconds())
		// 关闭 Sink；这里的错误仍通过 errCh 抛出，让主协程统一处理
		if err := p.Sink.Close(); err != nil {
			errCh <- fmt.Errorf("%s: close: %w", p.Name, err)
		}
	}()

	// 优先等 writer 正常跑完；若任意阶段先报错，则取第一个错误返回
	select {
	case <-done:
	case err := <-errCh:
		m.ErrCount.Add(1)
		return err
	}

	// writer 正常结束后再扫一次 errCh，捞取 Sink.Close() 等尾部错误
	select {
	case err := <-errCh:
		if err != nil {
			m.ErrCount.Add(1)
			return err
		}
	default:
	}
	return nil
}
