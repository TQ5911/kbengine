package crossTeamApp

import (
	pb "centralService/src/crossTeamServer/crossTeamApp/gameServerService"
	"sort"
	"time"
)

// Member 队伍成员。仅由所属 worker goroutine 访问，无需加锁。
// 注意：成员离线即退队，中心不维护在线/离线状态。
type Member struct {
	GbId     uint64
	ServerId uint32 // 本服 serverId（归属服，讨伐协调/邀请等按此路由）
	// RouteServerId 成员当前实际所在服 serverId（推送路由依据）：
	// 跨服副本中成员客户端连在跨服服上，由状态上报（ReportMemberStateRequest.serverId）刷新；
	// 瞬态字段，随下一次状态上报自愈
	RouteServerId uint32
	Name          string
	Level         int32
	School        int32
	Score         int32

	// 小组编号与组内位置：服务端内部数据，用于按 5 人一组渲染与位置调整。
	// 允许稀疏（退出不紧凑），pos 不严格限制在 1~5。
	GroupIdx int32
	Pos      int32

	// 成员展示补充（建队/申请/邀请/入队时由游戏服带入，中心只存不解读）
	Sex        int32
	PicFrameId int32
	OpenId     string

	// 语音状态三态（客户端位图由游戏服解包后经 setVoiceState 上传，中心只存不解读，
	// 全量下发与变更推送时原样带出；isBlockMics 不单独存，组包时按队伍 BlockedMembers 判定填充）
	EnableMics    bool
	EnableSpeaker bool
	InVoiceRoom   bool

	// 高频状态快照（3s 上报覆盖，随收随广播）
	Hp       int64
	MaxHp    int64
	SpaceNo  int32
	PosX     float32
	PosY     float32
	PosZ     float32
	ReportTS int64
}

func newMember(info *pb.MemberInfo) *Member {
	return &Member{
		GbId:          info.GbId,
		ServerId:      info.ServerId,
		RouteServerId: info.ServerId,
		Name:          info.Name,
		Level:         info.Level,
		School:        info.School,
		Score:         info.Score,
		GroupIdx:      info.GroupIdx,
		Pos:           info.Pos,
		Sex:           info.Sex,
		PicFrameId:    info.PicFrameId,
		OpenId:        info.OpenId,
		EnableMics:    info.EnableMics,
		EnableSpeaker: info.EnableSpeaker,
		InVoiceRoom:   info.InVoiceRoom,
	}
}

// toPb 转成员 pb。isBlockMics 与队伍 BlockedMembers 同源，这里不填，
// 由队伍侧组包（memberToPb/全量 toPb）按禁麦表判定填充
func (m *Member) toPb() *pb.MemberInfo {
	return &pb.MemberInfo{
		GbId:          m.GbId,
		ServerId:      m.ServerId,
		Name:          m.Name,
		Level:         m.Level,
		School:        m.School,
		Score:         m.Score,
		GroupIdx:      m.GroupIdx,
		Pos:           m.Pos,
		Sex:           m.Sex,
		PicFrameId:    m.PicFrameId,
		OpenId:        m.OpenId,
		EnableMics:    m.EnableMics,
		EnableSpeaker: m.EnableSpeaker,
		InVoiceRoom:   m.InVoiceRoom,
	}
}

func (m *Member) toStatePb() *pb.MemberState {
	return &pb.MemberState{
		GbId:          m.GbId,
		Hp:            m.Hp,
		MaxHp:         m.MaxHp,
		Level:         m.Level,
		Score:         m.Score,
		SpaceNo:       m.SpaceNo,
		PosX:          m.PosX,
		PosY:          m.PosY,
		PosZ:          m.PosZ,
		RouteServerId: m.RouteServerId,
	}
}

// ApplyInfo 入队申请（60s 超时，瞬态数据）
type ApplyInfo struct {
	Info        *pb.MemberInfo
	ApplyTS     int64
	ApplySource int32 // 申请来源（枚举复用本服 TeamJoinType，中心只存不解读）
}

// CrossTeamData 队伍权威数据（CrossTeamInfo）。仅由所属 worker goroutine 访问。
type CrossTeamData struct {
	TeamId      uint64
	Target      int32
	DungeonMap  int32 // 目标对应的讨伐副本（创建时由游戏服查表带入，目标不可改故创建后不变）
	MinLevel    int32
	MinScore    int32
	Password    string // 非空 = 私密队伍（不进列表/匹配池）
	Intro       string
	CaptainGbId uint64
	MaxNum      int32
	AutoMatch   bool
	AutoEnter   bool // 满员自动进入副本（队长设置，成员加入/选项设置时检查触发）
	Members     map[uint64]*Member
	Applicants  map[uint64]*ApplyInfo
	Invites     map[uint64]*pb.MemberInfo // 待应答邀请：inviteeGbId -> 邀请时快照的被邀请人信息
	CreateTS    int64
	UpdateTS    int64

	// 客户端接口对齐补充（isPublish 不单独存，按 Password 是否为空派生）
	DeputyGbId              uint64 // 副团长（setDeputy 任命/取消，唯一名额；0=无；随全量快照下发）
	LastDungeonFinishedTime int64  // 重进 CD 截止时刻（crusadeFinished 写入 = 完成时刻 + CRUSADE_REJOIN_CD_SECONDS；随全量数据下发）
	AutoMatchTime           int64  // 本队开启自动匹配的时间（客户端匹配 UI 用，关闭时清 0）

	// 本服链路两字段（创建时固化、永不变化，目标不可改故无需更新路径）：
	// IsCross=true 跨服走迁移链路；false 本服建空间本服进本，且仅允许本服玩家
	// （以 DunServer 为同服约束基准）。DunServer 为副本创建目标服，0=非法（讨伐启动报错）
	IsCross   bool
	DunServer uint32

	// 语音麦模式与禁麦表（语义沿用本服组队，经中心同步）
	MicsMode       int32
	BlockedMembers map[uint64]bool

	// 讨伐协调状态：完整状态机见 CRUSADE_STATE_*。
	// 检查中/空间创建中为瞬态；IN_DUNGEON 期间队伍禁止新申请/加入
	CrusadeState     int32 // CRUSADE_STATE_*
	CrusadeDungeonNo int32
	CrusadeDeadline  int64           // 检查/建空间超时时间戳（秒），worker sweep 处理
	CrusadeResults   map[uint64]bool // 成员条件检查结果汇总

	// 队伍标记（第四步 标记三件套）：PlayerMarks 存 MARK_TEAMMATE/MARK_ENEMY，
	// SceneMarks 存 MARK_SCENE；key 均为槽位 index（1~TEAM_MARK_MAX_SLOT）。
	// 变更经 markChangePush 单条增量下发（只发队长当前所在服）；随队伍解散一并销毁
	PlayerMarks        map[int32]*pb.MarkInfo
	SceneMarks         map[int32]*pb.MarkInfo
	OnlyCaptainCanMark bool // 仅队长可标记开关（本服 onlyCaptainCanMark 对应）
}

// isInDungeon 返回队伍是否已在副本中（通过讨伐状态机判断）
func (t *CrossTeamData) isInDungeon() bool {
	return t.CrusadeState == CRUSADE_STATE_IN_DUNGEON
}

func newCrossTeamData(req *pb.CreateTeamRequest) *CrossTeamData {
	now := time.Now().Unix()
	team := &CrossTeamData{
		TeamId:             req.TeamId,
		Target:             req.Target,
		DungeonMap:         req.DungeonMap,
		MinLevel:           req.MinLevel,
		MinScore:           req.MinScore,
		Password:           req.Password,
		Intro:              req.Intro,
		CaptainGbId:        req.Captain.GbId,
		MaxNum:             req.MaxNum,
		AutoMatch:          req.AutoMatch,
		AutoEnter:          req.AutoEnter,
		IsCross:            req.IsCross,
		DunServer:          req.DunServer,
		Members:            make(map[uint64]*Member),
		Applicants:         make(map[uint64]*ApplyInfo),
		Invites:            make(map[uint64]*pb.MemberInfo),
		CreateTS:           now,
		UpdateTS:           now,
		BlockedMembers:     make(map[uint64]bool),
		PlayerMarks:        make(map[int32]*pb.MarkInfo),
		SceneMarks:         make(map[int32]*pb.MarkInfo),
		OnlyCaptainCanMark: true,
	}
	// 创建即开启自动匹配：记录开启时间（客户端匹配 UI 用）
	if req.AutoMatch {
		team.AutoMatchTime = now
	}
	team.Members[req.Captain.GbId] = newMember(req.Captain)
	return team
}

// memberCnt 当前人数
func (t *CrossTeamData) memberCnt() int32 {
	return int32(len(t.Members))
}

// groupMembers 按 groupIdx 分组，返回 map[groupIdx][]*Member（每组内按 Pos 升序）
func (t *CrossTeamData) groupMembers() map[int32][]*Member {
	groups := make(map[int32][]*Member)
	for _, m := range t.Members {
		groups[m.GroupIdx] = append(groups[m.GroupIdx], m)
	}
	for _, list := range groups {
		sort.Slice(list, func(i, j int) bool {
			return list[i].Pos < list[j].Pos
		})
	}
	return groups
}

// maxGroupIdx 返回当前最大小组编号，无成员时返回 0
func (t *CrossTeamData) maxGroupIdx() int32 {
	var max int32
	for _, m := range t.Members {
		if m.GroupIdx > max {
			max = m.GroupIdx
		}
	}
	return max
}

// groupMemberCnt 返回指定小组当前人数
func (t *CrossTeamData) groupMemberCnt(groupIdx int32) int {
	cnt := 0
	for _, m := range t.Members {
		if m.GroupIdx == groupIdx {
			cnt++
		}
	}
	return cnt
}

// nextPos 返回指定小组下一个可用位置（当前最大 pos + 1，空组返回 1）
func (t *CrossTeamData) nextPos(groupIdx int32) int32 {
	var max int32
	for _, m := range t.Members {
		if m.GroupIdx == groupIdx && m.Pos > max {
			max = m.Pos
		}
	}
	if max == 0 {
		return 1
	}
	return max + 1
}

// assignNewMemberPos 为新入队成员分配 groupIdx/pos：
// 优先落入人数未满的小组末尾
func (t *CrossTeamData) assignNewMemberPos() (int32, int32) {
	groups := t.groupMembers()
	var bestGroup int32
	for idx, list := range groups {
		cnt := len(list)
		if cnt >= CROSS_TEAM_GROUP_SIZE {
			continue
		}
		bestGroup = min(bestGroup, idx)
	}
	return bestGroup, t.nextPos(bestGroup)
}

// checkConditionCode 校验等级/战力门槛，返回错误码（ERROR_CODE_SUCCESS 表示满足）：
// 先判等级再判战力，与原 checkCondition 合取语义一致，错误码细分为等级不足/战力不足
func (t *CrossTeamData) checkConditionCode(info *pb.MemberInfo) int32 {
	if info.Level < t.MinLevel {
		return ERROR_CODE_LEVEL_NOT_ENOUGH
	}
	if info.Score < t.MinScore {
		return ERROR_CODE_SCORE_NOT_ENOUGH
	}
	return ERROR_CODE_SUCCESS
}

// checkServerMatch 同服校验：本服目标队伍（!IsCross）仅允许 DunServer 同服玩家，
// 跨服队伍不做限制（落点：joinApply/replyInvite 同意/matchJoin，见 D3-1）
func (t *CrossTeamData) checkServerMatch(serverId uint32) bool {
	return t.IsCross || serverId == t.DunServer
}

// pickNewCaptain 从剩余成员中选新队长。
// 离线即退队，剩余成员均可作为新队长；无成员时返回 0。
// 调用方应先把老队长移出 Members
func (t *CrossTeamData) pickNewCaptain() uint64 {
	for gbId := range t.Members {
		return gbId
	}
	return 0
}

// serverIds 成员当前所在服去重列表（面向客户端推送的路由依据，跨服副本中为跨服服）
func (t *CrossTeamData) serverIds() []uint32 {
	set := make(map[uint32]bool)
	for _, m := range t.Members {
		set[m.RouteServerId] = true
	}
	out := make([]uint32, 0, len(set))
	for serverId := range set {
		out = append(out, serverId)
	}
	return out
}

// serverGbIds 按成员当前所在服分组 gbId（状态广播/聊天/成员变更等推送按此路由）
func (t *CrossTeamData) serverGbIds() map[uint32][]uint64 {
	out := make(map[uint32][]uint64)
	for _, m := range t.Members {
		out[m.RouteServerId] = append(out[m.RouteServerId], m.GbId)
	}
	return out
}

// homeServerIds 成员本服去重列表（讨伐协调消息路由依据：CrusadeGo 驱动本服 Avatar 迁移）
func (t *CrossTeamData) homeServerIds() []uint32 {
	set := make(map[uint32]bool)
	for _, m := range t.Members {
		set[m.ServerId] = true
	}
	out := make([]uint32, 0, len(set))
	for serverId := range set {
		out = append(out, serverId)
	}
	return out
}

// homeServerGbIds 按成员本服分组 gbId（讨伐条件检查/中止等发给本服 Avatar 的协调消息用）
func (t *CrossTeamData) homeServerGbIds() map[uint32][]uint64 {
	out := make(map[uint32][]uint64)
	for _, m := range t.Members {
		out[m.ServerId] = append(out[m.ServerId], m.GbId)
	}
	return out
}

// memberToPb 转成员 pb 并按队伍禁麦表填充 isBlockMics（与 blockedMembers 同源下发）
func (t *CrossTeamData) memberToPb(m *Member) *pb.MemberInfo {
	info := m.toPb()
	info.IsBlockMics = t.BlockedMembers[m.GbId]
	return info
}

// marksOfType 按标记类型返回所属容器（MARK_SCENE 入 SceneMarks，其余入 PlayerMarks）
func (t *CrossTeamData) marksOfType(markType int32) map[int32]*pb.MarkInfo {
	if markType == MARK_TYPE_SCENE {
		return t.SceneMarks
	}
	return t.PlayerMarks
}

// marksToPb 标记 map 转 pb 列表（按槽位 index 升序，保证全量下发顺序稳定）
func marksToPb(marks map[int32]*pb.MarkInfo) []*pb.MarkInfo {
	idxList := make([]int32, 0, len(marks))
	for idx := range marks {
		idxList = append(idxList, idx)
	}
	sort.Slice(idxList, func(i, j int) bool { return idxList[i] < idxList[j] })
	out := make([]*pb.MarkInfo, 0, len(marks))
	for _, idx := range idxList {
		out = append(out, marks[idx])
	}
	return out
}

// toPb 转全量 pb（TeamDataResp 用）
func (t *CrossTeamData) toPb() *pb.CrossTeamInfo {
	info := &pb.CrossTeamInfo{
		TeamId:                  t.TeamId,
		Target:                  t.Target,
		DungeonMap:              t.DungeonMap,
		MinLevel:                t.MinLevel,
		MinScore:                t.MinScore,
		Password:                t.Password,
		Intro:                   t.Intro,
		CaptainGbId:             t.CaptainGbId,
		MaxNum:                  t.MaxNum,
		AutoMatch:               t.AutoMatch,
		AutoEnter:               t.AutoEnter,
		InDungeon:               t.isInDungeon(),
		CreateTS:                t.CreateTS,
		UpdateTS:                t.UpdateTS,
		MicsMode:                t.MicsMode,
		IsPublish:               t.Password == "", // 公开队伍派生：无密码即公开
		DeputyGbId:              t.DeputyGbId,
		LastDungeonFinishedTime: t.LastDungeonFinishedTime,
		AutoMatchTime:           t.AutoMatchTime,
		IsCross:                 t.IsCross,
		DunServer:               t.DunServer,
		MemberNum:               t.memberCnt(),
		OnlyCaptainCanMark:      t.OnlyCaptainCanMark,
		PlayerMarks:             marksToPb(t.PlayerMarks),
		SceneMarks:              marksToPb(t.SceneMarks),
		Members:                 make([]*pb.MemberInfo, 0, len(t.Members)),
	}
	for gbId := range t.BlockedMembers {
		info.BlockedMembers = append(info.BlockedMembers, gbId)
	}
	members := make([]*Member, 0, len(t.Members))
	for _, m := range t.Members {
		members = append(members, m)
	}
	sort.Slice(members, func(i, j int) bool {
		if members[i].GroupIdx != members[j].GroupIdx {
			return members[i].GroupIdx < members[j].GroupIdx
		}
		return members[i].Pos < members[j].Pos
	})
	for _, m := range members {
		info.Members = append(info.Members, t.memberToPb(m))
	}
	return info
}

// toListItemPb 转队伍列表条目（队长预览信息随条目下发，问题记录#4）
func (t *CrossTeamData) toListItemPb() *pb.TeamListItem {
	captain := &pb.MemberBasicInfo{}
	if m, ok := t.Members[t.CaptainGbId]; ok {
		captain = &pb.MemberBasicInfo{
			GbId:     m.GbId,
			ServerId: m.ServerId,
			Name:     m.Name,
			Sex:      m.Sex,
			School:   m.School,
			Score:    m.Score,
			Level:    m.Level,
		}
	}
	return &pb.TeamListItem{
		TeamId:        t.TeamId,
		Target:        t.Target,
		MinLevel:      t.MinLevel,
		MinScore:      t.MinScore,
		Captain:       captain,
		MemberCnt:     t.memberCnt(),
		MaxNum:        t.MaxNum,
		Intro:         t.Intro,
		IsPublish:     t.Password == "",
		AutoMatchTime: t.AutoMatchTime,
	}
}
