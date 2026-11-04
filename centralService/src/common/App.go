package common

import (
	"centralService/src/appLog"
	"centralService/src/trpc"
	"errors"
	"net"
	"net/http"
	"os"
	"os/signal"
	"reflect"
	"runtime"
	"runtime/debug"
	"runtime/pprof"
	"strconv"
	"sync"
	"time"
)

func handler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")

	p := pprof.Lookup("goroutine")
	p.WriteTo(w, 1)
}

type IApp interface {
	Start()
	Stop()
	NewService(net.Conn, uint8) trpc.IServerEndPoint
	GetServices() []*ServiceInfo
}

type App struct {
	AppName    string
	SignalChan chan os.Signal
}

type ServiceInfo struct {
	ServiceType       uint8
	ServiceName       string
	ServiceListenAddr string
}

func (self *App) GetName() string {
	return self.AppName
}

func (self *App) StartDebugService(addr string) {
	debugSvr := http.NewServeMux()
	debugSvr.HandleFunc("/", handler)
	_ = http.ListenAndServe(addr, debugSvr)
}

func (self *App) RegisterSignals(ss ...os.Signal) {
	self.SignalChan = make(chan os.Signal, 1)
	signal.Notify(self.SignalChan, ss...)
}

func (self *App) Start() {

}

func (self *App) Stop() {

}

func Run(app IApp) {
	if app == nil {
		appLog.Error("common.Run: app interface is nil, server instance returned nil. exiting")
		appLog.BootFailed("app_is_nil")
		ExitProgram(1, "app_is_nil")
		return
	}
	v := reflect.ValueOf(app)
	if v.Kind() == reflect.Ptr && v.IsNil() {
		appLog.Errorf("common.Run: server instance is a typed-nil %s, initialization likely failed. exiting", v.Type().String())
		appLog.BootFailed("app_is_typed_nil")
		ExitProgram(1, "app_is_typed_nil")
		return
	}

	defer func() {
		if r := recover(); r != nil {
			appLog.Errorf("========== SERVER PANIC ==========")
			appLog.Errorf("panic: %v", r)
			appLog.Errorf("stack trace:\n%s", string(debug.Stack()))
			appLog.Errorf("==================================")
			appLog.BootFailed("panic", "stage=run")
			// reason 统一交给 ExitProgram 打，避免 exit 行出现两条
			ExitProgram(1, "panic")
		}
	}()

	// 先取服务清单再 Start：HTTP 类服务的 Start 会阻塞，取不到就晚了。
	// 各服务的 GetServices 只读全局配置，不依赖 Start 的副作用。
	services := app.GetServices()

	// 中心服有两种形态，ready 的判定不一样：
	//   1) TCP 类（centralLogin / router / auction ...）：Start() 只做初始化就返回，
	//      监听由下面的 common.Run 统一建，必须等全部端口 Listen 成功才算就绪；
	//   2) HTTP 类（maple / queueServer）：GetServices() 返回 nil，Start() 自己同步
	//      阻塞在 ListenAndServe / server.Serve 上，永远不会返回，走不到下面的监听逻辑。
	// 所以 len(services)==0 不能当成"没声明端口的故障"，要单独走 ready 判定。

	if len(services) == 0 {
		runHttpOnlyApp(app)
		return
	}

	app.Start()

	// 收集每个端口的 Listen 结果，全部成功才打 ready。
	// 原实现 Listen 失败只打一行日志就 return，进程继续跑、systemd 认为 active，
	// 但端口实际不可用 —— 这种"假活"正是要靠启动 TAG 抓出来的场景。
	type listenResult struct {
		addr string
		err  error
	}
	results := make(chan listenResult, len(services))

	group := sync.WaitGroup{}
	for _, info := range services {
		group.Add(1)
		go func(serviceInfo *ServiceInfo) {
			defer group.Done()
			// 兜底：GetServices 若返回了 nil 元素，net.Listen 会 panic，
			// 那样这一路永远不上报结果，主协程会卡死在收结果上
			if serviceInfo == nil {
				results <- listenResult{addr: "-", err: errors.New("nil service info")}
				return
			}
			listener, err := net.Listen("tcp", serviceInfo.ServiceListenAddr)
			// 先上报结果再进入 accept 循环，主协程才能及时判定 ready
			results <- listenResult{addr: serviceInfo.ServiceListenAddr, err: err}
			if err != nil {
				appLog.Infow("server is running failed", "name:", GetServerName(), "id:", GetServerID(), "service name:", serviceInfo.ServiceName, "listen addr:", serviceInfo.ServiceListenAddr, "error:", err)
				return
			}
			defer listener.Close()
			appLog.Infow("server is running", "name:", GetServerName(), "id:", GetServerID(), "service name:", serviceInfo.ServiceName, "listen addr:", serviceInfo.ServiceListenAddr)
			for {
				conn, err := listener.Accept()
				if err != nil {
					appLog.Error("encounter error while accept, err: ", err)
					continue
				}
				appLog.Infof("new connection from %v on %s. goroutines: %d\n", conn.RemoteAddr(), serviceInfo.ServiceName, runtime.NumGoroutine())
				service := app.NewService(conn, serviceInfo.ServiceType)
				go service.Serve()
			}
		}(info)
	}

	// 等所有端口的 Listen 结果到齐再判定，失败的地址与错误一并打进 TAG 行
	failCount := 0
	failAddrs := ""
	failFirstErr := ""
	for i := 0; i < len(services); i++ {
		r := <-results
		if r.err == nil {
			continue
		}
		failCount++
		if failCount == 1 {
			failAddrs = r.addr
			failFirstErr = r.err.Error()
		}
	}
	if failCount > 0 {
		appLog.BootFailed("listen",
			"addr="+appLog.NormalizeField(failAddrs),
			"fail_count="+strconv.Itoa(failCount),
			"err="+appLog.NormalizeField(failFirstErr))
	} else {
		// len(services)==0 的 HTTP 类服务也走这里：Start() 已正常返回
		appLog.BootReady()
	}

	group.Wait()
	app.Stop()
}

// httpOnlyReadyDelay HTTP 类服务（Start 阻塞型）判定 ready 的等待窗口。
//
// 依据：这类服务在 Start() 里先绑定端口再进入 Serve 循环，端口绑定失败会立刻
// panic（maple 用 appLog.Panic，queueServer 直接 panic），不可能等到窗口结束。
// 所以窗口内既没 panic 也没返回，就说明端口已经绑上、进程已经进入服务循环。
const httpOnlyReadyDelay = 300 * time.Millisecond

// runHttpOnlyApp 处理 GetServices() 返回 nil 的服务（maple / queueServer）。
//
// 这类服务的 Start() 会同步阻塞到进程结束，因此：
//   - 必须放到独立协程里跑，否则 Run 里后面的代码永远执行不到、ready 打不出来；
//   - panic 需要在协程内自己 recover —— Run 外层的 defer 只能兜当前协程，
//     兜不住新协程，端口被占用这种最常见的启动失败会变成"进程直接消失、无 TAG"。
func runHttpOnlyApp(app IApp) {
	exited := make(chan struct{})

	go func() {
		defer func() {
			if r := recover(); r != nil {
				appLog.Errorf("========== SERVER PANIC (start) ==========")
				appLog.Errorf("panic: %v", r)
				appLog.Errorf("stack trace:\n%s", string(debug.Stack()))
				appLog.Errorf("==========================================")
				appLog.BootFailed("panic", "stage=start")
				// 直接退出，不再 close(exited)：避免主协程同时打一条 start_returned
				ExitProgram(1, "panic")
			}
		}()
		app.Start()
		close(exited)
	}()

	select {
	case <-exited:
		// Start 正常返回：没有进入服务循环，进程不能算就绪
		appLog.BootFailed("start_returned")
	case <-time.After(httpOnlyReadyDelay):
		appLog.BootReady()
	}

	// 保持原语义：Run 要等服务循环真正结束才返回
	<-exited
	app.Stop()
}
