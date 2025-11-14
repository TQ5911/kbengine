package CentralLogin
type YouximaoData struct {
	SdkUserName string `json:",omitempty"`
	UserID uint32 `json:",omitempty"`
	SdkUserID string `json:",omitempty"`
	ChannelID uint32 `json:",omitempty"`
	Username string `json:",omitempty"`
}
type YouximaoVerifyResult struct {
	State uint32 `json:",omitempty"`
	Data YouximaoData `json:",omitempty"`
}

type MsdkVerifyResult struct {
	Ret uint32 `json:",omitempty"`
	Msg string `json:",omitempty"`
	Seq string `json:",omitempty"`
}

type MsdkFriendVal struct {
	Openid string `json:"openid,omitempty"`
	UserName string `json:"user_name,omitempty"`
	Gender uint32 `json:"gender,omitempty"`
	PictureUrl string `json:"picture_url,omitempty"`
	Country string `json:"country,omitempty"`
	Provice string `json:"provice,omitempty"`
	City string `json:"city,omitempty"`
	Language string `json:"language,omitempty"`
}

type MsdkFriendResult struct {
	Ret uint32 `json:",omitempty"`
	Msg string `json:",omitempty"`
	Lists []MsdkFriendVal `json:",omitempty"`
	IsLost uint32 `json:",omitempty"`
}