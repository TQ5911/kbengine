package Queue

import (
	"centralService/src/appLog"
	"centralService/src/common"
	clientService "centralService/src/queueServer/queueApp/clientService"
	gameServerService "centralService/src/queueServer/queueApp/gameServerService"
	"centralService/src/trpc"
	"fmt"
	"net"
	"sync"
	"syscall"
	"time"

	"github.com/gomodule/redigo/redis"
	_ "github.com/go-sql-driver/mysql"
	"github.com/google/uuid"
	"github.com/spf13/viper"
	"golang.org/x/time/rate"
)

var QueueConfig = AppConfig{}
var ServerListCfg = viper.New()
var ConfMD5 = ""
var MaxOnlineNum int = 10000
var LimitPerSecond = 10

const (
	_ = iota
	SERVICE_CLIENT_AUTH
	SERVICE_GAME_SERVER
)

type LoginAction func(*QueueApp) error

type QueueApp struct {
	common.App
	gameServers      map[uint32]*GameServerService
	channelToHost    map[uuid.UUID]*GameServerService
	serversLock      *sync.RWMutex
	gameClients      map[string]*QueueClientService
	channelToClient  map[uuid.UUID]*QueueClientService
	clientsLock      *sync.RWMutex
	actions          chan LoginAction
	serverQueues     map[uint32]*Queue
	serverVIPQueues  map[uint32]*Queue
	queuesLock       *sync.RWMutex
	httpServer       *HttpService
	redisPool        *redis.Pool
	waitMapServerMgr *WaitMapServerMgr
}

func NewQueueApp() *QueueApp {
	gameServers := make(map[uint32]*GameServerService)
	channelToHost := make(map[uuid.UUID]*GameServerService)
	gameClients := make(map[string]*QueueClientService)
	channelToClient := make(map[uuid.UUID]*QueueClientService)
	actions := make(chan LoginAction, 10)
	serverQueues := make(map[uint32]*Queue)
	serverVIPQueues := make(map[uint32]*Queue)

	redisPool := common.NewRedisPool(common.RedisPoolOptions{
		ServerName:  "queue",
		Addr:        QueueConfig.RedisServer.Addr,
		Username:    QueueConfig.RedisServer.Username,
		Password:    QueueConfig.RedisServer.Passwd,
		Db:          QueueConfig.RedisServer.Db,
		MaxIdle:     16,
		MaxActive:   1000,
		IdleTimeout: 100,
	})
	waitMapServerMgr := NewWaitMapServerMgr(nil)

	app := QueueApp{
		common.App{AppName: "QueueApp"},
		gameServers,
		channelToHost,
		new(sync.RWMutex),
		gameClients,
		channelToClient,
		new(sync.RWMutex),
		actions,
		serverQueues,
		serverVIPQueues,
		new(sync.RWMutex),
		nil,
		redisPool,
		waitMapServerMgr,
	}
	app.waitMapServerMgr.app = &app

	return &app
}

func (self *QueueApp) GetServices() []*common.ServiceInfo {
	return nil
}

func (self *QueueApp) Start() {
	self.App.Start()

	self.RegisterSignals(syscall.SIGINT, syscall.SIGKILL, syscall.SIGTERM)

	fmt.Printf("app starting: %+v\n", QueueConfig)

	go func() {
		<-self.SignalChan
		self.Stop()
	}()

	self.httpServer = &HttpService{app: self}
	go self.StartDebugService(QueueConfig.AddressForDebug)
	self.waitMapServerMgr.Start()
	self.httpServer.startHttpServer(QueueConfig.HttpServer)
}

func (self *QueueApp) Stop() {

}

func (self *QueueApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	var service trpc.IServerEndPoint = nil
	if serviceType == SERVICE_GAME_SERVER {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = &GameServerService{ServerEndPoint: gameServerService.NewQueueServerService(gameServerService.NewGameServerClient(channel)), app: self}
		channel.SetEndPoint(service)
	} else if serviceType == SERVICE_CLIENT_AUTH {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = &QueueClientService{
			ServerEndPoint: clientService.NewQueueServerService(clientService.NewGameClientClient(channel)),
			app:            self,
			activeTickCnt:  0,
			isReqQueue:     false,
			isValid:        true,
			isQueueSuc:     false,
		}
		channel.SetEndPoint(service)
		service.(*QueueClientService).startCheckValidTimer()
	}

	return service
}

func (self *QueueApp) NewHttpClientService(accountName string, serverId string) *QueueClientService {
	serverHost := ServerListCfg.GetString(fmt.Sprintf("serverList.%s", serverId))
	service := &QueueClientService{
		ServerEndPoint: nil,
		app:            self,
		activeTickCnt:  0,
		isReqQueue:     false,
		isValid:        true,
		isQueueSuc:     false,
		serverId:       serverId,
		accountName:    accountName,
		serverHost:     serverHost,
		tLastRecv:      time.Now().Unix(),
	}
	go service.startCheckLastRecvTimer()
	return service
}

func (self *QueueApp) NewHttpServerService(serverId uint32) *GameServerService {
	service := &GameServerService{
		ServerEndPoint: nil,
		app:            self,
		hostId:         serverId,
		limiter:        rate.NewLimiter(rate.Limit(LimitPerSecond), LimitPerSecond),
		queueTicker:    time.NewTicker(time.Second * 1),
		clearTicker:    time.NewTicker(time.Second * 5),
	}
	self.addGameServer(service)
	go service.tickQueue()
	go service.clearQueue()
	return service
}

func (self *QueueApp) addClient(service *QueueClientService) {
	keyName := service.accountName
	//如果有老的，先把老的删了，否则客户端不断开快速连过来时，上一个连接超时会把当前的删掉
	self.clientsLock.Lock()
	defer self.clientsLock.Unlock()

	oldClient, ok := self.gameClients[keyName]

	if ok {
		self.removeClient(oldClient, false)
	}

	self.gameClients[keyName] = service
	//self.channelToClient[service.GetRpcChannel().ChannelUUID] = service
}

func (self *QueueApp) removeClient(service *QueueClientService, optional ...bool) {
	if !service.isValid {
		return
	}
	needLock := true
	if len(optional) == 1 {
		needLock = optional[0]
	}

	if needLock {
		self.clientsLock.Lock()
		defer self.clientsLock.Unlock()
	}

	service.isValid = false
	keyName := service.accountName
	delete(self.gameClients, keyName)
	//delete(self.channelToClient, service.GetRpcChannel().ChannelUUID)
	//serverId := common.Str2UInt32(service.serverId)
	//accountName := service.accountName
	//if !service.isQueueSuc {
	//	self.removeFromQueue(serverId, accountName)
	//}
}

func (self *QueueApp) getClient(accountName string) *QueueClientService {
	self.clientsLock.RLock()
	defer self.clientsLock.RUnlock()
	keyName := accountName
	if clientSvc, ok := self.gameClients[keyName]; ok {
		return clientSvc
	}
	return nil
}

func remove(slice []uint32, elem uint32) []uint32 {
	for i := range slice {
		if slice[i] == elem {
			slice = append(slice[:i], slice[i+1:]...)
			return slice
		}
	}
	return slice
}

func (self *QueueApp) addGameServer(service *GameServerService) {
	self.serversLock.Lock()
	defer self.serversLock.Unlock()

	self.gameServers[service.hostId] = service
	//self.channelToHost[service.GetRpcChannel().ChannelUUID] = service
}

func (self *QueueApp) removeGameServer(service *GameServerService) {
	self.serversLock.Lock()
	defer self.serversLock.Unlock()

	delete(self.gameServers, service.hostId)
	//delete(self.channelToHost, service.GetRpcChannel().ChannelUUID)
}

func (self *QueueApp) getGameServer(hostId uint32) *GameServerService {
	self.serversLock.RLock()
	defer self.serversLock.RUnlock()

	if gs, ok := self.gameServers[hostId]; ok {
		return gs
	}
	return nil
}

func (self *QueueApp) enQueue(serverId uint32, accountName string, isVIP bool) int {
	self.queuesLock.Lock()
	defer self.queuesLock.Unlock()
	queueId := -1

	var tarQueueMap *map[uint32]*Queue
	if isVIP {
		tarQueueMap = &self.serverVIPQueues
	} else {
		tarQueueMap = &self.serverQueues
	}

	if queue, ok := (*tarQueueMap)[serverId]; ok {
		queueId = queue.Enqueue(Item(accountName))
	} else {
		queue := NewQueue()
		queueId = queue.Enqueue(Item(accountName))
		(*tarQueueMap)[serverId] = queue
	}
	return queueId
}

func (self *QueueApp) clearQueue(serverId uint32) {
	self.queuesLock.Lock()
	defer self.queuesLock.Unlock()

	appLog.Info("clearQueue: ", serverId)
	if queue, ok := self.serverVIPQueues[serverId]; ok {
		queue.mut.Lock()
		defer queue.mut.Unlock()
		tempQueue := NewQueue()
		tempMap := make(map[string]bool)
		for i := range queue.Items {
			client := self.getClient(string(queue.Items[i]))
			if client != nil {
				if _, ok := tempMap[string(queue.Items[i])]; !ok {
					tempMap[string(queue.Items[i])] = true
					tempQueue.Enqueue(queue.Items[i])
				}
			}
		}
		self.serverVIPQueues[serverId].Items = tempQueue.Items
	}

	if queue, ok := self.serverQueues[serverId]; ok {
		queue.mut.Lock()
		defer queue.mut.Unlock()
		tempQueue := NewQueue()
		tempMap := make(map[string]bool)
		for i := range queue.Items {
			client := self.getClient(string(queue.Items[i]))
			if client != nil {
				if _, ok := tempMap[string(queue.Items[i])]; !ok {
					tempMap[string(queue.Items[i])] = true
					tempQueue.Enqueue(queue.Items[i])
				}
			}
		}
		self.serverQueues[serverId].Items = tempQueue.Items
	}
}

func (self *QueueApp) deQueue(serverId uint32) *Item {
	self.queuesLock.Lock()
	defer self.queuesLock.Unlock()

	if queue, ok := self.serverVIPQueues[serverId]; ok {
		res := queue.Dequeue()
		if res != nil {
			return res
		}
	}

	if queue, ok := self.serverQueues[serverId]; ok {
		return queue.Dequeue()
	}
	return nil
}

// 目标服当前排队人数（普通队列+VIP队列）
func (self *QueueApp) queueSize(serverId uint32) int {
	self.queuesLock.RLock()
	defer self.queuesLock.RUnlock()

	size := 0
	if queue, ok := self.serverQueues[serverId]; ok {
		queue.mut.Lock()
		size += len(queue.Items)
		queue.mut.Unlock()
	}
	if queue, ok := self.serverVIPQueues[serverId]; ok {
		queue.mut.Lock()
		size += len(queue.Items)
		queue.mut.Unlock()
	}
	return size
}

func (self *QueueApp) buildAccountKey(accountType string, accountName string) string {
	return common.JoinToStr(accountName, ":", accountType)
}

func (self *QueueApp) QueueTick(serverId uint32) *Queue {
	self.queuesLock.Lock()
	defer self.queuesLock.Unlock()

	if queue, ok := self.serverQueues[serverId]; ok {
		queue.mut.Lock()
		defer queue.mut.Unlock()
		for i := range queue.Items {
			client := self.getClient(string(queue.Items[i]))
			if client != nil {
				client.SetQueueId(i + 1)
			}
		}
	}

	if vipQueue, ok := self.serverVIPQueues[serverId]; ok {
		vipQueue.mut.Lock()
		defer vipQueue.mut.Unlock()
		for i := range vipQueue.Items {
			client := self.getClient(string(vipQueue.Items[i]))
			if client != nil {
				client.SetQueueId(i + 1)
			}
		}
	}
	return nil
}
