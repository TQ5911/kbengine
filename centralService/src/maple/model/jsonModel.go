package model

type Server struct {
	Id              int    `json:"id"`
	ServerName      string `json:"server_name"`
	ZoneId          int    `json:"zone_id"`
	ZoneName        string `json:"zone_name"`
	GameServer      string `json:"game_server"`
	QueueServer     string `json:"queue_server"`
	CentralLogin    string `json:"central_login"`
	ServerGroup     int    `json:"server_group"`
	ServerState     int    `json:"server_state"`
	ServerFlagState int    `json:"server_flag_state"`
	Alias           string `json:"alias"`
	StartTime       int64  `json:"start_time"`
}
type ServerList struct {
	Servers []Server `json:"servers"`
}

type ZoneData struct {
	ZoneId   int    `json:"zone_id"`
	ZoneName string `json:"zone_name"`
}

type RemoveServerRequest struct {
	Id int `json:"id"`
}

type RemoveZoneRequest struct {
	ZoneId int `json:"zone_id"`
}

type GetAllServerResponse struct {
	Servers []Server          `json:"servers"`
	Zones   []ZoneData        `json:"zones"`
	KV      map[string]string `json:"kv"`
}

// 和服映射: from_server_id 是被合入的服, to_server_id 是合入目标服
type AddMergeRequest struct {
	FromServerId int `json:"from_server_id"`
	ToServerId   int `json:"to_server_id"`
}

// 拉取和服信息时的返回: 每条映射都"折叠"到最终的根服
// 例如 raw: 10002->10003, 10003->10001
// 输出 merge_map: {10002:10001, 10003:10001}
type GetMergeServerResponse struct {
	MergeMap map[int]int `json:"merge_map"`
}
