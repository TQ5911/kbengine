package MapleApp

import (
	"centralService/src/appLog"
	"centralService/src/maple/model"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strconv"
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

	sql := "SELECT server_id, server_name, zone_id, game_server, queue_server, server_group, server_state, server_flag_state, alias, start_time, central_login FROM `maple`"
	rows, err := mhs.app.db.Query(sql)
	if err != nil {
		appLog.Error("exec sql error: ", err.Error())
	}

	var serverList []model.Server
	for rows.Next() {
		var server model.Server
		err = rows.Scan(&server.Id, &server.ServerName, &server.ZoneId, &server.GameServer, &server.QueueServer, &server.ServerGroup, &server.ServerState, &server.ServerFlagState, &server.Alias, &server.StartTime, &server.CentralLogin)
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

		sql = "INSERT INTO `maple` (`server_id`, `server_name`, `zone_id`, `game_server`, `queue_server`, `server_group`, `server_state`, `server_flag_state`, `alias`, `start_time`, `central_login`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
		if _, err = tx.Exec(sql, server.Id, server.ServerName, server.ZoneId, server.GameServer, server.QueueServer, server.ServerGroup, server.ServerState, server.ServerFlagState, server.Alias, server.StartTime, server.CentralLogin); err != nil {
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

	sql := "SELECT server_id, server_name, zone_id, game_server, queue_server, server_group, server_state, server_flag_state, alias, start_time, central_login FROM `maple`"
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
		if err = rows.Scan(&s.Id, &s.ServerName, &s.ZoneId, &s.GameServer, &s.QueueServer, &s.ServerGroup, &s.ServerState, &s.ServerFlagState, &s.Alias, &s.StartTime, &s.CentralLogin); err != nil {
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
	}

	var server model.Server
	err = json.Unmarshal(body, &server)
	if err != nil {
		appLog.Error("unmarshal body error: ", err.Error())
	}

	// 先判断是否存在
	sql := "SELECT COUNT(*) FROM `maple` WHERE `server_id` = ?"
	var count int
	err = mhs.app.db.QueryRow(sql, server.Id).Scan(&count)
	if err != nil {
		appLog.Error("exec sql error: ", err.Error())
	}

	if count == 0 {
		sql = "INSERT INTO `maple` (`server_id`, `server_name`, `zone_id`, `game_server`, `queue_server`, `server_group`, `server_state`, `server_flag_state`, `alias`, `start_time`, `central_login`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
		_, err = mhs.app.db.Exec(sql, server.Id, server.ServerName, server.ZoneId, server.GameServer, server.QueueServer, server.ServerGroup, server.ServerState, server.ServerFlagState, server.Alias, server.StartTime, server.CentralLogin)
		if err != nil {
			appLog.Error("exec sql error: ", err.Error())
		}

		sql = "INSERT INTO `maple_zone` (`zone_id`, `zone_name`) VALUES (?, ?)"
		_, err = mhs.app.db.Exec(sql, server.ZoneId, server.ZoneName)
		if err != nil {
			appLog.Error("exec sql error: ", err.Error())
		}
	} else {
		sql = "UPDATE `maple` SET `server_name` = ?, `zone_id` = ?, `game_server` = ?, `queue_server` = ?, `server_group` = ?, `server_state` = ?, `server_flag_state` = ?, `alias` = ?, `start_time` = ?, `central_login` = ? WHERE `server_id` = ?"
		_, err = mhs.app.db.Exec(sql, server.ServerName, server.ZoneId, server.GameServer, server.QueueServer, server.ServerGroup, server.ServerState, server.ServerFlagState, server.Alias, server.StartTime, server.CentralLogin, server.Id)
		if err != nil {
			appLog.Error("exec sql error: ", err.Error())
		}
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

// getAllMergeServer: 返回折叠后的最终映射, 每个 from 都直接指向根服 (沿链追溯到没有出边的节点)。
// 例如 raw: {10002:10003, 10003:10001}
// 输出 merge_map: {10002:10001, 10003:10001}
func (mhs *MapleHttpService) getAllMergeServer(w http.ResponseWriter, r *http.Request) {
	enableCors(&w)

	raw, err := mhs.loadMergeMap()
	if err != nil {
		appLog.Error("load merge map error: ", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("internal server error"))
		return
	}

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

	response := model.GetMergeServerResponse{
		MergeMap: mergeMap,
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

	err := http.ListenAndServe(listenAddr, nil)
	if err != nil {
		appLog.Panic("fail to serve at", listenAddr)
	}
}
