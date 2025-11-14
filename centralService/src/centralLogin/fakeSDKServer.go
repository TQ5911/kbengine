package main

import (
	"centralService/src/appLog"
	CentralLogin "centralService/src/centralLogin/centralLoginApp"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strings"

	"github.com/gogf/greuse"
)

var friendsMap = make(map[int8]string, 10)

func buildFriendsMap() {
	resFmt := `{"Ret":0,"Msg":"","IsLost":0,"Lists":[%s]}`
	friendVal := `{"openid":"1709973036100386592","user_name":"狮子座的那个男人","gender":1,"picture_url":"https://q.qlogo.cn/qqapp/1110663613/02A0817531EC297D6CD7078AAFF5A2A8/","country":"","provice":"","city":"Pudong"}`
	var friendList [10]string
	friendsMap[0] = fmt.Sprintf(resFmt, "")
	for i := 1; i < 10; i++ {
		for j := 0; j < i; j++ {
			friendList[j] = friendVal
		}
		friendsMap[int8(i)] = fmt.Sprintf(resFmt, strings.Join(friendList[:i], ","))
	}
}

func handleMSDKRequest(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, `{"Ret":0,"Msg":"success","Seq":"123456"}`)
}

func handleWxFriendRequest(w http.ResponseWriter, r *http.Request) {
	num := rand.Uint32() % 10
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, friendsMap[int8(num)])
}

func startHttpServer(listenAddr string) {
	appLog.Info("startHttpServer", listenAddr)

	http.HandleFunc("/v2/auth/verify_login", handleMSDKRequest)
	http.HandleFunc("/v2/friend/friend_list", handleWxFriendRequest)

	listener, err := greuse.Listen("tcp", listenAddr)
	if err != nil {
		panic(err)
	}
	defer listener.Close()

	server := &http.Server{}
	panic(server.Serve(listener))
}

func main() {
	args := os.Args
	if len(args) < 2 {
		log.Println("Usage: fakeSDKServer port")
		return
	}

	if !appLog.LogInit("fakeSDKServer.log", -1, 0) {
		log.Println("failed to init log:", CentralLogin.LoginConfig.LogPath, CentralLogin.LoginConfig.LogLevel)
		return
	}

	buildFriendsMap()

	addr := fmt.Sprintf("0.0.0.0:%s", args[1])
	startHttpServer(addr)
}
