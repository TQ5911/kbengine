package merger

import "context"

type MergeContext struct {
	Logger                 any
	MergeInfo              any
	AccountIDMap           any
	AvatarIDMap            any
	DstAccount             any
	DuplicatedAccount      any
	AccountDBIDBase        int64
	AvatarDBIDBase         int64
	AvatarTableIDCol       string
}

type ctxKey struct{}

func ContextWith(ctx context.Context, mc *MergeContext) context.Context {
	return context.WithValue(ctx, ctxKey{}, mc)
}

func FromContext(ctx context.Context) *MergeContext {
	if v, ok := ctx.Value(ctxKey{}).(*MergeContext); ok {
		return v
	}
	return nil
}