package allianceApp

import (
	"centralService/src/appLog"
	"centralService/src/common"
	cmap "centralService/src/common/concurrent_map"
	"log"

	"github.com/fsnotify/fsnotify"
	"github.com/spf13/viper"
)

const (
	CFG_TYPE_GUILD_CONST          = "1"
	CFG_TYPE_MESSAGE_GUILD_LOG    = "2"
	CFG_TYPE_ITEM_DATA            = "3"
	CFG_TYPE_MESSAGE_CHAT_MESSAGE = "4"
)

var ConfigStore *CfgData

type CfgData struct {
	cfgVipers       cmap.ConcurrentMap[string, *viper.Viper]
	cfgFileMD5Datas cmap.ConcurrentMap[string, string]
	cfgFiles        map[string]string
}

func GetCfgFiles() map[string]string {
	datas := map[string]string{
		CFG_TYPE_GUILD_CONST:          "../data/guild.guildConst.txt",
		CFG_TYPE_MESSAGE_GUILD_LOG:    "../data/message.guildLog.txt",
		CFG_TYPE_ITEM_DATA:            "../data/itemData.itemData.txt",
		CFG_TYPE_MESSAGE_CHAT_MESSAGE: "../data/message.chatMessage.txt",
	}
	return datas
}

func InitConfigStore() bool {
	ConfigStore = &CfgData{
		cfgFileMD5Datas: cmap.New[string](),
		cfgVipers:       cmap.New[*viper.Viper](),
		cfgFiles:        GetCfgFiles(),
	}

	return ConfigStore != nil
}

func InitJsonCfg(cfgType string, cfgPath string) error {
	cfg := viper.New()
	cfg.SetConfigType("json")
	cfg.SetConfigFile(cfgPath)
	err := cfg.ReadInConfig()
	if err != nil {
		appLog.Error("Error reading cfg file", err.Error(), cfgPath)
		return err
	}
	cfgMD5, err := common.ReadFileMd5(cfgPath)
	if err != nil {
		appLog.Error("fail to get config md5:", err.Error())
		return err
	}
	ConfigStore.cfgFileMD5Datas.Set(cfgType, cfgMD5)
	ConfigStore.cfgVipers.Set(cfgType, cfg)
	cfg.OnConfigChange(func(e fsnotify.Event) {
		appLog.Info("cfg file changed:", e.Name)
		curMD5, err := common.ReadFileMd5(cfgPath)
		if err != nil {
			log.Println("fail to get cfg md5:", err.Error())
			return
		}

		oldMD5, ret := ConfigStore.cfgFileMD5Datas.Get(cfgType)
		if ret {
			if curMD5 == oldMD5 {
				appLog.Info("cfg file no changed:", e.Name, curMD5, oldMD5)
				return
			}
		}

		appLog.Info("cfg file real changed:", e.Name, curMD5, oldMD5)
		ConfigStore.cfgFileMD5Datas.Set(cfgType, curMD5)
		err = cfg.ReadInConfig()
		if err != nil {
			appLog.Error("Error reading cfg file", err.Error())
		}
	})
	cfg.WatchConfig()
	return nil
}
