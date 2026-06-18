package DropApp

import "sync"

type DropItemLocker struct {
	locks sync.Map
}

func (l *DropItemLocker) Lock(uniqueId uint64) {
	itemMu := &sync.Mutex{}
	actual, loaded := l.locks.LoadOrStore(uniqueId, itemMu)
	if loaded {
		itemMu = actual.(*sync.Mutex)
	}
	itemMu.Lock()
}

func (l *DropItemLocker) Unlock(uniqueId uint64) {
	value, ok := l.locks.Load(uniqueId)
	if ok {
		value.(*sync.Mutex).Unlock()
	}
}
