package app

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"centralService/src/trpc"
	"crypto/md5"
	"database/sql"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"math/rand"
	"net"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"

	"centralService/src/orderService/httputil"
	"centralService/src/orderService/service"

	cmap "centralService/src/common/concurrent_map"

	"github.com/fsnotify/fsnotify"
	"github.com/garyburd/redigo/redis"
	_ "github.com/go-sql-driver/mysql"
	"github.com/google/uuid"
	"github.com/spf13/viper"
)

const (
	_ = iota
	SERVICE_order
)

type CfgData struct {
	cfgVipers       cmap.ConcurrentMap[string, *viper.Viper]
	cfgFileMD5Datas cmap.ConcurrentMap[string, string]
	cfgFiles        map[string]string
}

type MysqlConfig struct {
	Addr     string
	User     string
	Password string
	Db       string
}

type RedisConfig struct {
	Addr     string
	Username string
	Password string
	Db       int
}

type AppConfig struct {
	GameServerServiceAddr string
	ServerName            string
	ServerId              uint32
	LogPath               string
	LogLevel              int
	LogRotateSize         string
	Mysql                 MysqlConfig
	Redis                 RedisConfig
	HttpAddr              string
	ApiSecret             string
	OrderDataSecret       string
	PayNotifyApi          string
	PayNotifySecret       string
}

var OrderServiceConfig = AppConfig{}

type ServerConfig struct {
}

type GameServerInfo struct {
	serverName   string
	OrderService trpc.IServerEndPoint
	rwLock       *sync.RWMutex
}

type OrderApp struct {
	common.App
	redisPool     *redis.Pool
	db            *sql.DB
	httpService   *HttpCommandService
	gameServers   map[uint32]map[uint32]*GameServerInfo
	ChannelToHost map[uuid.UUID]uint32
	serversMutex  *sync.RWMutex
	OrderChan     chan *OrderData
}

func InitConfigStore() bool {
	ConfigStore = &CfgData{
		cfgFileMD5Datas: cmap.New[string](),
		cfgVipers:       cmap.New[*viper.Viper](),
		cfgFiles:        GetCfgFiles(),
	}
	for cfgType, cfgFilePath := range ConfigStore.cfgFiles {
		ret := InitJsonCfg(cfgType, cfgFilePath)
		if ret != nil {
			appLog.Error("cfg init failed ", ret.Error(), cfgType, cfgFilePath)
			return ret != nil
		}
	}
	return ConfigStore != nil
}

func InitJsonCfg(cfgType string, cfgPath string) error {
	cfg := viper.New()
	cfg.SetConfigType("json")
	cfg.SetConfigFile(cfgPath)
	err := cfg.ReadInConfig()
	if err != nil {
		appLog.Error("Error reading cfg file", err.Error(), cfgPath)
		return err
	}
	cfgMD5, err := common.ReadFileMd5(cfgPath)
	if err != nil {
		appLog.Error("fail to get config md5:", err.Error())
		return err
	}
	// 记录文件MD5
	ConfigStore.cfgFileMD5Datas.Set(cfgType, cfgMD5)
	// 记录viper
	ConfigStore.cfgVipers.Set(cfgType, cfg)
	// 设置文件变化事件监听
	cfg.OnConfigChange(func(e fsnotify.Event) {
		appLog.Info("cfg file changed:", e.Name)
		curMD5, err := common.ReadFileMd5(cfgPath)
		if err != nil {
			appLog.Error("fail to get cfg md5 error", err.Error())
			return
		}

		oldMD5, ret := ConfigStore.cfgFileMD5Datas.Get(cfgType)
		if ret {
			if curMD5 == oldMD5 {
				appLog.Info("cfg file no changed:", e.Name, curMD5, oldMD5)
				return
			}
		}

		appLog.Info("cfg file real changed:", e.Name, curMD5, oldMD5)
		ConfigStore.cfgFileMD5Datas.Set(cfgType, curMD5)
		err = cfg.ReadInConfig()
		if err != nil {
			appLog.Error("Error reading cfg file", err.Error())
		}
	})
	// 启动文件监听
	cfg.WatchConfig()
	return nil
}

func NewOrderApp() *OrderApp {
	if !InitConfigStore() {
		appLog.Error("init config store error !!!")
		return nil
	}

	db, err := sql.Open("mysql", fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8",
		OrderServiceConfig.Mysql.User, OrderServiceConfig.Mysql.Password, OrderServiceConfig.Mysql.Addr, OrderServiceConfig.Mysql.Db))

	if err != nil {
		appLog.Error("open msyql error: ", err.Error())
		return nil
	}

	if err = db.Ping(); err != nil {
		appLog.Error("mysql connect err", err.Error())
		return nil
	}

	redisCli := common.NewRedisPool(common.RedisPoolOptions{
		ServerName:  "orderService",
		Addr:        OrderServiceConfig.Redis.Addr,
		Username:    OrderServiceConfig.Redis.Username,
		Password:    OrderServiceConfig.Redis.Password,
		Db:          strconv.Itoa(OrderServiceConfig.Redis.Db),
		MaxIdle:     16,
		MaxActive:   100,
		IdleTimeout: 100,
	})
	if redisCli == nil {
		return nil
	}

	app := OrderApp{
		App:           common.App{AppName: OrderServiceConfig.ServerName},
		redisPool:     redisCli,
		db:            db,
		serversMutex:  &sync.RWMutex{},
		gameServers:   make(map[uint32]map[uint32]*GameServerInfo),
		httpService:   &HttpCommandService{},
		ChannelToHost: make(map[uuid.UUID]uint32),
		OrderChan:     make(chan *OrderData),
	}
	return &app
}

func (mg *OrderApp) GetServices() []*common.ServiceInfo {
	services := []*common.ServiceInfo{
		{
			ServiceType:       SERVICE_GAME_SERVER,
			ServiceName:       "游戏服连接监听",
			ServiceListenAddr: OrderServiceConfig.GameServerServiceAddr,
		},
	}
	return services
}

func (mg *OrderApp) Start() {
	mg.httpService.app = mg
	go mg.httpService.startHttpApiServer(OrderServiceConfig.HttpAddr)
}

func (mg *OrderApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	var clientService trpc.IServerEndPoint = nil
	if serviceType == SERVICE_GAME_SERVER {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		clientService = &OrderService{ServerEndPoint: service.NewOrderServiceService(service.NewGameServerClient(channel)), app: mg, status: ServiceStatus_Connected}
		channel.SetEndPoint(clientService)
	}

	return clientService
}

func (mg *OrderApp) doRegisterServer(hostId uint32, compId uint32, hostName string, service trpc.IServerEndPoint) error {
	appLog.Infow("register server", "hostId", hostId, "compId", compId, "hostName", hostName)
	if hostId == 0 {
		return errors.New(fmt.Sprint("register server err: invalid hostId:", hostId))
	}

	mg.serversMutex.Lock()
	defer mg.serversMutex.Unlock()

	if _, ok := mg.gameServers[hostId]; !ok {
		mg.gameServers[hostId] = make(map[uint32]*GameServerInfo)
	}
	mg.gameServers[hostId][compId] = &GameServerInfo{
		hostName, service,
		new(sync.RWMutex)}
	mg.ChannelToHost[service.GetRpcChannel().ChannelUUID] = hostId

	return nil
}

func (mg *OrderApp) unRegisterServer(service *OrderService) {
	appLog.Infow("unRegisterServer", "serverId", service.serverId, "compId", service.compId)
	mg.serversMutex.Lock()
	defer mg.serversMutex.Unlock()

	if gameServerMap, ok := mg.gameServers[service.serverId]; ok {
		if gameServer, ok := gameServerMap[service.compId]; ok {
			delete(gameServerMap, service.compId)
			delete(mg.ChannelToHost, gameServer.OrderService.GetRpcChannel().ChannelUUID)
		}

		if len(gameServerMap) == 0 {
			delete(mg.gameServers, service.serverId)
		}
	}
}

func (mg *OrderApp) AddOrder(order *OrderData) {
	go func(order *OrderData) {
		mg.OrderChan <- order
	}(order)
}

func (mg *OrderApp) GetOrderService(serverId uint32, compId uint32) *OrderService {
	mg.serversMutex.RLock()
	defer mg.serversMutex.RUnlock()
	if gameServerMap, ok := mg.gameServers[serverId]; ok {
		if len(gameServerMap) == 0 {
			return nil
		}
		if compId == 0 {
			k := rand.Intn(len(gameServerMap))
			for _, gameServer := range gameServerMap {
				if k == 0 {
					orderService := gameServer.OrderService.(*OrderService)
					if nil == orderService || orderService.status != ServiceStatus_Connected {
						return nil
					}
					return orderService
				}
				k -= 1
			}
		} else if gameServer, okk := gameServerMap[compId]; okk {
			orderService := gameServer.OrderService.(*OrderService)
			if nil == orderService || orderService.status != ServiceStatus_Connected {
				return nil
			}
			return orderService
		}
	}
	return nil
}

func (mg *OrderApp) doAcquireOrderLock(outTradeNo string) (bool, error) {
	lockKey := GetOrderLockKey(outTradeNo)
	conn := mg.redisPool.Get()
	defer conn.Close()
	_, err := conn.Do("SET", lockKey, 1, "NX", "EX", Order_Lock_Time)
	if err == redis.ErrNil {
		return false, nil
	}
	if err != nil {
		return false, err
	}
	return true, nil
}

func (mg *OrderApp) doReleaseOrderLock(outTradeNo string) error {
	lockKey := GetOrderLockKey(outTradeNo)
	conn := mg.redisPool.Get()
	defer conn.Close()
	_, err := conn.Do("DEL", lockKey)
	return err
}

func (mg *OrderApp) ProcessOrder(order *OrderData, svc *HttpCommandService, w http.ResponseWriter) {
	appLog.Debugf("ProcessOrder, outTradeNo: %v", order.OutTradeNo)
	// createTime
	layout := "2006-01-02 15:04:05"
	createTime, err := time.Parse(layout, order.CreateTime)
	if err != nil {
		appLog.Errorf("ProcessOrder create time error, roleId: %v, serverId: %v outTradeNo: %v, createTime:%v ", order.UserRoleId, order.ServerId, order.OutTradeNo, order.CreateTime)
		errMsg := "create time error"
		responseBytes := svc._buildErrResponse(ARGS_ERR, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	// payTime
	payTime, err := time.Parse(layout, order.PayTime)
	if err != nil {
		appLog.Errorf("ProcessOrder create time error, roleId: %v, serverId: %v outTradeNo: %v, payTime:%v ", order.UserRoleId, order.ServerId, order.OutTradeNo, order.PayTime)
		errMsg := "pay time error"
		responseBytes := svc._buildErrResponse(ARGS_ERR, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	// 获取本地配置中心
	itemCfg, ret := ConfigStore.cfgVipers.Get(CFG_TYPE_ITEM_DATA)
	if !ret || nil == itemCfg {
		appLog.Error("ProcessOrder missing item cfg store ")
		errMsg := "item cfg missing"
		responseBytes := svc._buildErrResponse(ITEM_CFG_MISSING, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	// 检查product code
	b := itemCfg.GetStringMap(strconv.FormatUint(uint64(order.ProductCode), 10))
	if nil == b {
		appLog.Error("ProcessOrder missing item info cfg ", order.ProductCode)
		errMsg := "product code error"
		responseBytes := svc._buildErrResponse(ARGS_ERR, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	// 获取锁
	ret, err = mg.doAcquireOrderLock(order.OutTradeNo)
	if err != nil {
		appLog.Errorf("ProcessOrder redis get lock fail error: %v, outTradeNo: %v", err.Error(), order.OutTradeNo)
		errMsg := "redis error"
		responseBytes := svc._buildErrResponse(REDIS_ERROR, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}
	// 获取成功后，延迟释放锁
	defer mg.doReleaseOrderLock(order.OutTradeNo)
	if !ret {
		appLog.Debugf("ProcessOrder, in processing, outTradeNo: %v", order.OutTradeNo)
		errMsg := "in processing"
		responseBytes := svc._buildErrResponse(IN_PROCESSING, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}
	// 查询订单状态
	sql := "select orderProcessStatus, serverId, userRoleId, productCode, buyNum, roleName from `orderData` where `OutTradeNo` = ?"
	stmt, err := mg.db.Prepare(sql)
	if err != nil {
		appLog.Errorf("ProcessOrder mysql prepare error: %v, outTradeNo: %v", err.Error(), order.OutTradeNo)
		errMsg := "mysql error"
		responseBytes := svc._buildErrResponse(MYSQL_ERROR, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}
	defer stmt.Close()

	rows, err := stmt.Query(order.OutTradeNo)
	if err != nil {
		appLog.Errorf("ProcessOrder mysql query error: %v, outTradeNo: %v", err.Error(), order.OutTradeNo)
		errMsg := "mysql error"
		responseBytes := svc._buildErrResponse(MYSQL_ERROR, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}
	defer rows.Close()

	orderProcessStatus := -1
	serverId := 0
	gbId := 0
	itemId := 0
	itemCount := 0
	roleName := ""
	for rows.Next() {
		err = rows.Scan(&orderProcessStatus, &serverId, &gbId, &itemId, &itemCount, &roleName)
		if err != nil {
			appLog.Errorf("ProcessOrder mysql scan error: %v, outTradeNo: %v", err.Error(), order.OutTradeNo)
			errMsg := "mysql error"
			responseBytes := svc._buildErrResponse(MYSQL_ERROR, errMsg)
			svc.sendIDIPResponse(w, 200, responseBytes)
			return
		}
		break
	}
	// 订单已入库，成功返回
	if orderProcessStatus != -1 {
		if orderProcessStatus == 1 {
			appLog.Debugf("ProcessOrder, success, outTradeNo: %v", order.OutTradeNo)
			errMsg := "success"
			responseBytes := svc._buildErrResponse(SUCCESS, errMsg)
			svc.sendIDIPResponse(w, 200, responseBytes)
		} else if orderProcessStatus == 0 {
			mg.SendToGameServer(order, svc, w, createTime.Unix(), int32(itemId), int32(itemCount), order.PayableAmount, uint64(gbId), uint32(serverId), roleName)
		}
		return
	}

	sql = "INSERT INTO `orderData` (`orderNo`, `outTradeNo`,`createTime`,`gameId`,`userGameId`," +
		"`userId`, `userRoleId`, `roleName`, `serverId`, `serverName`, `productId`,`productCode`," +
		"`channelProductId`, `productName`, `buyNum`, `payTime`, `payableAmount`, `actualAmount`," +
		"`payType`, `orderSource`, `orderProcessStatus`, `addToSafe`)" +
		" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	result, err := mg.db.Exec(sql, order.OrderNo, order.OutTradeNo, createTime.Unix(), order.GameId, order.UserGameId,
		order.UserId, order.UserRoleId, order.RoleName, order.ServerId, order.ServerName, order.ProductId,
		order.ProductCode, order.ChannelProductId, order.ProductName, order.BuyNum, payTime.Unix(), order.PayableAmount,
		order.ActualAmount, order.PayType, order.OrderSource, 0, order.AddToSafe)
	if err != nil {
		appLog.Errorf("ProcessOrder insert order to db error: %v, outTradeNo: %v", err.Error(), order.OutTradeNo)
		errMsg := "mysql error"
		responseBytes := svc._buildErrResponse(MYSQL_ERROR, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	affectedCount, err := result.RowsAffected()
	if err != nil {
		appLog.Errorf("ProcessOrder insert order then get row affected error: %v, outTradeNo: %v", err.Error(), order.OutTradeNo)
		errMsg := "mysql error"
		responseBytes := svc._buildErrResponse(MYSQL_ERROR, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	if affectedCount != 1 {
		appLog.Errorf("ProcessOrder row affected wrong: %v, outTradeNo: %v", affectedCount, order.OutTradeNo)
		errMsg := "mysql error"
		responseBytes := svc._buildErrResponse(MYSQL_ERROR, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
	}

	mg.SendToGameServer(order, svc, w, createTime.Unix(), order.ProductCode, int32(order.BuyNum), order.PayableAmount, uint64(order.UserRoleId), uint32(order.ServerId), order.RoleName)

	appLog.Debugf("ProcessOrder success, outTradeNo: %v", order.OutTradeNo)
	return
}

func (mg *OrderApp) SendToGameServer(order *OrderData, svc *HttpCommandService, w http.ResponseWriter, createTime int64, itemId int32, itemCount int32, itemPrice float32, gbId uint64, serverId uint32, roleName string) {
	orderService := mg.GetOrderService(uint32(serverId), 0)
	if orderService != nil {
		response := &service.OrderRequest{}
		response.ServerId = order.ServerId
		response.OutTradeNo = order.OutTradeNo
		response.CreateTime = createTime
		response.ItemId = int32(itemId)
		response.ItemCount = int32(itemCount)
		response.GbId = int64(gbId)
		response.Price = float64(itemPrice)
		response.AddToSafe = order.AddToSafe == 1
		response.RoleName = roleName
		_, err := orderService.GetClientEndPoint().(service.IGameServerInterface).NotifyOrder(response)
		if err != nil {
			appLog.Errorf("ProcessOrder send order to game error: %v, outTradeNo: %v", err.Error(), order.OutTradeNo)
			errMsg := "game server error"
			responseBytes := svc._buildErrResponse(SERVER_ERROR, errMsg)
			svc.sendIDIPResponse(w, 200, responseBytes)
			return
		} else {
			appLog.Debugf("ProcessOrder, in delivery, outTradeNo: %v", order.OutTradeNo)
			errMsg := "in delivery"
			responseBytes := svc._buildErrResponse(IN_DELIVERY, errMsg)
			svc.sendIDIPResponse(w, 200, responseBytes)
		}
	} else {
		appLog.Errorf("ProcessOrder get game service error: missing, gbId: %v, outTradeNo: %v, serverId: %v, itemId: %v, itemCount:%v, itemPrice: %v", gbId, order.OutTradeNo, serverId, itemId, itemCount, itemPrice)
		errMsg := "game server missing"
		responseBytes := svc._buildErrResponse(SERVER_MISSING, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}
}

func (mg *OrderApp) NotifyOrder(OutTradeNo string, OrderResult int32) {
	appLog.Debugf("NotifyOrder, outTradeNo: %v", OutTradeNo)
	if OrderResult != SUCCESS {
		return
	}
	common.ExecuteConcurrentlyWithArgs(func(OutTradeNo string) {
		sql := "UPDATE `orderData` SET `orderProcessStatus` = 1 WHERE `outTradeNo`=?"
		_, err := mg.db.Exec(sql, OutTradeNo)
		if err != nil {
			appLog.Errorf("NotifyOrder update error: %v, outTradeNo:%v", err.Error(), OutTradeNo)
			return
		}
		params := map[string]interface{}{
			"outTradeNo": OutTradeNo,
		}
		jsonData, err := json.Marshal(params)
		if err != nil {
			appLog.Errorf("NotifyOrder marshal error: %v, outTradeNo:%v", err.Error(), OutTradeNo)
			return
		}
		appLog.Infof("NotifyOrder encode string: %v", string(jsonData))
		h := md5.New()
		h.Write(jsonData)
		h.Write([]byte(OrderServiceConfig.PayNotifySecret))

		signVal := hex.EncodeToString(h.Sum(nil))
		sign := strings.ToLower(signVal)
		addr := fmt.Sprintf("%v?sign=%v", OrderServiceConfig.PayNotifyApi, sign)
		respData, err := httputil.PostJson(addr, params)
		if err != nil {
			appLog.Errorf("NotifyOrder post json error: %v, sign:%v, data:%v", err.Error(), sign, string(jsonData))
			return
		}
		appLog.Debugf("NotifyOrder result: %v, sign:%v, data:%v", respData, sign, string(jsonData))
	}, OutTradeNo)
}
