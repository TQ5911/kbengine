package job_queue

type Handler func()

type JobWrapper struct {
	callback Handler
}

func (mgr *JobWrapper) Do() {
	if nil != mgr.callback {
		mgr.callback()
	}
}

func (mgr *JobWrapper) Add(handler Handler) bool {
	if nil == mgr.callback {
		mgr.callback = handler
		return true
	}
	return false
}
