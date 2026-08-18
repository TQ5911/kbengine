package cache

import (
	"sync"

	"gamemerge/internal/domain"
)

type DstAccountCache struct {
	mu     sync.RWMutex
	byName map[string]domain.AccountInfo
}

func NewDstAccount() *DstAccountCache {
	return &DstAccountCache{byName: make(map[string]domain.AccountInfo)}
}

func (c *DstAccountCache) Put(name string, info domain.AccountInfo) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.byName[name] = info
}

func (c *DstAccountCache) Get(name string) (domain.AccountInfo, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()
	v, ok := c.byName[name]
	return v, ok
}

func (c *DstAccountCache) Lookup(name string) (int64, bool) {
	info, ok := c.Get(name)
	if !ok {
		return 0, false
	}
	return info.DBID, true
}

func (c *DstAccountCache) Len() int {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return len(c.byName)
}