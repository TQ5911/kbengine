package allianceApp

import (
	"centralService/src/allianceService/allianceApp/gameServerService"
	"centralService/src/appLog"
	"centralService/src/common/concurrent_map"
	"database/sql"
	"fmt"
	"math"
	"sort"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"
	"unicode/utf8"
)

const (
	// 资金
	FUND = 1
	// 玄铁
	IRON = 2
)

const (
	// 敌对消耗
	ENEMY_COST = 1
	// 捐赠消耗
	DONATE_COST = 2
	// 援助消耗
	AID_COST = 3
)

const (
	ErrCodeSuccess                                = 0
	ErrCodeGameServerMissing                      = 1
	ErrCodeGameClientMissing                      = 2
	ErrCodeNoGuildConstCfg                        = 3
	ErrCodeNoMessageGuildLogCfg                   = 4
	ErrCodeNoMessageChatMessageCfg                = 5
	ErrCodeGuildNotLeader                         = 1001
	ErrCodeAlreadyInAlliance                      = 1002
	ErrCodeNotInAlliance                          = 1003
	ErrCodeAllianceFull                           = 1004
	ErrCodeAllianceNotFound                       = 1005
	ErrCodeApplyLimitReached                      = 1006
	ErrCodeApplyListFull                          = 1007
	ErrCodeGuildInWar                             = 1008
	ErrCodeNotAllianceLeader                      = 1009
	ErrCodeCooldown                               = 1010
	ErrCodeAidTooSoon                             = 1011
	ErrCodeInsufficientFund                       = 1012
	ErrCodeNameInvalid                            = 1013
	ErrCodeAlreadyApplied                         = 1014
	ErrCodeApplyNotFound                          = 1015
	ErrCodeInviteNotFound                         = 1016
	ErrCodeTargetAllianceMember                   = 1017
	ErrCodeWarAlreadyExists                       = 1018
	ErrCodeWarNotFound                            = 1019
	ErrCodeMemberNotFound                         = 1020
	ErrCodeCannotWarAllianceMember                = 1021
	ErrCodeGuildJoiningWar                        = 1022
	ErrCodeDeclarationInvalid                     = 1023
	ErrCodeCannotWarAllianceGuild                 = 1024 // Alliance cannot declare war on guild in another alliance
	ErrCodeGuildCannotWarAlliance                 = 1025 // Guild in alliance cannot declare war on an alliance
	ErrCodeNameAlreadyExists                      = 1026 // Alliance name already taken
	ErrCodeCannotWarSameAlliance                  = 1027 // Guilds in same alliance cannot declare war on each other
	ErrCodeGuildNotFound                          = 1028 // 申请加入的帮会在源服务器上不存在
	ErrCodeGuildSourceServerOffline               = 1029 // 帮会所在源服务器未连接到 allianceService, 无法校验帮会存在
	ErrCodeInviteTargetServerOffline              = 1030 // 邀请的目标帮会所在服务器未连接到 allianceService, 无法校验目标帮会存在
	ErrCodeAlreadyInvited                         = 1031
	ErrCodeYouAreLeader                           = 1032
	ErrCodeAidResourceFail                        = 1033
	ErrCodeDeclareWarSameId                       = 1034
	ErrCodeCannotWarSameGuild                     = 1035
	ErrCodeCannotWarTargetAllianceIsNotExisted    = 1036
	ErrCodeDifferentServerInDeclareWarIsForbidden = 1037
	ErrCodeWrongTargetServerIdInDeclareWar        = 1038

	MemberRoleLeader = 1
	MemberRoleMember = 2

	ApplyStatusPending  = 0
	ApplyStatusApproved = 1
	ApplyStatusRejected = 2
	ApplyStatusCanceled = 3

	InviteStatusPending  = 0
	InviteStatusAccepted = 1
	InviteStatusRejected = 2

	AllianceChangedInfo    = 1
	AllianceChangedJoin    = 2
	AllianceChangedLeave   = 3
	AllianceChangedDisband = 4

	WarAttackTypeAlliance = 1
	WarAttackTypeGuild    = 2
	WarTargetTypeAlliance = 1
	WarTargetTypeGuild    = 2

	EventCreate         = 1
	EventJoin           = 2
	EventLeave          = 3
	EventKick           = 4
	EventWarDeclared    = 5
	EventWarTarget      = 6
	EventAid            = 7
	EventDonate         = 8
	EventAllianceWar    = 9
	EventAllianceTarget = 10
)

// 敌对类型
const (
	// 联盟
	enemyTypeAlliance = 1
	// 帮会
	enemyTypeGuild = 2
)

const (
	// 资金
	guildAssetTypeFund = 1
	// 玄铁
	guildAssetTypeIron = 2
)

// MaxEventsPerAlliance is the cap for the per-alliance event log.
// Both the in-memory cache and the MySQL `alliance_event` table keep at most
// this many rows per alliance. When the cap is exceeded, the oldest entries
// (by created_at, then id) are dropped from cache and deleted from DB.

type broadcastFunc func(func(*gameServerService.GameClientClient))

// guildApplyRecord is the per-guild "where have I applied?" index. A guild
// may apply to many alliances simultaneously; this index lets us look up
// the full pending-apply set for a guild in O(1) instead of scanning every
// alliance's applies map. Membership changes (apply, cancel, approve-elsewhere)
// are tracked here in lockstep with the per-alliance `cache.applies` map.
type guildApplyRecord struct {
	sync.RWMutex
	// allianceId -> applyInfo (each guild can have at most one pending apply
	// per alliance, so the allianceId is a unique key within this set).
	items map[uint64]*gameServerService.AllianceApplyInfo
}

func newGuildApplyRecord() *guildApplyRecord {
	return &guildApplyRecord{items: make(map[uint64]*gameServerService.AllianceApplyInfo)}
}

// addGuildApply registers a pending apply for the given guild in the
// per-guild index. Safe to call concurrently. The caller must also have
// updated the per-alliance `cache.applies` map.
func (ad *AllianceData) addGuildApply(guildId uint64, applyInfo *gameServerService.AllianceApplyInfo) {
	if applyInfo == nil {
		return
	}
	ad.guildAppliesLock.Lock()
	defer ad.guildAppliesLock.Unlock()
	rec, ok := ad.guildApplies[guildId]
	if !ok {
		rec = newGuildApplyRecord()
		ad.guildApplies[guildId] = rec
	}
	rec.Lock()
	defer rec.Unlock()
	rec.items[applyInfo.AllianceId] = applyInfo
}

// removeGuildApply drops the pending apply for (guildId, allianceId) from
// the per-guild index. Cleans up the outer entry when the inner set goes empty.
func (ad *AllianceData) removeGuildApply(guildId, allianceId uint64) bool {
	ad.guildAppliesLock.Lock()
	defer ad.guildAppliesLock.Unlock()
	rec, ok := ad.guildApplies[guildId]
	if !ok {
		return false
	}
	rec.Lock()
	defer rec.Unlock()
	delete(rec.items, allianceId)
	empty := len(rec.items) == 0
	if empty {
		// Re-check inside the write lock; another goroutine may have re-added.
		if cur, ok := ad.guildApplies[guildId]; ok && cur == rec && len(cur.items) == 0 {
			delete(ad.guildApplies, guildId)
		}
	}
	return true
}

// guildInviteRecord is the per-guild "who has invited me?" index. A guild
// can be invited by many alliances simultaneously; this index lets GetInviteList
// (invitee view) return all pending invites targeting a guild in O(K) where K
// is the number of pending invites for that guild, instead of scanning every
// alliance's `invites` map.
//
// We key the inner set by inviteId (not allianceId) because:
//   - An invite has a globally unique inviteId (DB AUTOINCREMENT).
//   - inviteId is what the caller (AcceptInvite / RejectInvite / completeInviteGuild)
//     already has at hand for removal — no extra lookup needed.
//   - The value (AllianceInviteInfo) carries AllianceId + GuildId, so the
//     cross-references are still recoverable.
type guildInviteRecord struct {
	sync.RWMutex
	items map[uint64]*gameServerService.AllianceInviteInfo
}

func newGuildInviteRecord() *guildInviteRecord {
	return &guildInviteRecord{items: make(map[uint64]*gameServerService.AllianceInviteInfo)}
}

// addGuildInvite registers a pending invite targeting `guildId` in the
// per-guild index. Safe to call concurrently. The caller must also have
// updated the per-alliance `cache.invites` map. If an entry with the same
// inviteId already exists, it's overwritten (the new value is the latest
// snapshot — covers DB reload + fresh write in the same restart window).
func (ad *AllianceData) addGuildInvite(guildId uint64, inviteInfo *gameServerService.AllianceInviteInfo) {
	if inviteInfo == nil {
		return
	}
	ad.invitesByGuildLock.Lock()
	defer ad.invitesByGuildLock.Unlock()
	rec, ok := ad.invitesByGuild[guildId]
	if !ok {
		rec = newGuildInviteRecord()
		ad.invitesByGuild[guildId] = rec
	}
	rec.Lock()
	defer rec.Unlock()
	// Inner key is the inviteId (not allianceId) — inviteId is the
	// globally unique row id and is what the call sites
	// (AcceptInvite / RejectInvite / completeInviteGuild) have at
	// hand for the matching remove. allianceId alone could collide
	// if the same guild ever received two invites from the same
	// alliance at different times (the second would silently
	// overwrite the first in the old code).
	rec.items[inviteInfo.AllianceId] = inviteInfo
}

// removeGuildInvite drops the pending invite with the given inviteId from
// the per-guild index for `guildId`. Cleans up the outer entry when the
// inner set goes empty. Returns false if no record exists for that guild.
func (ad *AllianceData) removeGuildInvite(guildId, allianceId uint64) bool {
	ad.invitesByGuildLock.Lock()
	defer ad.invitesByGuildLock.Unlock()
	rec, ok := ad.invitesByGuild[guildId]
	if !ok {
		return false
	}
	rec.Lock()
	defer rec.Unlock()
	delete(rec.items, allianceId)
	empty := len(rec.items) == 0
	if empty {
		// Re-check inside the write lock; another goroutine may have re-added.
		if cur, ok := ad.invitesByGuild[guildId]; ok && cur == rec && len(cur.items) == 0 {
			delete(ad.invitesByGuild, guildId)
		}
	}
	return true
}

// removeAllGuildInvitesForAlliance sweeps every per-guild entry and removes
// the invite if it was sent by `allianceId`. Used by DisbandLeague: when an
// alliance is removed from `ad.alliances`, all of its pending invites
// (stored in the per-guild index) must be cleared so GetInviteList does not
// return dangling entries pointing at a now-deleted alliance.
//
// O(G) where G is the number of guilds that had a pending invite from this
// alliance — bounded by the active invite set, not the total guild count.
func (ad *AllianceData) removeAllGuildInvitesForAlliance(allianceId uint64) {
	ad.invitesByGuildLock.Lock()
	defer ad.invitesByGuildLock.Unlock()
	for guildId, rec := range ad.invitesByGuild {
		rec.Lock()
		for inviteId, inv := range rec.items {
			if inv != nil && inv.AllianceId == allianceId {
				delete(rec.items, inviteId)
			}
		}
		empty := len(rec.items) == 0
		rec.Unlock()
		if empty {
			delete(ad.invitesByGuild, guildId)
		}
	}
}

// getGuildInvites returns a snapshot of all pending invites targeting
// `guildId`, ordered by createdAt ASC then inviteId ASC (stable). Returns
// an empty slice (not nil) when the guild has no pending invites — callers
// can rely on `len(...) == 0` to distinguish "no invites" from "unknown".
func (ad *AllianceData) getGuildInvites(guildId uint64) []*gameServerService.AllianceInviteInfo {
	ad.invitesByGuildLock.RLock()
	rec, ok := ad.invitesByGuild[guildId]
	ad.invitesByGuildLock.RUnlock()
	if !ok {
		return []*gameServerService.AllianceInviteInfo{}
	}
	rec.RLock()
	defer rec.RUnlock()
	out := make([]*gameServerService.AllianceInviteInfo, 0, len(rec.items))
	for _, inv := range rec.items {
		if inv == nil {
			continue
		}
		out = append(out, inv)
	}
	// Stable order: oldest invites first, ties broken by inviteId.
	sort.SliceStable(out, func(i, j int) bool {
		if out[i].CreatedAt != out[j].CreatedAt {
			return out[i].CreatedAt < out[j].CreatedAt
		}
		return out[i].InviteId < out[j].InviteId
	})
	return out
}

// cancelOtherGuildApplies cancels every pending apply for `guildId` except
// the one to `joinedAllianceId`. Returns the list of (allianceId, applyInfo)
// pairs that were cancelled so the caller can fire leader notifications.
//
// Used by ApproveJoin (auto-approve) and completeApproveJoin (manual) to
// enforce "one guild in one alliance": as soon as this guild is accepted
// somewhere, all other pending applications are stale and must be revoked.
//
// O(K) where K is the number of OTHER alliances this guild applied to
// (NOT the total number of alliances in the system).
//
// db may be nil (test path) — in that case the SQL update is skipped, but
// the in-memory cache + index are still maintained so callers can exercise
// the algorithm end-to-end.
func (ad *AllianceData) buildCancelledApply(data *cancelledApply) *cancelledApply {
	return &cancelledApply{
		AllianceId:         data.AllianceId,
		AllianceName:       data.AllianceName,
		AllianceTotalScore: data.AllianceTotalScore,
		ApplyId:            data.ApplyId,
		GuildId:            data.GuildId,
		GuildName:          data.GuildName,
		GuildServerId:      data.GuildServerId,
		GuildScore:         data.GuildScore,
		GuildIcon:          data.GuildIcon,
		DspFlag:            data.DspFlag,
		LeaderGuildId:      data.LeaderGuildId,
		LeaderServerId:     data.LeaderServerId,
	}
}

func (ad *AllianceData) buildAllianceApplyInfo(data *gameServerService.AllianceApplyInfo) *gameServerService.AllianceApplyInfo {
	return &gameServerService.AllianceApplyInfo{
		ApplyId:          data.ApplyId,
		AllianceId:       data.AllianceId,
		GuildId:          data.GuildId,
		GuildName:        data.GuildName,
		GuildScore:       data.GuildScore,
		ServerId:         data.ServerId,
		Status:           data.Status,
		CreatedAt:        data.CreatedAt,
		LeaderGuildId:    data.LeaderGuildId,
		GuildIcon:        data.GuildIcon,
		DspFlag:          data.DspFlag,
		MemberCount:      data.MemberCount,
		GuildLevel:       data.GuildLevel,
		MaxMemberNum:     data.MaxMemberNum,
		LeaderGbId:       data.LeaderGbId,
		LeaderName:       data.LeaderName,
		LeaderLevel:      data.LeaderLevel,
		LeaderProfession: data.LeaderProfession,
		LeaderGender:     data.LeaderGender,
	}
}

func (ad *AllianceData) cancelOtherGuildApplies(db *sql.DB, guildId, joinedAllianceId uint64) []*cancelledApply {
	ad.guildAppliesLock.Lock()
	rec, ok := ad.guildApplies[guildId]
	ad.guildAppliesLock.Unlock()
	if !ok {
		return nil
	}

	// Phase 1: enumerate under the inner RLock, decide what to cancel.
	rec.Lock()

	var toCancel []*gameServerService.AllianceApplyInfo
	for allianceId, apply := range rec.items {
		if allianceId == joinedAllianceId {
			continue
		}
		toCancel = append(toCancel, ad.buildAllianceApplyInfo(apply))
	}
	rec.Unlock()
	if len(toCancel) == 0 {
		return nil
	}

	// Phase 2: mutate under write lock + DB.
	cancelled := make([]*cancelledApply, 0, len(toCancel))
	for _, apply := range toCancel {
		if db != nil {
			db.Exec("UPDATE alliance_apply SET apply_state = ? WHERE id = ?", ApplyStatusCanceled, apply.ApplyId)
		}
		// Snapshot the target alliance's leader routing + display data
		// while we already hold the per-alliance lock, so the caller can
		// fire the cancel notification without re-acquiring it later.
		// We pull (name, leaderServerId, totalScore) in one go — all
		// three feed the ApplyCancelledItem on the guild-side notify,
		// and leaderServerId also routes the alliance-side notify.
		var (
			allianceName       string
			leaderServerId     uint32
			allianceTotalScore uint64
		)
		if targetCache, ok := ad.alliances.Get(apply.AllianceId); ok {
			targetCache.Lock()

			delete(targetCache.applies, guildId)
			if targetCache.info != nil {
				allianceName = targetCache.info.Name
				leaderServerId = targetCache.info.LeaderServerId
				allianceTotalScore = targetCache.info.TotalScore
			}
			targetCache.Unlock()
		}
		cancelled = append(cancelled, &cancelledApply{
			AllianceId:         apply.AllianceId,
			AllianceName:       allianceName,
			AllianceTotalScore: allianceTotalScore,
			ApplyId:            apply.ApplyId,
			GuildId:            guildId,
			GuildName:          apply.GuildName,
			GuildServerId:      apply.ServerId,
			GuildScore:         apply.GuildScore,
			GuildIcon:          apply.GuildIcon,
			DspFlag:            apply.DspFlag,
			LeaderGuildId:      apply.LeaderGuildId,
			LeaderServerId:     leaderServerId,
		})
		rec.Lock()
		delete(rec.items, apply.AllianceId)
		rec.Unlock()
	}
	rec.RLock()
	empty := len(rec.items) == 0
	rec.RUnlock()
	// Phase 3: clean outer entry if needed.
	if empty {
		ad.guildAppliesLock.Lock()
		delete(ad.guildApplies, guildId)
		ad.guildAppliesLock.Unlock()
	}
	return cancelled
}

// cancelledApply is the small record emitted by cancelOtherGuildApplies so
// the caller can notify both affected alliance leaders (their inbox
// needs the apply row dropped) AND the originating guild leader (their
// "sent applies" view needs the rows dropped). Carries just enough
// routing + display data for both notification paths.
//
// Routing fields:
//   - LeaderServerId : game server hosting the cancelled alliance's
//     leader (== recipient of OnApplyCancelledNotify). Equivalent to
//     AllianceInfo.LeaderServerId — i.e. "the server this alliance
//     lives on".
//   - GuildServerId  : game server hosting the applying guild
//     (== recipient of OnSelfAppliesCancelledNotify).
//
// Display fields (carried into ApplyCancelledItem on the wire):
//   - AllianceName      : alliance display label
//   - AllianceTotalScore: alliance power (== AllianceInfo.TotalScore),
//     included so the guild's sent-applies view can keep its row
//     layout consistent across refresh + cancel.
type cancelledApply struct {
	AllianceId         uint64
	AllianceName       string
	AllianceTotalScore uint64
	ApplyId            uint64
	GuildId            uint64
	GuildName          string
	GuildServerId      uint32
	GuildScore         uint64
	GuildIcon          uint32
	DspFlag            uint32
	LeaderGuildId      uint64
	LeaderServerId     uint32
}

type AllianceData struct {
	db              *sql.DB
	alliances       concurrent_map.ConcurrentMap[uint64, *AllianceCache]
	guildToAlliance concurrent_map.ConcurrentMap[uint64, uint64]
	broadcast       broadcastFunc
	// guildApplies is the global per-guild pending-apply index. Guarded
	// by guildAppliesLock so reads (ApplyToJoin pre-checks, GetSentApplies)
	// don't contend with writes (apply/approve/cancel).
	//
	// Why this matters: a single approval in ApproveJoin needs to cancel
	// every OTHER pending apply for that guild. Without this index the code
	// would do O(N_alliances) scans; with it the work is O(K) where K is
	// the (small) number of pending applies for that specific guild.
	guildApplies     map[uint64]*guildApplyRecord
	guildAppliesLock sync.RWMutex
	// invitesByGuild is the global per-guild pending-invite index. A guild
	// can be invited by many alliances simultaneously; this index lets
	// GetInviteList (invitee view) answer "show me all invites targeting
	// guild X" in O(K) where K is the number of pending invites for X,
	// instead of scanning every alliance's `invites` map.
	//
	// Maintained in lockstep with the per-alliance `cache.invites` map:
	//   - addGuildInvite  — InviteGuild / completeInviteGuild / DB load
	//   - removeGuildInvite — AcceptInvite / RejectInvite / DisbandLeague
	invitesByGuild     map[uint64]*guildInviteRecord
	invitesByGuildLock sync.RWMutex
	// sortedAlliances is a parallel index over `alliances` maintained in
	// sort-key order: totalScore DESC, memberCount DESC, createdAt ASC,
	// allianceId ASC. It is rebuilt incrementally whenever a cache's
	// derived fields change, so GetLeagueList / SearchLeague can serve
	// from this slice without sorting on every read.
	sortedAlliances []*AllianceCache
	sortedLock      sync.RWMutex

	// allianceNames is a case-insensitive name → allianceId map used to
	// reject duplicate alliance names in CreateLeague / ModifyLeagueInfo
	// without hitting the DB. Populated at startup in loadFromDB and kept
	// in sync via the helpers below.
	allianceNames     map[string]uint64
	allianceNamesLock sync.RWMutex

	// pendingApproveJoins tracks ApproveJoin requests that are mid-flight on
	// a cross-server guild existence check. Keyed by the internal uuid we
	// stamped on the outbound CheckGuildExistsRequest. Populated by
	// ApproveJoin when it decides to defer the result; resolved by the
	// OnCheckGuildExistsResult handler (or by the game-server disconnect
	// sweep). Concurrent-safe via sync.Map.
	pendingApproveJoins sync.Map
	// pendingInviteGuilds tracks InviteGuild requests that are mid-flight on
	// a cross-server guild existence check (target guild on TargetServerId).
	// Same uuid-keyed sync.Map shape as pendingApproveJoins, sharing the
	// same OnCheckGuildExistsResult handler — the handler tries
	// pendingApproveJoins first, then pendingInviteGuilds.
	pendingInviteGuilds sync.Map
	// pendingDeclareWars tracks DeclareWar requests that are mid-flight
	// on a cross-server guild existence check for a *lone target guild*
	// (i.e. targetType=Guild AND target not in ad.guildToAlliance). Same
	// uuid-keyed sync.Map shape; the OnCheckGuildExistsResult handler
	// tries the three maps in order.
	pendingDeclareWars sync.Map
	// pendingGuildSimpleInfos tracks GetGuildSimpleInfo requests that are
	// mid-flight for a cross-server guild simple info query. Keyed by the
	// caller-supplied uuid from GetGuildSimpleInfoRequest. Populated by
	// GetGuildSimpleInfo when it forwards the CheckGuildSimpleInfo to the
	// target game server; resolved by OnCheckGuildSimpleInfoResult.
	// Concurrent-safe via sync.Map.
	pendingGuildSimpleInfos sync.Map
	// pendingApproveUUID monotonically allocates uuids for the outbound
	// CheckGuildExistsRequest. Avoids colliding with caller-supplied UUIDs
	// by starting from a high offset.
	pendingApproveUUID uint64

	// sendCheckGuildExistsHook fires the cross-server guild existence check.
	// Returns false when the source game server is not connected. Tests
	// override this to capture the call without needing a real trpc channel.
	sendCheckGuildExistsHook func(app *AllianceApp, srcServerId uint32, guildId, uuid uint64, checkCD bool) bool

	// notifyAllianceCancelHook fires OnApplyCancelledNotify to the
	// affected alliance leader's game server. Tests override this to
	// capture the call without needing a live trpc channel; production
	// code leaves it nil and falls through to the real dispatch path.
	// joinedAllianceId is the alliance the applying guild actually
	// joined (== the "context" field on the wire), c is the per-apply
	// record describing the apply being cancelled.
	notifyAllianceCancelHook func(app *AllianceApp, joinedAllianceId uint64, c *cancelledApply)

	// notifyGuildCancelHook fires OnSelfAppliesCancelledNotify (the
	// batched "your other applies were cancelled" notify) to the
	// applying guild's game server. Same hook-vs-real-dispatch split
	// as notifyAllianceCancelHook. cancelled is the FULL list returned
	// by cancelOtherGuildApplies so the test can assert the whole batch.
	notifyGuildCancelHook func(app *AllianceApp, guildId, joinedAllianceId uint64, cancelled []*cancelledApply)
	isInited              bool
	initedLock            sync.RWMutex
}

// pendingApproveJoin captures every piece of state needed to finish an
// ApproveJoin after a successful guild-existence check on the source server.
type pendingApproveJoin struct {
	allianceId        uint64
	guildId           uint64
	applyId           uint64
	applyInfo         *gameServerService.AllianceApplyInfo // snapshot, not a live pointer
	originalUuid      uint64                               // alliance leader's UUID, used in the deferred OnApproveJoinResult
	leaderServerId    uint32                               // game server to send the final result back to
	requesterServerId uint32                               // game server that sent the ApproveJoin (== leaderServerId in normal flow)
	createdAt         time.Time
	messageId         uint64
	eventLimit        uint32
}

// pendingInviteGuild captures every piece of state needed to finish an
// InviteGuild after a successful guild-existence check on the target
// guild's game server (TargetServerId). The structure mirrors
// pendingApproveJoin but the routing is inverted — the *target* guild's
// server is the one doing the existence check, and the *inviter*
// (alliance leader) is who needs the final OnInviteGuildResult back.
type pendingInviteGuild struct {
	allianceId            uint64                                // inviter's alliance
	targetGuildId         uint64                                // guild being invited
	targetServerId        uint32                                // server hosting the target guild (== source for the check)
	inviterLeaderServerId uint32                                // server to send OnInviteGuildResult back to
	originalUuid          uint64                                // inviter's UUID, echoed in the deferred OnInviteGuildResult
	inviteeSnapshot       *gameServerService.AllianceInviteInfo // pre-built cache row (invitee-guild data + inviter name fields); mutated under cache.Lock when the deferred callback runs
	createdAt             time.Time
}

// pendingDeclareWar captures every piece of state needed to finish a
// DeclareWar after a successful guild-existence check on the *target
// guild's* game server (in.TargetServerId). Mirrors pendingInviteGuild:
// the target's server does the existence check, the attacker's
// server gets the final OnDeclareWarResult.
//
// Only created when in.TargetType == WarTargetTypeGuild AND the
// target guild is NOT in ad.guildToAlliance (i.e. a "lone" target —
// we don't have it in any alliance cache and can't otherwise verify
// it exists). Alliance↔Alliance and guild-in-an-alliance targets
// skip this check entirely.
type pendingDeclareWar struct {
	attackType                             uint32
	attackId                               uint64
	attackServerId                         uint32
	targetType                             uint32
	targetId                               uint64
	targetServerId                         uint32 // server hosting the target guild (== source for the existence check)
	attackerServerId                       uint32 // game server to send OnDeclareWarResult back to
	originalUuid                           uint64 // attacker's UUID, echoed in the deferred OnDeclareWarResult
	endTime                                uint32 // war declaration's expiry, fixed at DeclareWar time (not at callback time)
	warCost                                uint64 // pre-computed cost for alliance-initiated war; 0 if attacker is a guild
	createdAt                              time.Time
	declareWarEventIdAllianceToGuild       int
	declareWarMsgIdAllianceToGuild         int
	declareWarMsgIdGuildToGuild            int
	eventLimit                             int
	fromGuildName                          string
	toGuildName                            string
	amount                                 uint64
	guildEventIdAllianceToGuild            int
	guildEventIdGuildAttackToGuildTarget   int
	guildEventIdGuildTargetFromGuildAttack int
}

// pendingGuildSimpleInfo captures the state needed to route a guild simple
// info query result back to the originating game server. The requester
// sends GetGuildSimpleInfo with a caller-supplied uuid; the allianceService
// forwards CheckGuildSimpleInfo to the target game server, and when
// OnCheckGuildSimpleInfoResult arrives with that same uuid, it sends
// OnGetGuildSimpleInfoResult back to the requester via this struct.
type pendingGuildSimpleInfo struct {
	requesterServerId uint32
	createdAt         time.Time
}

func newPendingApproveUUID() uint64 {
	// Start at 1<<48 so internal UUIDs never collide with caller UUIDs.
	return atomic.AddUint64(&pendingApproveUUIDBase, 1)
}

var pendingApproveUUIDBase uint64 = 1 << 48

type AllianceCache struct {
	sync.RWMutex
	info    *gameServerService.AllianceInfo
	members map[uint64]*gameServerService.AllianceMemberInfo
	applies map[uint64]*gameServerService.AllianceApplyInfo
	invites map[uint64]*gameServerService.AllianceInviteInfo
	// events stores the most recent MaxEventsPerAlliance events for the
	// alliance, ordered ASC by (created_at, id) — i.e. oldest at [0], newest
	// at the tail. Cap is enforced on every append in `addEvent`.
	events []*gameServerService.AllianceEventInfo
}

func uint64Sharding(key uint64) uint32 {
	return uint32(key)
}

// EnemiesCache stores the original (AttackType, targetType, endTime)
// war row metadata. The per-guild enemy view lives in
// guildRelationCache (fed via AddRelation with GuildRelationEnemy) —
// that cache is the source of truth for "is X hostile to Y" and
// what GetEnemyList reads.
//
// byRow survives here because three management paths still need the
// original row shape:
//
//   - checkAndRemoveExpiredWars scans byRow for expired endTimes,
//     then issues DB DELETE + OnWarEnded broadcast with the
//     original (AttackType, targetType).
//   - DisbandLeague iterates byRow to find every war row touching
//     the disbanded alliance, then calls removeEnemyPairs.
//   - CancelWar (via removeEnemyPairs) drops the byRow entry so the
//     same row can't be removed twice.
type EnemiesCache struct {
	sync.RWMutex
	// byRow[enemyKey] = AllianceEnemyInfo (the original war row).
	byRow map[string]*gameServerService.AllianceEnemyInfo
}

var enemiesCache = &EnemiesCache{
	byRow: make(map[string]*gameServerService.AllianceEnemyInfo),
}

// guildEnemyAllianceCache is the per-guild inverse index from guildId
// to the alliances that guild is at war with. Updated in lockstep with
// addEnemyPairs / removeEnemyPairs so it always reflects the active war
// set without an extra scan. Read by GetEnemyAllianceList.
//
// byGuild[guildId][allianceId] = endTime  (0 if the war has no expiry)
type guildEnemyAllianceCacheType struct {
	sync.RWMutex
	byGuild map[uint64]map[uint64]uint32
}

var guildEnemyAllianceCache = &guildEnemyAllianceCacheType{
	byGuild: make(map[uint64]map[uint64]uint32),
}

func (c *guildEnemyAllianceCacheType) add(guildId, allianceId uint64, endTime uint32) {
	c.Lock()
	defer c.Unlock()
	m, ok := c.byGuild[guildId]
	if !ok {
		m = make(map[uint64]uint32)
		c.byGuild[guildId] = m
	}
	m[allianceId] = endTime
}

func (c *guildEnemyAllianceCacheType) remove(guildId, allianceId uint64) {
	c.Lock()
	defer c.Unlock()
	m, ok := c.byGuild[guildId]
	if !ok {
		return
	}
	delete(m, allianceId)
	if len(m) == 0 {
		delete(c.byGuild, guildId)
	}
}

// entitySideInvolvesGuild reports whether `guildId` is on `sideType` of a
// war row. A guild is involved when it is the row's entity directly (a guild
// on that side) or when it is currently a member of the alliance named as
// the entity on that side.
func (ad *AllianceData) entitySideInvolvesGuild(sideType uint32, entityId, guildId uint64, cache *AllianceCache) bool {
	if sideType == WarAttackTypeAlliance || sideType == WarTargetTypeAlliance {
		// The side names an alliance; only a current member is involved.
		if nil != cache && cache.info.AllianceId == entityId {
			_, ok := cache.members[guildId]
			return ok
		}
		cache, ok := ad.alliances.Get(entityId)
		if !ok {
			return false
		}
		cache.RLock()
		_, ok = cache.members[guildId]
		cache.RUnlock()
		return ok
	}
	return entityId == guildId
}

// resolveOppositeSideGuilds expands the side `sideType` of a war row into the
// concrete list of guildIds on that side (a single element for a guild entity,
// the current member set for an alliance entity). Used for query derivation.
func (ad *AllianceData) resolveOppositeSideGuilds(sideType uint32, entityId uint64) []uint64 {
	if sideType == WarAttackTypeAlliance || sideType == WarTargetTypeAlliance {
		return ad.getMemberGuildIDs(entityId)
	}
	return []uint64{entityId}
}

// getEnemyRelationsForGuild derives the list of guilds that `guildId` is
// currently hostile toward (slash at war with) from the entity-level war rows
// in enemiesCache.byRow plus current alliance membership.
//
// For each war row, if `guildId` is a participant on either side (directly as
// a guild or via its current alliance membership), every guild on the opposite
// side — resolved to concrete guilds — is an enemy of `guildId` (excluding
// `guildId` itself). This recomputes from live state each call, so a guild that
// leaves an alliance immediately stops inheriting that alliance's wars while
// its own direct guild-vs-guild wars remain (those rows are independent).
func (ad *AllianceData) getEnemyRelationsForGuild(guildId uint64) []uint64 {
	seen := make(map[uint64]struct{})
	var out []uint64
	enemiesCache.RLock()
	defer enemiesCache.RUnlock()
	for _, row := range enemiesCache.byRow {
		attackerInvolved := ad.entitySideInvolvesGuild(row.AttackType, row.AttackId, guildId, nil)
		targetInvolved := ad.entitySideInvolvesGuild(row.TargetType, row.TargetId, guildId, nil)
		if attackerInvolved {
			for _, eg := range ad.resolveOppositeSideGuilds(row.TargetType, row.TargetId) {
				if eg != 0 && eg != guildId {
					if _, dup := seen[eg]; !dup {
						seen[eg] = struct{}{}
						out = append(out, eg)
					}
				}
			}
		}
		if targetInvolved {
			for _, eg := range ad.resolveOppositeSideGuilds(row.AttackType, row.AttackId) {
				if eg != 0 && eg != guildId {
					if _, dup := seen[eg]; !dup {
						seen[eg] = struct{}{}
						out = append(out, eg)
					}
				}
			}
		}
	}
	return out
}

// getEnemyRelationsForAlliance derives the list of guilds that `allianceId`
// (as a whole) is at war with. Scans every entity row touching the alliance on
// either side and resolves the opposite side to concrete guilds. Used to answer
// "which guilds is this alliance fighting" independently of any single member.
func (ad *AllianceData) getEnemyRelationsForAlliance(allianceId uint64) []uint64 {
	seen := make(map[uint64]struct{})
	var out []uint64
	enemiesCache.RLock()
	defer enemiesCache.RUnlock()
	for _, row := range enemiesCache.byRow {
		if row.AttackType == WarAttackTypeAlliance && row.AttackId == allianceId {
			for _, eg := range ad.resolveOppositeSideGuilds(row.TargetType, row.TargetId) {
				if eg != 0 {
					if _, dup := seen[eg]; !dup {
						seen[eg] = struct{}{}
						out = append(out, eg)
					}
				}
			}
		}
		if row.TargetType == WarTargetTypeAlliance && row.TargetId == allianceId {
			for _, eg := range ad.resolveOppositeSideGuilds(row.AttackType, row.AttackId) {
				if eg != 0 {
					if _, dup := seen[eg]; !dup {
						seen[eg] = struct{}{}
						out = append(out, eg)
					}
				}
			}
		}
	}
	return out
}

// hasEntityEnemies reports whether `guildId` is currently involved in any war,
// either directly as a guild entity or indirectly as a member of an alliance
// that is a war party. Replaces the old per-pair GuildRelationCache.HasEnemies
// gate used before entity-level hostility: a guild cannot join an alliance
// while it is fighting (directly or via its current alliance).
func (ad *AllianceData) hasEntityEnemies(guildId uint64, cache *AllianceCache) bool {
	enemiesCache.RLock()
	defer enemiesCache.RUnlock()
	for _, row := range enemiesCache.byRow {
		if ad.entitySideInvolvesGuild(row.AttackType, row.AttackId, guildId, cache) ||
			ad.entitySideInvolvesGuild(row.TargetType, row.TargetId, guildId, cache) {
			return true
		}
	}
	return false
}

// getAllEnemyRelationsForSync returns every active entity-level war row plus
// the current alliance-relation version, for the RegisterGameServer full-state
// sync. Unlike GetAllRelations (which returns the per-pair guild cache), this
// comes straight from the authoritative entity store enemiesCache.byRow.
func (ad *AllianceData) getAllEnemyRelationsForSync() ([]*gameServerService.EnemyRelationInfo, uint32) {
	enemiesCache.RLock()
	defer enemiesCache.RUnlock()
	out := make([]*gameServerService.EnemyRelationInfo, 0, len(enemiesCache.byRow))
	for _, row := range enemiesCache.byRow {
		out = append(out, &gameServerService.EnemyRelationInfo{
			AttackType:     row.AttackType,
			AttackId:       row.AttackId,
			AttackServerId: row.AttackServerId,
			TargetType:     row.TargetType,
			TargetId:       row.TargetId,
			TargetServerId: row.TargetServerId,
			EndTime:        row.EndTime,
		})
	}
	guildRelationCache.RLock()
	version := guildRelationCache.version
	guildRelationCache.RUnlock()
	return out, version
}

// addEnemyPairs records ONE entity-level war row in enemiesCache.byRow
// and NOTHING else.
//
// Before the entity-level refactor this function expanded the war row into
// N×M guild↔guild pairs written into guildRelationCache (as
// GuildRelationEnemy) plus a guildEnemyAllianceCache inverse index. That
// flattened model is gone: guildRelationCache now carries UNION only, and
// per-guild hostility is DERIVED at runtime from the entity rows + current
// alliance membership (see getEnemyRelationsForGuild / hasEntityEnemies).
//
// `attackerServerId`/`targetServerId` are carried on the row so downstream
// consumers (broadcast, register sync) can route correctly.
func (ad *AllianceData) addEnemyPairs(AttackType, targetType uint32, AttackId, targetId uint64, endTime, attackerServerId, targetServerId uint32) {
	key := enemyKey(AttackType, AttackId, targetType, targetId)
	enemiesCache.Lock()
	enemiesCache.byRow[key] = &gameServerService.AllianceEnemyInfo{
		AttackType:     AttackType,
		AttackId:       AttackId,
		AttackServerId: attackerServerId,
		TargetType:     targetType,
		TargetId:       targetId,
		TargetServerId: targetServerId,
		EndTime:        endTime,
	}
	enemiesCache.Unlock()
}

// removeEnemyPairs is the inverse of addEnemyPairs — it drops the single
// entity-level war row from enemiesCache.byRow. Used by CancelWar,
// checkAndRemoveExpiredWars, and DisbandLeague. It never touches
// guildRelationCache (UNION-only) and never removes any other war row, so a
// guild's unrelated direct guild-vs-guild war survives if an alliance it was
// once part of is disbanded.
func (ad *AllianceData) removeEnemyPairs(AttackType, targetType uint32, AttackId, targetId uint64) {
	key := enemyKey(AttackType, AttackId, targetType, targetId)
	enemiesCache.Lock()
	delete(enemiesCache.byRow, key)
	enemiesCache.Unlock()
}

// Guild relation types
const (
	GuildRelationNone  = 0
	GuildRelationUnion = 1
	GuildRelationEnemy = 2
)

type GuildRelationCache struct {
	sync.RWMutex
	// relations[small_large] = GuildRelationInfo. Source of truth for
	// every per-pair guild↔guild relation (UNION, ENEMY, etc.). The
	// pair key is sorted (small, large) so AddRelation(1, 2) and
	// AddRelation(2, 1) hit the same entry.
	relations map[string]*gameServerService.GuildRelationInfo
	// byGuild[guildId][otherGuildId] = GuildRelationInfo. Per-guild
	// inverse index for O(K) "what relations does this guild have"
	// lookups. Maintained in lockstep with `relations` inside
	// AddRelation / RemoveRelation — every writer goes through those
	// two methods, so the two views cannot diverge.
	//
	// The value is the same pointer as in `relations`; updating
	// RelationType / EndTime on one updates the other (no copy).
	byGuild map[uint64]map[uint64]*gameServerService.GuildRelationInfo
	version uint32
}

var guildRelationCache = &GuildRelationCache{
	relations: make(map[string]*gameServerService.GuildRelationInfo),
	byGuild:   make(map[uint64]map[uint64]*gameServerService.GuildRelationInfo),
	version:   1,
}

func guildRelationKey(guildUUID1, guildUUID2 uint64) string {
	if guildUUID1 < guildUUID2 {
		return fmt.Sprintf("%d_%d", guildUUID1, guildUUID2)
	}
	return fmt.Sprintf("%d_%d", guildUUID2, guildUUID1)
}

// sortGuildIDs returns the two guild IDs sorted in ascending order
func sortGuildIDs(a, b uint64) (uint64, uint64) {
	if a < b {
		return a, b
	}
	return b, a
}

func (grc *GuildRelationCache) AddRelation(guildUUID1, guildUUID2 uint64, relationType uint32, endTime uint32) {
	small, large := sortGuildIDs(guildUUID1, guildUUID2)
	if small == large {
		return // a guild isn't in a relation with itself
	}
	key := guildRelationKey(small, large)
	info := &gameServerService.GuildRelationInfo{
		GuildUUID1:   small,
		GuildUUID2:   large,
		RelationType: relationType,
		EndTime:      endTime,
	}
	grc.Lock()
	defer grc.Unlock()
	grc.version++
	grc.relations[key] = info
	// Mirror into the per-guild inverse index. The pointer is
	// shared (not a copy) so any future field update on `info`
	// reflects in both views — but RelationType / EndTime are
	// currently treated as immutable per pair.
	if grc.byGuild[small] == nil {
		grc.byGuild[small] = make(map[uint64]*gameServerService.GuildRelationInfo)
	}
	if grc.byGuild[large] == nil {
		grc.byGuild[large] = make(map[uint64]*gameServerService.GuildRelationInfo)
	}
	grc.byGuild[small][large] = info
	grc.byGuild[large][small] = info
}

func (grc *GuildRelationCache) RemoveRelation(guildUUID1, guildUUID2 uint64) {
	small, large := sortGuildIDs(guildUUID1, guildUUID2)
	key := guildRelationKey(small, large)
	grc.Lock()
	defer grc.Unlock()
	grc.version++
	delete(grc.relations, key)
	if m, ok := grc.byGuild[small]; ok {
		delete(m, large)
		if len(m) == 0 {
			delete(grc.byGuild, small)
		}
	}
	if m, ok := grc.byGuild[large]; ok {
		delete(m, small)
		if len(m) == 0 {
			delete(grc.byGuild, large)
		}
	}
}

func (grc *GuildRelationCache) getEnemyRelations(guildId uint64) []*gameServerService.GuildRelationInfo {
	grc.RLock()
	defer grc.RUnlock()
	m, ok := grc.byGuild[guildId]
	if !ok {
		return nil
	}
	out := make([]*gameServerService.GuildRelationInfo, 0, len(m))
	for _, rel := range m {
		if rel != nil && rel.RelationType == GuildRelationEnemy {
			out = append(out, rel)
		}
	}
	return out
}

func (grc *GuildRelationCache) getUnionRelations(guildId uint64) []*gameServerService.GuildRelationInfo {
	grc.RLock()
	defer grc.RUnlock()
	m, ok := grc.byGuild[guildId]
	if !ok {
		return nil
	}
	out := make([]*gameServerService.GuildRelationInfo, 0, len(m))
	for _, rel := range m {
		if rel != nil && rel.RelationType == GuildRelationUnion {
			out = append(out, rel)
		}
	}
	return out
}

func (grc *GuildRelationCache) GetRelation(guildUUID1, guildUUID2 uint64) uint32 {
	key := guildRelationKey(guildUUID1, guildUUID2)
	grc.RLock()
	defer grc.RUnlock()
	if rel, exists := grc.relations[key]; exists {
		return rel.RelationType
	}
	return GuildRelationNone
}

// HasEnemies returns true if guildId has at least one active enemy
// relation. Used to gate alliance-join operations — guilds currently
// at war are not allowed to join an alliance.
func (grc *GuildRelationCache) HasEnemies(guildId uint64) bool {
	grc.RLock()
	defer grc.RUnlock()
	m, ok := grc.byGuild[guildId]
	if !ok {
		return false
	}
	for _, rel := range m {
		if rel != nil && rel.RelationType == GuildRelationEnemy {
			return true
		}
	}
	return false
}

func (grc *GuildRelationCache) GetAllRelations() ([]*gameServerService.GuildRelationInfo, uint32) {
	grc.RLock()
	defer grc.RUnlock()
	result := make([]*gameServerService.GuildRelationInfo, 0, len(grc.relations))
	for _, rel := range grc.relations {
		result = append(result, rel)
	}
	return result, grc.version
}

func enemyKey(attackType uint32, attackId uint64, targetType uint32, targetId uint64) string {
	return fmt.Sprintf("%d_%d_%d_%d", attackType, attackId, targetType, targetId)
}

func NewAllianceData(db *sql.DB) *AllianceData {
	ad := &AllianceData{
		db:              db,
		alliances:       concurrent_map.NewWithCustomShardingFunction[uint64, *AllianceCache](uint64Sharding),
		guildToAlliance: concurrent_map.NewWithCustomShardingFunction[uint64, uint64](uint64Sharding),
		guildApplies:    make(map[uint64]*guildApplyRecord),
		invitesByGuild:  make(map[uint64]*guildInviteRecord),
		allianceNames:   make(map[string]uint64),
	}
	ad.loadFromDB(db)
	ad.loadEnemiesFromDB(db)
	ad.loadAppliesAndInvitesFromDB(db)
	ad.initedLock.Lock()
	defer ad.initedLock.Unlock()
	ad.isInited = true
	return ad
}

func (ad *AllianceData) SetBroadcaster(b broadcastFunc) {
	ad.broadcast = b
}

// getMemberGuildIDsLocked — 调用者已持有 cache.Lock 或 cache.RLock
func (ad *AllianceData) getMemberGuildIDsLocked(cache *AllianceCache) []uint64 {
	ids := make([]uint64, 0, len(cache.members))
	for guildId := range cache.members {
		ids = append(ids, guildId)
	}
	return ids
}

// getMemberGuildIDs — 自行获取锁，用于无锁调用者
func (ad *AllianceData) getMemberGuildIDs(allianceId uint64) []uint64 {
	cache, ok := ad.alliances.Get(allianceId)
	if !ok {
		return nil
	}
	cache.RLock()
	defer cache.RUnlock()
	return ad.getMemberGuildIDsLocked(cache)
}

// addWarGuildRelations broadcasts ONE entity-level war relation to all
// game servers when a war is created.
//
// Before the entity-level refactor this expanded the war into N×M
// guild↔guild pairs and broadcast a GuildRelationEnemy pair per pair via
// OnBroadcastAddGuildRelation. That flattening is gone: hostility is
// derived from the entity row (see enemiesCache.byRow) + alliance
// membership, so a single OnBroadcastAddEnemyRelation carrying the war
// row is the complete signal.
func (ad *AllianceData) addWarGuildRelations(app *AllianceApp, AttackType uint32, AttackId uint64, targetType uint32, targetId uint64) {
	var attackerServerId, targetServerId uint32
	enemiesCache.RLock()
	row := enemiesCache.byRow[enemyKey(AttackType, AttackId, targetType, targetId)]
	enemiesCache.RUnlock()
	if row != nil {
		attackerServerId = row.AttackServerId
		targetServerId = row.TargetServerId
	}
	app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
		client.OnBroadcastAddEnemyRelation(&gameServerService.EnemyRelationInfo{
			AttackType:     AttackType,
			AttackId:       AttackId,
			AttackServerId: attackerServerId,
			TargetType:     targetType,
			TargetId:       targetId,
			TargetServerId: targetServerId,
		})
	})
}

func (ad *AllianceData) removeWarGuildRelations(app *AllianceApp, AttackType uint32, AttackId uint64, targetType uint32, targetId uint64) {
	var attackerServerId, targetServerId uint32
	enemiesCache.RLock()
	row := enemiesCache.byRow[enemyKey(AttackType, AttackId, targetType, targetId)]
	enemiesCache.RUnlock()
	if row != nil {
		attackerServerId = row.AttackServerId
		targetServerId = row.TargetServerId
	}
	app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
		client.OnBroadcastRemoveEnemyRelation(&gameServerService.EnemyRelationInfo{
			AttackType:     AttackType,
			AttackId:       AttackId,
			AttackServerId: attackerServerId,
			TargetType:     targetType,
			TargetId:       targetId,
			TargetServerId: targetServerId,
		})
	})
}

// broadcastRemoveEnemyRelation pushes an OnBroadcastRemoveEnemyRelation to every
// game server so it drops the given entity-level war row from its
// enemyRelationDic. Used by the disband paths (DisbandLeague / disbandAlliance)
// where a disbanded alliance's rows are deleted from the Go cache + DB — the
// game servers must also be told, otherwise they retain a stale row. Those rows
// are inert under membership-based derivation (no guild is a member after
// disband and every member's leagueUUID is reset to 0), but cleaning them keeps
// enemyRelationDic consistent with the authoritative Go store.
func (ad *AllianceData) broadcastRemoveEnemyRelation(app *AllianceApp, v *gameServerService.AllianceEnemyInfo) {
	app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
		client.OnBroadcastRemoveEnemyRelation(&gameServerService.EnemyRelationInfo{
			AttackType:     v.AttackType,
			AttackId:       v.AttackId,
			AttackServerId: v.AttackServerId,
			TargetType:     v.TargetType,
			TargetId:       v.TargetId,
			TargetServerId: v.TargetServerId,
			EndTime:        v.EndTime,
		})
	})
}

// removeAllEnemyRelationsForGuild dissolves every entity-level war row in which
// `guildUUID` is a direct party — as a guild entity on the attack side or the
// target side. Called when a guild is dissolved (RemoveGuildInfo): since the
// guild no longer exists, each war it personally declared or that was declared
// against it is cancelled.
//
// Scope note: league-scoped rows where the guild's (former) alliance is a party
// are intentionally left intact. Those rows belong to the alliance and its
// remaining members, not to the dissolved guild — the guild stops inheriting
// them the moment it is removed from the alliance (its leagueUUID is cleared),
// so leaving the rows does not keep the dissolved guild hostile.
func (ad *AllianceData) removeAllEnemyRelationsForGuild(app *AllianceApp, db *sql.DB, guildUUID uint64, keepGuildToGuild bool) {
	// Snapshot the rows under RLock to avoid mutating byRow during iteration;
	// each removal below re-locks briefly.
	enemiesCache.RLock()
	var toRemove []*gameServerService.AllianceEnemyInfo
	for _, row := range enemiesCache.byRow {
		if keepGuildToGuild {
			if row.AttackType == WarAttackTypeGuild && row.TargetType == WarTargetTypeGuild {
				continue
			}
		}
		if (row.AttackType == WarAttackTypeGuild && row.AttackId == guildUUID) ||
			(row.TargetType == WarTargetTypeGuild && row.TargetId == guildUUID) {
			toRemove = append(toRemove, row)
		}
	}
	enemiesCache.RUnlock()

	for _, row := range toRemove {
		db.Exec("DELETE FROM alliance_enemy WHERE attacker_type = ? AND attacker_id = ? AND target_type = ? AND target_id = ?",
			row.AttackType, row.AttackId, row.TargetType, row.TargetId)
		ad.broadcastRemoveEnemyRelation(app, row)
		ad.removeEnemyPairs(row.AttackType, row.TargetType, row.AttackId, row.TargetId)
	}
}

// addAllianceMemberRelations adds UNION relations between a new member and all existing members
func (ad *AllianceData) addAllianceMemberRelations(app *AllianceApp, cache *AllianceCache, newGuildId uint64) {
	memberIds := ad.getMemberGuildIDsLocked(cache)
	guildRelationCache.RLock()
	guildRelationVersion := guildRelationCache.version
	guildRelationCache.RUnlock()
	for _, existingGuildId := range memberIds {
		if existingGuildId != newGuildId {
			guildRelationCache.AddRelation(newGuildId, existingGuildId, GuildRelationUnion, 0)
			// Broadcast to game servers (use sorted IDs)
			small, large := sortGuildIDs(newGuildId, existingGuildId)
			app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
				client.OnBroadcastAddGuildRelation(&gameServerService.GuildRelationInfo{
					GuildUUID1:   small,
					GuildUUID2:   large,
					RelationType: GuildRelationUnion,
					Version:      guildRelationVersion,
				})
			})
		}
	}
}

// removeAllianceMemberRelations removes UNION relations when a member leaves
func (ad *AllianceData) removeAllianceMemberRelations(app *AllianceApp, cache *AllianceCache, guildId uint64) {
	memberIds := ad.getMemberGuildIDsLocked(cache)
	guildRelationCache.RLock()
	guildRelationVersion := guildRelationCache.version
	guildRelationCache.RUnlock()
	for _, otherGuildId := range memberIds {
		if otherGuildId != guildId {
			guildRelationCache.RemoveRelation(guildId, otherGuildId)
			// Broadcast to game servers (use sorted IDs)
			small, large := sortGuildIDs(guildId, otherGuildId)
			app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
				client.OnBroadcastRemoveGuildRelation(&gameServerService.GuildRelationRemoveInfo{
					GuildUUID1: small,
					GuildUUID2: large,
					Version:    guildRelationVersion,
				})
			})
		}
	}
}

func (ad *AllianceData) loadFromDB(db *sql.DB) {
	rows, err := db.Query("SELECT id, alliance_name, declaration, leader_guild_id, approve_type, fund, created_at FROM alliance WHERE alliance_state = 1")
	if err != nil {
		appLog.Error("load alliances error:", err.Error())
		return
	}
	eventLimit := 0
	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		appLog.Error("load alliances error: missing guild const cfg")
		return
	}
	eventCfg := guildCfg.GetStringMapString("guild_unionEventLimit")
	if a, ok := eventCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			appLog.Error("load alliances error:", err.Error())
			return
		}
		if b <= 0 {
			appLog.Error("load alliances error: less than or equal with zero")
			return
		}
		eventLimit = b
	} else {
		appLog.Error("load alliances error: guild const cfg load fail")
		return
	}
	defer rows.Close()

	for rows.Next() {
		var (
			id, leaderGuildId, fund uint64
			name, declaration       string
			approveType, createdAt  uint32
		)
		err = rows.Scan(&id, &name, &declaration, &leaderGuildId, &approveType, &fund, &createdAt)
		if err != nil {
			appLog.Error("scan alliance error:", err.Error())
			continue
		}
		info := &gameServerService.AllianceInfo{
			AllianceId:    id,
			Name:          name,
			Declaration:   declaration,
			LeaderGuildId: leaderGuildId,
			ApproveType:   approveType,
			Fund:          fund,
			CreatedAt:     createdAt,
		}
		cache := &AllianceCache{
			info:    info,
			members: make(map[uint64]*gameServerService.AllianceMemberInfo),
			applies: make(map[uint64]*gameServerService.AllianceApplyInfo),
			invites: make(map[uint64]*gameServerService.AllianceInviteInfo),
			events:  make([]*gameServerService.AllianceEventInfo, 0, eventLimit),
		}
		ad.alliances.Set(id, cache)
		ad.allianceNamesLock.Lock()
		ad.allianceNames[strings.ToLower(name)] = id
		ad.allianceNamesLock.Unlock()

		// Load members (盟主数据已上提 alliance;成员只保留帮会级属性)
		memberRows, err := db.Query("SELECT guild_id, server_id, guild_score, leader_gb_id, leader_name, leader_level, leader_profession, leader_gender, member_count, member_role, join_time, guild_icon, guild_level, guild_name, dsp_flag, max_member_num FROM alliance_member WHERE alliance_id = ?", id)
		if err == nil {
			for memberRows.Next() {
				var guildId uint64
				var serverId, leaderLevel, role, joinTime, guildIcon, guildLevel, memberCount, dspFlag, maxMemberNum, leaderGender uint32
				var guildScore, leaderGbId uint64
				var guildName, leaderName string
				var leaderProfession int32
				err = memberRows.Scan(&guildId, &serverId, &guildScore, &leaderGbId, &leaderName, &leaderLevel, &leaderProfession, &leaderGender, &memberCount, &role, &joinTime, &guildIcon, &guildLevel, &guildName, &dspFlag, &maxMemberNum)
				if err == nil {
					cache.members[guildId] = &gameServerService.AllianceMemberInfo{
						GuildId:          guildId,
						GuildName:        guildName,
						ServerId:         serverId,
						GuildScore:       guildScore,
						MemberCount:      memberCount,
						Role:             role,
						JoinTime:         joinTime,
						GuildIcon:        guildIcon,
						GuildLevel:       guildLevel,
						DspFlag:          dspFlag,
						MaxMemberNum:     maxMemberNum,
						LeaderGbId:       leaderGbId,
						LeaderName:       leaderName,
						LeaderLevel:      leaderLevel,
						LeaderProfession: uint32(leaderProfession),
						LeaderGender:     leaderGender,
					}
					ad.guildToAlliance.Set(guildId, id)
				}
			}
			memberRows.Close()
		}

		for a := range cache.members {
			for b := range cache.members {
				guildRelationCache.AddRelation(a, b, GuildRelationUnion, 0)
			}
		}
		// Load the most recent MaxEventsPerAlliance events for this alliance.
		// The query returns newest-first; we reverse so the cache is stored
		// oldest-first to match the append/trim logic in `addEvent`.
		eventRows, err := db.Query("SELECT id, event_type, params_json, created_at FROM alliance_event WHERE alliance_id = ? ORDER BY created_at DESC, id DESC LIMIT ?", id, eventLimit)
		if err == nil {
			loaded := make([]*gameServerService.AllianceEventInfo, 0, eventLimit)
			for eventRows.Next() {
				var e gameServerService.AllianceEventInfo
				var eventArgs string
				err = eventRows.Scan(&e.EventId, &e.EventType, &eventArgs, &e.CreatedAt)
				e.EventArgs = strings.Split(eventArgs, "|")
				if err == nil {
					loaded = append(loaded, &e)
				}
			}
			eventRows.Close()
			// Reverse to ASC order (oldest → newest)
			for i, j := 0, len(loaded)-1; i < j; i, j = i+1, j-1 {
				loaded[i], loaded[j] = loaded[j], loaded[i]
			}
			cache.events = loaded
		}

		cache.updateDerivedFields()
	}

	// Build the sortedAlliances index once after the map is fully populated.
	ad.rebuildSortedAlliances()

	if ad.alliances.Count() > 0 {
		appLog.Info(fmt.Sprintf("loaded %d alliances from db", ad.alliances.Count()))
	}
}

func (ad *AllianceData) loadEnemiesFromDB(db *sql.DB) {
	rows, err := db.Query("SELECT attacker_type, attacker_id, attacker_server_id, target_type, target_id, target_server_id, end_time FROM alliance_enemy")
	if err != nil {
		appLog.Error("load enemies error:", err.Error())
		return
	}
	defer rows.Close()

	for rows.Next() {
		var AttackType, targetType, attackerServerId, targetServerId uint32
		var AttackId, targetId uint64
		var endTime uint32
		err = rows.Scan(&AttackType, &AttackId, &attackerServerId, &targetType, &targetId, &targetServerId, &endTime)
		if err != nil {
			continue
		}
		ad.addEnemyPairs(AttackType, targetType, AttackId, targetId, endTime, attackerServerId, targetServerId)
	}
}

func (ad *AllianceData) loadAppliesAndInvitesFromDB(db *sql.DB) {
	rows, err := db.Query("SELECT id, alliance_id, guild_id, guild_name, guild_score, server_id, apply_state, created_at, guild_icon, dsp_flag FROM alliance_apply WHERE apply_state = 0")
	if err != nil {
		appLog.Error("load applies error:", err.Error())
		return
	}
	defer rows.Close()

	for rows.Next() {
		var a gameServerService.AllianceApplyInfo
		rows.Scan(&a.ApplyId, &a.AllianceId, &a.GuildId, &a.GuildName, &a.GuildScore, &a.ServerId, &a.Status, &a.CreatedAt, &a.GuildIcon, &a.DspFlag)
		// Take the address of a fresh copy so each cache entry has its own
		// backing storage (not a shared loop variable alias).
		if cache, ok := ad.alliances.Get(a.AllianceId); ok {
			cache.Lock()
			cache.applies[a.GuildId] = &a
			cache.Unlock()
		}
		// Also populate the per-guild O(1) lookup index so restart-restore
		// matches the live ApplyToJoin path.
		ad.addGuildApply(a.GuildId, &a)
	}

	rows2, err := db.Query("SELECT id, alliance_id, alliance_name, guild_id, server_id, invite_state, created_at FROM alliance_invite WHERE invite_state = 0")
	if err != nil {
		appLog.Error("load invites error:", err.Error())
		return
	}
	defer rows2.Close()

	for rows2.Next() {
		var inv gameServerService.AllianceInviteInfo
		rows2.Scan(&inv.InviteId, &inv.AllianceId, &inv.AllianceName, &inv.GuildId, &inv.ServerId, &inv.Status, &inv.CreatedAt)
		if cache, ok := ad.alliances.Get(inv.AllianceId); ok {
			cache.Lock()
			cache.invites[inv.GuildId] = &inv
			// 刷新下联盟数据
			inv.AllianceName = cache.info.Name
			inv.Members = make([]*gameServerService.AllianceInviteMemberInfo, 0)
			for _, member := range cache.members {
				inv.Members = append(inv.Members, &gameServerService.AllianceInviteMemberInfo{
					GuildUUID:    member.GuildId,
					GuildName:    member.GuildName,
					GuildScore:   member.GuildScore,
					GuildIcon:    member.GuildIcon,
					GuildLevel:   member.GuildLevel,
					DspFlag:      member.DspFlag,
					MemberCount:  member.MemberCount,
					MaxMemberNum: member.MaxMemberNum,
				})
			}
			cache.Unlock()
		}
		// Mirror into the per-guild O(1) lookup index so restart-restore
		// matches the live InviteGuild / completeInviteGuild path.
		ad.addGuildInvite(inv.GuildId, &inv)
	}
}

func (c *AllianceCache) updateDerivedFields() {
	c.info.MemberCount = uint32(len(c.members))
	var totalScore uint64
	for _, m := range c.members {
		totalScore += m.GuildScore
	}
	c.info.TotalScore = totalScore
	// Derive leader routing info from the leader member record.
	for _, m := range c.members {
		if m.Role == MemberRoleLeader {
			c.info.LeaderServerId = m.ServerId
			c.info.LeaderGbId = m.LeaderGbId
			c.info.LeaderGuildId = m.GuildId
			c.info.LeaderGuildName = m.GuildName
			c.info.LeaderName = m.LeaderName
			c.info.LeaderLevel = m.LeaderLevel
			c.info.LeaderProfession = int32(m.LeaderProfession)
			c.info.LeaderGender = m.LeaderGender
			break
		}
	}
}

func nowTS() uint32 {
	return uint32(time.Now().Unix())
}

// ==== Core: Create ====

func (ad *AllianceData) CreateLeague(db *sql.DB, app *AllianceApp, in *gameServerService.CreateLeagueRequest) (uint64, uint32, *gameServerService.AllianceInfo, []*gameServerService.AllianceMemberInfo) {
	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return 0, ErrCodeNoGuildConstCfg, nil, nil
	}
	eventLimit := 0
	eventCfg := guildCfg.GetStringMapString("guild_unionEventLimit")
	if a, ok := eventCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return 0, ErrCodeNoGuildConstCfg, nil, nil
		}
		if b <= 0 {
			return 0, ErrCodeNoGuildConstCfg, nil, nil
		}
		eventLimit = b
	} else {
		return 0, ErrCodeNoGuildConstCfg, nil, nil
	}

	minNameLen := 0
	maxNameLen := 0
	maxCreedLen := 0
	minName := guildCfg.GetStringMapString("guild_unionNameMinLength")
	if a, ok := minName["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：1", err)
			return 0, ErrCodeNoGuildConstCfg, nil, nil
		}
		if b <= 0 {
			return 0, ErrCodeNoGuildConstCfg, nil, nil
		}
		minNameLen = b
	} else {
		return 0, ErrCodeNoGuildConstCfg, nil, nil
	}

	maxName := guildCfg.GetStringMapString("guild_unionNameMaxLength")
	if a, ok := maxName["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return 0, ErrCodeNoGuildConstCfg, nil, nil
		}
		if b <= 0 {
			return 0, ErrCodeNoGuildConstCfg, nil, nil
		}
		maxNameLen = b
	} else {
		return 0, ErrCodeNoGuildConstCfg, nil, nil
	}

	maxCreed := guildCfg.GetStringMapString("guild_unionCreedMaxLength")
	if a, ok := maxCreed["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：3", err)
			return 0, ErrCodeNoGuildConstCfg, nil, nil
		}
		if b <= 0 {
			return 0, ErrCodeNoGuildConstCfg, nil, nil
		}
		maxCreedLen = b
	} else {
		return 0, ErrCodeNoGuildConstCfg, nil, nil
	}

	nameLen := utf8.RuneCountInString(in.Name)
	if nameLen < minNameLen || nameLen > maxNameLen {
		return 0, ErrCodeNameInvalid, nil, nil
	}
	declarationLen := utf8.RuneCountInString(in.Declaration)
	if declarationLen > maxCreedLen {
		return 0, ErrCodeDeclarationInvalid, nil, nil
	}

	messageCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_GUILD_LOG)
	if !ok {
		return 0, ErrCodeNoMessageGuildLogCfg, nil, nil
	}
	messageId := 0
	if v := messageCfg.GetInt("guild_unionCreate"); v > 0 {
		messageId = v
	} else {
		return 0, ErrCodeNoMessageGuildLogCfg, nil, nil
	}

	// Check name uniqueness via cache
	if _, exists := ad.checkAllianceName(in.Name); exists {
		return 0, ErrCodeNameAlreadyExists, nil, nil
	}

	if !ad.guildToAlliance.SetIfAbsent(in.GuildId, in.AllianceId) {
		return 0, ErrCodeAlreadyInAlliance, nil, nil
	}

	allianceId := in.AllianceId

	_, err := db.Exec(
		"INSERT INTO alliance (id, alliance_name, declaration, leader_guild_id, approve_type, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
		allianceId, in.Name, in.Declaration, in.GuildId, in.ApproveType, nowTS(), nowTS(),
	)
	if err != nil {
		appLog.Error("create alliance db error:", err.Error())
		ad.guildToAlliance.Remove(in.GuildId)
		return 0, ErrCodeAllianceNotFound, nil, nil
	}

	// Add leader as first member (盟主数据已上提 alliance,这里只存帮会级属性)
	_, err = db.Exec(
		"INSERT INTO alliance_member (alliance_id, guild_id, server_id, guild_score, leader_gb_id, leader_name, leader_level, leader_profession, leader_gender, member_count, member_role, join_time, guild_icon, guild_level, guild_name, dsp_flag, max_member_num) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
		allianceId, in.GuildId, in.ServerId, in.GuildScore, in.PlayerGbId, in.LeaderName, in.LeaderLevel, in.LeaderProfession, in.LeaderGender, in.MemberCount, MemberRoleLeader, nowTS(), in.GuildIcon, in.GuildLevel, in.GuildName, in.DspFlag, in.MaxMemberNum,
	)
	if err != nil {
		appLog.Error("insert leader member error:", err.Error())
		ad.guildToAlliance.Remove(in.GuildId)
		return 0, ErrCodeAllianceNotFound, nil, nil
	}

	info := &gameServerService.AllianceInfo{
		AllianceId:       allianceId,
		Name:             in.Name,
		Declaration:      in.Declaration,
		LeaderGuildId:    in.GuildId,
		LeaderServerId:   in.ServerId,
		LeaderGbId:       in.PlayerGbId,
		LeaderName:       in.LeaderName,
		LeaderLevel:      in.LeaderLevel,
		LeaderProfession: in.LeaderProfession,
		LeaderGender:     in.LeaderGender,
		ApproveType:      in.ApproveType,
		Fund:             0,
		MemberCount:      1,
		TotalScore:       in.GuildScore,
		CreatedAt:        nowTS(),
	}

	member := &gameServerService.AllianceMemberInfo{
		GuildId:          in.GuildId,
		ServerId:         in.ServerId,
		Role:             MemberRoleLeader,
		JoinTime:         nowTS(),
		GuildScore:       in.GuildScore,
		MemberCount:      in.MemberCount,
		GuildIcon:        in.GuildIcon,
		GuildLevel:       in.GuildLevel,
		GuildName:        in.GuildName,
		DspFlag:          in.DspFlag,
		MaxMemberNum:     in.MaxMemberNum,
		LeaderGbId:       in.PlayerGbId,
		LeaderName:       in.LeaderName,
		LeaderLevel:      in.LeaderLevel,
		LeaderProfession: uint32(in.LeaderProfession),
		LeaderGender:     in.LeaderGender,
	}

	cache := &AllianceCache{
		info:    info,
		members: make(map[uint64]*gameServerService.AllianceMemberInfo),
		applies: make(map[uint64]*gameServerService.AllianceApplyInfo),
		invites: make(map[uint64]*gameServerService.AllianceInviteInfo),
		events:  make([]*gameServerService.AllianceEventInfo, 0, eventLimit),
	}
	cache.members[in.GuildId] = member
	ad.alliances.Set(allianceId, cache)
	cache.updateDerivedFields()
	ad.addAllianceName(in.Name, allianceId)

	// Register the new alliance in the sortedAlliances index. The cache's
	// info (MemberCount/TotalScore/CreatedAt/AllianceId) is already final
	// for the creation event, so a single insert is enough.
	ad.insertSortedAlliance(cache)

	ad.addEvent(db, app, eventLimit, allianceId, messageId, fmt.Sprintf("%s|%s", in.LeaderName, in.Name))

	return allianceId, ErrCodeSuccess, info, []*gameServerService.AllianceMemberInfo{member}
}

func (ad *AllianceData) ReportGuildScore(db *sql.DB, app *AllianceApp, in *gameServerService.ReportGuildScoreRequest) uint32 {
	allianceId, exists := ad.guildToAlliance.Get(in.GuildId)
	if !exists {
		return ErrCodeSuccess
	}

	cache, ok := ad.alliances.Get(allianceId)
	if !ok {
		return ErrCodeSuccess
	}

	cache.Lock()

	updated := false
	member, ok := cache.members[in.GuildId]
	if ok {
		member.GuildScore = in.GuildScore
		cache.updateDerivedFields()
		updated = true
	}
	cache.Unlock()
	if updated {
		// Sort key (TotalScore) changed; rebuild the index position.
		ad.resortAlliance(cache)
		db.Exec("UPDATE alliance_member SET guild_score = ? WHERE alliance_id = ? AND guild_id = ?", in.GuildScore, allianceId, in.GuildId)
	}

	return ErrCodeSuccess
}

func (ad *AllianceData) SyncGuildInfo(db *sql.DB, app *AllianceApp, in *gameServerService.SyncGuildInfoRequest) uint32 {
	allianceId, exists := ad.guildToAlliance.Get(in.GuildId)
	if !exists {
		return ErrCodeSuccess
	}

	cache, ok := ad.alliances.Get(allianceId)
	if !ok {
		return ErrCodeSuccess
	}

	cache.Lock()
	defer cache.Unlock()
	member, ok := cache.members[in.GuildId]
	if ok {
		member.GuildName = in.GuildName
		member.GuildIcon = in.GuildIcon
		member.DspFlag = in.DspFlag
		member.GuildLevel = in.GuildLevel
		member.MemberCount = in.MemberCount
		member.MaxMemberNum = in.MaxMemberCount
		member.GuildScore = in.GuildScore
		member.LeaderGbId = in.LeaderGbId
		member.LeaderName = in.LeaderName
		member.LeaderLevel = in.LeaderLevel
		member.LeaderProfession = in.LeaderProfession
		member.LeaderGender = in.LeaderGender
		cache.updateDerivedFields()

		// Always write to DB (even if not in memory cache — unlikely path)
		db.Exec(
			`UPDATE alliance_member SET
			guild_name = ?, guild_icon = ?, dsp_flag = ?,
			guild_level = ?, member_count = ?, guild_score = ?,
			leader_gb_id = ?, leader_name = ?, leader_level = ?,
			leader_profession = ?, leader_gender = ?,max_member_num=?
		WHERE alliance_id = ? AND guild_id = ?`,
			in.GuildName, in.GuildIcon, in.DspFlag,
			in.GuildLevel, in.MemberCount, in.GuildScore,
			in.LeaderGbId, in.LeaderName, in.LeaderLevel,
			in.LeaderProfession, in.LeaderGender, in.MaxMemberCount,
			allianceId, in.GuildId,
		)
	}

	return ErrCodeSuccess
}

// ==== Core: Disband ====

func (ad *AllianceData) DisbandLeague(db *sql.DB, app *AllianceApp, in *gameServerService.DisbandLeagueRequest) (uint32, map[uint32][]uint64) {
	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound, nil
	}

	// Group guild IDs by serverId before removing from cache
	cache.Lock()
	if cache.info.LeaderGbId != in.PlayerGbId {
		return ErrCodeNotAllianceLeader, nil
	}

	db.Exec("UPDATE alliance SET alliance_state = 2 WHERE id = ?", in.AllianceId)
	serverGuilds := make(map[uint32][]uint64)
	for guildId, member := range cache.members {
		serverGuilds[member.ServerId] = append(serverGuilds[member.ServerId], guildId)
		ad.guildToAlliance.Remove(guildId)
		// Guild leaves via disband — drop any pending applies for it (rare
		// since disbanding is the leader's call, but the index entry would
		// leak otherwise).
		ad.removeGuildApply(guildId, cache.info.AllianceId)
	}
	cache.Unlock()
	db.Exec("DELETE FROM alliance_member WHERE alliance_id = ?", in.AllianceId)
	db.Exec("DELETE FROM alliance_apply WHERE alliance_id = ?", in.AllianceId)
	db.Exec("DELETE FROM alliance_invite WHERE alliance_id = ?", in.AllianceId)
	db.Exec("DELETE FROM alliance_event WHERE alliance_id = ?", in.AllianceId)
	db.Exec("DELETE FROM alliance_enemy WHERE (attacker_type = 1 AND attacker_id = ?) OR (target_type = 1 AND target_id = ?)", in.AllianceId, in.AllianceId)

	// Clear enemy cache: walk every war row that references this
	// alliance on either side and call removeEnemyPairs to clean up
	// both the per-guild pairs and the byRow management record.
	// We need to snapshot the keys under lock first to avoid mutating
	// the map during iteration when removeEnemyPairs frees the byRow
	// entry.
	enemiesCache.RLock()
	rowKeysToRemove := make([]*gameServerService.AllianceEnemyInfo, 0)
	for _, v := range enemiesCache.byRow {
		if (v.AttackType == 1 && v.AttackId == in.AllianceId) || (v.TargetType == 1 && v.TargetId == in.AllianceId) {
			rowKeysToRemove = append(rowKeysToRemove, v)
		}
	}
	enemiesCache.RUnlock()
	for _, v := range rowKeysToRemove {
		// Tell game servers to drop the row from their enemyRelationDic
		// (matches "解散后取消所有与该联盟有关的敌对关系" at server level),
		// then remove it from the authoritative Go cache.
		ad.broadcastRemoveEnemyRelation(app, v)
		ad.removeEnemyPairs(v.AttackType, v.TargetType, v.AttackId, v.TargetId)
	}
	cache.RLock()
	ad.removeSortedAlliance(cache)

	serverIdWithMemberGuildIds := make(map[uint32][]uint64)
	for _, m := range cache.members {
		memberGuildIds, ok := serverIdWithMemberGuildIds[m.ServerId]
		if !ok {
			memberGuildIds = make([]uint64, 0)
		}
		memberGuildIds = append(memberGuildIds, m.GuildId)
		serverIdWithMemberGuildIds[m.ServerId] = memberGuildIds
	}
	allianceName := cache.info.Name
	cache.RUnlock()
	for serverId, memberGuildIds := range serverIdWithMemberGuildIds {
		if gs := app.getGameServer(serverId); gs != nil {
			if client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient); ok {
				client.OnLeagueDisband(&gameServerService.LeagueDisband{
					MemberGuildIds: memberGuildIds,
				})
			}
		}
	}

	ad.removeAllianceName(allianceName)
	ad.alliances.Remove(in.AllianceId)

	// Sweep the per-guild invite index. The alliance's pending invites
	// (stored under each invitee's guildId) are now dangling — without
	// this cleanup GetInviteList could return invites pointing at a
	// non-existent allianceId after a restart or a quick leader disband.
	ad.removeAllGuildInvitesForAlliance(in.AllianceId)

	return ErrCodeSuccess, serverGuilds
}

// --- Alliance name cache helpers ---

func (ad *AllianceData) addAllianceName(name string, allianceId uint64) {
	ad.allianceNamesLock.Lock()
	ad.allianceNames[strings.ToLower(name)] = allianceId
	ad.allianceNamesLock.Unlock()
}

func (ad *AllianceData) removeAllianceName(name string) {
	ad.allianceNamesLock.Lock()
	delete(ad.allianceNames, strings.ToLower(name))
	ad.allianceNamesLock.Unlock()
}

func (ad *AllianceData) checkAllianceName(name string) (uint64, bool) {
	ad.allianceNamesLock.RLock()
	id, ok := ad.allianceNames[strings.ToLower(name)]
	ad.allianceNamesLock.RUnlock()
	return id, ok
}

// disbandAlliance performs full alliance cleanup (same as DisbandLeague) and
// broadcasts DisbandLeagueNotify to all game servers that hosted the disbanded
// alliance's member guilds. Used when the last member leaves — the caller MUST
// hold cache.RLock() (or stronger) since it reads cache.info.AllianceId.
func (ad *AllianceData) disbandAlliance(db *sql.DB, app *AllianceApp, allianceId uint64, cache *AllianceCache, serverGuilds map[uint32][]uint64) {
	db.Exec("DELETE FROM alliance WHERE id = ?", allianceId)
	db.Exec("DELETE FROM alliance_apply WHERE alliance_id = ?", allianceId)
	db.Exec("DELETE FROM alliance_invite WHERE alliance_id = ?", allianceId)
	db.Exec("DELETE FROM alliance_event WHERE alliance_id = ?", allianceId)
	db.Exec("DELETE FROM alliance_enemy WHERE (attacker_type = 1 AND attacker_id = ?) OR (target_type = 1 AND target_id = ?)", allianceId, allianceId)

	// Clean up enemy cache — snapshot row keys under enemiseCache lock,
	// then remove each pair individually.
	enemiesCache.Lock()
	rowKeysToRemove := make([]*gameServerService.AllianceEnemyInfo, 0)
	for k, v := range enemiesCache.byRow {
		if (v.AttackType == 1 && v.AttackId == allianceId) || (v.TargetType == 1 && v.TargetId == allianceId) {
			rowKeysToRemove = append(rowKeysToRemove, v)
			delete(enemiesCache.byRow, k)
		}
	}
	enemiesCache.Unlock()
	for _, v := range rowKeysToRemove {
		// Tell game servers to drop the row from their enemyRelationDic
		// (matches "解散后取消所有与该联盟有关的敌对关系" at server level),
		// then remove it from the authoritative Go cache.
		ad.broadcastRemoveEnemyRelation(app, v)
		ad.removeEnemyPairs(v.AttackType, v.TargetType, v.AttackId, v.TargetId)
	}
	cache.RLock()
	ad.removeAllianceName(cache.info.Name)
	ad.removeSortedAlliance(cache)
	cache.RUnlock()
	ad.alliances.Remove(allianceId)
	ad.removeAllGuildInvitesForAlliance(allianceId)

	// Broadcast DisbandLeagueNotify to every server that hosted a member
	for serverId, guildIds := range serverGuilds {
		if gs := app.getGameServer(serverId); gs != nil {
			if client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient); ok {
				client.OnDisbandLeagueNotify(&gameServerService.DisbandLeagueNotify{
					AllianceId: allianceId,
					GuildIds:   guildIds,
				})
			}
		}
	}
}

// ==== Core: Modify ====

func (ad *AllianceData) ModifyLeagueInfo(db *sql.DB, app *AllianceApp, in *gameServerService.ModifyLeagueInfoRequest) uint32 {
	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound
	}
	cache.Lock()
	defer cache.Unlock()
	if in.PlayerGbId != cache.info.LeaderGbId {
		return ErrCodeNotAllianceLeader
	}
	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg
	}
	minNameLen := 0
	maxNameLen := 0
	maxCreedLen := 0
	minName := guildCfg.GetStringMapString("guild_unionNameMinLength")
	if a, ok := minName["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：1", err)
			return ErrCodeNoGuildConstCfg
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg
		}
		minNameLen = b
	} else {
		return ErrCodeNoGuildConstCfg
	}

	maxName := guildCfg.GetStringMapString("guild_unionNameMaxLength")
	if a, ok := maxName["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return ErrCodeNoGuildConstCfg
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg
		}
		maxNameLen = b
	} else {
		return ErrCodeNoGuildConstCfg
	}

	maxCreed := guildCfg.GetStringMapString("guild_unionCreedMaxLength")
	if a, ok := maxCreed["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：3", err)
			return ErrCodeNoGuildConstCfg
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg
		}
		maxCreedLen = b
	} else {
		return ErrCodeNoGuildConstCfg
	}

	nameLen := utf8.RuneCountInString(in.Name)
	if nameLen < minNameLen || nameLen > maxNameLen {
		return ErrCodeNameInvalid
	}
	declarationLen := utf8.RuneCountInString(in.Declaration)
	if declarationLen > maxCreedLen {
		return ErrCodeDeclarationInvalid
	}

	// Check name uniqueness if the name is actually changing
	oldName := cache.info.Name
	if !strings.EqualFold(oldName, in.Name) {
		if _, exists := ad.checkAllianceName(in.Name); exists {
			return ErrCodeNameAlreadyExists
		}
	}

	cache.info.Name = in.Name
	cache.info.Declaration = in.Declaration
	cache.info.ApproveType = in.ApproveType

	db.Exec("UPDATE alliance SET alliance_name = ?, declaration = ?, approve_type = ?, updated_at = ? WHERE id = ?",
		cache.info.Name, cache.info.Declaration, cache.info.ApproveType, nowTS(), in.AllianceId)

	// Update name cache if the name changed
	if !strings.EqualFold(oldName, in.Name) {
		ad.removeAllianceName(oldName)
		ad.addAllianceName(in.Name, in.AllianceId)
	}

	return ErrCodeSuccess
}

// ==== List & Search ====

// buildListEntry snapshots an AllianceCache into the wire-shape used by
// GetLeagueList / SearchLeague. It holds the per-cache RLock briefly so
// reading cache.members is race-free; the sort order is already provided
// by the caller (the sortedAlliances index).
func buildListEntry(cache *AllianceCache) *gameServerService.AllianceListEntry {
	members := make([]*gameServerService.AllianceListMemberInfo, 0, len(cache.members))
	for _, m := range cache.members {
		if m == nil {
			continue
		}
		members = append(members, &gameServerService.AllianceListMemberInfo{
			GuildId:   m.GuildId,
			GuildName: m.GuildName,
			GuildIcon: m.GuildIcon,
			DspFlag:   m.DspFlag,
			ServerId:  m.ServerId,
			Score:     m.GuildScore,
		})

	}
	sort.Slice(members, func(i, j int) bool { return members[i].GuildId < members[j].GuildId })
	return &gameServerService.AllianceListEntry{
		AllianceId: cache.info.AllianceId,
		Name:       cache.info.Name,
		ServerId:   cache.info.LeaderServerId,
		Members:    members,
	}
}

func (ad *AllianceData) GetLeagueList(in *gameServerService.GetLeagueListRequest) (uint32, []*gameServerService.AllianceListEntry) {
	pageSize := int(in.PageSize)
	if pageSize <= 0 {
		pageSize = 5
	}
	pageIndex := int(in.PageIndex)
	if pageIndex < 0 {
		pageIndex = 0
	}

	// Resolve the page slice under the sorted lock and release it before
	// touching the per-cache locks. The copy is bounded by pageSize, not
	// the full alliance population, so a list of N alliances no longer
	// pays O(N) per request to project a single page.
	ad.sortedLock.RLock()
	total := len(ad.sortedAlliances)
	start := pageIndex * pageSize
	if start >= total {
		ad.sortedLock.RUnlock()
		return 0, []*gameServerService.AllianceListEntry{}
	}
	end := start + pageSize
	if end > total {
		end = total
	}
	pageCaches := ad.sortedAlliances[start:end]
	ad.sortedLock.RUnlock()
	// Build entries only for the requested page. buildListEntry acquires
	// the per-cache RLock; doing it outside the sortedLock keeps the
	// critical section short.
	entries := make([]*gameServerService.AllianceListEntry, 0, len(pageCaches))
	for _, cache := range pageCaches {
		cache.RLock()
		entries = append(entries, buildListEntry(cache))
		cache.RUnlock()
	}

	totalPage := 0
	if total > 0 && pageSize > 0 {
		totalPage = (total + pageSize - 1) / pageSize
	}
	return uint32(totalPage), entries
}

func (ad *AllianceData) SearchLeague(in *gameServerService.SearchLeagueRequest) []*gameServerService.AllianceListEntry {
	// Iterate the pre-sorted index; matches preserve the canonical order so
	// the client sees results ranked exactly the way GetLeagueList ranks them.
	ad.sortedLock.RLock()
	defer ad.sortedLock.RUnlock()

	entries := make([]*gameServerService.AllianceListEntry, 0)
	for _, cache := range ad.sortedAlliances {
		cache.RLock()
		if contains(cache.info.Name, in.Keyword) {
			entries = append(entries, buildListEntry(cache))
		}
		cache.RUnlock()
	}
	return entries
}

func (ad *AllianceData) GetLeagueDetail(in *gameServerService.GetLeagueDetailRequest) (*gameServerService.AllianceInfo, []*gameServerService.AllianceMemberInfo, uint32) {
	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return nil, nil, ErrCodeAllianceNotFound
	}

	cache.RLock()
	defer cache.RUnlock()
	members := make([]*gameServerService.AllianceMemberInfo, 0, len(cache.members))
	for _, m := range cache.members {
		members = append(members, ad.copyAllianceMember(m))
	}
	info := ad.copyAllianceData(cache.info)
	sort.Slice(members, func(i, j int) bool {
		return members[i].GuildId < members[j].GuildId
	})
	return info, members, ErrCodeSuccess
}

func (ad *AllianceData) copyAllianceMember(in *gameServerService.AllianceMemberInfo) *gameServerService.AllianceMemberInfo {
	allianceMember := &gameServerService.AllianceMemberInfo{
		GuildId:          in.GuildId,
		GuildName:        in.GuildName,
		ServerId:         in.ServerId,
		GuildScore:       in.GuildScore,
		MemberCount:      in.MemberCount,
		Role:             in.Role,
		JoinTime:         in.JoinTime,
		GuildIcon:        in.GuildIcon,
		GuildLevel:       in.GuildLevel,
		DspFlag:          in.DspFlag,
		MaxMemberNum:     in.MaxMemberNum,
		LeaderGbId:       in.LeaderGbId,
		LeaderName:       in.LeaderName,
		LeaderLevel:      in.LeaderLevel,
		LeaderProfession: in.LeaderProfession,
		LeaderGender:     in.LeaderGender,
	}
	return allianceMember
}

func (ad *AllianceData) copyAllianceData(in *gameServerService.AllianceInfo) *gameServerService.AllianceInfo {
	allianceInfo := &gameServerService.AllianceInfo{
		AllianceId:      in.AllianceId,
		Name:            in.Name,
		Declaration:     in.Declaration,
		LeaderGuildId:   in.LeaderGuildId,
		LeaderServerId:  in.LeaderServerId,
		LeaderGuildName: in.LeaderGuildName,
		ApproveType:     in.ApproveType,
		Fund:            in.Fund,
		MemberCount:     in.MemberCount,
		TotalScore:      in.TotalScore,
		// 2026-08-26: AllianceInfo 去掉 ServerId 字段(冗余),已通过 LeaderServerId 传递
		CreatedAt:        in.CreatedAt,
		LeaderGbId:       in.LeaderGbId,
		LeaderName:       in.LeaderName,
		LeaderLevel:      in.LeaderLevel,
		LeaderProfession: in.LeaderProfession,
		LeaderGender:     in.LeaderGender,
	}
	return allianceInfo
}

// GetAllianceBasicInfo returns a focused 9-field projection of an alliance
// (declaration + approval mode + leader identity) keyed by allianceId.
// It hits the in-memory alliance cache only — no SQL. ErrCode is
// ErrCodeAllianceNotFound if the id is unknown.
func (ad *AllianceData) GetAllianceBasicInfo(in *gameServerService.GetLeagueBasicInfoRequest) (*gameServerService.AllianceBasicInfo, uint32) {
	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return nil, ErrCodeAllianceNotFound
	}
	cache.RLock()
	defer cache.RUnlock()
	if cache.info == nil {
		return nil, ErrCodeAllianceNotFound
	}
	out := &gameServerService.AllianceBasicInfo{
		AllianceId:     cache.info.AllianceId,
		Declaration:    cache.info.Declaration,
		ApproveType:    cache.info.ApproveType,
		LeaderServerId: cache.info.LeaderServerId,
		LeaderGbId:     cache.info.LeaderGbId,
	}
	// Leader personal info is maintained by alliance_member;
	// populate from the leader guild's member record.
	if leaderMember, ok := cache.members[cache.info.LeaderGuildId]; ok {
		out.LeaderName = leaderMember.LeaderName
		out.LeaderGender = leaderMember.LeaderGender
		out.LeaderLevel = leaderMember.LeaderLevel
		out.LeaderProfession = int32(leaderMember.LeaderProfession)
	}
	return out, ErrCodeSuccess
}

// GetAllianceSimpleInfo returns a LeagueSimpleInfo view of an alliance
// (name + totalScore + member roster with guildId/guildName/guildIcon/dspFlag).
// It hits the in-memory alliance cache only — no SQL.
func (ad *AllianceData) GetAllianceSimpleInfo(in *gameServerService.GetLeagueSimpleInfoRequest) (*gameServerService.LeagueSimpleInfo, uint32) {
	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return nil, ErrCodeAllianceNotFound
	}
	cache.RLock()
	defer cache.RUnlock()
	out := &gameServerService.LeagueSimpleInfo{
		AllianceId: cache.info.AllianceId,
		Name:       cache.info.Name,
		TotalScore: cache.info.TotalScore,
	}
	for _, m := range cache.members {
		out.Members = append(out.Members, &gameServerService.LeagueSimpleMember{
			GuildId:   m.GuildId,
			GuildName: m.GuildName,
			GuildIcon: m.GuildIcon,
			DspFlag:   m.DspFlag,
		})
	}
	return out, ErrCodeSuccess
}

// ==== Member: Apply ====

// buildMemberInfoFromApply projects an ApplyToJoinRequest into a fully
// populated AllianceMemberInfo (joining joinTime + defaulting memberRole).
// Extracted so unit tests can verify the field-mapping without a live DB.
func buildMemberInfoFromApply(in *gameServerService.ApplyToJoinRequest, joinTS uint32) *gameServerService.AllianceMemberInfo {
	return &gameServerService.AllianceMemberInfo{
		GuildId:          in.GuildId,
		GuildName:        in.GuildName,
		ServerId:         in.ServerId,
		GuildScore:       in.GuildScore,
		MemberCount:      in.MemberCount,
		Role:             MemberRoleMember,
		JoinTime:         joinTS,
		GuildIcon:        in.GuildIcon,
		GuildLevel:       in.GuildLevel,
		DspFlag:          in.DspFlag,
		MaxMemberNum:     in.MaxMemberNum,
		LeaderGbId:       in.LeaderGbId,
		LeaderName:       in.LeaderName,
		LeaderLevel:      in.LeaderLevel,
		LeaderProfession: in.LeaderProfession,
		LeaderGender:     in.LeaderGender,
	}
}

// buildMemberInfoFromApplySnapshot projects a snapshotted AllianceApplyInfo
// (the kind stored in cache.applies / pendingApproveJoin.applyInfo) into a
// fully populated AllianceMemberInfo for completeApproveJoin's INSERT.
// The snapshot already carries guildName / guildIcon / dspFlag /
// memberCount / guildLevel / maxMemberNum — see buildApplyInfo.
//
// If the snapshot is missing any of the newer fields (legacy data, or a
// caller that predates the field addition), the missing fields land as
// their zero value rather than blocking the join.
func buildMemberInfoFromApplySnapshot(applyInfo *gameServerService.AllianceApplyInfo, joinTS uint32) *gameServerService.AllianceMemberInfo {
	return &gameServerService.AllianceMemberInfo{
		GuildId:          applyInfo.GuildId,
		GuildName:        applyInfo.GuildName,
		ServerId:         applyInfo.ServerId,
		GuildScore:       applyInfo.GuildScore,
		MemberCount:      applyInfo.MemberCount,
		Role:             MemberRoleMember,
		JoinTime:         joinTS,
		GuildIcon:        applyInfo.GuildIcon,
		GuildLevel:       applyInfo.GuildLevel,
		DspFlag:          applyInfo.DspFlag,
		MaxMemberNum:     applyInfo.MaxMemberNum,
		LeaderGbId:       applyInfo.LeaderGbId,
		LeaderName:       applyInfo.LeaderName,
		LeaderLevel:      applyInfo.LeaderLevel,
		LeaderProfession: applyInfo.LeaderProfession,
		LeaderGender:     applyInfo.LeaderGender,
	}
}

// ApplyToJoin processes a guild's apply-to-join request. Both the auto-approve
// and manual-approval paths return the alliance card data (id / name / power)
// so the caller can surface "joined <X> with power Y" to the client without a
// follow-up RPC.
//
// Returns:
//   - errCode          : error code; ErrCodeSuccess on either auto-approve or
//     pending-manual paths.
//   - applyInfo        : set only on the manual-approval path (nil on
//     auto-approve, since the applyInfo IS the new
//     membership in that case).
//   - allianceId       : the alliance id the guild is joining (0 on error paths
//     before the alliance cache is located).
//   - allianceName     : alliance name (empty on error paths).
//   - alliancePower    : alliance totalScore / 战力 (0 on error paths).
func (ad *AllianceData) ApplyToJoin(db *sql.DB, app *AllianceApp, in *gameServerService.ApplyToJoinRequest) (uint32, *gameServerService.AllianceApplyInfo, uint64, string, uint64) {
	messageCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_GUILD_LOG)
	if !ok {
		return ErrCodeNoMessageGuildLogCfg, nil, 0, "", 0
	}
	messageId := 0
	if v := messageCfg.GetInt("guild_unionJoin"); v > 0 {
		messageId = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, nil, 0, "", 0
	}

	if _, exists := ad.guildToAlliance.Get(in.GuildId); exists {
		return ErrCodeAlreadyInAlliance, nil, 0, "", 0
	}

	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound, nil, 0, "", 0
	}
	cache.Lock()
	defer cache.Unlock()
	// Snapshot the alliance card data before any path that might lock/mutate
	// the cache, so we always return a consistent view to the caller.
	allianceId, allianceName, alliancePower := cache.info.AllianceId, cache.info.Name, cache.info.TotalScore

	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg, nil, 0, "", 0
	}
	eventLimit := 0
	eventCfg := guildCfg.GetStringMapString("guild_unionEventLimit")
	if a, ok := eventCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return ErrCodeNoGuildConstCfg, nil, 0, "", 0
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, nil, 0, "", 0
		}
		eventLimit = b
	} else {
		return ErrCodeNoGuildConstCfg, nil, 0, "", 0
	}
	unionNum := 0
	unionApplicationNum := 0
	unionNumCfg := guildCfg.GetStringMapString("guild_unionNum")
	if a, ok := unionNumCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：1", err)
			return ErrCodeNoGuildConstCfg, nil, 0, "", 0
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, nil, 0, "", 0
		}
		unionNum = b
	} else {
		return ErrCodeNoGuildConstCfg, nil, 0, "", 0
	}

	unionApplicationNumCfg := guildCfg.GetStringMapString("guild_unionApplicationNum")
	if a, ok := unionApplicationNumCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：1", err)
			return ErrCodeNoGuildConstCfg, nil, 0, "", 0
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, nil, 0, "", 0
		}
		unionApplicationNum = b
	} else {
		return ErrCodeNoGuildConstCfg, nil, 0, "", 0
	}

	if _, ok := cache.applies[in.GuildId]; ok {
		return ErrCodeAlreadyApplied, nil, allianceId, allianceName, alliancePower
	}
	memberCount := len(cache.members)
	if memberCount >= unionNum {
		return ErrCodeAllianceFull, nil, allianceId, allianceName, alliancePower
	}
	applyCount := len(cache.applies)
	if applyCount >= unionApplicationNum {
		return ErrCodeApplyListFull, nil, allianceId, allianceName, alliancePower
	}
	// 宣战中的帮会不可以加入联盟
	if ad.hasEntityEnemies(in.GuildId, cache) {
		return ErrCodeGuildInWar, nil, allianceId, allianceName, alliancePower
	}

	// 自动同意
	if cache.info.ApproveType == 0 {
		// Auto approve — persist a full member snapshot sourced from the
		// apply request (AllianceMemberInfo minus joinTime, which we stamp here).
		joinTS := nowTS()
		_, err := db.Exec(
			"INSERT INTO alliance_member (alliance_id, guild_id, server_id, guild_score, leader_gb_id, leader_name, leader_level, leader_profession, leader_gender, member_count, member_role, join_time, guild_icon, guild_level, guild_name, dsp_flag, max_member_num) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
			in.AllianceId, in.GuildId, in.ServerId, in.GuildScore,
			in.LeaderGbId, in.LeaderName, in.LeaderLevel, in.LeaderProfession, in.LeaderGender,
			in.MemberCount, MemberRoleMember, joinTS,
			in.GuildIcon, in.GuildLevel, in.GuildName,
			in.DspFlag, in.MaxMemberNum,
		)
		if err != nil {
			appLog.Error("auto approve insert member error:", err.Error())
			return ErrCodeAllianceNotFound, nil, allianceId, allianceName, alliancePower
		}

		memberInfo := buildMemberInfoFromApply(in, joinTS)
		cache.members[in.GuildId] = memberInfo
		cache.updateDerivedFields()
		ad.guildToAlliance.Set(in.GuildId, in.AllianceId)

		// === "one guild in one alliance" rule ===
		// Auto-approve just put this guild into the alliance; cancel every
		// OTHER pending apply the guild has open so they don't sit stale.
		// O(K) via the per-guild index where K = #pending applies for this guild.
		ad.cancelOtherGuildApplies(db, in.GuildId, in.AllianceId)
		// Drop this just-resolved apply from the index (it's now a membership,
		// not a pending apply).
		ad.removeGuildApply(in.GuildId, in.AllianceId)

		// Member count and total score just changed; re-seat in the sorted
		// index.
		ad.resortAlliance(cache)

		ad.addEventLocked(db, app, eventLimit, cache, messageId, fmt.Sprintf("%s|%s", in.GuildName, cache.info.Name))
		// 通知盟主，有新帮会加入了
		ad.notifyAllianceLeaderNewMemberJoined(app, cache.info.LeaderServerId, cache.info.LeaderGbId, memberInfo)
		// 通知帮会，加入了新联盟
		ad.notifyAllianceApplyMemberJoined(app, cache.info.AllianceId, memberInfo.GuildId, memberInfo.ServerId)
		// 建立关系
		ad.addAllianceMemberRelations(app, cache, memberInfo.GuildId)

		return ErrCodeSuccess, nil, allianceId, allianceName, alliancePower
	}

	// Manual approval
	result, err := db.Exec(
		"INSERT INTO alliance_apply (alliance_id, guild_id, guild_name, guild_score, server_id, apply_state, created_at, guild_icon, dsp_flag) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
		in.AllianceId, in.GuildId, in.GuildName, in.GuildScore, in.ServerId, ApplyStatusPending, nowTS(),
		in.GuildIcon, in.DspFlag,
	)
	if err != nil {
		appLog.Error("insert apply error:", err.Error())
		return ErrCodeAllianceNotFound, nil, allianceId, allianceName, alliancePower
	}

	applyId, _ := result.LastInsertId()
	applyInfo := buildApplyInfo(in, uint64(applyId), nowTS(), cache.info.LeaderGuildId)
	cache.applies[in.GuildId] = applyInfo
	ad.addGuildApply(in.GuildId, applyInfo)
	return ErrCodeSuccess, applyInfo, allianceId, allianceName, alliancePower
}

// buildApplyInfo projects an ApplyToJoinRequest + DB-stamped fields into a
// fully populated AllianceApplyInfo. Extracted so unit tests can verify
// the field mapping (including the cosmetic guild_icon / dsp_flag snapshot)
// without a live DB.
func buildApplyInfo(in *gameServerService.ApplyToJoinRequest, applyId uint64, createdAt uint32, leaderGuildId uint64) *gameServerService.AllianceApplyInfo {
	return &gameServerService.AllianceApplyInfo{
		ApplyId:       applyId,
		AllianceId:    in.AllianceId,
		GuildId:       in.GuildId,
		GuildName:     in.GuildName,
		GuildScore:    in.GuildScore,
		ServerId:      in.ServerId,
		Status:        ApplyStatusPending,
		CreatedAt:     createdAt,
		LeaderGuildId: leaderGuildId,
		GuildIcon:     in.GuildIcon,
		DspFlag:       in.DspFlag,
		// Guild-level stats — snapshotted here so completeApproveJoin
		// (which runs in a deferred callback, possibly after the source
		// game server loses the request context) can INSERT a full
		// alliance_member row without going back to the caller.
		MemberCount:  in.MemberCount,
		GuildLevel:   in.GuildLevel,
		MaxMemberNum: in.MaxMemberNum,
		// Guild leader personal info — snapped at apply time so
		// completeApproveJoin has the applicant's leader data.
		LeaderGbId:       in.LeaderGbId,
		LeaderName:       in.LeaderName,
		LeaderLevel:      in.LeaderLevel,
		LeaderProfession: in.LeaderProfession,
		LeaderGender:     in.LeaderGender,
	}
}

// buildNewApplyNotify projects the full AllianceApplyInfo (which already
// carries guildIcon / dspFlag from the apply snapshot) into the focused
// 5-field NewApplyNotify broadcast to the alliance leader's server.
// Nil-safe so a missing applyInfo doesn't crash the broadcast.
func buildNewApplyNotify(applyInfo *gameServerService.AllianceApplyInfo) *gameServerService.NewApplyNotify {
	if applyInfo == nil {
		return nil
	}
	return &gameServerService.NewApplyNotify{
		GuildUUID:  applyInfo.GuildId,
		GuildName:  applyInfo.GuildName,
		GuildIcon:  applyInfo.GuildIcon,
		DspFlag:    applyInfo.DspFlag,
		Power:      applyInfo.GuildScore,
		LeaderGbId: applyInfo.LeaderGbId,
		ApplyTime:  uint64(applyInfo.CreatedAt),
	}
}

// ==== Member: Approve ====

// ApproveJoin validates the ApproveJoin request and (when the apply is
// found) defers the actual join to a follow-up guild-existence check on
// the source game server. The deferred result is delivered later by
// OnCheckGuildExistsResult.
//
// Returns:
//   - errCode            : error code for *immediate* failures (pre-checks).
//     Success here means "deferred, wait for callback".
//   - joinedGuildId      : always 0 in the deferred case; populated only on
//     immediate error paths (kept for backwards compat
//     with the caller's signature).
//   - deferred           : true when the result will arrive later via
//     OnCheckGuildExistsResult. Callers should NOT send
//     OnApproveJoinResult themselves when this is true.
func (ad *AllianceData) ApproveJoin(db *sql.DB, app *AllianceApp, in *gameServerService.ApproveJoinRequest, requesterServerId uint32) (uint32, uint64, bool) {
	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound, 0, false
	}

	messageCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_GUILD_LOG)
	if !ok {
		return ErrCodeNoMessageGuildLogCfg, 0, false
	}
	messageId := 0
	if v := messageCfg.GetInt("guild_unionJoin"); v > 0 {
		messageId = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, 0, false
	}

	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg, 0, false
	}

	eventLimit := 0
	eventCfg := guildCfg.GetStringMapString("guild_unionEventLimit")
	if a, ok := eventCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return ErrCodeNoGuildConstCfg, 0, false
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, 0, false
		}
		eventLimit = b
	} else {
		return ErrCodeNoGuildConstCfg, 0, false
	}
	unionNum := 0
	unionNumCfg := guildCfg.GetStringMapString("guild_unionNum")
	if a, ok := unionNumCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：1", err)
			return ErrCodeNoGuildConstCfg, 0, false
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, 0, false
		}
		unionNum = b
	} else {
		return ErrCodeNoGuildConstCfg, 0, false
	}

	cache.Lock()
	defer cache.Unlock()

	if len(cache.members) >= unionNum {
		return ErrCodeAllianceFull, 0, false
	}

	applyInfo, ok := cache.applies[in.GuildId]
	if !ok {
		return ErrCodeApplyNotFound, 0, false
	}

	// Snapshot the applyInfo so the pending entry is independent of the
	// live cache state (which can be mutated by other RPCs while we wait
	// for the existence check).
	applySnapshot := *applyInfo

	// === Cross-server guild existence pre-check ===
	// Before approving, verify the applying guild still exists on its
	// source server. If the source server isn't connected, fail fast.
	pendingUuid := newPendingApproveUUID()
	pending := &pendingApproveJoin{
		allianceId:        in.AllianceId,
		guildId:           in.GuildId,
		applyInfo:         &applySnapshot,
		originalUuid:      in.Uuid,
		leaderServerId:    cache.info.LeaderServerId,
		requesterServerId: requesterServerId,
		createdAt:         time.Now(),
		messageId:         uint64(messageId),
		eventLimit:        uint32(eventLimit),
	}

	// Default hook: send via the live RPC channel. Tests inject a stub.
	hook := ad.sendCheckGuildExistsHook
	if hook == nil {
		hook = defaultSendCheckGuildExists
	}
	if !hook(app, applySnapshot.ServerId, applySnapshot.GuildId, pendingUuid, true) {
		return ErrCodeGuildSourceServerOffline, 0, false
	}

	// RPC was dispatched; record the pending state. The OnCheckGuildExistsResult
	// handler will resolve it (success or "guild not found").
	ad.pendingApproveJoins.Store(pendingUuid, pending)
	return ErrCodeSuccess, 0, true
}

// defaultSendCheckGuildExists is the production hook: looks up the source
// game server via the app registry and dispatches CheckGuildExists on its
// GameClient stub. Returns false if the source server is not connected.
func defaultSendCheckGuildExists(app *AllianceApp, srcServerId uint32, guildId, uuid uint64, checkCD bool) bool {
	srcGS := app.getGameServer(srcServerId)
	if srcGS == nil {
		return false
	}
	srcClient, ok := srcGS.GetClientEndPoint().(*gameServerService.GameClientClient)
	if !ok {
		return false
	}
	srcClient.CheckGuildExists(&gameServerService.CheckGuildExistsRequest{
		GuildId: guildId,
		Uuid:    uuid,
		CheckCD: checkCD,
	})
	return true
}

// completeApproveJoin finishes the join after a successful existence check.
// Holds cache.Lock while writing. Returns (errCode, joinedGuildId).
func (ad *AllianceData) completeApproveJoin(db *sql.DB, app *AllianceApp, p *pendingApproveJoin) (uint32, uint64) {
	cache, ok := ad.alliances.Get(p.allianceId)
	if !ok {
		return ErrCodeAllianceNotFound, 0
	}

	cache.Lock()

	// Re-check the apply is still there (it may have been cancelled /
	// rejected by another path while we waited).
	if _, ok := cache.applies[p.guildId]; !ok {
		cache.Unlock()
		return ErrCodeApplyNotFound, 0
	}

	// 宣战中的帮会不可以加入联盟
	if ad.hasEntityEnemies(p.guildId, cache) {
		cache.Unlock()
		return ErrCodeGuildInWar, 0
	}

	// INSERT all 12 alliance_member columns. memberInfo carries every
	// guild-level field snapshotted on the apply (see buildApplyInfo +
	// buildMemberInfoFromApplySnapshot) so the SQL gets the same values
	// the in-memory cache does — no more hardcoded 0s for guildIcon /
	// guildLevel / guildName / dspFlag / maxMemberNum / memberCount.
	joinTS := nowTS()
	memberInfo := buildMemberInfoFromApplySnapshot(p.applyInfo, joinTS)
	if db != nil {
		db.Exec("UPDATE alliance_apply SET apply_state = ? WHERE id = ?", ApplyStatusApproved, p.applyId)
		db.Exec("INSERT INTO alliance_member (alliance_id, guild_id, server_id, guild_score, leader_gb_id, leader_name, leader_level, leader_profession, leader_gender, member_count, member_role, join_time, guild_icon, guild_level, guild_name, dsp_flag, max_member_num) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
			p.allianceId,
			memberInfo.GuildId,
			memberInfo.ServerId,
			memberInfo.GuildScore,
			memberInfo.LeaderGbId,
			memberInfo.LeaderName,
			memberInfo.LeaderLevel,
			memberInfo.LeaderProfession,
			memberInfo.LeaderGender,
			memberInfo.MemberCount,
			memberInfo.Role,
			memberInfo.JoinTime,
			memberInfo.GuildIcon,
			memberInfo.GuildLevel,
			memberInfo.GuildName,
			memberInfo.DspFlag,
			memberInfo.MaxMemberNum,
		)
	}
	cache.members[p.guildId] = memberInfo
	delete(cache.applies, p.guildId)
	cache.updateDerivedFields()
	cache.Unlock()

	ad.guildToAlliance.Set(p.guildId, p.allianceId)

	// === "one guild in one alliance" rule (manual-approval path) ===
	// Same as the auto-approve path: revoke every other pending apply for
	// this guild now that it's been accepted here.
	ad.cancelOtherGuildApplies(db, p.guildId, p.allianceId)
	ad.removeGuildApply(p.guildId, p.allianceId)

	// Sort key changed (member count / total score); re-seat in the index.
	cache.Lock()
	ad.resortAlliance(cache)

	ad.addEventLocked(db, app, int(p.eventLimit), cache, int(p.messageId), fmt.Sprintf("%s|%s", p.applyInfo.GuildName, cache.info.Name))
	// 通知盟主，有新帮会加入了
	ad.notifyAllianceLeaderNewMemberJoined(app, cache.info.LeaderServerId, cache.info.LeaderGbId, memberInfo)
	// 通知帮会，加入了新联盟
	ad.notifyAllianceApplyMemberJoined(app, cache.info.AllianceId, memberInfo.GuildId, memberInfo.ServerId)
	// 建立关系
	ad.addAllianceMemberRelations(app, cache, memberInfo.GuildId)
	cache.Unlock()
	return ErrCodeSuccess, p.guildId
}

// failPendingApproveJoin removes a pending entry by uuid. Used by the
// OnCheckGuildExistsResult handler on the not-found path and by the
// game-server disconnect sweep.
func (ad *AllianceData) failPendingApproveJoin(pendingUuid uint64) *pendingApproveJoin {
	raw, ok := ad.pendingApproveJoins.LoadAndDelete(pendingUuid)
	if !ok {
		return nil
	}
	return raw.(*pendingApproveJoin)
}

// ==== Member: Reject ====

// RejectJoin uses the per-guild O(1) index to locate the apply instead of
// scanning every alliance's applies map. Performance: O(K) where K is the
// number of pending applies this specific guild has (typically 0..3).
func (ad *AllianceData) RejectJoin(db *sql.DB, in *gameServerService.RejectJoinRequest) (uint32, uint64) {
	// Find the (guildId, allianceId) for this applyId via the index.
	// RejectJoin's request doesn't carry guildId (only applyId), so we
	// scan the outer map — but the scan is O(guildsWithPendingApplies)
	// in the worst case, which is small in practice (the index itself
	// only grows when a guild has at least one pending apply).
	var targetGuildId uint64
	var targetAllianceId uint64
	var found bool
	var applyId uint64
	ad.guildAppliesLock.RLock()
	for guildId, rec := range ad.guildApplies {
		rec.RLock()
		for allianceId, a := range rec.items {
			if a.GuildId == in.GuildId {
				targetGuildId = guildId
				targetAllianceId = allianceId
				applyId = a.ApplyId
				found = true
				break
			}
		}
		rec.RUnlock()
		if found {
			break
		}
	}
	ad.guildAppliesLock.RUnlock()
	if !found {
		return ErrCodeApplyNotFound, 0
	}

	db.Exec("UPDATE alliance_apply SET apply_state = ? WHERE id = ?", ApplyStatusRejected, applyId)
	if targetCache, ok := ad.alliances.Get(targetAllianceId); ok {
		targetCache.Lock()
		defer targetCache.Unlock()
		delete(targetCache.applies, targetGuildId)

	}
	ad.removeGuildApply(targetGuildId, targetAllianceId)
	return ErrCodeSuccess, targetGuildId
}

// ==== Member: Cancel Apply ====

// CancelApply uses the per-guild O(1) index: the request already carries
// the guildId, so lookup is a single map read + inner RLock scan.
func (ad *AllianceData) CancelApply(db *sql.DB, in *gameServerService.CancelApplyRequest) (uint32, uint64) {
	ad.guildAppliesLock.RLock()
	rec, ok := ad.guildApplies[in.GuildId]
	ad.guildAppliesLock.RUnlock()
	if !ok {
		return ErrCodeApplyNotFound, 0
	}
	rec.RLock()
	var targetAllianceId uint64
	var found bool
	var applyId uint64
	for allianceId, a := range rec.items {
		if a.GuildId == in.GuildId {
			targetAllianceId = allianceId
			applyId = a.ApplyId
			found = true
			break
		}
	}
	rec.RUnlock()
	if !found {
		return ErrCodeApplyNotFound, 0
	}

	db.Exec("UPDATE alliance_apply SET apply_state = ? WHERE id = ?", ApplyStatusCanceled, applyId)
	if targetCache, ok := ad.alliances.Get(targetAllianceId); ok {
		targetCache.Lock()
		defer targetCache.Unlock()
		delete(targetCache.applies, in.GuildId)

	}
	ad.removeGuildApply(in.GuildId, targetAllianceId)
	return ErrCodeSuccess, targetAllianceId
}

// ==== Member: Invite ====

// InviteGuild validates the invite pre-conditions and dispatches a
// cross-server guild-existence check on the TARGET guild's server
// (TargetServerId). The actual cache.invites write + DB INSERT +
// OnNewInviteNotify broadcast happen later in completeInviteGuild
// once the existence check confirms the target guild still exists.
//
// Returns (errCode, deferred). deferred=true means "the existence
// check is in flight; the final OnInviteGuildResult will arrive from
// OnCheckGuildExistsResult". Callers should NOT send
// OnInviteGuildResult themselves when deferred=true (just like
// ApproveJoin's contract).
//
// Pre-checks run synchronously here so the caller can fail fast on
// obvious errors (already in alliance / alliance full / alliance
// missing / cfg missing) without round-tripping to the target server.
//
// `requesterServerId` is the server that initiated the InviteGuild
// RPC (== inviter's leader server in the normal flow). It's used to
// route the deferred OnInviteGuildResult back to the inviter.
//
// db is the MySQL handle; nil is allowed in unit tests (the deferred
// path skips SQL — see completeInviteGuild).
func (ad *AllianceData) InviteGuild(db *sql.DB, app *AllianceApp, in *gameServerService.InviteGuildRequest, requesterServerId uint32) (uint32, bool) {
	if _, exists := ad.guildToAlliance.Get(in.TargetGuildId); exists {
		return ErrCodeAlreadyInAlliance, false
	}

	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound, false
	}
	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg, false
	}

	unionNum := 0
	unionNumCfg := guildCfg.GetStringMapString("guild_unionNum")
	if a, ok := unionNumCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：1", err)
			return ErrCodeNoGuildConstCfg, false
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, false
		}
		unionNum = b
	} else {
		return ErrCodeNoGuildConstCfg, false
	}

	cache.RLock()
	defer cache.RUnlock()
	if _, ok := cache.invites[in.TargetGuildId]; ok {
		return ErrCodeAlreadyInvited, false
	}
	memberCount := len(cache.members)

	if memberCount >= unionNum {
		return ErrCodeAllianceFull, false
	}

	inviteeSnapshot := &gameServerService.AllianceInviteInfo{
		InviteId:     0, // patched in completeInviteGuild
		AllianceId:   cache.info.AllianceId,
		AllianceName: cache.info.Name,
		ServerId:     cache.info.LeaderServerId, // 2026-08-26: AllianceInfo 去掉 serverId 后,改用 LeaderServerId (语义等价:联盟所在 server = 盟主所在 server)
		CreatedAt:    nowTS(),
		Power:        cache.info.TotalScore,
	}
	inviteeSnapshot.Members = make([]*gameServerService.AllianceInviteMemberInfo, 0)
	for _, member := range cache.members {
		inviteeSnapshot.Members = append(inviteeSnapshot.Members, &gameServerService.AllianceInviteMemberInfo{
			GuildUUID:  member.GuildId,
			GuildName:  member.GuildName,
			GuildScore: member.GuildScore,
			GuildIcon:  member.GuildIcon,
			DspFlag:    member.DspFlag,
		})
	}

	pendingUuid := newPendingApproveUUID()
	pending := &pendingInviteGuild{
		allianceId:            in.AllianceId,
		targetGuildId:         in.TargetGuildId,
		targetServerId:        in.TargetServerId,
		inviterLeaderServerId: cache.info.LeaderServerId,
		originalUuid:          in.Uuid,
		inviteeSnapshot:       inviteeSnapshot,
		createdAt:             time.Now(),
	}

	hook := ad.sendCheckGuildExistsHook
	if hook == nil {
		hook = defaultSendCheckGuildExists
	}
	if !hook(app, in.TargetServerId, in.TargetGuildId, pendingUuid, true) {
		// Source server not connected → fail fast. Caller sends
		// OnInviteGuildResult with this errCode immediately (NOT
		// deferred), so the inviter UI shows the right error
		// without waiting for a callback that'll never arrive.
		return ErrCodeInviteTargetServerOffline, false
	}

	ad.pendingInviteGuilds.Store(pendingUuid, pending)
	// Success here means "deferred; wait for callback".
	return ErrCodeSuccess, true
}

// completeInviteGuild finishes the invite after the target guild's
// server confirms existence. Re-checks the pre-conditions (the world
// may have changed while we waited), runs the INSERT, writes the
// cached invite, and broadcasts OnNewInviteNotify to the target
// guild's server.
//
// Caller (OnCheckGuildExistsResult handler) is responsible for
// sending OnInviteGuildResult back to the inviter — this function
// just runs the data side.
//
// app may be nil in unit tests; in that case we skip the broadcast
// but the cache write + DB INSERT still go through.
func (ad *AllianceData) completeInviteGuild(db *sql.DB, app *AllianceApp, p *pendingInviteGuild) uint32 {
	cache, ok := ad.alliances.Get(p.allianceId)
	if !ok {
		return ErrCodeAllianceNotFound
	}

	// Re-check pre-conditions: between dispatch and now the target
	// guild could have joined another alliance, or the inviter
	// alliance could have filled up.
	if _, exists := ad.guildToAlliance.Get(p.targetGuildId); exists {
		return ErrCodeAlreadyInAlliance
	}

	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg
	}

	unionNum := 0
	unionNumCfg := guildCfg.GetStringMapString("guild_unionNum")
	if a, ok := unionNumCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：1", err)
			return ErrCodeNoGuildConstCfg
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg
		}
		unionNum = b
	} else {
		return ErrCodeNoGuildConstCfg
	}

	cache.Lock()
	defer cache.Unlock()
	if len(cache.members) >= unionNum {
		return ErrCodeAllianceFull
	}
	// 宣战中的帮会不可以加入联盟（邀请方在被邀请帮会进入宣战后仍可发邀请，
	// 但 AcceptInvite 会在接受时拦截；此处提前拦截避免无谓的 DB 写入）。
	if ad.hasEntityEnemies(p.targetGuildId, cache) {
		return ErrCodeGuildInWar
	}

	// INSERT into alliance_invite. db may be nil in unit tests;
	// skip SQL and synthesize a 0 inviteId so the cache + broadcast
	// still work.
	var inviteId uint64
	if db != nil {
		result, err := db.Exec(
			"INSERT INTO alliance_invite (alliance_id, alliance_name, guild_id, server_id, invite_state, created_at) VALUES (?, ?, ?, ?, ?, ?)",
			p.allianceId, cache.info.Name, p.targetGuildId, p.targetServerId, InviteStatusPending, nowTS(),
		)
		if err != nil {
			return ErrCodeAllianceNotFound
		}
		lastId, _ := result.LastInsertId()
		inviteId = uint64(lastId)
	}

	stored := *p.inviteeSnapshot
	stored.InviteId = inviteId
	stored.AllianceId = cache.info.AllianceId
	// Refresh inviter-side fields in case the cache mutated while
	// we waited (member count / total score can shift).
	stored.AllianceName = cache.info.Name
	stored.ServerId = cache.info.LeaderServerId // 2026-08-26: AllianceInfo 去掉 serverId 后改用 LeaderServerId
	stored.Power = cache.info.TotalScore
	stored.GuildId = p.targetGuildId
	stored.Members = make([]*gameServerService.AllianceInviteMemberInfo, 0)
	for _, member := range cache.members {
		stored.Members = append(stored.Members, &gameServerService.AllianceInviteMemberInfo{
			GuildUUID:    member.GuildId,
			GuildName:    member.GuildName,
			GuildScore:   member.GuildScore,
			GuildIcon:    member.GuildIcon,
			GuildLevel:   member.GuildLevel,
			DspFlag:      member.DspFlag,
			MemberCount:  member.MemberCount,
			MaxMemberNum: member.MaxMemberNum,
		})
	}

	cache.invites[p.targetGuildId] = &stored
	// Mirror into the per-guild invite index so GetInviteList (invitee
	// view) can return this invite without scanning every alliance.
	ad.addGuildInvite(p.targetGuildId, &stored)

	// Broadcast OnNewInviteNotify to the target guild's server so
	// the invitee UI updates without a manual refresh. Failure
	// here is non-fatal — the cached invite is the source of truth
	// and AcceptInvite can still resolve it on the next GetInviteList
	// poll from the invitee side.
	if app != nil {
		if gs := app.getGameServer(p.targetServerId); gs != nil {
			if client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient); ok {
				client.OnNewInviteNotify(&stored)
			}
		}
	}

	return ErrCodeSuccess
}

// failPendingInviteGuild removes a pending invite by uuid. Returns
// the removed entry (or nil) so the caller can route the failure
// notification back to the inviter. Same pattern as
// failPendingApproveJoin.
func (ad *AllianceData) failPendingInviteGuild(pendingUuid uint64) *pendingInviteGuild {
	raw, ok := ad.pendingInviteGuilds.LoadAndDelete(pendingUuid)
	if !ok {
		return nil
	}
	return raw.(*pendingInviteGuild)
}

// failPendingDeclareWar removes a pending DeclareWar by uuid. Used
// by the OnCheckGuildExistsResult handler on both the exists and the
// not-found paths. Returns nil if the uuid is unknown (handler logs
// and continues). The return is non-nil even for the not-found case
// so the caller can echo back the originalUuid in the deferred
// OnDeclareWarResult.
func (ad *AllianceData) failPendingDeclareWar(pendingUuid uint64) *pendingDeclareWar {
	raw, ok := ad.pendingDeclareWars.LoadAndDelete(pendingUuid)
	if !ok {
		return nil
	}
	return raw.(*pendingDeclareWar)
}

// completeDeclareWar finishes the war declaration after the target
// guild's server confirms existence. Mirrors the synchronous path in
// DeclareWar: fund deduction (if alliance attacker), DB INSERT,
// addEnemyPairs, OnWarStarted broadcast, addWarGuildRelations
// broadcast. Re-checks the pre-conditions (the world may have
// changed while we waited):
//
//   - Attacker alliance (if applicable) still exists and has enough
//     fund.
//   - Target guild (if it was a lone target) hasn't joined another
//     alliance in the meantime (would violate Rule 3 / 5/6).
//   - Same-alliance rule (Rule 8) still satisfied.
//
// Caller (OnCheckGuildExistsResult handler) is responsible for
// sending OnDeclareWarResult back to the attacker's server — this
// function just runs the data side and returns the (errCode, endTime).
func (ad *AllianceData) completeDeclareWar(db *sql.DB, app *AllianceApp, p *pendingDeclareWar) (uint32, uint32) {
	// Re-check target guild isn't in an alliance now (covers the
	// case where it joined one during the deferred wait).
	if p.targetType == WarTargetTypeGuild {
		if _, ok := ad.guildToAlliance.Get(p.targetId); ok {
			return ErrCodeCannotWarAllianceMember, 0
		}
	}

	// Re-check attacker alliance still exists & has enough fund.
	if p.attackType == WarAttackTypeAlliance {
		cache, ok := ad.alliances.Get(p.attackId)
		if !ok {
			return ErrCodeAllianceNotFound, 0
		}
		cache.Lock()
		if cache.info.Fund < p.warCost {
			cache.Unlock()
			return ErrCodeInsufficientFund, 0
		}
		cache.info.Fund -= p.warCost
		newFund := cache.info.Fund
		cache.Unlock()
		db.Exec("UPDATE alliance SET fund = ? WHERE id = ?", p.attackId, newFund)
	}

	// Re-check same-alliance rule for G→G.
	if p.attackType == WarAttackTypeGuild && p.targetType == WarTargetTypeGuild {
		attackerAllianceId, attackerInAlliance := ad.guildToAlliance.Get(p.attackId)
		_, targetInAlliance := ad.guildToAlliance.Get(p.targetId)
		if attackerInAlliance && targetInAlliance && attackerAllianceId == ad.guildToAllianceMust(p.targetId) {
			return ErrCodeCannotWarSameAlliance, 0
		}
	}

	_, dbErr := db.Exec("INSERT INTO alliance_enemy (attacker_type, attacker_id, attacker_server_id, target_type, target_id, target_server_id, end_time, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
		p.attackType, p.attackId, p.attackerServerId, p.targetType, p.targetId, p.targetServerId, p.endTime, nowTS())
	if dbErr != nil {
		appLog.Error("completeDeclareWar: insert enemy error:", dbErr.Error())
		return ErrCodeAllianceNotFound, 0
	}

	ad.addEnemyPairs(p.attackType, p.targetType, p.attackId, p.targetId, p.endTime, p.attackerServerId, p.targetServerId)

	// Broadcast war started
	broadcast := &gameServerService.WarStartedBroadcast{
		Enemy: &gameServerService.EnemyRowInfo{
			AttackType:     p.attackType,
			AttackId:       p.attackId,
			AttackServerId: p.attackerServerId,
			TargetId:       p.targetId,
			TargetType:     p.targetType,
			TargetServerId: p.targetServerId,
			EndTime:        p.endTime,
		},
	}
	ad.addWarGuildRelations(app, p.attackType, p.attackId, p.targetType, p.targetId)
	app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
		client.OnWarStarted(broadcast)
	})

	if p.attackType == WarAttackTypeAlliance {
		if p.targetType == WarTargetTypeGuild {
			cache, ok := ad.alliances.Get(p.attackId)
			if !ok {
				return ErrCodeAllianceNotFound, 0
			}
			cache.RLock()
			allianceName := cache.info.Name
			allianceId := cache.info.AllianceId
			cache.RUnlock()
			ad.addEvent(db, app, p.eventLimit, allianceId, p.declareWarEventIdAllianceToGuild, fmt.Sprintf("%s|%s", allianceName, p.toGuildName))
			ad.NotifyGuildEvent(app, p.targetServerId, p.targetId, uint32(p.guildEventIdAllianceToGuild), []string{allianceName})
		}
	}

	if p.targetType == WarTargetTypeGuild {
		if p.attackType == WarAttackTypeAlliance {
			cache, ok := ad.alliances.Get(p.attackId)
			if !ok {
				return ErrCodeAllianceNotFound, 0
			}

			cache.RLock()
			attackAllianceName := cache.info.Name
			cache.RUnlock()

			app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
				client.OnLeagueBroadCastMessageNotify(&gameServerService.LeagueBroadCastMessage{
					FromUID:     p.attackId,
					ToUID:       p.targetId,
					MessageId:   uint32(p.declareWarMsgIdAllianceToGuild),
					MessageArgs: []string{attackAllianceName, p.toGuildName},
				})
			})
		} else if p.attackType == WarAttackTypeGuild {
			ad.NotifyGuildEvent(app, p.targetServerId, p.targetId, uint32(p.guildEventIdGuildTargetFromGuildAttack), []string{p.fromGuildName})
			ad.NotifyGuildEvent(app, p.attackServerId, p.attackId, uint32(p.guildEventIdGuildAttackToGuildTarget), []string{p.toGuildName})
			app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
				client.OnLeagueBroadCastMessageNotify(&gameServerService.LeagueBroadCastMessage{
					FromUID:     p.attackId,
					ToUID:       p.targetId,
					MessageId:   uint32(p.declareWarMsgIdGuildToGuild),
					MessageArgs: []string{p.fromGuildName, p.toGuildName},
				})
			})
		}

	}
	return ErrCodeSuccess, p.endTime
}

// guildToAllianceMust returns the allianceId for guildId, or 0 if
// not in any alliance. Convenience helper for the same-alliance
// re-check above; the 0 is fine because the "same alliance" check
// requires both guilds to be in some alliance.
func (ad *AllianceData) guildToAllianceMust(guildId uint64) uint64 {
	id, _ := ad.guildToAlliance.Get(guildId)
	return id
}

// ==== Member: Accept Invite ====

func (ad *AllianceData) AcceptInvite(db *sql.DB, app *AllianceApp, in *gameServerService.AcceptInviteRequest) (uint32, uint64) {
	if _, exists := ad.guildToAlliance.Get(in.GuildId); exists {
		return ErrCodeAlreadyInAlliance, 0
	}

	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg, 0
	}
	eventLimit := 0
	eventCfg := guildCfg.GetStringMapString("guild_unionEventLimit")
	if a, ok := eventCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return ErrCodeNoGuildConstCfg, 0
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, 0
		}
		eventLimit = b
	} else {
		return ErrCodeNoGuildConstCfg, 0
	}
	unionNum := 0
	unionNumCfg := guildCfg.GetStringMapString("guild_unionNum")
	if a, ok := unionNumCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：1", err)
			return ErrCodeNoGuildConstCfg, 0
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, 0
		}
		unionNum = b
	} else {
		return ErrCodeNoGuildConstCfg, 0
	}

	messageCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_GUILD_LOG)
	if !ok {
		return ErrCodeNoMessageGuildLogCfg, 0
	}
	messageId := 0
	if v := messageCfg.GetInt("guild_unionJoin"); v > 0 {
		messageId = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, 0
	}

	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound, 0
	}

	cache.Lock()
	defer cache.Unlock()

	if len(cache.members) >= unionNum {
		return ErrCodeAllianceFull, 0
	}

	invInfo, exists := cache.invites[in.GuildId]
	if !exists {
		return ErrCodeInviteNotFound, 0
	}

	// 宣战中的帮会不可以加入联盟
	if ad.hasEntityEnemies(in.GuildId, cache) {
		return ErrCodeGuildInWar, 0
	}

	memberInfo := &gameServerService.AllianceMemberInfo{
		GuildId:          in.GuildId,
		GuildName:        in.GuildName,
		ServerId:         in.ServerId,
		GuildScore:       in.GuildScore,
		MemberCount:      in.MemberCount,
		Role:             MemberRoleMember,
		JoinTime:         nowTS(),
		GuildIcon:        in.GuildIcon,
		GuildLevel:       in.GuildLevel,
		DspFlag:          in.DspFlag,
		MaxMemberNum:     in.MaxMemberNum,
		LeaderGbId:       in.LeaderGbId,
		LeaderName:       in.LeaderName,
		LeaderLevel:      in.LeaderLevel,
		LeaderProfession: in.LeaderProfession,
		LeaderGender:     in.LeaderGender,
	}
	if db != nil {
		db.Exec("UPDATE alliance_invite SET invite_state = ? WHERE id = ?", InviteStatusAccepted, invInfo.InviteId)
		db.Exec("INSERT INTO alliance_member (alliance_id, guild_id, server_id, guild_score, leader_gb_id, leader_name, leader_level, leader_profession, leader_gender, member_count, member_role, join_time, guild_icon, guild_level, guild_name, dsp_flag, max_member_num) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
			invInfo.AllianceId,
			memberInfo.GuildId,
			memberInfo.ServerId,
			memberInfo.GuildScore,
			memberInfo.LeaderGbId,
			memberInfo.LeaderName,
			memberInfo.LeaderLevel,
			memberInfo.LeaderProfession,
			memberInfo.LeaderGender,
			memberInfo.MemberCount,
			memberInfo.Role,
			memberInfo.JoinTime,
			memberInfo.GuildIcon,
			memberInfo.GuildLevel,
			memberInfo.GuildName,
			memberInfo.DspFlag,
			memberInfo.MaxMemberNum,
		)
	}

	cache.members[in.GuildId] = memberInfo
	delete(cache.invites, in.GuildId)
	ad.removeGuildInvite(in.GuildId, invInfo.AllianceId)
	cache.updateDerivedFields()
	ad.guildToAlliance.Set(in.GuildId, invInfo.AllianceId)

	ad.cancelOtherGuildApplies(db, in.GuildId, in.AllianceId)
	// Drop this just-resolved apply from the index (it's now a membership,
	// not a pending apply).
	ad.removeGuildApply(in.GuildId, in.AllianceId)

	// Member count and total score just changed; re-seat in the sorted
	// index.
	ad.resortAlliance(cache)

	ad.addEventLocked(db, app, eventLimit, cache, messageId, fmt.Sprintf("%s|%s", in.GuildName, cache.info.Name))
	// 通知盟主，有新帮会加入了
	ad.notifyAllianceLeaderNewMemberJoined(app, cache.info.LeaderServerId, cache.info.LeaderGbId, memberInfo)
	// 通知帮会，加入了新联盟
	ad.notifyAllianceApplyMemberJoined(app, cache.info.AllianceId, memberInfo.GuildId, memberInfo.ServerId)
	// 建立关系
	ad.addAllianceMemberRelations(app, cache, memberInfo.GuildId)

	return ErrCodeSuccess, in.AllianceId
}

// ==== Member: Reject Invite ====

func (ad *AllianceData) RejectInvite(db *sql.DB, in *gameServerService.RejectInviteRequest) (uint32, uint64) {
	targetCache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound, 0
	}

	targetCache.Lock()
	defer targetCache.Unlock()

	invInfo, exists := targetCache.invites[in.GuildId]
	if !exists {
		return ErrCodeInviteNotFound, 0
	}

	db.Exec("UPDATE alliance_invite SET invite_state = ? WHERE id = ?", InviteStatusRejected, invInfo.InviteId)
	delete(targetCache.invites, in.GuildId)
	ad.removeGuildInvite(in.GuildId, invInfo.AllianceId)
	return ErrCodeSuccess, in.AllianceId
}

// ==== Member: Kick ====

func (ad *AllianceData) KickMember(db *sql.DB, app *AllianceApp, in *gameServerService.KickMemberRequest) uint32 {
	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg
	}
	eventLimit := 0
	eventCfg := guildCfg.GetStringMapString("guild_unionEventLimit")
	if a, ok := eventCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return ErrCodeNoGuildConstCfg
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg
		}
		eventLimit = b
	} else {
		return ErrCodeNoGuildConstCfg
	}

	messageCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_GUILD_LOG)
	if !ok {
		return ErrCodeNoMessageGuildLogCfg
	}
	messageId := 0
	if v := messageCfg.GetInt("guild_unionExit"); v > 0 {
		messageId = v
	} else {
		return ErrCodeNoMessageGuildLogCfg
	}

	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound
	}

	cache.Lock()

	if cache.info.LeaderGbId != in.PlayerGbId {
		cache.Unlock()
		return ErrCodeNotAllianceLeader
	}

	isLeader := cache.info.LeaderGuildId == in.TargetGuildId
	member, memberExists := cache.members[in.TargetGuildId]

	if isLeader {
		cache.Unlock()
		return ErrCodeNotAllianceLeader
	}
	if !memberExists {
		cache.Unlock()
		return ErrCodeMemberNotFound
	}
	cache.Unlock()

	db.Exec("DELETE FROM alliance_member WHERE alliance_id = ? AND guild_id = ?", in.AllianceId, in.TargetGuildId)

	ad.guildToAlliance.Remove(in.TargetGuildId)
	ad.removeGuildApply(in.TargetGuildId, in.AllianceId)

	// Sort key changed (member count / total score); re-seat in the index.
	cache.Lock()
	// Remove UNION relations between kicked member and all other members
	ad.removeAllianceMemberRelations(app, cache, in.TargetGuildId)
	ad.removeAllEnemyRelationsForGuild(app, db, in.TargetGuildId, true)
	ad.addEventLocked(db, app, eventLimit, cache, messageId, fmt.Sprintf("%s|%s", member.GuildName, cache.info.Name))
	serverIdWithMemberGuildIds := make(map[uint32][]uint64)
	for _, m := range cache.members {
		memberGuildIds, ok := serverIdWithMemberGuildIds[m.ServerId]
		if !ok {
			memberGuildIds = make([]uint64, 0)
		}
		memberGuildIds = append(memberGuildIds, m.GuildId)
		serverIdWithMemberGuildIds[m.ServerId] = memberGuildIds
	}
	cache.Unlock()
	for serverId, memberGuildIds := range serverIdWithMemberGuildIds {
		if gs := app.getGameServer(serverId); gs != nil {
			if client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient); ok {
				client.OnLeagueGuildLeave(&gameServerService.LeagueGuildLeave{
					GuildId:        in.TargetGuildId,
					MemberGuildIds: memberGuildIds,
				})
			}
		}
	}

	// Snapshot the full member list (including the one being removed) so
	// we can broadcast DisbandLeagueNotify if this leaves the alliance empty.
	cache.RLock()
	serverGuilds := make(map[uint32][]uint64)
	for gid, m := range cache.members {
		serverGuilds[m.ServerId] = append(serverGuilds[m.ServerId], gid)
	}
	// The kicked guild is still in cache.members at this point, so
	// it's already included in the snapshot above.

	delete(cache.members, in.TargetGuildId)

	isEmpty := len(cache.members) == 0
	cache.RUnlock()
	if isEmpty {
		ad.disbandAlliance(db, app, in.AllianceId, cache, serverGuilds)
	} else {
		cache.Lock()
		cache.updateDerivedFields()
		ad.resortAlliance(cache)
		cache.Unlock()
	}

	return ErrCodeSuccess
}

// ==== Member: Leave ====

func (ad *AllianceData) LeaveLeague(db *sql.DB, app *AllianceApp, in *gameServerService.LeaveLeagueRequest) uint32 {
	return ad.doLeaveLeague(db, app, in.AllianceId, in.GuildId, in.PlayerGbId)
}

func (ad *AllianceData) doLeaveLeague(db *sql.DB, app *AllianceApp, allianceId uint64, guildId uint64, playerGbId uint64) uint32 {
	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg
	}
	eventLimit := 0
	eventCfg := guildCfg.GetStringMapString("guild_unionEventLimit")
	if a, ok := eventCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return ErrCodeNoGuildConstCfg
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg
		}
		eventLimit = b
	} else {
		return ErrCodeNoGuildConstCfg
	}
	messageCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_GUILD_LOG)
	if !ok {
		return ErrCodeNoMessageGuildLogCfg
	}
	messageId := 0
	if v := messageCfg.GetInt("guild_unionExit"); v > 0 {
		messageId = v
	} else {
		return ErrCodeNoMessageGuildLogCfg
	}

	cache, ok := ad.alliances.Get(allianceId)
	if !ok {
		return ErrCodeAllianceNotFound
	}

	cache.Lock()

	// 盟主退出的时候，如果还有其他帮会，需要转让
	if playerGbId == cache.info.LeaderGbId {
		if len(cache.members) > 1 {
			cache.Unlock()
			return ErrCodeYouAreLeader
		}

	}

	member, memberExists := cache.members[guildId]

	if !memberExists {
		cache.Unlock()
		return ErrCodeMemberNotFound
	}
	cache.Unlock()
	db.Exec("DELETE FROM alliance_member WHERE alliance_id = ? AND guild_id = ?", allianceId, guildId)

	ad.guildToAlliance.Remove(guildId)
	ad.removeGuildApply(guildId, allianceId)

	// Sort key changed (member count / total score); re-seat in the index.
	// Remove UNION relations between leaving member and all other members
	cache.Lock()
	ad.removeAllianceMemberRelations(app, cache, guildId)
	ad.removeAllEnemyRelationsForGuild(app, db, guildId, true)
	ad.addEventLocked(db, app, eventLimit, cache, messageId, fmt.Sprintf("%s|%s", member.GuildName, cache.info.Name))
	serverIdWithMemberGuildIds := make(map[uint32][]uint64)
	for _, m := range cache.members {
		memberGuildIds, ok := serverIdWithMemberGuildIds[m.ServerId]
		if !ok {
			memberGuildIds = make([]uint64, 0)
		}
		memberGuildIds = append(memberGuildIds, m.GuildId)
		serverIdWithMemberGuildIds[m.ServerId] = memberGuildIds
	}
	cache.Unlock()
	for serverId, memberGuildIds := range serverIdWithMemberGuildIds {
		if gs := app.getGameServer(serverId); gs != nil {
			if client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient); ok {
				client.OnLeagueGuildLeave(&gameServerService.LeagueGuildLeave{
					GuildId:        guildId,
					MemberGuildIds: memberGuildIds,
				})
			}
		}
	}
	// Snapshot the full member list (including the one leaving) so we can
	// broadcast DisbandLeagueNotify if this leaves the alliance empty.
	cache.Lock()
	serverGuilds := make(map[uint32][]uint64)
	for gid, m := range cache.members {
		serverGuilds[m.ServerId] = append(serverGuilds[m.ServerId], gid)
	}

	delete(cache.members, guildId)
	isEmpty := len(cache.members) == 0
	cache.Unlock()
	if isEmpty {
		ad.disbandAlliance(db, app, allianceId, cache, serverGuilds)
	} else {
		cache.Lock()
		cache.updateDerivedFields()
		ad.resortAlliance(cache)
		cache.Unlock()
	}
	return ErrCodeSuccess
}

// ==== Member: Transfer Leader ====

func (ad *AllianceData) TransferLeader(db *sql.DB, app *AllianceApp, in *gameServerService.TransferLeaderRequest) (uint32, *gameServerService.AllianceInfo) {
	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound, nil
	}

	cache.Lock()
	defer cache.Unlock()
	if in.PlayerGbId != cache.info.LeaderGbId {
		return ErrCodeNotAllianceLeader, nil
	}
	_, memberExists := cache.members[in.TargetGuildId]
	oldLeaderGuildId := cache.info.LeaderGuildId

	if !memberExists {
		return ErrCodeMemberNotFound, nil
	}

	cache.members[oldLeaderGuildId].Role = MemberRoleMember
	cache.members[in.TargetGuildId].Role = MemberRoleLeader

	cache.updateDerivedFields()

	db.Exec("UPDATE alliance_member SET member_role = ? WHERE alliance_id = ? AND guild_id = ?", MemberRoleMember, in.AllianceId, oldLeaderGuildId)
	db.Exec("UPDATE alliance_member SET member_role = ? WHERE alliance_id = ? AND guild_id = ?", MemberRoleLeader, in.AllianceId, in.TargetGuildId)

	db.Exec("UPDATE alliance SET leader_guild_id = ? WHERE id = ?",
		cache.info.LeaderGuildId, cache.info.AllianceId)

	return ErrCodeSuccess, cache.info
}

// ==== Apply List ====

func (ad *AllianceData) GetApplyList(in *gameServerService.GetApplyListRequest) ([]*gameServerService.AllianceApplyInfo, uint32) {
	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return nil, 0
	}

	cache.RLock()
	defer cache.RUnlock()
	applies := make([]*gameServerService.AllianceApplyInfo, 0, len(cache.applies))
	for _, a := range cache.applies {
		applies = append(applies, a)
	}
	count := uint32(len(applies))

	return applies, count
}

// ==== Invite List ====

// GetInviteList returns the invitee view of pending invites — one
// AllianceInviteInfo per alliance that has invited `in.GuildId` and
// has not yet been resolved (accepted / rejected / cancelled).
//
// Implementation: O(K) where K is the number of pending invites for
// the requesting guild, via the per-guild index `invitesByGuild`. The
// legacy implementation scanned every alliance in the system (O(N))
// to find invites whose GuildId matched; the index is the O(1)-ish
// fast path. Each AllianceInviteInfo returned is the live cached
// pointer (read-only for the caller); the `Members` slice inside is
// the alliance roster snapshot taken at the time the invite was
// created (or refreshed by completeInviteGuild).
//
// Edge cases:
//   - Guild has no pending invites → empty slice, count 0
//   - Index race during a concurrent insert → index is updated under
//     its own lock; we may briefly return a stale (about-to-be-added)
//     or miss a (about-to-be-removed) entry, both of which self-heal
//     on the next poll.
func (ad *AllianceData) GetInviteList(in *gameServerService.GetInviteListRequest) ([]*gameServerService.AllianceInviteInfo, uint32) {
	invites := ad.getGuildInvites(in.GuildId)
	return invites, uint32(len(invites))
}

// ==== Sent Applies ====

// GetSentApplies returns the guild leader's "sent applies" view —
// one row per alliance the guild has a pending apply with. Each row
// carries the 4 alliance-side fields (allianceId / allianceName /
// serverId / totalScore) so the leader's inbox can render without a
// follow-up RPC.
//
// Implementation: O(K) where K is the number of pending applies for
// this specific guild (typically 0..3), via the per-guild index
// `guildApplies`. The legacy implementation scanned every alliance
// (O(N_alliances)) — the index was originally added to make the
// cancel-other-applies path fast, and we reuse it here for the same
// reason.
//
// Concurrency:
//   - per-guild index: short RLock snapshot to enumerate applyIds
//   - per-alliance cache: short RLock to read name/serverId/totalScore
//
// Locks are released before the build phase so we don't hold them
// across the (potentially many) cache reads.
func (ad *AllianceData) GetSentApplies(in *gameServerService.GetSentAppliesRequest) ([]*gameServerService.SentApplyItem, uint32) {
	ad.guildAppliesLock.RLock()
	rec, ok := ad.guildApplies[in.GuildId]
	ad.guildAppliesLock.RUnlock()
	if !ok {
		return []*gameServerService.SentApplyItem{}, 0
	}

	// Phase 1: snapshot every pending apply for this guild under the
	// inner RLock. The map values are pointers; we keep them live so
	// status / createdAt reflect current state, but treat the alliance-
	// side fields (name / serverId / totalScore) as read-once-at-this-
	// moment snapshots.
	rec.RLock()
	defer rec.RUnlock()
	// Phase 2: project each apply + its target alliance into a
	// SentApplyItem. Alliance cache lock is acquired per-row briefly
	// to read the snapshot fields.
	items := make([]*gameServerService.SentApplyItem, 0, len(rec.items))
	for _, apply := range rec.items {
		var (
			allianceName string
			serverId     uint32
			totalScore   uint64
		)
		if targetCache, exists := ad.alliances.Get(apply.AllianceId); exists {
			targetCache.RLock()

			if targetCache.info != nil {
				allianceName = targetCache.info.Name
				serverId = targetCache.info.LeaderServerId
				totalScore = targetCache.info.TotalScore
			}
			targetCache.RUnlock()
		}
		items = append(items, &gameServerService.SentApplyItem{
			ApplyId:      apply.ApplyId,
			AllianceId:   apply.AllianceId,
			AllianceName: allianceName,
			ServerId:     serverId,
			TotalScore:   totalScore,
			CreatedAt:    apply.CreatedAt,
			Status:       apply.Status,
		})
	}
	return items, uint32(len(items))
}

// ==== Diplomacy: Declare War ====

func (ad *AllianceData) DeclareWar(db *sql.DB, app *AllianceApp, in *gameServerService.DeclareWarRequest, requesterServerId uint32) (uint32, uint32, bool) {
	guildCfg, _ := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if guildCfg == nil {
		return ErrCodeNoGuildConstCfg, 0, false
	}
	eventLimit := 0
	eventCfg := guildCfg.GetStringMapString("guild_unionEventLimit")
	if a, ok := eventCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return ErrCodeNoGuildConstCfg, 0, false
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, 0, false
		}
		eventLimit = b
	} else {
		return ErrCodeNoGuildConstCfg, 0, false
	}
	chatCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_CHAT_MESSAGE)
	if !ok {
		return ErrCodeNoMessageChatMessageCfg, 0, false
	}
	declareWarMessageIdOne := 0
	if v := chatCfg.GetInt("guild_declareWar1"); v > 0 {
		declareWarMessageIdOne = v
	} else {
		return ErrCodeNoMessageChatMessageCfg, 0, false
	}
	declareWarMessageIdTwo := 0
	if v := chatCfg.GetInt("guild_declareWar2"); v > 0 {
		declareWarMessageIdTwo = v
	} else {
		return ErrCodeNoMessageChatMessageCfg, 0, false
	}
	declareWarMessageIdThree := 0
	if v := chatCfg.GetInt("guild_declareWar3"); v > 0 {
		declareWarMessageIdThree = v
	} else {
		return ErrCodeNoMessageChatMessageCfg, 0, false
	}
	declareWarMessageIdFour := 0
	if v := chatCfg.GetInt("guild_declareWar4"); v > 0 {
		declareWarMessageIdFour = v
	} else {
		return ErrCodeNoMessageChatMessageCfg, 0, false
	}

	messageCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_GUILD_LOG)
	if !ok {
		return ErrCodeNoMessageGuildLogCfg, 0, false
	}
	enmityDeclareOne := 0
	if v := messageCfg.GetInt("guild_enmityDeclare"); v > 0 {
		enmityDeclareOne = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, 0, false
	}
	unionDeclareOne := 0
	if v := messageCfg.GetInt("guild_unionDeclare"); v > 0 {
		unionDeclareOne = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, 0, false
	}
	enmityDeclareTwo := 0
	if v := messageCfg.GetInt("guild_enmityDeclare2"); v > 0 {
		enmityDeclareTwo = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, 0, false
	}
	unionDeclareTwo := 0
	if v := messageCfg.GetInt("guild_unionDeclare2"); v > 0 {
		unionDeclareTwo = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, 0, false
	}

	enmityDescOne := 0
	if v := messageCfg.GetInt("guild_enmityDesc1"); v > 0 {
		enmityDescOne = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, 0, false
	}

	enmityDescTwo := 0
	if v := messageCfg.GetInt("guild_enmityDesc2"); v > 0 {
		enmityDescTwo = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, 0, false
	}

	enmityDescThree := 0
	if v := messageCfg.GetInt("guild_enmityDesc3"); v > 0 {
		enmityDescThree = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, 0, false
	}

	enmityDescFour := 0
	if v := messageCfg.GetInt("guild_enmityDesc4"); v > 0 {
		enmityDescFour = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, 0, false
	}

	key := enemyKey(in.AttackType, in.AttackId, in.TargetType, in.TargetId)

	enemiesCache.RLock()
	_, exists := enemiesCache.byRow[key]
	enemiesCache.RUnlock()
	if exists {
		return ErrCodeWarAlreadyExists, 0, false
	}

	guildCfg, ok = ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg, 0, false
	}

	enemyTime := 0
	enemyTimeCfg := guildCfg.GetStringMapString("guild_enmityTime")
	if a, ok := enemyTimeCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：1", err)
			return ErrCodeNoGuildConstCfg, 0, false
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, 0, false
		}
		enemyTime = b
	} else {
		return ErrCodeNoGuildConstCfg, 0, false
	}

	enemyCost := uint64(0)
	enemyCostCfg := guildCfg.GetStringMapString("guild_enmityUnionCost")
	if a, ok := enemyCostCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return ErrCodeNoGuildConstCfg, 0, false
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, 0, false
		}
		enemyCost = uint64(b)
	} else {
		return ErrCodeNoGuildConstCfg, 0, false
	}

	if in.AttackId == in.TargetId {
		return ErrCodeDeclareWarSameId, 0, false
	}

	// 我是联盟宣战，需要确定我是盟主
	if in.AttackType == WarAttackTypeAlliance {
		// 我是联盟宣战，需要确定我是盟主
		cache, ok := ad.alliances.Get(in.AttackId)
		if !ok {
			return ErrCodeAllianceNotFound, 0, false
		}
		cache.RLock()
		if cache.info.LeaderGbId != in.PlayerGbId {
			cache.RUnlock()
			return ErrCodeNotAllianceLeader, 0, false
		}
		cache.RUnlock()
	}
	// 宣战目标是联盟，判断下联盟是否存在
	if in.TargetType == WarAttackTypeAlliance {
		_, ok := ad.alliances.Get(in.TargetId)
		if !ok {
			return ErrCodeAllianceNotFound, 0, false
		}
	}
	// 我的联盟宣战帮会，排除对方有联盟，排除联盟内宣战
	if in.AttackType == WarAttackTypeAlliance && in.TargetType == WarTargetTypeGuild {
		if targetAllianceId, ok := ad.guildToAlliance.Get(in.TargetId); ok {
			if targetAllianceId == in.AttackId {
				return ErrCodeCannotWarSameAlliance, 0, false
			}
			return ErrCodeCannotWarAllianceMember, 0, false
		}
	}
	// 我的帮会宣战联盟，排除我有联盟，排除联盟内宣战
	if in.AttackType == WarAttackTypeGuild && in.TargetType == WarTargetTypeAlliance {
		if attackerAllianceId, ok := ad.guildToAlliance.Get(in.AttackId); ok {
			if attackerAllianceId == in.TargetId {
				return ErrCodeCannotWarSameAlliance, 0, false
			}
			return ErrCodeGuildCannotWarAlliance, 0, false
		}
	}
	// 我的帮会宣战帮会，排除同个联盟内的帮会宣战
	if in.AttackType == WarAttackTypeGuild && in.TargetType == WarAttackTypeGuild {
		if in.AttackId == in.TargetId {
			return ErrCodeCannotWarSameGuild, 0, false
		}
		attackerAllianceId, ok1 := ad.guildToAlliance.Get(in.AttackId)
		if ok1 {
			targetAllianceId, ok2 := ad.guildToAlliance.Get(in.TargetId)
			if ok2 {
				if attackerAllianceId == targetAllianceId {
					return ErrCodeCannotWarSameAlliance, 0, false
				}
			}
		}
	}
	endTime := nowTS() + uint32(enemyTime)
	// 如果宣战的目标是帮会，需要去源服务器判断帮会是否存在
	if in.TargetType == WarTargetTypeGuild {
		targetAlianceId, ok := ad.guildToAlliance.Get(in.TargetId)
		if !ok {
			pendingUuid := newPendingApproveUUID()
			pending := &pendingDeclareWar{
				attackType:                             in.AttackType,
				attackId:                               in.AttackId,
				attackServerId:                         requesterServerId,
				targetType:                             in.TargetType,
				targetId:                               in.TargetId,
				targetServerId:                         in.TargetServerId,
				attackerServerId:                       requesterServerId, // server that issued the RPC — receives the deferred OnDeclareWarResult
				originalUuid:                           in.Uuid,
				endTime:                                endTime,
				warCost:                                enemyCost,
				createdAt:                              time.Now(),
				declareWarEventIdAllianceToGuild:       enmityDeclareOne,
				declareWarMsgIdAllianceToGuild:         declareWarMessageIdFour,
				declareWarMsgIdGuildToGuild:            declareWarMessageIdOne,
				eventLimit:                             eventLimit,
				fromGuildName:                          in.GuildName,
				amount:                                 in.Amount,
				guildEventIdAllianceToGuild:            enmityDescFour,
				guildEventIdGuildAttackToGuildTarget:   enmityDescOne,
				guildEventIdGuildTargetFromGuildAttack: enmityDescTwo,
			}

			hook := ad.sendCheckGuildExistsHook
			if hook == nil {
				hook = defaultSendCheckGuildExists
			}
			if !hook(app, in.TargetServerId, in.TargetId, pendingUuid, false) {
				// Target's server not connected → fail fast. Caller
				// sends OnDeclareWarResult with this errCode
				// immediately.
				return ErrCodeInviteTargetServerOffline, 0, false
			}

			ad.pendingDeclareWars.Store(pendingUuid, pending)
			return ErrCodeSuccess, endTime, true
		}
		if in.AttackType == WarAttackTypeGuild {
			cache, ok := ad.alliances.Get(targetAlianceId)
			if !ok {
				return ErrCodeAllianceNotFound, 0, false
			}

			cache.RLock()
			toMember, ok := cache.members[in.TargetId]
			if !ok {
				return ErrCodeNotInAlliance, 0, false
			}
			toGuildName := toMember.GuildName
			cache.RUnlock()
			ad.NotifyGuildEvent(app, in.TargetServerId, in.TargetId, uint32(enmityDescTwo), []string{in.GuildName})
			ad.NotifyGuildEvent(app, requesterServerId, in.AttackId, uint32(enmityDescOne), []string{toGuildName})
			app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
				client.OnLeagueBroadCastMessageNotify(&gameServerService.LeagueBroadCastMessage{
					FromUID:     in.AttackId,
					ToUID:       in.TargetId,
					MessageId:   uint32(declareWarMessageIdOne),
					MessageArgs: []string{in.GuildName, toGuildName},
				})
			})
		}
	}

	// Synchronous path: target is in our cache (alliance or member
	// guild), no cross-server check needed. Fund deduction happens
	// here so it only applies when we're actually committing the war
	// — if we'd left it at the top, a deferred completeDeclareWar
	// would have to re-check fund availability anyway.
	if in.AttackType == WarAttackTypeAlliance {
		cache, ok := ad.alliances.Get(in.AttackId)
		if !ok {
			return ErrCodeAllianceNotFound, 0, false
		}
		cache.Lock()
		if cache.info.Fund < enemyCost {
			cache.Unlock()
			return ErrCodeInsufficientFund, 0, false
		}
		cache.info.Fund -= enemyCost
		newFund := cache.info.Fund
		cache.Unlock()
		db.Exec("UPDATE alliance SET fund = ? WHERE id = ?", in.AttackId, newFund)
	}

	_, dbErr := db.Exec("INSERT INTO alliance_enemy (attacker_type, attacker_id, attacker_server_id, target_type, target_id, target_server_id, end_time, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
		in.AttackType, in.AttackId, requesterServerId, in.TargetType, in.TargetId, in.TargetServerId, endTime, nowTS())
	if dbErr != nil {
		appLog.Error("insert enemy error:", dbErr.Error())
		return ErrCodeAllianceNotFound, 0, false
	}

	ad.addEnemyPairs(in.AttackType, in.TargetType, in.AttackId, in.TargetId, endTime, requesterServerId, in.TargetServerId)

	if in.TargetType == WarTargetTypeAlliance {
		if in.AttackType == WarAttackTypeAlliance {
			cache, ok := ad.alliances.Get(in.AttackId)
			if !ok {
				return ErrCodeAllianceNotFound, 0, false
			}
			cache.RLock()
			allianceName := cache.info.Name
			allianceId := cache.info.AllianceId
			cache.RUnlock()
			targetCache, ok := ad.alliances.Get(in.TargetId)
			if !ok {
				return ErrCodeAllianceNotFound, 0, false
			}
			targetCache.RLock()
			targetAllianceName := targetCache.info.Name
			targetAllianceId := targetCache.info.AllianceId
			targetCache.RUnlock()
			ad.addEvent(db, app, eventLimit, allianceId, unionDeclareOne, fmt.Sprintf("%s|%s", allianceName, targetAllianceName))
			ad.addEvent(db, app, eventLimit, targetAllianceId, unionDeclareTwo, fmt.Sprintf("%s|%s", allianceName, targetAllianceName))
		} else if in.AttackType == WarAttackTypeGuild {
			targetCache, ok := ad.alliances.Get(in.TargetId)
			if !ok {
				return ErrCodeAllianceNotFound, 0, false
			}
			targetCache.RLock()
			targetAllianceName := targetCache.info.Name
			targetAllianceId := targetCache.info.AllianceId
			targetCache.RUnlock()
			ad.addEvent(db, app, eventLimit, targetAllianceId, enmityDeclareTwo, fmt.Sprintf("%s|%s", in.GuildName, targetAllianceName))
			ad.NotifyGuildEvent(app, requesterServerId, in.AttackId, uint32(enmityDescThree), []string{targetAllianceName})
		}
	}

	// Broadcast war started
	broadcast := &gameServerService.WarStartedBroadcast{
		Enemy: &gameServerService.EnemyRowInfo{
			AttackType:     in.AttackType,
			AttackId:       in.AttackId,
			AttackServerId: requesterServerId,
			TargetId:       in.TargetId,
			TargetType:     in.TargetType,
			TargetServerId: in.TargetServerId,
			EndTime:        endTime,
		},
	}

	// Add ENEMY relations between involved guilds
	ad.addWarGuildRelations(app, in.AttackType, in.AttackId, in.TargetType, in.TargetId)
	app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
		client.OnWarStarted(broadcast)
	})

	if in.TargetType == WarTargetTypeAlliance {
		if in.AttackType == WarAttackTypeAlliance {
			cache, ok := ad.alliances.Get(in.AttackId)
			if !ok {
				return ErrCodeAllianceNotFound, 0, false
			}

			cache.RLock()
			attackAllianceName := cache.info.Name
			cache.RUnlock()

			targetCache, ok := ad.alliances.Get(in.TargetId)
			if !ok {
				return ErrCodeAllianceNotFound, 0, false
			}
			targetCache.RLock()
			targetAllianceName := targetCache.info.Name
			targetCache.RUnlock()

			app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
				client.OnLeagueBroadCastMessageNotify(&gameServerService.LeagueBroadCastMessage{
					FromUID:     in.AttackId,
					ToUID:       in.TargetId,
					MessageId:   uint32(declareWarMessageIdThree),
					MessageArgs: []string{attackAllianceName, targetAllianceName},
				})
			})
		} else if in.AttackType == WarAttackTypeGuild {
			targetCache, ok := ad.alliances.Get(in.TargetId)
			if !ok {
				return ErrCodeAllianceNotFound, 0, false
			}
			targetCache.RLock()
			targetAllianceName := targetCache.info.Name
			targetCache.RUnlock()
			app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
				client.OnLeagueBroadCastMessageNotify(&gameServerService.LeagueBroadCastMessage{
					FromUID:     in.AttackId,
					ToUID:       in.TargetId,
					MessageId:   uint32(declareWarMessageIdTwo),
					MessageArgs: []string{in.GuildName, targetAllianceName},
				})
			})
		}

	}

	return ErrCodeSuccess, endTime, false
}

// ==== Diplomacy: Enemy List ====

// GetEnemyList returns one EnemyGuildInfo per guild that `in.GuildId` is
// currently at war with, derived from the entity-level war rows in
// enemiesCache.byRow plus current alliance membership. A guild is at war with
// another when either is a direct entity of a war row or a current member of an
// alliance that is a war party (see getEnemyRelationsForGuild). Because the
// answer is derived from live membership on each call, a guild that leaves an
// alliance immediately stops inheriting that alliance's wars while its own
// direct guild-vs-guild wars remain.
//
// Each row's EndTime is the war row's expiry (0 = no expiry). The list is
// sorted by guildId ASC for stable wire output.
func (ad *AllianceData) GetEnemyList(in *gameServerService.GetEnemyListRequest) []*gameServerService.EnemyGuildInfo {
	enemyGuilds := ad.getEnemyRelationsForGuild(in.GuildId)
	if len(enemyGuilds) == 0 {
		return []*gameServerService.EnemyGuildInfo{}
	}
	// Collect endTime per enemy guild; a guild may appear in more than one war
	// row, keep the earliest (most restrictive) expiry.
	endTimes := make(map[uint64]uint32, len(enemyGuilds))
	enemiesCache.RLock()
	for _, row := range enemiesCache.byRow {
		attackerInvolved := ad.entitySideInvolvesGuild(row.AttackType, row.AttackId, in.GuildId, nil)
		targetInvolved := ad.entitySideInvolvesGuild(row.TargetType, row.TargetId, in.GuildId, nil)
		if attackerInvolved {
			for _, eg := range ad.resolveOppositeSideGuilds(row.TargetType, row.TargetId) {
				if eg != 0 && eg != in.GuildId {
					if cur, ok := endTimes[eg]; !ok || (row.EndTime != 0 && (cur == 0 || row.EndTime < cur)) {
						endTimes[eg] = row.EndTime
					}
				}
			}
		}
		if targetInvolved {
			for _, eg := range ad.resolveOppositeSideGuilds(row.AttackType, row.AttackId) {
				if eg != 0 && eg != in.GuildId {
					if cur, ok := endTimes[eg]; !ok || (row.EndTime != 0 && (cur == 0 || row.EndTime < cur)) {
						endTimes[eg] = row.EndTime
					}
				}
			}
		}
	}
	enemiesCache.RUnlock()

	out := make([]*gameServerService.EnemyGuildInfo, 0, len(enemyGuilds))
	for _, eg := range enemyGuilds {
		out = append(out, &gameServerService.EnemyGuildInfo{
			GuildId: eg,
			EndTime: endTimes[eg],
		})
	}
	sort.Slice(out, func(i, j int) bool { return out[i].GuildId < out[j].GuildId })
	return out
}

// GetEnemyAllianceList returns the entity-level war rows that `in.GuildId`
// (and/or `in.AllianceId`) is a party to. Reads enemiesCache.byRow directly —
// the authoritative entity store — matching by the requesting guild entity or
// its alliance entity. Note: a guild that is a member of an alliance is treated
// as participating in that alliance's wars at query time, so this reflects the
// current membership snapshot.
func (ad *AllianceData) GetEnemyAllianceList(in *gameServerService.GetEnemyAllianceListRequest) []*gameServerService.EnemyRowInfo {
	enemiesCache.RLock()
	defer enemiesCache.RUnlock()

	out := make([]*gameServerService.EnemyRowInfo, 0, len(enemiesCache.byRow))
	for _, row := range enemiesCache.byRow {
		var matches bool
		if in.GuildId > 0 {
			if row.AttackType == WarAttackTypeGuild && row.AttackId == in.GuildId {
				matches = true
			} else if row.TargetType == WarTargetTypeGuild && row.TargetId == in.GuildId {
				matches = true
			}
		}
		if !matches {
			if in.AllianceId > 0 {
				if row.AttackType == WarAttackTypeAlliance && row.AttackId == in.AllianceId {
					matches = true
				} else if row.TargetType == WarAttackTypeAlliance && row.TargetId == in.AllianceId {
					matches = true
				}
			}
		}

		if matches {
			out = append(out, &gameServerService.EnemyRowInfo{
				AttackId:       row.AttackId,
				AttackType:     row.AttackType,
				AttackServerId: row.AttackServerId,
				TargetId:       row.TargetId,
				TargetType:     row.TargetType,
				TargetServerId: row.TargetServerId,
				EndTime:        row.EndTime,
			})
		}
	}
	return out
}

func (ad *AllianceData) GetUnionList(in *gameServerService.GetUnionListRequest) []*gameServerService.UnionGuildInfo {
	rels := guildRelationCache.getUnionRelations(in.GuildId)
	if len(rels) == 0 {
		return []*gameServerService.UnionGuildInfo{}
	}
	out := make([]*gameServerService.UnionGuildInfo, 0, len(rels))
	for _, r := range rels {
		other := r.GuildUUID2
		if r.GuildUUID2 == in.GuildId {
			other = r.GuildUUID1
		}
		out = append(out, &gameServerService.UnionGuildInfo{
			GuildId: other,
		})
	}
	sort.Slice(out, func(i, j int) bool { return out[i].GuildId < out[j].GuildId })
	return out
}

// ==== Diplomacy: Check League Relation ====

func (ad *AllianceData) CheckLeagueRelation(in *gameServerService.CheckLeagueRelationRequest) (bool, uint64) {
	a1, ok1 := ad.guildToAlliance.Get(in.GuildId1)
	a2, ok2 := ad.guildToAlliance.Get(in.GuildId2)

	if ok1 && ok2 && a1 == a2 {
		return true, a1
	}
	return false, 0
}

// ==== Diplomacy: Get Guild Alliance ====

func (ad *AllianceData) GetGuildAlliance(in *gameServerService.GetGuildAllianceRequest) (uint64, uint32) {
	if allianceId, ok := ad.guildToAlliance.Get(in.GuildId); ok {
		return allianceId, ErrCodeSuccess
	}
	return 0, 1
}

// ==== Resource: Donate ====

func (ad *AllianceData) DonateFund(db *sql.DB, app *AllianceApp, in *gameServerService.DonateFundRequest) (uint32, uint64, uint64) {
	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound, in.AllianceId, 0
	}

	ratio := 1.0
	leagueFundGain := uint64(math.Floor(float64(in.Amount) * ratio))

	cache.Lock()
	defer cache.Unlock()
	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg, in.AllianceId, 0
	}
	eventLimit := 0
	eventCfg := guildCfg.GetStringMapString("guild_unionEventLimit")
	if a, ok := eventCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return ErrCodeNoGuildConstCfg, in.AllianceId, 0
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg, in.AllianceId, 0
		}
		eventLimit = b
	} else {
		return ErrCodeNoGuildConstCfg, in.AllianceId, 0
	}
	fromMember, fromExists := cache.members[in.GuildId]
	if !fromExists {
		return ErrCodeNotInAlliance, in.AllianceId, 0
	}
	messageCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_GUILD_LOG)
	if !ok {
		return ErrCodeNoMessageGuildLogCfg, in.AllianceId, 0
	}
	messageId1 := 0
	if v := messageCfg.GetInt("guild_unionDonate"); v > 0 {
		messageId1 = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, in.AllianceId, 0
	}
	messageId2 := 0
	if v := messageCfg.GetInt("guild_unionDonate2"); v > 0 {
		messageId2 = v
	} else {
		return ErrCodeNoMessageGuildLogCfg, in.AllianceId, 0
	}

	itemName := ""
	itemCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_ITEM_DATA)
	if !ok {
		return ErrCodeNoMessageGuildLogCfg, in.AllianceId, 0
	}
	v := itemCfg.GetStringMap(strconv.FormatInt(int64(in.ItemId), 10))
	if y, ok := v["name"]; ok {
		s, ok := y.(string)
		if ok {
			itemName = s
		}
	}
	if len(itemName) == 0 {
		return ErrCodeNoMessageGuildLogCfg, in.AllianceId, 0
	}
	cache.info.Fund += leagueFundGain
	fund := cache.info.Fund

	db.Exec("UPDATE alliance SET fund = ? WHERE id = ?", fund, in.AllianceId)
	db.Exec("INSERT INTO alliance_donate_log (alliance_id, guild_id, amount, league_fund_get, created_at) VALUES (?, ?, ?, ?, ?)",
		in.AllianceId, in.GuildId, in.Amount, leagueFundGain, nowTS())
	ad.addEventLocked(db, app, eventLimit, cache, messageId2, fmt.Sprintf("%s|%d|%d", fromMember.GuildName, in.ItemId, in.Amount))
	ad.NotifyGuildEvent(app, fromMember.ServerId, fromMember.GuildId, uint32(messageId1), []string{cache.info.Name, strconv.Itoa(int(in.ItemId)), strconv.Itoa(int(in.Amount))})
	return ErrCodeSuccess, in.AllianceId, fund
}

// ==== Resource: Aid ====

func (ad *AllianceData) AidResource(db *sql.DB, app *AllianceApp, in *gameServerService.AidResourceRequest) uint32 {
	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg
	}

	eventLimit := 0
	aidRequirement := 0
	eventCfg := guildCfg.GetStringMapString("guild_unionEventLimit")
	if a, ok := eventCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return ErrCodeNoGuildConstCfg
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg
		}
		eventLimit = b
	} else {
		return ErrCodeNoGuildConstCfg
	}
	aidRequirementCfg := guildCfg.GetStringMapString("guild_aidRequirement")
	if a, ok := aidRequirementCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：2", err)
			return ErrCodeNoGuildConstCfg
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg
		}
		aidRequirement = b
	} else {
		return ErrCodeNoGuildConstCfg
	}
	messageCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_GUILD_LOG)
	if !ok {
		return ErrCodeNoMessageGuildLogCfg
	}
	messageId1 := 0
	if v := messageCfg.GetInt("guild_unionSupport1"); v > 0 {
		messageId1 = v
	} else {
		return ErrCodeNoMessageGuildLogCfg
	}
	messageId2 := 0
	if v := messageCfg.GetInt("guild_unionSupport2"); v > 0 {
		messageId2 = v
	} else {
		return ErrCodeNoMessageGuildLogCfg
	}
	messageId3 := 0
	if v := messageCfg.GetInt("guild_unionSupport3"); v > 0 {
		messageId3 = v
	} else {
		return ErrCodeNoMessageGuildLogCfg
	}
	chatCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_CHAT_MESSAGE)
	if !ok {
		return ErrCodeNoMessageChatMessageCfg
	}
	chat1 := 0
	if v := chatCfg.GetInt("guild_unionSupport1"); v > 0 {
		chat1 = v
	} else {
		return ErrCodeNoMessageChatMessageCfg
	}

	chat2 := 0
	if v := chatCfg.GetInt("guild_unionSupport2"); v > 0 {
		chat2 = v
	} else {
		return ErrCodeNoMessageChatMessageCfg
	}

	chat3 := 0
	if v := chatCfg.GetInt("guild_unionSupport3"); v > 0 {
		chat3 = v
	} else {
		return ErrCodeNoMessageChatMessageCfg
	}

	itemName := ""
	itemCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_ITEM_DATA)
	if !ok {
		return ErrCodeNoMessageGuildLogCfg
	}
	v := itemCfg.GetStringMap(strconv.FormatInt(int64(in.ItemId), 10))
	if y, ok := v["name"]; ok {
		s, ok := y.(string)
		if ok {
			itemName = s
		}
	}
	if len(itemName) == 0 {
		return ErrCodeNoMessageGuildLogCfg
	}

	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound
	}

	cache.Lock()
	defer cache.Unlock()

	fromMember, fromExists := cache.members[in.FromGuildId]
	toMember, toExists := cache.members[in.ToGuildId]
	if !fromExists || !toExists {
		return ErrCodeNotInAlliance
	}
	nowTime := nowTS()
	gapTime := uint32(aidRequirement) * 86400
	if uint32(fromMember.JoinTime+gapTime) >= nowTime {
		return ErrCodeAidResourceFail
	}
	if uint32(toMember.JoinTime+gapTime) >= nowTime {
		return ErrCodeAidResourceFail
	}
	ad.addEventLocked(db, app, eventLimit, cache, messageId3, fmt.Sprintf("%s|%s|%d|%d", fromMember.GuildName, toMember.GuildName, in.ItemId, in.Amount))

	ad.NotifyGuildEvent(app, fromMember.ServerId, fromMember.GuildId, uint32(messageId1), []string{toMember.GuildName, strconv.Itoa(int(in.ItemId)), strconv.Itoa(0), strconv.Itoa(int(in.Amount))})
	ad.NotifyGuildEvent(app, toMember.ServerId, toMember.GuildId, uint32(messageId2), []string{fromMember.GuildName, strconv.Itoa(int(in.ItemId)), strconv.Itoa(0), strconv.Itoa(int(in.Amount))})
	ad.NotifyGuildMsg(app, fromMember.ServerId, fromMember.GuildId, uint32(chat1), []string{toMember.GuildName, strconv.Itoa(int(in.ItemId)), strconv.Itoa(0), strconv.Itoa(int(in.Amount))})
	ad.NotifyGuildMsg(app, toMember.ServerId, toMember.GuildId, uint32(chat2), []string{fromMember.GuildName, strconv.Itoa(int(in.ItemId)), strconv.Itoa(0), strconv.Itoa(int(in.Amount))})
	gs := app.getGameServer(toMember.ServerId)
	if gs == nil {
		return ErrCodeGameServerMissing
	}
	client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient)
	if !ok || client == nil {
		return ErrCodeGameClientMissing
	}

	client.OnGuildAidResourceNotify(&gameServerService.GuildAidResourceNotify{
		GuildId:  in.ToGuildId,
		SrcType:  AID_COST,
		ItemType: IRON,
		ItemNum:  in.Amount,
	})

	ad.DistributeEventTips(cache, app, uint32(chat3), []string{fromMember.GuildName, toMember.GuildName, strconv.Itoa(int(in.ItemId)), strconv.Itoa(int(fromMember.LeaderGbId)), strconv.Itoa(int(in.Amount))})

	return ErrCodeSuccess
}

func (ad *AllianceData) DistributeEventTips(cache *AllianceCache, app *AllianceApp, messageId uint32, messageArgs []string) {
	serverToGuilds := groupMembersByServer(cache)
	if nil == serverToGuilds || len(serverToGuilds) == 0 {
		// 联盟存在但没有任何成员(理论上不应发生),直接返回成功
		return
	}

	for serverId := range serverToGuilds {
		gs := app.getGameServer(serverId)
		if gs == nil {
			continue
		}
		client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient)
		if !ok || client == nil {
			continue
		}
		client.OnEventTipsNotify(&gameServerService.EventTipsNotify{
			LeagueUUID:  cache.info.AllianceId,
			MessageId:   messageId,
			MessageArgs: messageArgs,
		})
	}
}

// ==== Resource: Get League Fund ====

func (ad *AllianceData) GetLeagueFund(in *gameServerService.GetLeagueFundRequest) uint64 {
	if cache, ok := ad.alliances.Get(in.AllianceId); ok {
		cache.RLock()
		defer cache.RUnlock()
		fund := cache.info.Fund

		return fund
	}
	return 0
}

// ==== Events ====
//
// Per-alliance event log uses a memory cache + MySQL store, both capped at
// MaxEventsPerAlliance. The cache is the source of truth for `GetEventList`
// (avoiding a per-request SQL query), while MySQL keeps the same window so
// the data survives restarts. When the cap is exceeded, the oldest events
// are dropped from both stores.

func (ad *AllianceData) GetEventList(in *gameServerService.GetEventListRequest) []*gameServerService.AllianceEventInfo {
	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return []*gameServerService.AllianceEventInfo{}
	}

	cache.RLock()
	defer cache.RUnlock()
	result := make([]*gameServerService.AllianceEventInfo, 0, len(cache.events))
	for _, event := range cache.events {
		result = append(result, event)
	}

	return result
}

func (ad *AllianceData) addEvent(db *sql.DB, app *AllianceApp, eventLimit int, allianceId uint64, eventType int, paramsJson string) {
	cache, ok := ad.alliances.Get(allianceId)
	if !ok {
		return
	}
	cache.Lock()
	defer cache.Unlock()
	ad.addEventLocked(db, app, eventLimit, cache, eventType, paramsJson)
}

func (ad *AllianceData) addEventLocked(db *sql.DB, app *AllianceApp, eventLimit int, cache *AllianceCache, eventType int, paramsJson string) {
	createdAt := nowTS()
	allianceId := cache.info.AllianceId
	// 1) Persist to MySQL first and capture the auto-incremented id so the
	//    cache row has the same identifier the client will see on reads.
	//    db may be nil in unit tests; in that case we skip the INSERT and
	//    synthesize a 0 id so the in-memory cache + broadcast still work.
	var lastId int64
	if db != nil {
		res, err := db.Exec(
			"INSERT INTO alliance_event (alliance_id, event_type, params_json, created_at) VALUES (?, ?, ?, ?)",
			allianceId, eventType, paramsJson, createdAt,
		)
		if err != nil {
			appLog.Error("addEvent insert error:", err.Error())
			return
		}
		lastId, _ = res.LastInsertId()
	}

	eventInfo := &gameServerService.AllianceEventInfo{
		EventId:   uint64(lastId),
		EventType: uint32(eventType),
		EventArgs: strings.Split(paramsJson, "|"),
		CreatedAt: createdAt,
	}

	// 2) Update the in-memory cache (lock the cache to serialize writers).
	//    The alliance may have been disbanded between the upstream action and
	//    this call, so tolerate a missing cache entry.
	var overflowIds []interface{}
	if cache, ok := ad.alliances.Get(allianceId); ok {
		cache.events = append(cache.events, eventInfo)

		if len(cache.events) > eventLimit {
			overflow := cache.events[:len(cache.events)-eventLimit]
			cache.events = cache.events[len(cache.events)-eventLimit:]
			overflowIds = make([]interface{}, 0, len(overflow))
			for _, ev := range overflow {
				overflowIds = append(overflowIds, ev.EventId)
			}
		}
	}

	// 3) Mirror the trim in MySQL so on-disk storage never exceeds the cap.
	if len(overflowIds) > 0 {
		ad.deleteEventsByID(db, overflowIds)
	}

	// 4) Broadcast the new event only to game servers that currently host at
	//    least one guild belonging to this alliance. Game servers with no
	//    member guilds in this alliance do not need to know about the event.
	ad.broadcastNewEventToAlliance(app, allianceId, eventInfo)
}

// broadcastNewEventToAlliance sends a NewEventBroadcast to every game server
// that has at least one guild member in the given alliance. The broadcast
// scope is the alliance's member guilds only — other alliances' servers and
// any orphan servers are skipped. Each broadcast is enriched with the list
// of guild IDs on the receiving server that belong to the alliance, so the
// game server can fan the event out to exactly those guilds without further
// filtering. Failures on individual servers are swallowed by the underlying
// rpc client; a missing alliance cache entry means there is nothing to
// broadcast.
func (ad *AllianceData) broadcastNewEventToAlliance(app *AllianceApp, allianceId uint64, event *gameServerService.AllianceEventInfo) {
	if app == nil || event == nil {
		return
	}
	cache, ok := ad.alliances.Get(allianceId)
	if !ok {
		return
	}

	serverToGuilds := groupMembersByServer(cache)
	if nil == serverToGuilds || len(serverToGuilds) == 0 {
		return
	}

	for serverId, guildIds := range serverToGuilds {
		gs := app.getGameServer(serverId)
		if gs == nil {
			continue
		}
		client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient)
		if !ok || client == nil {
			continue
		}
		// Build a per-server guild ID slice. The slice is owned by this
		// broadcast call so it's safe to ship as a protobuf repeated field;
		// the rpc client marshals it immediately before returning.
		broadcast := &gameServerService.NewEventBroadcast{
			AllianceId: allianceId,
			Event:      event,
			GuildIds:   guildIds,
		}
		client.OnNewEvent(broadcast)
	}
}

// groupMembersByServer returns a map from game serverId to the list of
// member guild IDs that live on that server. The cache is read under
// RLock; the returned map and slices are caller-owned and safe to
// iterate after Unlock. Nil member entries and zero-guild entries are
// filtered out, so the result is empty when the alliance has no members.
func groupMembersByServer(cache *AllianceCache) map[uint32][]uint64 {
	if cache == nil {
		return nil
	}
	out := make(map[uint32][]uint64)
	for _, m := range cache.members {
		if m == nil {
			continue
		}
		out[m.ServerId] = append(out[m.ServerId], m.GuildId)
	}
	if len(out) == 0 {
		return nil
	}
	return out
}

// deleteEventsByID removes a batch of event rows by primary key. Failures
// are logged but do not propagate — the cache has already been trimmed and
// the next trim pass will keep the on-disk count bounded.
func (ad *AllianceData) deleteEventsByID(db *sql.DB, ids []interface{}) {
	if len(ids) == 0 {
		return
	}
	placeholders := make([]string, len(ids))
	for i := range placeholders {
		placeholders[i] = "?"
	}
	query := "DELETE FROM alliance_event WHERE id IN (" + strings.Join(placeholders, ",") + ")"
	if _, err := db.Exec(query, ids...); err != nil {
		appLog.Error("addEvent trim delete error:", err.Error())
	}
}

// ==== Chat ====

func (ad *AllianceData) SendChatMessage(app *AllianceApp, in *gameServerService.SendChatMessageRequest) uint32 {
	// 2026-08-24 联盟频道改造: 只对属于该联盟的帮会广播
	// 旧实现 BroadcastToGameServers 会推给所有 game server,浪费 RPC,也不符合"只对联盟下帮会"语义
	// 新实现参照 broadcastNewEventToGuilds 的 groupMembersByServer 模式,
	// 只给"该联盟有成员帮会"的 game server 推 ChatMessageBroadcast。
	// game server 端 onChatMessage 还会再按 Guild.leagueUUID 本地过滤一次(纵深防御)。

	cache, ok := ad.alliances.Get(in.AllianceId)
	if !ok {
		return ErrCodeAllianceNotFound
	}

	serverToGuilds := groupMembersByServer(cache)
	if nil == serverToGuilds || len(serverToGuilds) == 0 {
		// 联盟存在但没有任何成员(理论上不应发生),直接返回成功
		return ErrCodeSuccess
	}

	chatMsg := &gameServerService.AllianceChatMessage{
		SenderGuildId:   in.SenderGuildId,
		SenderGuildName: in.SenderGuildName,
		SenderServerId:  in.SenderServerId,
		AvatarInfo:      in.AvatarInfo,
		Content:         in.Content,
		SendTime:        nowTS(),
		SenderType:      0, // 玩家发言固定 0=PLAYER;援助/宣战的系统消息走单独路径(未来可定义 AllianceChatSenderType enum)
	}

	for serverId := range serverToGuilds {
		gs := app.getGameServer(serverId)
		if gs == nil {
			continue
		}
		client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient)
		if !ok || client == nil {
			continue
		}
		client.OnChatMessage(&gameServerService.ChatMessageBroadcast{
			AllianceId: in.AllianceId,
			Message:    chatMsg,
		})
	}

	return ErrCodeSuccess
}

func (ad *AllianceData) GetChatHistory(in *gameServerService.GetChatHistoryRequest) []*gameServerService.AllianceChatMessage {
	return nil
}

// ==== Tick: Check Expired Wars ====

func (ad *AllianceData) checkAndRemoveExpiredWars(db *sql.DB, app *AllianceApp) {
	now := nowTS()

	// Snapshot the expired row keys under the cache lock so we can
	// drop the lock before running the per-row DB delete + broadcast
	// (each broadcast hops the gRPC client and would otherwise hold
	// the cache for the duration of every server round-trip).
	type expiredRow struct {
		key        string
		AttackType uint32
		AttackId   uint64
		targetType uint32
		targetId   uint64
	}
	expired := make([]expiredRow, 0)

	enemiesCache.RLock()
	for k, v := range enemiesCache.byRow {
		if v.EndTime <= now {
			expired = append(expired, expiredRow{
				key:        k,
				AttackType: v.AttackType,
				AttackId:   v.AttackId,
				targetType: v.TargetType,
				targetId:   v.TargetId,
			})
		}
	}
	enemiesCache.RUnlock()

	for _, r := range expired {
		// Re-check under no lock; the row may have been cancelled or
		// refreshed by a concurrent DeclareWar between snapshot and
		// remove. removeEnemyPairs is itself idempotent and bails on
		// a missing byRow entry, so a stale snapshot is safe.
		ad.removeEnemyPairs(r.AttackType, r.targetType, r.AttackId, r.targetId)
		db.Exec("DELETE FROM alliance_enemy WHERE attacker_type = ? AND attacker_id = ? AND target_type = ? AND target_id = ?",
			r.AttackType, r.AttackId, r.targetType, r.targetId)

		app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
			client.OnWarEnded(&gameServerService.WarEndedBroadcast{
				AttackType: r.AttackType,
				AttackId:   r.AttackId,
				TargetType: r.targetType,
				TargetId:   r.targetId,
			})
		})

		ad.removeWarGuildRelations(app, r.AttackType, r.AttackId, r.targetType, r.targetId)
	}
}

// ==== Helpers ====

func (ad *AllianceData) notifyAllianceLeaderNewMemberJoined(app *AllianceApp, leaderServerId uint32, playerGbId uint64, member *gameServerService.AllianceMemberInfo) {
	if app == nil || leaderServerId == 0 {
		return
	}
	if gs := app.getGameServer(leaderServerId); gs != nil {
		if client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient); ok {
			client.OnNewMemberJoined(&gameServerService.NewMemberJoinedNotify{
				PlayerGbId: playerGbId,
				Member:     member,
			})
		}
	}
}

func (ad *AllianceData) notifyAllianceApplyMemberJoined(app *AllianceApp, allianceId uint64, guildUUID uint64, applyServerId uint32) {
	if app == nil || applyServerId == 0 {
		return
	}
	if gs := app.getGameServer(applyServerId); gs != nil {
		if client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient); ok {
			client.OnJoinToAllianceNotify(&gameServerService.JoinToAllianceNotify{
				AllianceId: allianceId,
				GuildUUID:  guildUUID,
			})
		}
	}
}

func contains(s, substr string) bool {
	if len(substr) == 0 {
		return true
	}
	return len(s) >= len(substr) && containsKMP(s, substr)
}

func containsKMP(s, sub string) bool {
	for i := 0; i <= len(s)-len(sub); i++ {
		match := true
		for j := 0; j < len(sub); j++ {
			if s[i+j] != sub[j] {
				match = false
				break
			}
		}
		if match {
			return true
		}
	}
	return false
}

// compareAlliances returns -1 if a should come before b in the league list,
// +1 if a should come after b, and 0 if they are equal. The order is:
// totalScore DESC, memberCount DESC, createdAt ASC, allianceId ASC.
//
// Reading the fields without holding the cache's lock mirrors the existing
// behaviour of the pre-sorted read path (uint32/uint64 word-sized reads);
// writers that mutate these fields via updateDerivedFields are expected to
// do so while holding the cache's write lock.
func compareAlliances(a, b *AllianceCache) int {
	if a == nil && b == nil {
		return 0
	}
	if a == nil {
		return 1
	}
	if b == nil {
		return -1
	}
	if a.info.TotalScore != b.info.TotalScore {
		if a.info.TotalScore > b.info.TotalScore {
			return -1
		}
		return 1
	}
	if a.info.MemberCount != b.info.MemberCount {
		if a.info.MemberCount > b.info.MemberCount {
			return -1
		}
		return 1
	}
	if a.info.CreatedAt != b.info.CreatedAt {
		if a.info.CreatedAt < b.info.CreatedAt {
			return -1
		}
		return 1
	}
	if a.info.AllianceId != b.info.AllianceId {
		if a.info.AllianceId < b.info.AllianceId {
			return -1
		}
		return 1
	}
	return 0
}

// insertSortedAlliance inserts cache at the correct position in the
// sortedAlliances index. The slice's existing order must already be
// correct; this is O(n) due to the in-place shift.
func (ad *AllianceData) insertSortedAlliance(cache *AllianceCache) {
	if cache == nil {
		return
	}
	ad.sortedLock.Lock()
	defer ad.sortedLock.Unlock()
	pos := sortedInsertPosition(ad.sortedAlliances, cache)
	ad.sortedAlliances = append(ad.sortedAlliances, nil)
	copy(ad.sortedAlliances[pos+1:], ad.sortedAlliances[pos:])
	ad.sortedAlliances[pos] = cache
}

// removeSortedAlliance removes cache from the sorted index. No-op if the
// alliance is not present.
func (ad *AllianceData) removeSortedAlliance(cache *AllianceCache) {
	if cache == nil {
		return
	}
	ad.sortedLock.Lock()
	defer ad.sortedLock.Unlock()
	for i, c := range ad.sortedAlliances {
		if c == cache || (c != nil && c.info.AllianceId == cache.info.AllianceId) {
			ad.sortedAlliances = append(ad.sortedAlliances[:i], ad.sortedAlliances[i+1:]...)
			return
		}
	}
}

// resortAlliance removes cache from the sorted index (if present) and
// re-inserts it at the position dictated by the current sort key. Use
// this whenever MemberCount or TotalScore changes.
func (ad *AllianceData) resortAlliance(cache *AllianceCache) {
	if cache == nil {
		return
	}
	ad.sortedLock.Lock()
	defer ad.sortedLock.Unlock()
	for i, c := range ad.sortedAlliances {
		if c == cache || (c != nil && c.info.AllianceId == cache.info.AllianceId) {
			ad.sortedAlliances = append(ad.sortedAlliances[:i], ad.sortedAlliances[i+1:]...)
			break
		}
	}
	pos := sortedInsertPosition(ad.sortedAlliances, cache)
	ad.sortedAlliances = append(ad.sortedAlliances, nil)
	copy(ad.sortedAlliances[pos+1:], ad.sortedAlliances[pos:])
	ad.sortedAlliances[pos] = cache
}

// sortedInsertPosition returns the smallest index at which cache should be
// inserted to keep the slice sorted. The slice is searched with a linear
// scan, which is good enough for the small-to-medium alliance populations
// this service is expected to host; switch to binary search if the index
// grows large enough to need it.
func sortedInsertPosition(sorted []*AllianceCache, cache *AllianceCache) int {
	for i, c := range sorted {
		if compareAlliances(c, cache) > 0 {
			return i
		}
	}
	return len(sorted)
}

// rebuildSortedAlliances wipes and rebuilds the sorted index from the
// current alliance map. Used at startup (loadFromDB) and as a recovery
// path; do not call on every data change.
func (ad *AllianceData) rebuildSortedAlliances() {
	ad.sortedLock.Lock()
	defer ad.sortedLock.Unlock()
	ad.sortedAlliances = ad.sortedAlliances[:0]
	ad.alliances.IterCb(func(_ uint64, c *AllianceCache) {
		ad.sortedAlliances = append(ad.sortedAlliances, c)
	})
	// Sort using the standard library; this is a one-shot rebuild, not
	// the hot path, so the extra allocation is acceptable.
	sort.SliceStable(ad.sortedAlliances, func(i, j int) bool {
		return compareAlliances(ad.sortedAlliances[i], ad.sortedAlliances[j]) < 0
	})
}

func (ad *AllianceData) NotifyGuildEvent(app *AllianceApp, serverId uint32, guildId uint64, messageId uint32, messageArgs []string) bool {
	gs := app.getGameServer(serverId)
	if gs == nil {
		return false
	}
	client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient)
	if !ok || client == nil {
		return false
	}

	client.OnLeagueGuildEventNotify(&gameServerService.LeagueGuildEvent{
		GuildId:     guildId,
		MessageId:   messageId,
		MessageArgs: messageArgs,
	})
	return true
}

func (ad *AllianceData) NotifyGuildMsg(app *AllianceApp, serverId uint32, guildId uint64, messageId uint32, messageArgs []string) bool {
	gs := app.getGameServer(serverId)
	if gs == nil {
		return false
	}
	client, ok := gs.GetClientEndPoint().(*gameServerService.GameClientClient)
	if !ok || client == nil {
		return false
	}

	client.OnLeagueGuildMessageNotify(&gameServerService.LeagueGuildMessage{
		GuildId:     guildId,
		MessageId:   messageId,
		MessageArgs: messageArgs,
	})
	return true
}

func (ad *AllianceData) RecruitLeagueMember(app *AllianceApp, leagueUUID uint64) uint32 {
	cache, ok := ad.alliances.Get(leagueUUID)
	if !ok {
		return ErrCodeAllianceNotFound
	}
	cache.Lock()
	defer cache.Unlock()
	guildCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_GUILD_CONST)
	if !ok {
		return ErrCodeNoGuildConstCfg
	}
	unionNum := 0
	unionApplicationNum := 0
	unionNumCfg := guildCfg.GetStringMapString("guild_unionNum")
	if a, ok := unionNumCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：1", err)
			return ErrCodeNoGuildConstCfg
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg
		}
		unionNum = b
	} else {
		return ErrCodeNoGuildConstCfg
	}
	unionApplicationNumCfg := guildCfg.GetStringMapString("guild_unionApplicationNum")
	if a, ok := unionApplicationNumCfg["value"]; ok {
		b, err := strconv.Atoi(a)
		if err != nil {
			fmt.Println("转换失败：1", err)
			return ErrCodeNoGuildConstCfg
		}
		if b <= 0 {
			return ErrCodeNoGuildConstCfg
		}
		unionApplicationNum = b
	} else {
		return ErrCodeNoGuildConstCfg
	}

	memberCount := len(cache.members)
	if memberCount >= unionNum {
		return ErrCodeAllianceFull
	}

	applyCount := len(cache.applies)
	if applyCount >= unionApplicationNum {
		return ErrCodeApplyListFull
	}
	chatCfg, ok := ConfigStore.cfgVipers.Get(CFG_TYPE_MESSAGE_CHAT_MESSAGE)
	if !ok {
		return ErrCodeNoMessageChatMessageCfg
	}
	recruitChatMessageId := 0
	if v := chatCfg.GetInt("guild_union_recruit_chat"); v > 0 {
		recruitChatMessageId = v
	} else {
		return ErrCodeNoMessageChatMessageCfg
	}
	app.BroadcastToGameServers(func(client *gameServerService.GameClientClient) {
		client.OnLeagueBroadCastMessageNotify(&gameServerService.LeagueBroadCastMessage{
			FromUID:     leagueUUID,
			ToUID:       leagueUUID,
			MessageId:   uint32(recruitChatMessageId),
			MessageArgs: []string{strconv.Itoa(int(cache.info.AllianceId)), cache.info.Name},
		})
	})
	return ErrCodeSuccess
}

func (ad *AllianceData) CheckLeaveGuild(db *sql.DB, app *AllianceApp, leagueUUID uint64, guildId uint64, playerGbId uint64) bool {
	ret := ad.doLeaveLeague(db, app, leagueUUID, guildId, playerGbId)
	// 退掉联盟
	return ret == ErrCodeAllianceNotFound || ret == ErrCodeSuccess
}

func (ad *AllianceData) QueryLeagueUUID(guildId uint64) (uint64, bool) {
	ad.initedLock.RLock()
	defer ad.initedLock.RUnlock()
	if ad.isInited {
		leagueUUID, ret := ad.guildToAlliance.Get(guildId)
		if ret {
			return leagueUUID, true
		}
		return 0, true
	}
	return 0, false
}

func (ad *AllianceData) RemoveEnemyRelation(app *AllianceApp, db *sql.DB, guildId uint64) uint32 {
	ad.removeAllEnemyRelationsForGuild(app, db, guildId, false)
	return ErrCodeSuccess
}
