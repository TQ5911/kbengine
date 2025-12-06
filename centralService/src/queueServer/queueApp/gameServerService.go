package Queue

import (
	"centralService/src/appLog"
	gameServerService "centralService/src/queueServer/queueApp/gameServerService"
	"centralService/src/trpc"
	"errors"
	"fmt"
	"log"
	"strconv"
	"time"

	"github.com/garyburd/redigo/redis"
	"golang.org/x/time/rate"
)

// 给游戏服务器提供的接口
type GameServerService struct {
	*trpc.ServerEndPoint
	app         *QueueApp
	hostId      uint32
	limiter     *rate.Limiter
	queueTicker *time.Ticker
}

func (self *GameServerService) OnLoseConnection() {
	self.app.removeGameServer(self)
}

func (self *GameServerService) RegisterServer(in *gameServerService.GameServerInfo) (*gameServerService.Void, error) {
	log.Println("register server:", in.HostId)

	server := self.app.getGameServer(in.HostId)
	if server != nil {
		return nil, errors.New(fmt.Sprint("server is already registered: ", in.HostId))
	}

	if in.HostId == 0 {
		return nil, errors.New(fmt.Sprint("invalid hostId: ", in.HostId))
	}

	self.hostId = in.HostId
	self.limiter = rate.NewLimiter(rate.Limit(LimitPerSecond), LimitPerSecond)
	self.queueTicker = time.NewTicker(time.Second * 1)

	self.app.addGameServer(self)
	go self.tickQueue()
	return nil, nil
}

func (self *GameServerService) tickQueue() {
	conn := self.app.redisPool.Get()
	defer conn.Close()
	onlineNum, err := redis.Int(conn.Do("get", "ServerOnlineNum_"+strconv.Itoa(int(self.hostId))))
	if err != nil {
		appLog.Error("tickQueue get ServerOnlineNum_"+strconv.Itoa(int(self.hostId))+" failed", err.Error())
		return
	}
	for {
		<-self.queueTicker.C
		if onlineNum < MaxOnlineNum {
			for {
				if self.limiter.Tokens() < 1 {
					break
				}
				if !self.limiter.Allow() {
					break
				}

				noInQueue := false
				for {
					accountNamePtr := self.app.deQueue(self.hostId)
					if accountNamePtr != nil {
						var accountName = string(*accountNamePtr)
						client := self.app.getClient(accountName)
						if client != nil {
							client.isQueueSuc = true
							client._replyQueueSuccess(self.hostId, accountName)
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

		self.app.QueueTick(self.hostId)
	}
}

func (self *GameServerService) ActiveTick(in *gameServerService.Void) (*gameServerService.Void, error) {
	_, err := self.GetClientEndPoint().(*gameServerService.GameServerClient).ActiveTickCallback(&gameServerService.Void{})
	return nil, err
}
