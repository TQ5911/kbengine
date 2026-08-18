package cache

import (
	"sync"
	"testing"

	"gamemerge/internal/domain"
)

func TestDstAccountCache(t *testing.T) {
	c := NewDstAccount()
	c.Put("alice", domain.AccountInfo{DBID: 100, IsDst: true})
	c.Put("bob", domain.AccountInfo{DBID: 200, IsDst: true})

	if got, ok := c.Get("alice"); !ok || got.DBID != 100 {
		t.Fatalf("Get(alice) = %+v, %v", got, ok)
	}
	if _, ok := c.Get("unknown"); ok {
		t.Fatal("expected unknown to miss")
	}
	if c.Len() != 2 {
		t.Fatalf("Len = %d, want 2", c.Len())
	}
}

func TestDstAccountCacheConcurrent(t *testing.T) {
	c := NewDstAccount()
	const n = 500
	var wg sync.WaitGroup
	wg.Add(n)
	for i := 0; i < n; i++ {
		go func(i int) {
			defer wg.Done()
			c.Put("u-"+itoa(i), domain.AccountInfo{DBID: int64(i), IsDst: true})
		}(i)
	}
	wg.Wait()
	if c.Len() != n {
		t.Fatalf("Len = %d, want %d", c.Len(), n)
	}
}

func TestDuplicatedAccountCache(t *testing.T) {
	c := NewDuplicatedAccount()
	c.Put(1, 100)
	c.Put(2, 200)

	if got, ok := c.Get(1); !ok || got != 100 {
		t.Fatalf("Get(1) = %d, %v", got, ok)
	}
	if _, ok := c.Get(999); ok {
		t.Fatal("expected 999 to miss")
	}
	if c.Len() != 2 {
		t.Fatalf("Len = %d, want 2", c.Len())
	}
}

func itoa(i int) string {
	if i == 0 {
		return "0"
	}
	neg := false
	if i < 0 {
		neg = true
		i = -i
	}
	buf := [20]byte{}
	pos := len(buf)
	for i > 0 {
		pos--
		buf[pos] = byte('0' + i%10)
		i /= 10
	}
	if neg {
		pos--
		buf[pos] = '-'
	}
	return string(buf[pos:])
}