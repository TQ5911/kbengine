package crossTeamApp

import (
	"centralService/src/appLog"
	pb "centralService/src/crossTeamServer/crossTeamApp/gameServerService"
	"centralService/src/trpc"
	"errors"
	"fmt"
)

// GameServerService 一个游戏服/跨服服连接的端点（中心不区分两者身份，
// 本服与跨服服部署同款 CrossTeamStub，连接管理方式一致）。
type GameServerService struct {
	*trpc.ServerEndPoint
	app      *CrossTeamApp
	serverId uint32
}

func (gss *GameServerService) OnLoseConnection() {
	gss.app.removeGameServer(gss)
	appLog.Infof(
		"on lose connection, serverId=%d remaining=%d",
		gss.serverId,
		len(gss.app.getGameServers(gss.serverId)),
	)
}

func (gss *GameServerService) RegisterGameServer(in *pb.RegisterGameServerRequest) (*pb.Void, error) {
	appLog.Info("register game server:", in.ServerId)
	if in.ServerId == 0 {
		return nil, errors.New(fmt.Sprint("invalid ServerId: ", in.ServerId))
	}

	gss.serverId = in.ServerId
	gss.app.addGameServer(gss)

	appLog.Infof("game server %d registered, total connections: %d", in.ServerId, len(gss.app.getGameServers(in.ServerId)))
	return nil, nil
}

func (gss *GameServerService) ActiveTick(in *pb.Void) (*pb.Void, error) {
	_, err := gss.GetClientEndPoint().(*pb.GameServerClient).ActiveTickCallback(&pb.Void{})
	return nil, err
}

// ---------------------------------------------------------------------------
// 业务消息处理器：按并发模型投递——队伍相关消息按 teamId 投入
// 对应 worker channel 串行处理，散人匹配投入 per-target 池 goroutine，
// 聊天进 0.5s 聚合缓冲。业务实现见 teamOps.go。
// ---------------------------------------------------------------------------

func (gss *GameServerService) CreateTeam(in *pb.CreateTeamRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "CreateTeam", func(w *teamWorker) {
		gss.app.createTeam(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) JoinApply(in *pb.JoinApplyRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "JoinApply", func(w *teamWorker) {
		gss.app.joinApply(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) ReqJoin(in *pb.ReqJoinRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "ReqJoin", func(w *teamWorker) {
		gss.app.reqJoin(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) ClearApplyList(in *pb.ClearApplyListRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "ClearApplyList", func(w *teamWorker) {
		gss.app.clearApplyList(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) SetDeputy(in *pb.SetDeputyRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "SetDeputy", func(w *teamWorker) {
		gss.app.setDeputy(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) ReplyApply(in *pb.ReplyApplyRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "ReplyApply", func(w *teamWorker) {
		gss.app.replyApply(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) Invite(in *pb.InviteRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "Invite", func(w *teamWorker) {
		gss.app.invite(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) ReplyInvite(in *pb.ReplyInviteRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "ReplyInvite", func(w *teamWorker) {
		gss.app.replyInvite(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) LeaveTeam(in *pb.LeaveTeamRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "LeaveTeam", func(w *teamWorker) {
		gss.app.leaveTeam(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) Kick(in *pb.KickRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "Kick", func(w *teamWorker) {
		gss.app.kick(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) QueryTeam(in *pb.QueryTeamRequest) (*pb.Void, error) {
	key := in.TeamId
	if key == 0 {
		key = in.GbId
	}
	gss.app.dispatcher.Dispatch(key, "QueryTeam", func(w *teamWorker) {
		gss.app.queryTeam(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) TransferCaptain(in *pb.TransferCaptainRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "TransferCaptain", func(w *teamWorker) {
		gss.app.transferCaptain(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) ApplyBecomeCaptain(in *pb.ApplyBecomeCaptainRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "ApplyBecomeCaptain", func(w *teamWorker) {
		gss.app.applyBecomeCaptain(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) ReplyBecomeCaptain(in *pb.ReplyBecomeCaptainRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "ReplyBecomeCaptain", func(w *teamWorker) {
		gss.app.replyBecomeCaptain(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) Disband(in *pb.DisbandRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "Disband", func(w *teamWorker) {
		gss.app.disband(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) SetTeamSettings(in *pb.SetTeamSettingsRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "SetTeamSettings", func(w *teamWorker) {
		gss.app.setTeamSettings(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) SetAutoMatch(in *pb.SetAutoMatchRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "SetAutoMatch", func(w *teamWorker) {
		gss.app.setAutoMatch(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) sendTeamListResult(msg *pb.TeamListResultMsg) {
	_, err := gss.GetClientEndPoint().(*pb.GameServerClient).TeamListResult(msg)
	if err != nil {
		appLog.Errorf(
			"send teamListResult failed, serverId=%d uuid=%d err=%v",
			gss.serverId,
			msg.Uuid,
			err,
		)
	}
}

// GetTeamList 队伍列表查询：读后台协程维护的 target 快照，一波全量返回（问题记录#5）。
// 本服目标队伍（!isCross）仅当队伍 dunServer 与请求方 serverId 一致时返回（D3-1）
func (gss *GameServerService) GetTeamList(in *pb.GetTeamListRequest) (*pb.Void, error) {
	gss.app.teamListSnapshotMu.RLock()
	entry := gss.app.teamListSnapshot[in.Target]
	gss.app.teamListSnapshotMu.RUnlock()

	var entries []*teamListEntry
	if entry != nil {
		entries = entry.items
	}

	gss.sendTeamListResult(&pb.TeamListResultMsg{
		Uuid:   in.Uuid,
		Teams:  filterTeamListByServer(entries, in.ServerId),
		Target: in.Target,
	})
	return nil, nil
}

func (gss *GameServerService) EnterMatchPool(in *pb.EnterMatchPoolRequest) (*pb.Void, error) {
	if in.Player == nil {
		return nil, nil
	}
	// 已在跨服队伍中禁止入池（第一道拦截在玩家本服，此处为中心兜底）
	if gss.app.getPlayerTeam(in.Player.GbId) != 0 {
		replyOpTarget(
			gss,
			in.Uuid,
			ERROR_CODE_ALREADY_IN_TEAM,
			0,
			in.Player.GbId,
			in.Target,
		)
		return nil, nil
	}
	// 散人入池：变更走 target 池所属 goroutine 的 channel；
	// timeoutSeconds 为游戏服读配表 maxMatchTime 带入的本次匹配超时（<=0 时池内回落中心配置）
	gss.app.matchPools.EnterPool(in.Player, in.Target, in.TimeoutSeconds)
	return nil, nil
}

func (gss *GameServerService) LeaveMatchPool(in *pb.LeaveMatchPoolRequest) (*pb.Void, error) {
	gss.app.matchPools.LeavePool(in.GbId)
	return nil, nil
}

func (gss *GameServerService) MatchJoin(in *pb.MatchJoinRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "MatchJoin", func(w *teamWorker) {
		gss.app.matchJoin(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) ReportMemberState(in *pb.ReportMemberStateRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "ReportMemberState", func(w *teamWorker) {
		gss.app.reportMemberState(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) MemberOffline(in *pb.MemberOfflineRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "MemberOffline", func(w *teamWorker) {
		gss.app.memberOffline(w, in)
	})
	return nil, nil
}

func (gss *GameServerService) SetMicsMode(in *pb.SetMicsModeRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "SetMicsMode", func(w *teamWorker) {
		gss.app.setMicsMode(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) BlockMic(in *pb.BlockMicRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "BlockMic", func(w *teamWorker) {
		gss.app.blockMic(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) AdjustMemberPos(in *pb.AdjustMemberPosRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "AdjustMemberPos", func(w *teamWorker) {
		gss.app.adjustMemberPos(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) SetVoiceState(in *pb.SetVoiceStateRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "SetVoiceState", func(w *teamWorker) {
		gss.app.setVoiceState(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) GetApplyList(in *pb.GetApplyListRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "GetApplyList", func(w *teamWorker) {
		gss.app.getApplyList(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) TeamChatMsg(in *pb.TeamChatMsgRequest) (*pb.Void, error) {
	// 聊天上行进 0.5s 聚合缓冲，flush 时按成员所在服分组批量推送。
	// 完整透传 CHAT_MSG_DATA（msg/voiceUrl/msgType/code）与拼 avatarInfo 所需发送者信息，
	// 中心只做转发不解读（敏感词/频道 CD 在发送方本服完成）
	gss.app.chatBuffer.Add(in.TeamId, &pb.ChatMsg{
		SenderGbId:       in.SenderGbId,
		SenderName:       in.SenderName,
		Content:          in.Content,
		Ts:               in.Ts,
		MsgType:          in.MsgType,
		VoiceUrl:         in.VoiceUrl,
		Code:             in.Code,
		SenderSchool:     in.SenderSchool,
		SenderLevel:      in.SenderLevel,
		SenderSex:        in.SenderSex,
		SenderPicFrameId: in.SenderPicFrameId,
	})
	return nil, nil
}

func (gss *GameServerService) StartCrusade(in *pb.StartCrusadeRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "StartCrusade", func(w *teamWorker) {
		gss.app.startCrusade(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) CrusadeCheckResult(in *pb.CrusadeCheckResultRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "CrusadeCheckResult", func(w *teamWorker) {
		gss.app.crusadeCheckResult(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) CrusadeSpaceReady(in *pb.CrusadeSpaceReadyRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "CrusadeSpaceReady", func(w *teamWorker) {
		gss.app.crusadeSpaceReady(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) CrusadeFinished(in *pb.CrusadeFinishedRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "CrusadeFinished", func(w *teamWorker) {
		gss.app.crusadeFinished(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) AddMark(in *pb.AddMarkRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "AddMark", func(w *teamWorker) {
		gss.app.addMark(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) DelMark(in *pb.DelMarkRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "DelMark", func(w *teamWorker) {
		gss.app.delMark(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) SetOnlyCaptainMark(in *pb.SetOnlyCaptainMarkRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "SetOnlyCaptainMark", func(w *teamWorker) {
		gss.app.setOnlyCaptainMark(w, gss, in)
	})
	return nil, nil
}

func (gss *GameServerService) FollowAsk(in *pb.FollowAskRequest) (*pb.Void, error) {
	gss.app.dispatcher.Dispatch(in.TeamId, "FollowAsk", func(w *teamWorker) {
		gss.app.followAsk(w, gss, in)
	})
	return nil, nil
}
