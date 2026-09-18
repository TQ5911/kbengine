package main

import (
	"centralService/src/base"
	CentralLogin "centralService/src/centralLogin/centralLoginApp"
	"centralService/src/common"
	"fmt"
	"log"

	"github.com/fsnotify/fsnotify"
	"github.com/spf13/viper"
)

func main() {
	configPath := "./serverList.json"
	CentralLogin.ServerListCfg.SetConfigFile(configPath)
	if err := CentralLogin.ServerListCfg.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			log.Panicf("ServerList config file not found: %s\n", configPath)
		} else {
			log.Panicf("fail to open serverList config file: %s\n", configPath)
		}
	}

	fileMD5, err := common.ReadFileMd5(configPath)
	if err != nil {
		log.Println("fail to get config md5:", err.Error())
		return
	}

	CentralLogin.ConfMD5 = fileMD5

	CentralLogin.ServerListCfg.WatchConfig()
	CentralLogin.ServerListCfg.OnConfigChange(func(e fsnotify.Event) {
		fmt.Println("config file changed:", e.Name)
		curMD5, err := common.ReadFileMd5(configPath)
		if err != nil {
			log.Println("fail to get config md5:", err.Error())
			return
		}

		if curMD5 == CentralLogin.ConfMD5 {
			return
		}

		CentralLogin.ConfMD5 = curMD5

		CentralLogin.ServerListCfg.ReadInConfig()
	})

	//loading config service
	if !CentralLogin.InitConfigService() {
		log.Println("Init Config Service failed !!!")
		return
	}

	base.Init(&CentralLogin.LoginConfig, func() common.IApp {
		return CentralLogin.NewCentralLoginApp()
	})
}
