package logging

import (
	"context"
	"fmt"
	"io"
	"log/slog"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

type Level slog.Level

const (
	LevelDebug Level = Level(slog.LevelDebug)
	LevelInfo  Level = Level(slog.LevelInfo)
	LevelWarn  Level = Level(slog.LevelWarn)
	LevelError Level = Level(slog.LevelError)
)

func ParseLevel(s string) (Level, error) {
	switch strings.ToLower(strings.TrimSpace(s)) {
	case "", "info":
		return LevelInfo, nil
	case "debug":
		return LevelDebug, nil
	case "warn", "warning":
		return LevelWarn, nil
	case "error":
		return LevelError, nil
	default:
		return LevelInfo, fmt.Errorf("unknown log level %q", s)
	}
}

type Options struct {
	Dir        string
	FilePrefix string
	Level      Level
	AlsoStderr bool
}

func (o Options) withDefaults() Options {
	if o.Dir == "" {
		o.Dir = "logs"
	}
	if o.FilePrefix == "" {
		o.FilePrefix = "gamemerge"
	}
	if o.AlsoStderr {
		o.AlsoStderr = true
	}
	return o
}

type Logger struct {
	*slog.Logger
	closers []io.Closer
	mu      sync.Mutex
	closed  bool
}

func New(opts Options) (*Logger, error) {
	opts = opts.withDefaults()

	if err := os.MkdirAll(opts.Dir, 0o755); err != nil {
		return nil, fmt.Errorf("create log dir %q: %w", opts.Dir, err)
	}

	file, err := openDaily(opts.Dir, opts.FilePrefix)
	if err != nil {
		return nil, err
	}

	var writer io.Writer = file
	if opts.AlsoStderr {
		writer = io.MultiWriter(file, os.Stderr)
	}

	handler := slog.NewJSONHandler(writer, &slog.HandlerOptions{
		Level: slog.Level(opts.Level),
	})

	l := &Logger{
		Logger:  slog.New(handler),
		closers: []io.Closer{file},
	}
	return l, nil
}

func (l *Logger) Close() error {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.closed {
		return nil
	}
	l.closed = true

	var firstErr error
	for _, c := range l.closers {
		if err := c.Close(); err != nil && firstErr == nil {
			firstErr = err
		}
	}
	return firstErr
}

func (l *Logger) With(args ...any) *Logger {
	return &Logger{
		Logger:  l.Logger.With(args...),
		closers: l.closers,
	}
}

func (l *Logger) WithContext(ctx context.Context) *Logger {
	if v, ok := ctx.Value(ctxKey{}).(*Logger); ok && v != nil {
		return v
	}
	return l
}

type ctxKey struct{}

func ContextWith(ctx context.Context, l *Logger) context.Context {
	return context.WithValue(ctx, ctxKey{}, l)
}

func openDaily(dir, prefix string) (*os.File, error) {
	name := fmt.Sprintf("%s-%s.log", prefix, time.Now().UTC().Format("2006-01-02"))
	path := filepath.Join(dir, name)
	f, err := os.OpenFile(path, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0o644)
	if err != nil {
		return nil, fmt.Errorf("open log file %q: %w", path, err)
	}
	return f, nil
}
