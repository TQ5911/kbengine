package idmap

import "sync"

type IDMap struct {
	mu      sync.RWMutex
	base    int64
	old2New map[int64]int64
}

func New(base int64) *IDMap {
	return &IDMap{
		base:    base,
		old2New: make(map[int64]int64),
	}
}

func (m *IDMap) Base() int64 {
	return m.base
}

func (m *IDMap) Reserve(oldID int64) int64 {
	newID := oldID + m.base
	m.Put(oldID, newID)
	return newID
}

func (m *IDMap) Put(oldID, newID int64) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.old2New[oldID] = newID
}

func (m *IDMap) Get(oldID int64) (int64, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()
	v, ok := m.old2New[oldID]
	return v, ok
}

func (m *IDMap) Len() int {
	m.mu.RLock()
	defer m.mu.RUnlock()
	return len(m.old2New)
}