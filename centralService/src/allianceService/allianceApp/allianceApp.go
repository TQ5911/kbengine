package allianceApp

import (
	"centralService/src/allianceService/allianceApp/gameServerService"
	"centralService/src/appLog"
	"centralService/src/common"
	"centralService/src/trpc"
	"database/sql"
	"fmt"
	"net"
	"sync"
	"syscall"
	"time"

	_ "github.com/go-sql-driver/mysql"
	"github.com/google/uuid"
)

var AllianceConfig = AppConfig{}

var AllianceBizConstCfg = BizConstCfg{}

const (
	SERVICE_ALLIANCE = iota + 1
)

type AllianceApp struct {
	common.App
	db            *sql.DB
	serversLock   sync.RWMutex
	gameServers   map[string]*GameServerService
	channelToHost map[uuid.UUID]*GameServerService
	allianceData  *AllianceData
}

func (app *AllianceApp) GetName() string {
	return app.AppName
}

func (app *AllianceApp) GetServices() []*common.ServiceInfo {
	return []*common.ServiceInfo{
		{
			ServiceType:       SERVICE_ALLIANCE,
			ServiceName:       app.AppName,
			ServiceListenAddr: AllianceConfig.AllianceServiceAddr,
		},
	}
}

func (app *AllianceApp) NewService(conn net.Conn, serviceType uint8) trpc.IServerEndPoint {
	var service trpc.IServerEndPoint = nil
	if serviceType == SERVICE_ALLIANCE {
		rpcUUID := uuid.New()
		channel := trpc.NewRpcChannel(rpcUUID, conn)
		service = &GameServerService{
			ServerEndPoint: gameServerService.NewAllianceServiceService(gameServerService.NewGameClientClient(channel)),
			app:            app,
		}
		channel.SetEndPoint(service)
	}
	return service
}

func (app *AllianceApp) Start() {
	appLog.Info("alliance app start", app)
	app.App.Start()

	app.RegisterSignals(syscall.SIGINT, syscall.SIGKILL, syscall.SIGTERM)
	go func() {
		<-app.SignalChan
		app.Stop()
	}()

	go func() {
		timer := time.NewTicker(time.Second * 1)
		for {
			<-timer.C
			app.tick()
		}
	}()

	go app.StartDebugService(AllianceConfig.AddressForDebug)
}

func (app *AllianceApp) tick() {
	app.allianceData.checkAndRemoveExpiredWars(app.db, app)
}

func (app *AllianceApp) Stop() {
	appLog.Info("alliance app stop")
}

func (app *AllianceApp) addGameServer(service *GameServerService) {
	app.serversLock.Lock()
	defer app.serversLock.Unlock()

	serviceKey := app.getServiceKey(service.serverId)
	app.gameServers[serviceKey] = service
	app.channelToHost[service.GetRpcChannel().ChannelUUID] = service
}

func (app *AllianceApp) doRemoveGameServer(service *GameServerService) {
	app.serversLock.Lock()
	defer app.serversLock.Unlock()

	serviceKey := app.getServiceKey(service.serverId)
	delete(app.gameServers, serviceKey)
	delete(app.channelToHost, service.GetRpcChannel().ChannelUUID)
}
func (app *AllianceApp) removeGameServer(service *GameServerService) {
	app.doRemoveGameServer(service)
	// Fail any pending ApproveJoin that was waiting on a guild-existence
	// check from this (now-disconnected) source server.
	app.allianceData.pendingApproveJoins.Range(func(key, value interface{}) bool {
		p := value.(*pendingApproveJoin)
		if p.applyInfo.ServerId == service.serverId {
			app.allianceData.pendingApproveJoins.Delete(key)
			if leaderGS := app.getGameServer(p.leaderServerId); leaderGS != nil {
				leaderGS.getClient().OnApproveJoinResult(&gameServerService.ApproveJoinResult{
					Uuid:    p.originalUuid,
					ErrCode: ErrCodeGuildSourceServerOffline,
				})
			}
		}
		return true
	})

	// Fail any pending InviteGuild that was waiting on a guild-existence
	// check from this (now-disconnected) target server. The inviter's
	// alliance leader gets OnInviteGuildResult with the offline error.
	app.allianceData.pendingInviteGuilds.Range(func(key, value interface{}) bool {
		p := value.(*pendingInviteGuild)
		if p.targetServerId == service.serverId {
			app.allianceData.pendingInviteGuilds.Delete(key)
			if inviterGS := app.getGameServer(p.inviterLeaderServerId); inviterGS != nil {
				inviterGS.getClient().OnInviteGuildResult(&gameServerService.InviteGuildResult{
					Uuid:    p.originalUuid,
					ErrCode: ErrCodeInviteTargetServerOffline,
				})
			}
		}
		return true
	})

	// Fail any pending DeclareWar that was waiting on a guild-existence
	// check from this (now-disconnected) target server. The attacker's
	// game server gets OnDeclareWarResult with the offline error. (If
	// the disconnected server is the *attacker*'s server, the
	// pending entry is harmless — it'll just fail later in
	// completeDeclareWar if/when the target's server replies.)
	app.allianceData.pendingDeclareWars.Range(func(key, value interface{}) bool {
		pw := value.(*pendingDeclareWar)
		if pw.targetServerId == service.serverId {
			app.allianceData.pendingDeclareWars.Delete(key)
			if attackerGS := app.getGameServer(pw.attackerServerId); attackerGS != nil {
				attackerGS.getClient().OnDeclareWarResult(&gameServerService.DeclareWarResult{
					Uuid:    pw.originalUuid,
					ErrCode: ErrCodeInviteTargetServerOffline,
					EndTime: 0,
				})
			}
		}
		return true
	})
}

func (app *AllianceApp) getServiceKey(serverId uint32) string {
	return fmt.Sprintf("%d", serverId)
}

func NewAllianceApp() *AllianceApp {
	if !InitConfigStore() {
		appLog.Error("init config store error !!!")
		return nil
	}
	for cfgType, cfgPath := range ConfigStore.cfgFiles {
		ret := InitJsonCfg(cfgType, cfgPath)
		if ret != nil {
			appLog.Error("cfg init failed ", ret.Error(), cfgType, cfgPath)
			return nil
		}
	}

	db, err := sql.Open("mysql", fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8",
		AllianceConfig.Mysql.User, AllianceConfig.Mysql.Passwd, AllianceConfig.Mysql.Addr, AllianceConfig.Mysql.Db))

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

	allianceData := NewAllianceData(db)
	app := &AllianceApp{
		App:           common.App{AppName: "AllianceApp"},
		db:            db,
		serversLock:   sync.RWMutex{},
		gameServers:   make(map[string]*GameServerService),
		channelToHost: make(map[uuid.UUID]*GameServerService),
		allianceData:  allianceData,
	}
	allianceData.SetBroadcaster(func(f func(*gameServerService.GameClientClient)) {
		app.BroadcastToGameServers(f)
	})
	return app
}

func (app *AllianceApp) getGameServer(serverId uint32) *GameServerService {
	app.serversLock.RLock()
	defer app.serversLock.RUnlock()

	serviceKey := app.getServiceKey(serverId)
	if gs, ok := app.gameServers[serviceKey]; ok {
		return gs
	}
	return nil
}

func (app *AllianceApp) BroadcastToGameServers(msgFunc func(client *gameServerService.GameClientClient)) {
	app.serversLock.RLock()
	defer app.serversLock.RUnlock()

	for _, server := range app.gameServers {
		client, ok := server.GetClientEndPoint().(*gameServerService.GameClientClient)
		if ok {
			msgFunc(client)
		}
	}
}

func (app *AllianceApp) BroadcastToGameServersExcept(msgFunc func(client *gameServerService.GameClientClient), exceptServerId uint32) {
	app.serversLock.RLock()
	defer app.serversLock.RUnlock()

	for _, server := range app.gameServers {
		if server.serverId == exceptServerId {
			continue
		}
		client, ok := server.GetClientEndPoint().(*gameServerService.GameClientClient)
		if ok {
			msgFunc(client)
		}
	}
}
