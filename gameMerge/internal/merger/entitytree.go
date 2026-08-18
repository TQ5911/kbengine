package merger

import (
	"context"
	"fmt"
	"sync"
)

type Runner interface {
	Run(ctx context.Context) error
}

type EntityTree struct {
	Name      string
	Pipeline  Runner
	Children  []*EntityTree
	parentRef string
}

func (t *EntityTree) Run(ctx context.Context) error {
	if t.Pipeline != nil {
		if err := t.Pipeline.Run(ctx); err != nil {
			return fmt.Errorf("%s: %w", t.Name, err)
		}
	}

	if len(t.Children) == 0 {
		return nil
	}

	errCh := make(chan error, len(t.Children))
	var wg sync.WaitGroup
	for _, child := range t.Children {
		child.parentRef = t.Name
		wg.Add(1)
		go func(child *EntityTree) {
			defer wg.Done()
			if err := child.Run(ctx); err != nil {
				errCh <- err
			}
		}(child)
	}
	wg.Wait()
	close(errCh)

	for err := range errCh {
		if err != nil {
			return err
		}
	}
	return nil
}