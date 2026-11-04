package MapleApp

import (
	"centralService/src/appLog"
	"centralService/src/maple/model"
	"crypto/hmac"
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strconv"
	"strings"
	"time"
)

// 和服映射表 maple_merge_server 期望
// ( from_server_id INT PRIMARY KEY, to_server_id INT, INDEX(to_server_id) )
// 其中 from_server_id 是被合入的服, to_server_id 是合入目标; 每服最多一条出边。

type MapleHttpService struct {
	app *MapleApp
}

func NewMapleHttpService(app *MapleApp) *MapleHttpService {
	mhs := MapleHttpService{
		app: app,
	}
	return &mhs
}

func (mhs *MapleHttpService) handleAuth(w http.ResponseWriter, r *http.Request) bool {
	for k, v := range r.Header {
		appLog.Info(k, v)
	}

	ts := r.Header.Get("ts")
	nc := r.Header.Get("nc")
	method := r.Method

	tsInt, err := strconv.ParseInt(ts, 10, 64)
	if err != nil {
		appLog.Error("parse ts error: ", err.Error())
		w.WriteHeader(http.StatusUnauthorized)
		return false
	}

	now := time.Now().Unix()
	if tsInt < now-10 || tsInt > now+10 {
		appLog.Error("ts out of range: ", tsInt)
		w.WriteHeader(http.StatusUnauthorized)
		return false
	}

	secret := MapleConfig.Secret

	plainText := fmt.Sprintf("%s%s%s", method, ts, nc)

	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(plainText))
	macStr := hex.EncodeToString(mac.Sum(nil))

	sign := r.Header.Get("sign")

	if sign != macStr {
		appLog.Error("sign error: ", sign, macStr)
		w.WriteHeader(http.StatusUnauthorized)
		return false
	}

	return true
}

func (mhs *MapleHttpService) getAllZone() map[uint32]string {
	sql := "SELECT zone_id, zone_name FROM `maple_zone`"
	rows, err := mhs.app.db.Query(sql)
	if err != nil {
		appLog.Error("exec sql error: ", err.Error())
	}

	zoneMap := make(map[uint32]string)
	for rows.Next() {
		var zoneId uint32
		var zoneName string
		err = rows.Scan(&zoneId, &zoneName)
		if err != nil {
			appLog.Error("scan row error: ", err.Error())
		}
		zoneMap[zoneId] = zoneName
	}

	return zoneMap
}

func (mhs *MapleHttpService) getAllKV() map[string]string {
	sql := "SELECT `key`, `value` FROM `maple_kv`"
	rows, err := mhs.app.db.Query(sql)
	if err != nil {
		appLog.Error("exec sql error: ", err.Error())
	}

	kvMap := make(map[string]string)
	for rows.Next() {
		var key string
		var value string
		err = rows.Scan(&key, &value)
		if err != nil {
			appLog.Error("scan row error: ", err.Error())
		}
		kvMap[key] = value
	}

	return kvMap
}

func (mhs *MapleHttpService) getAllServer(w http.ResponseWriter, r *http.Request) {
	appLog.Info("getAllServer")
	enableCors(&w)

	zoneMap := mhs.getAllZone()

	sql := "SELECT server_id, server_name, zone_id, game_server, queue_server, server_group, server_sub_group, server_state, server_flag_state, alias, start_time, central_login FROM `maple`"
	rows, err := mhs.app.db.Query(sql)
	if err != nil {
		appLog.Error("exec sql error: ", err.Error())
	}

	var serverList []model.Server
	for rows.Next() {
		var server model.Server
		err = rows.Scan(&server.Id, &server.ServerName, &server.ZoneId, &server.GameServer, &server.QueueServer, &server.ServerGroup, &server.ServerSubGroup, &server.ServerState, &server.ServerFlagState, &server.Alias, &server.StartTime, &server.CentralLogin)
		if err != nil {
			appLog.Error("scan row error: ", err.Error())
		}

		server.ZoneName = zoneMap[uint32(server.ZoneId)]
		serverList = append(serverList, server)
	}

	kvMap := mhs.getAllKV()

	var zoneList []model.ZoneData
	for id, name := range zoneMap {
		zoneList = append(zoneList, model.ZoneData{
			ZoneId:   int(id),
			ZoneName: name,
		})
	}

	response := model.GetAllServerResponse{
		Servers: serverList,
		Zones:   zoneList,
		KV:      kvMap,
	}

	jsonData, err := json.Marshal(response)
	if err != nil {
		appLog.Error("marshal json error:", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}

func (mhs *MapleHttpService) handleImport(w http.ResponseWriter, r *http.Request) {
	// Allow CORS for browser-based tools
	enableCors(&w)
	if !mhs.handleAuth(w, r) {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("unauthorized"))
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		appLog.Error("read body error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

	appLog.Info("body: ", string(body))

	var serverList model.ServerList
	err = json.Unmarshal(body, &serverList)
	if err != nil {
		appLog.Error("unmarshal body error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("unmarshal body error"))
		return
	}

	appLog.Info("serverList: ", serverList)

	// Full import: clear existing data, then insert all
	tx, err := mhs.app.db.Begin()
	if err != nil {
		appLog.Error("begin tx error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("begin tx error"))
		return
	}

	// Delete from child table first to satisfy FK constraints, if any
	if _, err = tx.Exec("DELETE FROM `maple`"); err != nil {
		appLog.Error("clear maple error: ", err.Error())
		tx.Rollback()
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("clear maple error"))
		return
	}
	if _, err = tx.Exec("DELETE FROM `maple_zone`"); err != nil {
		appLog.Error("clear maple_zone error: ", err.Error())
		tx.Rollback()
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("clear maple_zone error"))
		return
	}

	for _, server := range serverList.Servers {
		// Insert or update zone first to ensure referential integrity
		sql := "INSERT INTO `maple_zone` (`zone_id`, `zone_name`) VALUES (?, ?) ON DUPLICATE KEY UPDATE `zone_name`=VALUES(`zone_name`)"
		if _, err = tx.Exec(sql, server.ZoneId, server.ZoneName); err != nil {
			appLog.Error("exec zone sql error: ", err.Error())
			tx.Rollback()
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte("insert zone error"))
			return
		}

		sql = "INSERT INTO `maple` (`server_id`, `server_name`, `zone_id`, `game_server`, `queue_server`, `server_group`, `server_state`, `server_flag_state`, `alias`, `start_time`, `central_login`, `server_sub_group`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
		if _, err = tx.Exec(sql, server.Id, server.ServerName, server.ZoneId, server.GameServer, server.QueueServer, server.ServerGroup, server.ServerState, server.ServerFlagState, server.Alias, server.StartTime, server.CentralLogin, server.ServerSubGroup); err != nil {
			appLog.Error("exec server sql error: ", err.Error())
			tx.Rollback()
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte("insert server error"))
			return
		}
	}

	if err = tx.Commit(); err != nil {
		appLog.Error("commit tx error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("commit tx error"))
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("success"))
}

// handleExport returns full JSON of zones and servers
func (mhs *MapleHttpService) handleExport(w http.ResponseWriter, r *http.Request) {
	appLog.Info("handleExport")
	enableCors(&w)

	if !mhs.handleAuth(w, r) {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("unauthorized"))
		return
	}

	zoneMap := mhs.getAllZone()

	sql := "SELECT server_id, server_name, zone_id, game_server, queue_server, server_group, server_sub_group, server_state, server_flag_state, alias, start_time, central_login FROM `maple`"
	rows, err := mhs.app.db.Query(sql)
	if err != nil {
		appLog.Error("exec sql error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

	var list model.ServerList
	for rows.Next() {
		var s model.Server
		if err = rows.Scan(&s.Id, &s.ServerName, &s.ZoneId, &s.GameServer, &s.QueueServer, &s.ServerGroup, &s.ServerSubGroup, &s.ServerState, &s.ServerFlagState, &s.Alias, &s.StartTime, &s.CentralLogin); err != nil {
			appLog.Error("scan row error: ", err.Error())
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte("scan row error"))
			return
		}
		s.ZoneName = zoneMap[uint32(s.ZoneId)]
		list.Servers = append(list.Servers, s)
	}

	jsonData, err := json.Marshal(list)
	if err != nil {
		appLog.Error("marshal json error:", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}

func enableCors(w *http.ResponseWriter) {
	(*w).Header().Set("Access-Control-Allow-Origin", "*")
	(*w).Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
	(*w).Header().Set("Access-Control-Allow-Headers", "Authorization, ts, nc, sign, Content-Type")
}

func (mhs *MapleHttpService) getAllZoneData(w http.ResponseWriter, r *http.Request) {
	appLog.Info("getAllZoneData")
	enableCors(&w)

	zoneMap := mhs.getAllZone()

	jsonData, err := json.Marshal(zoneMap)
	if err != nil {
		appLog.Error("marshal json error:", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}

func (mhs *MapleHttpService) addZone(w http.ResponseWriter, r *http.Request) {
	if !mhs.handleAuth(w, r) {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("unauthorized"))
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		appLog.Error("read body error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

	appLog.Info("body: ", string(body))

	var zoneData model.ZoneData
	err = json.Unmarshal(body, &zoneData)
	if err != nil {
		appLog.Error("unmarshal body error: ", err.Error())
	}

	sql := "INSERT INTO `maple_zone` (`zone_id`, `zone_name`) VALUES (?, ?)"
	_, err = mhs.app.db.Exec(sql, zoneData.ZoneId, zoneData.ZoneName)
	if err != nil {
		appLog.Error("exec sql error: ", err.Error())
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("success"))
}

func (mhs *MapleHttpService) removeZone(w http.ResponseWriter, r *http.Request) {
	appLog.Info("removeZone")
	enableCors(&w)

	if !mhs.handleAuth(w, r) {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("unauthorized"))
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		appLog.Error("read body error: ", err.Error())
	}

	appLog.Info("body: ", string(body))

	var req model.RemoveZoneRequest
	err = json.Unmarshal(body, &req)
	if err != nil {
		appLog.Error("unmarshal body error: ", err.Error())
	}

	sql := "DELETE FROM `maple_zone` WHERE `zone_id` = ?"
	_, err = mhs.app.db.Exec(sql, req.ZoneId)
	if err != nil {
		appLog.Error("exec sql error: ", err.Error())
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("success"))
}

func (mhs *MapleHttpService) updateZone(w http.ResponseWriter, r *http.Request) {
	appLog.Info("updateZone")
	enableCors(&w)

	if !mhs.handleAuth(w, r) {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("unauthorized"))
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		appLog.Error("read body error: ", err.Error())
	}

	appLog.Info("body: ", string(body))

	var zoneData model.ZoneData
	err = json.Unmarshal(body, &zoneData)
	if err != nil {
		appLog.Error("unmarshal body error: ", err.Error())
	}

	sql := "UPDATE `maple_zone` SET `zone_name` = ? WHERE `zone_id` = ?"
	_, err = mhs.app.db.Exec(sql, zoneData.ZoneName, zoneData.ZoneId)
	if err != nil {
		appLog.Error("exec sql error: ", err.Error())
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("success"))
}

// serverPatch 是 updateServer 的请求体, 字段全部用指针: nil 表示请求体里没有该字段, 对应列保持库里原值;
// 传了零值 (0 / "" ) 则表示确实要写成零值。所以前端可以只提交 { "id": 10001, "server_state": 2 } 这样的增量补丁。
type serverPatch struct {
	Id              *int    `json:"id"`
	ServerId        *int    `json:"server_id"` // 兼容用 server_id 当主键的调用方
	ServerName      *string `json:"server_name"`
	ZoneId          *int    `json:"zone_id"`
	ZoneName        *string `json:"zone_name"` // 不是 maple 表的列, 落到 maple_zone
	GameServer      *string `json:"game_server"`
	QueueServer     *string `json:"queue_server"`
	CentralLogin    *string `json:"central_login"`
	ServerGroup     *int    `json:"server_group"`
	ServerSubGroup  *int    `json:"server_sub_group"`
	ServerState     *int    `json:"server_state"`
	ServerFlagState *int    `json:"server_flag_state"`
	Alias           *string `json:"alias"`
	StartTime       *int64  `json:"start_time"`
}

// serverId 取主键, 同时兼容 id / server_id 两种写法。
func (p *serverPatch) serverId() (int, bool) {
	if p.Id != nil {
		return *p.Id, true
	}
	if p.ServerId != nil {
		return *p.ServerId, true
	}
	return 0, false
}

// patchColumn 是 maple 表上一个待更新的列。
type patchColumn struct {
	column string
	value  interface{}
}

// mapleColumns 返回请求里实际出现过的 maple 列, 顺序固定, 用于动态拼 UPDATE。
// 注意 zone_name 不在这里, 它对应 maple_zone 表, 由调用方单独处理。
func (p *serverPatch) mapleColumns() []patchColumn {
	var cols []patchColumn
	addStr := func(col string, v *string) {
		if v != nil {
			cols = append(cols, patchColumn{col, *v})
		}
	}
	addInt := func(col string, v *int) {
		if v != nil {
			cols = append(cols, patchColumn{col, *v})
		}
	}

	addStr("server_name", p.ServerName)
	addInt("zone_id", p.ZoneId)
	addStr("game_server", p.GameServer)
	addStr("queue_server", p.QueueServer)
	addStr("central_login", p.CentralLogin)
	addInt("server_group", p.ServerGroup)
	addInt("server_sub_group", p.ServerSubGroup)
	addInt("server_state", p.ServerState)
	addInt("server_flag_state", p.ServerFlagState)
	addStr("alias", p.Alias)
	if p.StartTime != nil {
		cols = append(cols, patchColumn{"start_time", *p.StartTime})
	}
	return cols
}

// valOr: 指针为 nil 时取默认值, 用于插入新服时补齐没传的字段。
func valOr[T any](p *T, def T) T {
	if p == nil {
		return def
	}
	return *p
}

// upsertZone: zone_name 不在 maple 表里, 需要单独维护 maple_zone。
func upsertZone(tx *sql.Tx, zoneId int, zoneName string) error {
	sqlStr := "INSERT INTO `maple_zone` (`zone_id`, `zone_name`) VALUES (?, ?) ON DUPLICATE KEY UPDATE `zone_name`=VALUES(`zone_name`)"
	_, err := tx.Exec(sqlStr, zoneId, zoneName)
	return err
}

func (mhs *MapleHttpService) updateServer(w http.ResponseWriter, r *http.Request) {
	appLog.Info("updateServer")
	enableCors(&w)

	if !mhs.handleAuth(w, r) {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("unauthorized"))
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		appLog.Error("read body error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

	appLog.Info("updateServer body: ", string(body))

	// 用 serverPatch 反序列化, 才能区分"字段没传"和"字段传了零值"
	var patch serverPatch
	if err = json.Unmarshal(body, &patch); err != nil {
		appLog.Error("unmarshal body error: ", err.Error())
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("unmarshal body error"))
		return
	}

	serverId, ok := patch.serverId()
	if !ok || serverId <= 0 {
		appLog.Error("updateServer: missing or invalid server id, body: ", string(body))
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("missing server id"))
		return
	}

	tx, err := mhs.app.db.Begin()
	if err != nil {
		appLog.Error("begin tx error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("begin tx error"))
		return
	}

	fail := func(msg string, cause error) {
		if cause != nil {
			appLog.Error(msg, ": ", cause.Error())
		}
		tx.Rollback()
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(msg))
	}

	// 先判断是否存在
	var count int
	if err = tx.QueryRow("SELECT COUNT(*) FROM `maple` WHERE `server_id` = ?", serverId).Scan(&count); err != nil {
		fail("query server error", err)
		return
	}

	// zone_name 要落到 maple_zone, 需要用 zone_id 定位: 补丁里没给就沿用库里现有的值
	zoneId := 0
	if patch.ZoneId != nil {
		zoneId = *patch.ZoneId
	}

	if count == 0 {
		// 不存在则插入: 补丁里没传的字段按零值落库; server_sub_group 除外, 建表默认值是 1 (见 bin/maple/up.sql)
		if patch.ZoneName != nil && zoneId != 0 {
			if err = upsertZone(tx, zoneId, *patch.ZoneName); err != nil {
				fail("insert zone error", err)
				return
			}
		}

		sqlStr := "INSERT INTO `maple` (`server_id`, `server_name`, `zone_id`, `game_server`, `queue_server`, `server_group`, `server_state`, `server_flag_state`, `alias`, `start_time`, `central_login`, `server_sub_group`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
		_, err = tx.Exec(sqlStr, serverId, valOr(patch.ServerName, ""), zoneId, valOr(patch.GameServer, ""), valOr(patch.QueueServer, ""), valOr(patch.ServerGroup, 0), valOr(patch.ServerState, 0), valOr(patch.ServerFlagState, 0), valOr(patch.Alias, ""), valOr(patch.StartTime, int64(0)), valOr(patch.CentralLogin, ""), valOr(patch.ServerSubGroup, 1))
		if err != nil {
			fail("insert server error", err)
			return
		}
	} else {
		// 增量更新: 只拼请求里出现过的列, 没出现的列保持原值
		cols := patch.mapleColumns()
		if len(cols) > 0 {
			sets := make([]string, 0, len(cols))
			args := make([]interface{}, 0, len(cols)+1)
			for _, c := range cols {
				sets = append(sets, "`"+c.column+"` = ?")
				args = append(args, c.value)
			}
			args = append(args, serverId)

			sqlStr := "UPDATE `maple` SET " + strings.Join(sets, ", ") + " WHERE `server_id` = ?"
			if _, err = tx.Exec(sqlStr, args...); err != nil {
				fail("update server error", err)
				return
			}
		}

		// 只有显式传了 zone_name 才动 maple_zone, 否则不要把 zone_name 清空
		if patch.ZoneName != nil {
			if patch.ZoneId == nil {
				if err = tx.QueryRow("SELECT `zone_id` FROM `maple` WHERE `server_id` = ?", serverId).Scan(&zoneId); err != nil {
					fail("query zone id error", err)
					return
				}
			}
			if zoneId != 0 {
				if err = upsertZone(tx, zoneId, *patch.ZoneName); err != nil {
					fail("update zone error", err)
					return
				}
			} else {
				appLog.Error("updateServer: zone_id is 0, skip zone update, server_id=", serverId)
			}
		}
	}

	if err = tx.Commit(); err != nil {
		appLog.Error("commit tx error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("commit tx error"))
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("success"))
}

func (mhs *MapleHttpService) handleUpdateKV(w http.ResponseWriter, r *http.Request) {
	appLog.Info("handleUpdateKV")
	enableCors(&w)

	if !mhs.handleAuth(w, r) {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("unauthorized"))
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		appLog.Error("read body error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

	appLog.Info("body: ", string(body))

	var kvMap map[string]string
	err = json.Unmarshal(body, &kvMap)
	if err != nil {
		appLog.Error("unmarshal body error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("unmarshal body error"))
		return
	}

	tx, err := mhs.app.db.Begin()
	if err != nil {
		appLog.Error("begin tx error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("begin tx error"))
		return
	}

	for key, value := range kvMap {
		sql := "INSERT INTO `maple_kv` (`key`, `value`) VALUES (?, ?) ON DUPLICATE KEY UPDATE `value`=VALUES(`value`)"
		if _, err = tx.Exec(sql, key, value); err != nil {
			appLog.Error("exec kv sql error: ", err.Error())
			tx.Rollback()
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte("insert kv error"))
			return
		}
	}

	if err = tx.Commit(); err != nil {
		appLog.Error("commit tx error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("commit tx error"))
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("success"))
}

func (mhs *MapleHttpService) removeServer(w http.ResponseWriter, r *http.Request) {
	appLog.Info("removeServer")
	enableCors(&w)

	if !mhs.handleAuth(w, r) {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("unauthorized"))
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		appLog.Error("read body error: ", err.Error())
	}

	appLog.Info("body: ", string(body))

	var server model.RemoveServerRequest
	err = json.Unmarshal(body, &server)
	if err != nil {
		appLog.Error("unmarshal body error: ", err.Error())
	}

	sql := "DELETE FROM `maple` WHERE `server_id` = ?"
	_, err = mhs.app.db.Exec(sql, server.Id)
	if err != nil {
		appLog.Error("exec sql error: ", err.Error())
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("success"))
}

func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "*")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		next.ServeHTTP(w, r)
	})
}

// loadMergeMap: 一次性把 maple_merge_server 全部 (from -> to) 加载到内存。
// 在 addMergeServer 的环形检测和 getAllMergeServer 的折叠中都会用到, 避免每跳一次 SQL。
func (mhs *MapleHttpService) loadMergeMap() (map[int]int, error) {
	rows, err := mhs.app.db.Query("SELECT `from_server_id`, `to_server_id` FROM `maple_merge_server`")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	m := make(map[int]int)
	for rows.Next() {
		var from, to int
		if err = rows.Scan(&from, &to); err != nil {
			return nil, err
		}
		m[from] = to
	}
	return m, nil
}

// hasPath: 在给定 from->to 内存图中, 从 from 出发能否沿有向边走到 to (BFS, 带 visited)。
func hasPath(from int, to int, m map[int]int) bool {
	if from == to {
		return true
	}
	visited := make(map[int]bool)
	queue := []int{from}
	for len(queue) > 0 {
		cur := queue[0]
		queue = queue[1:]
		if visited[cur] {
			continue
		}
		visited[cur] = true
		next, ok := m[cur]
		if !ok {
			continue
		}
		if next == to {
			return true
		}
		queue = append(queue, next)
	}
	return false
}

// addMergeServer: 新增一条 from->to 的和服映射。
//   - 同一 from 已存在映射则覆盖 (ON DUPLICATE KEY UPDATE);
//   - 写入前先做环形检测: to 必须不能沿现有有向边走回 from, 否则加上 from->to 会形成环;
//   - 注意这里是按"加入新边前"的状态判断, 所以 from 自身的旧出边 (如果有) 不会参与新边的环判定,
//     因为 from 的出边被新边替换, 而旧出边的下游链路在 new 视角下与 from 不相连。
func (mhs *MapleHttpService) addMergeServer(w http.ResponseWriter, r *http.Request) {
	if !mhs.handleAuth(w, r) {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("unauthorized"))
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		appLog.Error("read body error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

	appLog.Info("addMergeServer body: ", string(body))

	var req model.AddMergeRequest
	if err = json.Unmarshal(body, &req); err != nil {
		appLog.Error("unmarshal body error: ", err.Error())
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("invalid request"))
		return
	}

	from, to := req.FromServerId, req.ToServerId
	if from == to {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("from and to cannot be the same"))
		return
	}

	curMap, err := mhs.loadMergeMap()
	if err != nil {
		appLog.Error("load merge map error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

	// 环形检测: 从 to 出发能不能走回 from。
	// 注意 from 自己当前的出边 (curMap[from]) 应当从图中"摘掉", 因为加入新边后该出边将被替换。
	if curMap[from] == to {
		// 重复写入相同映射, 直接视为成功
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("success"))
		return
	}
	delete(curMap, from)

	if hasPath(to, from, curMap) {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("cycle detected"))
		return
	}

	sql := "INSERT INTO `maple_merge_server` (`from_server_id`, `to_server_id`) VALUES (?, ?) ON DUPLICATE KEY UPDATE `to_server_id`=VALUES(`to_server_id`)"
	if _, err = mhs.app.db.Exec(sql, from, to); err != nil {
		appLog.Error("exec merge sql error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("success"))
}

// foldMergeMap: 给定原始 from->to 内存图, 把每条链路折叠到根服 (沿链追溯到没有出边的节点)。
// 例如 raw: {10002:10003, 10003:10001} -> {10002:10001, 10003:10001}
func foldMergeMap(raw map[int]int) map[int]int {
	mergeMap := make(map[int]int, len(raw))
	for from := range raw {
		cur := from
		visited := make(map[int]bool)
		for {
			if visited[cur] {
				// 不应该出现 (addMergeServer 已经做了环形检测), 这里保险起见跳出
				appLog.Errorf("merge chain cycle detected at server_id=%d", cur)
				break
			}
			visited[cur] = true
			next, hasOut := raw[cur]
			if !hasOut {
				mergeMap[from] = cur
				break
			}
			cur = next
		}
	}
	return mergeMap
}

// removeMergeServer: 按主键 from_server_id 删除一条和服映射, 用来修正 addMergeServer 时填错的映射。
//   - 删完之后, 该 from 服在 foldMergeMap 中没有出边, 会被视作根服, 不再出现在折叠后的 merge_map 中;
//   - 不存在的 from_server_id 视为幂等成功 (DELETE 影响 0 行不报错)。
func (mhs *MapleHttpService) removeMergeServer(w http.ResponseWriter, r *http.Request) {
	enableCors(&w)

	if !mhs.handleAuth(w, r) {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("unauthorized"))
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		appLog.Error("read body error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

	appLog.Info("removeMergeServer body: ", string(body))

	var req model.RemoveMergeRequest
	if err = json.Unmarshal(body, &req); err != nil {
		appLog.Error("unmarshal body error: ", err.Error())
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("invalid request"))
		return
	}

	sql := "DELETE FROM `maple_merge_server` WHERE `from_server_id` = ?"
	if _, err = mhs.app.db.Exec(sql, req.FromServerId); err != nil {
		appLog.Error("exec merge delete sql error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("success"))
}

// getAllMergeServer: 返回折叠后的最终映射, 每个 from 都直接指向根服 (沿链追溯到没有出边的节点)。
// 例如 raw: {10002:10003, 10003:10001}
// 输出 merge_map: {10002:10001, 10003:10001}
func (mhs *MapleHttpService) getAllMergeServer(w http.ResponseWriter, r *http.Request) {
	raw, err := mhs.loadMergeMap()
	if err != nil {
		appLog.Error("load merge map error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

	response := model.GetMergeServerResponse{
		MergeMap: foldMergeMap(raw),
	}

	jsonData, err := json.Marshal(response)
	if err != nil {
		appLog.Error("marshal json error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonData)
}

func (mhs *MapleHttpService) start(listenAddr string) {
	http.Handle("/getAllServer", corsMiddleware(http.HandlerFunc(mhs.getAllServer)))
	http.Handle("/getAllZoneData", corsMiddleware(http.HandlerFunc(mhs.getAllZoneData)))
	http.Handle("/import", corsMiddleware(http.HandlerFunc(mhs.handleImport)))
	http.Handle("/export", corsMiddleware(http.HandlerFunc(mhs.handleExport)))
	http.Handle("/addZone", corsMiddleware(http.HandlerFunc(mhs.addZone)))
	http.Handle("/removeZone", corsMiddleware(http.HandlerFunc(mhs.removeZone)))
	http.Handle("/updateZone", corsMiddleware(http.HandlerFunc(mhs.updateZone)))
	http.Handle("/updateServer", corsMiddleware(http.HandlerFunc(mhs.updateServer)))
	http.Handle("/removeServer", corsMiddleware(http.HandlerFunc(mhs.removeServer)))
	http.Handle("/updateKV", corsMiddleware(http.HandlerFunc(mhs.handleUpdateKV)))
	http.Handle("/getAllMergeServer", corsMiddleware(http.HandlerFunc(mhs.getAllMergeServer)))
	http.Handle("/addMergeServer", corsMiddleware(http.HandlerFunc(mhs.addMergeServer)))
	http.Handle("/removeMergeServer", corsMiddleware(http.HandlerFunc(mhs.removeMergeServer)))

	err := http.ListenAndServe(listenAddr, nil)
	if err != nil {
		appLog.Panic("fail to serve at", listenAddr)
	}
}
