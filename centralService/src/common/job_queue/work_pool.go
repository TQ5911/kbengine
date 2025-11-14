package job_queue

// 获取一个协程池
func NewWorkPool(workCount int, taskQueueCount int) *Leader {
	leader := createLeader(workCount, taskQueueCount)
	leader.run()
	return leader
}

// 测试代码
// type test struct {
// }

// func (t *test) Do() {
// 	b := make([]byte, 64)
// 	b = b[:runtime.Stack(b, false)]
// 	b = b[:bytes.IndexByte(b, ':')]
// 	fmt.Println("test ", string(b))
// 	time.Sleep(time.Duration(1) * time.Second)
// }

// func main() {
// 	l := NewWorkPool(10)
// 	go func() {
// 		for i := 1; i <= 20; i++ {
// 			t := test{}
// 			AddWork(l, &t)
// 		}
// 	}()

// 	for {
// 		fmt.Println("go count: ", runtime.NumGoroutine())
// 		time.Sleep(2 * time.Second)
// 	}
// }
