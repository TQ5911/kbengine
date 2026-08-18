package merger_test

import (
	"context"
	"testing"

	"gamemerge/internal/merger"
	"gamemerge/internal/merger/transformer"
)

func TestRootTransformerOffsetsID(t *testing.T) {
	meta := merger.NewTableMeta("root", []string{"id", "val"})
	idm := &stubIDMapPut{}
	t1 := &transformer.RootTransformer{Meta: meta, IDCol: "id", IDBase: 100, IDMap: idm}

	out, err := t1.Process(context.Background(), merger.Row{int64(7), "x"})
	if err != nil {
		t.Fatalf("Process: %v", err)
	}
	if out[0].(int64) != 107 {
		t.Fatalf("id = %d, want 107", out[0])
	}
	if idm.m[7] != 107 {
		t.Fatalf("idmap not updated: %+v", idm.m)
	}
}

func TestRootTransformerJoinParentHit(t *testing.T) {
	meta := merger.NewTableMeta("root", []string{"id", "sm_accountDBID"})
	idm := &stubIDMapPut{}
	pmap := &stubIDMapGet{m: map[int64]int64{3: 3000}}
	t1 := &transformer.RootTransformer{
		Meta: meta, IDCol: "id", IDBase: 1000, IDMap: idm,
		ParentCol: "sm_accountDBID", ParentMap: pmap,
	}

	out, err := t1.Process(context.Background(), merger.Row{int64(5), int64(3)})
	if err != nil {
		t.Fatalf("Process: %v", err)
	}
	if out[0].(int64) != 1005 {
		t.Fatalf("id = %d", out[0])
	}
	if out[1].(int64) != 3000 {
		t.Fatalf("sm_accountDBID = %d, want 3000", out[1])
	}
}

func TestRootTransformerJoinParentMissing(t *testing.T) {
	meta := merger.NewTableMeta("root", []string{"id", "sm_accountDBID"})
	idm := &stubIDMapPut{}
	pmap := &stubIDMapGet{m: map[int64]int64{}}
	t1 := &transformer.RootTransformer{
		Meta: meta, IDCol: "id", IDBase: 1000, IDMap: idm,
		ParentCol: "sm_accountDBID", ParentMap: pmap,
	}
	out, err := t1.Process(context.Background(), merger.Row{int64(5), int64(3)})
	if err != nil {
		t.Fatalf("Process: %v", err)
	}
	if out != nil {
		t.Fatalf("missing parent should drop, got %v", out)
	}
}

func TestRootTransformerNoParentMapKeepsValue(t *testing.T) {
	meta := merger.NewTableMeta("root", []string{"id", "sm_accountDBID"})
	idm := &stubIDMapPut{}
	t1 := &transformer.RootTransformer{
		Meta: meta, IDCol: "id", IDBase: 1000, IDMap: idm,
		ParentCol: "sm_accountDBID", ParentMap: nil,
	}
	out, err := t1.Process(context.Background(), merger.Row{int64(5), int64(3)})
	if err != nil {
		t.Fatalf("Process: %v", err)
	}
	if out[1].(int64) != 3 {
		t.Fatalf("sm_accountDBID should stay as 3, got %d", out[1])
	}
}