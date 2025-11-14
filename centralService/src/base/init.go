package base

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"centralService/src/common/report"
	"log"
	"os"

	"github.com/spf13/viper"
)

func Init(configFileName string, config interface{}, serverInstance func() common.IApp) bool {
	ret := initCfg(configFileName, config)
	if !ret {
		return ret
	}

	cfg := common.GetServerCfg()
	if nil == cfg {
		log.Println("base server init fail:", "server config is not inited properly")
		return false
	}

	ret = initLog(cfg)
	if !ret {
		return ret
	}

	ret = initCommon(cfg)
	if !ret {
		return ret
	}

	ret = initReport(cfg)
	if !ret {
		return ret
	}
	ret = initServer(serverInstance)
	if !ret {
		return ret
	}
	return ret
}

func initCfg(configFileName string, config interface{}) bool {
	if err := common.GetConfig(configFileName, config); err != nil {
		log.Println("base server init fail:", err.Error())
		return false
	}
	return true
}

func initLog(cfg *viper.Viper) bool {
	logPath := cfg.GetString("logPath")
	logLevel := cfg.GetInt("logLevel")
	logRotateSize := cfg.GetInt("logRotateSize")
	if !appLog.LogInit(logPath, logLevel, logRotateSize) {
		log.Println("base server init fail:", logPath, logLevel, logRotateSize)
		return false
	}
	return true
}

func initCommon(cfg *viper.Viper) bool {
	common.SetServerName(cfg.GetString("serverName"))
	common.SetServerID(cfg.GetInt("serverId"))

	common.InitAndParseFlag()
	ok := common.WritePidFile()
	if !ok {
		log.Println("base server init fail:", "common init failed")
		os.Exit(2)
	}

	common.StartListenKillSignal()
	return true
}

func initReport(cfg *viper.Viper) bool {
	reportAddr := cfg.GetString("reportAddr")
	if len(reportAddr) == 0 {
		log.Println("report is not configured")
		return true
	}
	serverId := cfg.GetInt("serverId")
	serverName := cfg.GetString("serverName")
	if len(serverName) == 0 {
		serverName = "unkow server"
	}
	interval := cfg.GetInt("reportInterval")
	if interval == 0 {
		interval = 1
	}
	perTimeMaxLimit := cfg.GetInt("reportPerTimeMaxLimit")
	if perTimeMaxLimit == 0 {
		perTimeMaxLimit = 5
	}
	cacheMaxLimit := cfg.GetInt("reportCacheMaxLimit")
	if cacheMaxLimit == 0 {
		cacheMaxLimit = 100
	}
	ret := report.InitQiWeiReport(reportAddr, serverId, serverName, interval, perTimeMaxLimit, cacheMaxLimit)
	if !ret {
		log.Println("base server init fail:", "report init failed", reportAddr)
		return false
	}
	return true
}

func initServer(serverInstance func() common.IApp) bool {
	app := serverInstance()
	if app != nil {
		common.Run(app)
	} else {
		common.ExitProgram(1)
	}
	return true
}
