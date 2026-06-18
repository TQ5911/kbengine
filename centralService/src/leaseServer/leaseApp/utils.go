package LeaseApp

import (
	"centralService/src/appLog"
	"fmt"
	"runtime/debug"
)

func SafeGo(fn func()) {
	go func() {
		defer func() {
			if r := recover(); r != nil {
				appLog.Error("[SafeGo] panic recovered: ", fmt.Sprintf("%v\n%s", r, debug.Stack()))
			}
		}()
		fn()
	}()
}
