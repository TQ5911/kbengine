package crossTeamApp

import (
	"centralService/src/appLog"
	pb "centralService/src/crossTeamServer/crossTeamApp/gameServerService"
	"sort"
	"time"

	"google.golang.org/protobuf/proto"
)

// ---------------------------------------------------------------------------
// 队伍业务逻辑。除特别说明外，本文件函数均只在队伍所属 worker goroutine 内执行
// （由 gameServerService.go 的 RPC 处理器经 dispatcher.Dispatch 投递），
// 因此可以直接读写 worker 持有的队伍数据，无需加锁。
// 对外推送统一经 sendToServer 按成员当前所在服路由（Member.RouteServerId，
// 跨服副本中成员客户端连在跨服服上，随状态上报刷新）；
// 讨伐协调消息（检查/迁移/中止）例外，按成员本服路由（Member.ServerId，见 crusadeOps.go）。
// ---------------------------------------------------------------------------

// checkCaptain 中心权威校验操作人是否为当前队长。
// 游戏服 Stub 缓存可能因异步推送延迟而失效，因此必须在中心再核一次。
func checkCaptain(team *CrossTeamData, captainGbId uint64) bool {
	return captainGbId != 0 && captainGbId == team.CaptainGbId
}

// replyOpTarget 操作结果回执（显式 target）：直接经请求来源连接回给操作发起人所在服
func replyOpTarget(gss *GameServerService, uuid uint64, code int32, teamId uint64, gbId uint64, target int32) {
	if gss == nil || gss.ServerEndPoint == nil || gss.GetClientEndPoint() == nil {
		return
	}
	_, err := gss.GetClientEndPoint().(*pb.GameServerClient).TeamOpResult(&pb.TeamOpResultMsg{
		Uuid:       uuid,
		ResultCode: code,
		TeamId:     teamId,
		GbId:       gbId,
		Target:     target,
	})
	if err != nil {
		appLog.Errorf("send teamOpResult failed, serverId=%d teamId=%d code=%d err=%v", gss.serverId, teamId, code, err)
	}
}

// replyOp 操作结果回执：target 按 teamId 从 worker 队伍数据解析（队伍已不存在/未建成时为 0，
// 客户端按通用处理）；无 worker 上下文或以请求目标为准的入口（EnterMatchPool/createTeam 失败）走 replyOpTarget
func (w *teamWorker) replyOp(gss *GameServerService, uuid uint64, code int32, teamId uint64, gbId uint64) {
	target := int32(0)
	if team := w.getTeam(teamId); team != nil {
		target = team.Target
	}
	replyOpTarget(gss, uuid, code, teamId, gbId, target)
}

// notifyReplyApply 向申请人所在服发送入队申请结果通知（申请时与队长应答统一通道，
// 携带目标/门槛/密码/申请来源供客户端失败交互；team 为 nil 时相关字段下发零值）
func (cta *CrossTeamApp) notifyReplyApply(serverId uint32, teamId uint64, applicantGbId uint64, code int32, applySource int32, team *CrossTeamData) {
	msg := &pb.ReplyApplyNotifyMsg{
		TeamId:        teamId,
		ApplicantGbId: applicantGbId,
		ResultCode:    code,
		ApplySource:   applySource,
	}
	if team != nil {
		msg.Target = team.Target
		msg.Password = team.Password
		msg.RequireLevel = team.MinLevel
		msg.RequireScore = team.MinScore
	}
	cta.sendToServer(serverId, "replyApplyNotify", func(client *pb.GameServerClient) error {
		_, err := client.ReplyApplyNotify(msg)
		return err
	})
}

// pushOpResult 操作结果主动推送（非请求回执，uuid=0）：经 sendToServer 推到目标玩家所在服，
// 游戏服按 gbId 路由到本人 cell；与 replyOp 回执共用 teamOpResult 通道与客户端协议
// （撮合入队作废/队长申请结果等异步事件用）
func (cta *CrossTeamApp) pushOpResult(serverId uint32, teamId uint64, gbId uint64, code int32, target int32) {
	cta.sendToServer(serverId, "teamOpResult", func(client *pb.GameServerClient) error {
		_, err := client.TeamOpResult(&pb.TeamOpResultMsg{
			ResultCode: code,
			TeamId:     teamId,
			GbId:       gbId,
			Target:     target,
		})
		return err
	})
}

// pushTeamCreateSuccess 创建队伍成功：只推创建人本人
func (cta *CrossTeamApp) pushTeamCreateSuccess(team *CrossTeamData) {
	captain := team.Members[team.CaptainGbId]
	if captain == nil {
		return
	}
	msg := &pb.TeamCreateSuccessPushMsg{Team: team.toPb(), ReceiverGbIds: []uint64{team.CaptainGbId}}
	cta.sendToServer(captain.RouteServerId, "teamCreateSuccessPush", func(client *pb.GameServerClient) error {
		_, err := client.TeamCreateSuccessPush(msg)
		return err
	})
}

// pushTeamJoinSuccess 新成员入队成功：只推新成员本人所在服、只发本人
func (cta *CrossTeamApp) pushTeamJoinSuccess(team *CrossTeamData, serverId uint32, gbId uint64) {
	cta.sendToServer(serverId, "teamJoinSuccessPush", func(client *pb.GameServerClient) error {
		_, err := client.TeamJoinSuccessPush(&pb.TeamJoinSuccessPushMsg{Team: team.toPb(), ReceiverGbIds: []uint64{gbId}})
		return err
	})
}

// pushMemberJoin 进队推送：按服逐一定制 receiverGbIds
func (cta *CrossTeamApp) pushMemberJoin(gbIdsByServer map[uint32][]uint64, msg *pb.MemberJoinPushMsg) {
	appLog.Debugw("pushMemberJoin", "teamId", msg.TeamId, "gbId", msg.Member.GetGbId())
	for serverId, gbIds := range gbIdsByServer {
		perServerMsg := proto.Clone(msg).(*pb.MemberJoinPushMsg)
		perServerMsg.ReceiverGbIds = gbIds
		cta.sendToServer(serverId, "memberJoinPush", func(client *pb.GameServerClient) error {
			_, err := client.MemberJoinPush(perServerMsg)
			return err
		})
	}
}

// pushMemberLeave 离队/被踢/离线退出推送：按服逐一定制 receiverGbIds
func (cta *CrossTeamApp) pushMemberLeave(gbIdsByServer map[uint32][]uint64, msg *pb.MemberLeavePushMsg) {
	appLog.Debugw("pushMemberLeave", "teamId", msg.TeamId, "gbId", msg.GbId, "reason", msg.Reason)
	for serverId, gbIds := range gbIdsByServer {
		perServerMsg := proto.Clone(msg).(*pb.MemberLeavePushMsg)
		perServerMsg.ReceiverGbIds = gbIds
		cta.sendToServer(serverId, "memberLeavePush", func(client *pb.GameServerClient) error {
			_, err := client.MemberLeavePush(perServerMsg)
			return err
		})
	}
}

// pushCaptainChange 队长变更推送：按服逐一定制 receiverGbIds
func (cta *CrossTeamApp) pushCaptainChangeMsg(gbIdsByServer map[uint32][]uint64, msg *pb.CaptainChangePushMsg) {
	appLog.Debugw("pushCaptainChange", "teamId", msg.TeamId, "newCaptainGbId", msg.NewCaptainGbId)
	for serverId, gbIds := range gbIdsByServer {
		perServerMsg := proto.Clone(msg).(*pb.CaptainChangePushMsg)
		perServerMsg.ReceiverGbIds = gbIds
		cta.sendToServer(serverId, "captainChangePush", func(client *pb.GameServerClient) error {
			_, err := client.CaptainChangePush(perServerMsg)
			return err
		})
	}
}

// pushDeputyChangeMsg 副团长变更推送：按服逐一定制 receiverGbIds（deputyGbId=0 表示取消）
func (cta *CrossTeamApp) pushDeputyChangeMsg(gbIdsByServer map[uint32][]uint64, msg *pb.DeputyChangePushMsg) {
	appLog.Debugw("pushDeputyChange", "teamId", msg.TeamId, "deputyGbId", msg.DeputyGbId)
	for serverId, gbIds := range gbIdsByServer {
		perServerMsg := proto.Clone(msg).(*pb.DeputyChangePushMsg)
		perServerMsg.ReceiverGbIds = gbIds
		cta.sendToServer(serverId, "deputyChangePush", func(client *pb.GameServerClient) error {
			_, err := client.DeputyChangePush(perServerMsg)
			return err
		})
	}
}

// pushMarkChange 队伍标记变更推送：单条增量，只发队长当前所在服（RouteServerId）。
// 标记仅副本内可用，打本时全队均在副本所在服，其他服无接收意义；
// receiverGbIds 带全队 gbId，由该服 Stub 按本服实有成员路由转发
func (cta *CrossTeamApp) pushMarkChange(team *CrossTeamData, changeType int32, mark *pb.MarkInfo) {
	captain, ok := team.Members[team.CaptainGbId]
	if !ok {
		return
	}
	msg := &pb.MarkChangePushMsg{
		TeamId:             team.TeamId,
		ChangeType:         changeType,
		Mark:               mark,
		OnlyCaptainCanMark: team.OnlyCaptainCanMark,
		ReceiverGbIds:      make([]uint64, 0, len(team.Members)),
	}
	for gbId := range team.Members {
		msg.ReceiverGbIds = append(msg.ReceiverGbIds, gbId)
	}
	cta.sendToServer(captain.RouteServerId, "markChangePush", func(client *pb.GameServerClient) error {
		_, err := client.MarkChangePush(msg)
		return err
	})
}

// pushTeamDisband 解散推送：按服逐一定制 receiverGbIds（解散前快照）
func (cta *CrossTeamApp) pushTeamDisband(gbIdsByServer map[uint32][]uint64, msg *pb.TeamDisbandPushMsg) {
	appLog.Debugw("pushTeamDisband", "teamId", msg.TeamId)
	for serverId, gbIds := range gbIdsByServer {
		perServerMsg := proto.Clone(msg).(*pb.TeamDisbandPushMsg)
		perServerMsg.ReceiverGbIds = gbIds
		cta.sendToServer(serverId, "teamDisbandPush", func(client *pb.GameServerClient) error {
			_, err := client.TeamDisbandPush(perServerMsg)
			return err
		})
	}
}

// pushTeamSettingsChange 队伍设置变更推送：按服逐一定制 receiverGbIds
func (cta *CrossTeamApp) pushTeamSettingsChange(gbIdsByServer map[uint32][]uint64, msg *pb.TeamSettingsChangePushMsg) {
	appLog.Debugw("pushTeamSettingsChange", "teamId", msg.TeamId, "autoEnter", msg.AutoEnter)
	for serverId, gbIds := range gbIdsByServer {
		perServerMsg := proto.Clone(msg).(*pb.TeamSettingsChangePushMsg)
		perServerMsg.ReceiverGbIds = gbIds
		cta.sendToServer(serverId, "teamSettingsChangePush", func(client *pb.GameServerClient) error {
			_, err := client.TeamSettingsChangePush(perServerMsg)
			return err
		})
	}
}

// pushTeamAutoMatchChange 自动匹配开关变更推送：按服逐一定制 receiverGbIds
func (cta *CrossTeamApp) pushTeamAutoMatchChange(gbIdsByServer map[uint32][]uint64, msg *pb.TeamAutoMatchChangePushMsg) {
	appLog.Debugw("pushTeamAutoMatchChange", "teamId", msg.TeamId, "autoMatch", msg.AutoMatch)
	for serverId, gbIds := range gbIdsByServer {
		perServerMsg := proto.Clone(msg).(*pb.TeamAutoMatchChangePushMsg)
		perServerMsg.ReceiverGbIds = gbIds
		cta.sendToServer(serverId, "teamAutoMatchChangePush", func(client *pb.GameServerClient) error {
			_, err := client.TeamAutoMatchChangePush(perServerMsg)
			return err
		})
	}
}

// pushTeamMicsModeChange 调整麦模式推送：按服逐一定制 receiverGbIds
func (cta *CrossTeamApp) pushTeamMicsModeChange(gbIdsByServer map[uint32][]uint64, msg *pb.TeamMicsModeChangePushMsg) {
	appLog.Debugw("pushTeamMicsModeChange", "teamId", msg.TeamId, "micsMode", msg.MicsMode)
	for serverId, gbIds := range gbIdsByServer {
		perServerMsg := proto.Clone(msg).(*pb.TeamMicsModeChangePushMsg)
		perServerMsg.ReceiverGbIds = gbIds
		cta.sendToServer(serverId, "teamMicsModeChangePush", func(client *pb.GameServerClient) error {
			_, err := client.TeamMicsModeChangePush(perServerMsg)
			return err
		})
	}
}

// pushMemberMicBlock 禁麦/解除禁麦推送：按服逐一定制 receiverGbIds
func (cta *CrossTeamApp) pushMemberMicBlock(gbIdsByServer map[uint32][]uint64, msg *pb.MemberMicBlockPushMsg) {
	appLog.Debugw("pushMemberMicBlock", "teamId", msg.TeamId, "gbId", msg.GbId, "blocked", msg.Blocked)
	for serverId, gbIds := range gbIdsByServer {
		perServerMsg := proto.Clone(msg).(*pb.MemberMicBlockPushMsg)
		perServerMsg.ReceiverGbIds = gbIds
		cta.sendToServer(serverId, "memberMicBlockPush", func(client *pb.GameServerClient) error {
			_, err := client.MemberMicBlockPush(perServerMsg)
			return err
		})
	}
}

// pushMemberVoiceState 成员语音状态变更推送：按服逐一定制 receiverGbIds
func (cta *CrossTeamApp) pushMemberVoiceState(gbIdsByServer map[uint32][]uint64, msg *pb.MemberVoiceStatePushMsg) {
	appLog.Debugw("pushMemberVoiceState", "teamId", msg.TeamId, "gbId", msg.GbId)
	for serverId, gbIds := range gbIdsByServer {
		perServerMsg := proto.Clone(msg).(*pb.MemberVoiceStatePushMsg)
		perServerMsg.ReceiverGbIds = gbIds
		cta.sendToServer(serverId, "memberVoiceStatePush", func(client *pb.GameServerClient) error {
			_, err := client.MemberVoiceStatePush(perServerMsg)
			return err
		})
	}
}

// notifyApplyRemove 申请移除通知：申请被同意/拒绝/超时清理时向队长所在服推送，
// 客户端据此把申请人从申请列表移除（副团长功能期可扩展 receivers）
func (cta *CrossTeamApp) notifyApplyRemove(serverId uint32, teamId uint64, applicantGbId uint64, captainGbId uint64) {
	cta.sendToServer(serverId, "applyRemoveNotify", func(client *pb.GameServerClient) error {
		_, err := client.ApplyRemoveNotify(&pb.ApplyRemoveNotifyMsg{
			TeamId:        teamId,
			ApplicantGbId: applicantGbId,
			ReceiverGbIds: []uint64{captainGbId},
		})
		return err
	})
}

func (cta *CrossTeamApp) pushCaptainChange(team *CrossTeamData) {
	cta.pushCaptainChangeMsg(team.serverGbIds(), &pb.CaptainChangePushMsg{
		TeamId:         team.TeamId,
		NewCaptainGbId: team.CaptainGbId,
	})
}

// pushDeputyChange 副团长变更推送（任命/取消，全队；deputyGbId=0 表示取消）
func (cta *CrossTeamApp) pushDeputyChange(team *CrossTeamData) {
	cta.pushDeputyChangeMsg(team.serverGbIds(), &pb.DeputyChangePushMsg{
		TeamId:     team.TeamId,
		DeputyGbId: team.DeputyGbId,
	})
}

// pushBecomeCaptainApply 申请成为队长提示推送：推给队长本人（含申请人展示信息）；
// 按队长当前路由服发送（跨服副本中队长客户端连在跨服服，随状态上报刷新）
func (cta *CrossTeamApp) pushBecomeCaptainApply(team *CrossTeamData, applicant *Member) {
	captain := team.Members[team.CaptainGbId]
	if captain == nil {
		return
	}
	msg := &pb.BecomeCaptainApplyPushMsg{
		TeamId: team.TeamId,
		Applicant: &pb.MemberBasicInfo{
			GbId:     applicant.GbId,
			ServerId: applicant.ServerId,
			Name:     applicant.Name,
			Sex:      applicant.Sex,
			School:   applicant.School,
			Score:    applicant.Score,
		},
		ReceiverGbIds: []uint64{team.CaptainGbId},
	}
	cta.sendToServer(captain.RouteServerId, "becomeCaptainApplyPush", func(client *pb.GameServerClient) error {
		_, err := client.BecomeCaptainApplyPush(msg)
		return err
	})
}

// pushAdjustMemberPos 成员位置调整推送：按服逐一定制 receiverGbIds，参数原样下发
func (cta *CrossTeamApp) pushAdjustMemberPos(team *CrossTeamData, in *pb.AdjustMemberPosRequest) {
	msg := &pb.AdjustMemberPosPushMsg{
		TeamId:      in.TeamId,
		SrcGbId:     in.SrcGbId,
		SrcGroupIdx: in.SrcGroupIdx,
		DstGbId:     in.DstGbId,
		DstGroupIdx: in.DstGroupIdx,
	}
	for serverId, gbIds := range team.serverGbIds() {
		perServerMsg := proto.Clone(msg).(*pb.AdjustMemberPosPushMsg)
		perServerMsg.ReceiverGbIds = gbIds
		cta.sendToServer(serverId, "adjustMemberPosPush", func(client *pb.GameServerClient) error {
			_, err := client.AdjustMemberPosPush(perServerMsg)
			return err
		})
	}
}

// ---------------------------------------------------------------------------
// 队伍撮合摘要事件同步（team worker -> target pool goroutine）
// ---------------------------------------------------------------------------

// syncTeamSummary 队伍撮合相关数据（门槛/人数/autoMatch 等）变更后同步摘要到目标池
func (cta *CrossTeamApp) syncTeamSummary(team *CrossTeamData) {
	cta.matchPools.UpsertTeamSummary(&teamSummary{
		teamId:    team.TeamId,
		target:    team.Target,
		minLevel:  team.MinLevel,
		minScore:  team.MinScore,
		maxNum:    team.MaxNum,
		memberCnt: team.memberCnt(),
		createTS:  team.CreateTS,
		isCross:   team.IsCross,
		dunServer: team.DunServer,
		matchable: team.Password == "" && team.AutoMatch && !team.isInDungeon(),
	})
}

// removeTeamSummary 队伍解散/目标改走时从目标池摘除摘要
func (cta *CrossTeamApp) removeTeamSummary(teamId uint64, target int32) {
	cta.matchPools.RemoveTeamSummary(teamId, target)
}

// addMember 加入成员（调用方已完成全部校验）：落数据 + 索引 + 出匹配池 + 推送。
// 推送语义：新成员本人所在服收全量 TeamJoinSuccessPush，全体成员所在服收"新增成员"增量
// 新成员入队落位：优先填入人数最少且未满的小组末尾，否则新建小组。
func (cta *CrossTeamApp) addMember(w *teamWorker, team *CrossTeamData, info *pb.MemberInfo) {
	info.GroupIdx, info.Pos = team.assignNewMemberPos()
	team.Members[info.GbId] = newMember(info)
	cta.setPlayerTeam(info.GbId, team.TeamId)
	// 入队后若曾在散人匹配池中则强制出池
	cta.matchPools.RemovePlayer(info.GbId)
	// 新成员本人收全量队伍数据（经 receiverGbIds 指定，仅本人）
	cta.pushTeamJoinSuccess(team, info.ServerId, info.GbId)
	// 全体成员收"新增成员"增量（新成员所在服重复覆盖一次全量，幂等无害）；
	// isBlockMics 与全量组包同口径，按队伍禁麦表判定填充（禁麦表不清退队者，兜底重入队场景）
	info.IsBlockMics = team.BlockedMembers[info.GbId]
	cta.pushMemberJoin(team.serverGbIds(), &pb.MemberJoinPushMsg{
		TeamId: team.TeamId,
		Member: info,
	})
	cta.syncTeamSummary(team)
	cta.markTeamListDirty(team.Target)
	appLog.Infof(
		"member join team, teamId=%d gbId=%d serverId=%d members=%d",
		team.TeamId,
		info.GbId,
		info.ServerId,
		team.memberCnt(),
	)

	// 满员自动进本：开启开关且本次加入后满员则自动发起讨伐
	cta.maybeAutoCrusade(w, team)
}

// removeMember 移出成员：删数据 + 删索引 + "移除成员"增量（被移出者由游戏服侧清空）；
// 队伍空则解散
func (cta *CrossTeamApp) removeMember(w *teamWorker, team *CrossTeamData, gbId uint64, reason int32) {
	if _, ok := team.Members[gbId]; !ok {
		return
	}
	// 先取路由（含被移出者所在服与被移出者本人），再删数据
	gbIdsByServer := team.serverGbIds()
	delete(team.Members, gbId)
	cta.removePlayerTeam(gbId)
	cta.matchPools.RemovePlayer(gbId)
	cta.pushMemberLeave(gbIdsByServer, &pb.MemberLeavePushMsg{
		TeamId: team.TeamId,
		GbId:   gbId,
		Reason: reason,
	})
	appLog.Infof(
		"member removed from team, teamId=%d gbId=%d reason=%d members=%d",
		team.TeamId,
		gbId,
		reason,
		team.memberCnt(),
	)

	if team.memberCnt() == 0 {
		cta.disbandTeam(w, team)
		return
	}
	// 被移出者是队长（离线/主动离队）时立即移交：从剩余成员中选新队长（优先在线，本服同款语义）
	if gbId == team.CaptainGbId {
		team.CaptainGbId = team.pickNewCaptain()
		cta.pushCaptainChange(team)
	}
	cta.syncTeamSummary(team)
	cta.markTeamListDirty(team.Target)
}

// disbandTeam 解散队伍："解散"增量通知全体（ ex ）成员所在服 + 清索引
func (cta *CrossTeamApp) disbandTeam(w *teamWorker, team *CrossTeamData) {
	// 先取路由与接收者快照（解散前全体成员），再删数据
	gbIdsByServer := team.serverGbIds()
	for gbId := range team.Members {
		cta.removePlayerTeam(gbId)
	}
	delete(w.teams, team.TeamId)
	cta.pushTeamDisband(gbIdsByServer, &pb.TeamDisbandPushMsg{
		TeamId: team.TeamId,
	})
	cta.removeTeamSummary(team.TeamId, team.Target)
	cta.markTeamListDirty(team.Target)
	appLog.Infof("team disbanded, teamId=%d", team.TeamId)
}

// handleMemberOffline 成员离线：离线即离队（本服同款语义，队长也不例外——
// 队长被移出时由 removeMember 立即从剩余成员中移交队长；队伍空则解散）
func (cta *CrossTeamApp) handleMemberOffline(w *teamWorker, team *CrossTeamData, gbId uint64) {
	if _, ok := team.Members[gbId]; !ok {
		return
	}
	cta.removeMember(w, team, gbId, LEAVE_REASON_OFFLINE)
}

// ---------------------------------------------------------------------------
// 以下为各 RPC 的业务实现（worker 上下文）
// ---------------------------------------------------------------------------

func (cta *CrossTeamApp) createTeam(w *teamWorker, gss *GameServerService, in *pb.CreateTeamRequest) {
	captainGbId := uint64(0)
	if in.Captain != nil {
		captainGbId = in.Captain.GbId
	}
	if in.TeamId == 0 || in.Captain == nil || in.Target <= 0 || in.MaxNum <= 0 ||
		in.MinLevel < 0 || in.MinScore < 0 {
		replyOpTarget(gss, in.Uuid, ERROR_CODE_INVALID_PARAM, in.TeamId, captainGbId, in.Target)
		return
	}
	if w.getTeam(in.TeamId) != nil {
		replyOpTarget(gss, in.Uuid, ERROR_CODE_DUPLICATED_TEAM, in.TeamId, captainGbId, in.Target)
		return
	}
	if cta.getPlayerTeam(captainGbId) != 0 {
		replyOpTarget(gss, in.Uuid, ERROR_CODE_ALREADY_IN_TEAM, in.TeamId, captainGbId, in.Target)
		return
	}

	team := newCrossTeamData(in)
	w.teams[team.TeamId] = team
	cta.setPlayerTeam(captainGbId, team.TeamId)

	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, team.TeamId, captainGbId)

	cta.pushTeamCreateSuccess(team)
	cta.syncTeamSummary(team)
	cta.markTeamListDirty(team.Target)

	appLog.Infof(
		"create team, teamId=%d target=%d captain=%d serverId=%d autoMatch=%v",
		team.TeamId,
		team.Target,
		captainGbId,
		in.Captain.ServerId,
		team.AutoMatch,
	)
}

func (cta *CrossTeamApp) joinApply(w *teamWorker, gss *GameServerService, in *pb.JoinApplyRequest) {
	applicant := in.Applicant
	team := w.getTeam(in.TeamId)
	// 申请结果（成功/失败）统一经 notifyReplyApply 主动通知申请人所在服，
	// 不再走 TeamOpResult uuid 回执（游戏服侧同步不再注册 remoteCallCache）
	replyResult := func(code int32) {
		cta.notifyReplyApply(applicant.ServerId, in.TeamId, applicant.GbId, code, in.ApplySource, team)
	}
	if team == nil {
		replyResult(ERROR_CODE_TEAM_NOT_FOUND)
		return
	}
	if team.isInDungeon() {
		replyResult(ERROR_CODE_TEAM_IN_DUNGEON)
		return
	}
	// 本服目标队伍仅允许本服玩家（D3-1，以 dunServer 为同服约束基准）
	if !team.checkServerMatch(applicant.ServerId) {
		replyResult(ERROR_CODE_SERVER_MISMATCH)
		return
	}
	if cta.getPlayerTeam(applicant.GbId) != 0 {
		replyResult(ERROR_CODE_ALREADY_IN_TEAM)
		return
	}
	if team.memberCnt() >= team.MaxNum {
		replyResult(ERROR_CODE_TEAM_FULL)
		return
	}
	if len(team.Applicants) >= TEAM_APPLY_MAX_NUM {
		replyResult(ERROR_CODE_APPLY_LIST_FULL)
		return
	}
	if code := team.checkConditionCode(applicant); code != ERROR_CODE_SUCCESS {
		replyResult(code)
		return
	}
	// 密码细分：目标队伍有密码而申请未携带 -> 需要密码；携带但不匹配 -> 密码错误
	if team.Password != "" {
		if in.Password == "" {
			replyResult(ERROR_CODE_NEED_PASSWORD)
			return
		}
		if team.Password != in.Password {
			replyResult(ERROR_CODE_PASSWORD_WRONG)
			return
		}
	}

	// 重复申请刷新时间戳即可
	team.Applicants[applicant.GbId] = &ApplyInfo{
		Info:        applicant,
		ApplyTS:     time.Now().Unix(),
		ApplySource: in.ApplySource,
	}

	// 通知队长所在服（captainGbId 随推送下发，游戏服 Stub 不再维护队伍缓存）
	if captain, ok := team.Members[team.CaptainGbId]; ok {
		cta.sendToServer(captain.ServerId, "joinApplyNotify", func(client *pb.GameServerClient) error {
			_, err := client.JoinApplyNotify(&pb.JoinApplyNotifyMsg{
				TeamId:      team.TeamId,
				Applicant:   applicant,
				CaptainGbId: team.CaptainGbId,
				Target:      team.Target,
				ApplySource: in.ApplySource,
			})
			return err
		})
	}
	appLog.Infof("join apply, teamId=%d applicant=%d serverId=%d", in.TeamId, applicant.GbId, applicant.ServerId)
}

// reqJoin 免审批快速入队（本服 reqJoinTeam 对应）：不落地申请记录，
// 校验口径与 joinApply 一致（本服目标队约束/密码细分 25/5/门槛细分 6/26），通过即直接入队；
// 结果经 notifyReplyApply 主动通知申请人（applySource 下发 0，与审批流共用客户端通道），不走 uuid 回执
func (cta *CrossTeamApp) reqJoin(w *teamWorker, gss *GameServerService, in *pb.ReqJoinRequest) {
	applicant := in.Applicant
	team := w.getTeam(in.TeamId)
	replyResult := func(code int32) {
		cta.notifyReplyApply(applicant.ServerId, in.TeamId, applicant.GbId, code, 0, team)
	}
	if team == nil {
		replyResult(ERROR_CODE_TEAM_NOT_FOUND)
		return
	}
	if team.isInDungeon() {
		replyResult(ERROR_CODE_TEAM_IN_DUNGEON)
		return
	}
	// 本服目标队伍仅允许本服玩家（D3-1，与 joinApply 同口径）
	if !team.checkServerMatch(applicant.ServerId) {
		replyResult(ERROR_CODE_SERVER_MISMATCH)
		return
	}
	if cta.getPlayerTeam(applicant.GbId) != 0 {
		replyResult(ERROR_CODE_ALREADY_IN_TEAM)
		return
	}
	if team.memberCnt() >= team.MaxNum {
		replyResult(ERROR_CODE_TEAM_FULL)
		return
	}
	if code := team.checkConditionCode(applicant); code != ERROR_CODE_SUCCESS {
		replyResult(code)
		return
	}
	// 密码细分（与 joinApply 同口径）：目标队伍有密码而请求未携带 -> 需要密码；携带但不匹配 -> 密码错误
	if team.Password != "" {
		if in.Password == "" {
			replyResult(ERROR_CODE_NEED_PASSWORD)
			return
		}
		if team.Password != in.Password {
			replyResult(ERROR_CODE_PASSWORD_WRONG)
			return
		}
	}

	// 快速入队前清掉可能存在的本人待审批记录，避免队长后续应答时状态错乱
	if _, ok := team.Applicants[applicant.GbId]; ok {
		delete(team.Applicants, applicant.GbId)
		if captain, ok := team.Members[team.CaptainGbId]; ok {
			cta.notifyApplyRemove(captain.ServerId, in.TeamId, applicant.GbId, team.CaptainGbId)
		}
	}

	cta.addMember(w, team, applicant)
	cta.notifyReplyApply(applicant.ServerId, in.TeamId, applicant.GbId, ERROR_CODE_SUCCESS, 0, team)
	appLog.Infof("req join team, teamId=%d applicant=%d serverId=%d", in.TeamId, applicant.GbId, applicant.ServerId)
}

// clearApplyList 一键清空申请列表（本服 clearApplyJoinDic 对应，队长操作）：
// 逐个申请人按"被拒绝"通知（申请人侧结果闭环，避免清空后悬挂待审批），
// 队长侧逐个 applyRemoveNotify 同步剔除（客户端逐条移除后列表即空）；
// 操作结果经 uuid 回执通知队长
func (cta *CrossTeamApp) clearApplyList(w *teamWorker, gss *GameServerService, in *pb.ClearApplyListRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.CaptainGbId)
		return
	}
	if in.CaptainGbId != team.CaptainGbId {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}

	applicantCnt := len(team.Applicants)
	if applicantCnt > 0 {
		captain := team.Members[team.CaptainGbId]
		for gbId, apply := range team.Applicants {
			if captain != nil {
				cta.notifyApplyRemove(captain.ServerId, in.TeamId, gbId, team.CaptainGbId)
			}
			cta.notifyReplyApply(apply.Info.ServerId, in.TeamId, gbId, ERROR_CODE_APPLY_REJECTED, apply.ApplySource, team)
		}
		team.Applicants = make(map[uint64]*ApplyInfo)
	}
	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.CaptainGbId)
	appLog.Infof("clear apply list, teamId=%d captain=%d applicants=%d", in.TeamId, in.CaptainGbId, applicantCnt)
}

// setDeputy 任命/取消副团长（本服 transferRaidDeputy 对应，队长操作）：
// deputyGbId=0 表示取消；全队唯一名额，任命新副团长直接覆盖旧的（本服同口径）；
// 任命目标必须是本队成员且不能是队长本人（队长不能兼任副团长），
// 取消需当前确有副团长（对齐本服 _cancelRaidDeputy 的 NOT_RAID_DEPUTY 校验）；
// 校验通过更新内存 + 全量快照字段 deputyGbId（toPb 随全量下发），
// 操作结果经 uuid 回执（成功也回，操作者 UI 闭环），变更全队推送 deputyChangePush
func (cta *CrossTeamApp) setDeputy(w *teamWorker, gss *GameServerService, in *pb.SetDeputyRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.CaptainGbId)
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}
	if in.DeputyGbId != 0 {
		// 任命：目标是本队成员且不是队长本人
		if in.DeputyGbId == team.CaptainGbId {
			w.replyOp(gss, in.Uuid, ERROR_CODE_INVALID_PARAM, in.TeamId, in.CaptainGbId)
			return
		}
		if _, ok := team.Members[in.DeputyGbId]; !ok {
			w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_TEAM_MEMBER, in.TeamId, in.DeputyGbId)
			return
		}
	} else {
		// 取消：当前须有副团长（对齐本服校验）
		if team.DeputyGbId == 0 {
			w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_DEPUTY, in.TeamId, in.CaptainGbId)
			return
		}
	}

	team.DeputyGbId = in.DeputyGbId
	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.CaptainGbId)

	cta.pushDeputyChange(team)
	appLog.Infof("set deputy, teamId=%d captain=%d deputy=%d", in.TeamId, in.CaptainGbId, in.DeputyGbId)
}

// ---------------- 队伍标记（第四步 标记三件套） ----------------
// 数据存中心，变更经 pushMarkChange 单条增量下发（只发队长当前所在服）。
// 对齐本服静默语义：校验失败仅日志，不走 uuid 回执。

// addMark 添加标记（本服 reqAddMarkMember 对应，仅副本内可用）：
// 同槽位直接覆盖；同目标去重（队友按 gbId、敌方/场景按 entId），换槽先推 DELETE 再推 ADD
func (cta *CrossTeamApp) addMark(w *teamWorker, gss *GameServerService, in *pb.AddMarkRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		appLog.Warnf("add mark but team not found, teamId=%d operator=%d", in.TeamId, in.OperatorGbId)
		return
	}
	if _, ok := team.Members[in.OperatorGbId]; !ok {
		appLog.Warnf("add mark but operator not in team, teamId=%d operator=%d", in.TeamId, in.OperatorGbId)
		return
	}
	if team.OnlyCaptainCanMark && in.OperatorGbId != team.CaptainGbId {
		appLog.Infof("add mark blocked by onlyCaptainCanMark, teamId=%d operator=%d", in.TeamId, in.OperatorGbId)
		return
	}
	mark := in.Mark
	if mark == nil || mark.Index <= 0 || mark.Index > TEAM_MARK_MAX_SLOT ||
		mark.Type <= MARK_TYPE_NONE || mark.Type > MARK_TYPE_SCENE {
		appLog.Warnf("add mark invalid param, teamId=%d operator=%d mark=%v", in.TeamId, in.OperatorGbId, mark)
		return
	}

	marks := team.marksOfType(mark.Type)
	if mark.Type != MARK_TYPE_SCENE {
		// 同目标去重：同一目标只占一个槽位（对齐本服 playerCache 语义），换槽先推删除
		for idx, old := range marks {
			sameTarget := mark.GbId > 0 && old.GbId == mark.GbId ||
				mark.GbId == 0 && mark.EntId > 0 && old.EntId == mark.EntId
			if !sameTarget || idx == mark.Index {
				continue
			}
			delete(marks, idx)
			cta.pushMarkChange(team, MARK_CHANGE_DELETE, old)
		}
	}
	marks[mark.Index] = mark

	cta.pushMarkChange(team, MARK_CHANGE_ADD, mark)
	appLog.Infof("add mark, teamId=%d operator=%d type=%d index=%d gbId=%d entId=%d",
		in.TeamId, in.OperatorGbId, mark.Type, mark.Index, mark.GbId, mark.EntId)
}

// delMark 删除标记（本服 reqDelMarkMember 对应）：按 type+index 删除
func (cta *CrossTeamApp) delMark(w *teamWorker, gss *GameServerService, in *pb.DelMarkRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		return
	}
	if _, ok := team.Members[in.OperatorGbId]; !ok {
		return
	}
	if team.OnlyCaptainCanMark && in.OperatorGbId != 0 && in.OperatorGbId != team.CaptainGbId {
		return
	}
	marks := team.marksOfType(in.Type)
	mark, ok := marks[in.Index]
	if !ok {
		return
	}
	delete(marks, in.Index)

	cta.pushMarkChange(team, MARK_CHANGE_DELETE, mark)
	appLog.Infof("del mark, teamId=%d operator=%d type=%d index=%d", in.TeamId, in.OperatorGbId, in.Type, in.Index)
}

// setOnlyCaptainMark 仅队长可标记开关（本服 reqChangeOnlyCaptain 对应，队长操作）
func (cta *CrossTeamApp) setOnlyCaptainMark(w *teamWorker, gss *GameServerService, in *pb.SetOnlyCaptainMarkRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		return
	}
	if team.OnlyCaptainCanMark == in.OnlyCaptain {
		return
	}
	team.OnlyCaptainCanMark = in.OnlyCaptain

	cta.pushMarkChange(team, MARK_CHANGE_CAPTAIN, nil)
	appLog.Infof("set onlyCaptainCanMark, teamId=%d captain=%d onlyCaptain=%v",
		in.TeamId, in.CaptainGbId, in.OnlyCaptain)
}

// followAsk 召集（本服 sendAllMemberFollowAsk 对应，队长操作）：跟随本体由客户端实现，
// 中心仅复核队长并把召集指令（队长当前场景/坐标）广播到队长当前所在服
// （与标记同一决策：跟随仅副本内使用，打本时全队均在副本所在服）；
// receiverGbIds 为全队（不含队长本人），由该服 Stub 按本服实有成员路由转发。
// 对齐本服静默语义：校验失败仅日志，不走 uuid 回执
func (cta *CrossTeamApp) followAsk(w *teamWorker, gss *GameServerService, in *pb.FollowAskRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		appLog.Warnf("follow ask but team not found, teamId=%d captain=%d", in.TeamId, in.CaptainGbId)
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		appLog.Warnf("follow ask but not captain, teamId=%d operator=%d", in.TeamId, in.CaptainGbId)
		return
	}
	captain := team.Members[team.CaptainGbId]
	if captain == nil {
		return
	}

	msg := &pb.FollowAskPushMsg{
		TeamId:        team.TeamId,
		SpaceNo:       in.SpaceNo,
		PosX:          in.PosX,
		PosY:          in.PosY,
		PosZ:          in.PosZ,
		ReceiverGbIds: make([]uint64, 0, len(team.Members)-1),
	}
	for gbId := range team.Members {
		if gbId == team.CaptainGbId {
			continue
		}
		msg.ReceiverGbIds = append(msg.ReceiverGbIds, gbId)
	}
	if len(msg.ReceiverGbIds) == 0 {
		return
	}
	cta.sendToServer(captain.RouteServerId, "followAskPush", func(client *pb.GameServerClient) error {
		_, err := client.FollowAskPush(msg)
		return err
	})
	appLog.Infof(
		"follow ask, teamId=%d captain=%d routeServer=%d receivers=%d",
		in.TeamId,
		in.CaptainGbId,
		captain.RouteServerId,
		len(msg.ReceiverGbIds),
	)
}

func (cta *CrossTeamApp) replyApply(w *teamWorker, gss *GameServerService, in *pb.ReplyApplyRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.CaptainGbId)
		return
	}
	if in.CaptainGbId != team.CaptainGbId {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}
	apply, ok := team.Applicants[in.ApplicantGbId]
	if !ok {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_APPLIED, in.TeamId, in.CaptainGbId)
		return
	}
	delete(team.Applicants, in.ApplicantGbId)
	// 申请移除通知（同意/拒绝/复核失败统一移除），队长客户端同步从申请列表剔除
	if captain, ok := team.Members[team.CaptainGbId]; ok {
		cta.notifyApplyRemove(captain.ServerId, in.TeamId, in.ApplicantGbId, team.CaptainGbId)
	}

	if !in.Agree {
		w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.CaptainGbId)
		cta.notifyReplyApply(
			apply.Info.ServerId,
			in.TeamId,
			in.ApplicantGbId,
			ERROR_CODE_APPLY_REJECTED,
			apply.ApplySource,
			team,
		)
		return
	}

	// 同意：中心复核队伍状态后入队
	code := int32(ERROR_CODE_SUCCESS)
	switch {
	case team.isInDungeon():
		code = ERROR_CODE_TEAM_IN_DUNGEON
	case cta.getPlayerTeam(in.ApplicantGbId) != 0:
		code = ERROR_CODE_ALREADY_IN_TEAM
	case team.memberCnt() >= team.MaxNum:
		code = ERROR_CODE_TEAM_FULL
	default:
		// 门槛复核：等级/战力不足分别返回细分错误码
		code = team.checkConditionCode(apply.Info)
	}

	w.replyOp(gss, in.Uuid, code, in.TeamId, in.CaptainGbId)
	if code != ERROR_CODE_SUCCESS {
		cta.notifyReplyApply(
			apply.Info.ServerId,
			in.TeamId,
			in.ApplicantGbId,
			code,
			apply.ApplySource,
			team,
		)
		return
	}

	cta.addMember(w, team, apply.Info)
	cta.notifyReplyApply(
		apply.Info.ServerId,
		in.TeamId,
		in.ApplicantGbId,
		ERROR_CODE_SUCCESS,
		apply.ApplySource,
		team,
	)
}

func (cta *CrossTeamApp) invite(w *teamWorker, gss *GameServerService, in *pb.InviteRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.InviterGbId)
		return
	}
	inviter, ok := team.Members[in.InviterGbId]
	if !ok {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_TEAM_MEMBER, in.TeamId, in.InviterGbId)
		return
	}
	if team.isInDungeon() {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_IN_DUNGEON, in.TeamId, in.InviterGbId)
		return
	}
	if team.memberCnt() >= team.MaxNum {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_FULL, in.TeamId, in.InviterGbId)
		return
	}
	if cta.getPlayerTeam(in.InviteeGbId) != 0 {
		w.replyOp(gss, in.Uuid, ERROR_CODE_ALREADY_IN_TEAM, in.TeamId, in.InviterGbId)
		return
	}

	// 记录待应答邀请（被邀请人应答时复核）
	team.Invites[in.InviteeGbId] = &pb.MemberInfo{GbId: in.InviteeGbId, ServerId: in.InviteeServerId}
	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.InviterGbId)

	// 向被邀请人所在服推送邀请（只带邀请人信息与队伍目标，供客户端弹窗展示）
	cta.sendToServer(in.InviteeServerId, "inviteNotify", func(client *pb.GameServerClient) error {
		_, err := client.InviteNotify(&pb.InviteNotifyMsg{
			Inviter:     team.memberToPb(inviter),
			TeamId:      team.TeamId,
			Target:      team.Target,
			InviteeGbId: in.InviteeGbId,
			InviteType:  in.InviteType,
		})
		return err
	})
	appLog.Infof(
		"invite, teamId=%d inviter=%d invitee=%d inviteeServer=%d",
		in.TeamId,
		in.InviterGbId,
		in.InviteeGbId,
		in.InviteeServerId,
	)
}

func (cta *CrossTeamApp) replyInvite(w *teamWorker, gss *GameServerService, in *pb.ReplyInviteRequest) {
	invitee := in.Invitee
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, invitee.GbId)
		return
	}
	if _, ok := team.Invites[invitee.GbId]; !ok {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_INVITED, in.TeamId, invitee.GbId)
		return
	}
	delete(team.Invites, invitee.GbId)

	if !in.Agree {
		w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, invitee.GbId)
		return
	}

	// 同意：复核队伍状态（互斥校验由其本服完成）后入队；
	// 本服目标队伍复核被邀请人同服（D3-1，以 dunServer 为同服约束基准）
	code := int32(ERROR_CODE_SUCCESS)
	switch {
	case team.isInDungeon():
		code = ERROR_CODE_TEAM_IN_DUNGEON
	case !team.checkServerMatch(invitee.ServerId):
		code = ERROR_CODE_SERVER_MISMATCH
	case cta.getPlayerTeam(invitee.GbId) != 0:
		code = ERROR_CODE_ALREADY_IN_TEAM
	case team.memberCnt() >= team.MaxNum:
		code = ERROR_CODE_TEAM_FULL
	}

	w.replyOp(gss, in.Uuid, code, in.TeamId, invitee.GbId)
	if code == ERROR_CODE_SUCCESS {
		cta.addMember(w, team, invitee)
	}
}

func (cta *CrossTeamApp) leaveTeam(w *teamWorker, gss *GameServerService, in *pb.LeaveTeamRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.GbId)
		return
	}
	if _, ok := team.Members[in.GbId]; !ok {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_TEAM_MEMBER, in.TeamId, in.GbId)
		return
	}
	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.GbId)

	// 队长离队：removeMember 内立即从剩余成员移交队长（本服同款语义），仅剩自己则解散
	cta.removeMember(w, team, in.GbId, LEAVE_REASON_LEAVE)
}

func (cta *CrossTeamApp) kick(w *teamWorker, gss *GameServerService, in *pb.KickRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.KickedGbId)
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}
	if _, ok := team.Members[in.KickedGbId]; !ok {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_TEAM_MEMBER, in.TeamId, in.KickedGbId)
		return
	}
	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.KickedGbId)
	cta.removeMember(w, team, in.KickedGbId, LEAVE_REASON_KICK)
}

func (cta *CrossTeamApp) transferCaptain(w *teamWorker, gss *GameServerService, in *pb.TransferCaptainRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.NewCaptainGbId)
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}
	if _, ok := team.Members[in.NewCaptainGbId]; !ok {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_TEAM_MEMBER, in.TeamId, in.NewCaptainGbId)
		return
	}

	team.CaptainGbId = in.NewCaptainGbId
	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.NewCaptainGbId)

	cta.pushCaptainChange(team)
	cta.markTeamListDirty(team.Target)
	appLog.Infof("transfer captain, teamId=%d newCaptain=%d", in.TeamId, in.NewCaptainGbId)
}

// applyBecomeCaptain 申请成为队长（本服 doApplyBecomeCaptain 对应）：
// 中心不留存待应答记录（本服语义，队长应答时重新复核身份即可覆盖过期弹窗），
// 校验通过后直接把申请提示推给队长
func (cta *CrossTeamApp) applyBecomeCaptain(w *teamWorker, gss *GameServerService, in *pb.ApplyBecomeCaptainRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.GbId)
		return
	}
	applicant, ok := team.Members[in.GbId]
	if !ok {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_TEAM_MEMBER, in.TeamId, in.GbId)
		return
	}
	if in.GbId == team.CaptainGbId {
		w.replyOp(gss, in.Uuid, ERROR_CODE_INVALID_PARAM, in.TeamId, in.GbId)
		return
	}

	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.GbId)
	cta.pushBecomeCaptainApply(team, applicant)
	appLog.Infof(
		"apply become captain, teamId=%d applicant=%d captain=%d",
		in.TeamId,
		in.GbId,
		team.CaptainGbId,
	)
}

// replyBecomeCaptain 队长应答"申请成为队长"。同意：换队长 + 位置对调
// （队长永远在第一：新队长换入原队长位，对齐梳理注记 2/决策 D2 服务端行为），
// 推送队长变更 + 位置变更；拒绝：主动通知申请人
func (cta *CrossTeamApp) replyBecomeCaptain(w *teamWorker, gss *GameServerService, in *pb.ReplyBecomeCaptainRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.CaptainGbId)
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}
	applicant, ok := team.Members[in.ApplicantGbId]
	if !ok {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_TEAM_MEMBER, in.TeamId, in.CaptainGbId)
		return
	}
	oldCaptain := team.Members[team.CaptainGbId]
	if oldCaptain == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_COMMON, in.TeamId, in.CaptainGbId)
		return
	}
	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.CaptainGbId)

	if !in.Agree {
		cta.pushOpResult(applicant.ServerId, in.TeamId, in.ApplicantGbId, ERROR_CODE_BECOME_CAPTAIN_REJECTED, team.Target)
		appLog.Infof(
			"reply become captain rejected, teamId=%d applicant=%d",
			in.TeamId,
			in.ApplicantGbId,
		)
		return
	}

	// 位置对调：申请人与原队长交换 groupIdx/pos（推送沿用 adjustMemberPos 语义，字段为操作前位置）
	oldCaptainGbId := team.CaptainGbId
	srcGroupIdx, srcPos := applicant.GroupIdx, applicant.Pos
	dstGroupIdx, dstPos := oldCaptain.GroupIdx, oldCaptain.Pos
	applicant.GroupIdx, applicant.Pos = dstGroupIdx, dstPos
	oldCaptain.GroupIdx, oldCaptain.Pos = srcGroupIdx, srcPos
	team.CaptainGbId = in.ApplicantGbId

	cta.pushCaptainChange(team)
	cta.pushAdjustMemberPos(team, &pb.AdjustMemberPosRequest{
		TeamId:      team.TeamId,
		SrcGbId:     in.ApplicantGbId,
		SrcGroupIdx: srcGroupIdx,
		DstGbId:     oldCaptainGbId,
		DstGroupIdx: dstGroupIdx,
	})
	cta.markTeamListDirty(team.Target)
	appLog.Infof(
		"reply become captain agreed, teamId=%d newCaptain=%d oldCaptain=%d",
		in.TeamId,
		in.ApplicantGbId,
		oldCaptainGbId,
	)
}

func (cta *CrossTeamApp) disband(w *teamWorker, gss *GameServerService, in *pb.DisbandRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.CaptainGbId)
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}
	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.CaptainGbId)
	cta.disbandTeam(w, team)
}

func (cta *CrossTeamApp) setTeamSettings(w *teamWorker, gss *GameServerService, in *pb.SetTeamSettingsRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.CaptainGbId)
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}
	if in.MinLevel < 0 || in.MinScore < 0 {
		w.replyOp(gss, in.Uuid, ERROR_CODE_INVALID_PARAM, in.TeamId, in.CaptainGbId)
		return
	}
	// 队伍目标创建后不可改，这里只更新门槛/介绍/满员自动进本/密码（空串=取消密码转公开队）
	team.MinLevel = in.MinLevel
	team.MinScore = in.MinScore
	team.Intro = in.Intro
	team.AutoEnter = in.AutoEnter
	team.Password = in.Password

	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, 0)
	// "设置变更"增量推送（仅变更字段）
	cta.pushTeamSettingsChange(team.serverGbIds(), &pb.TeamSettingsChangePushMsg{
		TeamId:    team.TeamId,
		MinLevel:  team.MinLevel,
		MinScore:  team.MinScore,
		Intro:     team.Intro,
		AutoEnter: team.AutoEnter,
		Password:  team.Password,
	})

	// 密码变更影响 matchable（公开=无密码）：私密转公开且自动匹配时摘要事件同步回撮合池，
	// 公开转私密时摘要 matchable 重算为 false，撮合遍历自然剔除（isPublish 按密码派生，不单独存）
	cta.syncTeamSummary(team)
	cta.markTeamListDirty(team.Target)
	appLog.Infof(
		"set team settings, teamId=%d minLevel=%d minScore=%d autoEnter=%v hasPassword=%v",
		in.TeamId,
		in.MinLevel,
		in.MinScore,
		in.AutoEnter,
		team.Password != "",
	)

	// 开启满员自动进本时，若当前已满员则立即尝试发起讨伐
	cta.maybeAutoCrusade(w, team)
}

// setAutoMatch 自动匹配开关（队长操作，修改频率高，与 setTeamSettings 拆分）：
// 变更后"自动匹配"增量推送 + 同步撮合摘要（matchable 依赖 AutoMatch）
func (cta *CrossTeamApp) setAutoMatch(w *teamWorker, gss *GameServerService, in *pb.SetAutoMatchRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.CaptainGbId)
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}
	team.AutoMatch = in.AutoMatch
	// 开启时记录匹配开始时间（客户端匹配 UI 用），关闭时清 0
	if in.AutoMatch {
		team.AutoMatchTime = time.Now().Unix()
	} else {
		team.AutoMatchTime = 0
	}

	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, 0)
	cta.pushTeamAutoMatchChange(team.serverGbIds(), &pb.TeamAutoMatchChangePushMsg{
		TeamId:    team.TeamId,
		AutoMatch: team.AutoMatch,
	})
	cta.syncTeamSummary(team)
	appLog.Infof("set auto match, teamId=%d autoMatch=%v", in.TeamId, in.AutoMatch)
}

// setMicsMode 切换语音麦模式（队长操作），变更后"麦模式"增量推送
func (cta *CrossTeamApp) setMicsMode(w *teamWorker, gss *GameServerService, in *pb.SetMicsModeRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.CaptainGbId)
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}
	team.MicsMode = in.MicsMode
	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, 0)
	cta.pushTeamMicsModeChange(team.serverGbIds(), &pb.TeamMicsModeChangePushMsg{
		TeamId:   team.TeamId,
		MicsMode: team.MicsMode,
	})
	appLog.Infof("set mics mode, teamId=%d micsMode=%d", in.TeamId, in.MicsMode)
}

// blockMic 禁麦/解除禁麦（队长操作），变更后"禁麦"增量推送
func (cta *CrossTeamApp) blockMic(w *teamWorker, gss *GameServerService, in *pb.BlockMicRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.TargetGbId)
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}
	if _, ok := team.Members[in.TargetGbId]; !ok {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_TEAM_MEMBER, in.TeamId, in.TargetGbId)
		return
	}
	if in.Blocked {
		team.BlockedMembers[in.TargetGbId] = true
	} else {
		delete(team.BlockedMembers, in.TargetGbId)
	}
	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.TargetGbId)
	cta.pushMemberMicBlock(team.serverGbIds(), &pb.MemberMicBlockPushMsg{
		TeamId:  team.TeamId,
		GbId:    in.TargetGbId,
		Blocked: in.Blocked,
	})
	appLog.Infof("block mic, teamId=%d targetGbId=%d blocked=%v", in.TeamId, in.TargetGbId, in.Blocked)
}

// adjustMemberPos 成员位置调整（队长操作）。
// - dstGbId != 0：交换 src 与 dst 的 groupIdx + pos（支持组内/组间互换）
// - dstGbId == 0：将 src 移动到 dstGroupIdx 小组末尾
func (cta *CrossTeamApp) adjustMemberPos(w *teamWorker, gss *GameServerService, in *pb.AdjustMemberPosRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.CaptainGbId)
		return
	}
	if !checkCaptain(team, in.CaptainGbId) {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.CaptainGbId)
		return
	}
	if team.isInDungeon() {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_IN_DUNGEON, in.TeamId, in.CaptainGbId)
		return
	}
	src, ok := team.Members[in.SrcGbId]
	if !ok {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_TEAM_MEMBER, in.TeamId, in.SrcGbId)
		return
	}
	if src.GroupIdx != in.SrcGroupIdx {
		w.replyOp(gss, in.Uuid, ERROR_CODE_INVALID_POS, in.TeamId, in.SrcGbId)
		return
	}

	if in.DstGbId == 0 {
		// 移动到目标小组末尾：目标小组必须存在，且移动后不超过 5 人
		if team.groupMemberCnt(in.DstGroupIdx) == 0 {
			w.replyOp(gss, in.Uuid, ERROR_CODE_INVALID_POS, in.TeamId, in.SrcGbId)
			return
		}
		if src.GroupIdx == in.DstGroupIdx {
			// 移动到本组末尾：只刷新 pos，不破坏顺序语义
			src.Pos = team.nextPos(in.DstGroupIdx)
		} else {
			if team.groupMemberCnt(in.DstGroupIdx) >= CROSS_TEAM_GROUP_SIZE {
				w.replyOp(gss, in.Uuid, ERROR_CODE_GROUP_FULL, in.TeamId, in.SrcGbId)
				return
			}
			src.GroupIdx = in.DstGroupIdx
			src.Pos = team.nextPos(in.DstGroupIdx)
		}
	} else {
		if in.SrcGbId == in.DstGbId {
			w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.SrcGbId)
			return
		}
		dst, ok := team.Members[in.DstGbId]
		if !ok {
			w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_TEAM_MEMBER, in.TeamId, in.DstGbId)
			return
		}
		if dst.GroupIdx != in.DstGroupIdx {
			w.replyOp(gss, in.Uuid, ERROR_CODE_INVALID_POS, in.TeamId, in.DstGbId)
			return
		}
		// 交换 groupIdx + pos
		srcGroupIdx, srcPos := src.GroupIdx, src.Pos
		src.GroupIdx, src.Pos = dst.GroupIdx, dst.Pos
		dst.GroupIdx, dst.Pos = srcGroupIdx, srcPos
	}

	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.SrcGbId)
	cta.pushAdjustMemberPos(team, in)
	appLog.Infof(
		"adjust member pos, teamId=%d src=%d srcGroup=%d dst=%d dstGroup=%d",
		in.TeamId, in.SrcGbId, in.SrcGroupIdx, in.DstGbId, in.DstGroupIdx,
	)
}

// setVoiceState 成员语音状态同步（决策 2 独立推送）：客户端位图由游戏服解包后上传，
// 中心只存不解读。校验队伍存在 + 请求者是成员 -> 更新成员三态 -> 向队伍各成员所在服
// 广播 MemberVoiceStatePush（isBlockMics 按队伍禁麦表判定带出）
func (cta *CrossTeamApp) setVoiceState(w *teamWorker, gss *GameServerService, in *pb.SetVoiceStateRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.GbId)
		return
	}
	member, ok := team.Members[in.GbId]
	if !ok {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_TEAM_MEMBER, in.TeamId, in.GbId)
		return
	}
	member.EnableMics = in.EnableMics
	member.EnableSpeaker = in.EnableSpeaker
	member.InVoiceRoom = in.InVoiceRoom

	w.replyOp(gss, in.Uuid, ERROR_CODE_SUCCESS, in.TeamId, in.GbId)
	cta.pushMemberVoiceState(team.serverGbIds(), &pb.MemberVoiceStatePushMsg{
		TeamId:        team.TeamId,
		GbId:          in.GbId,
		EnableMics:    member.EnableMics,
		EnableSpeaker: member.EnableSpeaker,
		InVoiceRoom:   member.InVoiceRoom,
		IsBlockMics:   team.BlockedMembers[in.GbId],
	})
	appLog.Infof(
		"set voice state, teamId=%d gbId=%d mics=%v speaker=%v inRoom=%v",
		in.TeamId,
		in.GbId,
		in.EnableMics,
		in.EnableSpeaker,
		in.InVoiceRoom,
	)
}

// getApplyList 申请列表拉取（队长查看/断线重建）：仅队长可拉，
// 按 uuid 经请求来源连接单播 ApplyListPush 回请求者（MemberInfo 透传申请时快照，含 sex 等新字段）
func (cta *CrossTeamApp) getApplyList(w *teamWorker, gss *GameServerService, in *pb.GetApplyListRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(gss, in.Uuid, ERROR_CODE_TEAM_NOT_FOUND, in.TeamId, in.GbId)
		return
	}
	if in.GbId != team.CaptainGbId {
		w.replyOp(gss, in.Uuid, ERROR_CODE_NOT_CAPTAIN, in.TeamId, in.GbId)
		return
	}

	applicants := make([]*pb.ApplyInfo, 0, len(team.Applicants))
	for _, apply := range team.Applicants {
		applicants = append(applicants, &pb.ApplyInfo{
			Member:      apply.Info,
			ApplySource: apply.ApplySource,
			ApplyTS:     apply.ApplyTS,
		})
	}
	// 按申请时间升序，客户端按序展示
	sort.Slice(applicants, func(i, j int) bool {
		if applicants[i].ApplyTS != applicants[j].ApplyTS {
			return applicants[i].ApplyTS < applicants[j].ApplyTS
		}
		return applicants[i].Member.GetGbId() < applicants[j].Member.GetGbId()
	})

	_, err := gss.GetClientEndPoint().(*pb.GameServerClient).ApplyListPush(&pb.ApplyListPushMsg{
		Uuid:         in.Uuid,
		TeamId:       team.TeamId,
		ReceiverGbId: in.GbId,
		Applicants:   applicants,
	})
	if err != nil {
		appLog.Errorf(
			"send applyListPush failed, serverId=%d teamId=%d gbId=%d err=%v",
			gss.serverId,
			team.TeamId,
			in.GbId,
			err,
		)
	}
}

// matchJoin 两段式入队第二段：散人本服权威复检通过后向中心确认入队，
// 中心复检队伍（存在/有空位/仍自动匹配/未 InDungeon/门槛仍满足）后正式入队；
// 任一失败则作废，通知散人所在服"入队作废、需重新发起匹配"
func (cta *CrossTeamApp) matchJoin(w *teamWorker, gss *GameServerService, in *pb.MatchJoinRequest) {
	team := w.getTeam(in.TeamId)
	code := int32(ERROR_CODE_SUCCESS)
	switch {
	case team == nil:
		code = ERROR_CODE_TEAM_NOT_FOUND
	case team.isInDungeon():
		code = ERROR_CODE_TEAM_IN_DUNGEON
	case !team.checkServerMatch(in.Member.ServerId):
		// 本服目标队伍仅撮合同服散人（撮合侧已按 serverId 过滤，此处为中心复核）
		code = ERROR_CODE_SERVER_MISMATCH
	case cta.getPlayerTeam(in.Member.GbId) != 0:
		code = ERROR_CODE_ALREADY_IN_TEAM
	case !team.AutoMatch:
		code = ERROR_CODE_MATCH_JOIN_INVALID
	case team.memberCnt() >= team.MaxNum:
		code = ERROR_CODE_TEAM_FULL
	default:
		// 门槛复核：等级/战力不足分别返回细分错误码
		code = team.checkConditionCode(in.Member)
	}

	// 已删除跨 tick 的 pending：MatchSuccess -> MatchJoin 是服务器事件流转，正常延迟远低于
	// matchTick 间隔，由最终队满兜底。后续压测评估 MatchJoin 因队满失败的概率。
	w.replyOp(gss, in.Uuid, code, in.TeamId, in.Member.GbId)
	if code != ERROR_CODE_SUCCESS {
		// 入队作废：通知散人重新发起匹配（team 可能为 nil，target 此时补 0）
		target := int32(0)
		if team != nil {
			target = team.Target
		}
		cta.pushOpResult(in.Member.ServerId, in.TeamId, in.Member.GbId, ERROR_CODE_MATCH_JOIN_INVALID, target)
		appLog.Warnf("match join invalid, teamId=%d gbId=%d code=%d", in.TeamId, in.Member.GbId, code)
		return
	}
	cta.addMember(w, team, in.Member)
	appLog.Infof("match join done, teamId=%d gbId=%d", in.TeamId, in.Member.GbId)
}

// reportMemberState 成员状态 3s 聚合上报：
// 更新成员 hp/level/score/pos 等高频快照 -> 向该队伍各成员当前所在服广播。
// 上报方即成员当前真实所在服（跨服副本中由跨服服上的镜像上报），据此刷新推送路由；
// 本服镜像（ghost）不上报（游戏服 cell 侧已拦截），否则路由会在本服/跨服服间抖动。
// 离线即退队由专门的 MemberOffline RPC 处理，不再通过状态上报接口同步。
func (cta *CrossTeamApp) reportMemberState(w *teamWorker, gss *GameServerService, in *pb.ReportMemberStateRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		appLog.Debugf("report member state but team not found, teamId=%d serverId=%d", in.TeamId, in.ServerId)
		return
	}
	for _, state := range in.Members {
		member, ok := team.Members[state.GbId]
		if !ok {
			continue
		}
		member.Hp = state.Hp
		member.MaxHp = state.MaxHp
		member.Level = state.Level
		member.Score = state.Score
		member.SpaceNo = state.SpaceNo
		member.PosX = state.PosX
		member.PosY = state.PosY
		member.PosZ = state.PosZ
		member.ReportTS = in.ReportTS
		member.RouteServerId = in.ServerId
	}

	// 向各成员当前所在服广播全量状态快照（逐服附上该服接收者 gbId 列表，Stub 不再维护队伍缓存）
	members := make([]*pb.MemberState, 0, len(team.Members))
	for _, member := range team.Members {
		members = append(members, member.toStatePb())
	}
	for serverId, gbIds := range team.serverGbIds() {
		msg := &pb.BroadcastMemberStateMsg{
			TeamId:        team.TeamId,
			ReportTS:      in.ReportTS,
			Members:       members,
			ReceiverGbIds: gbIds,
		}
		cta.sendToServer(serverId, "broadcastMemberState", func(client *pb.GameServerClient) error {
			_, err := client.BroadcastMemberState(msg)
			return err
		})
	}
}

// memberOffline 游戏服主动上报成员离线：离线即退队，由专门 RPC 处理。
func (cta *CrossTeamApp) memberOffline(w *teamWorker, in *pb.MemberOfflineRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		appLog.Debugf("member offline but team not found, teamId=%d gbId=%d", in.TeamId, in.GbId)
		return
	}
	cta.handleMemberOffline(w, team, in.GbId)
}

// queryTeam 跨服服按需查询/校验队伍数据：
// teamId 非 0 时按队伍直查（队伍预览/跨服进本前校验），应答 QueryTeamCrossRespMsg；
// gbId 非 0 时按玩家反查所在队伍（客户端主动全量查询/登录恢复），应答 TeamDataRespMsg。
// 两条路径均按 uuid 单播回请求来源连接
func (cta *CrossTeamApp) queryTeam(w *teamWorker, gss *GameServerService, in *pb.QueryTeamRequest) {
	// teamId 直查路径（队伍预览用）：请求已按 teamId 投到本 worker，直接查
	if in.TeamId != 0 {
		resp := &pb.QueryTeamCrossRespMsg{Uuid: in.Uuid}
		if team := w.getTeam(in.TeamId); team != nil {
			resp.Success = true
			resp.Team = team.toPb()
		}
		_, err := gss.GetClientEndPoint().(*pb.GameServerClient).QueryTeamCrossResp(resp)
		if err != nil {
			appLog.Errorf(
				"send queryTeamCrossResp failed, serverId=%d teamId=%d err=%v",
				gss.serverId,
				in.TeamId,
				err,
			)
		}
		return
	}

	// gbId 反查路径（登录恢复）：反查到的队伍可能属于其他 worker，需重新投递
	teamId := cta.getPlayerTeam(in.GbId)
	if teamId != 0 && teamId%uint64(len(cta.dispatcher.workers)) != uint64(w.idx) {
		cta.dispatcher.Dispatch(teamId, "QueryTeam", func(w *teamWorker) {
			cta.queryTeam(w, gss, in)
		})
		return
	}

	team := w.getTeam(teamId)

	resp := &pb.TeamDataRespMsg{Uuid: in.Uuid}
	if team != nil {
		resp.Success = true
		resp.Team = team.toPb()
	}
	_, err := gss.GetClientEndPoint().(*pb.GameServerClient).TeamDataResp(resp)
	if err != nil {
		appLog.Errorf("send teamDataResp failed, serverId=%d teamId=%d err=%v", gss.serverId, teamId, err)
	}
}

// flushTeamChat 聊天聚合 flush（ChatBuffer 投回队伍 worker）：
// 按成员当前所在服分组批量推送 TeamChatBatch
func (cta *CrossTeamApp) flushTeamChat(w *teamWorker, teamId uint64, msgs []*pb.ChatMsg) {
	team := w.getTeam(teamId)
	if team == nil {
		appLog.Debugf("flush team chat but team not found, teamId=%d msgs=%d", teamId, len(msgs))
		return
	}
	// 逐服定制：附上该服接收者 gbId 列表（Stub 不再维护队伍缓存，靠 receiverGbIds 路由）
	for serverId, gbIds := range team.serverGbIds() {
		batch := &pb.TeamChatBatchMsg{TeamId: teamId, Msgs: msgs, ReceiverGbIds: gbIds}
		cta.sendToServer(serverId, "teamChatBatch", func(client *pb.GameServerClient) error {
			_, err := client.TeamChatBatch(batch)
			return err
		})
	}
}
