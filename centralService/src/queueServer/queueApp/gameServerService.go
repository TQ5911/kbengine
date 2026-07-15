package Queue

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"context"
	gameServerService "centralService/src/queueServer/queueApp/gameServerService"
	"centralService/src/trpc"
	"fmt"
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
	clearTicker *time.Ticker
}

func (self *GameServerService) OnLoseConnection() {
	self.app.removeGameServer(self)
}

// 每5秒清除队列中等待时间超过10秒的账号
func (self *GameServerService) clearQueue() {
	for {
		<-self.clearTicker.C
		self.app.clearQueue(self.hostId)
	}
}

func (self *GameServerService) tickQueue() {
	for {
		ctx, cancel := context.WithTimeout(context.Background(), common.RedisOpTimeout)
		conn, err := self.app.redisPool.GetContext(ctx)
		cancel()
		if err != nil {
			appLog.Errorf("tickQueue get redis conn failed, hostId=%d, err=%s", self.hostId, err.Error())
			<-self.queueTicker.C
			continue
		}
		<-self.queueTicker.C
		onlineNum, err := redis.Int(conn.Do("get", "g:normal_online_num"+strconv.Itoa(int(self.hostId))))
		conn.Close()
		if err != nil {
			appLog.Error("tickQueue get g:normal_online_num"+strconv.Itoa(int(self.hostId))+" failed", err.Error())
			continue
		}
		appLog.Info("tickQueue: ", onlineNum, " ", "g:normal_online_num"+strconv.Itoa(int(self.hostId)), " ", MaxOnlineNum)
		var items []string
		for k, v := range self.app.serverVIPQueues {
			items = append(items, fmt.Sprintf("(%d: %v), ", k, v.Items))
		}
		appLog.Info("vip queue: ", items)

		var items2 []string
		for k, v := range self.app.serverQueues {
			items2 = append(items2, fmt.Sprintf("(%d: %v), ", k, v.Items))
		}
		appLog.Info("queue: ", items2)
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
