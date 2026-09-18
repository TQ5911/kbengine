package crossTeamApp

const (
	_ = iota
	SERVICE_CROSS_TEAM
)

const (
	// DEFAULT_WORKER_NUM 队伍 worker 默认数量（配置 WorkerNum <= 0 时生效）
	DEFAULT_WORKER_NUM = 16
	// MATCH_TICK_SECONDS 撮合轮次周期（秒，同本服 TeamMatchStub 节奏）
	MATCH_TICK_SECONDS = 3
	// CHAT_FLUSH_MS 聊天聚合缓冲 flush 周期（毫秒，0.5s 短缓存聚合）
	CHAT_FLUSH_MS = 500
	// WORKER_SWEEP_SECONDS worker 周期扫描间隔（申请超时/队长离线转让等）
	WORKER_SWEEP_SECONDS = 3
	// MATCH_TIMEOUT_SECONDS 散人匹配入池默认超时（秒），超时出池并下发 MatchTimeout。
	// 可在配置 matchTimeoutSeconds 覆盖；决策 D5 起游戏服入池时按玩家携带配表 maxMatchTime，
	// 本值仅作为未携带（<=0）时的回落默认
	MATCH_TIMEOUT_SECONDS = 300
)

// matchTimeoutSeconds 散人匹配入池回落超时（秒），NewCrossTeamApp 按配置覆盖；
// 玩家入池携带 timeoutSeconds>0 时按玩家值生效
var matchTimeoutSeconds = MATCH_TIMEOUT_SECONDS

const (
	// TEAM_APPLY_MAX_NUM 申请列表上限（参照本服 TEAM_APPLY_JOIN_MAX_NUM）
	TEAM_APPLY_MAX_NUM = 20
	// APPLY_TIMEOUT_SECONDS 入队申请超时（秒），超时由 worker 周期清理
	APPLY_TIMEOUT_SECONDS = 60
	// TEAM_LIST_REFRESH_SECONDS 队伍列表快照后台刷新周期（秒）
	TEAM_LIST_REFRESH_SECONDS = 5
	// CROSS_TEAM_GROUP_SIZE 每个小组人数上限（客户端按 5 人一组显示）
	CROSS_TEAM_GROUP_SIZE = 5
)

// MemberLeavePush 的 reason（离队场景细分）
const (
	_                    = iota
	LEAVE_REASON_LEAVE   // 主动离队
	LEAVE_REASON_KICK    // 被踢出
	LEAVE_REASON_OFFLINE // 离线被移出
)

// TeamOpResult 的 resultCode 错误码
const (
	ERROR_CODE_SUCCESS             = 0
	ERROR_CODE_COMMON              = 1
	ERROR_CODE_TEAM_NOT_FOUND      = 2  // 队伍不存在
	ERROR_CODE_TEAM_FULL           = 3  // 队伍已满
	ERROR_CODE_TEAM_IN_DUNGEON     = 4  // 正在跨服副本中，禁止新申请/加入
	ERROR_CODE_PASSWORD_WRONG      = 5  // 密码错误
	ERROR_CODE_LEVEL_NOT_ENOUGH    = 6  // 等级不足（原 NOT_MEET_CONDITION 拆分）
	ERROR_CODE_APPLY_LIST_FULL     = 7  // 申请列表已满
	ERROR_CODE_NOT_CAPTAIN         = 8  // 不是队长
	ERROR_CODE_NOT_TEAM_MEMBER     = 9  // 目标玩家不在队伍中
	ERROR_CODE_ALREADY_IN_TEAM     = 10 // 已在其他跨服队伍中
	ERROR_CODE_INVALID_PARAM       = 11 // 参数非法（目标/门槛等）
	ERROR_CODE_DUPLICATED_TEAM     = 12 // teamId 已存在
	ERROR_CODE_NOT_INVITED         = 13 // 无有效邀请
	ERROR_CODE_NOT_APPLIED         = 14 // 无有效申请
	ERROR_CODE_APPLY_REJECTED      = 15 // 入队申请被拒绝
	ERROR_CODE_MATCH_JOIN_INVALID  = 16 // 撮合入队作废（队伍已满/解散/不再自动匹配等），需重新发起匹配
	ERROR_CODE_CRUSADE_RATE_LIMIT  = 17 // 讨伐发起被限流（全组并发上限/单服每秒上限）
	ERROR_CODE_CRUSADE_IN_PROGRESS = 18 // 已有进行中的讨伐检查/副本
	ERROR_CODE_GROUP_FULL          = 19 // 目标小组已满 5 人
	ERROR_CODE_INVALID_POS         = 20 // 源/目标位置信息与中心不一致
	// 21 已被游戏服侧 CROSS_TEAM_RESULT_NOT_IMPLEMENTED 占用，中心不再使用；
	// 22 起与游戏服侧 gameconst.CROSS_TEAM_RESULT_* 编号一一对齐
	ERROR_CODE_SERVER_MISMATCH    = 22 // 本服目标队伍仅允许本服玩家（成员 serverId 与队伍 dunServer 不一致）
	ERROR_CODE_DUN_SERVER_INVALID = 23 // 副本创建目标服非法（dunServer=0）
	// 申请成为队长被队长拒绝（replyBecomeCaptain 拒绝时主动通知申请人）
	ERROR_CODE_BECOME_CAPTAIN_REJECTED = 24
	// 需要密码（目标队伍设了密码而申请未携带，与密码错误区分）
	ERROR_CODE_NEED_PASSWORD = 25
	// 战力不足（与等级不足按 ERROR_CODE_LEVEL_NOT_ENOUGH=6 区分）
	ERROR_CODE_SCORE_NOT_ENOUGH = 26
	// 无副团长可取消（setDeputy 取消时校验，对齐本服 transferRaidDeputy 的
	// ENUM_RAID_NOT_RAID_DEPUTY 口径；与游戏服侧 gameconst.CROSS_TEAM_RESULT_NOT_DEPUTY 对齐）
	ERROR_CODE_NOT_DEPUTY = 27
)

// 讨伐状态机
const (
	CRUSADE_STATE_NONE           = 0 // 无讨伐
	CRUSADE_STATE_CHECKING       = 1 // 条件检查中
	CRUSADE_STATE_SPACE_CREATING = 2 // 副本空间创建中
	CRUSADE_STATE_IN_DUNGEON     = 3 // 已在副本中（原 InDungeon 字段并入状态机）
)

// 讨伐中止原因（CrusadeAbortMsg.reason）
const (
	CRUSADE_ABORT_CHECK_FAIL     = 1 // 有成员条件检查不满足
	CRUSADE_ABORT_CHECK_TIMEOUT  = 2 // 检查超时
	CRUSADE_ABORT_SPACE_FAILED   = 3 // 副本空间创建失败/超时
	CRUSADE_ABORT_CROSS_NOT_CONN = 4 // 跨服服未连接
)

// CRUSADE_CHECK_TIMEOUT_SECONDS 条件检查/空间创建超时（秒），worker sweep 处理
const CRUSADE_CHECK_TIMEOUT_SECONDS = 30

// CRUSADE_REJOIN_CD_SECONDS 讨伐重进冷却（秒，同本服 raid_rejoinCdTime）：
// 副本结束 crusadeFinished 写 LastDungeonFinishedTime = 完成时刻 + 本常量（CD 截止时刻，
// 对齐本服 refreshLastDungeonFinishedTime 线上值口径），截止前禁止再次发起
const CRUSADE_REJOIN_CD_SECONDS = 5

// TEAM_MARK_MAX_SLOT 队伍标记槽位上限（1-based，对齐本服 gameconst.TEAM_MARK_MAX_SLOT）
const TEAM_MARK_MAX_SLOT = 8

// 标记类型（MarkInfo.type，对齐本服 gameconst.TeamMarkType）
const (
	MARK_TYPE_NONE     = 0
	MARK_TYPE_TEAMMATE = 1 // 标记队友
	MARK_TYPE_ENEMY    = 2 // 标记敌方/怪物（唯一有服务端联动的类型：怪物死亡自动摘除）
	MARK_TYPE_SCENE    = 3 // 场景点标记
)

// 标记变更类型（MarkChangePushMsg.changeType，对齐本服 gameconst.TeamMarkChangeType）
const (
	MARK_CHANGE_NONE    = 0
	MARK_CHANGE_ADD     = 1
	MARK_CHANGE_MODIFY  = 2 // 预留（同槽覆盖/换槽以 DELETE+ADD 表达，不下发 MODIFY）
	MARK_CHANGE_DELETE  = 3
	MARK_CHANGE_CAPTAIN = 4 // 仅队长开关变更（mark 无效，onlyCaptainCanMark 有效）
)
