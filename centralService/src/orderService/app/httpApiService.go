package app

import (
	"bytes"
	"centralService/src/appLog"
	"crypto/aes"
	"crypto/cipher"
	"crypto/hmac"
	"crypto/md5"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"sort"
	"strings"
)

const (
	SUCCESS          = 0
	SERVER_NOT_EXIST = -1000
	PLAYER_NOT_EXIST = -1001
	REDIS_ERROR      = -1002
	MYSQL_ERROR      = -1003
	IN_PROCESSING    = -1004
	IN_DELIVERY      = -1005
	SIGN_ERR         = -1006
	ARGS_ERR         = -1007
	SERVER_ERROR     = -1008
	SERVER_MISSING   = -1009
	ITEM_CFG_MISSING = -1010
)

type CommandRequest struct {
	Action int16
	Datas  string
}

type OrderData struct {
	/**
	* 订单号（订单中心记录的统一订单号）
	 */
	OrderNo string `json:"OrderNo"`

	/**
	* 商单号（订单在支付渠道上的商单号）
	 */
	OutTradeNo string `json:"OutTradeNo"`

	/**
	* 订单创建时间
	 */
	CreateTime string `json:"CreateTime"`

	/**
	* 游戏ID，区分不同游戏
	 */
	GameId string `json:"GameId"`

	/**
	* GID - 账号在游戏中的唯一ID
	 */
	UserGameId string `json:"UserGameId"`

	/**
	* UID - 账号在我司的唯一ID
	 */
	UserId int64 `json:"UserId"`

	/**
	* GBID - 游戏角色ID
	 */
	UserRoleId int64 `json:"UserRoleId"`

	/**
	* 角色名
	 */
	RoleName string `json:"RoleName"`

	/**
	* 游戏区服号
	 */
	ServerId int32 `json:"ServerId"`

	/**
	* 游戏区服名称
	 */
	ServerName string `json:"ServerName"`

	/**
	* 商品ID
	 */
	ProductId int64 `json:"ProductId"`

	/**
	* 产品ID（如30000001）
	 */
	ProductCode int32 `json:"ProductCode"`

	/**
	* 渠道商品ID（如GOODS_001_MONTH）
	 */
	ChannelProductId string `json:"ChannelProductId"`

	/**
	* 商品名称
	 */
	ProductName string `json:"ProductName"`

	/**
	* 商品数量（APP内默认1，网页端支持超过1）
	 */
	BuyNum int `json:"BuyNum"`

	/**
	* 订单支付时间
	 */
	PayTime string `json:"PayTime"`

	/**
	* 应付金额
	 */
	PayableAmount float32 `json:"PayableAmount"`

	/**
	* 实付金额
	 */
	ActualAmount float32 `json:"ActualAmount"`

	/**
	* 订单状态：待支付/已支付/已完成/关闭取消
	 */
	OrderState string `json:"OrderState"`

	/**
	* 支付状态：未支付/支付中/支付成功/支付失败
	 */
	PayState string `json:"PayState"`

	/**
	* 支付方式：支付宝/微信
	 */
	PayType string `json:"PayType"`

	/**
	* 订单来源：APP PC H5
	 */
	OrderSource string `json:"OrderSource"`
	/**
	* 是否进保管箱-手动，1-自动
	 */
	AddToSafe uint8 `json:"AddToSafe"`
}

type CommandResponse struct {
	Result int32                  `json:"result"`
	Msg    string                 `json:"msg"`
	Body   map[string]interface{} `json:"body"`
}

type HttpCommandService struct {
	app *OrderApp
}

func (svc *HttpCommandService) _buildErrResponse(errCode int32, errMsg string) []byte {
	respData := CommandResponse{Result: errCode, Msg: errMsg, Body: nil}
	respData.Body = map[string]interface{}{}
	respBytes, err := json.Marshal(respData)
	if err != nil {
		appLog.Errorf("marshal response err: %v", err.Error())
		return nil
	}
	return respBytes
}

func (svc *HttpCommandService) sendIDIPResponse(w http.ResponseWriter, statusCode int, resBytes []byte) {
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

func (svc *HttpCommandService) handleHttpRequest(w http.ResponseWriter, req *http.Request) {
	if req.Method != "POST" {
		appLog.Errorf("req method err: %s", req.Method)
		w.WriteHeader(405)
		return
	}

	if len(OrderServiceConfig.ApiSecret) == 0 {
		appLog.Errorf("api secret missing err")
		w.WriteHeader(403)
		return
	}

	signStr, ok := req.URL.Query()["sign"]
	if !ok {
		appLog.Errorf("api sign missing err")
		w.WriteHeader(403)
		return
	}

	bodyBytes, err := io.ReadAll(io.LimitReader(req.Body, int64(4096)))
	if err != nil && err != io.EOF {
		appLog.Errorf("read body err: %s", err.Error())
		w.WriteHeader(400)
		return
	}

	if !svc.checkRequestSign(bodyBytes, signStr) {
		appLog.Errorf("invalid signature")
		errMsg := "request sign error"
		responseBytes := svc._buildErrResponse(SIGN_ERR, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}

	reqData := CommandRequest{}
	jsonDecoder := json.NewDecoder(bytes.NewReader(bodyBytes))
	jsonDecoder.UseNumber()

	err = jsonDecoder.Decode(&reqData)
	if err != nil {
		appLog.Errorf("parse request error: %s", err.Error())
		w.WriteHeader(400)
		return
	}

	if reqData.Action == Recharge || reqData.Action == Retry {
		datas, err := svc.decryptDatas(reqData.Datas, OrderServiceConfig.OrderDataSecret)
		if err != nil {
			appLog.Errorf("cannot decrypt args: %v, %v", reqData, err.Error())
			errMsg := "decrypt failed"
			responseBytes := svc._buildErrResponse(ARGS_ERR, errMsg)
			svc.sendIDIPResponse(w, 200, responseBytes)
			return
		}

		orderData := OrderData{}
		jsonDecoder := json.NewDecoder(bytes.NewReader(datas))
		jsonDecoder.UseNumber()

		err = jsonDecoder.Decode(&orderData)
		if err != nil {
			appLog.Errorf("unmarshal error args: %v, %v", string(datas), err.Error())
			errMsg := "unmarshal error"
			responseBytes := svc._buildErrResponse(ARGS_ERR, errMsg)
			svc.sendIDIPResponse(w, 200, responseBytes)
			return
		}

		svc.app.ProcessOrder(&orderData, svc, w)

	} else {
		appLog.Errorf(fmt.Sprintf("unsupported action name: %v", reqData.Action))
		errMsg := "invalid action name"
		responseBytes := svc._buildErrResponse(ARGS_ERR, errMsg)
		svc.sendIDIPResponse(w, 200, responseBytes)
		return
	}
}

func (svc *HttpCommandService) encryptDatas(plaintext []byte, secret string) (string, error) {
	block, _ := aes.NewCipher([]byte(secret))
	gcm, _ := cipher.NewGCM(block)
	nonce := make([]byte, gcm.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return "", err
	}
	ciphertext := gcm.Seal(nonce, nonce, plaintext, nil)
	return base64.StdEncoding.EncodeToString(ciphertext), nil
}

// 根据密码生成 AES 密钥（32字节）和零 IV（16字节）
func (svc *HttpCommandService) deriveKeyAndIV(password string) (secretKey []byte, iv []byte) {
	// 计算 SHA-256 哈希，得到 32 字节的密钥材料
	hash := sha256.Sum256([]byte(password))
	secretKey = hash[:] // 作为 AES-256 密钥

	// 零 IV（16 字节，与 AES 块大小相同）
	iv = make([]byte, aes.BlockSize) // 全零

	return secretKey, iv
}

// 如果需要直接构造 AES 块和 CBC 模式（假设使用 CBC 模式，与 Java 常见默认行为一致）
func (svc *HttpCommandService) createAESBlockMode(password string) (cipher.BlockMode, error) {
	secretKey, iv := svc.deriveKeyAndIV(password)

	block, err := aes.NewCipher(secretKey)
	if err != nil {
		return nil, err
	}

	// 使用 CBC 模式，IV 为零向量（Java 中通常也是 CBC + PKCS5Padding）
	mode := cipher.NewCBCEncrypter(block, iv)
	return mode, nil
}

func (svc *HttpCommandService) decryptDatas(ciphertextB64 string, secret string) ([]byte, error) {
	data, err := base64.StdEncoding.DecodeString(ciphertextB64)
	if err != nil {
		return nil, err
	}
	dst := make([]byte, len(data))
	secretKey, iv := svc.deriveKeyAndIV(secret)
	block, err := aes.NewCipher([]byte(secretKey))
	if err != nil {
		return nil, err
	}
	mode := cipher.NewCBCDecrypter(block, iv)
	mode.CryptBlocks(dst, data)
	dst, err = svc.pKCS7Unpadding(dst)
	if err != nil {
		return nil, err
	}
	return dst, nil
}

func (svc *HttpCommandService) pKCS7Unpadding(data []byte) ([]byte, error) {
	length := len(data)
	if length == 0 {
		return nil, errors.New("empty data")
	}
	paddingLen := int(data[length-1])
	if paddingLen > length || paddingLen > aes.BlockSize {
		return nil, errors.New("invalid padding")
	}
	return data[:length-paddingLen], nil
}

func (svc *HttpCommandService) checkRequestSign(dataBytes []byte, signList []string) bool {
	if len(OrderServiceConfig.ApiSecret) == 0 {
		return true
	}
	if len(signList) == 0 {
		return false
	}
	sign := signList[0]
	h := md5.New()
	h.Write(dataBytes)
	h.Write([]byte(OrderServiceConfig.ApiSecret))

	signVal := hex.EncodeToString(h.Sum(nil))
	if strings.ToLower(signVal) == strings.ToLower(sign) {
		return true
	}
	appLog.Errorf("invalid signature, need:%v, get:%v", signVal, sign)
	return false
}

func (svc *HttpCommandService) generateSignature(params map[string]string) string {
	// 1. 获取所有键并排序
	keys := make([]string, 0, len(params))
	for k := range params {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	// 2. 拼接字符串 key=value&...
	var builder strings.Builder
	for _, k := range keys {
		builder.WriteString(k)
		builder.WriteString("=")
		builder.WriteString(params[k])
		builder.WriteString("&")
	}
	msg := strings.TrimSuffix(builder.String(), "&")

	// 3. HMAC-SHA256
	mac := hmac.New(sha256.New, []byte(OrderServiceConfig.ApiSecret))
	mac.Write([]byte(msg))
	return hex.EncodeToString(mac.Sum(nil))
}

func (svc *HttpCommandService) signMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// 只处理 GET/POST 表单参数（也可解析 JSON body，见下文扩展）
		if err := r.ParseForm(); err != nil {
			responseBytes := svc._buildErrResponse(ARGS_ERR, "parse error")
			svc.sendIDIPResponse(w, http.StatusBadRequest, responseBytes)
			return
		}

		// 提取所有参数（排除 sign 本身）
		params := make(map[string]string)
		for k, v := range r.Form {
			if k == "sign" {
				continue
			}
			params[k] = v[0] // 取第一个值（若允许多值需调整）
		}

		// 获取客户端传来的签名
		providedSign := r.FormValue("sign")
		if providedSign == "" {
			responseBytes := svc._buildErrResponse(ARGS_ERR, "sign is missing")
			svc.sendIDIPResponse(w, http.StatusUnauthorized, responseBytes)
			return
		}

		// 计算期望签名并比较（使用 hmac.Equal 防止时序攻击）
		expectedSign := svc.generateSignature(params)
		if !hmac.Equal([]byte(providedSign), []byte(expectedSign)) {
			responseBytes := svc._buildErrResponse(ARGS_ERR, "sign is error")
			svc.sendIDIPResponse(w, http.StatusUnauthorized, responseBytes)
			return
		}

		// 验证通过，继续处理请求
		next.ServeHTTP(w, r)
	}
}

// CORS middleware to add appropriate headers to HTTP responses
func (svc *HttpCommandService) corsMiddleware(next http.HandlerFunc) http.HandlerFunc {
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

func (svc *HttpCommandService) startHttpApiServer(listenAddr string) {
	appLog.Info("start http api service !")
	mux := http.NewServeMux()
	mux.HandleFunc("/orderService", svc.corsMiddleware(svc.handleHttpRequest))
	err := http.ListenAndServe(listenAddr, mux)
	if err != nil {
		appLog.Panicf("fail to serve at %v", listenAddr)
	}
}
