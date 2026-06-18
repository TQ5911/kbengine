package common

import (
	"centralService/src/appLog"
	"fmt"
	"runtime/debug"
)

func ExecuteConcurrently(f func()) {
	go func() {
		defer func() {
			if r := recover(); r != nil {
				appLog.Error("recuver from panic: ", fmt.Sprintf("%v\n%s", r, debug.Stack()))
			}
		}()
		f()
	}()
}

func ExecuteConcurrentlyWithArgs[T any](f func(T), arg T) {
	go func(arg T) {
		defer func() {
			if r := recover(); r != nil {
				appLog.Error("recuver from panic: ", fmt.Sprintf("%v\n%s", r, debug.Stack()))
			}
		}()
		f(arg)
	}(arg)
}
