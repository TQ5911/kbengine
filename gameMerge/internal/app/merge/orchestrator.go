package merge

import (
	"context"
	"errors"
	"fmt"
	"log/slog"
	"time"

	"gamemerge/internal/config"
	"gamemerge/internal/infrastructure/mysql"
)

type Orchestrator struct {
	Cfg *config.Config
}

func (o *Orchestrator) Run(ctx context.Context) error {
	if o.Cfg == nil {
		return errors.New("merge: nil config")
	}

	for i, jobSpec := range o.Cfg.Merge.Jobs {
		jobCtx, cancel := context.WithTimeout(ctx, 30*time.Minute)
		err := o.runJob(jobCtx, i, jobSpec)
		cancel()
		if err != nil {
			return err
		}
	}
	return nil
}

func (o *Orchestrator) runJob(ctx context.Context, idx int, jobSpec config.ServerPair) error {
	resolved, err := o.Cfg.Resolve(jobSpec)
	if err != nil {
		return fmt.Errorf("job %d: %w", idx, err)
	}

	srcDB, err := mysql.Open(toMysqlConfig(resolved.SrcConfig))
	if err != nil {
		return fmt.Errorf("job %d (%s): open src: %w", idx, resolved.SrcName, err)
	}
	defer srcDB.Close()
	if err := mysql.Ping(ctx, srcDB); err != nil {
		return fmt.Errorf("job %d (%s): ping src: %w", idx, resolved.SrcName, err)
	}

	dstDB, err := mysql.Open(toMysqlConfig(resolved.DstConfig))
	if err != nil {
		return fmt.Errorf("job %d (%s): open dst: %w", idx, resolved.DstName, err)
	}
	defer dstDB.Close()
	if err := mysql.Ping(ctx, dstDB); err != nil {
		return fmt.Errorf("job %d (%s): ping dst: %w", idx, resolved.DstName, err)
	}

	job := &Job{
		Src:        srcDB,
		Dst:        dstDB,
		ReadBatch:  o.Cfg.Merge.ReadBatch,
		WriteBatch: o.Cfg.Merge.WriteBatch,
	}

	slog.Info("job start", "job", idx,
		"src", resolved.SrcName, "dst", resolved.DstName,
	)
	if err := job.Run(ctx, nil); err != nil {
		slog.Error("job failed", "job", idx, "err", err)
		return err
	}
	slog.Info("job done", "job", idx)
	return nil
}

func toMysqlConfig(m config.MySQL) mysql.Config {
	return mysql.Config{
		Host:     m.Host,
		Port:     m.Port,
		Username: m.Username,
		Password: m.Password,
		DB:       m.DB,
	}
}
