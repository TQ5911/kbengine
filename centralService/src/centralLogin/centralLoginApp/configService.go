package CentralLogin

import (
	"centralService/src/appLog"
	"centralService/src/common"
	"log"

	"github.com/fsnotify/fsnotify"
	"github.com/spf13/viper"
)

type ConfigStore struct {
	ConstConfig *viper.Viper
}

var ConfigService *ConfigStore

const constConfigPath string = "../data/const.const.txt"

var constConfigMD5 = ""

func InitConfigService() bool {
	ConfigService = &ConfigStore{}
	ConfigService.ConstConfig = viper.New()
	ConfigService.ConstConfig.SetConfigType("json")
	ConfigService.ConstConfig.SetConfigFile(constConfigPath)

	err := ConfigService.ConstConfig.ReadInConfig()
	if err != nil {
		log.Println("Error in reading file: ", constConfigPath, ", error: ", err.Error())
		return false
	}

	constConfigMD5, err = common.ReadFileMd5(constConfigPath)
	if err != nil {
		log.Println("Error in calculating file: ", constConfigPath, " md5 failed", ", error: ", err.Error())
		return false
	}

	ConfigService.ConstConfig.WatchConfig()
	ConfigService.ConstConfig.OnConfigChange(func(e fsnotify.Event) {
		log.Println("ConstConfig file has changed: ", e.Name)
		newMD5, err := common.ReadFileMd5(constConfigPath)
		if err != nil {
			log.Println("Error in calculating new file: ", constConfigPath, " md5 failed", ", error: ", err.Error())
			return
		}

		if newMD5 == constConfigMD5 {
			return
		}

		constConfigMD5 = newMD5
		err = ConfigService.ConstConfig.ReadInConfig()
		if err != nil {
			log.Println("Error in reading new file: ", constConfigPath, ", error: ", err.Error())
			return
		}
		log.Println("Reload new file successfully, file: ", constConfigPath, ", md5: ", constConfigMD5)
	})
	return true
}

func (self *ConfigStore) GetConfig(dataKey string) interface{} {
	d := self.ConstConfig.GetStringMap(dataKey)
	if d == nil {
		appLog.Error("ConstConfig file get key: ", dataKey, " failed !!!")
		return nil
	}
	v, ok := d["value"]
	if !ok {
		appLog.Error("ConstConfig file get key: ", dataKey, " with value failed !!!")
		return nil
	}
	return v
}

func (self *ConfigStore) GetString(dataKey string) (string, bool) {
	d := self.GetConfig(dataKey)
	if nil == d {
		return "", false
	}
	return d.(string), true
}

func (self *ConfigStore) GetInt32(dataKey string) (int32, bool) {
	d := self.GetConfig(dataKey)
	if nil == d {
		return 0, false
	}
	return int32(d.(float64)), true
}
