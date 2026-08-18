package merger

import (
	"context"
	"fmt"
	"sync"
)

type Stage struct {
	Name  string
	Items []Runner
}

func (s *Stage) Run(ctx context.Context) error {
	if len(s.Items) == 0 {
		return nil
	}
	errCh := make(chan error, len(s.Items))
	var wg sync.WaitGroup
	for _, item := range s.Items {
		wg.Add(1)
		go func(item Runner) {
			defer wg.Done()
			if err := item.Run(ctx); err != nil {
				errCh <- err
			}
		}(item)
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

// Step 是 DAG 节点：Name 唯一标识，Deps 列出所有前置 step 名（必须都注册在同一次
// RunDAG 调用里），Fn 是执行逻辑。
type Step struct {
	Name string
	Deps []string
	Fn   func(ctx context.Context) error
}

// RunDAG 按依赖关系并发执行 steps：
//   - 没有依赖（Deps 为空或 nil）的 step 立刻并发启动；
//   - 一个 step 完成后，递减所有以它为依赖的 step 的剩余依赖计数；归零的立刻启动；
//   - 第一个 error 时 cancel 子 ctx 通知兄弟节点退出，返回首个 error。
//
// 与 RunLayer / Stage 的关键区别：DAG 不强制按"层"对齐——一个 step 完成时它的
// 唯一下游可以立刻开始，不必等其他无关 step 跑完。比如 KBE 完成时 tbl_Account
// 立即启动，不需要等 Guild / 4 个 auto-increment-id 表跑完。
//
// 约定：Deps 里出现的名字必须能在 steps 里找到，否则返回 error（避免静默 hang）。
// 不做循环检测；写错（环）会在 wg.Wait 阶段死锁，由 caller 自查。
func RunDAG(ctx context.Context, steps []Step) error {
	if len(steps) == 0 {
		return nil
	}

	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	byName := make(map[string]Step, len(steps))
	remaining := make(map[string]int, len(steps))
	for _, s := range steps {
		byName[s.Name] = s
		if len(s.Deps) > 0 {
			remaining[s.Name] = len(s.Deps)
		}
	}

	// 校验：Deps 引用的 name 必须存在；否则启动时不会被激活、整个 DAG 静默 hang。
	for _, s := range steps {
		for _, dep := range s.Deps {
			if _, ok := byName[dep]; !ok {
				return fmt.Errorf("runDAG: step %q depends on unknown step %q", s.Name, dep)
			}
		}
	}

	var (
		mu    sync.Mutex
		errCh = make(chan error, len(steps))
		wg    sync.WaitGroup
	)

	// startLocked：调用方必须持 mu。spawn goroutine 后立即返回；goroutine 自己
	// 跑 Fn，结束后再抢 mu 来通知下游。
	var startLocked func(s Step)
	startLocked = func(s Step) {
		wg.Add(1)
		go func(s Step) {
			defer wg.Done()
			err := s.Fn(ctx)
			if err != nil {
				errCh <- fmt.Errorf("%s: %w", s.Name, err)
				cancel()
				return
			}
			mu.Lock()
			for _, other := range steps {
				if remaining[other.Name] == 0 {
					continue
				}
				for _, dep := range other.Deps {
					if dep == s.Name {
						remaining[other.Name]--
						if remaining[other.Name] == 0 {
							startLocked(other)
						}
						break
					}
				}
			}
			mu.Unlock()
		}(s)
	}

	mu.Lock()
	for _, s := range steps {
		if remaining[s.Name] == 0 {
			startLocked(s)
		}
	}
	mu.Unlock()

	wg.Wait()
	close(errCh)

	for err := range errCh {
		if err != nil {
			return err
		}
	}
	return nil
}