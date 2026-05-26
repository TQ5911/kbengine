# -*- encoding:utf-8 -*-

import KBEngine

import global_data
from KBEDebug import *
import Math
import random
import sys
import gzip
import json

sys.path.append('./scripts/common')
sys.path.append('./scripts/common/Lib')
sys.path.append('./scripts/server_common')

import global_data as GD
from collections import deque
import sMath
import utils
import formula
from AvatarBase import AvatarBase
# import skill_skill as SS
import tutorConst_newbieStep as TCNSD
import gameconst
from ai import botAI

mount_item_id = [30050078, 30050080, 30050090]


# --- RPC call statistics decorator for PlayerAvatar ---
import functools
import inspect


def _count_call(key: str):
    def _decorator(func):
        @functools.wraps(func)
        def _wrap(*args, **kwargs):
            try:
                stats = GD.rpc_call_statistics
                stats[key] = stats.get(key, 0) + 1
            except Exception:
                pass
            return func(*args, **kwargs)
        return _wrap
    return _decorator


def rpc_counted_class(cls):
    """Class decorator that wraps instance methods (including inherited).

    - Counts calls into GD.rpc_call_statistics using key: "<SubClass>.<method>"
    - Skips dunder, properties, staticmethod, classmethod.
    - Avoids double-wrapping if a name is already wrapped on the subclass.
    """
    seen = set()
    # Walk the MRO so we also include parent classes
    for base in cls.mro():
        if base is object:
            continue
        for name, attr in base.__dict__.items():
            if name in seen:
                continue
            if name.startswith('__') and name.endswith('__'):
                continue
            # Skip non-instance-method descriptors
            if isinstance(attr, (staticmethod, classmethod, property)):
                continue
            if inspect.isfunction(attr):
                # If subclass already defines a wrapper, keep it
                existing = cls.__dict__.get(name)
                if existing is not None and inspect.isfunction(existing) and existing is not attr:
                    seen.add(name)
                    continue
                setattr(cls, name, _count_call(f"{cls.__name__}.{name}")(attr))
                seen.add(name)
    return cls


class ModeDoing(object):
    MODE_INIT = 0
    MODE_MOVE = 1
    MODE_FIGHT = 2
    MODE_SEND_CHART = 3
    MODE_ALL = 4


class StreamStringVal(object):
    def __init__(self, id, dataTypeId, datasize, descr, dateType):
        self.id = id
        self.dataTypeId = dataTypeId
        self.datasize = datasize
        self.descr = descr
        self.dateType = dateType
        self.datas = bytes()

    def appendDatas(self, datas):
        self.datas += datas

    # def onStreamDataCompleted(self, owner):
    #     datas = gzip.decompress(self.datas)
    #     jsonData = json.loads(datas, encoding='utf-8')
    #     if self.dataTypeId == gameconst.StreamStringID.NORMAL_BAG_INFO:
    #         DEBUG_MSG("bagData", jsonData)


class Avatar(AvatarBase):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG("Avatar::__init__")
        self.streamStringDic = {}

    # def think(self, timer=0):
    #     KBEngine.addTimer(0, 3000, self.think)
    #     self.callDelegateMethod('think', ())

    def onEnterSpace(self):
        """
        KBEngine method.
        这个entity进入了一个新的space
        """
        DEBUG_MSG("%s::onEnterSpace: %i" % (self.__class__.__name__, self.id))

    def onLeaveSpace(self):
        """
        KBEngine method.
        这个entity将要离开当前space
        """
        DEBUG_MSG("%s::onLeaveSpace: %i" % (self.__class__.__name__, self.id))

    def onBecomePlayer(self):
        """
        KBEngine method.
        当这个entity被引擎定义为角色时被调用
        """
        DEBUG_MSG("%s::onBecomePlayer: %i" % (self.__class__.__name__, self.id))

    def update(self):
        pass

    ########## avatar.def ##########
    def onJump(self, *arg):
        pass

    def onGmCommandResult(self, *arg):
        pass

    def syncServerTime(self, *arg):
        pass

    def onAddTeleporterId(self, skillid):
        pass

    def onTeleport(self, *arg):
        pass

    ########## avatar.def end ##########
    def onBotMoveOver(self):
        pass

    def onGetMailList(self, mails):
        pass

    def onUpdateSkillBuilds(self, *args):
        pass

    def onGetBagData(self, *args):
        DEBUG_MSG("onGetBagData:", args)
        pass

    def onAddItems(self, *args):
        pass

    def onUseItems(self, *args):
        pass

    def onBagSort(self, *args):
        pass

    def onUnlockGrids(self, *args):
        pass

    def onDropItems(self, *args):
        pass

    def onGetAvailableTelIds(self, *args):
        pass

    def onGMNewbieFinished(self):
        DEBUG_MSG("avatar onGMNewbieFinished:")
        pass

    def onGetAvatarNewbieStep(self, *args):
        DEBUG_MSG("onGetAvatarNewbieStep")
        pass

    def sendChart(self):
        pass


class SkillCD(object):
    def __init__(self, skillId, *args):
        self.skillId = skillId

        self._nextRefresh = 0

    # @property
    # def cd(self):
    #     return SS.datas[self.skillId]['CD']
    #
    # @property
    # def gcd(self):
    #     return SS.datas[self.skillId]['globalCD']

    @property
    def refreshed(self):
        return utils.getNow() > self._nextRefresh

    def reset(self):
        self._nextRefresh = 0

    def useSkill(self):
        self._nextRefresh = utils.getNow() + self.cd


class PlayerAvatarSkillsCDMixin(object):
    def __init__(self):
        self.skillsCds = {}
        self._skillsCdsCache = {}

    def initSkillsCDs(self, skills: dict):
        for skill in skills:
            slotId = skill['slotId']
            if slotId == -1:
                continue

            if skill['skillId'] == 0:
                continue
            if slotId in self._skillsCdsCache:
                newSkillCD = self._skillsCdsCache[slotId]
            else:
                newSKillId = skill['skillId']
                newSkillCD = SkillCD(newSKillId)

            if slotId in self.skillsCds:
                cachedSkillCD = self.skillsCds[slotId]
                self._skillsCdsCache[cachedSkillCD.skillId] = cachedSkillCD

            self.skillsCds[slotId] = newSkillCD

    def setSkillCD(self, slotId):
        if slotId not in self.skillsCds:
            ERROR_MSG('can\'t find skill in cd dic')
            return

        self.skillsCds[slotId].useSkill()

    def isSkillReady(self, slotId):
        if slotId not in self.skillsCds:
            ERROR_MSG('can\'t find skill in cd dic')
            return

        return self.skillsCds[slotId].refreshed

    def isSkillInCD(self, slotId):
        return not self.isSkillReady(slotId)


@rpc_counted_class
class PlayerAvatar(Avatar, botAI.BotAI, PlayerAvatarSkillsCDMixin):
    # 帮战相关
    battleFieldDungeonMatchingBeginTime = 0
    taskingType = 0

    def __init__(self):
        super(PlayerAvatar, self).__init__()
        super(Avatar, self).__init__()
        super(botAI.BotAI, self).__init__()
        DEBUG_MSG("PlayerAvatar::__init__")
        
        self.spawnPosition = Math.Vector3(self.position)
        self.randomWalkRadius = 30.0

        self.dstPos = Math.Vector3(self.position)

        self.bagSortFlag = True
        self.bagAddFlag = True

        self.bt_tree = self.buildBtTree()
        self.createTreeDic(self.bt_tree)

        self.skills_cache = deque()
        self.selected_skills = {}
        self.bt_tree_timer = 0

    def callDelegateMethod(self, methodName, args):
        d = self.clientapp.getPlayerDelegate()
        if not d:
            return

        func = getattr(d, methodName, None)
        GD.rpc_call_statistics[methodName] = GD.rpc_call_statistics.get(methodName, 0) + 1
        func and func(*args)

    # def botOffLine(self):
    #     self.cell.offline(gameconst.AVATAR_OFFLINE_REASON_GMKICK)

    def onBecomePlayer(self):
        """
        KBEngine method.
        当这个entity被引擎定义为角色时被调用
        """
        DEBUG_MSG("%s::onBecomePlayer: %i" % (self.__class__.__name__, self.id))
        # 注意：由于PlayerAvatar是引擎底层强制由Avatar转换过来，__init__并不会再调用
        # 这里手动进行初始化一下
        self.__init__()
        GD.clientappid_map[self.gbId] = self.clientapp.id
        GD.monsters_map[self.clientapp.id] = {}
        if self.isDead():
            self.cell.relive(1)
        self.dressEquipNum = 0
        self.unLockSkill = False
        # self.base.getAvatarNewbieStep()
        self.pos_index = random.randint(0, 3)
        self.pos_type = 1
        self.mode = ModeDoing.MODE_INIT
        self.target_pos = self._getRandomPatrolPos()
        self.is_fight = False

        self.startRandomTeleport = False
        # self.clientapp.callback(1, self.offlineBot)

    def offlineBot(self):
        DEBUG_MSG("offlineBot:", self.gbId)
        if self.cell:
            self.cell.offline(self.id, gameconst.AVATAR_OFFLINE_REASON_MANNUALLY)

    def gmfinishNewbie(self):
        DEBUG_MSG("gmfinishNewbie ")
        self.base.runGmCommand('$botFinishNewbie 0')

    def onEntityEnterWorld(self):
        DEBUG_MSG('avatar onEntityEnterWorld')

    def onEnterWorld(self):
        DEBUG_MSG('avatar onEnterWorld', self.id, self.name, self.gbId)
        self.callDelegateMethod('onEnterWorld', ())

    def syncServerTime(self, *args):
        d = self.clientapp.getPlayerDelegate()
        if not d:
            return

        d.clientObj.updateTickTime()

    def onEnterSpace(self):
        """
        KBEngine method.
        这个entity进入了一个新的space
        """
        DEBUG_MSG("%s::onEnterSpace: %i   %i" % (self.__class__.__name__, self.id, self.spaceNo))
        # self.callDelegateMethod('onEnterSpace', ())

    def onLeaveSpace(self):
        """
        KBEngine method.
        这个entity将要离开当前space
        """
        DEBUG_MSG("%s::onLeaveSpace: %i   %i" % (self.__class__.__name__, self.id, self.spaceNo))
        # self.callDelegateMethod('onLeaveSpace', ())

    def update(self):
        self.callDelegateMethod('update', ())
        pass

    def _checkNearBy(self, targetPos, dstDis=3):
        dis = sMath.distance2D(self.position, targetPos)
        return dis <= dstDis

    def unLockAllSkillByGm(self):
        DEBUG_MSG("unLockAllSkillByGm  ````````````````")
        self.base.runGmCommand('$activeallmonster 0')

    def useSkill(self, targetId, targetPos):
        direct = targetPos - self.position
        direct.normalise()
        skill_values = list(self.selected_skills.values())
        if 0 == len(skill_values):
            WARNING_MSG('player no skill use')
            return

        skillId = 0
        for _slid, _skid in self.selected_skills.items():
            if _skid != 0 and self.isSkillReady(_slid):
                skillId = _skid
                skillSlot = _slid
                break
        if skillId == 0:
            WARNING_MSG('-------------- NO SKILL USE, ALL IN CD.', skillId)
            return

        DEBUG_MSG('in useSKill:', skillId, targetId, direct)
        dis = sMath.distance2D(self.position, targetPos)
        # skillRng = SS.datas[skillId]['range']
        skillRng = skillRng if skillRng > 1 else 1
        if dis < skillRng - 0.5:
            # self.cell.botMoveTo(targetPos)
            self.cell.botStopMove()
            self.cell.useTargetSkill(skillId, targetId, direct, 0)
            self.setSkillCD(skillSlot)
        else:
            DEBUG_MSG('cant use still, to far away, move to target')
            self.cell.botMoveTo(targetPos)
            skill_args = [skillId, targetId, direct, 0]
            self.skills_cache.append(skill_args)

    def onGetMailList(self, *args):
        DEBUG_MSG('onGetMailList:', args)

    def onUseItems(self, *args):
        DEBUG_MSG('onUseItems:', args)

    def onBagSort(self, *args):
        DEBUG_MSG('onBagSort:', args)

    def onUnlockGrids(self, *args):
        DEBUG_MSG('onUnlockGrids:', args)

    def onDead(self, arg0):
        if self.mode:
            self.cell.relive(2)
            self.clientapp.callback(2, self.tlCB)

    def tlCB(self):
        self.base.runGmCommand('$addbuff 0 64000069 1')
        self.cell.switchPKModel(0)
        self.target_pos = self._getRandomPatrolPos()
        DEBUG_MSG('坐标: (%s,%s,%s):', (self.position[0], self.position[1], self.position[2]))
        self.base.runGmCommand('$setpos 0 7727.796 212.4391 4618.375')

    def onUpdateSkills(self, skills):
        DEBUG_MSG('onUpdateSkills')
        self.skills = skills['skills']
        self.selected_skills = {}
        for skill in self.skills:
            slotId = skill['slotId']
            if slotId == -1:
                continue
            self.selected_skills[slotId] = skill['skillId']
        self.initSkillsCDs(self.skills)
        DEBUG_MSG('onUpdateSkills:', self.selected_skills)
        self.unLockSkill = True

    def onUpdateSkillBuilds(self, builds, *args):
        DEBUG_MSG('onUpdateSkillBuilds')
        builds = builds['builds']
        buildId = 0
        self.onUpdateSkills(builds[buildId])

    def onUpdatePeaceCdInfo(self, guildUUID, endTime, flag):
        DEBUG_MSG('onUpdatePeaceCdInfo')
        self.base.agreeGuildBattlePeaceRequest(guildUUID)

    def enterWorldLineFinishNew(self):
        DEBUG_MSG("enterWorldLineFinishNew  taskingType", self.taskingType)
        if self.taskingType > 0:
            return
        if not formula.spaceInWorldLine(self.spaceNo):
            self.cell.enterWorldLine()
            return

    def onStartBattleFieldDungeonMatchingOwner(self, arg0, arg1, arg2):
        DEBUG_MSG("onStartBattleFieldDungeonMatchingOwner", arg0, arg1, arg2)
        if not arg2:
            return
        self.battleFieldDungeonMatchingBeginTime = arg1
        # self.cell.confirmNotifyToStartBattleFieldDungeon(arg0, True)

    def notifyToStartBattleFieldDungeon(self, arg0, arg1):
        DEBUG_MSG("notifyToStartBattleFieldDungeon", arg0, arg1)
        self.cell.confirmNotifyToStartBattleFieldDungeon(arg0, True)
        self.taskingType = 1
        return

    def onLeaveBattleFieldDungeon(self):
        DEBUG_MSG("onLeaveBattleFieldDungeon", self.taskingType)
        self.taskingType = 0
        self.base.runGmCommand('$selfregbtfdun 0 %s ' % (6000))

    def onCompleteBattleFieldDungeon(self, arg0):
        DEBUG_MSG("onCompleteBattleFieldDungeon", self.taskingType, arg0)
        # self.taskingType = 0

    def startBattleFieldDungeon(self):
        self.taskingType = 0
        self.base.runGmCommand('$selfregbtfdun 0 %s ' % (6000))

    # ---------------------------------------------------------------------------------------

    def switchLine(self):
        k = random.randint(0, 9)
        self.base.runGmCommand('$switchline 0 %s' % k)

    def onGetAvatarNewbieStep(self, newbieStep):
        stepLimit = max(TCNSD.datas.keys())
        DEBUG_MSG("onGetAvatarNewbieStep", newbieStep, stepLimit)
        # 如果没完成新手任务
        # if newbieStep != stepLimit:
        #     self.clientapp.callback(60, self.gmfinishNewbie)
        # else:
        #     # self.cell.switchPKModel(0)
        #     # self.cell.stopAutoCombat()
        #
        #     if self.gbId not in GD.player_level_map:
        #         return
        #
        #     if GD.player_level_map[self.gbId] <= 13:
        #         self.botInit()

    def onBotMoveOver(self):
        DEBUG_MSG('in onBotMoveOver')
        if self.mode == ModeDoing.MODE_MOVE:
            self.cell.botMoveTo(self.getDisPostion())

        if self.mode == ModeDoing.MODE_FIGHT:
            if self.position[0] > 7400 and self.position[0] < 8000:
                self.cell.startAutoCombat(False)

        if self.mode == ModeDoing.MODE_ALL:
            # 轩辕城跑图的
            if self.position[0] > 6400 and self.position[0] < 7000:
                self.cell.botMoveTo(self.getDisPostion())

            # 大漩涡打架的
            if self.position[0] > 7400 and self.position[0] < 8000:
                self.cell.startAutoCombat(False)

        if len(self.skills_cache) > 0:
            skill = self.skills_cache.popleft()
            DEBUG_MSG('in onBotMoveOver, use skill:', skill)
            self.cell.useTargetSkill(*skill)

    def getDisPostion(self):
        dstPosList = []
        if self.pos_type == 2:
            dstPosList = [Math.Vector3(6578, 166.03, 4603), Math.Vector3(6650, 166.14, 4603),
                          Math.Vector3(6730.313, 166.09, 4603),
                          Math.Vector3(6650, 166.14, 4603)]
        self.pos_index += 1
        return dstPosList[(self.pos_index) % 4]

    # GM完成新手回调
    def onGMNewbieFinished(self):
        DEBUG_MSG("onGMNewbieFinished ")
        # self.botFinishNewbie()

    def botInit(self):
        pass
        # 清理背包
        # self.base.runGmCommand('$cleanbag 0 0')
        # 等级
        # self.base.runGmCommand('$setlv 0 %s' % str(50))
        # 获得大量的钱
        # self.base.runGmCommand('$addcoin 0 100000000')

    # 升级响应
    def onAvatarLevelUp(self, old_lv, new_lv):
        DEBUG_MSG('onAvatarLevelUp ---- oldlv: %s  newlv: %s' % (old_lv, new_lv))

    # 穿装备响应
    def onDressEquipment(self, arg0):
        DEBUG_MSG('onDressEquipment: %s' % arg0)

    # 获得灵兽信息
    def onUpdateLingShouData(self, arg0):
        DEBUG_MSG('onUpdateLingShouData: %s' % arg0)

    def beNotifiedApplyJoinRaid(self, raidUUID, joinedPlayerGBID, joinedPlayerProp):
        DEBUG_MSG('beNotifiedApplyJoinRaid:: %s %s %s' % (raidUUID, joinedPlayerGBID, joinedPlayerProp))
        self.cell.replyJoinRaid(joinedPlayerGBID, True)

    def onTeleport(self, *arg):
        DEBUG_MSG("onTeleport:: %s", *arg)
        DEBUG_MSG('------- pos: %s', self.position)

    def onRelive(self):
        DEBUG_MSG('onRelive-----')

    def _getRandomPatrolPos(self):

        randPos = [[7771, 7761, 4568, 4572], ]
        intdeRand = random.randint(0, len(randPos) - 1)

        minX = randPos[intdeRand][0]
        maxX = randPos[intdeRand][1]
        minY = randPos[intdeRand][2]
        maxY = randPos[intdeRand][3]
        x = round(random.uniform(minX, maxX), 1)
        y = round(random.uniform(minY, maxY), 1)
        return (x, 217, y)

    def sendChart(self):
        if self.mode != ModeDoing.MODE_SEND_CHART:
            return
        self.base.runGmCommand('$botSendChartOne 0 %s' % 2)
        self.clientapp.callback(random.randint(22, 30), self.sendChart)

    def fight(self):
        if self.cell.position[0] > 7400 and self.cell.position[0] < 8000:
            dis = sMath.distance2D(self.position, self.target_pos)
            if dis > 3:
                self.cell.botMoveTo(self.target_pos)

            else:
                self.cell.switchPKModel(self.id, gameconst.PKModel.ATTACK)
                self.cell.startAutoCombat(False)

        self.clientapp.callback(10, self.fight)

    def onGmCommandResult(self, arg0, arg1):
        if arg1 == '开始聊天':
            self.mode = ModeDoing.MODE_SEND_CHART
            self.clientapp.callback(10, self.sendChart)

        if arg1 == '停止聊天':
            self.mode = ModeDoing.MODE_INIT

        if arg1 == '开始战斗':
            self.mode = ModeDoing.MODE_FIGHT
            self.pos_type = 1
            self.base.runGmCommand('$botToPos 0 %s 0' % 1)
            self.clientapp.callback(1, self.fight)

        if arg1 == '停止战斗':
            self.mode = ModeDoing.MODE_INIT

        if arg1 == '开始跑图':
            self.mode = ModeDoing.MODE_MOVE
            self.pos_type = 2
            self.base.runGmCommand('$botToPos 0 %s 0' % 2)

        if arg1 == '停止跑图':
            self.mode = ModeDoing.MODE_INIT

    def onApplyInviteTeamMsg(self, srcTeamId, srcPlayerGbId, srcPlayerName, captainName):
        self.cell.replyInviteTeam(srcTeamId, srcPlayerGbId, True)

    def onStartBattleFieldDungeonMatchingTeam(self, arg0, arg1, arg2):
        if not arg2:
            return
        self.battleFieldDungeonMatchingBeginTime = arg1

    def onLoseConnection(self):
        INFO_MSG("onLoseConnection,gbId:%s" % self.gbId)
        d = self.clientapp.getPlayerDelegate()
        if d and hasattr(d, 'onLoseConnection'):
            self.callDelegateMethod('onLoseConnection', ())
            return
        self.reloginBaseapp()

    def onStreamDataStarted(self, id, dataTypeId, datasize, descr, dateType):
        DEBUG_MSG("onStreamDataStarted", id, dataTypeId, datasize, descr, dateType)
        if id in self.streamStringDic:
            ERROR_MSG("onStreamDataStarted id has in streamStringDic", id)
            return

        self.streamStringDic[id] = StreamStringVal(id, dataTypeId, datasize, descr, dateType)

    def onStreamDataRecv(self, id, datas):
        if id not in self.streamStringDic:
            ERROR_MSG("onStreamDataRecv id not in streamStringDic", id)
            return

        self.streamStringDic[id].appendDatas(datas)

    def onStreamDataCompleted(self, id):
        DEBUG_MSG("onStreamDataCompleted", id)
        if id not in self.streamStringDic:
            ERROR_MSG("onStreamDataCompleted id not in streamStringDic", id)
            return
        streamDataVal = self.streamStringDic.pop(id)
        datas = gzip.decompress(streamDataVal.datas)
        jsonData = json.loads(datas, encoding='utf-8')
        self.onGetStreamData(streamDataVal.dataTypeId, jsonData)

    def onGetStreamData(self, dataTypeId, jsonData):
        self.callDelegateMethod('onGetStreamData', (dataTypeId, jsonData))

    def onMessage(self, arg1, arg2):
        pass
        # self.callDelegateMethod('onMessage', (arg1, arg2))

    def onMoveOver(self, cid, userArg):
        self.callDelegateMethod('onMoveOver', (cid, userArg))

    def onMoveFailure(self, cid, userArg):
        self.callDelegateMethod('onMoveFailure', (cid, userArg))

    def set_transformId(self, *args):
        self.callDelegateMethod('set_transformId', (args,))

    def set_guildUUID(self, *args):
        DEBUG_MSG("set_guildUUID", args)
        self.callDelegateMethod('set_guildUUID', (args,))

    def set_duelAttr(self, *args):
        DEBUG_MSG("set_duelAttr", args)
        self.callDelegateMethod('set_duelAttr', (args,))

    def set_level(self, *args):
        DEBUG_MSG("set_level", args)
        self.callDelegateMethod('set_level', (args,))

    def randomTeleport(self):
        if not self.startRandomTeleport:
            self.startRandomTeleport = True
            self._doRandomTeleport()

    def _doRandomTeleport(self):
        if random.randrange(99) < 10:
            import NPC_teleporter as tel
            telid = random.choice(list(tel.datas.keys()))
            lineNo = -1
            DEBUG_MSG('_doRandomTeleport', telid, lineNo)
            self.cell.telToTeleporter(telid, lineNo)

        self.clientapp.callback(random.randint(0, 60), self._doRandomTeleport)

    def set_state(self, *args):
        self.callDelegateMethod('set_state', args)

    def set_spaceNo(self, *args):
        self.callDelegateMethod('set_spaceNo', args)

    # def onLoginQuestions(self, nextAId, lastStep, todayAus, refresh):
    #     print("onLoginQuestions", nextAId, lastStep, todayAus, refresh)
    #     if nextAId != -1:
    #         self.nextAId = nextAId
    #         self.base.reqAnswer(self.nextAId, random.choice([1, 2, 3, 4]))
    #     else:
    #         self.nextAId = None
    #
    # def onAnswer(self, rightAnswer, lastStep, nextAId, todayAus):
    #     print("onAnswer", rightAnswer, lastStep, nextAId, todayAus)
    #     if nextAId != -1:
    #         self.nextAId = nextAId
    #         self.base.reqAnswer(self.nextAId, random.choice([1, 2, 3, 4]))
    #     else:
    #         print("start update toplist")
    #         self.base.runGmCommand('$gmUploadTopList 0')
    #         self.nextAId = None

    # 任务相关

    def onTaskUpdate(self, taskVals):
        self.callDelegateMethod('onTaskUpdate', (taskVals,))

    # def onClaimTask(self, taskId, taskVals):
    #     self.callDelegateMethod('onClaimTask', (taskId, taskVals))
    #     print("onClaimTask ", taskId, taskVals)

    def onTasksRem(self, taskIds):
        self.callDelegateMethod('onTaskUpdate', (taskIds,))
