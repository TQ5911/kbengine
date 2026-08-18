package merger_test

import (
	"context"
	"testing"

	"gamemerge/internal/merger"
	"gamemerge/internal/merger/transformer"
)

type stubDstAccount struct {
	m map[string]int64
}

func (s *stubDstAccount) Lookup(name string) (int64, bool) {
	v, ok := s.m[name]
	return v, ok
}

type stubDuplicatedPut struct {
	m map[int64]int64
}

func (s *stubDuplicatedPut) Put(src, dst int64) {
	if s.m == nil {
		s.m = map[int64]int64{}
	}
	s.m[src] = dst
}

type stubDuplicatedGet struct {
	m map[int64]int64
}

func (s *stubDuplicatedGet) Get(src int64) (int64, bool) {
	v, ok := s.m[src]
	return v, ok
}

type stubIDMapPut struct {
	m map[int64]int64
}

func (s *stubIDMapPut) Put(oldID, newID int64) {
	if s.m == nil {
		s.m = map[int64]int64{}
	}
	s.m[oldID] = newID
}

type stubIDMapGet struct {
	m map[int64]int64
}

func (s *stubIDMapGet) Get(oldID int64) (int64, bool) {
	v, ok := s.m[oldID]
	return v, ok
}

func TestKBETransformerSkipsDuplicated(t *testing.T) {
	meta := merger.NewTableMeta("kbe_accountinfos", []string{"accountName", "entityDBID"})
	dst := &stubDstAccount{m: map[string]int64{"alice": 999}}
	dup := &stubDuplicatedPut{}
	idm := &stubIDMapPut{}

	t1 := &transformer.KBETransformer{
		Meta: meta, DstAccount: dst, Duplicated: dup, IDMap: idm,
		Base: 100, NameCol: "accountName", EntityDBCol: "entityDBID",
	}

	out, err := t1.Process(context.Background(), merger.Row{"alice", int64(7)})
	if err != nil {
		t.Fatalf("Process: %v", err)
	}
	if out != nil {
		t.Fatalf("expected nil for duplicated, got %v", out)
	}
	if dup.m[7] != 999 {
		t.Fatalf("duplicated map not updated: %+v", dup.m)
	}

	out, err = t1.Process(context.Background(), merger.Row{"bob", int64(8)})
	if err != nil {
		t.Fatalf("Process: %v", err)
	}
	if got := out[1].(int64); got != 108 {
		t.Fatalf("bob entityDBID = %d, want 108", got)
	}
	if idm.m[8] != 108 {
		t.Fatalf("idmap not updated on miss: %+v", idm.m)
	}
}

func TestKBETransformerAcceptsByteSliceName(t *testing.T) {
	meta := merger.NewTableMeta("kbe_accountinfos", []string{"accountName", "entityDBID"})
	dst := &stubDstAccount{}
	dup := &stubDuplicatedPut{}
	idm := &stubIDMapPut{}
	t1 := &transformer.KBETransformer{
		Meta: meta, DstAccount: dst, Duplicated: dup, IDMap: idm,
		Base: 100, NameCol: "accountName", EntityDBCol: "entityDBID",
	}

	out, err := t1.Process(context.Background(), merger.Row{[]byte("charlie"), int64(11)})
	if err != nil {
		t.Fatalf("Process: %v", err)
	}
	if got := out[1].(int64); got != 111 {
		t.Fatalf("entityDBID = %d, want 111", got)
	}
	if idm.m[11] != 111 {
		t.Fatalf("idmap not updated: %+v", idm.m)
	}
}

func TestPassthroughTransformer(t *testing.T) {
	meta := merger.NewTableMeta("game_guild_avatar", []string{"gbId", "guildUUID"})
	t1 := &transformer.PassthroughTransformer{Meta: meta}

	in := merger.Row{int64(7), int64(42)}
	out, err := t1.Process(context.Background(), in)
	if err != nil {
		t.Fatalf("Process: %v", err)
	}
	if len(out) != 2 || out[0] != int64(7) || out[1] != int64(42) {
		t.Fatalf("row not passed through unchanged: %v", out)
	}
}