package common

import (
	"centralService/src/appLog"
	"centralService/src/trpc"
	"net"
	"net/http"
	"os"
	"os/signal"
	"runtime"
	"runtime/pprof"
	"sync"
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
	app.Start()
	services := app.GetServices()

	group := sync.WaitGroup{}
	for _, info := range services {
		group.Add(1)
		go func(serviceInfo *ServiceInfo) {
			defer group.Done()
			appLog.Infow("server is running", "name:", GetServerName(), "id:", GetServerID(), "service name:", serviceInfo.ServiceName, "listen addr:", serviceInfo.ServiceListenAddr)
			listener, err := net.Listen("tcp", serviceInfo.ServiceListenAddr)
			if err != nil {
				appLog.Infow("server is running failed", "name:", GetServerName(), "id:", GetServerID(), "service name:", serviceInfo.ServiceName, "listen addr:", serviceInfo.ServiceListenAddr, "error:", err)
				return
			}
			defer listener.Close()
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
	group.Wait()
	app.Stop()
}
