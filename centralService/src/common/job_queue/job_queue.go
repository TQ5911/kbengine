package job_queue

// 任务队列
type JobQueue struct {
	jobs chan Job
}

// 创建任务队列
func createJobQueue(size int) *JobQueue {
	return &JobQueue{
		jobs: make(chan Job, size),
	}
}
