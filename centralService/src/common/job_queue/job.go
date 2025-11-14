package job_queue

//任务抽象接口
type Job interface {
	Do()
}
