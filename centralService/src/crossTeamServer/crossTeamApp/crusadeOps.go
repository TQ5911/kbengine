package crossTeamApp

import (
	"centralService/src/appLog"
	pb "centralService/src/crossTeamServer/crossTeamApp/gameServerService"
	"sync/atomic"
	"time"
)

// ---------------------------------------------------------------------------
// 讨伐发起协调（无确认弹窗：全员条件检查通过即进本）。
// 状态机：NONE -> CHECKING -> SPACE_CREATING -> IN_DUNGEON -> NONE
// 超时/失败路径统一走 crusadeAbort 复位。
// 本文件函数均在队伍所属 worker goroutine 内执行。
// ---------------------------------------------------------------------------

// allowCrusadeStart 发起限流：全组并发上限 + 全局每秒发起上限。
// 仅跨服模式讨伐调用（D3-7：本服模式不占全组讨伐并发/每秒配额）
func (cta *CrossTeamApp) allowCrusadeStart(serverId uint32) bool {
	maxConcurrent := int64(CrossTeamConfig.CrusadeMaxConcurrent)
	if maxConcurrent > 0 && atomic.LoadInt64(&cta.crusadeOngoing) >= maxConcurrent {
		appLog.Warnf(
			"crusade start rate limited, ongoing=%d max=%d",
			cta.crusadeOngoing,
			maxConcurrent,
		)
		return false
	}

	limitPerSecond := CrossTeamConfig.CrusadeStartLimitPerSecond
	if limitPerSecond > 0 && cta.crusadeLimiter != nil {
		if !cta.crusadeLimiter.Allow() {
			appLog.Warnf(
				"crusade start rate limited, serverId=%d limit=%d/s",
				serverId,
				limitPerSecond,
			)
			return false
		}
	}

	return true
}

// startCrusade 队长发起讨伐：校验 -> 置检查中 -> 按成员所在服下发 CrusadeCheck
func (cta *CrossTeamApp) startCrusade(w *teamWorker, gss *GameServerService, in *pb.StartCrusadeRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		w.replyOp(
			gss,
			in.Uuid,
			ERROR_CODE_TEAM_NOT_FOUND,
			in.TeamId,
			in.GbId,
		)
		return
	}
	// 本服已校验队长身份，中心复核队长字段
	if in.GbId != team.CaptainGbId {
		w.replyOp(
			gss,
			in.Uuid,
			ERROR_CODE_NOT_CAPTAIN,
			in.TeamId,
			in.GbId,
		)
		return
	}
	if code := cta.tryStartCrusade(w, team); code != ERROR_CODE_SUCCESS {
		w.replyOp(gss, in.Uuid, code, in.TeamId, in.GbId)
		return
	}
	w.replyOp(
		gss,
		in.Uuid,
		ERROR_CODE_SUCCESS,
		in.TeamId,
		in.GbId,
	)
}

// tryStartCrusade 发起讨伐的内部实现：状态/副本/限流校验 -> 置检查中 -> 按成员所在服下发 CrusadeCheck。
// 返回错误码（ERROR_CODE_SUCCESS 表示已发起）；手动发起与满员自动进本共用，回执由调用方决定。
func (cta *CrossTeamApp) tryStartCrusade(w *teamWorker, team *CrossTeamData) int32 {
	if team.isInDungeon() {
		return ERROR_CODE_TEAM_IN_DUNGEON
	}
	if team.CrusadeState != CRUSADE_STATE_NONE {
		return ERROR_CODE_CRUSADE_IN_PROGRESS
	}
	dungeonNo := team.DungeonMap
	if dungeonNo == 0 {
		return ERROR_CODE_INVALID_PARAM
	}
	// 副本创建目标服必须有效（dunServer=0 为建队数据异常），
	// 直接失败返回明确错误码（中心与配置解耦，无降级目标服）
	if team.DunServer == 0 {
		return ERROR_CODE_DUN_SERVER_INVALID
	}
	// 重进 CD：LastDungeonFinishedTime 存 CD 截止时刻（crusadeFinished 写入，同本服
	// raid_rejoinCdTime 口径）；客户端按 CD 倒计时屏蔽入口，此处为中心兜底，复用限流错误码
	if team.LastDungeonFinishedTime != 0 &&
		time.Now().Unix() < team.LastDungeonFinishedTime {
		return ERROR_CODE_CRUSADE_RATE_LIMIT
	}
	captain := team.Members[team.CaptainGbId]
	var captainServerId uint32
	if captain != nil {
		captainServerId = captain.ServerId
	}
	// 讨伐并发/每秒限流仅约束跨服模式，本服模式跳过（D3-7）
	if team.IsCross && !cta.allowCrusadeStart(captainServerId) {
		return ERROR_CODE_CRUSADE_RATE_LIMIT
	}

	team.CrusadeState = CRUSADE_STATE_CHECKING
	team.CrusadeDungeonNo = dungeonNo
	team.CrusadeDeadline = time.Now().Unix() + CRUSADE_CHECK_TIMEOUT_SECONDS
	team.CrusadeResults = make(map[uint64]bool)
	// 进行中计数同样仅跨服模式占用，与 crusadeAbort/crusadeFinished 的递减保持对称
	if team.IsCross {
		atomic.AddInt64(&cta.crusadeOngoing, 1)
	}

	// 按成员本服分组下发条件检查（无确认弹窗，检查通过即进本；
	// 检查链路在本服 Avatar 上执行，与推送路由 RouteServerId 无关）
	timeoutTS := team.CrusadeDeadline
	for serverId, gbIds := range team.homeServerGbIds() {
		cta.sendToServer(serverId, "crusadeCheck", func(client *pb.GameServerClient) error {
			_, err := client.CrusadeCheck(&pb.CrusadeCheckMsg{
				TeamId:    team.TeamId,
				DungeonNo: dungeonNo,
				TimeoutTS: timeoutTS,
				GbIds:     gbIds,
			})
			return err
		})
	}
	appLog.Infof("start crusade, teamId=%d dungeonNo=%d members=%d", team.TeamId, dungeonNo, team.memberCnt())
	return ERROR_CODE_SUCCESS
}

// maybeAutoCrusade 满员自动进本检查：成员加入与 autoEnter 设置（setTeamSettings）时调用。
// 开关开启且当前满员则自动发起讨伐；未满足/发起失败仅记日志（无操作发起人可回执）。
func (cta *CrossTeamApp) maybeAutoCrusade(w *teamWorker, team *CrossTeamData) {
	if !team.AutoEnter || team.memberCnt() < team.MaxNum {
		return
	}
	if code := cta.tryStartCrusade(w, team); code != ERROR_CODE_SUCCESS {
		appLog.Infof("auto crusade not started, teamId=%d code=%d", team.TeamId, code)
	}
}

// crusadeCheckResult 各服上报本地成员检查结果：任一失败即中止，全员通过则创建副本空间
func (cta *CrossTeamApp) crusadeCheckResult(w *teamWorker, gss *GameServerService, in *pb.CrusadeCheckResultRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil || team.CrusadeState != CRUSADE_STATE_CHECKING {
		appLog.Debugf("crusadeCheckResult ignored, teamId=%d gbId=%d", in.TeamId, in.GbId)
		return
	}

	team.CrusadeResults[in.GbId] = in.Ok
	if !in.Ok {
		appLog.Infof("crusade check failed, teamId=%d gbId=%d reason=%s", in.TeamId, in.GbId, in.Reason)
		cta.crusadeAbort(w, team, CRUSADE_ABORT_CHECK_FAIL)
		return
	}

	if len(team.CrusadeResults) < len(team.Members) {
		return
	}

	// 全员通过：经队伍 dunServer 对应游戏服（跨服=跨服服、本服=本服）的
	// CrossTeamStub 中转创建副本空间。中心与配置解耦仅识别字段（不再读 crossServerId 配置），
	// 目标服无连接时中止并回报明确原因，不 panic
	dunServer := team.DunServer
	if len(cta.getGameServers(dunServer)) == 0 {
		appLog.Errorf(
			"crusade abort, dun server %d not connected, teamId=%d",
			dunServer,
			team.TeamId,
		)
		cta.crusadeAbort(w, team, CRUSADE_ABORT_CROSS_NOT_CONN)
		return
	}

	team.CrusadeState = CRUSADE_STATE_SPACE_CREATING
	team.CrusadeDeadline = time.Now().Unix() + CRUSADE_CHECK_TIMEOUT_SECONDS
	cta.sendToServer(dunServer, "createCrusadeSpace", func(client *pb.GameServerClient) error {
		_, err := client.CreateCrusadeSpace(&pb.CreateCrusadeSpaceMsg{
			TeamId:    team.TeamId,
			DungeonNo: team.CrusadeDungeonNo,
			// context 由目标服 Stub 依据 dungeonNo 与队伍数据自行组装，中心不透传业务数据
			Context: nil,
		})
		return err
	})
	appLog.Infof("crusade check all pass, create space, teamId=%d dungeonNo=%d", team.TeamId, team.CrusadeDungeonNo)
}

// crusadeSpaceReady 目标服回报副本空间就绪：置状态为 IN_DUNGEON + 重算撮合摘要，
// 然后向各成员所在服发 CrusadeGo（crossServerId=dunServer：跨服模式驱动本服 Avatar 迁移，
// 本服模式即本服 id，游戏服 Stub 据此分流走本地进本）
func (cta *CrossTeamApp) crusadeSpaceReady(w *teamWorker, gss *GameServerService, in *pb.CrusadeSpaceReadyRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil || team.CrusadeState != CRUSADE_STATE_SPACE_CREATING {
		appLog.Debugf("crusadeSpaceReady ignored, teamId=%d spaceUUID=%s", in.TeamId, in.SpaceUUID)
		return
	}

	if !in.Ok {
		appLog.Errorf("crusade space create failed, teamId=%d", in.TeamId)
		cta.crusadeAbort(w, team, CRUSADE_ABORT_SPACE_FAILED)
		return
	}

	team.CrusadeState = CRUSADE_STATE_IN_DUNGEON
	team.CrusadeResults = nil
	cta.syncTeamSummary(team)
	cta.markTeamListDirty(team.Target)

	members := team.toPb().Members
	// CrusadeGo 必须按成员本服路由（驱动本服 Avatar 跨服迁移/本服本地进本），
	// 此时状态已是 IN_DUNGEON，推送路由 serverIds() 已指向目标服，不能用
	for _, serverId := range team.homeServerIds() {
		cta.sendToServer(serverId, "crusadeGo", func(client *pb.GameServerClient) error {
			_, err := client.CrusadeGo(&pb.CrusadeGoMsg{
				TeamId:        team.TeamId,
				CrossServerId: team.DunServer,
				SpaceUUID:     in.SpaceUUID,
				// context 保留透传位（当前未使用）；游戏服 Stub 不再维护队伍缓存，
				// 组 CrossCrusadeContext 所需的队伍数据由 maxNum/members 随推送下发
				Context: nil,
				MaxNum:  team.MaxNum,
				Members: members,
			})
			return err
		})
	}
	appLog.Infof("crusade space ready, teamId=%d spaceUUID=%s", team.TeamId, in.SpaceUUID)
}

// crusadeFinished 副本结束通知：复位状态机（队伍不解散）+ 重算撮合摘要 + 全推重进 CD
func (cta *CrossTeamApp) crusadeFinished(w *teamWorker, gss *GameServerService, in *pb.CrusadeFinishedRequest) {
	team := w.getTeam(in.TeamId)
	if team == nil {
		appLog.Debugf("crusadeFinished but team not found, teamId=%d", in.TeamId)
		return
	}
	// 进行中计数在 startCrusade 时增加（仅跨服模式），
	// 在 abort（检查/建空间阶段）或此处（副本结束）恰好减一次，增减同以 IsCross 为口径
	needSettle := team.CrusadeState != CRUSADE_STATE_NONE
	if team.isInDungeon() {
		team.CrusadeState = CRUSADE_STATE_NONE
		// 记录重进 CD 截止时刻（= 完成时刻 + 冷却，同本服 refreshLastDungeonFinishedTime 口径；
		// 随全量数据下发，并即推全员刷新客户端倒计时屏蔽）
		team.LastDungeonFinishedTime = time.Now().Unix() + CRUSADE_REJOIN_CD_SECONDS
		cta.syncTeamSummary(team)
		cta.markTeamListDirty(team.Target)
		cta.pushDungeonCDRefresh(team)
	}
	if team.CrusadeState != CRUSADE_STATE_NONE {
		team.CrusadeState = CRUSADE_STATE_NONE
		team.CrusadeResults = nil
	}
	if needSettle && team.IsCross {
		atomic.AddInt64(&cta.crusadeOngoing, -1)
	}
	appLog.Infof("crusade finished, teamId=%d result=%d", team.TeamId, in.Result)
}

// pushDungeonCDRefresh 重进 CD 刷新推送：客户端向推送按成员路由服分组，逐服定制 receiverGbIds
// （成员回本迁移途中推送可能落到已销毁镜像而丢失，由回本后全量查询兜底刷新）
func (cta *CrossTeamApp) pushDungeonCDRefresh(team *CrossTeamData) {
	for serverId, gbIds := range team.serverGbIds() {
		msg := &pb.DungeonCDRefreshPushMsg{
			TeamId:                  team.TeamId,
			LastDungeonFinishedTime: team.LastDungeonFinishedTime,
			ReceiverGbIds:           gbIds,
		}
		cta.sendToServer(serverId, "dungeonCDRefreshPush", func(client *pb.GameServerClient) error {
			_, err := client.DungeonCDRefreshPush(msg)
			return err
		})
	}
}

// crusadeAbort 讨伐中止：通知各成员本服并复位状态（worker sweep 超时也走这里；
// 只在检查中/建空间中触发，成员尚未迁移，一律按本服路由）
func (cta *CrossTeamApp) crusadeAbort(w *teamWorker, team *CrossTeamData, reason int32) {
	team.CrusadeState = CRUSADE_STATE_NONE
	team.CrusadeResults = nil
	// 进行中计数仅跨服模式占用（与 startCrusade 的递增对称）
	if team.IsCross {
		atomic.AddInt64(&cta.crusadeOngoing, -1)
	}

	for serverId, gbIds := range team.homeServerGbIds() {
		msg := &pb.CrusadeAbortMsg{
			TeamId:        team.TeamId,
			Reason:        reason,
			ReceiverGbIds: gbIds,
		}
		cta.sendToServer(serverId, "crusadeAbort", func(client *pb.GameServerClient) error {
			_, err := client.CrusadeAbort(msg)
			return err
		})
	}
	appLog.Infof("crusade abort, teamId=%d reason=%d", team.TeamId, reason)
}
