package common

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

type CommandResponse struct {
	Result int32                  `json:"result,omitempty"`
	Msg    string                 `json:"msg,omitempty"`
	Body   []byte 				  `json:"body,omitempty"`
}

type MallCheckAccountRes struct {
	IsSuccess bool
}

const (
	MALL_HTTP_OK = iota + 200
	MALL_HTTP_DB_ERROR 
	MALL_HTTP_DB_NOT_EXIST
	MALL_HTTP_NOT_SAME_DID
	MALL_HTTP_UPDATE_MAIN_FAILED
	MALL_HTTP_MAIN_ACCOUNT
	MALL_HTTP_REDIS_ERROR
	MALL_HTTP_ACCOUNT_OFFLINE
	MALL_HTTP_SYNC_GAME_FAILED
	MALL_HTTP_TRANS_MAIN_FAILED
)