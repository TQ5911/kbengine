package main

import (
	"bufio"
	"centralService/src/appLog"
	clientService "centralService/src/centralLogin/centralLoginApp/clientService"
	WeTest "centralService/src/centralLogin/wetest"
	"centralService/src/trpc"
	"fmt"
	"io"
	"log"
	"math/rand"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/google/uuid"
)

type TestResult struct {
	resCode    int
	accoutName string
}

type LoginClient struct {
	*clientService.CentralServerClient
	serviceDesc trpc.ServiceDesc
	channel     *trpc.RpcChannel
	accountName string
	waitGroup   *sync.WaitGroup
	done        chan struct{}
	isTimeout   bool
	tStart      uint64
}

type TestData struct {
	Openid     string `json:"openid,omitempty"`
	UserName   string `json:"user_name,omitempty"`
	Gender     uint32 `json:"gender,omitempty"`
	PictureUrl string `json:"picture_url,omitempty"`
	Country    string `json:"country,omitempty"`
	Provice    string `json:"provice,omitempty"`
	City       string `json:"city,omitempty"`
	Language   string `json:"language,omitempty"`
}

var connResult chan TestResult
var weTest WeTest.WeTestApi
var dataClient WeTest.WeTestApi

func (self *LoginClient) run() {
	go self.checkActive()
	self.channel.Process()
}

func (self *LoginClient) checkActive() {
	ticker := time.NewTicker(time.Second * 10)
	for {
		<-ticker.C
		self.ActiveTick(&clientService.Void{})
	}
}

func (self *LoginClient) GetServiceDesc() *trpc.ServiceDesc {
	return &self.serviceDesc
}

func (self *LoginClient) OnLoseConnection() {

}
func (self *LoginClient) OnGetLoginKey(res *clientService.LoginKeyResponse) (*clientService.Void, error) {
	log.Printf("after login %+v\n", res)
	//in := &clientService.MsdkTokenLogin{}
	//in.AccountName = self.accountName
	//in.Token = res.SStr + "50_Zx_6u5GyguA-kLjrwNlpaJDW2WPRZWKg0rVryWTBnVBbX51Hv4Kf7YMH2DCJ-r9xKHoLRDHcrFB9zvPstGoWlFhkf__SP-3PY9ilB4cFGRk"
	//in.ChannelId = 1
	//in.Os = 1
	////log.Println("begin login:", in.AccountName)
	//self.LoginByMsdkToken(in)

	return nil, nil
}

func (self *LoginClient) OnLoginReply(res *clientService.LoginReply) (*clientService.Void, error) {
	log.Println("onLoginReply", self.accountName, res.Result, res.CentralServerId)
	if res.Result == clientService.LoginReply_LOGIN_SUCCESS {
		self.GetCharaterInfo(&clientService.Void{})
	}
	return nil, nil
}

func (self *LoginClient) OnGetCharacterInfo(*clientService.CharacterInfo) (*clientService.Void, error) {
	log.Println("OnGetCharacterInfo", self.accountName)
	return nil, nil
}

func (self *LoginClient) OnListServers(info *clientService.ServerInfo) (*clientService.Void, error) {
	log.Println("on list servers", self.accountName)

	return nil, nil
}

func (self *LoginClient) OnCheckCDKey(*clientService.CheckCDKeyReply) (*clientService.Void, error) {
	return nil, nil
}

func (self *LoginClient) OnGetServerListDir(*clientService.ServerListReply) (*clientService.Void, error) {
	return nil, nil
}

func (self *LoginClient) ActiveTickCallback(*clientService.Void) (*clientService.Void, error) {
	return nil, nil
}

func (self *LoginClient) GetRpcChannel() *trpc.RpcChannel {
	return nil
}
func (self *LoginClient) SetRpcChannel(channel *trpc.RpcChannel) {

}

func NewLoginClientEndPoint(conn net.Conn, wg *sync.WaitGroup, accountName string, done chan struct{}) trpc.IEndPoint {
	channel := trpc.NewRpcChannel(uuid.New(), conn)
	var client trpc.IEndPoint = &LoginClient{
		CentralServerClient: clientService.NewCentralServerClient(channel),
		serviceDesc:         clientService.GameClientServiceDesc,
		channel:             channel,
		waitGroup:           wg,
		accountName:         accountName,
		isTimeout:           false,
		tStart:              uint64(time.Now().UnixNano() / 1e6),
		done:                done,
	}
	channel.SetEndPoint(client)
	go client.(*LoginClient).run()
	return client
}

func singleClientTest(ipAddr string, accountName string, wg *sync.WaitGroup) {
	conn, err := net.DialTimeout("tcp4", ipAddr, time.Second*10)
	wg.Add(1)
	done := make(chan struct{}, 1)
	var client *LoginClient
	if err != nil {
		log.Println("fail to connect server:", err)

		connResult <- TestResult{1, accountName}
		dataClient.TransInfo(WeTest.TransInfo{"testLogin", 0, 2})
		done <- struct{}{}
	} else {
		client = NewLoginClientEndPoint(conn, wg, accountName, done).(*LoginClient)
		r := &clientService.LoginKeyRequest{RStr: "sdjghnadf23"}
		log.Println("login start", accountName)
		client.GetLoginKey(r)
	}
	select {
	case <-done:
		break
	case <-time.After(time.Second * 60):
		client.isTimeout = true
		connResult <- TestResult{2, accountName}
		tNow := uint64(time.Now().UnixNano() / 1e6)
		dataClient.TransInfo(WeTest.TransInfo{"testLogin", int(tNow - client.tStart), 3})
		break
	}
	wg.Done()
	close(done)
}

func initWeTestClient() {
	WeTest.InitClient()
	weTest = WeTest.New()
	startRst := weTest.StartTest(1)
	if startRst == nil {
		fmt.Println("start error, result is nil")
		return
	}
	if startRst["ret"] != "0" {
		fmt.Println("start error, ret=" + startRst["ret"])
		for k, v := range startRst {
			fmt.Println(k, v)
		}
		return
	}
	testId := startRst["testId"]
	instanceId := startRst["instanceId"]
	token := startRst["token"]
	dcAddr := startRst["dcAddr"]

	if testId == "" {
		fmt.Println("testId is nil")
		return
	}

	//第二步上报注册压力进程实例
	dataClient = WeTest.NewWithUrl("http://" + dcAddr)
	fmt.Println("start succeed, testId=" + testId + "; instanceId=" + instanceId + "; reportAddr=" + "http://" + dcAddr)

	//第二步上报注册压力进程实例
	dataClient.RegisterLoad(testId, instanceId, token)
}

func testLogin(ipAddr string, accountNameChan chan string, num int, duration time.Duration) {
	log.Println("begin test:", ipAddr, num, duration)

	wg := sync.WaitGroup{}
	total := 0
	succCnt := 0

	for i := 0; i < num; i++ {
		accName := <-accountNameChan
		go singleClientTest(ipAddr, accName, &wg)
	}

	go func() {
		<-time.After(duration)
		connResult <- TestResult{-1, ""}
	}()

	testComplete := make(chan struct{}, 1)

	stopTest := false
TEST:
	for {
		select {
		case ret := <-connResult:
			if ret.resCode < 0 {
				stopTest = true
				go func() {
					wg.Wait()
					testComplete <- struct{}{}
				}()
				continue
			}

			total += 1
			accountNameChan <- ret.accoutName
			if ret.resCode == 0 {
				succCnt += 1
			}

			if !stopTest {
				go func() {
					//time.Sleep(time.Millisecond*500)
					name := <-accountNameChan
					singleClientTest(ipAddr, name, &wg)
				}()
			}

		case <-testComplete:
			break TEST

		case <-time.After(time.Second*60 + duration):
			break TEST
		}
	}

	log.Printf("finish testing: %d/%d success\n", succCnt, total)
}

var letters = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

func RandString(n int) string {
	b := make([]rune, n)

	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}

func main() {
	args := os.Args
	if len(args) < 4 {
		log.Println("Usage: test ip connectionNum duration accountsFile")
		return
	}

	if !appLog.LogInit("test.log", -1, 0) {
		log.Println("failed to init log")
		return
	}

	ipAddr := args[1]
	connNum, err := strconv.ParseInt(args[2], 10, 32)
	duration, err2 := strconv.ParseInt(args[3], 10, 32)
	if err != nil || err2 != nil {
		log.Fatalln("connectionNum/duration must be integer")
	}

	connResult = make(chan TestResult, connNum)
	var accountNames chan string
	if len(args) >= 5 {
		accountArray := make([]string, 0, 1000)
		accountFilePath := args[4]
		fAccounts, err := os.OpenFile(accountFilePath, os.O_RDONLY, 0666)
		if err != nil {
			log.Println("cannot open file:", accountFilePath)
			return
		}

		reader := bufio.NewReader(fAccounts)
		for {
			line, err := reader.ReadString('\n')
			if err == io.EOF {
				accountArray = append(accountArray, strings.Trim(line, " \n"))
				break
			}
			if err != nil {
				log.Println("read file err", err.Error())
				return
			}
			trimName := strings.TrimSpace(line)
			if len(trimName) == 0 {
				continue
			}
			accountArray = append(accountArray, trimName)
		}

		accountNames = make(chan string, len(accountArray))
		for _, name := range accountArray {
			accountNames <- name
		}
	} else {
		accountNames = make(chan string, connNum)
		rand.Seed(time.Now().UnixNano())
		for i := 0; i < int(connNum); i++ {
			accountNames <- RandString(10)
		}
	}

	initWeTestClient()

	testLogin(ipAddr, accountNames, int(connNum), time.Second*time.Duration(duration))
}
