package Queue

import (
	"centralService/src/appLog"
	"centralService/src/common"
	clientService "centralService/src/queueServer/queueApp/clientService"
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
	QueueId    uint32 `json:"queueId"`
	State      uint8  `json:"state"`
	ServerId   uint32 `json:"serverId"`
	ServerHost string `json:"serverHost"`
	WaitTime   uint64 `json:"waitTime"`
}

func (self *HttpService) handleStartQueue(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	var accountNameStr = strings.Join(r.Form["accountName"], "")
	var serverIdStr = strings.Join(r.Form["serverId"], "")
	log.Println("handleStartQueue", accountNameStr, serverIdStr)
	serverId := common.Str2UInt32(serverIdStr)
	accountName := accountNameStr

	conn := self.app.redisPool.Get()
	defer conn.Close()

	onlineNum, err := redis.Int(conn.Do("get", "ServerOnlineNum_"+serverIdStr))
	if err != nil {
		appLog.Warn("handleStartQueue request invalid serverId: %d %+v\n", serverId, self.app.gameServers)
		response := QueueReply{}
		response.QueueId = 0
		response.State = uint8(clientService.QueueReply_QUEUE_FAILED)
		response.ServerId = serverId
		response.ServerHost = ""
		response.WaitTime = 0
		data, err := json.Marshal(response)
		if err != nil {
			appLog.Error("handleStartQueue json response failed", err.Error())
			w.WriteHeader(405)
			return
		}
		fmt.Fprintf(w, string(data))
		return
	}

	gameServer := self.app.getGameServer(serverId)
	if gameServer == nil {
		appLog.Info("handleStartQueue new game server", serverId)
		gameServer = self.app.NewHttpServerService(serverId)
	}

	accountKey := self.app.buildAccountKey(accountNameStr, strconv.Itoa(int(clientService.AccountType_ACCOUNT_TOKEN)))

	lastServerId, err := redis.Int(conn.Do("get", "AccountLogin_"+accountKey))
	if err != nil {
		appLog.Info("handleStartQueue get failed", accountKey, err.Error())
	} else {
		if lastServerId == int(serverId) {
			appLog.Info("handleStartQueue account is still online, no need queue", accountNameStr, serverId)
			serverHost := ServerListCfg.GetString(fmt.Sprintf("serverList.%s", serverIdStr))
			response := QueueReply{}
			response.QueueId = 0
			response.State = uint8(clientService.QueueReply_QUEUE_SUCCESS)
			response.ServerId = serverId
			response.ServerHost = serverHost
			response.WaitTime = 0
			data, err := json.Marshal(response)
			if err != nil {
				appLog.Error("handleStartQueue json response failed", err.Error())
				w.WriteHeader(405)
				return
			}
			fmt.Fprintf(w, string(data))
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

	if onlineNum < MaxOnlineNum && (hasGetTokenNoUse || gameServer.limiter.Allow()) {
		serverHost := ServerListCfg.GetString(fmt.Sprintf("serverList.%s", serverId))
		client := &QueueClientService{
			ServerEndPoint: nil,
			app:            self.app,
			activeTickCnt:  0,
			isReqQueue:     false,
			isValid:        true,
			isQueueSuc:     false,
			serverId:       serverIdStr,
			accountName:    accountName,
			serverHost:     serverHost,
			tLastRecv:      time.Now().Unix(),
		}

		response := QueueReply{}
		response.QueueId = 1
		response.State = uint8(clientService.QueueReply_QUEUE_SUCCESS)
		response.ServerId = serverId
		response.ServerHost = client.GetServerHost()
		response.WaitTime = client.GetWaitTime()
		data, err := json.Marshal(response)
		if err != nil {
			appLog.Error("handleStartQueue json response failed", err.Error())
			w.WriteHeader(405)
			return
		}
		fmt.Fprintf(w, string(data))
	} else {
		var client = self.app.NewHttpClientService(accountNameStr, serverIdStr)
		self.app.addClient(client)

		client.SetQueueId(self.app.enQueue(serverId, accountName))
		response := QueueReply{}
		response.QueueId = uint32(client.GetQueueId())
		response.State = uint8(clientService.QueueReply_QUEUE_IN_PROCESS)
		response.ServerId = serverId
		response.ServerHost = client.GetServerHost()
		response.WaitTime = client.GetWaitTime()
		data, err := json.Marshal(response)
		if err != nil {
			appLog.Error("handleStartQueue json response failed", err.Error())
			w.WriteHeader(405)
			return
		}
		fmt.Fprintf(w, string(data))
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
			appLog.Info("handleStartQueue queue success ", accountName, serverId)
			response := QueueReply{}
			response.QueueId = uint32(client.GetQueueId())
			response.State = uint8(clientService.QueueReply_QUEUE_SUCCESS)
			response.ServerId = serverId
			response.ServerHost = client.GetServerHost()
			response.WaitTime = 0
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
