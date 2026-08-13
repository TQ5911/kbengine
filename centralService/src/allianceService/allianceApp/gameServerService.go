package allianceApp

import (
	"centralService/src/allianceService/allianceApp/gameServerService"
	"centralService/src/appLog"
	"centralService/src/common"
	"centralService/src/trpc"
	"errors"
	"fmt"
	"time"
)

type GameServerService struct {
	*trpc.ServerEndPoint
	app      *AllianceApp
	serverId uint32
}

func (gss *GameServerService) OnLoseConnection() {
	appLog.Info("alliance: game server lost connection", gss.serverId)
	gss.app.removeGameServer(gss)
}

func (gss *GameServerService) RegisterGameServer(in *gameServerService.RegisterGameServerRequest) (*gameServerService.Void, error) {
	appLog.Info("alliance: register game server:", in.ServerId)
	if gss.app.getGameServer(in.ServerId) != nil {
		return nil, errors.New(fmt.Sprint("already registered: ", in.ServerId))
	}
	if in.ServerId == 0 {
		return nil, errors.New("invalid serverId")
	}
	gss.serverId = in.ServerId
	gss.app.addGameServer(gss)

	// Send all guild relations (UNION + ENEMY) to the newly registered game server
	relations, version := guildRelationCache.GetAllRelations()
	if len(relations) > 0 {
		gss.getClient().OnGuildRelationAll(&gameServerService.GuildRelationAllInfo{
			Relations: relations,
			Version:   version,
		})
	}

	return nil, nil
}

func (gss *GameServerService) ActiveTick(in *gameServerService.Void) (*gameServerService.Void, error) {
	_, err := gss.GetClientEndPoint().(*gameServerService.GameClientClient).ActiveTickCallback(&gameServerService.Void{})
	return nil, err
}

func (gss *GameServerService) getClient() *gameServerService.GameClientClient {
	return gss.GetClientEndPoint().(*gameServerService.GameClientClient)
}

// ==== Core ====

func (gss *GameServerService) CreateLeague(in *gameServerService.CreateLeagueRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("alliance: create league", in.Name, in.GuildId)
		allianceId, errCode, info, members := gss.app.allianceData.CreateLeague(gss.app.db, gss.app, in)
		gss.getClient().OnCreateLeagueResult(&gameServerService.CreateLeagueResult{
			AllianceId: allianceId,
			Uuid:       in.Uuid,
			ErrCode:    errCode,
			Alliance:   info,
			Members:    members,
		})
	})
	return nil, nil
}

func (gss *GameServerService) DisbandLeague(in *gameServerService.DisbandLeagueRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("alliance: disband league", in.AllianceId)
		errCode, serverGuilds := gss.app.allianceData.DisbandLeague(gss.app.db, gss.app, in)
		gss.getClient().OnDisbandLeagueResult(&gameServerService.DisbandLeagueResult{
			Uuid:    in.Uuid,
			ErrCode: errCode,
		})
		if errCode == ErrCodeSuccess {
			for serverId, guildIds := range serverGuilds {
				ids := guildIds
				gs := gss.app.getGameServer(serverId)
				if gs == nil {
					continue
				}
				client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient)
				if ok {
					client.OnDisbandLeagueNotify(&gameServerService.DisbandLeagueNotify{
						AllianceId: in.AllianceId,
						GuildIds:   ids,
					})
				}
			}
		}
	})
	return nil, nil
}

func (gss *GameServerService) ModifyLeagueInfo(in *gameServerService.ModifyLeagueInfoRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("alliance: modify league info", in.AllianceId)
		errCode := gss.app.allianceData.ModifyLeagueInfo(gss.app.db, gss.app, in)
		gss.getClient().OnModifyLeagueInfoResult(&gameServerService.ModifyLeagueInfoResult{
			Uuid:    in.Uuid,
			ErrCode: errCode,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetLeagueList(in *gameServerService.GetLeagueListRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		totalPage, entries := gss.app.allianceData.GetLeagueList(in)
		gss.getClient().OnLeagueListResult(&gameServerService.GetLeagueListResult{
			Entries:   entries,
			PageIndex: in.PageIndex,
			TotalPage: totalPage,
			Uuid:      in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) SearchLeague(in *gameServerService.SearchLeagueRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		entries := gss.app.allianceData.SearchLeague(in)
		gss.getClient().OnSearchLeagueResult(&gameServerService.SearchLeagueResult{
			Entries: entries,
			Uuid:    in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetLeagueDetail(in *gameServerService.GetLeagueDetailRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		allianceInfo, members, errCode := gss.app.allianceData.GetLeagueDetail(in)
		gss.getClient().OnLeagueDetailResult(&gameServerService.GetLeagueDetailResult{
			Alliance: allianceInfo,
			Members:  members,
			Uuid:     in.Uuid,
			ErrCode:  errCode,
		})
	})
	return nil, nil
}

// GetAllianceBasicInfo returns the focused 9-field projection of an alliance
// (declaration + approval mode + leader identity) to the requesting game server.
// All work is dispatched via ExecuteConcurrently to keep the RPC hot path fast.
func (gss *GameServerService) GetLeagueBasicInfo(in *gameServerService.GetLeagueBasicInfoRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		basicInfo, errCode := gss.app.allianceData.GetAllianceBasicInfo(in)
		gss.getClient().OnGetLeagueBasicInfoResult(&gameServerService.GetLeagueBasicInfoResult{
			Info:    basicInfo,
			Uuid:    in.Uuid,
			ErrCode: errCode,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetLeagueSimpleInfo(in *gameServerService.GetLeagueSimpleInfoRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		simpleInfo, errCode := gss.app.allianceData.GetAllianceSimpleInfo(in)
		gss.getClient().OnGetLeagueSimpleInfoResult(&gameServerService.GetLeagueSimpleInfoResult{
			Info:    simpleInfo,
			Uuid:    in.Uuid,
			ErrCode: errCode,
		})
	})
	return nil, nil
}

// ==== Member ====

func (gss *GameServerService) ApplyToJoin(in *gameServerService.ApplyToJoinRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("alliance: apply to join", in.GuildId, "->", in.AllianceId)
		errCode, applyInfo, allianceId, allianceName, alliancePower := gss.app.allianceData.ApplyToJoin(gss.app.db, gss.app, in)
		gss.getClient().OnApplyToJoinResult(&gameServerService.ApplyToJoinResult{
			Uuid:          in.Uuid,
			ErrCode:       errCode,
			AllianceId:    allianceId,
			AllianceName:  allianceName,
			AlliancePower: alliancePower,
		})
		if applyInfo != nil {
			if cache, ok := gss.app.allianceData.alliances.Get(in.AllianceId); ok {
				gs := gss.app.getGameServer(cache.info.LeaderServerId)
				if gs != nil {
					if client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient); ok {
						client.OnNewApplyNotify(buildNewApplyNotify(applyInfo))
					}
				}
			}
		}
	})
	return nil, nil
}

func (gss *GameServerService) ApproveJoin(in *gameServerService.ApproveJoinRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("alliance: approve join", in.GuildId, in.AllianceId)
		errCode, joinedGuildId, deferred := gss.app.allianceData.ApproveJoin(gss.app.db, gss.app, in, gss.serverId)
		if deferred {
			// Existence check is in flight on the source game server.
			// The final OnApproveJoinResult will arrive from the
			// OnCheckGuildExistsResult handler.
			return
		}
		gss.getClient().OnApproveJoinResult(&gameServerService.ApproveJoinResult{
			Uuid:          in.Uuid,
			ErrCode:       errCode,
			JoinedGuildId: joinedGuildId,
		})
	})
	return nil, nil
}

// OnCheckGuildExistsResult is the callback from a game server after a
// CheckGuildExists request. Resolves the corresponding pendingApproveJoin
// and either completes the join (if the guild exists) or notifies the
// alliance leader of the failure (if the guild has been disbanded or the
// source server lost it).
//
// Two pending paths can land here, sharing the same CheckGuildExists
// RPC + uuid keyspace:
//   - pendingApproveJoins : ApproveJoin dispatched the check on the
//     source server; result routes back to the alliance leader.
//   - pendingInviteGuilds : InviteGuild dispatched the check on the
//     TARGET guild's server; result routes back to the inviter
//     (also the alliance leader in the normal flow).
//
// We try ApproveJoin first, then fall through to InviteGuild.
func (gss *GameServerService) OnCheckGuildExistsResult(in *gameServerService.CheckGuildExistsResult) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		// === ApproveJoin path ===
		p := gss.app.allianceData.failPendingApproveJoin(in.Uuid)
		if p != nil {
			if !in.Exists {
				appLog.Info("alliance: approve deferred — source guild no longer exists, guildId=", p.guildId)
				ad := gss.app.allianceData
				if targetCache, ok := ad.alliances.Get(p.allianceId); ok {
					targetCache.Lock()
					delete(targetCache.applies, p.guildId)
					targetCache.updateDerivedFields()
					targetCache.Unlock()
				}
				ad.removeGuildApply(p.guildId, p.allianceId)
				if gss.app.db != nil {
					gss.app.db.Exec("UPDATE alliance_apply SET apply_state = ? WHERE id = ?", ApplyStatusRejected, p.applyInfo.ApplyId)
				}

				if leaderGS := gss.app.getGameServer(p.leaderServerId); leaderGS != nil {
					guildCD := uint32(0)
					if in.CheckCD {
						guildCD = in.GuildCD
					}
					leaderGS.getClient().OnApproveJoinResult(&gameServerService.ApproveJoinResult{
						Uuid:          p.originalUuid,
						ErrCode:       ErrCodeGuildNotFound,
						GuildCD:       guildCD,
						JoinedGuildId: p.guildId,
					})
				}
				return
			}
			// Guild exists — actually do the approve.
			errCode, joinedGuildId := gss.app.allianceData.completeApproveJoin(gss.app.db, gss.app, p)
			if leaderGS := gss.app.getGameServer(p.leaderServerId); leaderGS != nil {
				leaderGS.getClient().OnApproveJoinResult(&gameServerService.ApproveJoinResult{
					Uuid:          p.originalUuid,
					ErrCode:       errCode,
					JoinedGuildId: joinedGuildId,
				})
			}
			return
		}

		// === InviteGuild path ===
		pi := gss.app.allianceData.failPendingInviteGuild(in.Uuid)
		if pi != nil {
			if !in.Exists {
				appLog.Info("alliance: invite deferred — target guild no longer exists, targetGuildId=", pi.targetGuildId)

				if inviterGS := gss.app.getGameServer(pi.inviterLeaderServerId); inviterGS != nil {
					guildCD := uint32(0)
					if in.CheckCD {
						guildCD = in.GuildCD
					}
					inviterGS.getClient().OnInviteGuildResult(&gameServerService.InviteGuildResult{
						Uuid:          pi.originalUuid,
						ErrCode:       ErrCodeGuildNotFound,
						TargetGuildId: pi.inviteeSnapshot.GuildId,
						GuildCD:       guildCD,
					})
				}
				return
			}
			// Target guild exists — actually do the invite.
			errCode := gss.app.allianceData.completeInviteGuild(gss.app.db, gss.app, pi)
			if inviterGS := gss.app.getGameServer(pi.inviterLeaderServerId); inviterGS != nil {
				inviterGS.getClient().OnInviteGuildResult(&gameServerService.InviteGuildResult{
					Uuid:          pi.originalUuid,
					ErrCode:       errCode,
					TargetGuildId: pi.inviteeSnapshot.GuildId,
				})
			}
			return
		}

		// === DeclareWar path ===
		pw := gss.app.allianceData.failPendingDeclareWar(in.Uuid)
		if pw != nil {
			if !in.Exists {
				appLog.Info("alliance: war deferred — target guild no longer exists, targetGuildId=", pw.targetId)
				if attackerGS := gss.app.getGameServer(pw.attackerServerId); attackerGS != nil {
					attackerGS.getClient().OnDeclareWarResult(&gameServerService.DeclareWarResult{
						Uuid:    pw.originalUuid,
						ErrCode: ErrCodeGuildNotFound,
						EndTime: 0,
					})
				}

				if pw.attackType == WarAttackTypeGuild {
					gss.getClient().OnReturnGuildFundNotify(&gameServerService.ReturnGuildFundNotify{
						GuildId:  pw.attackId,
						SrcType:  ENEMY_COST,
						ItemType: FUND,
						ItemNum:  pw.amount,
					})
				}
				return
			}
			// Target guild exists — actually commit the war.
			pw.toGuildName = in.GuildName
			errCode, endTime := gss.app.allianceData.completeDeclareWar(gss.app.db, gss.app, pw)
			if attackerGS := gss.app.getGameServer(pw.attackerServerId); attackerGS != nil {
				attackerGS.getClient().OnDeclareWarResult(&gameServerService.DeclareWarResult{
					Uuid:    pw.originalUuid,
					ErrCode: errCode,
					EndTime: endTime,
				})
			}
			if errCode != ErrCodeSuccess {
				if pw.attackType == WarAttackTypeGuild {
					gss.getClient().OnReturnGuildFundNotify(&gameServerService.ReturnGuildFundNotify{
						GuildId:  pw.attackId,
						SrcType:  ENEMY_COST,
						ItemType: FUND,
						ItemNum:  pw.amount,
					})
				}
			}
			return
		}

		appLog.Warn("alliance: OnCheckGuildExistsResult with no pending entry, uuid=", in.Uuid)
	})
	return nil, nil
}

func (gss *GameServerService) RejectJoin(in *gameServerService.RejectJoinRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode, rejectedGuildId := gss.app.allianceData.RejectJoin(gss.app.db, in)
		gss.getClient().OnRejectJoinResult(&gameServerService.RejectJoinResult{
			Uuid:            in.Uuid,
			ErrCode:         errCode,
			RejectedGuildId: rejectedGuildId,
		})
	})
	return nil, nil
}

func (gss *GameServerService) CancelApply(in *gameServerService.CancelApplyRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode, allianceId := gss.app.allianceData.CancelApply(gss.app.db, in)
		gss.getClient().OnCancelApplyResult(&gameServerService.CancelApplyResult{
			Uuid:       in.Uuid,
			ErrCode:    errCode,
			AllianceId: allianceId,
		})
	})
	return nil, nil
}

// InviteGuild handles the alliance leader's "invite a guild" RPC.
// Pre-checks run synchronously (already-in-alliance, alliance full,
// target server offline) and fail-fast with OnInviteGuildResult;
// the actual invite creation is deferred behind a CheckGuildExists
// round-trip to the target guild's server. The deferred path runs
// completeInviteGuild and broadcasts OnInviteGuildResult + the
// invite notification from OnCheckGuildExistsResult — NOT here.
func (gss *GameServerService) InviteGuild(in *gameServerService.InviteGuildRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode, deferred := gss.app.allianceData.InviteGuild(gss.app.db, gss.app, in, gss.serverId)
		if deferred {
			// Result + invite notification will arrive from
			// OnCheckGuildExistsResult. The old synchronous
			// OnNewInviteNotify path is gone — completeInviteGuild
			// now owns that broadcast under cache.Lock().
			return
		}
		gss.getClient().OnInviteGuildResult(&gameServerService.InviteGuildResult{
			Uuid:    in.Uuid,
			ErrCode: errCode,
		})
	})
	return nil, nil
}

func (gss *GameServerService) AcceptInvite(in *gameServerService.AcceptInviteRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode, allianceId := gss.app.allianceData.AcceptInvite(gss.app.db, gss.app, in)
		gss.getClient().OnAcceptInviteResult(&gameServerService.AcceptInviteResult{
			Uuid:       in.Uuid,
			ErrCode:    errCode,
			AllianceId: allianceId,
		})
	})
	return nil, nil
}

func (gss *GameServerService) RejectInvite(in *gameServerService.RejectInviteRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode, allianceId := gss.app.allianceData.RejectInvite(gss.app.db, in)
		gss.getClient().OnRejectInviteResult(&gameServerService.RejectInviteResult{
			Uuid:       in.Uuid,
			ErrCode:    errCode,
			AllianceId: allianceId,
		})
	})
	return nil, nil
}

func (gss *GameServerService) KickMember(in *gameServerService.KickMemberRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode := gss.app.allianceData.KickMember(gss.app.db, gss.app, in)
		gss.getClient().OnKickMemberResult(&gameServerService.KickMemberResult{
			Uuid:    in.Uuid,
			ErrCode: errCode,
		})
	})
	return nil, nil
}

func (gss *GameServerService) LeaveLeague(in *gameServerService.LeaveLeagueRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode := gss.app.allianceData.LeaveLeague(gss.app.db, gss.app, in)
		gss.getClient().OnLeaveLeagueResult(&gameServerService.LeaveLeagueResult{
			Uuid:    in.Uuid,
			ErrCode: errCode,
		})
	})
	return nil, nil
}

func (gss *GameServerService) TransferLeader(in *gameServerService.TransferLeaderRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode, allianceInfo := gss.app.allianceData.TransferLeader(gss.app.db, gss.app, in)
		gss.getClient().OnTransferLeaderResult(&gameServerService.TransferLeaderResult{
			Uuid:     in.Uuid,
			ErrCode:  errCode,
			Alliance: allianceInfo,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetApplyList(in *gameServerService.GetApplyListRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		applies, totalCount := gss.app.allianceData.GetApplyList(in)
		gss.getClient().OnApplyListResult(&gameServerService.GetApplyListResult{
			Applies:    applies,
			TotalCount: totalCount,
			Uuid:       in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetInviteList(in *gameServerService.GetInviteListRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		invites, totalCount := gss.app.allianceData.GetInviteList(in)
		gss.getClient().OnInviteListResult(&gameServerService.GetInviteListResult{
			Invites:    invites,
			TotalCount: totalCount,
			Uuid:       in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetSentApplies(in *gameServerService.GetSentAppliesRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		applies, totalCount := gss.app.allianceData.GetSentApplies(in)
		gss.getClient().OnSentAppliesResult(&gameServerService.GetSentAppliesResult{
			Applies:    applies,
			TotalCount: totalCount,
			Uuid:       in.Uuid,
		})
	})
	return nil, nil
}

// ==== Diplomacy ====

func (gss *GameServerService) DeclareWar(in *gameServerService.DeclareWarRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode, endTime, deferred := gss.app.allianceData.DeclareWar(gss.app.db, gss.app, in, gss.serverId)
		if deferred {
			// Cross-server target-guild existence check in flight;
			// the OnCheckGuildExistsResult callback will send the
			// eventual OnDeclareWarResult. Don't send anything
			// here, otherwise the caller would see a spurious
			// success before the actual outcome.
			return
		}
		gss.getClient().OnDeclareWarResult(&gameServerService.DeclareWarResult{
			Uuid:    in.Uuid,
			ErrCode: errCode,
			EndTime: endTime,
		})

		if errCode != ErrCodeSuccess {
			if in.AttackType == WarAttackTypeGuild {
				gss.getClient().OnReturnGuildFundNotify(&gameServerService.ReturnGuildFundNotify{
					GuildId:  in.AttackId,
					SrcType:  ENEMY_COST,
					ItemType: FUND,
					ItemNum:  in.Amount,
				})
			}
		}
	})
	return nil, nil
}

func (gss *GameServerService) GetEnemyList(in *gameServerService.GetEnemyListRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		enemies := gss.app.allianceData.GetEnemyList(in)
		gss.getClient().OnEnemyListResult(&gameServerService.GetEnemyListResult{
			Enemies: enemies,
			Uuid:    in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetEnemyAllianceList(in *gameServerService.GetEnemyAllianceListRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		alliances := gss.app.allianceData.GetEnemyAllianceList(in)
		gss.getClient().OnEnemyAllianceListResult(&gameServerService.GetEnemyAllianceListResult{
			Enemies: alliances,
			Uuid:    in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetUnionList(in *gameServerService.GetUnionListRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		unions := gss.app.allianceData.GetUnionList(in)
		gss.getClient().OnUnionListResult(&gameServerService.GetUnionListResult{
			Unions: unions,
			Uuid:   in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) CheckLeagueRelation(in *gameServerService.CheckLeagueRelationRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		isSame, allianceId := gss.app.allianceData.CheckLeagueRelation(in)
		gss.getClient().OnCheckLeagueRelationResult(&gameServerService.CheckLeagueRelationResult{
			IsSameAlliance: isSame,
			AllianceId:     allianceId,
			Uuid:           in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetGuildAlliance(in *gameServerService.GetGuildAllianceRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		allianceId, errCode := gss.app.allianceData.GetGuildAlliance(in)
		gss.getClient().OnGetGuildAllianceResult(&gameServerService.GetGuildAllianceResult{
			AllianceId: allianceId,
			ErrCode:    errCode,
			Uuid:       in.Uuid,
		})
	})
	return nil, nil
}

// ==== Resource ====

func (gss *GameServerService) DonateFund(in *gameServerService.DonateFundRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode, allianceId, newFund := gss.app.allianceData.DonateFund(gss.app.db, gss.app, in)
		gss.getClient().OnDonateFundResult(&gameServerService.DonateFundResult{
			Uuid:         in.Uuid,
			ErrCode:      errCode,
			AllianceFund: newFund,
			AllianceId:   allianceId,
		})
		if errCode != ErrCodeSuccess {
			gss.getClient().OnReturnGuildFundNotify(&gameServerService.ReturnGuildFundNotify{
				GuildId:  in.GuildId,
				SrcType:  DONATE_COST,
				ItemType: FUND,
				ItemNum:  in.Amount,
			})
		}
	})
	return nil, nil
}

func (gss *GameServerService) AidResource(in *gameServerService.AidResourceRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode := gss.app.allianceData.AidResource(gss.app.db, gss.app, in)
		gss.getClient().OnAidResourceResult(&gameServerService.AidResourceResult{
			Uuid:    in.Uuid,
			ErrCode: errCode,
		})
		if errCode != ErrCodeSuccess {
			gss.getClient().OnReturnGuildFundNotify(&gameServerService.ReturnGuildFundNotify{
				GuildId:  in.FromGuildId,
				SrcType:  AID_COST,
				ItemType: IRON,
				ItemNum:  in.Amount,
			})
		}
	})
	return nil, nil
}

func (gss *GameServerService) GetLeagueFund(in *gameServerService.GetLeagueFundRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		fund := gss.app.allianceData.GetLeagueFund(in)
		gss.getClient().OnLeagueFundResult(&gameServerService.GetLeagueFundResult{
			Fund: fund,
			Uuid: in.Uuid,
		})
	})
	return nil, nil
}

// ==== Event & Chat ====

func (gss *GameServerService) GetEventList(in *gameServerService.GetEventListRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		events := gss.app.allianceData.GetEventList(in)
		gss.getClient().OnEventListResult(&gameServerService.GetEventListResult{
			Events: events,
			Uuid:   in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) SendChatMessage(in *gameServerService.SendChatMessageRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		errCode := gss.app.allianceData.SendChatMessage(gss.app.db, gss.app, in)
		gss.getClient().OnSendChatMessageResult(&gameServerService.SendChatMessageResult{
			Uuid:    in.Uuid,
			ErrCode: errCode,
		})
	})
	return nil, nil
}

func (gss *GameServerService) GetChatHistory(in *gameServerService.GetChatHistoryRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("alliance: get chat history", in.AllianceId)
		chats := gss.app.allianceData.GetChatHistory(in)
		gss.getClient().OnChatHistoryResult(&gameServerService.GetChatHistoryResult{
			Messages: chats,
			Uuid:     in.Uuid,
		})
	})
	return nil, nil
}

// ==== Guild Simple Info ====

func (gss *GameServerService) GetGuildSimpleInfo(in *gameServerService.GetGuildSimpleInfoRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		targetServerId := in.ServerId
		if targetServerId == 0 {
			appLog.Warn("alliance: GetGuildSimpleInfo serverId=0 not supported yet, guildId=", in.GuildId)
			// Notify the requester with an error.
			gss.getClient().OnGetGuildSimpleInfoResult(&gameServerService.GetGuildSimpleInfoResult{
				Uuid:    in.Uuid,
				ErrCode: 2, // server not resolved
			})
			return
		}
		targetGS := gss.app.getGameServer(targetServerId)
		if targetGS == nil {
			appLog.Warn("alliance: GetGuildSimpleInfo target server not connected, serverId=", targetServerId)
			gss.getClient().OnGetGuildSimpleInfoResult(&gameServerService.GetGuildSimpleInfoResult{
				Uuid:    in.Uuid,
				ErrCode: 3, // target server offline
			})
			return
		}
		// Store pending entry so OnCheckGuildSimpleInfoResult routes back to us.
		gss.app.allianceData.pendingGuildSimpleInfos.Store(in.Uuid, &pendingGuildSimpleInfo{
			requesterServerId: gss.serverId,
			createdAt:         time.Now(),
		})
		// Forward to the target game server.
		targetGS.getClient().CheckGuildSimpleInfo(&gameServerService.GetGuildSimpleInfoRequest{
			GuildId:  in.GuildId,
			ServerId: targetServerId,
			Uuid:     in.Uuid,
		})
	})
	return nil, nil
}

func (gss *GameServerService) OnCheckGuildSimpleInfoResult(in *gameServerService.GetGuildSimpleInfoResult) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		// Pop the pending entry.
		if raw, ok := gss.app.allianceData.pendingGuildSimpleInfos.LoadAndDelete(in.Uuid); ok {
			pending := raw.(*pendingGuildSimpleInfo)
			// Forward result to the original requester.
			requesterGS := gss.app.getGameServer(pending.requesterServerId)
			if requesterGS == nil {
				appLog.Warn("alliance: OnCheckGuildSimpleInfoResult requester server gone, serverId=", pending.requesterServerId)
				return
			}
			requesterGS.getClient().OnGetGuildSimpleInfoResult(&gameServerService.GetGuildSimpleInfoResult{
				Uuid:    in.Uuid,
				ErrCode: in.ErrCode,
				Info:    in.Info,
			})
		} else {
			appLog.Warn("alliance: OnCheckGuildSimpleInfoResult no pending entry, uuid=", in.Uuid)
		}
	})
	return nil, nil
}

func (gss *GameServerService) ReportGuildScore(in *gameServerService.ReportGuildScoreRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("alliance: report guild score", in.GuildId, in.GuildScore)
		errCode := gss.app.allianceData.ReportGuildScore(gss.app.db, gss.app, in)
		gss.getClient().OnReportGuildScoreResult(&gameServerService.ReportGuildScoreResult{
			Uuid:    in.Uuid,
			ErrCode: errCode,
		})
	})
	return nil, nil
}

func (gss *GameServerService) SyncGuildInfo(in *gameServerService.SyncGuildInfoRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("alliance: sync guild info", in.GuildId, in.GuildName)
		errCode := gss.app.allianceData.SyncGuildInfo(gss.app.db, gss.app, in)
		gss.getClient().OnSyncGuildInfoResult(&gameServerService.SyncGuildInfoResult{
			Uuid:    in.Uuid,
			ErrCode: errCode,
		})
	})
	return nil, nil
}

func (gss *GameServerService) RecruitLeagueMember(in *gameServerService.RecruitLeagueMemberRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("alliance: recruit league member", in.LeagueUUID)
		errCode := gss.app.allianceData.RecruitLeagueMember(gss.app, in.LeagueUUID)
		gss.getClient().OnRecruitLeagueMemberResult(&gameServerService.RecruitLeagueMemberResult{
			Uuid:       in.Uuid,
			ErrCode:    errCode,
			LeagueUUID: in.LeagueUUID,
		})
	})
	return nil, nil
}

func (gss *GameServerService) CheckLeaveGuild(in *gameServerService.CheckLeaveGuildRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("alliance: check leave guild", in.LeagueUUID, in.GuildId, in.PlayerGbId)
		ret := gss.app.allianceData.CheckLeaveGuild(gss.app.db, gss.app, in.LeagueUUID, in.GuildId, in.PlayerGbId)
		gss.getClient().OnCheckLeaveGuildResult(&gameServerService.CheckLeaveGuildResult{
			Uuid:       in.Uuid,
			Ret:        ret,
			GuildId:    in.GuildId,
			PlayerGbId: in.PlayerGbId,
		})
	})
	return nil, nil
}

func (gss *GameServerService) QueryLeagueUUID(in *gameServerService.QueryLeagueUUIDRequest) (*gameServerService.Void, error) {
	common.ExecuteConcurrently(func() {
		appLog.Info("alliance: query league uuid", in.GuildId)
		leagueUUID, ret := gss.app.allianceData.QueryLeagueUUID(in.GuildId)
		gss.getClient().OnQueryLeagueUUIDResult(&gameServerService.QueryLeagueUUIDResult{
			Uuid:       in.Uuid,
			Ret:        ret,
			LeagueUUID: leagueUUID,
			GuildId:    in.GuildId,
		})
	})
	return nil, nil
}
