package crossDataApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"centralService/src/crossDataServer/crossDataApp/gameServerService"
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

var CrossDataConfig = AppConfig{}

const (
	_ = iota
	SERVICE_CROSS_DATA
)

type CrossDataApp struct {
	common.App
	serversLock   sync.RWMutex
	gameServers   map[string]*GameServerService
	channelToHost map[uuid.UUID]*GameServerService
	guildData     *GuildData
	siegeWarData  *SiegeWarData
}

func (cda *CrossDataApp) GetName() string {
	return cda.AppName
}

func (cda *CrossDataApp) GetServices() []*common.ServiceInfo {
	return []*common.ServiceInfo{
		{
			ServiceType:       SERVICE_CROSS_DATA,
			ServiceName:       cda.AppName,
			ServiceListenAddr: CrossDataConfig.CrossDataServerAddr,
		},
	}
}

func (cda *CrossDataApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	var service trpc.IServerEndPoint = nil
	if serviceType == SERVICE_CROSS_DATA {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = &GameServerService{
			ServerEndPoint: gameServerService.NewCrossDataServerService(gameServerService.NewGameServerClient(channel)), app: cda}
		channel.SetEndPoint(service)
	}
	return service
}

// Start implements common.IApp.
// Subtle: this method shadows the method (App).Start of CrossDataApp.App.
func (cda *CrossDataApp) Start() {

	appLog.Info("cross data app start", cda)
	cda.App.Start()

	cda.RegisterSignals(syscall.SIGINT, syscall.SIGKILL, syscall.SIGTERM)
	go func() {
		<-cda.SignalChan
		cda.Stop()
	}()
	go cda.StartDebugService(CrossDataConfig.AddressForDebug)
}

// Stop implements common.IApp.
// Subtle: this method shadows the method (App).Stop of CrossDataApp.App.
func (cda *CrossDataApp) Stop() {
}

func (cda *CrossDataApp) addGameServer(service *GameServerService) {
	cda.serversLock.Lock()
	defer cda.serversLock.Unlock()

	serviceKey := cda.getServiceKey(service.serverId)
	cda.gameServers[serviceKey] = service
	cda.channelToHost[service.GetRpcChannel().ChannelUUID] = service
}

func (cda *CrossDataApp) removeGameServer(service *GameServerService) {
	cda.serversLock.Lock()
	defer cda.serversLock.Unlock()

	serviceKey := cda.getServiceKey(service.serverId)
	delete(cda.gameServers, serviceKey)
	delete(cda.channelToHost, service.GetRpcChannel().ChannelUUID)
}

func (cda *CrossDataApp) getServiceKey(serverId uint32) string {
	return strconv.Itoa(int(serverId))
}

func NewCrossDataApp() *CrossDataApp {
	db, err := sql.Open("mysql", fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8",
		CrossDataConfig.Mysql.User, CrossDataConfig.Mysql.Passwd, CrossDataConfig.Mysql.Addr, CrossDataConfig.Mysql.Db))

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

	app := CrossDataApp{common.App{AppName: "CrossDataApp"},
		sync.RWMutex{},
		make(map[string]*GameServerService),
		make(map[uuid.UUID]*GameServerService),
		NewGuildData(),
		NewSiegeWarData(db),
	}
	return &app
}

func (cda *CrossDataApp) getGameServer(serverId uint32) *GameServerService {
	cda.serversLock.RLock()
	defer cda.serversLock.RUnlock()

	serviceKey := cda.getServiceKey(serverId)
	if gs, ok := cda.gameServers[serviceKey]; ok {
		return gs
	}
	return nil
}
