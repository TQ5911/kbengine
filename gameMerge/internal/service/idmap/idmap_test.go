package idmap

import (
	"sync"
	"testing"
)

func TestReserve(t *testing.T) {
	m := New(100)
	if got := m.Reserve(1); got != 101 {
		t.Fatalf("Reserve(1) = %d, want 101", got)
	}
	if got := m.Reserve(2); got != 102 {
		t.Fatalf("Reserve(2) = %d, want 102", got)
	}
	if got, ok := m.Get(1); !ok || got != 101 {
		t.Fatalf("Get(1) = %d, %v", got, ok)
	}
}

func TestPut(t *testing.T) {
	m := New(100)
	m.Put(5, 999)
	if got, ok := m.Get(5); !ok || got != 999 {
		t.Fatalf("Get(5) = %d, %v", got, ok)
	}
}

func TestConcurrentAccess(t *testing.T) {
	m := New(0)
	const n = 1000
	var wg sync.WaitGroup
	wg.Add(n)
	for i := 0; i < n; i++ {
		go func(id int64) {
			defer wg.Done()
			m.Reserve(id)
		}(int64(i))
	}
	wg.Wait()
	if m.Len() != n {
		t.Fatalf("Len = %d, want %d", m.Len(), n)
	}
}