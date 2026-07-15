package adminApp

import (
	gsmanager "centralService/src/adminServer/adminProto/gsmanager"
	"centralService/src/appLog"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"strings"
)

type IDIPSendMailByAccountResp struct {
	Result uint8
	RetMsg string
}
type IDIPDelAccountResp IDIPSendMailByAccountResp
type IDIPAuthChangedResp IDIPSendMailByAccountResp

type IDIPGlobalCmd struct {
	broadcastAllServer bool
	handleFunc         func(service *HttpCommandService, reqData *CommandRequest, args ...interface{}) (int, []byte)
}

func handleBanAccount(service *HttpCommandService, reqData *CommandRequest, args ...interface{}) (int, []byte) {
	// $banaccount 当前只打列表里的第一个 centralLogin；如需 fanout 可参考 handleKickAccount。
	addr := ""
	if len(adminConfig.CentralLoginCmdAddressList) > 0 {
		addr = adminConfig.CentralLoginCmdAddressList[0]
	}
	urlStr := strings.Join([]string{"http://", addr, "/doLoginCommand",
		"?Cmd=", reqData.Command, "&args=", reqData.Args, "&partition=", strconv.Itoa(int(reqData.Partition)),
	}, "")
	appLog.Debug("urlStr", urlStr)
	request, err := http.NewRequest("GET", urlStr, nil)
	if err != nil {
		appLog.Errorf("post request error: %s\n", urlStr)
		return 400, nil
	}

	var responseBytes []byte = nil

	//post数据并接收http响应
	resp, err := http.DefaultClient.Do(request)
	if err != nil {
		appLog.Error("handleBanAccount: doLoginCommand error:", err.Error())
		return 400, nil
	} else {
		resCode := resp.StatusCode
		if resCode != 200 {
			errMsg := fmt.Sprintf("doLoginCommand: request error: %d", resCode)
			responseBytes = service._buildErrResponse(HTTP_CMD_REQUEST_ERR, errMsg)
		} else {
			respBody, _ := ioutil.ReadAll(resp.Body)
			response := gsmanager.HttpAPICommandResponse{}
			if err := json.Unmarshal([]byte(respBody), &response); err == nil {
				responseBytes = service.buildIDIPResponse(&response, reqData)
			} else {
				appLog.Error("Unmarshal respBody error:\n", err.Error(), respBody)
				return 400, nil
			}
		}
		return 200, responseBytes
	}
}

var GLOBAL_CMDS = map[string]IDIPGlobalCmd{
	"$banaccount": {broadcastAllServer: true, handleFunc: handleBanAccount},
}
