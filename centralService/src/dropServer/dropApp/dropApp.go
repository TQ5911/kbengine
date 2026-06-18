package DropApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	gameServerService "centralService/src/dropServer/dropApp/gameServerService"
	"centralService/src/trpc"
	"database/sql"
	"fmt"
	"net"
	"strconv"
	"sync"
	"syscall"
	"time"

	_ "github.com/go-sql-driver/mysql"
	"github.com/google/uuid"
)

var DropConfig = AppConfig{}

const (
	_ = iota
	SERVICE_DROP
)

type DropApp struct {
	common.App
	serversLock   sync.RWMutex
	gameServers   map[string]*GameServerService
	channelToHost map[uuid.UUID]*GameServerService
	db            *sql.DB
	dropItemLock  DropItemLocker
}

func NewDropApp() *DropApp {
	db, err := sql.Open("mysql", fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8",
		DropConfig.Mysql.User, DropConfig.Mysql.Passwd, DropConfig.Mysql.Addr, DropConfig.Mysql.Db))

	if err != nil {
		appLog.Error("open msyql error: ", err.Error())
		return nil
	}

	db.SetMaxIdleConns(50)
	db.SetConnMaxLifetime(time.Second * 290)
	db.SetMaxOpenConns(50)
	if err = db.Ping(); err != nil {
		appLog.Error("mysql connect err", err.Error())
		return nil
	}

	app := DropApp{App: common.App{AppName: "DropApp"},
		serversLock:   sync.RWMutex{},
		gameServers:   make(map[string]*GameServerService),
		channelToHost: make(map[uuid.UUID]*GameServerService),
		db:            db,
	}

	return &app
}

func (da *DropApp) Start() {
	da.App.Start()

	da.RegisterSignals(syscall.SIGINT, syscall.SIGKILL, syscall.SIGTERM)
	go func() {
		<-da.SignalChan
		da.Stop()
	}()

	go da.StartDebugService(DropConfig.AddressForDebug)
}

func (da *DropApp) Stop() {
}

func (da *DropApp) GetName() string {
	return da.AppName
}

func (da *DropApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	var service trpc.IServerEndPoint = nil
	if serviceType == SERVICE_DROP {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = &GameServerService{ServerEndPoint: gameServerService.NewDropServerService(gameServerService.NewGameServerClient(channel)), app: da}
		channel.SetEndPoint(service)
	}
	return service
}

func (da *DropApp) GetServices() []*common.ServiceInfo {
	return []*common.ServiceInfo{
		{
			ServiceType:       SERVICE_DROP,
			ServiceName:       "掉落服",
			ServiceListenAddr: DropConfig.DropServerAddr,
		},
	}
}

func (da *DropApp) addGameServer(service *GameServerService) {
	da.serversLock.Lock()
	defer da.serversLock.Unlock()

	serviceKey := da.getServiceKey(service.serverId)
	da.gameServers[serviceKey] = service
	da.channelToHost[service.GetRpcChannel().ChannelUUID] = service
}

func (da *DropApp) getServiceKey(serverId uint32) string {
	return strconv.Itoa(int(serverId))
}

func (da *DropApp) removeGameServer(service *GameServerService) {
	da.serversLock.Lock()
	defer da.serversLock.Unlock()

	serviceKey := da.getServiceKey(service.serverId)
	delete(da.gameServers, serviceKey)
	delete(da.channelToHost, service.GetRpcChannel().ChannelUUID)
}

func (da *DropApp) getGameServer(serverId uint32) *GameServerService {
	da.serversLock.RLock()
	defer da.serversLock.RUnlock()

	serviceKey := da.getServiceKey(serverId)
	if gs, ok := da.gameServers[serviceKey]; ok {
		return gs
	}
	return nil
}
