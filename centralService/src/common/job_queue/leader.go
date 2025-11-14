package job_queue

// 管理者
type Leader struct {
	// 任务队列
	jobQueue *JobQueue
	// 执行者个数
	workCount int
	// 队列大小
	queueCount int
	// 执行者队列
	workQueue chan *Worker
}

// 创建管理者
func createLeader(workCount int, size int) *Leader {
	jobQueue := createJobQueue(0)
	return &Leader{
		workCount:  workCount,
		queueCount: size,
		jobQueue:   jobQueue,
		workQueue:  make(chan *Worker, workCount),
	}
}

// 给执行者分发任务
func (mgr *Leader) run() {
	// 创建指定个数执行者
	for i := 0; i < mgr.workCount; i++ {
		// 这里会创建执行者实例
		worker := createWorker(mgr.queueCount)
		// 主动注册到leader的工作队列
		mgr.workQueue <- worker
		// 执行者开始工作
		worker.Start(mgr.workQueue)
	}

	//单独协程来调度任务的分发
	mgr.dispatch()
}

// 分发任务逻辑, 这里不做业务逻辑，只负责对接收到的任务进行派发，一个协程干活够了
func (mgr *Leader) dispatch() {
	go func() {
		for {
			select {
			// 从全局任务队列里取出任务
			case job := <-mgr.jobQueue.jobs:
				// 等待一个空闲的执行者
				worker := <-mgr.workQueue
				// 给执行者的工作队列塞一个任务
				worker.jobQueue.jobs <- job
			}
		}
	}()
}

// 往协程池里加入任务
func (mgr *Leader) AddWork(job Job) {
	mgr.jobQueue.jobs <- job
}
