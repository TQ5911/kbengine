package Auction

import (
	"centralService/src/appLog"
	gameServerService "centralService/src/auction/auctionApp/gameServerService"
	"centralService/src/common"
	cmap "centralService/src/common/concurrent_map"
	"centralService/src/trpc"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"hash/fnv"
	"log"

	"github.com/fsnotify/fsnotify"
	_ "github.com/go-sql-driver/mysql"
	"github.com/google/uuid"
	"github.com/spf13/viper"

	//"math"
	"math/rand"
	"net"
	"strconv"
	"strings"
	"sync"
	"syscall"
	"time"
)

var AuctionAppConfig = AppConfig{GmBuyInterception: 0}

type AuctionAction func(*AuctionApp) error

type CfgData struct {
	cfgVipers       cmap.ConcurrentMap[string, *viper.Viper]
	cfgFileMD5Datas cmap.ConcurrentMap[string, string]
	cfgFiles        map[string]string
}

type GameServerInfo struct {
	serverName     string
	AuctionService trpc.IServerEndPoint

	rwLock *sync.RWMutex
}

type AuctionApp struct {
	common.App
	gameServers   map[uint32]map[uint32]*GameServerInfo
	ChannelToHost map[uuid.UUID]uint32
	serversMutex  *sync.RWMutex
	actions       chan AuctionAction
	db            *sql.DB
	auctionMgr    *AuctionMgr
	gmAllBuyNum   uint64
	gmCurBuyNum   uint64
	funcChan      chan func()
}

func InitConfigStore() bool {
	ConfigStore = &CfgData{
		cfgFileMD5Datas: cmap.New[string](),
		cfgVipers:       cmap.New[*viper.Viper](),
		cfgFiles:        GetCfgFiles(),
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
			log.Println("fail to get cfg md5:", err.Error())
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

func NewAuctionApp() *AuctionApp {
	if !InitConfigStore() {
		appLog.Error("init config store error !!!")
		return nil
	}

	gameServers := make(map[uint32]map[uint32]*GameServerInfo)
	channelMap := make(map[uuid.UUID]uint32)
	actions := make(chan AuctionAction, 10)

	db, err := sql.Open("mysql", fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8",
		AuctionAppConfig.Mysql.User, AuctionAppConfig.Mysql.Passwd, AuctionAppConfig.Mysql.Addr, AuctionAppConfig.Mysql.Db))

	if err != nil {
		appLog.Error("open msyql error: ", err.Error())
		return nil
	}

	db.SetMaxIdleConns(3000)
	db.SetConnMaxLifetime(time.Hour * 5)
	db.SetMaxOpenConns(3000)
	if err = db.Ping(); err != nil {
		appLog.Error("mysql connect err", err.Error())
		return nil
	}

	app := AuctionApp{common.App{AppName: "AuctionApp"},
		gameServers,
		channelMap,
		new(sync.RWMutex),
		actions,
		db,
		nil,
		0,
		0,
		make(chan func())}
	// 逐个初始化配置
	for cfgType, cfgPath := range ConfigStore.cfgFiles {
		ret := InitJsonCfg(cfgType, cfgPath)
		if ret != nil {
			appLog.Error("cfg init failed ", ret.Error(), cfgType, cfgPath)
			return nil
		}
	}
	app.auctionMgr = NewAuctionMgr(db, &app)
	return &app
}

func (au *AuctionApp) GetServices() []*common.ServiceInfo {
	services := []*common.ServiceInfo{
		{
			ServiceType:       SERVICE_GAME_SERVER,
			ServiceName:       "游戏服连接监听",
			ServiceListenAddr: AuctionAppConfig.GameServerServiceAddr,
		},
	}
	return services
}

func (au *AuctionApp) Start() {

	au.App.Start()

	au.RegisterSignals(syscall.SIGINT, syscall.SIGKILL, syscall.SIGTERM)

	fmt.Printf("app starting: %+v\n", AuctionAppConfig)

	go func() {
		<-au.SignalChan
		au.Stop()
	}()

	for i := 0; i < 100; i++ {
		go au.procFuncCache()
	}
	go au.StartDebugService(AuctionAppConfig.AddressForDebug)
}

func (au *AuctionApp) Stop() {
	appLog.Info("app stoping...")
	appLog.Sync()
}

func (au *AuctionApp) procFuncCache() {
	for {
		funcCache := <-au.funcChan
		if funcCache == nil {
			continue
		}
		funcCache()
	}
}

func (au *AuctionApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	var service trpc.IServerEndPoint = nil
	if serviceType == SERVICE_GAME_SERVER {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = BuildGameServerService(gameServerService.NewAuctionServerService(gameServerService.NewGameServerClient(channel)), au)
		channel.SetEndPoint(service)
	}

	return service
}

func (au *AuctionApp) doRegisterServer(hostId uint32, compId uint32, hostName string, service trpc.IServerEndPoint) error {
	appLog.Infow("register server", "hostId", hostId, "compId", compId, "hostName", hostName)
	if hostId == 0 {
		return errors.New(fmt.Sprint("register server err: invalid hostId:", hostId))
	}

	au.serversMutex.Lock()
	defer au.serversMutex.Unlock()

	if _, ok := au.gameServers[hostId]; !ok {
		au.gameServers[hostId] = make(map[uint32]*GameServerInfo)
	}
	au.gameServers[hostId][compId] = &GameServerInfo{
		hostName, service,
		new(sync.RWMutex)}
	au.ChannelToHost[service.GetRpcChannel().ChannelUUID] = hostId

	return nil
}

func (au *AuctionApp) unRegisterServer(service *GameServerService) {
	appLog.Infow("unRegisterServer", "serverId", service.serverId, "compId", service.compId)
	au.serversMutex.Lock()
	defer au.serversMutex.Unlock()

	if gameServerMap, ok := au.gameServers[service.serverId]; ok {
		if gameServer, ok := gameServerMap[service.compId]; ok {
			delete(gameServerMap, service.compId)
			delete(au.ChannelToHost, gameServer.AuctionService.GetRpcChannel().ChannelUUID)
		}

		if len(gameServerMap) == 0 {
			delete(au.gameServers, service.serverId)
		}
	}
}

func (au *AuctionApp) GetGameServer(serverId uint32, compId uint32) *GameServerInfo {
	au.serversMutex.RLock()
	defer au.serversMutex.RUnlock()
	if gameServerMap, ok := au.gameServers[serverId]; ok {
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
			adminServ := gameServer.AuctionService.(*GameServerService)
			if adminServ.status != ServiceStatus_Connected {
				return nil
			}
			return gameServer
		}
	}
	return nil
}

func (au *AuctionApp) SaleItem(playerGBID uint64, itemDict string, totalPrice uint64, number uint32, bagType uint8, extra string, addPublicityTime uint32) (*AuctionItem, string, error) {
	var item *ItemData
	if err := json.Unmarshal([]byte(itemDict), &item); err != nil {
		appLog.Errorw("SaleItem: json.Unmarshal err", "itemDict", itemDict)
		return nil, extra, err
	}

	var m map[string]interface{}
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("SaleItem: Decode err", "extra", extra)
		return nil, extra, err
	}

	auctionItemUUID, err := m["opUUID"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("SaleItem: opUUID err", "extra", extra)
		return nil, extra, err
	}

	addTime := time.Now().Unix()
	auctionItem, err := au.auctionMgr.AddAuctionItem(AUCTION_TYPE_COIN, uint64(auctionItemUUID), addTime, item, totalPrice, number, bagType, AUCTION_SOURCE_PLAYER, AUCTION_STATUS_INIT, 0, extra, playerGBID, addPublicityTime)
	if err != nil {
		appLog.Errorw("SaleItem: AddAuctionItem err", "err", err)
		return nil, extra, err
	}
	return auctionItem, extra, nil
}

func (au *AuctionApp) DoSaleItem(auctionItemUUID uint64, playerGBID uint64, extra string, result bool, service *GameServerService) (*AuctionItem, string, error) {
	appLog.Debugw("DoSaleItem", "auctionItemUUID", auctionItemUUID, "playerGBID", playerGBID, "extra", extra, "result", result)
	auctionItem, err := au.auctionMgr.GetAuctionItem(auctionItemUUID)
	if err != nil {
		appLog.Errorw("DoSaleItem: GetAuctionItem err", "err", err)
		return nil, extra, err
	}

	if result {
		var m map[string]interface{}
		dec := json.NewDecoder(strings.NewReader(extra))
		dec.UseNumber()
		err := dec.Decode(&m)
		if err != nil {
			appLog.Errorw("DoSaleItem: Decode err", "extra", extra)
			return nil, extra, err
		}

		status := AUCTION_STATUS_SELLING
		curTime := time.Now().Unix()
		// 检查是否需要公示
		if auctionItem.GetPublicityGap()+auctionItem.AddTime > curTime {
			status = AUCTION_STATUS_PUBLICITY
		}

		err = auctionItem.Add(au.db, uint8(status))
		if err != nil {
			appLog.Errorw("DoSaleItem: Add err", "err", err, "auctionItemUUID", auctionItemUUID, "playerGBID", playerGBID, "extra", extra, "result", result)
			return nil, extra, err
		}

		au.auctionMgr.setStatus(uint8(status), auctionItem, true)
		auctionItemUUIDStr := strconv.FormatUint(auctionItemUUID, 10)

		if status == AUCTION_STATUS_SELLING {
			if _, ok := au.auctionMgr.expiredTimerMap.Get(auctionItemUUIDStr); ok {
				return nil, extra, errors.New("DoSaleItem: already in expiredTimerMap")
			}

			duration := auctionItem.itemExpiredTime() - curTime
			timer := time.AfterFunc(time.Duration(duration)*time.Second, func() {
				au.auctionMgr.setItemExpired(auctionItemUUID)
			})
			au.auctionMgr.expiredTimerMap.Set(auctionItemUUIDStr, timer)
		} else if status == AUCTION_STATUS_PUBLICITY {
			if _, ok := au.auctionMgr.endPublicityTimerMap.Get(auctionItemUUIDStr); ok {
				return nil, extra, errors.New("DoSaleItem: already in endPublicityTimerMap")
			}

			duration := auctionItem.GetPublicityGap() + auctionItem.AddTime - curTime
			if duration > 0 {
				timer := time.AfterFunc(time.Duration(duration)*time.Second, func() {
					au.auctionMgr.setItemSelling(auctionItemUUID, true)
				})
				au.auctionMgr.endPublicityTimerMap.Set(auctionItemUUIDStr, timer)
			} else {
				au.auctionMgr.setItemSelling(auctionItemUUID, false)
			}
		}

		au.RefreshPlayerCoinAuctionData(playerGBID, service)

	} else {
		au.auctionMgr.auctionItems.Remove(strconv.FormatUint(auctionItemUUID, 10))
		return nil, extra, nil
	}

	var m map[string]interface{}
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err = dec.Decode(&m)
	if err != nil {
		appLog.Errorw("DoSaleItem: Decode err", "err", err)
		return nil, extra, err
	}

	tlogProps := m["tlogProps"].(map[string]interface{})
	roleName := tlogProps["role_name"].(string)
	totalPrice := auctionItem.Price
	m["roleName"] = roleName
	m["totalPrice"] = totalPrice

	extraB, err := json.Marshal(m)
	if err != nil {
		appLog.Errorw("DoSaleItem: Marshal err", "err", err)
		return nil, extra, err
	}

	return auctionItem, string(extraB), nil
}

func (au *AuctionApp) GenUUID() uint64 {
	id := uuid.New()
	h := fnv.New64()
	h.Write([]byte(id.String()))
	uuidHash := int64(h.Sum64())
	if uuidHash < 0 {
		uuidHash = -uuidHash
	}
	return uint64(uuidHash)
}

// 购买物品
func (au *AuctionApp) BuyItem(playerGBID uint64, auctionItemUUID uint64, number uint32, extra string) (uint64, string, uint64, int64, uint32, uint32, error) {
	appLog.Debugw("BuyItem", "playerGBID", playerGBID, "auctionItemUUID", auctionItemUUID, "number", number, "extra", extra)

	auctionItem, ret := au.auctionMgr.CheckBuyItem(auctionItemUUID, number)
	if ret != AUCTION_OK {
		switch ret {
		case AUCTION_NOT_IN_AUCTION:
			appLog.Warnw("BuyItem: not in auction", "auctionItemUUID", auctionItemUUID)
		case AUCTION_BUY_ITEM_NOT_ENOUGH:
			appLog.Warnw("BuyItem: buy item not enough", "auctionItemUUID", auctionItemUUID)
		case AUCTION_IS_EXPIRED:
			appLog.Warnw("BuyItem: is expired", "auctionItemUUID", auctionItemUUID)
		case AUCTION_ITEM_IS_LOCKED:
			appLog.Warnw("BuyItem: item is locked", "auctionItemUUID", auctionItemUUID)
		default:
			appLog.Errorw("BuyItem: failed", "ret", ret, "auctionItemUUID", auctionItemUUID)
		}
		return auctionItemUUID, extra, 0, 0, uint32(ret), 0, nil
	}
	buyType := BUY_TYPE_NORMAL
	// 抢购中的，用1做通用的锁，然后时间设定为抢购的两倍时间
	if auctionItem.CheckInSnatch() {
		buyType = BUY_TYPE_SNATCH
		getLock := auctionItem.lock(uint32(auctionItem.getSnatchTime())*2, SNATCH_LOCK_ID, au, true)
		if !getLock {
			appLog.Debugw("BuyItem: get lock failed", "auctionItemUUID", auctionItem.AuctionItemUUID)
			ret = AUCTION_ITEM_IS_LOCKED
			return auctionItemUUID, extra, 0, 0, uint32(ret), 0, nil
		}
	} else {
		getLock := auctionItem.lock(60, playerGBID, au, true)
		if !getLock {
			appLog.Debugw("BuyItem: get lock failed", "auctionItemUUID", auctionItem.AuctionItemUUID)
			ret = AUCTION_ITEM_IS_LOCKED
			return auctionItemUUID, extra, 0, 0, uint32(ret), 0, nil
		}
	}

	var m map[string]interface{}
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		ret = PARAM_ERROR
		appLog.Errorw("BuyItem: NewDecoder err", "err", err)
		return auctionItemUUID, extra, 0, 0, uint32(ret), 0, err
	}

	m["selectItemLocked"] = auctionItem.LockPlayerGBID
	m["auctionBuyItemId"] = auctionItem.ItemData.ItemId
	m["auctionBuyItemNum"] = number

	extraB, err := json.Marshal(m)
	if err != nil {
		ret = PARAM_ERROR
		appLog.Errorw("BuyItem: Marshal err", "err", err)
		return auctionItemUUID, extra, 0, 0, uint32(ret), 0, err
	}
	price := auctionItem.Price
	return auctionItemUUID, string(extraB), price, auctionItem.GetPublicityEndTime(), uint32(ret), uint32(buyType), nil
}

func (au *AuctionApp) DoBuyItem(auctionItemUUID uint64, playerGBID uint64, errno uint32, price uint64, extra string, service *GameServerService) (*AuctionItem, string, error) {
	appLog.Debugw("DoBuyItem", "auctionItemUUID", auctionItemUUID, "playerGBID", playerGBID, "errno", errno, "price", price, "extra", extra)
	isOK := true
	if errno != AUCTION_OK {
		isOK = false
	}

	var m map[string]interface{}
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("DoBuyItem: Decode err", "err", err)
		return nil, extra, err
	}

	itemLock, err := m["selectItemLocked"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("DoBuyItem: selectItemLocked err", "err", err)
		return nil, extra, err
	}

	auctionItem, err := au.auctionMgr.GetAuctionItem(auctionItemUUID)
	if err != nil {
		appLog.Errorw("DoBuyItem: GetAuctionItem err", "err", err)
		return auctionItem, extra, err
	}

	if auctionItem.LockPlayerGBID > 0 && uint64(itemLock) != auctionItem.LockPlayerGBID {
		appLog.Errorw("DoBuyItem: m_auctionItemLocked != auctionItem.LockPlayerGBID", "itemLock", itemLock, "auctionItem.LockPlayerGBID", auctionItem.LockPlayerGBID)
		return auctionItem, extra, errors.New("DoBuyItem: m_auctionItemLocked != auctionItem.LockPlayerGBID")
	}

	m["isOK"] = isOK
	if !isOK {
		auctionItem.unLock()
		m["errno"] = errno
		extraB, err := json.Marshal(m)
		if err != nil {
			appLog.Errorw("DoBuyItem: Marshal err", "err", err)
			return auctionItem, extra, err
		}
		return auctionItem, string(extraB), nil
	}
	auctionBuyItemNum, err := m["auctionBuyItemNum"].(json.Number).Int64()
	if err != nil {
		auctionItem.unLock()
		appLog.Errorw("DoBuyItem: auctionBuyItemNum err", "err", err)
		return auctionItem, extra, err
	}

	buyNum := uint32(auctionBuyItemNum)
	_, err = au.auctionMgr.doBuyItem(auctionItem, buyNum, playerGBID, m)
	auctionItem.unLock()
	if err != nil {
		appLog.Errorw("DoBuyItem: doBuyItem err", "err", err)
		extraB, err := json.Marshal(m)
		if err != nil {
			appLog.Errorw("DoBuyItem: Marshal err", "err", err)
			return auctionItem, extra, err
		}
		return auctionItem, string(extraB), err
	}

	if auctionItem.FromPlayerGBID != 0 {
		gameServer := au.GetGameServer(auctionItem.ServerId, 0)
		if gameServer == nil {
			appLog.Errorw("DoBuyItem: gameServer == nil", "auctionItem", auctionItem, "playerGBID", playerGBID, "errno", errno, "price", price, "extra", extra)
		} else {
			au.RefreshPlayerCoinAuctionData(auctionItem.FromPlayerGBID, gameServer.AuctionService.(*GameServerService))
		}
	}
	au.auctionMgr.priceRecord.AddAvgPriceRecord(auctionItem.ItemData.ItemId, auctionItem.Price, buyNum, au)
	au.auctionMgr.priceRecord.AddLastPriceRecord(auctionItem.ItemData.ItemId, auctionItem.getEachPrice(), au.db)
	extraB, err := json.Marshal(m)
	if err != nil {
		appLog.Errorw("DoBuyItem: Marshal err", "err", err)
		return auctionItem, extra, err
	}
	return auctionItem, string(extraB), nil
}

func (au *AuctionApp) onItemBeSaled(auctionItem *AuctionItem, buyNumber uint32, extra string, fromPlayerGBID uint64) {
	appLog.Debugw("onItemBeSaled", "auctionItem", auctionItem, "buyNumber", buyNumber, "extra", extra, "fromPlayerGBID", fromPlayerGBID)
	gameServer := au.GetGameServer(auctionItem.ServerId, 0)
	if gameServer == nil {
		appLog.Errorw("onItemBeSaled: gameServer == nil", "auctionItem", auctionItem, "buyNumber", buyNumber, "extra", extra, "fromPlayerGBID", fromPlayerGBID)
		return
	}

	_, err := gameServer.AuctionService.(*GameServerService).OnItemBeSaled(fromPlayerGBID, auctionItem, buyNumber, extra)
	if err != nil {
		appLog.Errorw("onItemBeSaled: OnItemBeSaled err", "err", err, "auctionItem", auctionItem, "buyNumber", buyNumber, "extra", extra, "fromPlayerGBID", fromPlayerGBID)
		return
	}
}

func (au *AuctionApp) getAllServerIds() []uint32 {
	au.serversMutex.RLock()
	defer au.serversMutex.RUnlock()
	serverIds := make([]uint32, 0)
	for serverId, _ := range au.gameServers {
		serverIds = append(serverIds, serverId)
	}
	return serverIds
}

func (au *AuctionApp) broadcastOnItemSaling(auctionUUID uint64, itemID uint32, gbId uint64) {
	au.serversMutex.RLock()
	defer au.serversMutex.RUnlock()
	allServerIds := au.getAllServerIds()
	for _, serverId := range allServerIds {
		gameServer := au.GetGameServer(serverId, 0)
		if nil != gameServer {
			gameServer.AuctionService.(*GameServerService).OnItemSaling(auctionUUID, itemID, gbId)
		}
	}
}

func (au *AuctionApp) CancelSaleItem(playerGBID uint64, auctionItemUUID uint64, extra string) (*AuctionItem, string, uint32, error) {
	var m map[string]interface{}
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("CancelSaleItem: Decode err", "err", err)
		return nil, extra, PARAM_ERROR, err
	}

	auctionItem, ret := au.auctionMgr.CheckCancelSaleItem(auctionItemUUID, playerGBID)
	if ret != AUCTION_OK {
		m["auctionItemUUID"] = auctionItemUUID
		appLog.Warnw("CancelSaleItem failed", "ret", ret, "auctionItemUUID", auctionItemUUID)
		extraB, er := json.Marshal(m)
		if er != nil {
			appLog.Errorw("CancelSaleItem: Marshal err", "err", err)
			return auctionItem, extra, ret, err
		}
		return auctionItem, string(extraB), ret, nil
	}

	if !auctionItem.lock(60, playerGBID, au, true) {
		m["auctionItemUUID"] = auctionItemUUID
		appLog.Warnw("CancelSaleItem lock failed", "ret", ret, "auctionItemUUID", auctionItemUUID)
		extraB, er := json.Marshal(m)
		if er != nil {
			appLog.Errorw("CancelSaleItem: Marshal err", "err", err)
			return auctionItem, extra, AUCTION_ITEM_IS_LOCKED, err
		}
		return auctionItem, string(extraB), AUCTION_ITEM_IS_LOCKED, nil
	}

	extraB, er := json.Marshal(m)
	if er != nil {
		appLog.Errorw("CancelSaleItem: Marshal err", "err", err)
		return auctionItem, extra, ret, err
	}

	return auctionItem, string(extraB), ret, nil
}

func (au *AuctionApp) DoCancelSaleItem(auctionItemUUID uint64, playerGBID uint64, extra string, service *GameServerService) (*AuctionItem, string, uint32) {
	auctionItem, errno := au.auctionMgr.doCancelSaleItemCheck(auctionItemUUID, playerGBID)
	if errno == AUCTION_OK {
		err := au.auctionMgr.doCancelSaleItem(auctionItem)
		if err != nil {
			appLog.Errorw("DoCancelSaleItem: doCancelSaleItem err", "err", err, "auctionItemUUID", auctionItemUUID, "playerGBID", playerGBID, "extra", extra)
			if auctionItem != nil {
				auctionItem.unLock()
			}
			return nil, extra, PARAM_ERROR
		}
		if auctionItem != nil {
			auctionItem.unLock()
		}
		au.RefreshPlayerCoinAuctionData(playerGBID, service)
	} else {
		if auctionItem != nil {
			auctionItem.unLock()
			auctionItem.IsNeedRemove = false
			if auctionItem.Status == AUCTION_STATUS_PUBLICITY {
				au.auctionMgr.addAuctionItemToPublicityIndex(INDEX_KEY_ITEMID, auctionItem.getIndexVal(INDEX_KEY_ITEMID), auctionItem)

			} else {
				au.auctionMgr.addAuctionItemToIndex(INDEX_KEY_ITEMID, auctionItem.getIndexVal(INDEX_KEY_ITEMID), auctionItem)
			}
		}
	}

	return auctionItem, extra, errno
}

func (au *AuctionApp) SearchItemsByItemId(playerGBID uint64, itemIds []uint32, limit uint32, offset uint32, isPublicity uint32, extra string) ([]*AuctionItem, uint32, error) {
	auctionItems, allCount := au.auctionMgr.SearchItemByItemIds(itemIds, playerGBID, limit, offset, isPublicity)
	appLog.Debugw("SearchItemsByItemId", "auctionItems", auctionItems, "allCount", allCount)
	return auctionItems, allCount, nil
}

func (au *AuctionApp) GetCurrentSaleItemInfo(itemId uint32, playerGBID uint64, isPublicity uint32) ([]*AuctionItem, uint32, error) {
	appLog.Debugw("GetCurrentSaleItemInfo", "playerGBID", playerGBID, "itemId", itemId, "isPublicity", isPublicity)
	itemIds := []uint32{itemId}
	auctionItems, allCount := au.auctionMgr.SearchItemByItemIds(itemIds, playerGBID, 3, 0, isPublicity)
	appLog.Debugw("GetCurrentSaleItemInfo 2", "auctionItems", auctionItems, "allCount", allCount)
	return auctionItems, allCount, nil
}

func (au *AuctionApp) GetItemLastPrice(itemId uint32) (float32, error) {
	lastPrice := au.auctionMgr.GetItemLastPrice(itemId)
	return lastPrice, nil
}

func (au *AuctionApp) GetItemAvgPrice(itemId uint32) (float32, error) {
	avgPrice := au.auctionMgr.GetItemAvgPrice(itemId)
	return avgPrice, nil
}

func (au *AuctionApp) GetPlayerAuctionItems(playerGBID uint64) []*AuctionItem {
	auctionItems := au.auctionMgr.GetPlayerAuctionItemsByPlayerGBID(playerGBID)
	return auctionItems
}

func (au *AuctionApp) LoadPlayerAuctionItem(playerGBID uint64, extra string) ([]uint64, string, error) {
	auctionItemUUIDs := au.auctionMgr.LoadPlayerAuctionItemUUIDs(playerGBID)

	return auctionItemUUIDs, extra, nil
}

func (au *AuctionApp) RefreshPlayerCoinAuctionData(playerGBID uint64, service *GameServerService) {
	if playerGBID == 0 {
		return
	}

	if service == nil {
		return
	}

	auctionItemUUIDs := au.auctionMgr.LoadPlayerAuctionItemUUIDs(playerGBID)

	_, err := service.RefreshPlayerCoinAuctionData(playerGBID, auctionItemUUIDs, "{}")
	if err != nil {
		return
	}
}

func (au *AuctionApp) DoCommand(command string, extra string) (string, error) {
	switch command {
	case "gmGetAuctionItemPriceInfo":
		return au.gmGetAuctionItemPriceInfo(extra)
	case "gmSaleAuctionItem":
		return au.gmSaleAuctionItem(extra)
	case "gmCancelSaleAuctionItem":
		return au.gmCancelSaleAuctionItem(extra)
	case "gmCancelSaleAuctionItemByPlayerGbId":
		return au.gmCancelSaleAuctionItemByPlayerGbId(extra)
	case "gmSetAuctionItemRecommendPrice":
		return au.gmSetAuctionItemRecommendPrice(extra)
	case "gmGetAuctionItemNumByItemId":
		return au.gmGetAuctionItemNumByItemId(extra)
	case "gmEndSaleAuctionItem":
		return au.gmEndSaleAuctionItem(extra)
	case "gmBuyAuctionItem":
		return au.gmBuyAuctionItem(extra)
	case "gmEndBuyAuctionItem":
		return au.gmEndBuyAuctionItem(extra)
	case "gmAddAuctionBlackList":
		return au.gmAddAuctionBlackList(extra)
	case "gmRemoveAuctionBlackList":
		return au.gmRemoveAuctionBlackList(extra)
	case "gmSetInterception":
		return au.gmSetInterception(extra)
	default:
		return "", errors.New("DoCommand: command not found")
	}
}

func (au *AuctionApp) gmGetAuctionItemPriceInfo(extra string) (string, error) {
	appLog.Infow("gmGetAuctionItemPriceInfo", "extra", extra)
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmGetAuctionItemPriceInfo: Decode err", "err", err)
		return "执行失败", err
	}
	itemId, err := m["itemId"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmGetAuctionItemPriceInfo: parse err", "err", err)
		return "执行失败", err
	}

	var minPrice uint64 = 0
	var maxPrice uint64 = 0
	var avgPrice uint64 = 0
	var recommendPrice float32 = 0
	var totalPrice uint64 = 0
	var itemNum uint32 = 0

	curTime := time.Now().Unix()
	lockedBtree := au.auctionMgr.getAuctionItemIndex(INDEX_KEY_ITEMID, strconv.FormatUint(uint64(itemId), 10))
	if lockedBtree == nil {
		return "执行成功", nil
	}
	lockedBtree.mu.RLock()
	defer lockedBtree.mu.RUnlock()
	lockedBtree.tree.Ascend(func(auctionItem *AuctionItem) bool {
		if auctionItem.Status != AUCTION_STATUS_SELLING {
			return true
		}

		if auctionItem.isItemExpired(curTime) {
			return true
		}

		totalPrice += auctionItem.Price * uint64(auctionItem.Number)
		itemNum += auctionItem.Number

		if auctionItem.Price < minPrice || minPrice == 0 {
			minPrice = auctionItem.Price
		}

		if auctionItem.Price > maxPrice {
			maxPrice = auctionItem.Price
		}

		return true
	})

	recommendPrice = au.auctionMgr.GetItemLastPrice(uint32(itemId))
	if itemNum > 0 {
		avgPrice = totalPrice / uint64(itemNum)
	}
	appLog.Infow("gmGetAuctionItemPriceInfo", "minPrice", minPrice, "maxPrice", maxPrice, "avgPrice", avgPrice, "recommendPrice", recommendPrice, "totalPrice", totalPrice, "itemNum", itemNum)

	extraMap := make(map[string]interface{})
	extraMap["minPrice"] = minPrice
	extraMap["maxPrice"] = maxPrice
	extraMap["avgPrice"] = avgPrice
	extraMap["recommendPrice"] = recommendPrice
	extraMap["totalPrice"] = totalPrice
	extraMap["itemNum"] = itemNum
	extraB, err := json.Marshal(extraMap)
	if err != nil {
		appLog.Errorw("gmGetAuctionItemPriceInfo: Marshal err", "err", err)
		return "", err
	}

	return string(extraB), nil
}

func (au *AuctionApp) gmSaleAuctionItem(extra string) (string, error) {
	appLog.Infow("gmSaleAuctionItem", "extra", extra)
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmSaleAuctionItem: Decode err", "err", err)
		return "执行失败", err
	}
	itemId, err := m["itemId"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmSaleAuctionItem: parse err", "err", err)
		return "执行失败", err
	}
	itemNum, err := m["itemNum"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmSaleAuctionItem: parse err", "err", err)
		return "执行失败", err
	}
	price, err := m["price"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmSaleAuctionItem: parse err", "err", err)
		return "执行失败", err
	}
	num, err := m["num"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmSaleAuctionItem: parse err", "err", err)
		return "执行失败", err
	}
	interval, err := m["interval"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmSaleAuctionItem: parse err", "err", err)
		return "执行失败", err
	}

	startTime, err := m["startTime"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmSaleAuctionItem: parse err", "err", err)
		return "执行失败", err
	}

	endTime, err := m["endTime"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmSaleAuctionItem: parse err", "err", err)
		return "执行失败", err
	}

	now := time.Now().Unix()
	duration := time.Duration(interval) * time.Second
	if now >= startTime {
		_, err := au.auctionMgr.gmSaleAuctionItem(uint32(itemId), uint32(itemNum), uint64(price), uint32(num), uint32(startTime), uint32(endTime))
		if err != nil {
			appLog.Errorw("gmSaleAuctionItem: gmSaleAuctionItem err", "err", err)
			return "执行失败", err
		}
	} else {
		duration = time.Duration(startTime-now) * time.Second
	}

	//au.auctionMgr.cancelGmTimer("gmSaleAuctionItem")
	ticker := time.NewTicker(duration)
	stopCh := make(chan struct{}, 1)
	au.auctionMgr.setGmTimer("gmSaleAuctionItem", stopCh)
	go func() {
		for {
			select {
			case <-ticker.C:
				_, err := au.auctionMgr.gmSaleAuctionItem(uint32(itemId), uint32(itemNum), uint64(price), uint32(num), uint32(startTime), uint32(endTime))
				if err != nil {
					appLog.Errorw("gmSaleAuctionItem: gmSaleAuctionItem err", "err", err)
					return
				}

				if time.Now().Unix() >= endTime && endTime != 0 {
					return
				}
				ticker.Reset(time.Second * time.Duration(interval))
			case <-stopCh:
				return
			}
		}
	}()

	return "执行成功", nil

}

func (au *AuctionApp) gmCancelSaleAuctionItem(extra string) (string, error) {
	appLog.Infow("gmCancelSaleAuctionItem", "extra", extra)
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmCancelSaleAuctionItem: Decode err", "err", err)
		return "执行失败", err
	}
	itemId, err := m["itemId"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmCancelSaleAuctionItem: parse err", "err", err)
		return "执行失败", err
	}

	minPrice, err := m["minPrice"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmCancelSaleAuctionItem: parse err", "err", err)
		return "执行失败", err
	}

	maxPrice, err := m["maxPrice"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmCancelSaleAuctionItem: parse err", "err", err)
		return "执行失败", err
	}

	lockedBtree := au.auctionMgr.getAuctionItemIndex(INDEX_KEY_ITEMID, strconv.FormatUint(uint64(itemId), 10))
	if lockedBtree == nil {
		return "执行成功", nil
	}
	lockedBtree.mu.RLock()
	defer lockedBtree.mu.RUnlock()
	lockedBtree.tree.Ascend(func(auctionItem *AuctionItem) bool {
		if auctionItem.Status != AUCTION_STATUS_SELLING {
			return true
		}

		if auctionItem.Price <= uint64(minPrice) || auctionItem.Price >= uint64(maxPrice) {
			if auctionItem.FromPlayerGBID == 0 {
				au.DoCancelSaleItem(auctionItem.AuctionItemUUID, 0, "", nil)
			} else {
				au.auctionMgr.setItemExpired(auctionItem.AuctionItemUUID)
			}
		}
		return true
	})

	return "执行成功", nil
}

func (au *AuctionApp) gmCancelSaleAuctionItemByPlayerGbId(extra string) (string, error) {
	appLog.Infow("gmCancelSaleAuctionItemByPlayerGbId", "extra", extra)
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmCancelSaleAuctionItemByPlayerGbId: Decode err", "err", err)
		return "执行失败", err
	}
	playerGbId, err := m["playerGbID"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmCancelSaleAuctionItemByPlayerGbId: parse err", "err", err)
		return "执行失败", err
	}

	itemId, err := m["itemId"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmCancelSaleAuctionItemByPlayerGbId: parse err", "err", err)
		return "执行失败", err
	}

	lockedBtree := au.auctionMgr.getAuctionItemIndex(INDEX_KEY_PLAYERGBID, strconv.FormatUint(uint64(playerGbId), 10))
	if lockedBtree == nil {
		return "执行成功", nil
	}
	lockedBtree.mu.RLock()
	defer lockedBtree.mu.RUnlock()
	lockedBtree.tree.Ascend(func(auctionItem *AuctionItem) bool {
		if auctionItem.ItemData.ItemId != uint32(itemId) {
			return true
		}

		if auctionItem.Status != AUCTION_STATUS_SELLING {
			return true
		}

		if auctionItem.FromPlayerGBID == 0 {
			au.DoCancelSaleItem(auctionItem.AuctionItemUUID, 0, "", nil)
		} else {
			au.auctionMgr.setItemExpired(auctionItem.AuctionItemUUID)
		}
		return true
	})

	return "执行成功", nil
}

func (au *AuctionApp) gmSetAuctionItemRecommendPrice(extra string) (string, error) {
	appLog.Infow("gmSetAuctionItemRecommendPrice", "extra", extra)
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmSetAuctionItemRecommendPrice: Decode err", "err", err)
		return "执行失败", err
	}
	itemId, err := m["itemId"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmSetAuctionItemRecommendPrice: parse itemId err", "err", err)
		return "执行失败", err
	}

	price, err := m["price"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmSetAuctionItemRecommendPrice: parse price err", "err", err)
		return "执行失败", err
	}

	setTime, err := m["setTime"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmSetAuctionItemRecommendPrice: parse setTime err", "err", err)
		return "执行失败", err
	}

	curTime := time.Now().Unix()
	if setTime <= curTime {
		au.auctionMgr.priceRecord.AddLastPriceRecord(uint32(itemId), float32(price), au.db)
	} else {
		duration := setTime - curTime
		timer := time.NewTimer(time.Duration(duration) * time.Second)

		go func(t *time.Timer) {
			for {
				<-t.C
				au.auctionMgr.priceRecord.AddLastPriceRecord(uint32(itemId), float32(price), au.db)
			}
		}(timer)
	}

	return "执行成功", nil
}

func (au *AuctionApp) gmGetAuctionItemNumByItemId(extra string) (string, error) {
	appLog.Infow("gmGetAuctionItemNumByItemId", "extra", extra)
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmGetAuctionItemNumByItemId: Decode err", "err", err)
		return "执行失败", err
	}
	itemId, err := m["itemId"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmGetAuctionItemNumByItemId: parse itemId err", "err", err)
		return "执行失败", err
	}

	var num uint32 = 0
	lockedBtree := au.auctionMgr.getAuctionItemIndex(INDEX_KEY_ITEMID, strconv.FormatUint(uint64(itemId), 10))
	if lockedBtree == nil {
		return "执行成功", nil
	}
	lockedBtree.mu.RLock()
	defer lockedBtree.mu.RUnlock()
	lockedBtree.tree.Ascend(func(auctionItem *AuctionItem) bool {
		if auctionItem.Status != AUCTION_STATUS_SELLING {
			return true
		}

		num += auctionItem.Number
		return true
	})

	appLog.Infow("gmGetAuctionItemNumByItemId", "itemId", itemId, "num", num)
	return "执行成功", nil
}

func (au *AuctionApp) gmEndSaleAuctionItem(extra string) (string, error) {
	appLog.Infow("gmEndSaleAuctionItem", "extra", extra)
	au.auctionMgr.cancelGmTimer("gmEndSaleAuctionItem")
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmEndSaleAuctionItem: Decode err", "err", err)
		return "执行失败", err
	}

	endTime, err := m["endTime"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmEndSaleAuctionItem: parse endTime err", "err", err)
		return "执行失败", err
	}

	curTime := time.Now().Unix()
	if endTime <= curTime {
		au.auctionMgr.cancelGmTimer("gmSaleAuctionItem")
	} else {
		duration := endTime - curTime
		timer := time.NewTimer(time.Duration(duration) * time.Second)
		au.auctionMgr.setGmTimer("gmEndSaleAuctionItem", timer)
		go func(t *time.Timer) {
			for {
				<-t.C
				au.auctionMgr.cancelGmTimer("gmSaleAuctionItem")
				au.auctionMgr.cancelGmTimer("gmEndSaleAuctionItem")
			}
		}(timer)
	}

	return "执行成功", nil
}

func (au *AuctionApp) gmBuyAuctionItem(extra string) (string, error) {
	appLog.Infow("gmBuyAuctionItem", "extra", extra)
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmBuyAuctionItem: Decode err", "err", err)
		return "执行失败", err
	}

	itemId, err := m["itemId"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmBuyAuctionItem: parse itemId err", "err", err)
		return "执行失败", err
	}

	itemNum, err := m["itemNum"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmBuyAuctionItem: parse itemNum err", "err", err)
		return "执行失败", err
	}

	price, err := m["price"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmBuyAuctionItem: parse price err", "err", err)
		return "执行失败", err
	}

	interval, err := m["interval"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmBuyAuctionItem: parse interval err", "err", err)
		return "执行失败", err
	}

	startTime, err := m["startTime"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmBuyAuctionItem: parse startTime err", "err", err)
		return "执行失败", err
	}

	allNum, err := m["allNum"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmBuyAuctionItem: parse allNum err", "err", err)
		return "执行失败", err
	}
	au.gmAllBuyNum = uint64(allNum)
	au.gmCurBuyNum = 0

	now := time.Now().Unix()
	duration := time.Duration(interval) * time.Second
	if now >= startTime {
		remainBuyNum := au.gmAllBuyNum - au.gmCurBuyNum
		if remainBuyNum > 0 {
			if uint64(itemNum) > remainBuyNum {
				itemNum = int64(remainBuyNum)
			}
		}
		_, realBuyNum, err := au.auctionMgr.gmBuyAuctionItem(uint32(itemId), uint32(itemNum), uint64(price), uint32(startTime))
		if err != nil {
			appLog.Errorw("gmBuyAuctionItem: gmBuyAuctionItem err", "err", err)
			return "执行失败", err
		}
		au.gmCurBuyNum += uint64(realBuyNum)
	} else {
		duration = time.Duration(startTime-now) * time.Second
	}

	au.auctionMgr.cancelGmTimer("gmBuyAuctionItem")
	ticker := time.NewTicker(duration)
	stopCh := make(chan struct{}, 1)
	au.auctionMgr.setGmTimer("gmBuyAuctionItem", stopCh)
	go func() {
		for {
			select {
			case <-ticker.C:
				remainBuyNum := au.gmAllBuyNum - au.gmCurBuyNum
				if remainBuyNum <= 0 {
					return
				}
				if uint64(itemNum) > remainBuyNum {
					itemNum = int64(remainBuyNum)
				}
				_, realBuyNum, err := au.auctionMgr.gmBuyAuctionItem(uint32(itemId), uint32(itemNum), uint64(price), uint32(startTime))
				if err != nil {
					appLog.Warnw("gmBuyAuctionItem: gmBuyAuctionItem err", "err", err)
				} else {
					au.gmCurBuyNum += uint64(realBuyNum)
				}
				ticker.Reset(time.Second * time.Duration(interval))
			case <-stopCh:
				return
			}
		}
	}()

	return "执行成功", nil
}

func (au *AuctionApp) gmEndBuyAuctionItem(extra string) (string, error) {
	appLog.Infow("gmEndBuyAuctionItem", "extra", extra)
	au.auctionMgr.cancelGmTimer("gmEndBuyAuctionItem")
	au.gmAllBuyNum = 0
	au.gmCurBuyNum = 0
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmEndBuyAuctionItem: Decode err", "err", err)
		return "执行失败", err
	}

	endTime, err := m["endTime"].(json.Number).Int64()
	if err != nil {
		appLog.Errorw("gmEndBuyAuctionItem: parse endTime err", "err", err)
		return "执行失败", err
	}

	curTime := time.Now().Unix()
	if endTime <= curTime {
		au.auctionMgr.cancelGmTimer("gmBuyAuctionItem")
	} else {
		duration := endTime - curTime
		timer := time.NewTimer(time.Duration(duration) * time.Second)
		au.auctionMgr.setGmTimer("gmEndBuyAuctionItem", timer)
		go func(t *time.Timer) {
			for {
				<-t.C
				au.auctionMgr.cancelGmTimer("gmBuyAuctionItem")
				au.auctionMgr.cancelGmTimer("gmEndBuyAuctionItem")
			}
		}(timer)
	}

	return "执行成功", nil
}

func (au *AuctionApp) getAuctionItemNumByCategoryId(itemIds []uint32, isPublicity int32) ([]uint32, []uint32, []float32, error) {
	itemIdArr := make([]uint32, 0)
	itemNumArr := make([]uint32, 0)
	eachPriceArr := make([]float32, 0)

	num := uint32(0)
	eachPrice := float32(0)
	for _, itemId := range itemIds {
		if isPublicity == 1 {
			num = au.auctionMgr.getAuctionItemPublicityIndexNum(INDEX_KEY_ITEMID, strconv.FormatUint(uint64(itemId), 10))
		} else {
			num = au.auctionMgr.getAuctionItemIndexNum(INDEX_KEY_ITEMID, strconv.FormatUint(uint64(itemId), 10))
		}
		if num == 0 {
			continue
		}
		if isPublicity == 1 {
			eachPrice = au.auctionMgr.GetLowestPricePublicityItem(INDEX_KEY_ITEMID, strconv.FormatUint(uint64(itemId), 10))
		} else {
			eachPrice = au.auctionMgr.GetLowestPriceItem(INDEX_KEY_ITEMID, strconv.FormatUint(uint64(itemId), 10))
		}

		if eachPrice == 0 {
			appLog.Errorw("getAuctionItemNumByCategoryId: get lowest price err", "itemId", itemId)
			continue
		}

		itemIdArr = append(itemIdArr, itemId)
		itemNumArr = append(itemNumArr, num)
		eachPriceArr = append(eachPriceArr, eachPrice)
	}
	return itemIdArr, itemNumArr, eachPriceArr, nil
}

func (au *AuctionApp) gmAddAuctionBlackList(extra string) (string, error) {
	appLog.Infow("gmAddAuctionBlackList", "extra", extra)
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmAddAuctionBlackList: Decode err", "err", err)
		return "执行失败", err
	}

	playerGbIds := m["playerGbIds"].(string)
	playerGbIds = strings.Trim(playerGbIds, "()")
	parts := strings.Split(playerGbIds, ",")
	for _, part := range parts {
		playerGbId, err := strconv.ParseUint(part, 10, 64)
		if err != nil {
			appLog.Errorw("gmAddAuctionBlackList: parse playerGbId err", "err", err)
			return "执行失败", err
		}
		au.auctionMgr.addAuctionBlackList(playerGbId)
	}

	return "执行成功", nil
}

func (au *AuctionApp) gmRemoveAuctionBlackList(extra string) (string, error) {
	appLog.Infow("gmRemoveAuctionBlackList", "extra", extra)
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmRemoveAuctionBlackList: Decode err", "err", err)
		return "执行失败", err
	}

	playerGbIds := m["playerGbIds"].(string)
	playerGbIds = strings.Trim(playerGbIds, "()")
	parts := strings.Split(playerGbIds, ",")
	for _, part := range parts {
		playerGbId, err := strconv.ParseUint(part, 10, 64)
		if err != nil {
			appLog.Errorw("gmRemoveAuctionBlackList: parse playerGbId err", "err", err)
			return "执行失败", err
		}
		au.auctionMgr.removeAuctionBlackList(playerGbId)
	}
	return "执行成功", nil
}

func (au *AuctionApp) gmSetInterception(extra string) (string, error) {
	appLog.Infow("gmSetInterception", "extra", extra)
	m := make(map[string]interface{})
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("gmSetInterception: Decode err", "err", err)
		return "执行失败", err
	}

	return "执行成功", nil
}

func (au *AuctionApp) buyItemByItemId(playerGbId uint64, itemId uint32, num uint32, price uint32) ([]uint64, uint32, uint32, error) {
	appLog.Debugw("buyItemByItemId", "playerGbId", playerGbId, "itemId", itemId, "num", num, "price", price)
	auctionItemUUIDS := make([]uint64, 0, num)
	auctionItems := make([]*AuctionItem, 0, num)
	var firstAuctionItem *AuctionItem
	remainNum := num
	totalPrice := uint32(0)
	lockedBtree := au.auctionMgr.getAuctionItemIndex(INDEX_KEY_ITEMID, strconv.FormatUint(uint64(itemId), 10))
	if lockedBtree == nil {
		return auctionItemUUIDS, remainNum, totalPrice, nil
	}
	lockedBtree.mu.Lock()
	defer lockedBtree.mu.Unlock()

	lockedBtree.tree.Ascend(func(auctionItem *AuctionItem) bool {
		if auctionItem.isLocked(0) {
			return true
		}

		if auctionItem.FromPlayerGBID == playerGbId {
			return true
		}

		if auctionItem.Status != AUCTION_STATUS_SELLING {
			return true
		}

		if auctionItem.IsDestroyed {
			return true
		}

		if uint32(auctionItem.Price) > price {
			return false
		}

		getLock := auctionItem.lock(60, playerGbId, au, false)
		if !getLock {
			appLog.Debugw("buyItemByItemId: get lock failed", "auctionItemUUID", auctionItem.AuctionItemUUID)
			return true
		}
		if auctionItem.Number <= remainNum {
			remainNum -= auctionItem.Number
			totalPrice += uint32(auctionItem.Price) * auctionItem.Number
		} else {
			totalPrice += uint32(auctionItem.Price) * remainNum
			remainNum = 0
		}
		if firstAuctionItem == nil {
			firstAuctionItem = auctionItem
		}
		auctionItemUUIDS = append(auctionItemUUIDS, auctionItem.AuctionItemUUID)
		auctionItems = append(auctionItems, auctionItem)

		return remainNum != 0
	})

	if len(auctionItems) != 0 {
		if firstAuctionItem != nil {
			err := au.auctionMgr.removeAuctionItemsFromIndex(INDEX_KEY_ITEMID, firstAuctionItem.getIndexVal(INDEX_KEY_ITEMID), auctionItems)
			if err != nil {
				appLog.Errorw("buyItemByItemId removeAuctionItemsFromIndex error", "err", err)
				return nil, remainNum, totalPrice, err
			}
		}
	}

	return auctionItemUUIDS, remainNum, totalPrice, nil
}

func (au *AuctionApp) doBuyItemByItemId(playerGbId uint64, errno uint32, itemId uint32, num uint32, price uint32, remainNum uint32, auctionItemUUIDs []uint64, totalPrice uint32, extra string) (*ItemData, string, error) {
	appLog.Debugw("doBuyItemByItemId", "playerGbId", playerGbId, "errno", errno, "itemId", itemId, "num", num, "price", price, "remainNum", remainNum, "auctionItemUUIDs", auctionItemUUIDs, "totalPrice", totalPrice, "extra", extra)
	var m map[string]interface{}
	dec := json.NewDecoder(strings.NewReader(extra))
	dec.UseNumber()
	err := dec.Decode(&m)
	if err != nil {
		appLog.Errorw("doBuyItemByItemId: Decode err", "err", err)
		return nil, extra, err
	}

	isOK := true
	if errno != AUCTION_OK {
		isOK = false
	}
	m["isOK"] = isOK
	set := make(map[uint64]*AuctionItem)
	curNum := num
	curTotalPrice := uint32(0)
	var itemData *ItemData
	buyNum := num - remainNum
	for _, auctionItemUUID := range auctionItemUUIDs {
		auctionItem, err := au.auctionMgr.GetAuctionItem(auctionItemUUID)
		if err != nil || auctionItem == nil {
			appLog.Errorw("doBuyItemByItemId: GetAuctionItem err", "err", err)
			return nil, extra, err
		}

		if auctionItem.LockPlayerGBID != playerGbId {
			appLog.Errorw("doBuyItemByItemId: auctionItem.LockPlayerGBID != playerGbId", "auctionItem.LockPlayerGBID", auctionItem.LockPlayerGBID, "playerGbId", playerGbId)
			return nil, extra, errors.New("auctionItem.LockPlayerGBID != playerGbId")
		}

		if curNum == 0 {
			appLog.Errorw("doBuyItemByItemId: curNum == 0")
			return nil, extra, errors.New("curNum == 0")
		}

		if !isOK {
			indexKey := INDEX_KEY_ITEMID
			auctionItem.unLock()
			cacheItem := &CacheItem{
				IndexKey:    indexKey,
				IndexVal:    auctionItem.getIndexVal(indexKey),
				AuctionItem: auctionItem,
				IsInit:      false,
			}
			au.auctionMgr.addCh <- cacheItem
			continue
		} else {
			if itemData == nil {
				itemData = NewItemData(auctionItem.ItemData, buyNum)
			}
			curBuyNum := auctionItem.Number
			if curNum < auctionItem.Number {
				curBuyNum = curNum
			} else {
				set[auctionItem.FromPlayerGBID] = auctionItem
			}
			curNum -= curBuyNum
			_, err = au.auctionMgr.doBuyItem(auctionItem, curBuyNum, playerGbId, m)
			if err != nil {
				appLog.Errorw("doBuyItemByItemId: doBuyItem err", "err", err)
				return nil, extra, err
			}
			curTotalPrice += uint32(auctionItem.Price) * curBuyNum
			au.auctionMgr.priceRecord.AddAvgPriceRecord(itemId, auctionItem.Price, curBuyNum, au)
		}
	}

	if !isOK {
		return nil, extra, nil
	}

	if curNum != remainNum {
		appLog.Errorw("doBuyItemByItemId: curNum != remainNum", "curNum", curNum, "remainNum", remainNum)
		return nil, extra, errors.New("doBuyItemByItemId: curNum != remainNum")
	}
	if curTotalPrice != totalPrice {
		appLog.Errorw("doBuyItemByItemId: curTotalPrice != totalPrice", "curTotalPrice", curTotalPrice, "totalPrice", totalPrice)
		return nil, extra, errors.New("doBuyItemByItemId: curTotalPrice != totalPrice")
	}

	for _, auctionItem := range set {
		if auctionItem.FromPlayerGBID != 0 {
			gameServer := au.GetGameServer(auctionItem.ServerId, 0)
			if gameServer == nil {
				appLog.Errorw("doBuyItemByItemId: gameServer == nil", "auctionItem.AuctionItemUUID", auctionItem.AuctionItemUUID, "auctionItem.FromPlayerGBID", auctionItem.FromPlayerGBID, "errno", errno, "price", price)
			} else {
				au.RefreshPlayerCoinAuctionData(auctionItem.FromPlayerGBID, gameServer.AuctionService.(*GameServerService))
			}
		}
	}

	extraB, err := json.Marshal(m)
	if err != nil {
		appLog.Errorw("doBuyItemByItemId: Marshal err", "err", err)
		return nil, extra, err
	}

	return itemData, string(extraB), nil
}

func (au *AuctionApp) getAuctionItemsByAuctionIds(auctionIds []uint64) ([]*AuctionItem, error) {
	auctionItems := make([]*AuctionItem, 0)
	for _, autionId := range auctionIds {
		auctionItem, ok := au.auctionMgr.auctionItems.Get(strconv.FormatUint(autionId, 10))
		if !ok {
			continue
		}
		auctionItems = append(auctionItems, auctionItem)
	}
	return auctionItems, nil
}
