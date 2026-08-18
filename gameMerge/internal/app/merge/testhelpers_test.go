package merge

import (
	"sync"

	"gamemerge/internal/service/idmap"
)

func newIDMapStub() *idmap.IDMap {
	return idmap.New(0)
}

var _ = sync.Mutex{} // reserved for future use