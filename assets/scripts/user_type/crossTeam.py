# -*- coding: utf-8 -*-
# 跨服组队数据类型：
# CrossTeamMemberCacheVal  成员缓存（姓名/等级/职业/战力/血量/所在服/spaceNo/position/分组位置）
# CrossTeamCacheVal        玩家视角队伍缓存（Avatar 持有，参照 TeamCacheValInPlayer）
# teamInfoPbToStreamDict   中心 CrossTeamInfo pb -> streamDict 纯转换（CrossTeamStub 已不维护
#                          队伍缓存，全量推送/登录恢复均直接由 pb 转换下发）
# memberInfoPbToStreamDict 中心 MemberInfo pb -> 成员 streamDict 纯转换（单成员增量推送用，
#                          与 teamInfoPbToStreamDict 成员条目同构，含高频快照默认初始值）
# markInfoPbToStreamDict   中心 MarkInfo pb -> 标记 streamDict 纯转换（键名对齐
#                          CLIENT_TEAM_MARK_VAL；markChangePush 增量与全量标记列表共用）
# 注意：变更类型等常量统一定义在 gameconst（与中心 crossConst.go 逐值对齐）

import gameconst
import userType


def emptyTeamMarkInfo():
    # CLIENT_TEAM_MARK_INFO 空结构（无标记时的初始值）
    return {'playerList': [], 'sceneList': [], 'onlyCaptainCanMark': False}


def markInfoPbToStreamDict(markInfo):
    # 中心 MarkInfo pb -> 标记 streamDict（CLIENT_TEAM_MARK_VAL 同构，全键输出）
    return {
        'type': markInfo.type,
        'index': markInfo.index,
        'name': markInfo.name,
        'gbId': markInfo.gbId,
        'serverId': markInfo.serverId,
        'entId': markInfo.entId,
        'pos': (markInfo.posX, markInfo.posY, markInfo.posZ),
        'spaceNo': markInfo.spaceNo,
    }


def teamInfoPbToStreamDict(teamInfo):
    # 中心 CrossTeamInfo pb -> 客户端 streamDict（与 CrossTeamCacheVal.toStreamDict 同构）。
    # pb 不含成员高频状态快照（hp/spaceNo/position），按默认初始值填充，
    # 客户端随后由 3s 的 onCrossTeamMemberState 广播覆盖。
    # 服务端按 groupIdx 分组、组内按 pos 升序下发；成员 dict 中携带 groupIdx/pos，
    # 既供服务端缓存重建，也随 CROSS_TEAM_MEMBER_CACHE_VAL 序列化下发客户端。
    _blockedSet = set(teamInfo.blockedMembers)
    groups = {}
    for _m in teamInfo.members:
        groups.setdefault(_m.groupIdx, []).append({
            'gbId': _m.gbId,
            'serverId': _m.serverId,
            'playerName': _m.name,
            'level': _m.level,
            'school': _m.school,
            'score': _m.score,
            'hp': 1,
            'maxHp': 1,
            'spaceNo': 0,
            'position': (0, 0, 0),
            'groupIdx': _m.groupIdx,
            'pos': _m.pos,
            # 客户端接口对齐补充（1.1）：展示/语音状态字段
            'sex': _m.sex,
            'picFrameId': _m.picFrameId,
            'enableMics': _m.enableMics,
            # 被禁麦与队伍级 blockedMembers 同源判定（与 memberVoiceStatePush 一致）
            'isBlockMics': _m.gbId in _blockedSet,
            'enableSpeaker': _m.enableSpeaker,
            'inVoiceRoom': _m.inVoiceRoom,
            'openId': _m.openId,
        })

    groupList = []
    for _idx in sorted(groups.keys()):
        _members = sorted(groups[_idx], key=lambda x: x.get('pos', 0))
        _memberList = []
        for _m in _members:
            _memberList.append({
                'gbId': _m['gbId'],
                'serverId': _m['serverId'],
                'playerName': _m['playerName'],
                'level': _m['level'],
                'school': _m['school'],
                'score': _m['score'],
                'hp': _m['hp'],
                'maxHp': _m['maxHp'],
                'spaceNo': _m['spaceNo'],
                'position': _m['position'],
                'groupIdx': _m['groupIdx'],
                'pos': _m['pos'],
                'sex': _m['sex'],
                'picFrameId': _m['picFrameId'],
                'enableMics': _m['enableMics'],
                'isBlockMics': _m['isBlockMics'],
                'enableSpeaker': _m['enableSpeaker'],
                'inVoiceRoom': _m['inVoiceRoom'],
                'openId': _m['openId'],
            })
        groupList.append({
            'groupIdx': _idx,
            'memberList': _memberList,
        })

    return {
        'teamId': teamInfo.teamId,
        'target': teamInfo.target,
        'captainGbId': teamInfo.captainGbId,
        'minLevel': teamInfo.minLevel,
        'minScore': teamInfo.minScore,
        'intro': teamInfo.intro,
        'maxNum': teamInfo.maxNum,
        'autoMatch': teamInfo.autoMatch,
        'autoEnter': teamInfo.autoEnter,
        'inDungeon': teamInfo.inDungeon,
        'micsMode': teamInfo.micsMode,
        'blockedMembers': list(teamInfo.blockedMembers),
        'groupList': groupList,
        # 客户端接口对齐补充（1.3）：isPublish 按 password 空否派生，memberNum 按成员数填；
        # password 随全量下发（队伍设置不改密码时客户端原样上传）
        'isPublish': teamInfo.password == '',
        'password': teamInfo.password,
        'deputyGbId': teamInfo.deputyGbId,
        'lastDungeonFinishedTime': teamInfo.lastDungeonFinishedTime,
        'autoMatchTime': teamInfo.autoMatchTime,
        'memberNum': len(teamInfo.members),
        # 队伍标记全量（中心权威数据；增量变更走 markChangePush 经 applyMarkChange 落地）
        'teamMarkInfo': {
            'playerList': [markInfoPbToStreamDict(_m) for _m in teamInfo.playerMarks],
            'sceneList': [markInfoPbToStreamDict(_m) for _m in teamInfo.sceneMarks],
            'onlyCaptainCanMark': teamInfo.onlyCaptainCanMark,
        },
    }


def memberInfoPbToStreamDict(memberInfo):
    # 中心 MemberInfo pb -> 成员 streamDict（与 teamInfoPbToStreamDict 成员条目同构）。
    # pb 不含成员高频状态快照（hp/spaceNo/position），按默认初始值填充，
    # 客户端随后由 3s 的 onCrossTeamMemberState 广播覆盖。
    # isBlockMics 直接用中心填充值（MemberJoinPush 单个成员推送无队伍 blockedMembers 列表；
    # 全量推送走 teamInfoPbToStreamDict 按 blockedMembers 判定）
    return {
        'gbId': memberInfo.gbId,
        'serverId': memberInfo.serverId,
        'playerName': memberInfo.name,
        'level': memberInfo.level,
        'school': memberInfo.school,
        'score': memberInfo.score,
        'hp': 1,
        'maxHp': 1,
        'spaceNo': 0,
        'position': (0, 0, 0),
        'groupIdx': memberInfo.groupIdx,
        'pos': memberInfo.pos,
        # 客户端接口对齐补充（1.1）：展示/语音状态字段
        'sex': memberInfo.sex,
        'picFrameId': memberInfo.picFrameId,
        'enableMics': memberInfo.enableMics,
        'isBlockMics': memberInfo.isBlockMics,
        'enableSpeaker': memberInfo.enableSpeaker,
        'inVoiceRoom': memberInfo.inVoiceRoom,
        'openId': memberInfo.openId,
    }


class CrossTeamMemberCacheVal(userType.UserSingleType):
    def __init__(self, gbId=0, serverId=0, playerName='', level=0, school=0, score=0):
        self.gbId = gbId
        self.serverId = serverId
        self.playerName = playerName
        self.level = level
        self.school = school
        self.score = score
        # 高频状态快照（中心 3s 广播覆盖）
        self.hp = 1
        self.maxHp = 1
        self.spaceNo = 0
        self.position = (0, 0, 0)
        # 服务端分组/排序数据（随 CROSS_TEAM_MEMBER_CACHE_VAL 下发，客户端编队展示用）
        self.groupIdx = 1
        self.pos = 1
        # 展示与语音状态字段（客户端接口对齐补充 1.1；全量初始值，变更走独立推送）
        self.sex = 0
        self.picFrameId = 0
        self.enableMics = False
        self.isBlockMics = False
        self.enableSpeaker = False
        self.inVoiceRoom = False
        self.openId = ''

    def fromStreamDict(self, dataDict):
        # 仅支持客户端 CROSS_TEAM_MEMBER_CACHE_VAL 结构（maxHp）
        self.gbId = dataDict.get('gbId', 0)
        self.serverId = dataDict.get('serverId', 0)
        self.playerName = dataDict.get('playerName', '')
        self.level = dataDict.get('level', 0)
        self.school = dataDict.get('school', 0)
        self.score = dataDict.get('score', 0)
        self.hp = dataDict.get('hp', 1)
        self.maxHp = dataDict.get('maxHp', 1)
        self.spaceNo = dataDict.get('spaceNo', 0)
        self.position = dataDict.get('position', (0, 0, 0))
        self._groupIdx = dataDict.get('groupIdx', 1)
        self._pos = dataDict.get('pos', 1)
        self.sex = dataDict.get('sex', 0)
        self.picFrameId = dataDict.get('picFrameId', 0)
        self.enableMics = dataDict.get('enableMics', False)
        self.isBlockMics = dataDict.get('isBlockMics', False)
        self.enableSpeaker = dataDict.get('enableSpeaker', False)
        self.inVoiceRoom = dataDict.get('inVoiceRoom', False)
        self.openId = dataDict.get('openId', '')

    def toStreamDict(self):
        # 客户端 CROSS_TEAM_MEMBER_CACHE_VAL 结构（groupIdx/pos 随成员下发，客户端编队展示用）
        return {
            'gbId': self.gbId,
            'serverId': self.serverId,
            'playerName': self.playerName,
            'level': self.level,
            'school': self.school,
            'score': self.score,
            'hp': self.hp,
            'maxHp': self.maxHp,
            'spaceNo': self.spaceNo,
            'position': self.position,
            'groupIdx': self._groupIdx,
            'pos': self._pos,
            'sex': self.sex,
            'picFrameId': self.picFrameId,
            'enableMics': self.enableMics,
            'isBlockMics': self.isBlockMics,
            'enableSpeaker': self.enableSpeaker,
            'inVoiceRoom': self.inVoiceRoom,
            'openId': self.openId,
        }

    def updateState(self, stateDict):
        # 更新成员高频状态快照
        if 'hp' in stateDict:
            self.hp = stateDict['hp']
        if 'maxHp' in stateDict:
            self.maxHp = stateDict['maxHp']
        if 'level' in stateDict:
            self.level = stateDict['level']
        if 'score' in stateDict:
            self.score = stateDict['score']
        if 'spaceNo' in stateDict:
            self.spaceNo = stateDict['spaceNo']
        if 'position' in stateDict:
            self.position = stateDict['position']

    def updateAttr(self, arrDic):
        for attrName, attrVal in arrDic.items():
            if not hasattr(self, attrName):
                continue

            setattr(self, attrName, attrVal)


class CrossTeamCacheVal(userType.UserSingleType):
    def __init__(self, teamId=0, target=0, captainGbId=0):
        self.teamId = teamId
        self.target = target
        self.captainGbId = captainGbId
        self.minLevel = 0
        self.minScore = 0
        self.intro = ''
        self.maxNum = 0
        self.autoMatch = False
        self.autoEnter = False
        self.inDungeon = False
        self.memberDict = {}  # {gbid: CrossTeamMemberCacheVal}
        self.micsMode = 0
        self.blockedMembers = []
        # 客户端接口对齐补充（1.3）：isPublish 由 password 空否派生
        self.isPublish = True
        self.password = ''
        self.deputyGbId = 0
        self.lastDungeonFinishedTime = 0
        self.autoMatchTime = 0
        self.teamMarkInfo = emptyTeamMarkInfo()

    def reset(self):
        self.teamId = 0
        self.target = 0
        self.captainGbId = 0
        self.minLevel = 0
        self.minScore = 0
        self.intro = ''
        self.maxNum = 0
        self.autoMatch = False
        self.autoEnter = False
        self.inDungeon = False
        self.memberDict = {}
        self.micsMode = 0
        self.blockedMembers = []
        self.isPublish = True
        self.password = ''
        self.deputyGbId = 0
        self.lastDungeonFinishedTime = 0
        self.autoMatchTime = 0
        self.teamMarkInfo = emptyTeamMarkInfo()

    def fromStreamDict(self, dataDict):
        self.teamId = dataDict.get('teamId', 0)
        self.target = dataDict.get('target', 0)
        self.captainGbId = dataDict.get('captainGbId', 0)
        self.minLevel = dataDict.get('minLevel', 0)
        self.minScore = dataDict.get('minScore', 0)
        self.intro = dataDict.get('intro', '')
        self.maxNum = dataDict.get('maxNum', 0)
        self.autoMatch = dataDict.get('autoMatch', False)
        self.autoEnter = dataDict.get('autoEnter', False)
        self.inDungeon = dataDict.get('inDungeon', False)
        self.micsMode = dataDict.get('micsMode', 0)
        self.blockedMembers = list(dataDict.get('blockedMembers', []))
        self.isPublish = dataDict.get('isPublish', True)
        self.password = dataDict.get('password', '')
        self.deputyGbId = dataDict.get('deputyGbId', 0)
        self.lastDungeonFinishedTime = dataDict.get('lastDungeonFinishedTime', 0)
        self.autoMatchTime = dataDict.get('autoMatchTime', 0)
        self.teamMarkInfo = dataDict.get('teamMarkInfo') or emptyTeamMarkInfo()
        self.memberDict = {}

        # 优先按新的 groupList 解析；兼容旧版平铺 memberList（整体视为第 1 组）
        _groupList = dataDict.get('groupList', [])
        if not _groupList and 'memberList' in dataDict:
            _groupList = [{'groupIdx': 1, 'memberList': dataDict['memberList']}]

        for _group in _groupList:
            _groupIdx = _group.get('groupIdx', 1)
            for _memberDict in _group.get('memberList', []):
                _memberDict['groupIdx'] = _groupIdx
                _val = CrossTeamMemberCacheVal()
                _val.fromStreamDict(_memberDict)
                self.memberDict[_val.gbId] = _val

    def toStreamDict(self):
        # 按 _groupIdx 分组、组内按 _pos 排序后下发
        _groups = {}
        for _m in self.memberDict.values():
            _groups.setdefault(_m._groupIdx, []).append(_m)

        _groupList = []
        for _idx in sorted(_groups.keys()):
            _members = sorted(_groups[_idx], key=lambda x: x._pos)
            _groupList.append({
                'groupIdx': _idx,
                'memberList': [_m.toStreamDict() for _m in _members],
            })

        return {
            'teamId': self.teamId,
            'target': self.target,
            'captainGbId': self.captainGbId,
            'minLevel': self.minLevel,
            'minScore': self.minScore,
            'intro': self.intro,
            'maxNum': self.maxNum,
            'autoMatch': self.autoMatch,
            'autoEnter': self.autoEnter,
            'inDungeon': self.inDungeon,
            'micsMode': self.micsMode,
            'blockedMembers': list(self.blockedMembers),
            'groupList': _groupList,
            # 客户端接口对齐补充（1.3）：memberNum 按成员数填
            'isPublish': self.isPublish,
            'password': self.password,
            'deputyGbId': self.deputyGbId,
            'lastDungeonFinishedTime': self.lastDungeonFinishedTime,
            'autoMatchTime': self.autoMatchTime,
            'memberNum': len(self.memberDict),
            'teamMarkInfo': self.teamMarkInfo,
        }

    def addMember(self, memberData):
        # 添加/更新成员；新成员继承旧状态快照（hp/maxHp/spaceNo/position）
        if isinstance(memberData, CrossTeamMemberCacheVal):
            _newVal = memberData
        else:
            _newVal = CrossTeamMemberCacheVal()
            _newVal.fromStreamDict(memberData)

        _oldVal = self.memberDict.get(_newVal.gbId)
        if _oldVal:
            _newVal.hp = _oldVal.hp
            _newVal.maxHp = _oldVal.maxHp
            _newVal.spaceNo = _oldVal.spaceNo
            _newVal.position = _oldVal.position
            _newVal.groupIdx = _oldVal._groupIdx
            _newVal.pos = _oldVal._pos

        self.memberDict[_newVal.gbId] = _newVal
        return _newVal

    def removeMember(self, gbId):
        return self.memberDict.pop(gbId, None)

    def setCaptain(self, captainGbId):
        self.captainGbId = captainGbId

    def updateSettings(self, settingsDict):
        # 更新门槛/介绍/满员自动进本/密码（目标创建后不可改；autoMatch 修改频率高，已拆分到 setAutoMatch）
        if 'minLevel' in settingsDict:
            self.minLevel = settingsDict['minLevel']
        if 'minScore' in settingsDict:
            self.minScore = settingsDict['minScore']
        if 'intro' in settingsDict:
            self.intro = settingsDict['intro']
        if 'autoEnter' in settingsDict:
            self.autoEnter = settingsDict['autoEnter']
        if 'password' in settingsDict:
            # isPublish 按 password 空否派生（空串=取消密码转公开队）；密码本体同步缓存
            self.password = settingsDict['password']
            self.isPublish = (settingsDict['password'] == '')

    def setAutoMatch(self, autoMatch):
        self.autoMatch = autoMatch

    def setMicsMode(self, micsMode):
        self.micsMode = micsMode

    def setMicBlock(self, gbId, blocked):
        if blocked:
            if gbId not in self.blockedMembers:
                self.blockedMembers.append(gbId)
        elif gbId in self.blockedMembers:
            self.blockedMembers.remove(gbId)

        # 成员 isBlockMics 字段与队伍级 blockedMembers 同源，同步更新保持全量一致
        _member = self.memberDict.get(gbId)
        if _member:
            _member.isBlockMics = blocked

    def setDeputy(self, deputyGbId):
        # 副团长（中心 setDeputy 任命/取消后经 onCrossTeamDeputyChange 推送落地；0=无副团长）
        self.deputyGbId = deputyGbId

    def applyMarkChange(self, changeType, markDict, onlyCaptainCanMark):
        # 队伍标记单条增量落地（中心 markChangePush 经 cell onCrossTeamMarkChange 到达）：
        # ADD 按槽位覆盖；DELETE 按槽位摘除；CAPTAIN 仅开关变更（markDict 为空表）。
        # onlyCaptainCanMark 始终携带中心当前值，顺带冗余校准
        self.teamMarkInfo['onlyCaptainCanMark'] = onlyCaptainCanMark
        if changeType == gameconst.TeamMarkChangeType.CAPTAIN or not markDict:
            return

        _key = 'sceneList' if markDict.get('type') == gameconst.TeamMarkType.MARK_SCENE else 'playerList'
        _markList = self.teamMarkInfo[_key]
        _idx = markDict.get('index', 0)
        if changeType == gameconst.TeamMarkChangeType.ADD:
            for _i, _old in enumerate(_markList):
                if _old.get('index') == _idx:
                    _markList[_i] = markDict
                    break
            else:
                _markList.append(markDict)
        elif changeType == gameconst.TeamMarkChangeType.DELETE:
            self.teamMarkInfo[_key] = [_m for _m in _markList if _m.get('index') != _idx]

    def updateMemberVoiceState(self, gbId, voiceDict):
        # 成员语音四态更新（onCrossTeamMemberVoiceState 独立推送落地）
        _member = self.memberDict.get(gbId)
        if not _member:
            return None

        for _key in ('enableMics', 'isBlockMics', 'enableSpeaker', 'inVoiceRoom'):
            if _key in voiceDict:
                setattr(_member, _key, voiceDict[_key])
        return _member

    def updateMemberState(self, gbId, stateDict):
        _member = self.memberDict.get(gbId)
        if _member:
            _member.updateState(stateDict)
        return _member

    def isInTeam(self, gbId):
        return gbId in self.memberDict

    def howManyMember(self):
        return len(self.memberDict)

    def isCaptain(self, gbId):
        return self.captainGbId == gbId

    def localMembers(self, serverId):
        # 本服成员迭代器
        for _memberVal in self.memberDict.values():
            if _memberVal.serverId == serverId:
                yield _memberVal

    def localGbIds(self, serverId):
        # 本服成员 gbId 迭代器
        for _memberVal in self.localMembers(serverId):
            yield _memberVal.gbId
