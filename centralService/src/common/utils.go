package common

import (
	clientService "centralService/src/centralLogin/centralLoginApp/clientService"
	"crypto/md5"
	"encoding/hex"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	"github.com/gomodule/redigo/redis"
	"github.com/spf13/viper"
)

var letters = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
var cfg = viper.New()

func RandString(n int) string {
	b := make([]rune, n)
	rand.Seed(time.Now().UnixNano())
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}

func InetNtoA(ip uint32) string {
	return fmt.Sprintf("%d.%d.%d.%d",
		byte(ip>>24), byte(ip>>16), byte(ip>>8), byte(ip))
}

func JoinToStr(args ...interface{}) string {
	ret := ""
	for _, arg := range args {
		ret += fmt.Sprintf("%v", arg)
	}
	return ret
}

func GetConfig(config interface{}) error {
	if nil == cfg {
		cfg = viper.New()
	}
	exeName := strings.ToLower(filepath.Base(filepath.Dir(os.Args[0])))
	cfg.SetConfigFile(exeName + ".json")
	err := cfg.ReadInConfig()
	if err != nil {
		return err
	}
	err = cfg.Unmarshal(config)
	if err != nil {
		return err
	}
	return nil
}

func GetAccoutType(platId int8) int32 {
	return int32(clientService.AccountType_ACCOUNT_TOKEN)
}

func Str2UInt32(str string) uint32 {
	u64, err := strconv.ParseUint(str, 10, 32)
	u32 := uint32(u64)
	if err == nil {
		return u32
	} else {
		log.Println("StrToUInt32 error", err, str)
	}
	return 0
}

func Str2UInt64(str string) uint64 {
	u64, err := strconv.ParseUint(str, 10, 64)
	if err == nil {
		return u64
	} else {
		log.Println("Str2UInt64 error", err, str)
	}
	return 0
}

func CalcFileSize(sizeStr string) int64 {
	if len(sizeStr) == 0 {
		return 0
	}
	var size int64
	var err error
	var multiply int64 = 1
	if strings.HasSuffix(sizeStr, "G") {
		multiply = 1024 * 1024 * 1024
		size, err = strconv.ParseInt(strings.Replace(sizeStr, "G", "", 1), 10, 64)
	} else if strings.HasSuffix(sizeStr, "M") {
		multiply = 1024 * 1024
		size, err = strconv.ParseInt(strings.Replace(sizeStr, "M", "", 1), 10, 64)
	} else if strings.HasSuffix(sizeStr, "K") {
		multiply = 1024
		size, err = strconv.ParseInt(strings.Replace(sizeStr, "K", "", 1), 10, 64)
	}
	if err != nil {
		log.Panic("cala size err:", sizeStr, err.Error())
	}

	return size * multiply
}

func GetMD5(s []byte) string {
	m := md5.New()
	m.Write([]byte(s))
	return hex.EncodeToString(m.Sum(nil))
}

func ReadFileMd5(file string) (string, error) {
	config, err := ioutil.ReadFile(file)
	if err != nil {
		return "", err
	}
	return GetMD5(config), nil
}

func RandMapKey(m map[string]string) string {
	mapKeys := make([]string, 0, len(m))
	for key := range m {
		mapKeys = append(mapKeys, key)
	}
	if len(mapKeys) > 0 {
		return mapKeys[rand.Intn(len(mapKeys))]
	}
	return ""
}

func GetRealAccount(accountType int, accountName string) string {
	return strconv.Itoa(accountType) + ":" + accountName
}

func GetAccountName(realAccount string) string {
	return strings.Split(realAccount, ":")[1]
}

func GetAccountInfo(realAccount string) (string, string) {
	strArrs := strings.Split(realAccount, ":")
	return strArrs[0], strArrs[1]
}

func GetNowTime() int64 {
	return time.Now().Unix()
}

func GetServerCfg() *viper.Viper {
	return cfg
}

// GetAvatarServerId: 从 Redis Hash `AvatarInfo_<gbId>` 中读 `serverId` 字段。
//
//   - playerInfoKey = "AvatarInfo_" + gbId, 是玩家档案的 Redis hash key
//   - serverId 字段在该 hash 内,值是十进制字符串 (例如 "20110")
//   - key 不存在、field 不存在、或 pool/gbId 为空, 都返回 (0, nil)
//   - 真正的错误 (网络/解析) 才返回 (0, err), 调用方按 err != nil 处理
//
// 用 HGET 而不是 HGETALL, 只拉一个字段, 减少不必要的数据。
func GetAvatarServerId(pool *redis.Pool, gbId string) (uint32, error) {
	if pool == nil {
		return 0, errors.New("getAvatarServerId: pool is nil")
	}
	if gbId == "" {
		return 0, errors.New("getAvatarServerId: gbId is empty")
	}

	conn, err := GetRedisConn(pool, "utils.GetAvatarServerId")
	if err != nil {
		return 0, fmt.Errorf("getAvatarServerId: get conn: %w", err)
	}
	defer conn.Close()

	val, err := redis.String(conn.Do("HGET", "AvatarInfo_"+gbId, "serverId"))
	if err == redis.ErrNil {
		// key 或 serverId 字段不存在, 视为"找不到", 不是错误
		return 0, nil
	}
	if err != nil {
		return 0, fmt.Errorf("getAvatarServerId: HGET: %w", err)
	}

	u, perr := strconv.ParseUint(val, 10, 32)
	if perr != nil {
		return 0, fmt.Errorf("getAvatarServerId: parse serverId %q: %w", val, perr)
	}
	return uint32(u), nil
}
