package base

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"centralService/src/common/report"
	"log"
	"net"
	"os"
	"strings"

	"github.com/spf13/viper"
)

func Init(config interface{}, serverInstance func() common.IApp) bool {
	ret := initCfg(config)
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

func initCfg(config interface{}) bool {
	if err := common.GetConfig(config); err != nil {
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
	ips, err := getLocalIPv4Addresses()
	if err != nil {
		log.Println("获取失败:", err)
		return false
	}

	ret := report.InitQiWeiReport(reportAddr, strings.Join(ips, " "), serverId, serverName, interval, perTimeMaxLimit, cacheMaxLimit)
	if !ret {
		log.Println("base server init fail:", "report init failed", reportAddr)
		return false
	}
	return true
}

func getLocalIPv4Addresses() ([]string, error) {
	var ips []string
	ifaces, err := net.Interfaces()
	if err != nil {
		return nil, err
	}
	for _, iface := range ifaces {
		// 跳过关闭、回环、虚拟网卡（可根据需要调整）
		if iface.Flags&net.FlagUp == 0 || iface.Flags&net.FlagLoopback != 0 {
			continue
		}
		// 跳过常见虚拟网卡名称
		name := strings.ToLower(iface.Name)
		if strings.Contains(name, "docker") || strings.Contains(name, "veth") || strings.Contains(name, "vmnet") {
			continue
		}
		addrs, err := iface.Addrs()
		if err != nil {
			continue
		}
		for _, addr := range addrs {
			if ipNet, ok := addr.(*net.IPNet); ok && ipNet.IP.To4() != nil {
				ips = append(ips, ipNet.IP.String())
			}
		}
	}
	return ips, nil
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
