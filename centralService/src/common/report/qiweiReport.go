package report

import (
	"centralService/src/common/httputil"
	"fmt"
	"log"
	"sync"
	"time"
)

type QiWeiReport struct {
	// 上报服务器ID
	reportServerID int
	// 上报服务器名
	reportServerName string
	// 单位时间内上报最新N个限制
	reportPerTimeMaxLimit int
	// 单位上报间隔
	reportInterval int
	// 日志缓存收集限制
	reportCacheMaxLimit int
	// 上报地址
	reportAddr string
	// 上报数据队列锁
	reportLock *sync.RWMutex
	// 上报数据队列
	reportDatas []string
	// 上报回调
	reportFunc func([]string)
}

// 获取前N个日志
func (qr *QiWeiReport) getDatas() []string {
	var pushDatas []string
	qr.reportLock.Lock()
	defer qr.reportLock.Unlock()
	if len(qr.reportDatas) >= qr.reportPerTimeMaxLimit {
		pushDatas = qr.reportDatas[:qr.reportPerTimeMaxLimit]
		qr.reportDatas = qr.reportDatas[qr.reportPerTimeMaxLimit:]
	} else {
		pushDatas = qr.reportDatas[:len(qr.reportDatas)]
		qr.reportDatas = qr.reportDatas[:0]
	}
	return pushDatas
}

// 摘取日志准备推送
func (qr *QiWeiReport) pickUpReportLog() []string {
	pushDatas := qr.getDatas()
	return pushDatas
}

// 加入待发送的数据
func (qr *QiWeiReport) addReportLog(data string) {
	if len(data) == 0 {
		return
	}
	qr.reportLock.Lock()
	defer qr.reportLock.Unlock()
	qr.reportDatas = append(qr.reportDatas, data)
	if qr.reportCacheMaxLimit > 0 {
		if len(qr.reportDatas) > qr.reportCacheMaxLimit {
			// 保留最后的qr.reportCacheMaxLimit长度的数据
			qr.reportDatas = qr.reportDatas[len(qr.reportDatas)-qr.reportCacheMaxLimit:]
		}
	}
}

// 间隔上报最新N个数据
func (qr *QiWeiReport) doReport() {
	t := time.NewTimer(time.Duration(1) * time.Second)
	for {
		<-t.C
		//时间片到，摘下当前的数据队列
		pushDatas := qr.pickUpReportLog()
		//开始干活
		if nil != pushDatas && len(pushDatas) > 0 {
			qr.reportFunc(pushDatas)
		}
		//重置下个时间片
		t.Reset(time.Duration(qr.reportInterval) * time.Second)
	}
}

var once sync.Once
var report *QiWeiReport

// 全局有且仅执行一次初始化
func InitQiWeiReport(addr string, serverID int, serverName string, interval int, perTimeMaxLimit int, cacheMaxLimit int) bool {
	if len(addr) == 0 || serverID < 0 || len(serverName) == 0 || interval <= 0 || perTimeMaxLimit <= 0 || cacheMaxLimit <= 0 {
		return false
	}
	once.Do(func() {
		report = &QiWeiReport{
			reportServerID:        serverID,
			reportServerName:      serverName,
			reportPerTimeMaxLimit: perTimeMaxLimit,
			reportInterval:        interval,
			reportCacheMaxLimit:   cacheMaxLimit,
			reportAddr:            addr,
			reportLock:            &sync.RWMutex{},
			reportDatas:           make([]string, 0),
			reportFunc: func(datas []string) {
				defer func() {
					if r := recover(); r != nil {
						log.Printf("report recover from panic: %v", r)
					}
				}()
				var reportDatas string
				reportDatas = fmt.Sprintf("ms report, server name: %v, server id: %v, time: %v", report.reportServerName, report.reportServerID, time.Now())
				for _, data := range datas {
					reportDatas += "\n"
					reportDatas += data
				}
				params := map[string]interface{}{
					"msgtype": "text",
					"text": map[string]interface{}{
						"content": reportDatas,
					},
				}
				respData, err := httputil.PostJson(addr, params)
				if err != nil {
					log.Printf("qiwei report error, report data: %v, resp data: %v, err: %v\n", reportDatas, respData, err.Error())
				}
			},
		}
		go report.doReport()
	})
	return true
}

// 往企微推送日志的主入口
func ReportQiWeiLog(data string) {
	if nil == report {
		log.Println("Pls init qiwei report first !!!")
		return
	}
	report.addReportLog(data)
}
