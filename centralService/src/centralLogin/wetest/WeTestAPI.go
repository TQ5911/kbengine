package wetest

import (
	"bytes"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net"
	"net/http"
	"net/url"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

//----------------------+++++++++++++++++---------------------- WeTestApi ----------------------+++++++++++++++++----------------------
const (
	secretid  = "f0aefa66fc6048cabfa04b047e83be7e"
	secretkey = "c1el4bmkirfvueuapm10"
	projectid = "xzj-logincenter"

	//wetest上报环境，需要根据不同环境选择其中一个
	//1.外网环境配置
	//apiurl = "" //待压测大师发布
	//zoneId = 0  //0表示腾讯云和其他外网环境，1表示腾讯IDC,2表示腾讯devnet

	////2.IDC环境配置
	apiurl = "http://api.paas.cloudtest.woa.com"
	zoneId = 1 //0表示腾讯云和其他外网环境，1表示腾讯IDC,2表示腾讯devnet
	//
	////3.DEVNET环境配置
	//apiurl = "http://api.paas.cloudtest.woa.com"
	//zoneId = 2 //0表示腾讯云和其他外网环境，1表示腾讯IDC,2表示腾讯devnet

	clientMum          = 1
	shouldMergerReport = true
	mergeTime          = 500 * 1000 * 1000
	mergeInfoCount     = 100
)

var (
	clientList      []*http.Client
	clientOrder     = 0
	testId          = ""
	instanceId      = ""
	token           = ""
	httpClient      *http.Client
	globalTimeStamp int64 = 0
	transInfoArray  []TransInfo
	lock            sync.Mutex
)

// 事务数据
type TransInfo struct {
	//TransName 事务名
	TransName string `json:"trans_name"`
	//TimeCost 耗时ms
	TimeCost int `json:"time_cost"`
	//TransResult 事务结果，0：失败，1：成功，2：错误，3：超时
	TransResult int `json:"trans_result"`
}

//在线人数数据
type StatisticsInfo struct {
	//RobotTotalNum 机器人总个数，上次上报到当前时刻的时间段
	RobotTotalNum int `json:"robot_total_num"`
	//RobotOnlineNum 机器人在线总个数，上次上报到当前时刻的时间段
	RobotOnlineNum int `json:"robot_online_num"`
	//RecvPkgTotalNum 收包总个数 ，上次上报到当前时刻的时间段
	RecvPkgTotalNum int `json:"recv_pkg_total_num"`
	//SendPkgTotalNum 发包总个数 ，上次上报到当前时刻的时间段
	SendPkgTotalNum int `json:"send_pkg_total_num"`
}

// 事务数据
type TransInfoPostData struct {
	// 数组格式
	Data []TransInfo `json:"data"`
}

//在线人数数据
type StatisticsInfoPostData struct {
	//在线人数
	Data StatisticsInfo `json:"data"`
}

// WeTestApi 封装
type WeTestApi struct {
	//secretid 用户的secret id
	secretid   string
	//secretkey 用户的secret key
	secretkey  string
	// 建立连接的host
	host       string
	//expiretime 签名失效时间，大于时间戳,如果为0为单次调用，最大有效期为一个月
	expiretime int
}

func New() WeTestApi {
	client := WeTestApi{secretid, secretkey, apiurl, 0}
	return client
}
func NewWithExpireTime(expireTime int) WeTestApi {
	client := WeTestApi{secretid, secretkey, apiurl, expireTime}
	return client
}
func NewWithUrl(url string) WeTestApi {
	client := WeTestApi{secretid, secretkey, url, 0}
	return client
}
func NewWithUrlExpireTime(url string, expireTime int) WeTestApi {
	client := WeTestApi{secretid, secretkey, url, expireTime}
	return client
}
func NewWithFullParam(secretId string, secretKey string, host string, expireTime int) WeTestApi {
	client := WeTestApi{secretId, secretKey, host, expireTime}
	return client
}

/*
	主要生成签名串，对应API文档第1节
*/
func (c *WeTestApi) getSignatureParams(requestUri string, queryData map[string]string, method string) map[string]string {
	timestamp := time.Now().Unix()
	nonce := rand.Intn(9999999)
	//nonce := 0
	var data map[string]string
	data = make(map[string]string)
	data["t"] = strconv.FormatInt(timestamp, 10)
	data["nonce"] = strconv.Itoa(nonce)
	//data["signaturemethod"] = "HmacSHA256"
	//data["expire"] = strconv.Itoa(c.expiretime)
	data["secret_id"] = c.secretid
	for key := range queryData {
		data[key] = queryData[key]
	}
	var keys []string
	for key := range data {
		keys = append(keys, key)
	}
	sort.Strings(keys)
	var queryStr string
	for _, k := range keys {
		//rKey := strings.ReplaceAll(k, "_", ".")
		//queryStr += rKey
		queryStr += k
		queryStr += "="
		queryStr += data[k]
		queryStr += "&"
	}
	if strings.HasSuffix(queryStr, "&") {
		queryStr = queryStr[0 : len(queryStr)-1]
	}
	sourceStr := method + "&" + url.QueryEscape(requestUri) + "&" + url.QueryEscape(queryStr)
	encodeStr := hmac.New(sha256.New, []byte(c.secretkey))
	encodeStr.Write([]byte(sourceStr))
	signature := base64.StdEncoding.EncodeToString(encodeStr.Sum(nil))
	var result map[string]string
	result = make(map[string]string)
	for _, k := range keys {
		result[k] = data[k]
	}
	result["sign"] = signature //这一步不要urlEncode,后面请求的时候回Encode
	fmt.Println("sourceStr=" + sourceStr + ";    signature=" + signature)
	return result
}

func (c *WeTestApi) getRequestUri(route string) string {
	return c.host + route
}

func (c *WeTestApi) doHttpGet(method string, url string, params map[string]string) map[string]string {
	req, err := http.NewRequest(method, c.getRequestUri(url), nil)
	req.Close = false
	if err == nil {
		q := req.URL.Query()
		for key := range params {
			q.Add(key, params[key])
		}
		req.URL.RawQuery = q.Encode()
	}

	var resp *http.Response
	resp, err = getClient().Do(req)
	if resp != nil {
		defer resp.Body.Close()
	}
	if err != nil {
		fmt.Println("doHttpGet_get_err=" + err.Error())
		return nil
	}
	body, err := ioutil.ReadAll(resp.Body)
	var v interface{}
	result := make(map[string]string)
	err = json.Unmarshal(body, &v)
	if err != nil {
		fmt.Println("doHttpGet_parse_err=" + err.Error() + "; url=" + c.getRequestUri(url) + "; response=" + string(body))
		return nil
	}
	data := v.(map[string]interface{})
	for k, v := range data {
		switch v := v.(type) {
		case string:
			result[k] = v
		case int:
			result[k] = strconv.Itoa(v)
		default:
			result[k] = fmt.Sprintf("%v", v)
		}
	}
	return result
}

func (c *WeTestApi) doHttpPost(method string, url string, params map[string]string, jsonData []byte) map[string]string {
	return c.doHttpPostWithReturn(method, url, params, jsonData, true)
}

func (c *WeTestApi) doHttpPostWithReturn(method string, url string, params map[string]string, jsonData []byte, parseRes bool) map[string]string {
	newParams := c.getSignatureParams(url, params, "POST")
	req, err := http.NewRequest(method, c.getRequestUri(url), nil)
	req.Close = false
	var encodeUrl string
	if err == nil {
		q := req.URL.Query()
		for key := range newParams {
			q.Add(key, newParams[key])
		}
		encodeUrl = c.getRequestUri(url) + "?" + q.Encode()
	}
	if encodeUrl != "" && len(encodeUrl) > 0 {
		req, err := http.NewRequest("POST", encodeUrl, bytes.NewBuffer(jsonData))
		if err != nil {
			fmt.Println("doHttpPost_request_err=" + err.Error())
			return nil
		}
		req.Header.Set("Content-Type", "application/json")
		req.Header.Set("Connection", "keep-alive")
		resp, err := getClient().Do(req)
		//resp, err := getClient().Post(encodeUrl, "application/json", bytes.NewBuffer(jsonData))
		if resp != nil {
			defer resp.Body.Close()
		}
		if err != nil {
			fmt.Println("doHttpPost_response_err=" + err.Error())
		}
		if resp == nil || resp.Body == nil {
			return nil
		}
		body, _ := ioutil.ReadAll(resp.Body) //建议必须全部读取http response的data, 这样TCP就不会残留数据，影响reuse

		if !parseRes {
			//为了尽量减少客户端不必要的处理耗时
			return nil
		}
		var v interface{}
		result := make(map[string]string)
		err = json.Unmarshal(body, &v)
		if err != nil {
			fmt.Println("doHttpPost_parse_err=" + err.Error() + "; response=" + string(body))
			return nil
		}
		data := v.(map[string]interface{})
		for k, v := range data {
			switch v := v.(type) {
			case string:
				result[k] = v
			case int:
				result[k] = strconv.Itoa(v)
			}
		}
		return result
	}
	return nil
}

/*
	开始上报测试，对应API文档第2节
	请求参数：
	必须 projectid string 项目ID，进入压测大师的项目主页，浏览器url中的projectid对应的参数即是
	必须 zoneid int 区域ID,(0表示腾讯云和其他外网环境，1表示腾讯IDC,2表示腾讯devne)
	返回值：
	testid string 本次测试的testid
	dcAddr string 性能测试数据上报的datacenter addr,测试进行中的数据均上报到该地址
	instanceid int 机器人压力进程的序号id,该参数由平台下发，停止测试api中需要使用此参数，最大同时支持16个压力进程
*/
func (c *WeTestApi) StartTest(zoneId int) map[string]string {
	url := "/loadmaster/data-collect/start-test"
	var params map[string]string
	params = make(map[string]string)
	params["projectid"] = projectid
	params["zoneid"] = strconv.Itoa(zoneId)
	newParams := c.getSignatureParams(url, params, "GET")
	return c.doHttpGet("GET", url, newParams)
}

/*
	上报注册压力进程，对应API文档第3节
	请求参数：
	必须 projectid string 项目ID，进入压测大师的项目主页，浏览器url中的projectid对应的参数即是
	必须 testid string 本次测试的testid
	必须 instanceid int 机器人压力进程的序号id,该参数由平台下发，停止测试api中需要使用此参数，最大同时支持16个压力进程
	返回值：
	只需关注是否错误
*/
func (c *WeTestApi) RegisterLoad(testId_ string, instId_ string,token_ string) map[string]string {
	url := "/gapsapi/data_collect_v1/register_load"
	var params map[string]string
	params = make(map[string]string)
	params["testid"] = testId_
	//params["projectid"] = projectid
	params["instanceid"] = instId_
	params["token"] = token_
	testId = testId_
	instanceId = instId_
	token = token_
	newParams := c.getSignatureParams(url, params, "GET")
	return c.doHttpGet("GET", url, newParams)
}

/*
	上报停止测试，对应API文档第6节
	请求参数：
	必须 projectid string 项目ID，进入压测大师的项目主页，浏览器url中的projectid对应的参数即是
	必须 testid string 本次测试的testid
	必须 instanceid int 机器人压力进程的序号id,由平台下发，最大同时支持16个压力进程
	返回值：
	只需关注是否错误
*/
func (c *WeTestApi) StopTest(testId string, instId string) map[string]string {
	url := "/loadmaster/data-collect/stop-test"
	var params map[string]string
	params = make(map[string]string)
	params["testid"] = testId
	params["projectid"] = projectid
	params["instid"] = instId
	newParams := c.getSignatureParams(url, params, "GET")
	return c.doHttpGet("GET", url, newParams)
}
func (c *WeTestApi) TransInfo(transInfo TransInfo) map[string]string {
	return c.TransInfoWithId(testId, instanceId, transInfo)
}
func (c *WeTestApi) TransInfoWithArray(transInfoArr []TransInfo) map[string]string {
	return c.TransInfoArrayWithId(testId, instanceId, transInfoArr)
}

/*
	上报事务数据，对应API文档第4节
	data 格式：
	必须 trans_name string 事务名
	必须 trans_result int 事务状态（0：失败，1：成功，2：错误，3：超时）
	必须 time_cost int 事务耗时，单位ms
	非必须 timestamps int 机器人进程机器的当前时间戳秒数
	非必须 timestampus int 机器人进程机器的当前时间戳微秒数
	非必须 ErrCode int 事务详细错误码
	非必须 ErrStr string 事务详细错描述
*/
func (c *WeTestApi) TransInfoWithId(testId string, instId string, transInfo TransInfo) map[string]string {
	if shouldMergerReport {
		lock.Lock()
		defer lock.Unlock()
		var resultMap map[string]string
		//合并上报。合并条件累计mergeTime ms或者已经累计的数组长度超过了mergeInfoCount
		curTimeStamp := time.Now().UnixNano()
		if globalTimeStamp <= 0 {
			//担心是之前比较就的没上报的，开始的就丢弃吧
			if len(transInfoArray) > 0 {
				transInfoArray = nil
			}
			globalTimeStamp = curTimeStamp
			transInfoArray = append(transInfoArray, transInfo)
			return nil
		} else if curTimeStamp-globalTimeStamp > mergeTime || len(transInfoArray) > mergeInfoCount {
			//累计时间到达或者累计次数到达
			if len(transInfoArray) > 0 {
				var tmpArray = make([]TransInfo, len(transInfoArray))
				copy(tmpArray, transInfoArray)
				transInfoArray = nil
				resultMap = c.TransInfoArrayWithId(testId, instId, tmpArray)
			}
			globalTimeStamp = curTimeStamp
			transInfoArray = append(transInfoArray, transInfo)
			return resultMap
		} else {
			transInfoArray = append(transInfoArray, transInfo)
			return nil
		}
	} else {
		var jsonArr []TransInfo
		jsonArr = append(jsonArr, transInfo)
		return c.TransInfoArrayWithId(testId, instId, jsonArr)
	}
}

func (c *WeTestApi) TransInfoArrayWithId(testId string, instId string, transInfo []TransInfo) map[string]string {
	myUrl := "/gapsapi/data_collect_v1/trans_info"
	var params map[string]string
	params = make(map[string]string)
	params["testid"] = testId
	//params["projectid"] = projectid
	params["instanceid"] = instId
	params["token"] = token
	var jsonArr []TransInfo
	for _, info := range transInfo {
		jsonArr = append(jsonArr, info)
	}
	postData := TransInfoPostData{jsonArr}
	b, err := json.Marshal(postData)
	if err != nil {
		return nil
	}
	return c.doHttpPost("POST", myUrl, params, b)
}

func (c *WeTestApi) StatisticsInfo(statisticsInfo StatisticsInfo) map[string]string {
	return c.StatisticsInfoWithId(testId, instanceId, statisticsInfo)
}

/*
	上报在线数据，对应API文档第5节
	data 格式：
	必须 robot_total_num int 机器人总个数，上次上报到当前时刻的时间段
	必须 robot_online_num int 机器人在线总个数，上次上报到当前时刻的时间段
	必须 recv_pkg_total_num int 收包个数，上次上报到当前时刻的时间段
	必须 send_pkg_total_num int 发包个数，上次上报到当前时刻的时间段
	非必须 timestamps int 机器人进程机器的当前时间戳秒数,单位秒
*/
func (c *WeTestApi) StatisticsInfoWithId(testId string, instId string, statisticsInfo StatisticsInfo) map[string]string {
	myUrl := "/gapsapi/data_collect_v1/statistics_info"
	var params map[string]string
	params = make(map[string]string)
	params["testid"] = testId
	//params["projectid"] = projectid
	params["instanceid"] = instId
	params["token"] = token
	postData := StatisticsInfoPostData{statisticsInfo}
	b, err := json.Marshal(postData)
	if err != nil {
		return nil
	}
	return c.doHttpPost("POST", myUrl, params, b)
}

//----------------------+++++++++++++++++---------------------- test ----------------------+++++++++++++++++----------------------

//初始化全局client
func InitClient() {
	httpClient = &http.Client{
		//Transport: &http.Transport{
		//	DisableKeepAlives: false,
		//	//Proxy:             http.ProxyFromEnvironment,
		//	DialContext: (&net.Dialer{
		//		Timeout:   30 * time.Second, // 创建一个TCP连接使用的时间
		//		KeepAlive: 600 * time.Second,
		//	}).DialContext,
		//	MaxIdleConns:          150,
		//	IdleConnTimeout:       60 * time.Second, //用于控制一个闲置连接在连接池中的保留时间，而不考虑一个客户端请求被阻塞在哪个阶段
		//	ResponseHeaderTimeout: 10 * time.Second,
		//	ExpectContinueTimeout: 1 * time.Second,  //限制client在发送包含 Expect: 100-continue的header到收到继续发送body的response之间的时间等待。注意在1.6中设置这个值会禁用HTTP/2(DefaultTransport自1.6.2起是个特例)
		//	TLSHandshakeTimeout:   10 * time.Second, //TLS握手超时时间
		//	MaxIdleConnsPerHost:   150,
		//	MaxConnsPerHost:       200,
		//},
		//Timeout: 120 * time.Second,
	}
	clientList = MakeClientList(clientMum)
}

//可以选择使用多个client，效率未验证
func MakeClientList(count int) []*http.Client {
	clientList := make([]*http.Client, count, count)
	for index := 0; index < count; index++ {
		clientList[index] = &http.Client{
			Transport: &http.Transport{
				DisableKeepAlives: false,
				//Proxy:             http.ProxyFromEnvironment,
				DialContext: (&net.Dialer{
					Timeout:   30 * time.Second, // 创建一个TCP连接使用的时间
					KeepAlive: 120 * time.Second,
				}).DialContext,
				MaxIdleConns:          3000,
				IdleConnTimeout:       60 * time.Second, //用于控制一个闲置连接在连接池中的保留时间，而不考虑一个客户端请求被阻塞在哪个阶段
				ResponseHeaderTimeout: 10 * time.Second,
				ExpectContinueTimeout: 30 * time.Second,
				MaxIdleConnsPerHost:   3000,
				MaxConnsPerHost:       3000,
			},
		}
	}
	return clientList
}

func getClient() *http.Client {
	clientOrder += 1
	return clientList[clientOrder%len(clientList)]
}

func main() {
	//InitClient()
	clientList = MakeClientList(clientMum)

	//第一步，调用开始上报测试
	//返回值 testid：本次测试的testid
	//返回值 dcAddr: 性能测试数据上报的datacenter addr,测试进行中的数据均上报到改地址
	//返回值 instanceid： 机器人压力进程的序号id,停止测试api中需要使用此参数，最大同时支持16个压力进程
	client := New()
	//zoneid 区域ID,(0表示腾讯云和其他外网环境，1表示腾讯IDC,2表示腾讯devne)
	startRst := client.StartTest(zoneId)
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
	testId = startRst["testId"]
	instanceId = startRst["instanceId"]
	token = startRst["token"]
	dcAddr := startRst["dcAddr"]

	if testId == "" {
		fmt.Println("testId is nil")
		return
	}
	dataClient := NewWithUrl("http://" + dcAddr)
	fmt.Println("start succeed, testId=" + testId + "; instanceId=" + instanceId + "; reportAddr=" + "http://" + dcAddr)

	//第二步上报注册压力进程实例
	dataClient.RegisterLoad(testId, instanceId, token)

	startTime := time.Now().UnixNano()
	//第三步，性能测试过程中的数据上报，可以模拟多次上报

	var wg sync.WaitGroup
	testNum := 1000
	wg.Add(testNum)
	for i := 0; i < testNum; i++ {
		transInfo := TransInfo{"Trans_Test_0", 1, 1}
		transInfoArr := []TransInfo{{"Trans_Test_0", 1, 1}, {"Trans_Test_1", 10, 1}, {"Trans_Test_2", 10, 1}}
		onlineInfo := StatisticsInfo{100, 50, 200, 300}
		go func() {
			dataClient.TransInfo(transInfo)
			time.Sleep(100)
			dataClient.TransInfoWithArray(transInfoArr)
			time.Sleep(100)
			dataClient.StatisticsInfo(onlineInfo)
			time.Sleep(100)
			wg.Done()
		}()
	}
	wg.Wait()
	endTime := time.Now().UnixNano()
	fmt.Println("end_time=" + strconv.FormatInt(time.Now().UnixNano(), 10))
	fmt.Println("\n\nreport_time_cost=" + strconv.FormatInt((endTime-startTime)/(1000*1000), 10))
	//最后，停止上报,注意是client
	var stopResult map[string]string
	stopResult = client.StopTest(testId, instanceId)
	fmt.Println("执行完成, stop_result=")
	fmt.Println(stopResult)
}
