package transformer

import (
	"context"
	"fmt"

	"gamemerge/internal/merger"
)

type RedStubRootTransformer struct {
	Meta      			merger.TableMeta
	IDCol     			string
	LastReleaseTimeCol 	string
	LastReleaseTimeMap	interface {
		Get(id int64) (int64, bool)
	}
}

func (t *RedStubRootTransformer) Process(ctx context.Context, row merger.Row) (merger.Row, error) {
	id, ok := t.Meta.GetInt64(row, t.IDCol)
	if !ok {
		return nil, fmt.Errorf("root: missing %s", t.IDCol)
	}
	src_lastReleaseTime, ok := t.Meta.GetInt64(row, t.LastReleaseTimeCol)
	if !ok {
		return nil, fmt.Errorf("root: missing %s", t.LastReleaseTimeCol)
	}
	dst_lastReleaseTime, ok := t.LastReleaseTimeMap.Get(id)
	if !ok {
		return nil, nil
	}
	lastReleaseTime := max(src_lastReleaseTime, dst_lastReleaseTime)
	t.Meta.Set(row, t.LastReleaseTimeCol, lastReleaseTime)
	return row, nil
}