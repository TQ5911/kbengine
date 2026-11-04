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
	// 最早的一行启动日志：此时配置没读、zap 也没起，只能走 stdout，
	// 但它是"进程确实被 systemd 拉起来了"的唯一证据，配置丢失时尤其重要
	appLog.BootBegin()

	ret := initCfg(config)
	if !ret {
		appLog.BootFailed("init_config")
		return ret
	}

	cfg := common.GetServerCfg()
	if nil == cfg {
		log.Println("base server init fail:", "server config is not inited properly")
		appLog.BootFailed("init_config")
		return false
	}

	ret = initLog(cfg)
	if !ret {
		appLog.BootFailed("init_log")
		return ret
	}

	// 配置已读到、业务日志已就绪，回填 serverName/serverId，
	// 让后续的 ready / failed / exit 行带上完整标识
	appLog.SetBootServerInfo(cfg.GetString("serverName"), cfg.GetInt("serverId"))

	ret = initCommon(cfg)
	if !ret {
		appLog.BootFailed("init_common")
		return ret
	}

	ret = initReport(cfg)
	if !ret {
		appLog.BootFailed("init_report")
		return ret
	}
	ret = initServer(serverInstance)
	if !ret {
		appLog.BootFailed("init_server")
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
		// 这里不能走 common.ExitProgram：它会删 pid 文件，而写失败恰恰说明
		// 该文件属于另一个还活着的进程，删掉等于把别人踢出保护
		appLog.BootFailed("write_pid_file")
		os.Exit(2)
	}

	common.StartListenKillSignal()

	// 接入方在配置文件中配置 mapleHttpAddr 即自动启用游戏服组别数据查询, 未配置则跳过
	common.InitGameServerDataFromConfig()
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
	if app == nil {
		appLog.BootFailed("app_init_return_nil")
		common.ExitProgram(1, "app_init_return_nil")
	}

	common.Run(app)

	// Run 返回说明服务循环已经结束（正常情况不会走到这里）。
	// 补一条 exit 并标记干净退出，让 starting / exit 能配对、下次 prev=clean。
	appLog.BootExit(0, "run_returned")
	appLog.MarkCleanExit()
	return true
}
