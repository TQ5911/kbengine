package pool

import (
	JQ "centralService/src/common/job_queue"
)

type TaskQueue struct {
	// 数据库任务队列
	dbTaskQueue *JQ.Leader

	// 游戏服回包任务队列
	gsTaskQueue *JQ.Leader
}

func NewTaskQueue(db_work_count int, db_task_queue_count int, gs_work_count int, gs_task_queue_count int) *TaskQueue {
	dq := JQ.NewWorkPool(db_work_count, db_task_queue_count)
	if nil == dq {
		return nil
	}
	gq := JQ.NewWorkPool(gs_work_count, gs_task_queue_count)
	if nil == gq {
		return nil
	}
	q := &TaskQueue{
		dbTaskQueue: dq,
		gsTaskQueue: gq,
	}
	return q
}

// 加入游戏服任务队列
func (mgr *TaskQueue) AddGsTask(job JQ.Job) {
	mgr.gsTaskQueue.AddWork(job)
}

// 加入数据库任务队列
func (mgr *TaskQueue) AddDbTask(job JQ.Job) {
	mgr.dbTaskQueue.AddWork(job)
}
