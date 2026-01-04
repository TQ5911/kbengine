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

type GetAllServerResponse struct {
	Servers []Server          `json:"servers"`
	KV      map[string]string `json:"kv"`
}
