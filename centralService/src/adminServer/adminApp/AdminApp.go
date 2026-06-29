package adminApp

import (
	gsmanager "centralService/src/adminServer/adminProto/gsmanager"
	webService "centralService/src/adminServer/adminProto/webservice"
	"centralService/src/appLog"
	"centralService/src/common"
	"errors"
	"fmt"
	"log"
	"math/rand"
	"net"
	"net/http"
	"strings"
	"sync"

	"github.com/google/uuid"
	"github.com/improbable-eng/grpc-web/go/grpcweb"
	"golang.org/x/time/rate"
	"google.golang.org/grpc"

	"centralService/src/trpc"

	"github.com/garyburd/redigo/redis"
)

const (
	_ = iota
	SERVICE_ADMINSERVER
)

var adminConfig AdminConfig = AdminConfig{}

func NewAdminApp() *AdminApp {
	err := common.GetConfig("adminConfig.json", &adminConfig)
	if err != nil {
		appLog.Error("failed to parse config file\n")
		return nil
	}
	gameServers := make(map[uint32]map[uint32]*GameServerInfo)
	channelMap := make(map[uuid.UUID]uint32)
	accountCmds := make(map[string]chan *gsmanager.HttpAPICommandResponse)

	redisPool := common.NewRedisPool(common.RedisPoolOptions{
		ServerName:  "admin",
		Addr:        adminConfig.RedisServer.Addr,
		Username:    adminConfig.RedisServer.Username,
		Password:    adminConfig.RedisServer.Passwd,
		Db:          adminConfig.RedisServer.Db,
		MaxIdle:     16,
		MaxActive:   16,
		IdleTimeout: 100,
	})

	return &AdminApp{common.App{AppName: "adminServer"}, nil, nil, nil, redisPool,
		gameServers, channelMap, accountCmds, new(sync.RWMutex), new(sync.RWMutex), new(sync.RWMutex)}
}

type AdminAppAction func(app *AdminApp) error

type GameServerInfo struct {
	serverName          string
	AdminService        trpc.IServerEndPoint
	PendingCommands     map[string]chan *webService.CommandResult
	PendingHttpCommands map[string]chan *gsmanager.HttpAPICommandResponse
	PendingAllHttpCmds  map[string]chan *gsmanager.HttpAPICommandResponse
	comps               *Components

	rwLockCommand     *sync.RWMutex
	rwLockHttpCommand *sync.RWMutex
	rwLockAllHtpCmds  *sync.RWMutex
	rwLockComps       *sync.RWMutex
}

func (mgr *GameServerInfo) AddPendingCommands(key string, data chan *webService.CommandResult) {
	mgr.rwLockCommand.Lock()
	defer mgr.rwLockCommand.Unlock()
	mgr.PendingCommands[key] = data
}

func (mgr *GameServerInfo) RemovePendingCommands(key string) {
	mgr.rwLockCommand.Lock()
	defer mgr.rwLockCommand.Unlock()
	delete(mgr.PendingCommands, key)
}

func (mgr *GameServerInfo) AddPendingHttpCommands(key string, data chan *gsmanager.HttpAPICommandResponse) {
	mgr.rwLockHttpCommand.Lock()
	defer mgr.rwLockHttpCommand.Unlock()
	mgr.PendingHttpCommands[key] = data
}

func (mgr *GameServerInfo) RemovePendingHttpCommands(key string) {
	mgr.rwLockHttpCommand.Lock()
	defer mgr.rwLockHttpCommand.Unlock()
	delete(mgr.PendingHttpCommands, key)
}

func (mgr *GameServerInfo) AddPendingAllHttpCmds(key string, data chan *gsmanager.HttpAPICommandResponse) {
	mgr.rwLockAllHtpCmds.Lock()
	defer mgr.rwLockAllHtpCmds.Unlock()
	mgr.PendingAllHttpCmds[key] = data
}

func (mgr *GameServerInfo) RemovePendingAllHttpCmds(key string) {
	mgr.rwLockAllHtpCmds.Lock()
	defer mgr.rwLockAllHtpCmds.Unlock()
	delete(mgr.PendingAllHttpCmds, key)
}

type AdminApp struct {
	common.App
	GmtService     *GRPCAPIService
	httpService    *HttpCommandService
	httpSDKService *HttpSDKService
	redisPool      *redis.Pool

	gameServers            map[uint32]map[uint32]*GameServerInfo
	ChannelToHost          map[uuid.UUID]uint32
	PendingAccountCommands map[string]chan *gsmanager.HttpAPICommandResponse

	rwLockGameServers            *sync.RWMutex
	rwLockChannelToHost          *sync.RWMutex
	rwLockPendingAccountCommands *sync.RWMutex
}

func (self *AdminApp) AddPendingAccountCommands(key string, data chan *gsmanager.HttpAPICommandResponse) {
	self.rwLockPendingAccountCommands.Lock()
	defer self.rwLockPendingAccountCommands.Unlock()
	self.PendingAccountCommands[key] = data
}

func (self *AdminApp) RemovePendingAccountCommands(key string) {
	self.rwLockPendingAccountCommands.Lock()
	defer self.rwLockPendingAccountCommands.Unlock()
	delete(self.PendingAccountCommands, key)
}

func (self *AdminApp) GetServices() []*common.ServiceInfo {
	services := []*common.ServiceInfo{&common.ServiceInfo{SERVICE_ADMINSERVER, "游戏服监听", adminConfig.AddressForGameServer}}
	return services
}

func (self *AdminApp) StartGRPCService() {
	server := grpc.NewServer()
	grpcService := GRPCAPIService{app: self}
	self.GmtService = &grpcService
	webService.RegisterAdminWebServer(server, &grpcService)

	gmtServer := grpcweb.WrapServer(server)
	handler := func(resp http.ResponseWriter, req *http.Request) {
		gmtServer.ServeHTTP(resp, req)
	}

	gmtHttpServer := http.Server{
		Addr:    adminConfig.AddressForGMT,
		Handler: http.HandlerFunc(handler),
	}

	go func() {
		if err := gmtHttpServer.ListenAndServe(); err != nil {
			log.Fatalf("failed starting http server: %v", err)
		}
	}()

	if adminConfig.AddreesForGRPC != "" {
		gs := grpc.NewServer()
		lis, err := net.Listen("tcp", adminConfig.AddreesForGRPC)
		if err != nil {
			log.Fatalf("grpc server: failed to listen: %v", err)
		}
		webService.RegisterAdminWebServer(gs, &grpcService)
		go gs.Serve(lis)
	}
}

func (self *AdminApp) Start() {
	self.StartGRPCService()

	go self.StartDebugService(adminConfig.AddressForDebug)

	limiter := rate.NewLimiter(1.2, 1)
	self.httpService = &HttpCommandService{
		app:              self,
		rateLimiter:      limiter,
		idempotencyMap:   make(map[string]*idempotencyEntry),
		idempotencyMutex: sync.RWMutex{},
		pendingRequests:  make(map[string][]chan *CommandResponse),
		pendingMutex:     sync.Mutex{},
	}
	go self.httpService.startHttpApiServer(adminConfig.HttpAPIAddress)

	self.httpSDKService = &HttpSDKService{self}
	go self.httpSDKService.startHttpApiServer(adminConfig.HttpSDKAddress)

}

func (self *AdminApp) Stop() {

}

func (self *AdminApp) GetRandomServerId() uint32 {
	self.rwLockGameServers.RLock()
	defer self.rwLockGameServers.RUnlock()
	k := rand.Intn(len(self.gameServers))
	for sid, _ := range self.gameServers {
		if k == 0 {
			return sid
		}
		k -= 1
	}
	return 0
}

func (self *AdminApp) GetGameServer(serverId uint32, compId uint32) *GameServerInfo {
	self.rwLockGameServers.RLock()
	defer self.rwLockGameServers.RUnlock()
	if gameServerMap, ok := self.gameServers[serverId]; ok {
		if len(gameServerMap) == 0 {
			return nil
		}
		if compId == 0 {
			k := rand.Intn(len(gameServerMap))
			for _, gameServer := range gameServerMap {
				if k == 0 {
					return gameServer
				}
				k -= 1
			}
		} else if gameServer, okk := gameServerMap[compId]; okk {
			adminServ := gameServer.AdminService.(*GameServerService)
			if adminServ.status != AdminServiceStatus_Connected {
				return nil
			}
			return gameServer
		}
	}
	return nil
}

func (self *AdminApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	if serviceType == SERVICE_ADMINSERVER {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service := &GameServerService{ServerEndPoint: gsmanager.NewAdminService(gsmanager.NewGameServerClient(channel)), app: self, status: AdminServiceStatus_Connected}
		channel.SetEndPoint(service)
		return service
	}
	return nil
}

func (self *AdminApp) doRegisterServer(hostId uint32, compId uint32, hostName string, service trpc.IServerEndPoint) error {
	appLog.Info("register server:", hostId, compId, hostName)
	if hostId == 0 {
		return errors.New(fmt.Sprint("register server err: invalid hostId:", hostId))
	}

	ipAddr := service.(trpc.IServerEndPoint).GetRpcChannel().GetRemoteAddr().String()
	machineIp := strings.Split(ipAddr, ":")[0]
	comps := findComponents(machineIp)

	self.rwLockGameServers.Lock()
	defer self.rwLockGameServers.Unlock()

	pendingCmds := make(map[string]chan *webService.CommandResult)
	idipPendingCmds := make(map[string]chan *gsmanager.HttpAPICommandResponse)
	pendingAllHttpCmds := make(map[string]chan *gsmanager.HttpAPICommandResponse)

	if _, ok := self.gameServers[hostId]; !ok {
		self.gameServers[hostId] = make(map[uint32]*GameServerInfo)
	}
	self.gameServers[hostId][compId] = &GameServerInfo{
		hostName, service, pendingCmds, idipPendingCmds, pendingAllHttpCmds,
		comps, new(sync.RWMutex), new(sync.RWMutex), new(sync.RWMutex), new(sync.RWMutex)}
	self.ChannelToHost[service.(trpc.IServerEndPoint).GetRpcChannel().ChannelUUID] = hostId

	return nil
}

func (self *AdminApp) unRegisterServer(service *GameServerService) {
	appLog.Info("unRegisterServer", service.serverId, service.compId)
	self.rwLockGameServers.Lock()
	defer self.rwLockGameServers.Unlock()

	if gameServerMap, ok := self.gameServers[service.serverId]; ok {
		if gameServer, ok := gameServerMap[service.compId]; ok {
			delete(gameServerMap, service.compId)
			delete(self.ChannelToHost, gameServer.AdminService.(trpc.IServerEndPoint).GetRpcChannel().ChannelUUID)
		}

		if len(gameServerMap) == 0 {
			delete(self.gameServers, service.serverId)
		}
	}
}

func (self *AdminApp) calcAllValidServers() int {
	num := 0
	self.rwLockGameServers.RLock()
	defer self.rwLockGameServers.RUnlock()

	for _, gameServerMap := range self.gameServers {
		for _, gameServer := range gameServerMap {
			if gameServer != nil {
				num += 1
			}
		}
	}
	return num
}

func (self *AdminApp) clearHttpCommands(uuidStr string) {
	self.rwLockGameServers.RLock()
	defer self.rwLockGameServers.RUnlock()

	for serverId, gameServerMap := range self.gameServers {
		for compId, gameServer := range gameServerMap {
			if gameServer != nil {
				gameServer.RemovePendingHttpCommands(uuidStr)
				gameServer.RemovePendingAllHttpCmds(uuidStr)
			} else {
				appLog.Error("clear server http commands error", uuidStr, serverId, compId)
			}
		}
	}
}
