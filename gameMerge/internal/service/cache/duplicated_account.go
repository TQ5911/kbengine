package cache

import (
	"sync"
)

type DuplicatedAccountCache struct {
	mu sync.RWMutex
	m  map[int64]int64
}

func NewDuplicatedAccount() *DuplicatedAccountCache {
	return &DuplicatedAccountCache{m: make(map[int64]int64)}
}

func (c *DuplicatedAccountCache) Put(srcDBID, dstDBID int64) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.m[srcDBID] = dstDBID
}

func (c *DuplicatedAccountCache) Get(srcDBID int64) (int64, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()
	v, ok := c.m[srcDBID]
	return v, ok
}

func (c *DuplicatedAccountCache) Len() int {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return len(c.m)
}