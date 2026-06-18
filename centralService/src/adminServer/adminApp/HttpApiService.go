package adminApp

import (
	"bytes"
	gsmanager "centralService/src/adminServer/adminProto/gsmanager"
	webService "centralService/src/adminServer/adminProto/webservice"
	"centralService/src/appLog"
	"crypto/md5"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/garyburd/redigo/redis"
	"github.com/google/uuid"
	"golang.org/x/time/rate"
)

const (
	HTTP_CMD_OK                         int32 = 0
	TARGET_NOT_EXIST                    int32 = 1
	HTTP_CMD_ERR_CMD_SERIAL_EXISTS            = -105
	HTTP_CMD_ERR_INVALD_RESULT          int32 = -200
	HTTP_CMD_ERR_DUMP_JSON              int32 = -201
	HTTP_CMD_ERR_GAME_SERVER_TIMEOUT          = -202
	HTTP_CMD_ERR_PARSE_REQUEST                = -203
	HTTP_CMD_ERR_MISSING_SIGNATURE            = -204
	HTTP_CMD_ERR_INVALID_PARTITION_TYPE       = -205
	HTTP_CMD_ERR_PARTITION_NOT_FOUND          = -206
	HTTP_CMD_ERR_PARSE_BODY                   = -207
	HTTP_CMD_ERR_INVALID_PLATID               = -208
	HTTP_CMD_ERR_INVALID_OPENID               = -209
	HTTP_CMD_ERR_INVALID_UNBAN                = -210
	HTTP_CMD_ERR_UNSUPPORTED_CMD              = -211
	HTTP_CMD_REQUEST_ERR                      = -212
	HTTP_CMD_SIGN_ERR                         int32 = -213
	HTTP_CMD_ARGS_ERR                         int32 = -218
	HTTP_CMD_ARGS_LEN_LIMIT                   int32 = -214
	HTTP_CMD_ERR_INNER                        = -215
	HTTP_CMD_ERR_SERVER                       = -216
	HTTP_CMD_ERR_SERVER_TIMEOUT               = -217
)

type CommandRequest struct {
	Partition int32
	Command   string
	Args      string
	SendTime  uint32
	Seqid     uint64
	SerialNo  string
}

type CommandResponse struct {
	Result int32                  `json:"result"`
	Msg    string                 `json:"msg"`
	Body   map[string]interface{} `json:"body"`
}

func StrToUInt32(str string) uint32 {
	u64, err := strconv.ParseUint(str, 10, 32)
	u32 := uint32(u64)
	if err == nil {
		return u32
	} else {
		appLog.Error("StrToUInt32 error", err, str)
	}
	return 0
}

type HttpCommandService struct {
	app              *AdminApp
	rateLimiter      *rate.Limiter
	idempotencyMap   map[string]*idempotencyEntry    // Stores processed requests for idempotency
	idempotencyMutex sync.RWMutex                    // Protects the idempotency map
	pendingRequests  map[string][]chan *CommandResponse // Tracks pending requests
	pendingMutex     sync.Mutex                      // Protects the pending requests map
}

// 幂等缓存条目：保存成功响应与过期时间
type idempotencyEntry struct {
	resp     *CommandResponse
	expireAt time.Time
}

const (
	// 幂等缓存的默认 TTL：5 分钟，覆盖客户端常见重试窗口
	idempotencyTTL = 5 * time.Minute
	// janitor 周期清理间隔
	idempotencyCleanupInterval = 1 * time.Minute
)

func (self *HttpCommandService) _buildErrResponse(errCode int32, errMsg string) []byte {
	respData := CommandResponse{Result: errCode, Msg: errMsg, Body: nil}
	respData.Body = map[string]interface{}{}
	respBytes, err := json.Marshal(respData)
	if err != nil {
		appLog.Errorf("marshal response err: %s\n", err.Error())
		return nil
	}
	return respBytes
}

func (self *HttpCommandService) sendErrResponse(errCode int32, errMsg string, w http.ResponseWriter) {
	responseBytes := self._buildErrResponse(errCode, errMsg)
	self.sendIDIPResponse(w, 200, responseBytes)
}

func (self *HttpCommandService) buildIDIPResponse(gameserverResponse *gsmanager.HttpAPICommandResponse, req *CommandRequest) []byte {
	tNow := time.Now()
	req.SendTime = uint32(tNow.Year())*1000 + uint32(tNow.Month())*100 + uint32(tNow.Day())

	var cmdResult map[string]interface{}

	if gameserverResponse.Result == HTTP_CMD_OK {
		jsonDecoder := json.NewDecoder(bytes.NewReader(gameserverResponse.Body))
		jsonDecoder.UseNumber()

		err := jsonDecoder.Decode(&cmdResult)

		if err != nil {
			errMsg := fmt.Sprintf("%v, %v", "cannot decode result data", err.Error())
			return self._buildErrResponse(HTTP_CMD_ERR_INVALD_RESULT, errMsg)
		}
	}

	respData := CommandResponse{}
	respData.Result = gameserverResponse.Result
	respData.Msg = gameserverResponse.RetErrMsg
	respData.Body = cmdResult

	appLog.Debugf("buildIDIPResponse: %+v\n", respData)
	respBytes, err := json.Marshal(respData)
	if err != nil {
		errMsg := "cannot decode response data"
		return self._buildErrResponse(HTTP_CMD_ERR_DUMP_JSON, errMsg)
	}
	return respBytes
}

func (self *HttpCommandService) checkRequestSign(dataBytes []byte, signList []string) bool {
	if len(adminConfig.HttpCmdSignKey) == 0 {
		return true
	}
	if len(signList) == 0 {
		return false
	}
	sign := signList[0]
	h := md5.New()
	h.Write(dataBytes)
	h.Write([]byte(adminConfig.HttpCmdSignKey))

	signVal := hex.EncodeToString(h.Sum(nil))
	if strings.ToLower(signVal) == strings.ToLower(sign) {
		return true
	}
	appLog.Errorf("invalid signature:%s %s\n", signVal, sign)
	return false
}

func (self *HttpCommandService) sendIDIPResponse(w http.ResponseWriter, statusCode int, resBytes []byte) {
	if resBytes != nil {
		w.WriteHeader(statusCode)
		headLine := "\n"
		w.Write([]byte(headLine))
		w.Write(resBytes)
	} else {
		w.WriteHeader(500)
		headLine := "\n"
		w.Write([]byte(headLine))
	}
}

func (self *HttpCommandService) handleHttpCmdRequest(w http.ResponseWriter, req *http.Request) {
	if req.Method != "POST" {
		w.WriteHeader(405)
		return
	}

	signStr, ok := req.URL.Query()["sign"]
	if !ok && len(adminConfig.HttpCmdSignKey) > 0 {
		appLog.Error("need signature\n")
		return
	}

	bodyBytes, err := ioutil.ReadAll(io.LimitReader(req.Body, int64(8192)))
	if err != nil && err != io.EOF {
		appLog.Errorf("read body err: %s\n", err.Error())
		return
	}

	if !self.checkRequestSign(bodyBytes, signStr) {
		errMsg := "request sign error"
		responseBytes := self._buildErrResponse(HTTP_CMD_SIGN_ERR, errMsg)
		self.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	reqData := CommandRequest{}
	jsonDecoder := json.NewDecoder(bytes.NewReader(bodyBytes))
	jsonDecoder.UseNumber()

	err = jsonDecoder.Decode(&reqData)
	if err != nil {
		appLog.Errorf("parse request error: %s\n", err.Error())
		w.WriteHeader(400)
		return
	}

	cmdUUID := uuid.New()
	uuidStr := cmdUUID.String()
	appLog.Infof("handleHttpCmdRequest request: %s %+v\n", req.URL.RequestURI(), reqData, uuidStr)

	var responseBytes []byte
	var statusCode int = 200

	sn := reqData.SerialNo
	if sn == "" {
		sn = strconv.FormatUint(reqData.Seqid, 10)
	}

	// 幂等快路径：已处理过且未过期，直接返回缓存响应（避免重复打到下游 game server）
	self.idempotencyMutex.RLock()
	entry, exists := self.idempotencyMap[sn]
	self.idempotencyMutex.RUnlock()

	if exists {
		if time.Now().Before(entry.expireAt) {
			respBytes, _ := json.Marshal(entry.resp)
			self.sendIDIPResponse(w, 200, respBytes)
			return
		}
		// 已过期：懒删除（仅当条目未被并发覆盖时删除）
		self.idempotencyMutex.Lock()
		if cur, ok := self.idempotencyMap[sn]; ok && cur == entry {
			delete(self.idempotencyMap, sn)
		}
		self.idempotencyMutex.Unlock()
	}

	// 主请求的最终响应（非 nil 表示成功，可进缓存）
	var finalResp *CommandResponse
	// 失败时构造的错误响应，仅用于广播给同 sn 的等待方，不进缓存
	var lastErrResp *CommandResponse

	// 同 sn 并发合并：等待方通过 channel 拿主请求的结果
	respChan := make(chan *CommandResponse, 1)

	self.pendingMutex.Lock()
	if pendingChans, exists := self.pendingRequests[sn]; exists {
		// 已有主请求在跑，把自己挂到等待列表
		self.pendingRequests[sn] = append(pendingChans, respChan)
		self.pendingMutex.Unlock()

		// 阻塞等待主请求处理完（无论成功失败都会被通知）
		appLog.Info("Waiting for concurrent request to complete\n")
		resp := <-respChan
		respBytes, _ := json.Marshal(resp)
		self.sendIDIPResponse(w, 200, respBytes)
		return
	}
	// 自己就是主请求，注册 channel 等待列表
	self.pendingRequests[sn] = []chan *CommandResponse{respChan}
	self.pendingMutex.Unlock()

	// 兜底清理 + 广播：无论主请求成功或失败都执行，避免等待方 goroutine 泄漏
	defer func() {
		// 1. 取走并清空 pendingRequests[sn]（无论 finalResp 是否为 nil）
		self.pendingMutex.Lock()
		pendingChans, hasWaiters := self.pendingRequests[sn]
		if hasWaiters {
			delete(self.pendingRequests, sn)
		}
		self.pendingMutex.Unlock()

		if !hasWaiters {
			return
		}

		// 2. 仅成功的 finalResp 才进幂等缓存（错误的响应不应被后续重试命中）
		if finalResp != nil {
			self.idempotencyMutex.Lock()
			self.idempotencyMap[sn] = &idempotencyEntry{
				resp:     finalResp,
				expireAt: time.Now().Add(idempotencyTTL),
			}
			self.idempotencyMutex.Unlock()
		}

		// 3. 决定广播给等待方的响应：成功用 finalResp，失败用 lastErrResp
		var broadcast *CommandResponse
		if finalResp != nil {
			broadcast = finalResp
		} else {
			broadcast = lastErrResp
		}
		if broadcast == nil {
			return
		}

		// 4. 通知所有等待方（包括主请求自己的 channel，发送是非阻塞的因 channel 有缓冲）
		for _, ch := range pendingChans {
			ch <- broadcast
			close(ch)
		}
	}()

	if reqData.Partition != 0 {
		var partition uint32 = 0
		if reqData.Partition < 0 {
			partition = self.app.GetRandomServerId()
			if partition == 0 {
				appLog.Error("handleHttpCmdRequest: partition err:\n", partition, reqData.Partition)
				// 错误：随机选取 server 失败，构造 lastErrResp 给等待方
				errMsg := "cannot get random server"
				responseBytes = self._buildErrResponse(HTTP_CMD_ERR_INNER, errMsg)
				lastErrResp = &CommandResponse{Result: HTTP_CMD_ERR_INNER, Msg: errMsg, Body: map[string]interface{}{}}
				w.WriteHeader(400)
				return
			}
		} else {
			partition = uint32(reqData.Partition)
		}
		serverId := adminConfig.GetNewServerId(partition)

		gameserver := self.app.GetGameServer(uint32(serverId), 0)
		if gameserver == nil {
			appLog.Errorf("invalid serverId: %v %d\n", reqData, serverId)
			errMsg := "partition not found"
			responseBytes = self._buildErrResponse(HTTP_CMD_ERR_PARTITION_NOT_FOUND, errMsg)
			// 同步构造 lastErrResp，避免 defer 中再解析一次
			lastErrResp = &CommandResponse{Result: HTTP_CMD_ERR_PARTITION_NOT_FOUND, Msg: errMsg, Body: map[string]interface{}{}}
			self.sendIDIPResponse(w, 200, responseBytes)
			return
		}

		httpCmd := gsmanager.HttpAPICommand{Uuid: uuidStr, Cmd: reqData.Command, Args: reqData.Args, SeqId: sn}
		respChan := make(chan *gsmanager.HttpAPICommandResponse, 1)
		gameserver.AddPendingHttpCommands(uuidStr, respChan)
		_, err = gameserver.AdminService.GetClientEndPoint().(gsmanager.IGameServerInterface).DoHttpCommand(&httpCmd)
		if err != nil {
			gameserver.RemovePendingHttpCommands(uuidStr)
			appLog.Errorf("invalid request args: %v %s\n", reqData, err.Error())
			// 错误：rpc 调用失败，构造 lastErrResp
			errMsg := "do command failed"
			responseBytes = self._buildErrResponse(HTTP_CMD_ERR_INNER, errMsg)
			lastErrResp = &CommandResponse{Result: HTTP_CMD_ERR_INNER, Msg: errMsg, Body: map[string]interface{}{}}
			w.WriteHeader(500)
			return
		}

		select {
		case response := <-respChan:
			gameserver.RemovePendingHttpCommands(uuidStr)
			if response.Result == HTTP_CMD_ERR_CMD_SERIAL_EXISTS {
				appLog.Errorf("command serial exists: %+v\n", reqData)
			}
			responseBytes = self.buildIDIPResponse(response, &reqData)

			// 把响应字节解析成 CommandResponse 作为 finalResp（用于缓存 + 广播）
			var resp CommandResponse
			if json.Unmarshal(responseBytes, &resp) == nil {
				finalResp = &resp
			}
		case <-time.After(10 * time.Second):
			appLog.Warnf("exec cmd timeout: %v\n", reqData)
			gameserver.RemovePendingHttpCommands(uuidStr)
			errMsg := "game server timeout"
			responseBytes = self._buildErrResponse(HTTP_CMD_ERR_GAME_SERVER_TIMEOUT, errMsg)
			// 超时也算失败：构造 lastErrResp 给等待方，不进缓存
			lastErrResp = &CommandResponse{Result: HTTP_CMD_ERR_GAME_SERVER_TIMEOUT, Msg: errMsg, Body: map[string]interface{}{}}
			statusCode = 400
		}

	} else {
		httpCmd := gsmanager.HttpAPICommand{Uuid: uuidStr, Cmd: reqData.Command, Args: reqData.Args, SeqId: sn}

		for serverId, _ := range self.app.gameServers {
			gameServer := self.app.GetGameServer(uint32(serverId), 0)
			if gameServer == nil {
				appLog.Errorf("handleHttpCmdRequest: invalid serverId: %v %d\n", reqData, serverId)
				continue
			}

			_, err = gameServer.AdminService.GetClientEndPoint().(gsmanager.IGameServerInterface).DoHttpCommand(&httpCmd)
			if err != nil {
				appLog.Errorf("handleHttpCmdRequest: invalid request args DoIDIPCommand: %v %s\n", reqData, err.Error())
				continue
			}
		}
		respData := CommandResponse{}
		respData.Result = HTTP_CMD_OK
		respData.Msg = "success"
		respData.Body = nil

		// Set finalResp for broadcast case
		finalResp = &respData

		respBytes, err := json.Marshal(respData)
		if err != nil {
			appLog.Errorf("handleHttpCmdRequest: encode data err: %s %v\n", err.Error(), respData)
		}
		statusCode, responseBytes = 200, respBytes
	}

	// Store response for idempotency for non-broadcast case (this line should remain empty)

	self.sendIDIPResponse(w, statusCode, responseBytes)
}

func (self *HttpCommandService) handlePlayerHttpCmdRequest(w http.ResponseWriter, req *http.Request) {
	if req.Method != "POST" {
		w.WriteHeader(405)
		return
	}

	signStr, ok := req.URL.Query()["sign"]
	if !ok && len(adminConfig.HttpCmdSignKey) > 0 {
		appLog.Error("need signature\n")
		return
	}

	bodyBytes, err := ioutil.ReadAll(io.LimitReader(req.Body, int64(20480)))
	if err != nil && err != io.EOF {
		appLog.Errorf("read body err: %s\n", err.Error())
		return
	}

	if !self.checkRequestSign(bodyBytes, signStr) {
		errMsg := "request sign error"
		appLog.Infof("handleHttpCmdRequest sign error: %s %v\n", req.URL.RequestURI(), bodyBytes)
		responseBytes := self._buildErrResponse(HTTP_CMD_SIGN_ERR, errMsg)
		self.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	reqData := CommandRequest{}
	jsonDecoder := json.NewDecoder(bytes.NewReader(bodyBytes))
	jsonDecoder.UseNumber()
	err = jsonDecoder.Decode(&reqData)
	if err != nil {
		appLog.Errorf("parse request error: %s %d\n", err.Error())
		w.WriteHeader(400)
		return
	}

	argsBytes, err := hex.DecodeString(reqData.Args)
	if err != nil {
		appLog.Errorf("cannot decode args: %v\n", reqData)
		errMsg := "invalid command args"
		responseBytes := self._buildErrResponse(HTTP_CMD_ARGS_ERR, errMsg)
		self.sendIDIPResponse(w, 200, responseBytes)
		return
	}
	argsStr := string(argsBytes)
	gbIdStr := strings.Split(argsStr, " ")[0]
	playerGbId, err := strconv.ParseUint(gbIdStr, 10, 64)
	if err != nil {
		appLog.Errorf("cannot decode args: %v\n", reqData)
		errMsg := "invalid player id, id should be the first arg"
		responseBytes := self._buildErrResponse(HTTP_CMD_ARGS_ERR, errMsg)
		self.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	cmdUUID := uuid.New()
	uuidStr := cmdUUID.String()
	appLog.Infof("handleHttpCmdRequest request: %s %+v\n", req.URL.RequestURI(), reqData, uuidStr)

	var responseBytes []byte
	var statusCode int = 200
	partition := uint32(playerGbId >> 48)

	serverId := adminConfig.GetNewServerId(partition)

	gameserver := self.app.GetGameServer(uint32(serverId), 0)
	if gameserver == nil {
		appLog.Errorf("invalid serverId: %v %d %d\n", reqData, serverId, playerGbId)
		errMsg := "partition not found"
		responseBytes = self._buildErrResponse(HTTP_CMD_ERR_PARTITION_NOT_FOUND, errMsg)
		self.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	sn := reqData.SerialNo
	if sn == "" {
		sn = strconv.FormatUint(reqData.Seqid, 10)
	}

	httpCmd := gsmanager.HttpAPICommand{Uuid: uuidStr, Cmd: reqData.Command, Args: reqData.Args, SeqId: sn}
	respChan := make(chan *gsmanager.HttpAPICommandResponse, 1)

	gameserver.AddPendingHttpCommands(uuidStr, respChan)
	_, err = gameserver.AdminService.GetClientEndPoint().(gsmanager.IGameServerInterface).DoHttpCommand(&httpCmd)
	if err != nil {
		gameserver.RemovePendingHttpCommands(uuidStr)
		appLog.Errorf("invalid request args: %v %s\n", reqData, err.Error())
		w.WriteHeader(500)
		return
	}

	select {
	case response := <-respChan:
		gameserver.RemovePendingHttpCommands(uuidStr)
		if response.Result == HTTP_CMD_ERR_CMD_SERIAL_EXISTS {
			appLog.Errorf("command serial exists: %+v\n", reqData)
		}
		responseBytes = self.buildIDIPResponse(response, &reqData)
	case <-time.After(10 * time.Second):
		appLog.Warnf("exec cmd timeout: %v\n", reqData)
		gameserver.RemovePendingHttpCommands(uuidStr)
		errMsg := "game server timeout"
		responseBytes = self._buildErrResponse(HTTP_CMD_ERR_GAME_SERVER_TIMEOUT, errMsg)
		statusCode = 400
	}

	// Store response for idempotency if valid JSON
	if responseBytes != nil {
		var resp CommandResponse
		if err := json.Unmarshal(responseBytes, &resp); err == nil {
			self.idempotencyMutex.Lock()
			self.idempotencyMap[sn] = &idempotencyEntry{
				resp:     &resp,
				expireAt: time.Now().Add(idempotencyTTL),
			}
			self.idempotencyMutex.Unlock()
		}
	}

	self.sendIDIPResponse(w, statusCode, responseBytes)
}

func (self *HttpCommandService) handlerTransferAvatarData(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	var serverId = strings.Join(r.Form["serverId"], "")
	var t = strings.Join(r.Form["t"], "")
	var playerName = strings.Join(r.Form["playerName"], "")
	var sign = strings.Join(r.Form["sign"], "")

	signString := t + playerName + adminConfig.TransferAvatarSignSecret
	has := md5.Sum([]byte(signString))
	checkSign := fmt.Sprintf("%x", has)

	appLog.Debug("handlerTransferAvatarData", serverId, t, sign, playerName, checkSign)
	if sign != checkSign {
		appLog.Error("check sign fail")
		fmt.Fprintf(w, "FAIL")
		return
	}
	buf, err := ioutil.ReadAll(r.Body)
	if err != nil {
		appLog.Error("handlerTransferAvatarData fail", err)
		fmt.Fprintf(w, "FAIL")
		return
	}
	encoded := base64.StdEncoding.EncodeToString(buf)
	go func() {
		_, err := self.app.GmtService.DoCommand(nil, &webService.CommandInfo{Acount: "snail", ServerId: StrToUInt32(serverId), Command: "$importAvatarData " + playerName + " " + encoded})
		if err != nil {
			appLog.Error("docmd:", err)
			return
		}
	}()
	fmt.Fprintf(w, "SUCCESS")
}

func (self *HttpCommandService) handleAccountHttpCmdRequest(w http.ResponseWriter, req *http.Request) {
	if req.Method != "POST" {
		w.WriteHeader(405)
		return
	}

	signStr, ok := req.URL.Query()["sign"]
	if !ok && len(adminConfig.HttpCmdSignKey) > 0 {
		appLog.Error("need signature\n")
		return
	}

	bodyBytes, err := ioutil.ReadAll(io.LimitReader(req.Body, int64(4096)))
	if err != nil && err != io.EOF {
		appLog.Errorf("read body err: %s\n", err.Error())
		return
	}

	if !self.checkRequestSign(bodyBytes, signStr) {
		errMsg := "request sign error"
		appLog.Infof("handleAccountHttpCmdRequest sign error: %s %v\n", req.URL.RequestURI(), bodyBytes)
		responseBytes := self._buildErrResponse(HTTP_CMD_SIGN_ERR, errMsg)
		self.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	reqData := CommandRequest{}
	jsonDecoder := json.NewDecoder(bytes.NewReader(bodyBytes))
	jsonDecoder.UseNumber()

	err = jsonDecoder.Decode(&reqData)
	if err != nil {
		appLog.Errorf("parse request error: %s\n", err.Error())
		w.WriteHeader(400)
		return
	}

	cmdUUID := uuid.New()
	uuidStr := cmdUUID.String()
	appLog.Infof("handleAccountHttpCmdRequest request: %s %+v\n", req.URL.RequestURI(), reqData, uuidStr)

	var responseBytes []byte
	var statusCode int = 200

	sn := reqData.SerialNo
	if sn == "" {
		sn = strconv.FormatUint(reqData.Seqid, 10)
	}

	if reqData.Partition > 0 {
		partition := uint32(reqData.Partition)
		serverId := adminConfig.GetNewServerId(partition)

		gameserver := self.app.GetGameServer(uint32(serverId), 0)
		if gameserver == nil {
			appLog.Errorf("invalid serverId: %v %d\n", reqData, serverId)
			errMsg := "partition not found"
			responseBytes = self._buildErrResponse(HTTP_CMD_ERR_PARTITION_NOT_FOUND, errMsg)
			self.sendIDIPResponse(w, 200, responseBytes)
			return
		}

		httpCmd := gsmanager.HttpAPICommand{Uuid: uuidStr, Cmd: reqData.Command, Args: reqData.Args, SeqId: sn}
		respChan := make(chan *gsmanager.HttpAPICommandResponse, 1)
		gameserver.AddPendingHttpCommands(uuidStr, respChan)

		_, err = gameserver.AdminService.GetClientEndPoint().(gsmanager.IGameServerInterface).DoHttpCommand(&httpCmd)
		if err != nil {
			gameserver.RemovePendingHttpCommands(uuidStr)
			appLog.Errorf("invalid request args: %v %s\n", reqData, err.Error())
			w.WriteHeader(500)
			return
		}

		select {
		case response := <-respChan:

			delete(gameserver.PendingHttpCommands, uuidStr)

			if response.Result == HTTP_CMD_ERR_CMD_SERIAL_EXISTS {
				appLog.Errorf("command serial exists: %+v\n", reqData)
			}
			responseBytes = self.buildIDIPResponse(response, &reqData)
		case <-time.After(10 * time.Second):
			appLog.Warnf("exec cmd timeout: %v\n", reqData)

			if _, ok = gameserver.PendingHttpCommands[uuidStr]; ok {

				delete(gameserver.PendingHttpCommands, uuidStr)

			}

			errMsg := "game server timeout"
			responseBytes = self._buildErrResponse(HTTP_CMD_ERR_GAME_SERVER_TIMEOUT, errMsg)
			statusCode = 400
		}
		self.sendIDIPResponse(w, statusCode, responseBytes)
	} else {
		httpCmd := gsmanager.HttpAPICommand{Uuid: uuidStr, Cmd: reqData.Command, Args: reqData.Args, SeqId: sn}

		respChan := make(chan *gsmanager.HttpAPICommandResponse, 1)

		self.app.AddPendingAccountCommands(uuidStr, respChan)
		self.app.rwLockGameServers.RLock()
		defer self.app.rwLockGameServers.RUnlock()
		for serverId, _ := range self.app.gameServers {
			gameserver := self.app.GetGameServer(uint32(serverId), 0)
			if gameserver == nil {
				appLog.Errorf("handleHttpCmdRequest: invalid serverId: %v %d\n", reqData, serverId)
				continue
			}

			_, err = gameserver.AdminService.GetClientEndPoint().(gsmanager.IGameServerInterface).DoHttpCommand(&httpCmd)
			if err != nil {
				appLog.Errorf("handleHttpCmdRequest: invalid request args DoIDIPCommand: %v %s\n", reqData, err.Error())
				continue
			}
		}

		select {
		case response := <-respChan:
			self.app.RemovePendingAccountCommands(uuidStr)
			if response.Result == HTTP_CMD_ERR_CMD_SERIAL_EXISTS {
				appLog.Errorf("command serial exists: %+v\n", reqData)
			}
			responseBytes = self.buildIDIPResponse(response, &reqData)
			self.sendIDIPResponse(w, statusCode, responseBytes)
			return
		case <-time.After(10 * time.Second):
			self.app.RemovePendingAccountCommands(uuidStr)
			responseBytes = self._buildErrResponse(HTTP_CMD_ERR_GAME_SERVER_TIMEOUT, "game server timeout")
			statusCode = 400
			self.sendIDIPResponse(w, statusCode, responseBytes)
			return
		}
	}
}

func (self *HttpCommandService) handleQueryRoleId(w http.ResponseWriter, req *http.Request) {
	if req.Method != "POST" {
		w.WriteHeader(405)
		return
	}

	signStr, ok := req.URL.Query()["sign"]
	if !ok && len(adminConfig.HttpCmdSignKey) > 0 {
		appLog.Errorf("need signature\n")
		return
	}

	bodyBytes, err := ioutil.ReadAll(io.LimitReader(req.Body, int64(8192)))
	if err != nil && err != io.EOF {
		appLog.Errorf("read body err: %s\n", err.Error())
		return
	}

	if !self.checkRequestSign(bodyBytes, signStr) {
		errMsg := "request sign error"
		responseBytes := self._buildErrResponse(HTTP_CMD_SIGN_ERR, errMsg)
		self.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	reqData := CommandRequest{}
	jsonDecoder := json.NewDecoder(bytes.NewReader(bodyBytes))
	jsonDecoder.UseNumber()

	err = jsonDecoder.Decode(&reqData)
	if err != nil {
		appLog.Errorf("parse request error: %s\n", err.Error())
		w.WriteHeader(400)
		return
	}

	conn := self.app.redisPool.Get()
	defer conn.Close()

	argsBytes, err := hex.DecodeString(reqData.Args)
	if err != nil {
		appLog.Errorf("cannot decode args: %v\n", reqData)
		errMsg := "invalid command args"
		responseBytes := self._buildErrResponse(HTTP_CMD_ARGS_ERR, errMsg)
		self.sendIDIPResponse(w, 200, responseBytes)
		return
	}
	argsStr := string(argsBytes)
	argsArr := strings.Split(argsStr, " ")
	tmpArgs := make([]interface{}, 1)
	tmpArgs[0] = "__LOGIN_ACCOUNT_GBID_KEY__"
	for _, arg := range argsArr {
		tmpArgs = append(tmpArgs, arg)
	}
	appLog.Infof("handleQueryRoleId argsStr: %v\n", tmpArgs)

	retsArr, err := redis.Strings(conn.Do("hmget", tmpArgs...))
	if err != nil {
		appLog.Errorf("handleQueryRoleId hmget err: %s\n", err.Error())
		w.WriteHeader(400)
		return
	}
	appLog.Infof("handleQueryRoleId hmget result: %v\n", retsArr)

	retsMap := make(map[string]interface{}, len(argsArr))
	for index, arg := range argsArr {
		if retsArr[index] != "" {
			retsMap[arg] = retsArr[index]
		}
	}

	respData := CommandResponse{}
	respData.Result = 0
	respData.Msg = ""
	respData.Body = retsMap
	respBytes, err := json.Marshal(respData)
	if err != nil {
		errMsg := "cannot decode response data"
		self._buildErrResponse(HTTP_CMD_ERR_DUMP_JSON, errMsg)
	}
	self.sendIDIPResponse(w, 200, respBytes)
}

func (self *HttpCommandService) revertMallSkuInfoRedis(skuId string, conn redis.Conn) {
	_, err := redis.Int(conn.Do("hdel", "__MALL_SKU_INFO_KEY__", skuId))
	if err != nil {
		appLog.Error("sync server failed, revert redis failed", skuId)
	}
}

func (self *HttpCommandService) cleanMallSkuLockRedis(skuLockKey string, conn redis.Conn) {
	_, err := redis.Int(conn.Do("del", skuLockKey))
	if err != nil {
		appLog.Error("cleanMallSkuLockRedis failed", skuLockKey)
	}
}

func (self *HttpCommandService) handleHttpAddSkuIdRequest(w http.ResponseWriter, req *http.Request) {
	if req.Method != "POST" {
		w.WriteHeader(405)
		return
	}

	signStr, ok := req.URL.Query()["sign"]
	if !ok && len(adminConfig.HttpCmdSignKey) > 0 {
		appLog.Error("need signature\n")
		return
	}

	bodyBytes, err := ioutil.ReadAll(io.LimitReader(req.Body, int64(512)))
	if err != nil && err != io.EOF {
		appLog.Errorf("read body err: %s\n", err.Error())
		return
	}

	if !self.checkRequestSign(bodyBytes, signStr) {
		self.sendErrResponse(HTTP_CMD_SIGN_ERR, "request sign error", w)
		return
	}

	if !self.rateLimiter.Allow() {
		appLog.Error("!!handleHttpAddSkuIdRequest rate limit up")
		w.WriteHeader(406)
		return
	}

	reqData := CommandRequest{}
	jsonDecoder := json.NewDecoder(bytes.NewReader(bodyBytes))
	jsonDecoder.UseNumber()

	err = jsonDecoder.Decode(&reqData)
	if err != nil {
		appLog.Errorf("parse request error: %s\n", err.Error())
		w.WriteHeader(400)
		return
	}

	conn := self.app.redisPool.Get()
	defer conn.Close()

	argsBytes, err := hex.DecodeString(reqData.Args)
	if err != nil {
		appLog.Errorf("cannot decode args: %v\n", reqData)
		self.sendErrResponse(HTTP_CMD_ARGS_ERR, "invalid command args", w)
		return
	}
	argsStr := string(argsBytes)
	argsArr := strings.Split(argsStr, " ")
	skuId := argsArr[0]
	proportion := argsArr[2]
	proportionArr := strings.Split(proportion, ":")
	inta, err := strconv.Atoi(proportionArr[1])
	if err != nil {
		appLog.Errorf("args err:%s, %v\n", argsStr, err.Error())
		self.sendErrResponse(HTTP_CMD_ARGS_ERR, "invalid command args", w)
		return
	}
	intb, err := strconv.Atoi(proportionArr[0])
	if err != nil {
		appLog.Errorf("args err:%s, %v\n", argsStr, err.Error())
		self.sendErrResponse(HTTP_CMD_ARGS_ERR, "invalid command args", w)
		return
	}
	var proportionF float64
	if intb == 0 || inta == 0 {
		proportionF = float64(0)
	} else {
		proportionF = float64(int((float64(inta)/float64(intb))*10000)) / 10000
	}

	cmdUUID := uuid.New()
	uuidStr := cmdUUID.String()
	appLog.Infof("handleHttpAddSkuIdRequest request: %s %v %s %v\n", req.URL.RequestURI(), proportionF, uuidStr, reqData)

	lockKey := fmt.Sprintf("__LOCK_SKU_KEY__:%s", skuId)
	_, err = redis.String(conn.Do("set", lockKey, 1, "nx", "ex", 35))
	if err != nil {
		appLog.Error("add SKU Lock failed", skuId, err.Error())
		self.sendErrResponse(HTTP_CMD_ARGS_ERR, "locking", w)
		return
	}

	defer self.cleanMallSkuLockRedis(lockKey, conn)
	n, err := redis.Int(conn.Do("hsetnx", "__MALL_SKU_INFO_KEY__", skuId, proportionF))
	if err != nil {
		appLog.Error("add __MALL_SKU_INFO_KEY__ failed", skuId, proportionF, err.Error())
		self.sendErrResponse(HTTP_CMD_ERR_INNER, "add cache error", w)
		return
	}

	if n == 0 {
		respData := CommandResponse{Result: HTTP_CMD_OK, Msg: "", Body: nil}
		respData.Body = map[string]interface{}{}
		respBytes, err := json.Marshal(respData)
		if err != nil {
			appLog.Errorf("marshal response err: %s\n", err.Error())
			self.sendErrResponse(HTTP_CMD_ERR_INNER, "json err", w)
			return
		}
		self.sendIDIPResponse(w, 200, respBytes)
		return
	}

	var responseBytes []byte
	var statusCode int = 200

	sn := reqData.SerialNo
	if sn == "" {
		sn = strconv.FormatUint(reqData.Seqid, 10)
	}

	num := self.app.calcAllValidServers()
	httpCmd := gsmanager.HttpAPICommand{Uuid: uuidStr, Cmd: reqData.Command, Args: reqData.Args, SeqId: sn}
	respChan := make(chan *gsmanager.HttpAPICommandResponse, num)

	self.app.rwLockGameServers.RLock()
	defer self.app.rwLockGameServers.RUnlock()
	for serverId, gameServerMap := range self.app.gameServers {
		for compId, gameServer := range gameServerMap {
			if gameServer != nil {
				gameServer.AddPendingAllHttpCmds(uuidStr, respChan)

				_, err = gameServer.AdminService.GetClientEndPoint().(gsmanager.IGameServerInterface).DoHttpCommand(&httpCmd)
				if err != nil {

					self.revertMallSkuInfoRedis(skuId, conn)
					self.sendErrResponse(HTTP_CMD_ERR_INNER, "do cmd failed", w)
					appLog.Errorf("handleHttpAddSkuIdRequest: invalid server: %v %d %d\n", reqData, serverId, compId)

					self.app.clearHttpCommands(uuidStr)
					return
				}
			}
		}
	}

	respData := CommandResponse{}
	for num > 0 {
		select {
		case response := <-respChan:
			if response.Result != 0 {
				appLog.Errorf("handleHttpAddSkuIdRequest: server err:  %v\n", response)
				respData.Result = response.Result
				respData.Msg = response.RetErrMsg
				goto OUT_LOOP
			}
			num -= 1
		case <-time.After(30 * time.Second):
			respData.Result = HTTP_CMD_ERR_SERVER_TIMEOUT
			respData.Msg = "timeout"
			goto OUT_LOOP
		}
	}

OUT_LOOP:
	self.app.clearHttpCommands(uuidStr)

	if num == 0 {
		respData.Result = HTTP_CMD_OK
		respData.Msg = "success"
		respData.Body = nil
	} else {
		respData.Body = nil
		appLog.Errorf("handleHttpAddSkuIdRequest: revertMallSkuInfoRedis %s\n", num)
		self.revertMallSkuInfoRedis(skuId, conn)
	}

	respBytes, err := json.Marshal(respData)
	if err != nil {
		appLog.Errorf("handleHttpAddSkuIdRequest: encode data err: %s %v\n", err.Error(), respData)
		self.revertMallSkuInfoRedis(skuId, conn)

		errMsg := "json err"
		responseBytes := self._buildErrResponse(HTTP_CMD_ERR_DUMP_JSON, errMsg)
		self.sendIDIPResponse(w, 200, responseBytes)
		return
	}
	statusCode, responseBytes = 200, respBytes
	self.sendIDIPResponse(w, statusCode, responseBytes)
}

// 周期清理过期的幂等缓存条目，防止长期运行内存无界增长
func (self *HttpCommandService) idempotencyJanitor(interval time.Duration) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()
	for range ticker.C {
		now := time.Now()
		// 扫描并删除已过期的条目
		self.idempotencyMutex.Lock()
		for k, v := range self.idempotencyMap {
			if now.After(v.expireAt) {
				delete(self.idempotencyMap, k)
			}
		}
		self.idempotencyMutex.Unlock()
	}
}

// CORS middleware to add appropriate headers to HTTP responses
func (self *HttpCommandService) corsMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// Allow all origins (can restrict to specific domains if needed)
		w.Header().Set("Access-Control-Allow-Origin", "*")
		// Allow POST and OPTIONS methods (OPTIONS is used for preflight requests)
		w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
		// Allow Content-Type header
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		// Handle preflight OPTIONS requests immediately
		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		// Call the original handler
		next(w, r)
	}
}

func (self *HttpCommandService) startHttpApiServer(listenAddr string) {
	// 启动幂等缓存周期清理协程，扫描并删除已过期的条目，避免长期运行内存膨胀
	go self.idempotencyJanitor(idempotencyCleanupInterval)

	// Wrap all handlers with CORS middleware
	http.HandleFunc("/docmd", self.corsMiddleware(self.handleHttpCmdRequest))
	http.HandleFunc("/doPlayerCmd", self.corsMiddleware(self.handlePlayerHttpCmdRequest))
	http.HandleFunc("/transferAvatarData", self.corsMiddleware(self.handlerTransferAvatarData))
	// http.HandleFunc("/apiNeteaseMusic/redirect", self.corsMiddleware(self.handlerNeteaseMusicRedirect))
	http.HandleFunc("/doAccountCmd", self.corsMiddleware(self.handleAccountHttpCmdRequest))
	http.HandleFunc("/queryRoleId", self.corsMiddleware(self.handleQueryRoleId))
	http.HandleFunc("/doAllCmd", self.corsMiddleware(self.handleHttpAddSkuIdRequest)) //仅支持skuId设置
	err := http.ListenAndServe(listenAddr, nil)
	if err != nil {
		appLog.Error("fail to serve at", listenAddr)
	}
}
