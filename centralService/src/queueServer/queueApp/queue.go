package Queue

import "sync"

type Item string

type Queue struct {
	Items []Item
	mut   *sync.Mutex
}

type IQueue interface {
	New() Queue
	Enqueue(t Item)
	Dequeue(t Item)
	IsEmpty() bool
	Size() int
}

func (q *Queue) New() *Queue {
	q.Items = []Item{}
	q.mut = &sync.Mutex{}
	return q
}

func (q *Queue) Enqueue(data Item) int {
	q.mut.Lock()
	defer q.mut.Unlock()
	q.Items = append(q.Items, data)
	return len(q.Items)
}

func (q *Queue) Dequeue() *Item {
	q.mut.Lock()
	defer q.mut.Unlock()

	if len(q.Items) > 0 {
		item := q.Items[0]
		q.Items = q.Items[1:len(q.Items)]
		return &item
	} else {
		return nil
	}
}

func (q *Queue) IsEmpty() bool {
	return len(q.Items) == 0
}

func (q *Queue) Size() int {
	return len(q.Items)
}

func (q *Queue) Remove(item Item) bool {
	q.mut.Lock()
	defer q.mut.Unlock()

	for i := range q.Items {
		if q.Items[i] == item {
			q.Items = append(q.Items[:i], q.Items[i+1:]...)
			return true
		}
	}

	return false
}

func NewQueue() *Queue {
	q := Queue{}
	q.New()

	return &q
}
