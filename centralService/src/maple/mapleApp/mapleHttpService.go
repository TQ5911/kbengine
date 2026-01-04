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

		// 0 是隐藏状态
		if server.ServerState == 0 {
			continue
		}

		server.ZoneName = zoneMap[uint32(server.ZoneId)]
		serverList = append(serverList, server)
	}

	kvMap := mhs.getAllKV()

	response := model.GetAllServerResponse{
		Servers: serverList,
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

func (mhs *MapleHttpService) start(listenAddr string) {
    http.Handle("/getAllServer", corsMiddleware(http.HandlerFunc(mhs.getAllServer)))
    http.Handle("/getAllZoneData", corsMiddleware(http.HandlerFunc(mhs.getAllZoneData)))
    http.Handle("/import", corsMiddleware(http.HandlerFunc(mhs.handleImport)))
    http.Handle("/export", corsMiddleware(http.HandlerFunc(mhs.handleExport)))
    http.Handle("/addZone", corsMiddleware(http.HandlerFunc(mhs.addZone)))
    http.Handle("/updateServer", corsMiddleware(http.HandlerFunc(mhs.updateServer)))
    http.Handle("/removeServer", corsMiddleware(http.HandlerFunc(mhs.removeServer)))
    http.Handle("/updateKV", corsMiddleware(http.HandlerFunc(mhs.handleUpdateKV)))

	err := http.ListenAndServe(listenAddr, nil)
	if err != nil {
		appLog.Panic("fail to serve at", listenAddr)
	}
}
