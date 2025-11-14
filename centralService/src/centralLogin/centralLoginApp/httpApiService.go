package CentralLogin

import (
	"centralService/src/appLog"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"

	//"os"
	"strconv"
	"strings"
	"time"

	//"golang.org/x/sys/unix"
	"centralService/src/common"

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

func (self *HttpService) startHttpServer(listenAddr string) {
	appLog.Info("startHttpServer", listenAddr)

	http.HandleFunc("/idipUnban", self.handleIDIPUnBanRequest)
	http.HandleFunc("/idipBan", self.handleIDIPBanRequest)
	http.HandleFunc("/delaccount", self.handleIDIPDelAccount)
	http.HandleFunc("/queryaccountlastlogin", self.handleIDIPQueryLastLogin)
	http.HandleFunc("/queryaccountservers", self.queryAccountServers)

	listener, err := greuse.Listen("tcp", listenAddr)
	if err != nil {
		panic(err)
	}
	defer listener.Close()

	server := &http.Server{}
	panic(server.Serve(listener))
}
