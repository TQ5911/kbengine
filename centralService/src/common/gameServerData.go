package common

import (
	"centralService/src/appLog"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

// 游戏服数据通用组件。
//
// 后台协程每 5s 通过 maple 服务的 http 接口全量拉取游戏服数据,
// 缓存 serverId -> 组别(server_group) 和 serverId -> 所属合并组根服(server_id) 的快照,
// 供各微服务查询。读路径完全无锁, 写路径通过 atomic.Value 整体替换快照。
//
// 另外按 maple 上报的 server_group + server_sub_group 维护一套双向索引:
//
//	"组别_子组别" -> 该组合下的 serverId 列表
//	serverId      -> "组别_子组别"
// 两个索引由同一份服务器列表同源构建, 保证反查出的 key 一定能在正向索引里命中。
// 查询入口: GetGameGroupWithSubGroupServerIdMap / GetGameServerIdGroupWithSubGroupKey
//          / GetGameServerIdListByServerId / GetAllGameGroupWithSubGroupServerIdMap。
// 由 serverId 反查组别与子组别数值: GetGameServerGroupWithSubGroup(原始分组)
//          / GetGameServerGroupWithSubGroupByMerge(和服折叠后);
// 按 组别+子组别 反查 serverId 是否命中: CheckServerIdInGroupWithSubGroup(原始分组)
//          / CheckServerIdInGroupWithSubGroupByMerge(和服折叠后)。
// 该索引按 maple 上报的原始分组建立, 不做和服折叠。
//
// 接入方式: base.initCommon 会调用 InitGameServerDataFromConfig 自动初始化,
// 接入方只需在服务配置文件中增加 "mapleHttpAddr" 配置项即为接入,
// 之后通过 GetGameServerGroup / GetGameServerMergeRoot 等查询对应信息;
// 启动时即依赖数据的逻辑(如按组构建内存索引)可通过 AfterInitMapleServer 注册回调,
// 待首轮数据拉取成功后执行。

const (
	// gameServerDataRefreshInterval 拉取 maple 游戏服数据的周期
	gameServerDataRefreshInterval = 5 * time.Second
	// gameServerDataHttpTimeout 单次 http 请求超时, 必须小于 gameServerDataRefreshInterval
	gameServerDataHttpTimeout = 3 * time.Second
	// gameServerDataURLPath maple 服务查询全部游戏服数据的接口路径
	gameServerDataURLPath = "/getAllServer"
	// gameServerMergeMapURLPath maple 服务查询和服折叠后映射的接口路径
	gameServerMergeMapURLPath = "/getAllMergeServer"
	// mapleHttpAddrConfigKey 服务配置文件中 maple http 地址的约定键名
	mapleHttpAddrConfigKey = "mapleHttpAddr"
)

// gameServerInfo /getAllServer 返回的单个游戏服数据, 只保留本组件关心的字段
type gameServerInfo struct {
	Id             int `json:"id"`
	ServerGroup    int `json:"server_group"`
	ServerSubGroup int `json:"server_sub_group"`
}

// gameServerDataResponse /getAllServer 的响应, 只解析 servers 字段
type gameServerDataResponse struct {
	Servers []gameServerInfo `json:"servers"`
}

// gameMergeMapResponse /getMergeMap 的响应, merge_map: serverId -> 该服所属合并组的根服
type gameMergeMapResponse struct {
	MergeMap map[int]int `json:"merge_map"`
}

var (
	// gameServerGroupMap serverId -> 组别 的只读快照, 每次拉取成功整体替换, 读无锁
	gameServerGroupMap               atomic.Pointer[map[int]int]      // map[int]int
	gameGroupServerIdMap             atomic.Pointer[map[int][]int]    // map[int][]int
	gameGroupWithSubGroupServerIdMap atomic.Pointer[map[string][]int] // map[string][]int
	gameServerIdGroupWithSubGroupMap atomic.Pointer[map[int]string]   // map[int]string
	// gameServerMergeMap serverId -> 所属合并组根服 的只读快照, 语义同上
	// 未参与和服的服不会出现在 map 中 (调用方可用 ok 区分)
	gameServerMergeMap       atomic.Pointer[map[int]int] // map[int]int
	gameServerDataHttpClient = &http.Client{Timeout: gameServerDataHttpTimeout}

	gameServerDataStartOnce sync.Once
	gameServerDataStopOnce  sync.Once
	gameServerDataStopChan  chan struct{}

	// afterInitMu 保护 afterInitInited 与 afterInitHooks
	afterInitMu     sync.Mutex
	afterInitInited bool     // 首轮游戏服数据是否已拉取成功
	afterInitHooks  []func() // 首轮数据拉取成功后待执行的回调(触发后清空)
)

// InitGameServerData 启动后台定时拉取。mapleHttpAddr 为 maple 服务的 http 地址,
// 支持 "127.0.0.1:9527" 或 "http://127.0.0.1:9527" 两种写法。
// 不做同步首拉: 各微服务与 maple 的启动顺序不可假定, 由后台协程持续重试直到成功;
// 重复调用只有首次生效。
func InitGameServerData(mapleHttpAddr string) {
	gameServerDataStartOnce.Do(func() {
		if !strings.HasPrefix(mapleHttpAddr, "http://") &&
			!strings.HasPrefix(mapleHttpAddr, "https://") {
			mapleHttpAddr = "http://" + mapleHttpAddr
		}
		baseURL := mapleHttpAddr
		gameServerDataStopChan = make(chan struct{})
		ExecuteConcurrently(func() { gameServerDataLoop(baseURL) })
	})
}

// InitGameServerDataFromConfig 从全局配置(GetServerCfg)读取 "mapleHttpAddr" 键并启动。
// 未配置时不启动定时查询, 静默跳过。
func InitGameServerDataFromConfig() {
	addr := GetServerCfg().GetString(mapleHttpAddrConfigKey)
	if len(addr) == 0 {
		appLog.Infow("InitGameServerDataFromConfig, need config:", "mapleHttpAddr", mapleHttpAddrConfigKey)
		return
	}
	InitGameServerData(addr)
}

// AfterInitMapleServer 注册"首轮 maple 游戏服数据拉取成功"回调:
// 数据就绪后在独立协程中执行 f, 仅执行一次; 注册时数据已就绪则立即(异步)执行。
// 供启动时即依赖组别/和服数据的逻辑使用。
// 注意: 未配置 mapleHttpAddr 时不存在拉取动作, 回调永远不会触发。
func AfterInitMapleServer(f func()) {
	afterInitMu.Lock()
	if afterInitInited {
		afterInitMu.Unlock()
		ExecuteConcurrently(f)
		return
	}
	afterInitHooks = append(afterInitHooks, f)
	afterInitMu.Unlock()
}

// runAfterInitHooks 首轮数据拉取成功后触发全部已注册回调, 各回调在独立协程中执行
func runAfterInitHooks() {
	afterInitMu.Lock()
	if afterInitInited {
		afterInitMu.Unlock()
		return
	}
	afterInitInited = true
	hooks := afterInitHooks
	afterInitHooks = nil
	afterInitMu.Unlock()

	appLog.Infof("gameServerData: first fetch success, run %d after-init hooks", len(hooks))
	for _, f := range hooks {
		ExecuteConcurrently(f)
	}
}

// StopGameServerData 停止后台拉取协程
func StopGameServerData() {
	gameServerDataStopOnce.Do(func() {
		if gameServerDataStopChan != nil {
			close(gameServerDataStopChan)
		}
	})
}

// GetGameServerGroup 查询游戏服对应的组别; 游戏服不存在或数据尚未就绪时返回 (0, false)。
//
// 在查 group 之前会先经过和服折叠: 若 serverId 存在于 mergeMap 中, 则用其根服 rootId 去查 group;
// 否则保持原 serverId。这样被合入服与目标服视为同一逻辑组, 跨组校验与货架过滤天然一致。
func GetGameServerGroup(serverId int) (int, bool) {
	lookupId := serverId
	if root, ok := getGameServerMergeMap()[serverId]; ok {
		lookupId = root
	}
	group, ok := getGameServerGroupMap()[lookupId]
	return group, ok
}

// GetAllGameServerGroups 返回当前 serverId -> 组别 的全量快照, 快照为只读, 调用方不得修改
func GetAllGameServerGroups() map[int]int {
	return getGameServerGroupMap()
}

// GetGameServerMergeRoot 查询游戏服所属合并组的根服; 未参与和服或数据未就绪时返回 (0, false)。
// 例如 raw: 10002->10003, 10003->10001; GetGameServerMergeRoot(10002) -> (10001, true)
func GetGameServerMergeRoot(serverId uint32) uint32 {
	root, ok := getGameServerMergeMap()[int(serverId)]
	if ok {
		return uint32(root)
	}
	return uint32(serverId)
}

// GetAllGameServerMergeMap 返回当前 serverId -> 所属合并组根服 的全量快照,
// 快照为只读, 调用方不得修改。仅包含参与过合服的服, 未参与合服的服不会出现在 map 中。
func GetAllGameServerMergeMap() map[int]int {
	return getGameServerMergeMap()
}

func CheckServerIdInGroup(groupId int, serverId uint32) bool {
	gId, ok := GetGameServerGroup(int(serverId))
	if !ok {
		appLog.Error("CheckServerIdInGroup: missing group id: ", groupId, serverId)
		return false
	}
	return gId == groupId
}

// CheckServerIdInGroupWithSubGroup 校验 serverId 是否属于指定的组别与子组别;
// 数据未就绪或 serverId 不存在时返回 false。
//
// 注意: 按 maple 上报的原始分组校验, 不做和服折叠;
// 需要与 CheckServerIdInGroup 一致的折叠语义请用 CheckServerIdInGroupWithSubGroupByMerge。
func CheckServerIdInGroupWithSubGroup(groupId, subGroupId int, serverId uint32) bool {
	gId, sId, ok := GetGameServerGroupWithSubGroup(int(serverId))
	if !ok {
		appLog.Error("CheckServerIdInGroupWithSubGroup: missing group info: ", groupId, subGroupId, serverId)
		return false
	}
	return gId == groupId && sId == subGroupId
}

// CheckServerIdInGroupWithSubGroupByMerge 校验 serverId 是否属于指定的组别与子组别,
// 与 CheckServerIdInGroup 一样先经过和服折叠: 被合入的服按其根服所在的分组校验;
// 数据未就绪或 serverId 不存在时返回 false。
func CheckServerIdInGroupWithSubGroupByMerge(groupId, subGroupId int, serverId uint32) bool {
	gId, sId, ok := GetGameServerGroupWithSubGroupByMerge(int(serverId))
	if !ok {
		appLog.Error("CheckServerIdInGroupWithSubGroupByMerge: missing group info: ", groupId, subGroupId, serverId)
		return false
	}
	return gId == groupId && sId == subGroupId
}

func getGameServerGroupMap() map[int]int {
	if v := gameServerGroupMap.Load(); v != nil {
		return *v
	}
	return map[int]int{}
}

func getGameServerMergeMap() map[int]int {
	if v := gameServerMergeMap.Load(); v != nil {
		return *v
	}
	return map[int]int{}
}

func GetGameGroupServerIdMap(groupId int) []int {
	if v := gameGroupServerIdMap.Load(); v != nil {
		d, ok := (*v)[groupId]
		if ok {
			return d
		}
	}
	return []int{}
}

func addGameGroupServerIdMap(serverGroupMap map[int]int) {
	d := make(map[int][]int)
	for k, v := range serverGroupMap {
		w, ok := d[v]
		if !ok {
			w = make([]int, 0)
		}
		w = append(w, k)
		d[v] = w
	}
	gameGroupServerIdMap.Store(&d)
}

// buildGameGroupWithSubGroupIndexes 由同一份服务器列表构建组别索引与反向索引:
//
//	groupWithSubGroupMap: "组别_子组别" -> 该组合下的 serverId 列表
//	serverIdKeyMap:       serverId      -> "组别_子组别"
//
// 两个索引同源构建, 保证任意 serverId 反查出的 key 一定能在正向索引里命中。
func buildGameGroupWithSubGroupIndexes(servers []gameServerInfo) (map[string][]int, map[int]string) {
	groupWithSubGroupMap := make(map[string][]int)
	serverIdKeyMap := make(map[int]string, len(servers))
	for _, server := range servers {
		key := GetGroupWithSubGroupKey(server.ServerGroup, server.ServerSubGroup)
		groupWithSubGroupMap[key] = append(groupWithSubGroupMap[key], server.Id)
		serverIdKeyMap[server.Id] = key
	}
	return groupWithSubGroupMap, serverIdKeyMap
}

// addGameGroupWithSubGroupIndexes 构建并存储组别索引与反向索引快照, 每次拉取成功整体替换。
func addGameGroupWithSubGroupIndexes(servers []gameServerInfo) {
	groupWithSubGroupMap, serverIdKeyMap := buildGameGroupWithSubGroupIndexes(servers)
	gameGroupWithSubGroupServerIdMap.Store(&groupWithSubGroupMap)
	gameServerIdGroupWithSubGroupMap.Store(&serverIdKeyMap)
}

func gameServerDataLoop(baseURL string) {
	ticker := time.NewTicker(1)
	defer ticker.Stop()
	for {
		select {
		case <-gameServerDataStopChan:
			return
		case <-ticker.C:
			ticker.Reset(gameServerDataRefreshInterval)
			refreshGameServerData(baseURL)
		}
	}
}

// refreshGameServerData 拉取一次数据, 成功则整体替换缓存快照, 失败保留旧数据。
// 两份快照 (group / merge) 的拉取互相独立, 各自失败互不影响;
// group 拉取成功(merge 已尝试)后触发 AfterInitMapleServer 注册的回调。
func refreshGameServerData(baseURL string) {
	groupURL := baseURL + gameServerDataURLPath
	mergeURL := baseURL + gameServerMergeMapURLPath

	serverGroupMapOK := false
	if servers, err := fetchGameServers(groupURL); err != nil {
		appLog.Error("gameServerData: refresh group failed: ", err.Error())
	} else {
		newMap := buildGameServerGroupMap(servers)
		gameServerGroupMap.Store(&newMap)
		addGameGroupServerIdMap(newMap)
		addGameGroupWithSubGroupIndexes(servers)
		serverGroupMapOK = true
	}

	serverMergeMapOK := false
	if newMap, err := fetchGameServerMergeMap(mergeURL); err != nil {
		appLog.Error("gameServerData: refresh merge failed: ", err.Error())
	} else {
		gameServerMergeMap.Store(&newMap)
		serverMergeMapOK = true
	}

	if serverGroupMapOK && serverMergeMapOK {
		runAfterInitHooks()
	}
}

// fetchGameServers 拉取 maple 的全部游戏服数据, 返回解析后的服务器列表。
// 只做 http + json 解析, 不做业务加工, 由调用方按需构建各类索引。
func fetchGameServers(url string) ([]gameServerInfo, error) {
	resp, err := gameServerDataHttpClient.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var response gameServerDataResponse
	if err = json.Unmarshal(body, &response); err != nil {
		return nil, err
	}

	return response.Servers, nil
}

// buildGameServerGroupMap 由服务器列表构建 serverId -> 组别 的映射
func buildGameServerGroupMap(servers []gameServerInfo) map[int]int {
	newMap := make(map[int]int, len(servers))
	for _, server := range servers {
		newMap[server.Id] = server.ServerGroup
	}
	return newMap
}

func fetchGameServerMergeMap(url string) (map[int]int, error) {
	resp, err := gameServerDataHttpClient.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var response gameMergeMapResponse
	if err = json.Unmarshal(body, &response); err != nil {
		return nil, err
	}

	if len(response.MergeMap) == 0 {
		return map[int]int{}, nil
	}

	newMap := make(map[int]int, len(response.MergeMap))
	for from, to := range response.MergeMap {
		newMap[from] = to
	}
	return newMap, nil
}

func GetGroupWithSubGroupKey(groupId, subGroupId int) string {
	return fmt.Sprintf("%v_%v", groupId, subGroupId)
}

// ParseGroupWithSubGroupKey 解析 GetGroupWithSubGroupKey 生成的 key, 还原组别与子组别
func ParseGroupWithSubGroupKey(key string) (int, int, bool) {
	var groupId, subGroupId int
	if _, err := fmt.Sscanf(key, "%d_%d", &groupId, &subGroupId); err != nil {
		return 0, 0, false
	}
	return groupId, subGroupId, true
}

// GetGameGroupWithSubGroupServerIdMap 查询指定组别+子组别下的 serverId 列表;
// 该组合不存在或数据尚未就绪时返回空切片。
//
// 注意: 本索引按 maple 上报的原始分组建立, 不做和服折叠(与 GetGameServerGroup 的折叠语义不同);
// 需要和服语义时先用 GetGameServerMergeRoot 把 serverId 换成根服再查。
func GetGameGroupWithSubGroupServerIdMap(groupId, subGroupId int) []int {
	key := GetGroupWithSubGroupKey(groupId, subGroupId)
	if v := gameGroupWithSubGroupServerIdMap.Load(); v != nil {
		if d, ok := (*v)[key]; ok {
			return d
		}
	}
	return []int{}
}

// GetGameServerIdGroupWithSubGroupKey 反向索引: 由 serverId 反查其所属的 "组别_子组别" key;
// 游戏服不存在或数据尚未就绪时返回 ("", false)。
//
// 注意: 同样是原始分组语义, 不做和服折叠。
func GetGameServerIdGroupWithSubGroupKey(serverId int) (string, bool) {
	if v := gameServerIdGroupWithSubGroupMap.Load(); v != nil {
		if key, ok := (*v)[serverId]; ok {
			return key, true
		}
	}
	return "", false
}

// GetGameServerIdListByServerId 由 serverId 反查其所在的 "组别_子组别", 再返回同组的 serverId 列表;
// serverId 不存在时返回空切片。这是反向索引与正向索引配合使用的常用入口。
func GetGameServerIdListByServerId(serverId int) []int {
	key, ok := GetGameServerIdGroupWithSubGroupKey(serverId)
	if !ok {
		return []int{}
	}
	if v := gameGroupWithSubGroupServerIdMap.Load(); v != nil {
		if d, ok := (*v)[key]; ok {
			return d
		}
	}
	return []int{}
}

// GetGameServerGroupWithSubGroup 由 serverId 反查其所属的组别与子组别;
// 游戏服不存在或数据尚未就绪时返回 (0, 0, false)。
//
// 注意: 按 maple 上报的原始分组返回, 不做和服折叠;
// 需要与 GetGameServerGroup 一致的折叠语义请用 GetGameServerGroupWithSubGroupByMerge。
func GetGameServerGroupWithSubGroup(serverId int) (int, int, bool) {
	key, ok := GetGameServerIdGroupWithSubGroupKey(serverId)
	if !ok {
		return 0, 0, false
	}
	groupId, subGroupId, ok := ParseGroupWithSubGroupKey(key)
	if !ok {
		return 0, 0, false
	}
	if groupId <= 0 || subGroupId <= 0 {
		return 0, 0, false
	}
	return groupId, subGroupId, true
}

// GetGameServerGroupWithSubGroupByMerge 由 serverId 反查其所属的组别与子组别,
// 与 GetGameServerGroup 一样先经过和服折叠: 被合入的服按其根服所在的分组返回;
// 游戏服不存在或数据尚未就绪时返回 (0, 0, false)。
func GetGameServerGroupWithSubGroupByMerge(serverId int) (int, int, bool) {
	lookupId := serverId
	if root, ok := getGameServerMergeMap()[serverId]; ok {
		lookupId = root
	}
	return GetGameServerGroupWithSubGroup(lookupId)
}

// GetAllGameGroupWithSubGroupServerIdMap 返回 "组别_子组别" -> serverId 列表 的全量快照,
// 快照为只读, 调用方不得修改
func GetAllGameGroupWithSubGroupServerIdMap() map[string][]int {
	if v := gameGroupWithSubGroupServerIdMap.Load(); v != nil {
		return *v
	}
	return map[string][]int{}
}

// GetAllGameServerIdGroupWithSubGroupMap 返回 serverId -> "组别_子组别" 的全量快照,
// 快照为只读, 调用方不得修改
func GetAllGameServerIdGroupWithSubGroupMap() map[int]string {
	if v := gameServerIdGroupWithSubGroupMap.Load(); v != nil {
		return *v
	}
	return map[int]string{}
}
