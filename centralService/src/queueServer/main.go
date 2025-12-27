package main

import (
	"centralService/src/base"
	"centralService/src/common"
	Queue "centralService/src/queueServer/queueApp"
	"log"

	"github.com/fsnotify/fsnotify"
	"github.com/spf13/viper"
)

func main() {
	configPath := "./serverList.json"
	Queue.ServerListCfg.SetConfigFile(configPath)
	if err := Queue.ServerListCfg.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			log.Panicf("ServerList config file not found: %s\n", configPath)
		} else {
			log.Panicf("fail to open serverList config file: %s\n", configPath)
		}
	}

	var err error
	Queue.ConfMD5, err = common.ReadFileMd5(configPath)
	if err != nil {
		log.Println("fail to get config md5:", err.Error())
		return
	}

	Queue.MaxOnlineNum = Queue.ServerListCfg.GetInt("maxOnlineNum")
	Queue.LimitPerSecond = Queue.ServerListCfg.GetInt("limitPerSecond")

	Queue.ServerListCfg.WatchConfig()
	Queue.ServerListCfg.OnConfigChange(func(e fsnotify.Event) {
		log.Println("config file changed:", e.Name)
		curMD5, err := common.ReadFileMd5(configPath)
		if err != nil {
			log.Println("fail to get config md5:", err.Error())
			return
		}

		if curMD5 == Queue.ConfMD5 {
			return
		}

		Queue.ConfMD5 = curMD5
		Queue.ServerListCfg.ReadInConfig()
		Queue.MaxOnlineNum = Queue.ServerListCfg.GetInt("maxOnlineNum")
		Queue.LimitPerSecond = Queue.ServerListCfg.GetInt("limitPerSecond")
		log.Print("maxOnlineNum: ", Queue.MaxOnlineNum, " limitPerSecond: ", Queue.LimitPerSecond)
	})

	base.Init("queueConf.json", &Queue.QueueConfig, func() common.IApp {
		return Queue.NewQueueApp()
	})
}
