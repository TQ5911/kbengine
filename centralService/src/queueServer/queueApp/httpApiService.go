package Queue

import (
	"centralService/src/appLog"
	"centralService/src/common"
	clientService "centralService/src/queueServer/queueApp/clientService"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/garyburd/redigo/redis"
	"github.com/gogf/greuse"
)

type HttpService struct {
	app *QueueApp
}

type QueueReply struct {
	QueueId        uint32         `json:"queueId"`
	State          uint8          `json:"state"`
	ServerId       uint32         `json:"serverId"`
	ServerHost     string         `json:"serverHost"`
	WaitTime       uint64         `json:"waitTime"`
	ServerOpenTime int64          `json:"serverOpenTime"`
	WaitMapServers map[string]int `json:"waitMapServers"`
}

func (self *HttpService) doQueueReply(w http.ResponseWriter, queueId uint32, state uint8, serverId uint32, serverHost string, waitTime uint64,
	serverOpenTime int64,
	waitMapServers map[string]int,
) {
	response := QueueReply{}
	response.QueueId = queueId
	response.State = state
	response.ServerId = serverId
	response.ServerHost = serverHost
	response.WaitTime = waitTime
	response.ServerOpenTime = serverOpenTime
	response.WaitMapServers = waitMapServers
	data, err := json.Marshal(response)
	if err != nil {
		appLog.Error("handleStartQueue json response failed", err.Error())
		w.WriteHeader(405)
		return
	}
	fmt.Fprintf(w, string(data))
}
func (self *HttpService) handleStartQueue(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	var accountNameStr = strings.Join(r.Form["accountName"], "")
	var serverIdStr = strings.Join(r.Form["serverId"], "")
	log.Println("handleStartQueue", accountNameStr, serverIdStr)
	serverId := common.Str2UInt32(serverIdStr)
	serverHost := ServerListCfg.GetString(fmt.Sprintf("serverList.%s", serverIdStr))
	accountName := accountNameStr

	ctx, cancel := context.WithTimeout(context.Background(), common.RedisOpTimeout)
	conn, err := self.app.redisPool.GetContext(ctx)
	cancel()
	if err != nil {
		appLog.Errorf("handleStartQueue get redis conn failed, account=%s server=%s, err=%s", accountNameStr, serverIdStr, err.Error())
		self.doQueueReply(w, 0, uint8(clientService.QueueReply_QUEUE_FAILED), serverId, serverHost, 0, 0, nil)
		return
	}
	defer conn.Close()

	//用户tagType
	userTagTypeSet := map[string]bool{}
	officialTagType, err := redis.String(conn.Do("get", "officialTagType_"+accountNameStr))
	if err == nil {
		tagList := strings.Split(officialTagType, ",")
		for _, tag := range tagList {
			userTagTypeSet[tag] = true
		}
	}
	log.Println("userTagTypeSet", userTagTypeSet)

	//白名单直接放行
	if _, ok := userTagTypeSet["0"]; ok {
		appLog.Info("account is white list, no need queue", accountNameStr, serverId)
		self.doQueueReply(w, 0, uint8(clientService.QueueReply_QUEUE_SUCCESS), serverId, serverHost, 0, 0, nil)
		return
	}

	//开服时间没到返回失败
	openTime, err := redis.String(conn.Do("get", "g:server_open_time"+serverIdStr))
	if err == nil {
		openTimeI64, err := strconv.ParseInt(openTime, 10, 64)
		if err == nil && openTimeI64 > time.Now().Unix() {
			appLog.Info("server not open", accountNameStr, serverId)
			self.doQueueReply(w, 0, uint8(clientService.QueueReply_BEFORE_OPENTIME), serverId, serverHost, 0, openTimeI64-time.Now().Unix(), nil)
			return
		}
	} else {
		appLog.Warn("get server open time failed", accountNameStr, serverId)
	}

	//维护时间
	serverOpenState, err := redis.String(conn.Do("get", "g:server_open_state"+serverIdStr))
	if err == nil {
		appLog.Warn("server maintenance ", serverOpenState, accountNameStr, serverId)
		if serverOpenState == "0" {
			self.doQueueReply(w, 0, uint8(clientService.QueueReply_MAINTENANCE), serverId, serverHost, 0, 0, nil)
			return
		}
	} else {
		appLog.Warn("get server maintenance time failed", accountNameStr, serverId)
	}

	//用户是绿通，免排队
	if _, ok := userTagTypeSet["3"]; ok {
		appLog.Info("account is green code, no need queue", accountNameStr, serverId)
		self.doQueueReply(w, 0, uint8(clientService.QueueReply_QUEUE_SUCCESS), serverId, serverHost, 0, 0, nil)
		return
	}

	//获取在线人数异常
	onlineNum, err := redis.Int(conn.Do("get", "g:normal_online_num"+serverIdStr))
	if err != nil {
		appLog.Warn("handleStartQueue request invalid serverId:\n", serverId, self.app.gameServers, err.Error())
		self.doQueueReply(w, 0, uint8(clientService.QueueReply_QUEUE_FAILED), serverId, serverHost, 0, 0, nil)
		return
	}

	gameServer := self.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Info("handleStartQueue new game server:", serverId)
		gameServer = self.app.NewHttpServerService(serverId)
	}

	accountKey := self.app.buildAccountKey(accountNameStr, strconv.Itoa(int(clientService.AccountType_ACCOUNT_TOKEN)))

	//已经在线
	lastServerId, err := redis.Int(conn.Do("get", "AccountLogin_"+accountKey))
	if err != nil {
		appLog.Info("handleStartQueue account is not online:", accountNameStr, "  err:", err.Error())
	} else {
		if lastServerId == int(serverId) {
			appLog.Info("handleStartQueue account is still online, no need queue", accountNameStr, serverId)
			self.doQueueReply(w, 0, uint8(clientService.QueueReply_QUEUE_SUCCESS), serverId, serverHost, 0, 0, nil)
			return
		}
	}

	hasGetTokenNoUse := false
	if onlineNum < MaxOnlineNum {
		for {
			if gameServer.limiter.Tokens() < 1 {
				break
			}
			if !gameServer.limiter.Allow() {
				break
			}
			hasGetTokenNoUse = true
			noInQueue := false
			for {
				accountNamePtr := self.app.deQueue(gameServer.hostId)
				if accountNamePtr != nil {
					var accountName = string(*accountNamePtr)
					client := self.app.getClient(accountName)
					if client != nil {
						client.isQueueSuc = true
						client._replyQueueSuccess(gameServer.hostId, accountName)
						hasGetTokenNoUse = false
						break
					}
				} else {
					noInQueue = true
					break
				}
			}

			if noInQueue {
				break
			}

		}
	}

	//当前无需排队
	if onlineNum < MaxOnlineNum && (hasGetTokenNoUse || gameServer.limiter.Allow()) {
		appLog.Info("queue success")
		self.doQueueReply(w, 1, uint8(clientService.QueueReply_QUEUE_SUCCESS), serverId, serverHost, 0, 0, nil)
		return
	} else {
		VIPFlag := false
		expireTime, err := redis.String(conn.Do("get", "g:vip:v:"+accountNameStr))
		expireTimeI64, err2 := strconv.ParseInt(expireTime, 10, 64)
		if err == nil && err2 == nil && expireTimeI64 > time.Now().Unix() {
			VIPFlag = true
		}
		appLog.Info("isVIP: ", VIPFlag, " err:", err, " err2:", err2)

		var client = self.app.NewHttpClientService(accountNameStr, serverIdStr)
		self.app.addClient(client)

		client.SetQueueId(self.app.enQueue(serverId, accountName, VIPFlag))

		// 进入排队时返回存活等待服列表（客户端自行选择）
		waitMapServers, _ := self.app.waitMapServerMgr.GetAliveFreeServers()

		self.doQueueReply(w, uint32(client.GetQueueId()), uint8(clientService.QueueReply_QUEUE_IN_PROCESS), serverId, client.GetServerHost(), client.GetWaitTime(), 0, waitMapServers)
	}
}

func (self *HttpService) handleGetQueueInfo(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	var accountNameStr = strings.Join(r.Form["accountName"], "")
	var serverIdStr = strings.Join(r.Form["serverId"], "")
	log.Println("handleGetQueueInfo: ", accountNameStr, serverIdStr)
	serverId := common.Str2UInt32(serverIdStr)
	//accountName := common.Str2UInt64(accountNameStr)
	accountName := accountNameStr

	var client = self.app.getClient(accountNameStr)
	if client == nil {
		appLog.Errorf("handleGetQueueInfo cannot find client: %s\n", accountNameStr)
		w.WriteHeader(400)
		return
	} else {
		client.OnRecv()
		if client.IsQueueSuc() {
			appLog.Info("handleStartQueue queue success ", accountName, " ", serverId)
			response := QueueReply{}
			response.QueueId = uint32(client.GetQueueId())
			response.State = uint8(clientService.QueueReply_QUEUE_SUCCESS)
			response.ServerId = serverId
			response.ServerHost = client.GetServerHost()
			response.WaitTime = 0
			response.WaitMapServers = nil
			data, err := json.Marshal(response)
			if err != nil {
				appLog.Error("handleGetQueueInfo json response failed", err.Error())
				w.WriteHeader(405)
				return
			}
			self.app.removeClient(client)
			fmt.Fprintf(w, string(data))
			return
		} else {
			response := QueueReply{}
			response.QueueId = uint32(client.GetQueueId())
			response.State = uint8(clientService.QueueReply_QUEUE_IN_PROCESS)
			response.ServerId = serverId
			response.ServerHost = client.GetServerHost()
			response.WaitTime = client.GetWaitTime()
			response.WaitMapServers, _ = self.app.waitMapServerMgr.GetAliveFreeServers()
			data, err := json.Marshal(response)
			if err != nil {
				appLog.Error("handleGetQueueInfo json response failed", err.Error())
				w.WriteHeader(405)
				return
			}
			fmt.Fprintf(w, string(data))

			return
		}
	}
}

func (self *HttpService) startHttpServer(listenAddr string) {
	appLog.Info("startHttpServer", listenAddr)

	http.HandleFunc("/startQueue", self.handleStartQueue)
	http.HandleFunc("/getQueueInfo", self.handleGetQueueInfo)

	listener, err := greuse.Listen("tcp", listenAddr)
	if err != nil {
		panic(err)
	}
	defer listener.Close()

	server := &http.Server{}
	panic(server.Serve(listener))
}
