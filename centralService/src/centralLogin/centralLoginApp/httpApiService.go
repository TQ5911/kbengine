package CentralLogin

import (
	"bytes"
	"centralService/src/appLog"
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"slices"

	//"os"
	"strconv"
	"strings"
	"time"

	//"golang.org/x/sys/unix"
	"centralService/src/common"

	"github.com/garyburd/redigo/redis"
	"github.com/gogf/greuse"
)

type IDIPResponse struct {
	Uuid      []byte `json:"uuid,omitempty"`
	Result    int32  `json:"result,omitempty"`
	RetErrMsg string `json:"retErrMsg,omitempty"`
	Body      []byte `json:"body,omitempty"`
}

type IDIPBanAccountBody struct {
	Result    uint32
	RetMsg    string
	BeginTime int64
	EndTime   int64
	BanTime   int32
}

type IDIPDelAccountBody struct {
	Result uint8
	RetMsg string
}

type IDIPQeuryAccountLastLogin struct {
	Result    uint8
	RetMsg    string
	LoginTime uint32
}

const IDIP_AQ_DO_ALL_SERVER_BAN_ACCOUNT_REQ int = 4163
const IDIP_AQ_DO_ALL_SERVER_BAN_POST_REQ int = 4167

type HttpService struct {
	app *CentralLoginApp
}

func (self *HttpService) handleIDIPUnBanRequest(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	var openId = strings.Join(r.Form["openId"], "")
	var platId = strings.Join(r.Form["platId"], "")
	var unBanAllAccount = strings.Join(r.Form["unBanAllAccount"], "")
	var unBanAllPost = strings.Join(r.Form["unBanAllPost"], "")
	appLog.Debug("handleIDIPUnBanRequest", openId, platId, unBanAllAccount, unBanAllPost)

	iPlatId, err := strconv.Atoi(platId)
	if err != nil {
		appLog.Error("handleIDIPRequest parse platId error", err)
		w.WriteHeader(405)
		return
	}

	iUnBanAllAccount, err := strconv.Atoi(unBanAllAccount)
	if err != nil {
		appLog.Error("handleIDIPRequest parse unBanAllAccount error", err)
		w.WriteHeader(405)
		return
	}
	iUnBanAllPost, err := strconv.Atoi(unBanAllPost)
	if err != nil {
		appLog.Error("handleIDIPRequest parse unBanAllPost error", err)
		w.WriteHeader(405)
		return
	}

	accountType := common.GetAccoutType(int8(iPlatId))

	if iUnBanAllAccount == 1 {
		sql := "update account set banAccountTime=?, banAccountReason=? where accountType=? and accountName=?"
		_, err := self.app.db.Exec(sql, 0, "", accountType, openId)
		if err != nil {
			appLog.Error("update account banAccountTime err: ", accountType, openId, err.Error())
			w.WriteHeader(405)
			return
		}
	}

	if iUnBanAllPost == 1 {
		sql := "update account set banPostTime=?, banPostReason=? where accountType=? and accountName=?"
		_, err := self.app.db.Exec(sql, 0, "", accountType, openId)
		if err != nil {
			appLog.Error("update account banPostTime err: ", accountType, openId, err.Error())
			w.WriteHeader(405)
			return
		}
	}

	w.WriteHeader(http.StatusOK)
	appLog.Info("handleIDIPUnBanRequest ok", openId, platId, unBanAllAccount, unBanAllPost)
	return
}

func (self *HttpService) handleIDIPBanRequest(w http.ResponseWriter, r *http.Request) {
	appLog.Debug("handleIDIPBanRequest")
	if r.Method != "POST" {
		w.WriteHeader(405)
		return
	}

	r.ParseForm()
	var CmdId = strings.Join(r.Form["CmdId"], "")
	cmdId, err := strconv.Atoi(CmdId)
	if err != nil {
		appLog.Error("handleIDIPRequest parse cmdid error", err)
		w.WriteHeader(405)
		return
	}

	var bodyData map[string]interface{}
	bodyBytes, err := ioutil.ReadAll(r.Body)
	if err != nil {
		appLog.Error("handleIDIPRequest parse r.Body error")
		w.WriteHeader(405)
		return
	}
	err = json.Unmarshal(bodyBytes, &bodyData)
	if err != nil {
		appLog.Errorf("handleIDIPRequest json Unmarshal error:%v\n", err)
		w.WriteHeader(405)
		return
	}

	tNow := time.Now().Unix()
	appLog.Debug("handleIDIPRequest bodyData", bodyData)
	switch cmdId {
	case IDIP_AQ_DO_ALL_SERVER_BAN_ACCOUNT_REQ:
		openId := bodyData["OpenId"]
		platId := int8(bodyData["PlatId"].(float64))
		accountType := common.GetAccoutType(platId)
		banTime := int64(bodyData["BanTime"].(float64))
		banReason := bodyData["BanReason"]
		var banEndTime int64 = -1
		if banTime != -1 {
			banEndTime = banTime + tNow
		}

		sql := "update account set banAccountTime=?, banAccountReason=? where accountType=? and accountName=?"
		_, err := self.app.db.Exec(sql, banEndTime, banReason, accountType, openId)
		if err != nil {
			appLog.Error("update account banAccountTime err: ", banEndTime, banReason, accountType, openId, err.Error())
			w.WriteHeader(405)
			return
		}
		resBody := IDIPBanAccountBody{}
		resBody.Result = 0
		resBody.RetMsg = ""
		resBody.BeginTime = tNow
		resBody.EndTime = banEndTime
		resBody.BanTime = int32(banTime)

		resBodyData, err := json.Marshal(resBody)
		if err != nil {
			appLog.Error("json userInfo failed", err.Error())
			w.WriteHeader(405)
			return
		}
		appLog.Debug("handleIDIPRequest resBody", resBody)

		response := IDIPResponse{}
		response.Result = 0
		response.RetErrMsg = ""
		response.Body = resBodyData
		data, err := json.Marshal(response)
		if err != nil {
			appLog.Error("json userInfo failed", err.Error())
			w.WriteHeader(405)
			return
		}
		fmt.Fprintf(w, string(data))
		break
	case IDIP_AQ_DO_ALL_SERVER_BAN_POST_REQ:
		openId := bodyData["OpenId"]
		platId := int8(bodyData["PlatId"].(float64))
		accountType := common.GetAccoutType(platId)
		banTime := int64(bodyData["BanTime"].(float64))
		banReason := bodyData["BanReason"]
		var banEndTime int64 = -1
		if banTime != -1 {
			banEndTime = banTime + tNow
		}

		sql := "update account set banPostTime=?, banPostReason=? where accountType=? and accountName=?"
		_, err := self.app.db.Exec(sql, banEndTime, banReason, accountType, openId)
		if err != nil {
			appLog.Error("update account banPostTime err: ", banEndTime, banReason, accountType, openId, err.Error())
			w.WriteHeader(405)
			return
		}
		resBody := IDIPBanAccountBody{}
		resBody.Result = 0
		resBody.RetMsg = ""
		resBody.BeginTime = tNow
		resBody.EndTime = banEndTime
		resBody.BanTime = int32(banTime)

		resBodyData, err := json.Marshal(resBody)
		if err != nil {
			appLog.Error("json userInfo failed", err.Error())
			w.WriteHeader(405)
			return
		}
		appLog.Debug("handleIDIPRequest resBody", resBody)

		response := IDIPResponse{}
		response.Result = 0
		response.RetErrMsg = ""
		response.Body = resBodyData
		data, err := json.Marshal(response)
		if err != nil {
			appLog.Error("json userInfo failed", err.Error())
			w.WriteHeader(405)
			return
		}
		fmt.Fprintf(w, string(data))
		break
	default:
		break
	}
}

func (self *HttpService) handleIDIPDelAccount(w http.ResponseWriter, r *http.Request) {
	appLog.Debug("handleIDIPDelAccount")
	if r.Method != "GET" {
		w.WriteHeader(405)
		return
	}

	err := r.ParseForm()
	if err != nil {
		appLog.Error("handleIDIPRequest parse handleIDIPDelAccount reqeust error", err)
		w.WriteHeader(405)
		return
	}

	accountTypeStr := strings.Join(r.Form["accType"], "")
	accountType, err := strconv.Atoi(accountTypeStr)
	if err != nil {
		appLog.Error("handleIDIPRequest parse handleIDIPDelAccount reqeust error, invalid accoutType", err, accountTypeStr)
		w.WriteHeader(405)
		return
	}
	accountGOpenID := strings.Join(r.Form["account"], "")
	resCode, err := self.app.delAccountByGOpenID(accountType, accountGOpenID)

	resBody := IDIPDelAccountBody{}
	resBody.Result = resCode
	resBody.RetMsg = ""

	resBodyData, err := json.Marshal(resBody)
	if err != nil {
		appLog.Error("handleIDIPDelAccount json userInfo failed", err.Error())
		w.WriteHeader(405)
		return
	}

	response := IDIPResponse{}
	response.Result = 0
	response.RetErrMsg = ""
	response.Body = resBodyData
	data, err := json.Marshal(response)
	if err != nil {
		appLog.Error("handleIDIPDelAccount json response failed", err.Error())
		w.WriteHeader(405)
		return
	}
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, string(data))
}

func (self *HttpService) handleIDIPQueryLastLogin(w http.ResponseWriter, r *http.Request) {
	appLog.Debug("handleIDIPQueryLastLogin")
	if r.Method != "GET" {
		w.WriteHeader(405)
		return
	}

	err := r.ParseForm()
	if err != nil {
		appLog.Error("handleIDIPRequest parse handleIDIPDelAccount reqeust error", err)
		w.WriteHeader(405)
		return
	}

	accountTypeStr := strings.Join(r.Form["accType"], "")
	accountType, err := strconv.Atoi(accountTypeStr)
	if err != nil {
		appLog.Error("handleIDIPRequest parse handleIDIPDelAccount reqeust error, invalid accoutType", err, accountTypeStr)
		w.WriteHeader(405)
		return
	}
	accountGOpenID := strings.Join(r.Form["account"], "")
	resCode, tLastLogin, err := self.app.queryAccountLastLogin(accountType, accountGOpenID)

	resBody := IDIPQeuryAccountLastLogin{}
	resBody.Result = resCode
	resBody.RetMsg = ""
	resBody.LoginTime = tLastLogin

	resBodyData, err := json.Marshal(resBody)
	if err != nil {
		appLog.Error("handleIDIPDelAccount json userInfo failed", err.Error())
		w.WriteHeader(405)
		return
	}

	response := IDIPResponse{}
	response.Result = 0
	response.RetErrMsg = ""
	response.Body = resBodyData
	data, err := json.Marshal(response)
	if err != nil {
		appLog.Error("handleIDIPDelAccount json response failed", err.Error())
		w.WriteHeader(405)
		return
	}
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, string(data))
}

func (self *HttpService) queryAccountServers(w http.ResponseWriter, r *http.Request) {
	appLog.Debug("queryAccountServers")
	if r.Method != "GET" {
		w.WriteHeader(405)
		return
	}

	err := r.ParseForm()
	if err != nil {
		appLog.Error("handleIDIPRequest parse queryAccountServers reqeust error", err)
		w.WriteHeader(405)
		return
	}

	accountTypeStr := strings.Join(r.Form["accType"], "")
	accountType, err := strconv.Atoi(accountTypeStr)
	if err != nil {
		appLog.Error("handleIDIPRequest parse queryAccountServers reqeust error, invalid accoutType", err, accountTypeStr)
		w.WriteHeader(405)
		return
	}
	accountGOpenID := strings.Join(r.Form["account"], "")
	resCode, servers, err := self.app.queryAccountServers(accountType, accountGOpenID)
	if err != nil {
		appLog.Error("handleIDIPRequest parse queryAccountServers reqeust error", err, accountTypeStr, resCode)
		w.WriteHeader(405)
		return
	}

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, servers)
}

type ActivationCodeReply struct {
	IsSuccess bool   `json:"isSuccess"`
	TagType   string `json:"tagType"`
	Code      int    `json:"code"`
}

type ActivationCodeData struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

const (
	ActivationCodeInvalid      int = 40001
	ActivationCodeExpired      int = 40002
	ActivationCodeUsed         int = 40003
	ActivationCodeMultipleUsed int = 429
	UnknownError               int = 500
)

func (self *HttpService) replyActivationCode(w http.ResponseWriter, isSuccess bool, tagType string, code int) {
	response := ActivationCodeReply{}
	response.IsSuccess = isSuccess
	response.TagType = tagType
	response.Code = code
	data, err := json.Marshal(response)
	if err != nil {
		appLog.Error("replyActivationCode json response failed", err.Error())
		w.WriteHeader(405)
		return
	}
	fmt.Fprintf(w, string(data))
}

func getCodeType(code string) string {
	mapCode := map[string]string{
		"INV": "2",
		"SP":  "3",
	}
	for k, v := range mapCode {
		if strings.HasPrefix(code, k) {
			return v
		}
	}
	return ""
}

func (self *HttpService) setRedisOfficialTagType(gameId string, code string) string {
	codeType := getCodeType(code)
	if codeType == "" {
		return ""
	}
	conn := self.app.redisPool.Get()
	defer conn.Close()
	officialTagType, err := redis.String(conn.Do("get", "officialTagType_"+gameId))
	if err != nil {
		appLog.Error("setRedisOfficialTagType get redis failed", err.Error())
		return ""
	}
	tagList := strings.Split(officialTagType, ",")
	if !slices.Contains(tagList, codeType) {
		tagList = append(tagList, codeType)
		redis.String(conn.Do("set", "officialTagType_"+gameId, strings.Join(tagList, ",")))
		appLog.Info("setRedisOfficialTagType set redis success", gameId, codeType)
		return codeType
	} else {
		appLog.Info("setRedisOfficialTagType redis already has", gameId, codeType)
	}
	return ""
}

func (self *HttpService) handleExchangeActivationCode(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	var gameId = strings.Join(r.Form["gameId"], "")
	var code = strings.Join(r.Form["code"], "")
	var token = strings.Join(r.Form["token"], "")
	var tagType = strings.Join(r.Form["tagType"], "")

	codeType := getCodeType(code)
	if codeType == "" {
		self.replyActivationCode(w, false, "", ActivationCodeInvalid)
		log.Println("handleExchangeActivationCode: ", gameId, code, tagType, "invalid code")
		return
	}

	log.Println("handleExchangeActivationCode: ", gameId, code, tagType)

	bodyMap := map[string]string{
		"userGameId": gameId,
		"code":       code,
	}
	jsonBody, _ := json.Marshal(bodyMap)
	var reqHost string
	if value, ok := LoginConfig.Official["reqhost"]; ok {
		reqHost = value.(string)
	} else {
		appLog.Error("handleExchangeActivationCode LoginConfig.Official[reqHost]")
		return
	}

	var reqURI string
	if value, ok := LoginConfig.Official["accesscode"]; ok {
		reqURI = value.(string)
	} else {
		appLog.Error("handleExchangeActivationCode LoginConfig.Official[reqURI]")
		return
	}

	reqURL := reqHost + reqURI
	client := http.Client{Timeout: 5 * time.Second}
	req, err := http.NewRequest(http.MethodPost, reqURL, bytes.NewReader(jsonBody))
	if err != nil {
		appLog.Warn(fmt.Sprintf("handleExchangeActivationCode NewRequest: %s", err.Error()))
		self.replyActivationCode(w, false, "", UnknownError)
		return
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("satoken", token)

	resp, err := client.Do(req)
	if err != nil {
		appLog.Warn(fmt.Sprintf("handleExchangeActivationCode Do: %s", err.Error()))
		self.replyActivationCode(w, false, "", UnknownError)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		appLog.Warn(fmt.Sprintf("handleExchangeActivationCode ReadAll: %s", err.Error()))
		self.replyActivationCode(w, false, "", UnknownError)
		return
	}

	log.Println("handleExchangeActivationCode: ", string(body))

	var response ActivationCodeData
	err = json.Unmarshal(body, &response)
	if err != nil {
		appLog.Warn(fmt.Sprintf("handleExchangeActivationCode Unmarshal: %s", err.Error()))
		self.replyActivationCode(w, false, "", UnknownError)
		return
	}

	if response.Code == 200 {
		c := self.setRedisOfficialTagType(gameId, code)
		self.replyActivationCode(w, true, c, response.Code)
	} else {
		self.replyActivationCode(w, false, "", response.Code)
	}
}

// handleKickClient 踢下线指定账号的客户端。期望 form 参数：
//   accountName — hex 编码的 "<accountType>-<accountName>" 字符串（accountType 已嵌入）
//   sign        — md5(hex(accountName) + LoginConfig.LoginHttpSecret) 的 hex 大/小写均可
// 调用后 CentralLoginApp.KickAccountClient 会断开 RPC 连接、从 gameClients 移除并清掉 Redis token，
// 使该账号后续 VerifyLogin 的 checkClientLogin 必返回 false。
func (self *HttpService) handleKickClient(w http.ResponseWriter, r *http.Request) {
	appLog.Debug("handleKickClient")
	if r.Method != "POST" {
		w.WriteHeader(405)
		return
	}
	if err := r.ParseForm(); err != nil {
		appLog.Error("handleKickClient parse form err", err)
		w.WriteHeader(400)
		return
	}

	encodedAccount := strings.Join(r.Form["accountName"], "")
	sign := strings.Join(r.Form["sign"], "")
	if encodedAccount == "" || sign == "" {
		appLog.Error("handleKickClient missing accountName/sign")
		w.WriteHeader(400)
		return
	}

	// 鉴权：md5(encodedAccount + secret)
	h := md5.New()
	h.Write([]byte(encodedAccount))
	h.Write([]byte(LoginConfig.LoginHttpSecret))
	expected := hex.EncodeToString(h.Sum(nil))
	if !strings.EqualFold(expected, sign) {
		appLog.Errorf("handleKickClient invalid sign: got=%s want=%s\n", sign, expected)
		w.WriteHeader(403)
		return
	}

	// 解码 & 还原 accountType / accountName
	decoded, err := hex.DecodeString(encodedAccount)
	if err != nil {
		appLog.Error("handleKickClient hex decode err", err)
		w.WriteHeader(400)
		return
	}
	accountStr := string(decoded)
	sepIdx := strings.Index(accountStr, ":")
	if sepIdx <= 0 || sepIdx == len(accountStr)-1 {
		appLog.Error("handleKickClient invalid account format:", accountStr)
		w.WriteHeader(400)
		return
	}
	platId, err := strconv.ParseUint(accountStr[:sepIdx], 10, 32)
	if err != nil {
		appLog.Error("handleKickClient parse platId err", err, accountStr)
		w.WriteHeader(400)
		return
	}
	accountName := accountStr[sepIdx+1:]

	self.app.KickAccountClient(uint32(platId), accountName)
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "ok")
}

func (self *HttpService) startHttpServer(listenAddr string) {
	appLog.Info("startHttpServer", listenAddr)

	http.HandleFunc("/exchangeActivationCode", self.handleExchangeActivationCode)
	http.HandleFunc("/kickClient", self.handleKickClient)

	listener, err := greuse.Listen("tcp", listenAddr)
	if err != nil {
		panic(err)
	}
	defer listener.Close()

	server := &http.Server{}
	panic(server.Serve(listener))
}
