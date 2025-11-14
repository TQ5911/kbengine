package adminApp

import (
	webService "centralService/src/adminServer/adminProto/webservice"
	"centralService/src/appLog"
	"fmt"
	"net/http"
	"strings"
)

type HttpSDKService struct {
	app *AdminApp
}

func (self *HttpSDKService) handlerNeteaseMusicRedirect(w http.ResponseWriter, r *http.Request) {
	codeStr, ok := r.URL.Query()["code"]
	if !ok && len(codeStr) == 0 {
		appLog.Error("param code err!\n")
		return
	}
	code := codeStr[0]
	stateStr, ok := r.URL.Query()["state"]
	if !ok && len(stateStr) == 0 {
		appLog.Error("param state err!\n")
		return
	}

	stats := strings.Split(stateStr[0], "-")
	if len(stats) != 2 {
		appLog.Error("param state data  err!\n")
		return
	}
	gbid := stats[1]
	serverId := stats[0]
	appLog.Debug("handlerNeteaseMusicRedirect------", serverId, gbid, code, adminConfig.NeteaseMusicRedirect)

	go func() {
		_, err := self.app.GmtService.DoCommand(nil, &webService.CommandInfo{Acount: "snail", ServerId: StrToUInt32(serverId), Command: "$pushNeteaseMusicCode " + gbid + " " + code})
		if err != nil {
			appLog.Error("docmd:", err)
			return
		}
	}()
	w.Header().Set("Location", adminConfig.NeteaseMusicRedirect)
	w.WriteHeader(301)
	fmt.Fprintf(w, "SUCCESS")
}

func (self *HttpSDKService) startHttpApiServer(listenAddr string) {
	mux := http.NewServeMux()
	mux.HandleFunc("/apiNeteaseMusic/redirect", self.handlerNeteaseMusicRedirect)
	err := http.ListenAndServe(listenAddr, mux)
	if err != nil {
		appLog.Panic("fail to serve at", listenAddr)
	}
}
