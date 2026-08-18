package main

import (
	"context"
	"flag"
	"fmt"
	"log/slog"
	"os"
	"time"

	_ "github.com/go-sql-driver/mysql"

	"gamemerge/internal/app/merge"
	"gamemerge/internal/config"
	"gamemerge/internal/infrastructure/logging"
)

var (
	version   = "dev"
	buildTime = "unknown"
	goVersion = "unknown"
)

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}

func run() error {
	configPath := flag.String("config", "configs/config.yaml", "path to config file")
	dryRun := flag.Bool("dry-run", false, "skip writes; only exercise the pipeline")
	flag.Parse()

	logger, err := logging.New(logging.Options{Dir: "logs", Level: logging.LevelInfo, AlsoStderr: true})
	if err != nil {
		return fmt.Errorf("init logger: %w", err)
	}
	defer logger.Close()

	slog.SetDefault(logger.Logger)

	slog.Info("gamemerge starting",
		"version", version,
		"buildTime", buildTime,
		"goVersion", goVersion,
		"dryRun", *dryRun,
	)

	cfg, err := config.Load(*configPath)
	if err != nil {
		return err
	}
	slog.Info("config loaded",
		"path", *configPath,
		"jobs", len(cfg.Merge.Jobs),
		"root", cfg.Merge.Root,
	)

	_ = dryRun

	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Hour)
	defer cancel()

	orch := &merge.Orchestrator{Cfg: cfg}
	return orch.Run(ctx)
}