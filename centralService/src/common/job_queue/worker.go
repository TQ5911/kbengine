package job_queue

//执行者
type Worker struct {
	jobQueue *JobQueue
	stop     chan bool
}

//创建执行者
func createWorker(size int) *Worker {
	jobQueue := createJobQueue(size)
	return &Worker{
		jobQueue: jobQueue,
		stop:     make(chan bool),
	}
}

//开始干活
func (mgr *Worker) Start(wq chan *Worker) {
	go func() {
		for {
			select {
			//取任务
			case job := <-mgr.jobQueue.jobs:
				//执行任务
				job.Do()
			case <-mgr.stop:
				return
			}
			//活干完了之后，要注册自己到工作队列
			wq <- mgr
		}
	}()
}

//停止干活
func (mgr *Worker) Stop() {
	go func() {
		mgr.stop <- true
	}()
}
