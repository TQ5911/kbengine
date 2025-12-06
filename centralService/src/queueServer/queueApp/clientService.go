package Queue

import (
	"centralService/src/appLog"
	"centralService/src/common"
	clientService "centralService/src/queueServer/queueApp/clientService"
	"centralService/src/trpc"
	"errors"
	"fmt"
	"log"
	"math"
	"time"
)

// 中心服向客户端提供的接口
type QueueClientService struct {
	*trpc.ServerEndPoint
	app           *QueueApp
	accountName   string
	activeTickCnt int
	isValid       bool
	channelId     uint32
	isReqQueue    bool
	serverId      string
	serverHost    string
	queueId       int
	isQueueSuc    bool
	tLastRecv     int64
}

type PayLoad struct {
	Exp    int64 `json:"exp"`
	UserId int64 `json:"userId"`
	Iat    int64 `json:"iat"`
}

func (self *QueueClientService) startCheckValidTimer() {
	time.AfterFunc(time.Duration(time.Second*30), func() {
		self.checkIsReqQueue()
	})
}

func (self *QueueClientService) checkIsReqQueue() {
	log.Println("checkIsReqQueue", self.isReqQueue)
	if !self.isReqQueue {
		self.GetRpcChannel().Disconnect()
	} else {
		log.Println("request has reqQueue", self.isReqQueue)
	}
}
func (self *QueueClientService) startCheckLastRecvTimer() {
	ticker := time.NewTicker(time.Second * 10)
	defer ticker.Stop()
	for range ticker.C {
		log.Println("checkLastRecv", self.tLastRecv)
		var curTime = time.Now().Unix()
		if curTime-self.tLastRecv > 60 {
			appLog.Warn("checkLastRecv longtime not receive, remove it", self.tLastRecv, curTime)
			self.app.removeClient(self)
			return
		}
	}
}

func (self *QueueClientService) OnLoseConnection() {
	self.app.removeClient(self)
}

func (self *QueueClientService) ActiveTick(in *clientService.Void) (*clientService.Void, error) {
	self.activeTickCnt += 1

	_, err := self.GetClientEndPoint().(clientService.IGameClientInterface).ActiveTickCallback(&clientService.Void{})
	return nil, err
}

func (self *QueueClientService) _replyQueueSuccess(serverId uint32, accountName string) error {
	appLog.Info("queue success ", self.accountName, self.serverId)

	//reply := clientService.QueueReply{State: clientService.QueueReply_QUEUE_SUCCESS, QueueId: uint32(self.queueId), ServerId: self.serverId, ServerHost: self.serverHost}
	//_, err := self.GetClientEndPoint().(clientService.IGameClientInterface).OnQueueReply(&reply)
	return nil
}

func (self *QueueClientService) GetQueueInfo(r *clientService.QueueRequest) (*clientService.Void, error) {
	appLog.Info("GetQueueInfo: ", r.ServerId, r.AccountName)
	serverId := common.Str2UInt32(r.ServerId)
	accountName := r.AccountName
	gameServer := self.app.getGameServer(serverId)
	if gameServer == nil {
		return nil, errors.New(fmt.Sprintf("[GetQueueInfo] cannot find gameserver : %d, %s", serverId, r.AccountName))
	}

	if self.isQueueSuc {
		err := self._replyQueueSuccess(serverId, accountName)
		if err != nil {
			self.app.removeClient(self)
			return nil, err
		}
	} else {
		reply := clientService.QueueReply{State: clientService.QueueReply_QUEUE_IN_PROCESS, QueueId: uint32(self.queueId), ServerId: r.ServerId, ServerHost: self.serverHost}
		self.GetClientEndPoint().(clientService.IGameClientInterface).OnQueueReply(&reply)
	}

	return nil, nil
}

func (self *QueueClientService) SetQueueId(queueId int) {
	self.queueId = queueId
}

func (self *QueueClientService) GetQueueId() int {
	return self.queueId
}

func (self *QueueClientService) GetServerHost() string {
	return self.serverHost
}

func (self *QueueClientService) IsQueueSuc() bool {
	return self.isQueueSuc
}

func (self *QueueClientService) OnRecv() {
	self.tLastRecv = time.Now().Unix()
}

func (self *QueueClientService) GetWaitTime() uint64 {
	var waitTime = uint64(math.Ceil(float64(self.queueId) / float64(LimitPerSecond)))
	return waitTime
}
