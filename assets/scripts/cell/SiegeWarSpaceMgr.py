import KBEngine
from KBEDebug import *
import formula, gameengine, iStaticSpaceMgr, utils, random, math, gametimer, iTimer
from gameconst import AchieveType
from gameconst import SiegeWarMonsterCustomId as siegeTp
from gameconst import SiegeWarMinimapDataType as SMDT
from gameconst import SiegeWarMonsterType as SMT
from gameconst import siegeWarMonsterEnumDict as siegeTpInt
from gameconst import siegeWarMiniMapNeedSync as smNeedSync
from gameconst import SiegeWarGameState
from gameconst import ChatChannel
import utils
import gametimer
import cityBattle_config as CBC
import time
import json
import sMath
import copy
import guildAuthorization_authorization as GA_AD
import guildAuthorization_authorizationID_def as GA_AI_DD
import CoreAreaFlag
import message_Message as MM
import buff
import buff_buff as BBD

startEGText = ""
for i in GA_AD.authorization2Job[GA_AI_DD.datas.cityBattleSiegeEnginesStart]:
    if startEGText == "":
        startEGText += GA_AD.datas[int(i)]["name"]
    else:
        startEGText += ","
        startEGText += GA_AD.datas[int(i)]["name"]

siegeWarScoreListQueueSize = 30
miniMapSyncMinTime = 5

#城战配置物
siegeWarConfig = {
    siegeTp.SIEGE_BOSS: {
        'siegeWarCamp': 1
    },
    siegeTp.MAIN_GATE: {
        'siegeWarCamp': 2
    },
    siegeTp.ORDER_GATE: {
        'siegeWarCamp': 2
    },
    siegeTp.BOW: {
        'siegeWarCamp': 2
    },
}

#城战器械kv
siegeWarQiXieLevel = {
    siegeTp.MAIN_GATE: 1,
    siegeTp.ORDER_GATE: 2,
    siegeTp.REINFORCE: 3,
    siegeTp.SIEGE_BOSS: 4,
    siegeTp.BOW: 5,
}

siegeWarGateTips = {
    11: 'cityBattle_gateTips1',
    12: 'cityBattle_gateTips2',
    21: 'cityBattle_gateTips3',
    22: 'cityBattle_gateTips4',
}

siegeWarGateTipArgs = {
    11: SMT.MAIN_GATE,
    12: SMT.MAIN_GATE,
    21: SMT.ORDER_GATE,
    22: SMT.ORDER_GATE,
}

#战魂创生物
class SiegeWarCreation:
    ATTACK_CREATION = 66000086
    DEFEND_CREATION = 66000087
    RECOVER_CREATION = 66000088

#战魂list
siegeWarCreationList = [
    SiegeWarCreation.ATTACK_CREATION,
    SiegeWarCreation.DEFEND_CREATION,
    SiegeWarCreation.RECOVER_CREATION,
]

#战魂buff
class SiegeWarBuff:
    ATTACK_BUFF = 64000097
    DEFEND_BUFF = 64000098
    RECOVER_BUFF = 64000099
    WUSHUANG_BUFF = 64000100

#todo读表
class SiegeWarScoreVal:
    SCORE_KILL = CBC.datas['cityBattle_pointObtain']['value'][0]
    SCORE_SIEGE_BOSS = CBC.datas['cityBattle_pointObtain']['value'][1]
    SCORE_MAIN_GATE = CBC.datas['cityBattle_pointObtain']['value'][2]
    SCORE_ORDER_GATE = CBC.datas['cityBattle_pointObtain']['value'][3]
    SCORE_REINFORCE = CBC.datas['cityBattle_pointObtain']['value'][4]
    SCORE_BOW = CBC.datas['cityBattle_pointObtain']['value'][5]
    SCORE_ENTER = 0

class SiegeWarScore:
    def __init__(self, gbId, school, name, scoreList):
        self.gbId = gbId
        self.school = school
        self.name = name
        self.killScore = scoreList[0]
        self.destroyScore = scoreList[1]
        self.totalScore = self.killScore + self.destroyScore

    def getData(self):
        return {
            'school': self.school,
            'name': self.name,
            'killScore': self.killScore,
            'destroyScore': self.destroyScore
        }

    def addScore(self, v, tp):
        if tp == 0:
            self.killScore += v
        elif tp == 1:
            self.destroyScore += v
        self.totalScore = self.killScore + self.destroyScore

class SiegeWarSpaceMgr(iStaticSpaceMgr.IStaticSpaceMgr):

    def __init__(self):
        iStaticSpaceMgr.IStaticSpaceMgr.__init__(self)
        INFO_MSG("SiegeWarSpaceMgr __init__")

        self.siegewarEntityDict = {}
        self.siegewarBowDict = {}
        self.siegewarTeleporterDict = {}
        self.offenseNum = 0
        self.defenseNum = 0
        self.spaceInvoked = False
        self.coreAreaFlag = None
        self.lastBuffCreateTime = 0
        self.lastMiniMapSyncTime = 0
        self.buffCreationDict = {}
        self._resetSiegeWarState({})

        self.pyAddTimer(1, 1, gametimer.SIEGE_WAR_SPACE_TICK)
        gameengine.getGlobalBase("SiegeWarSpaceStub").onSpaceMgrReady(self.spaceNo, self)

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.SIEGE_WAR_SPACE_TICK:
            self._onSiegeWarSpaceTick()
        else:
            if userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
                self._onDatetimeTimerTick()
            else:
                self._onTimer(tid, userArg)

    def _onSiegeWarSpaceTick(self):
        if not self.spaceInvoked:
            return

        self.checkSiegeBossPos()
        self.checkSpecialMonsterHpChange()
        if self.minimapChanged:
            if utils.getNow() >= self.lastMiniMapSyncTime + miniMapSyncMinTime or self.minimapNeedSyncImmediate:
                jsonData = json.dumps(self.minimapChangedData)
                DEBUG_MSG("[lj]sync minimapInfo:", jsonData)
                self.syncPlayer(lambda playerEnt: playerEnt.onSiegeWarMinimapInfoUpdate(jsonData))
                self.minimapChanged = False
                self.minimapNeedSyncImmediate = False
                self.minimapChangedData = {}
                self.lastMiniMapSyncTime = utils.getNow()

        if self.siegeWarState == SiegeWarGameState.SIEGE_WAR_STATE_PREPARE:
            if utils.getNow() >= self.officalStartTime:
                DEBUG_MSG("[lj]siegeWarState: ", self.siegeWarState, "->", SiegeWarGameState.SIEGE_WAR_STATE_BATTLE)
                self.siegeWarState = SiegeWarGameState.SIEGE_WAR_STATE_BATTLE
                gameengine.getGlobalBase("SiegeWarSpaceStub").onSiegeWarGameStateChange(self.siegeWarState, 0)

                #攻守方空气墙删除
                if siegeTp.ATTACK_AIRWALL in self.siegewarEntityDict:
                    self.siegewarEntityDict[siegeTp.ATTACK_AIRWALL].safeDestroy()
                    self.siegewarEntityDict.pop(siegeTp.ATTACK_AIRWALL)
                    DEBUG_MSG("[lj]remove: ATTACK_AIRWALL")
                removeList = []
                for customID in self.siegewarEntityDict:
                    if customID.startswith(siegeTp.DEFEND_AIRWALL):
                        removeList.append(customID)
                for customID in removeList:
                    self.siegewarEntityDict[customID].safeDestroy()
                    self.siegewarEntityDict.pop(customID)
                    DEBUG_MSG("[lj]remove: DEFEND_AIRWALL", customID)
        if self.siegeWarState == SiegeWarGameState.SIEGE_WAR_STATE_BATTLE:
            #战魂buff
            if utils.getNow() >= self.lastBuffCreateTime + CBC.datas['cityBattle_buffNumsRefreshGap']['value'] * 60:
                self.recreateBuffCreation()

            #结算
            if utils.getNow() >= self.officalEndTime:
                self.coreAreaOffenseCnt = self.coreAreaFlag.offenseNum
                self.coreAreaDefenseCnt = self.coreAreaFlag.defenseNum

                DEBUG_MSG("[lj]updateCoreArea: ", self.coreAreaOffenseCnt, self.coreAreaDefenseCnt)
                self.winnerCamp = self.getWinnerCamp()
                self.loserCamp = 1 if self.winnerCamp == 2 else 2
                self.winnerGuildUUID = self.offenseGuildUUID if self.winnerCamp == 1 else self.defenseGuildUUID
                self.loserGuildUUID = self.defenseGuildUUID if self.winnerCamp == 1 else self.offenseGuildUUID
                DEBUG_MSG("[lj]siegeWarState: ", self.siegeWarState, "->", SiegeWarGameState.SIEGE_WAR_STATE_BATTLE_END_AND_HAS_LOSER, "winnerCamp: ", self.winnerCamp, "loserCamp: ", self.loserCamp)
                self.siegeWarState = SiegeWarGameState.SIEGE_WAR_STATE_BATTLE_END_AND_HAS_LOSER
                gameengine.getGlobalBase("SiegeWarSpaceStub").onSiegeWarGameStateChange(self.siegeWarState, self.winnerCamp)
                #发奖励
                self.handleSiegeWarReward()

                #弹战报
                offenseArr = {
                    'coreAreaNum': self.coreAreaOffenseCnt,
                    'scoreList': self._getSiegeWarScoreData(1),
                }
                defenseArr = {
                    'coreAreaNum': self.coreAreaDefenseCnt,
                    'scoreList': self._getSiegeWarScoreData(2),
                }
                dataArray = [
                    offenseArr,
                    defenseArr,
                ]
                self.dataArray = copy.deepcopy(dataArray)
                DEBUG_MSG("[lj]siegeWar dataArray", self.winnerGuildUUID, self.loserGuildUUID, self.winnerCamp, self.mvpName, self.mvpSchool, self.dataArray)
                #结算后不能攻击
                for playerId in self.players.values():
                    playerEnt = KBEngine.entities.get(playerId)
                    if playerEnt:
                        playerEnt.siegeWarCanAttack = 0

        if self.siegeWarState == SiegeWarGameState.SIEGE_WAR_STATE_BATTLE_END_AND_HAS_LOSER:
            if utils.getNow() >= self.kickLoserTime:
                DEBUG_MSG("[lj]siegeWarState: ", self.siegeWarState, "->", SiegeWarGameState.SIEGE_WAR_STATE_BATTLE_END_AND_NO_LOSER)
                self.siegeWarState = SiegeWarGameState.SIEGE_WAR_STATE_BATTLE_END_AND_NO_LOSER
                gameengine.getGlobalBase("SiegeWarSpaceStub").onSiegeWarGameStateChange(self.siegeWarState, 0)

                self.syncPlayer(lambda playerEnt: playerEnt.onSiegeWarKickout() if playerEnt.siegeWarCamp == self.loserCamp else None)
        if self.siegeWarState == SiegeWarGameState.SIEGE_WAR_STATE_BATTLE_END_AND_NO_LOSER:
            if utils.getNow() >= self.closeTime:
                DEBUG_MSG("[lj]siegeWarState: ", self.siegeWarState, "->", SiegeWarGameState.SIEGE_WAR_STATE_END)
                self.siegeWarState = SiegeWarGameState.SIEGE_WAR_STATE_END
                gameengine.getGlobalBase("SiegeWarSpaceStub").onSiegeWarGameStateChange(self.siegeWarState, 0)
                self.syncPlayer(lambda playerEnt: playerEnt.onSiegeWarKickout())
                self.spaceInvoked = False

    def onGetWinnerDataFromCityOwnerMgr(self, dataList):
        DEBUG_MSG("[lj]SiegeWarSpaceMgr onGetWinnerDataFromCityOwnerMgr", dataList)
        self.cityOwnerId = dataList[0]
        self.cityOwnerName = dataList[1]
        self.cityOwnerSchool = dataList[6]
        self.cityOwnerSex = dataList[7]
        self.syncPlayer(lambda playerEnt: playerEnt.onSiegeWarBattleEnd(self.winnerGuildUUID, self.winnerCamp, self.mvpName, self.mvpSchool, self.dataArray,
                                                                        self.cityOwnerId, self.cityOwnerName, self.cityOwnerSchool, self.cityOwnerSex))

    def handleSiegeWarReward(self):
        self.handleSiegeWarMvp()
        #todo
        combatResult = []
        for camp in (1, 2):
            for scoreData in self.siegeWarscoreList[camp]:
                combatResult.append({
                    'gbId': scoreData.gbId,
                    'isMvp': scoreData.gbId == self.mvpGbId,
                    'score': scoreData.totalScore,
                    'isWinner': camp == self.winnerCamp,
                })

        gameengine.getGlobalBase("CrossSiegeWarStub").onCrossSiegeWarEnd(combatResult, self.winnerGuildUUID, self.loserGuildUUID)

    def handleSiegeWarMvp(self):
        if len(self.siegeWarscoreList[1]) > 0:
            self.mvpGbId = self.siegeWarscoreList[1][0].gbId
            self.mvpName = self.siegeWarscoreList[1][0].name
            self.mvpSchool = self.siegeWarscoreList[1][0].school
        if len(self.siegeWarscoreList[2]) > 0:
            if len(self.siegeWarscoreList[1]) == 0 or self.siegeWarscoreList[2][0].totalScore > self.siegeWarscoreList[1][0].totalScore:
                self.mvpGbId = self.siegeWarscoreList[2][0].gbId
                self.mvpName = self.siegeWarscoreList[2][0].name
                self.mvpSchool = self.siegeWarscoreList[2][0].school
        #todo 发reward

    def getWinnerCamp(self):
        #如果防守方没有帮会，则进攻方获胜
        if self.defenseGuildUUID == 0 and self.coreAreaOffenseCnt == 0 and self.coreAreaDefenseCnt == 0:
            DEBUG_MSG("[lj]getWinnerCamp: defenseGuildUUID is 0, offenseCnt is 0, defenseCnt is 0, return 1")
            return 1

        if self.coreAreaOffenseCnt > self.coreAreaDefenseCnt:
            return 1
        return 2

    def initStaticSpace(self):
        pass

    def recreateBuffCreation(self):
        self.lastBuffCreateTime = utils.getNow()
        for ent in self.buffCreationDict.values():
            ent.destroySelf()
        self.buffCreationDict.clear()
        cnt = min(CBC.datas['cityBattle_buffNumsOneTime']['value'], len(CBC.datas['cityBattle_buffPosition']['value']))
        numbers = random.sample(range(0, len(CBC.datas['cityBattle_buffPosition']['value'])), cnt)
        DEBUG_MSG("[lj]recreateBuffCreation: numbers", numbers)
        for i in numbers:
            pos = CBC.datas['cityBattle_buffPosition']['value'][i]
            creationId = random.choice(siegeWarCreationList)
            props = {'creationId': creationId,
                    'spaceNo': self.spaceNo,
                    'siegeWarCamp': 0,
                    'spaceMgrId': self.id,
                    }
            ent = KBEngine.createEntity('Creation', self.spaceID, [pos[0], pos[1], pos[2]], [0, 0, 0], props)
            DEBUG_MSG("[lj]resetSiegeWarState: createCreation", ent.id)
            self.buffCreationDict[ent.id] = ent

        #弹msg
        if self.isFirstBuffCreate:
            self.isFirstBuffCreate = False
            self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_buffFirstRefreshMsg']['value']), []))
            self.syncPlayer(lambda playerEnt: playerEnt.base.onRecvChannelMsg(ChatChannel.SIEGE_WAR, utils.buildChatChannelAvatarInfo(0, 0, 1, '', 1, 0, 0), MM.datas[CBC.datas['cityBattle_buffFirstRefreshMsg']['value']]['Message']))
        else:
            self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_buffRefreshMsg']['value']), []))
            self.syncPlayer(lambda playerEnt: playerEnt.base.onRecvChannelMsg(ChatChannel.SIEGE_WAR, utils.buildChatChannelAvatarInfo(0, 0, 1, '', 1, 0, 0), MM.datas[CBC.datas['cityBattle_buffRefreshMsg']['value']]['Message']))

    def onAvatarGetBuffCreation(self, creationId, avatar, buffId):
        if not avatar.IsAvatar:
            DEBUG_MSG("[lj]onAvatarGetBuffCreation: target is not avatar", avatar)
            return

        DEBUG_MSG("[lj]onAvatarGetBuffCreation", creationId, avatar.id, buffId)
        if creationId in self.buffCreationDict:
            creation = self.buffCreationDict.pop(creationId)
            creation.destroySelf()
            avatarCampStr = str(avatar.siegeWarCamp)

            #无双buff相关
            if buffId in CBC.datas['cityBattle_campbuffActivate']['value']:
                self.campWushuangBuffCnt[avatar.siegeWarCamp] = self.campWushuangBuffCnt.get(avatar.siegeWarCamp, 0) + 1
                # x/10战报
                msgArg4 = str(self.campWushuangBuffCnt[avatar.siegeWarCamp]) + "/" + str(CBC.datas['cityBattle_campBuffDemand']['value'])
                msg = MM.datas[CBC.datas['cityBattle_buffObtainMsg']['value']]['Message'].format(avatar.name, buff.Buff.getBuffName(buffId), avatarCampStr, msgArg4)
                self.syncPlayer(lambda playerEnt: playerEnt.base.onRecvChannelMsg(ChatChannel.SIEGE_WAR, utils.buildChatChannelAvatarInfo(0, 0, 1, '', 1, 0, 0), msg))
                #无双
                if self.campWushuangBuffCnt[avatar.siegeWarCamp] >= CBC.datas['cityBattle_campBuffDemand']['value']:
                    for playerId in self.players.values():
                        playerEnt = KBEngine.entities.get(playerId)
                        if playerEnt and playerEnt.siegeWarCamp == avatar.siegeWarCamp:
                            playerEnt.addBuff(SiegeWarBuff.WUSHUANG_BUFF, 1, playerEnt.id)
                            self.buffCacheDict.setdefault(playerEnt.gbId, {})
                            self.buffCacheDict[playerEnt.gbId][SiegeWarBuff.WUSHUANG_BUFF] = utils.getNow()
                    #激活无双buff
                    self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_campBuffMsg']['value']), [avatarCampStr, avatarCampStr, buff.Buff.getBuffName(SiegeWarBuff.WUSHUANG_BUFF)]))
                    msg = MM.datas[CBC.datas['cityBattle_campBuffMsg']['value']]['Message'].format(avatarCampStr, avatarCampStr, buff.Buff.getBuffName(SiegeWarBuff.WUSHUANG_BUFF))
                    self.syncPlayer(lambda playerEnt: playerEnt.base.onRecvChannelMsg(ChatChannel.SIEGE_WAR, utils.buildChatChannelAvatarInfo(0, 0, 1, '', 1, 0, 0), msg))
                    self.campWushuangBuffCnt[avatar.siegeWarCamp] = 0

            #buff效果
            avatar.addBuff(buffId, 1, avatar.id)
            self.buffCacheDict.setdefault(avatar.gbId, {})
            self.buffCacheDict[avatar.gbId][buffId] = utils.getNow()
        else:
            WARNING_MSG("[lj]onAvatarGetBuffCreation: creationId not in self.buffCreationDict", creationId, avatar.id, buffId)

    #todo帮会数据同步
    def resetSiegeWarState(self, guildDict):
        self.spaceInvoked = True
        self._resetSiegeWarState(guildDict)

    def _resetSiegeWarState(self, guildDict):
        self.lastMinimapSiegeBossPos = None
        self.reinforceCamp = 0
        self.mainGateDestroyed = False
        self.siegeWarBossInvoked = False
        self.revivePosDict = {}
        self.coreAreaOffenseCnt = 0
        self.coreAreaDefenseCnt = 0
        self.minimapInfo = {}
        self.minimapChanged = False
        self.minimapNeedSyncImmediate = False
        self.minimapChangedData = {}
        self.siegeWarMinimapSignal = {}
        self.siegeWarScoreData = {}
        self.siegeWarscoreList = {1: [], 2: []}
        self.mvpGbId = 0
        self.mvpName = "testMvpName"
        self.mvpSchool = 1
        self.offenseTeleporter = None
        self.cityOwnerId = 0
        self.cityOwnerName = ""
        self.cityOwnerSchool = 0
        self.cityOwnerSex = 0
        self.bowAliveCnt = 0
        self.campWushuangBuffCnt = {}
        self.isFirstBuffCreate = True
        self.offensiveJunXuQiXieLevelData = guildDict.get('offensiveJunXuQiXieLevelData', {})
        self.defensiveJunXuQiXieLevelData = guildDict.get('defensiveJunXuQiXieLevelData', {})
        self.buffCacheDict = {}

        x = CBC.datas['cityBattle_coreArea']['value'][0][0]
        z = CBC.datas['cityBattle_coreArea']['value'][0][1]

        if self.coreAreaFlag:
            self.coreAreaFlag.destroySelf()
        params = {
            'position': [x, 0, z],
            'direction': [0, 0, 0],
            'spaceNo': self.spaceNo,
        }
        self.coreAreaFlag = KBEngine.createEntity('CoreAreaFlag', self.spaceID, [x, 0, z], [0, 0, 0], params)

        if self.offenseNum != 0 or self.defenseNum != 0:
            WARNING_MSG("[lj]resetSiegeWarState: self.offenseNum or self.defenseNum is not 0", self.offenseNum, self.defenseNum)

        self.offenseNum = 0
        self.defenseNum = 0


        self.offenseGuildUUID = guildDict.get('offenseGuildUUID', 0)
        self.defenseGuildUUID = guildDict.get('defenseGuildUUID', 0)
        DEBUG_MSG("[lj]resetSiegeWarState: self.offenseGuildUUID, self.defenseGuildUUID", self.offenseGuildUUID, self.defenseGuildUUID)

        self.startTime = guildDict.get('sceneOpenTime', utils.getNow())
        self.officalStartTime = self.startTime + CBC.datas['cityBattle_prepareTime']['value'] * 60
        self.officalEndTime = self.officalStartTime + CBC.datas['cityBattle_fightTime']['value'] * 60
        self.kickLoserTime = self.officalEndTime + CBC.datas['cityBattle_lastTime2']['value'] * 60
        self.closeTime = self.officalEndTime + CBC.datas['cityBattle_lastTime']['value'] * 60
        self.lastBuffCreateTime = self.officalStartTime + CBC.datas['cityBattle_buffFirstRefresh']['value'] * 60 - CBC.datas['cityBattle_buffNumsRefreshGap']['value'] * 60
        self.siegeWarState = SiegeWarGameState.SIEGE_WAR_STATE_PREPARE
        gameengine.getGlobalBase("SiegeWarSpaceStub").onSiegeWarGameStateChange(self.siegeWarState, 0)
        self.winnerCamp = 0
        self.loserCamp = 0
        self.dataArray = []

        DEBUG_MSG("[lj]resetSiegeWarState: self.startTime, self.officalStartTime, self.officalEndTime, self.closeTime",
                  time.strftime("%Y.%m.%d-%H.%M.%S", time.localtime(self.startTime)),
                  time.strftime("%Y.%m.%d-%H.%M.%S", time.localtime(self.officalStartTime)),
                  time.strftime("%Y.%m.%d-%H.%M.%S", time.localtime(self.officalEndTime)),
                  time.strftime("%Y.%m.%d-%H.%M.%S", time.localtime(self.kickLoserTime)),
                  time.strftime("%Y.%m.%d-%H.%M.%S", time.localtime(self.closeTime)))


        _mapId = formula.getMapId(self.spaceNo)
        _dunData = utils.getDunStructureModuleData(_mapId)
        if not _dunData:
            ERROR_MSG("[lj]resetSiegeWarState: _dunData is None")
            return

        for i in (siegeTp.GATE_REBORN, siegeTp.ATTACK_REBORN, siegeTp.DEFEND_REBORN):
            if i in _dunData:
                for _data in _dunData[i].values():
                    self.revivePosDict[i] = (_data['PosX'], _data['PosY'], _data['PosZ'])

        DEBUG_MSG("[lj]resetSiegeWarState: self.revivePosDict", self.revivePosDict)

    def onMinimapInfoUpdate(self, entId, monsterType, dataType, data):
        self.minimapInfo.setdefault(entId, {SMDT.TYPE: monsterType})
        self.minimapInfo[entId][dataType] = data
        self.minimapChanged = True
        self.minimapChangedData.setdefault(entId, {})
        self.minimapChangedData[entId][dataType] = data

        DEBUG_MSG("[lj]onMinimapInfoUpdate", self.minimapInfo)

    #器械等级
    def getSiegeWarMonsterLevel(self, ent):
        lv = 1
        customId, gid = utils.getCustomIdAndGid(self.spaceNo, ent.gameEntityId)
        if customId is None:
            return lv
        if customId in siegeWarQiXieLevel:
            siegeWarCamp = 0
            if customId in siegeWarConfig:
                siegeWarCamp = siegeWarConfig[customId]['siegeWarCamp']
            if customId == siegeTp.REINFORCE:
                siegeWarCamp = self.reinforceCamp
            tp = siegeWarQiXieLevel[customId]
            if siegeWarCamp == 1:
                return self.offensiveJunXuQiXieLevelData.get(tp, 1)
            elif siegeWarCamp == 2:
                return self.defensiveJunXuQiXieLevelData.get(tp, 1)
        return lv

    def addEntity(self, entId, tags):
        super(SiegeWarSpaceMgr, self).addEntity(entId, tags)

        ent = KBEngine.entities.get(entId)
        if ent:
            DEBUG_MSG("[lj]addEntity", ent.className)

            if ent.className == 'CityBattleTeleporter':
                cbID = ent.cbID
                if cbID in self.siegewarTeleporterDict:
                    self.siegewarTeleporterDict[cbID].safeDestroy()
                self.siegewarTeleporterDict[cbID] = ent
                if ent.CBTelType == 2:
                    self.offenseTeleporter = ent
                return

            if not hasattr(ent, 'gameEntityId'):
                return

            customId, gid = utils.getCustomIdAndGid(self.spaceNo, ent.gameEntityId)
            if customId is None:
                DEBUG_MSG("[lj]addEntity: customId is None", ent.className, ent.gameEntityId)
                return

            #采集物必须没有刷新时间！！！！！！！！！！！！不然会一直循环创建，这里检查一下
            if ent.className == 'Collection':
                if ent.refreshTime != 0:
                    WARNING_MSG("[lj]addEntity: SiegeWar Collection refreshTime is not 0", ent.gameEntityId)
                    ent.refreshTime = 0

            #删除重复
            if customId == siegeTp.BOW:
                if gid in self.siegewarBowDict:
                    self.siegewarBowDict[gid].safeDestroy()
                    self.siegewarBowDict.pop(gid)
                self.siegewarBowDict[gid] = ent
                self.bowAliveCnt += 1
                DEBUG_MSG("[lj]addEntity: bowAliveCnt", self.bowAliveCnt)
            else:
                if customId in self.siegewarEntityDict:
                    self.siegewarEntityDict[customId].safeDestroy()
                self.siegewarEntityDict[customId] = ent


            #攻城兽出生无敌
            if customId == siegeTp.SIEGE_BOSS:
                ent.addBuff(64000070, 1, ent.id)

            #设置camp
            if customId in siegeWarConfig:
                ent.siegeWarCamp = siegeWarConfig[customId]['siegeWarCamp']

            #重生物
            if customId == siegeTp.REINFORCE:
                self.minimapNeedSyncImmediate = True
                ent.siegeWarCamp = self.reinforceCamp

            #minimap
            if customId in siegeTpInt:
                tpInt = siegeTpInt[customId]
                if tpInt in smNeedSync:
                    self.onMinimapInfoUpdate(entId, tpInt, SMDT.TYPE, tpInt)
                    self.onMinimapInfoUpdate(entId, tpInt, SMDT.HP, 1.0)
                    self.onMinimapInfoUpdate(entId, tpInt, SMDT.POS, [round(ent.position[0], 2), round(ent.position[1], 2), round(ent.position[2], 2)])
                    self.onMinimapInfoUpdate(entId, tpInt, SMDT.CAMP, ent.siegeWarCamp)
                    self.onMinimapInfoUpdate(entId, tpInt, SMDT.CONFIG_ID, int(gid))

    def syncMinimapInfoToPlayer(self, playerId):
        playerEnt = KBEngine.entities.get(playerId)
        if playerEnt:
            jsonData = json.dumps(self.minimapInfo)
            DEBUG_MSG("[lj]sync minimapInfo when player enter:", playerId, jsonData, self.minimapInfo)
            playerEnt.onSiegeWarMinimapInfoUpdate(jsonData)

    def syncSiegeWarMinimapSignalToPlayer(self, playerId):
        playerEnt = KBEngine.entities.get(playerId)
        if playerEnt:
            camp = playerEnt.siegeWarCamp
            arr = []
            if camp in self.siegeWarMinimapSignal:
                for tp, data in self.siegeWarMinimapSignal[camp].items():
                    arr.append({
                        'tp': tp,
                        'isAdd': True,
                        'text': data[0],
                        'pos': data[1]
                    })
            playerEnt.onSiegeWarMinimapSignalChange(arr)

    def syncSiegeWarEnterDataToPlayer(self, playerId):
        playerEnt = KBEngine.entities.get(playerId)
        if playerEnt:
            playerEnt.onSiegeWarEnterDataUpdate(self.offenseGuildUUID, self.defenseGuildUUID, self.startTime)

    def onPlayerRelogin(self, box, playerGbId):
        playerId = box.id
        self.syncMinimapInfoToPlayer(playerId)
        self.syncSiegeWarMinimapSignalToPlayer(playerId)
        self.syncSiegeWarEnterDataToPlayer(playerId)
        DEBUG_MSG("[lj]sync siegewar data to player when player relogin", playerId)

    def onPlayerEnter(self, playerId):
        self.syncMinimapInfoToPlayer(playerId)
        self.syncSiegeWarMinimapSignalToPlayer(playerId)
        self.syncSiegeWarEnterDataToPlayer(playerId)
        playerEnt = KBEngine.entities.get(playerId)
        playerEnt.siegeWarCanAttack = 1
        if playerId not in self.players:
            if playerEnt.siegeWarCamp == 1:
                self.offenseNum += 1
            elif playerEnt.siegeWarCamp == 2:
                self.defenseNum += 1

        if playerEnt.gbId in self.buffCacheDict:
            for buffId, time in self.buffCacheDict[playerEnt.gbId].items():
                remainTime = BBD.datas[buffId]['endByTime'] - (utils.getNow() - time)
                if remainTime > 0:
                    playerEnt.addBuff(buffId, 1, playerEnt.id, duration = remainTime)
        else:
            WARNING_MSG("[lj]onPlayerEnter: playerId is already in self.players", playerId)
        super(SiegeWarSpaceMgr, self).onPlayerEnter(playerId)
        #确保进入排行榜
        self.onPlayerScoreChange(playerEnt, SiegeWarScoreVal.SCORE_ENTER, 0)

        #城战结束时，玩家进入通知结算数据
        if self.siegeWarState == SiegeWarGameState.SIEGE_WAR_STATE_BATTLE_END_AND_HAS_LOSER or self.siegeWarState == SiegeWarGameState.SIEGE_WAR_STATE_BATTLE_END_AND_NO_LOSER:
            playerEnt.onSiegeWarBattleEnd(self.winnerGuildUUID, self.winnerCamp, self.mvpName, self.mvpSchool, self.dataArray,
                                          self.cityOwnerId, self.cityOwnerName, self.cityOwnerSchool, self.cityOwnerSex)
            DEBUG_MSG("[lj]onPlayerEnter: playerEnt.onSiegeWarBattleEnd", self.winnerGuildUUID, self.winnerCamp, self.mvpName, self.mvpSchool, self.dataArray)

        INFO_MSG('onPlayerEnter', playerId, 'offenseNum', self.offenseNum, 'defenseNum', self.defenseNum)

    def onPlayerLeave(self, playerGbId, playerId, box):
        if self.offenseTeleporter:
            self.offenseTeleporter.onPlayerLeave(playerGbId)
        else:
            WARNING_MSG("[lj]onPlayerLeave: self.offenseTeleporter is None", playerGbId, playerId)
        playerEnt = KBEngine.entities.get(playerId)
        if playerId in self.players:
            if playerEnt.siegeWarCamp == 1:
                self.offenseNum -= 1
            elif playerEnt.siegeWarCamp == 2:
                self.defenseNum -= 1
        else:
            WARNING_MSG("[lj]onPlayerLeave: playerId is not in self.players", playerId)
        super(SiegeWarSpaceMgr, self).onPlayerLeave(playerGbId, playerId, box)
        INFO_MSG('onPlayerLeave', playerId, 'offenseNum', self.offenseNum, 'defenseNum', self.defenseNum)

    def onPlayerRelive(self, box, playerGbId):
        super(SiegeWarSpaceMgr, self).onPlayerRelive(box, playerGbId)
        if self.coreAreaFlag:
            avatarCell = KBEngine.entities.get(box.id)
            if avatarCell:
                self.coreAreaFlag.onPlayerRelive(avatarCell)
            else:
                WARNING_MSG("[lj]onPlayerRelive: avatarCell is None", playerGbId)
        else:
            WARNING_MSG("[lj]onPlayerRelive: self.coreAreaFlag is None", playerGbId)
        if self.offenseTeleporter:
            self.offenseTeleporter.onPlayerRelive(playerGbId)
        else:
            WARNING_MSG("[lj]onPlayerRelive: self.offenseTeleporter is None", playerGbId)
        DEBUG_MSG("[lj]onPlayerRelive", playerGbId)

    def onPlayerDead(self, box, playerGbId):
        super(SiegeWarSpaceMgr, self).onPlayerDead(box, playerGbId)
        if self.coreAreaFlag:
            avatarCell = KBEngine.entities.get(box.id)
            if avatarCell:
                self.coreAreaFlag.onPlayerDead(avatarCell)
            else:
                WARNING_MSG("[lj]onPlayerDead: avatarCell is None", playerGbId)
        else:
            WARNING_MSG("[lj]onPlayerDead: self.coreAreaFlag is None", playerGbId)

    def onPlayerOffline(self, playerId, playerGbId):
        super(SiegeWarSpaceMgr, self).onPlayerOffline(playerId, playerGbId)
        if self.offenseTeleporter:
            self.offenseTeleporter.onPlayerOffline(playerGbId)
        else:
            WARNING_MSG("[lj]onPlayerOffline: self.offenseTeleporter is None", playerGbId)
        DEBUG_MSG("[lj]onPlayerOffline", playerGbId)

    def onSiegeWarMonsterDead(self, gameEntityId, killer):
        killer = utils.getHostEntity(killer)
        DEBUG_MSG("[lj]onSiegeWarMonsterDead", gameEntityId, killer)
        if not killer:
            DEBUG_MSG("[lj]onSiegeWarMonsterDead: killer is None", gameEntityId)
            return

        customId, gid = utils.getCustomIdAndGid(self.spaceNo, gameEntityId)
        if not customId:
            DEBUG_MSG("[lj]onSiegeWarMonsterDead: customId is None", gameEntityId)
            return

        if customId == siegeTp.REINFORCE:
            msgArg1 = CBC.datas['cityBattle_attack']['value'] if killer.siegeWarCamp == 1 else CBC.datas['cityBattle_defend']['value']
            self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_occupyTips2']['value']), [msgArg1]))
            self.reinforceCamp = killer.siegeWarCamp
            self.onPlayerScoreChange(killer, SiegeWarScoreVal.SCORE_REINFORCE, 1)
        elif customId == siegeTp.MAIN_GATE:
            self.mainGateDestroyed = True
            if siegeTp.GATE_AIRWALL in self.siegewarEntityDict:
                self.siegewarEntityDict[siegeTp.GATE_AIRWALL].safeDestroy()
                self.siegewarEntityDict.pop(siegeTp.GATE_AIRWALL)
            self._callback(0.1, 'siegeWarBossDelayDestroy', (), gametimer.TIMER_TAG_SIEGE_BOSS_DELAY_DESTROY)
            self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_occupyTips1']['value']), []))
            self.onPlayerScoreChange(killer, SiegeWarScoreVal.SCORE_MAIN_GATE, 1)
        elif customId == siegeTp.ORDER_GATE:
            if siegeTp.ORDER_GATE_AIRWALL in self.siegewarEntityDict:
                self.siegewarEntityDict[siegeTp.ORDER_GATE_AIRWALL].safeDestroy()
                self.siegewarEntityDict.pop(siegeTp.ORDER_GATE_AIRWALL)
            self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_destroyGate2']['value']), []))
            self.onPlayerScoreChange(killer, SiegeWarScoreVal.SCORE_ORDER_GATE, 1)
        elif customId == siegeTp.SIEGE_BOSS:
            self.onPlayerScoreChange(killer, SiegeWarScoreVal.SCORE_SIEGE_BOSS, 1)
        elif customId == siegeTp.BOW:
            self.onPlayerScoreChange(killer, SiegeWarScoreVal.SCORE_BOW, 1)
            self.bowAliveCnt -= 1
            DEBUG_MSG("[lj]onSiegeWarMonsterDead: bowAliveCnt", self.bowAliveCnt)
            if self.bowAliveCnt == 0:
                self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_breakAllBallista']['value']), []))
            else:
                self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_breakBallista']['value']), [killer.name]))
        if customId in self.siegewarEntityDict:
            self.siegewarEntityDict.pop(customId)

        self.minimapNeedSyncImmediate = True

    def siegeWarBossDelayDestroy(self):
        DEBUG_MSG("[lj]start siegeWarBossDelayDestroy")
        if siegeTp.SIEGE_BOSS in self.siegewarEntityDict:
            self.onMinimapInfoUpdate(self.siegewarEntityDict[siegeTp.SIEGE_BOSS].id, SMT.SIEGE_BOSS, SMDT.HP, 0.0)
            self.siegewarEntityDict[siegeTp.SIEGE_BOSS].safeDestroy()
            self.siegewarEntityDict.pop(siegeTp.SIEGE_BOSS)
            DEBUG_MSG("[lj]safeDestroy siegeWarBoss over")

    def onSiegeWarOpenGate(self, src):
        DEBUG_MSG("[lj]onSiegeWarOpenGate", src)
        if siegeTp.ORDER_GATE in self.siegewarEntityDict:
            self.onSiegeWarMonsterHpChange(self.siegewarEntityDict[siegeTp.ORDER_GATE].id, SMT.ORDER_GATE, 0.0)
            self.siegewarEntityDict[siegeTp.ORDER_GATE].safeDestroy()
            self.siegewarEntityDict.pop(siegeTp.ORDER_GATE)
            self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_openSwitch']['value']), [src.name]))
            self.onPlayerScoreChange(src, SiegeWarScoreVal.SCORE_ORDER_GATE, 1)
        if siegeTp.ORDER_GATE_AIRWALL in self.siegewarEntityDict:
            self.siegewarEntityDict[siegeTp.ORDER_GATE_AIRWALL].safeDestroy()
            self.siegewarEntityDict.pop(siegeTp.ORDER_GATE_AIRWALL)

    def siegeWarPrecheckCollection(self, src, collectionId):
        if collectionId == 16000046:
            if src.siegeWarCamp == 1:
                if siegeTp.ORDER_GATE in self.siegewarEntityDict:
                    return True
                else:
                    src.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_alreadyOpen']['value']), [])
                    return False
        elif collectionId == 16000047:
            if src.siegeWarCamp == 1:
                if not src.siegeWarGuildCache.get('startEG', False):
                    src.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_noPermission3']['value']), [startEGText])
                    return False
                else:
                    openMinute = CBC.datas['cityBattle_siegeEnginesTime']['value']
                    canOpenTime = self.officalStartTime + openMinute * 60
                    if utils.getNow() < canOpenTime:
                        src.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_siegeEngines']['value']), [str(openMinute)])
                        return False
                    return True
            else:
                src.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_siegeEnginesPermission']['value']), [])
                return False
        return False

    def getSiegeWarBoss(self):
        if not self.siegeWarBossInvoked:
            return None
        if siegeTp.SIEGE_BOSS in self.siegewarEntityDict:
            return self.siegewarEntityDict[siegeTp.SIEGE_BOSS]

    def checkSiegeBossPos(self):
        if not self.siegeWarBossInvoked:
            return
        if siegeTp.SIEGE_BOSS in self.siegewarEntityDict:
            posNow = self.siegewarEntityDict[siegeTp.SIEGE_BOSS].position
            posNow = [posNow[0], posNow[1], posNow[2]]
            if self.lastMinimapSiegeBossPos is None:
                self.lastMinimapSiegeBossPos = posNow
            if sMath.distance2DToCompareFrom3DPosition(self.lastMinimapSiegeBossPos, posNow) > 1:
                self.onMinimapInfoUpdate(self.siegewarEntityDict[siegeTp.SIEGE_BOSS].id, SMT.SIEGE_BOSS, SMDT.POS, [round(posNow[0], 2), round(posNow[1], 2), round(posNow[2], 2)])
                self.lastMinimapSiegeBossPos = posNow

    #小地图波纹特效需要更高频的同步(hp有变化时5s一次广播)
    def checkSpecialMonsterHpChange(self):
        checkType = [siegeTp.MAIN_GATE, siegeTp.SIEGE_BOSS]
        for monsterType in checkType:
            if monsterType in self.siegewarEntityDict:
                entId = self.siegewarEntityDict[monsterType].id
                if entId in self.minimapInfo and SMDT.HP in self.minimapInfo[entId]:
                    lastHpPercent = self.minimapInfo[entId][SMDT.HP]
                    hpPercent = round(self.siegewarEntityDict[monsterType].hp / self.siegewarEntityDict[monsterType].fullHp, 4)
                    if hpPercent < lastHpPercent:
                        DEBUG_MSG("[lj]checkSpecialMonsterHpChange: hpPercent < lastHpPercent", entId, monsterType, hpPercent, lastHpPercent)
                        self.onMinimapInfoUpdate(entId, monsterType, SMDT.HP, hpPercent)

    def getSiegeWarMainGate(self):
        if siegeTp.MAIN_GATE in self.siegewarEntityDict:
            return self.siegewarEntityDict[siegeTp.MAIN_GATE]
        return None

    def onSiegeWarInvokeBoss(self, src):
        DEBUG_MSG("[lj]onSiegeWarInvokeBoss", src)
        if siegeTp.SIEGE_BOSS in self.siegewarEntityDict:
            if siegeTp.MAIN_GATE in self.siegewarEntityDict:
                self.siegewarEntityDict[siegeTp.SIEGE_BOSS].removeBuff(64000070)
                self.siegewarEntityDict[siegeTp.SIEGE_BOSS].isSiegeWarBossInvoked = True
                self.siegewarEntityDict[siegeTp.SIEGE_BOSS].siegeWarBossTargetPos = self.siegewarEntityDict[siegeTp.MAIN_GATE].position
                self.siegeWarBossInvoked = True
                self.onMinimapInfoUpdate(self.siegewarEntityDict[siegeTp.SIEGE_BOSS].id, SMT.SIEGE_BOSS, SMDT.INVOKED, 1)
                self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getNeedTranslateMsgId(CBC.datas['cityBattle_siegeEnginesStart']['value']), []))

    def getSiegeWarRebornPos(self, src):
        DEBUG_MSG("[lj]getSiegeWarRebornPos", src)

        if src.siegeWarCamp == 1:
            return self.revivePosDict[siegeTp.ATTACK_REBORN], 0
        elif src.siegeWarCamp == 2:
            return (self.revivePosDict[siegeTp.GATE_REBORN], 0) if not self.mainGateDestroyed else (self.revivePosDict[siegeTp.DEFEND_REBORN], 0)
        else:
            ERROR_MSG("[lj]getSiegeWarRebornPos: src.siegeWarCamp is not 1 or 2", src.siegeWarCamp)
            return self.revivePosDict[siegeTp.ATTACK_REBORN], 0

    def onSiegeWarGateModifyHPMsg(self, gateType, msgType):
        DEBUG_MSG("[lj]onSiegeWarGateModifyHPMsg", gateType, msgType)
        tipCode = gateType * 10 + msgType
        tp = siegeWarGateTips[tipCode]
        args = str(siegeWarGateTipArgs[tipCode])
        self.syncPlayer(lambda playerEnt: playerEnt.showMsg(utils.getNeedTranslateMsgId(CBC.datas[tp]['value']), [args, ]))

    #城战物件每损失5%hp会触发一次，用于minimap同步
    def onSiegeWarMonsterHpChange(self, entId, monsterType, hpPercent):
        if monsterType in smNeedSync:
            hpPercent = round(hpPercent, 4)
            self.onMinimapInfoUpdate(entId, monsterType, SMDT.HP, hpPercent)

    def onSiegeWarMinimapSignalChange(self, tp, isAdd, text, pos, camp):
        self.siegeWarMinimapSignal.setdefault(camp, {})
        if isAdd:
            self.siegeWarMinimapSignal[camp][tp] = [text, pos]
            self.syncPlayer(lambda playerEnt: playerEnt.onSiegeWarMinimapSignalChange([{
                'tp': tp,
                'isAdd': isAdd,
                'text': text,
                'pos': pos
            }]) if playerEnt.siegeWarCamp == camp else None)
            DEBUG_MSG("[lj]onSiegeWarMinimapSignalChange: tp, isAdd, text, pos, camp", tp, isAdd, text, pos, camp)
        else:
            if tp in self.siegeWarMinimapSignal[camp]:
                self.siegeWarMinimapSignal[camp].pop(tp)
                self.syncPlayer(lambda playerEnt: playerEnt.onSiegeWarMinimapSignalChange([{
                    'tp': tp,
                    'isAdd': isAdd,
                    'text': text,
                    'pos': pos
                }]) if playerEnt.siegeWarCamp == camp else None)
                DEBUG_MSG("[lj]onSiegeWarMinimapSignalChange: tp, isAdd, text, pos, camp", tp, isAdd, text, pos, camp)
            else:
                WARNING_MSG("[lj]onSiegeWarMinimapSignalChange: tp is not in self.siegeWarMinimapSignal[camp]", tp, text, isAdd, pos, camp)

    def onPlayerScoreChange(self, src, val, scoreTp):
        if not src.IsAvatar:
            DEBUG_MSG("[lj]onPlayerScoreChange: src is not Avatar", src)
            return

        playerGBID = src.gbId
        camp = src.siegeWarCamp
        school = src.school
        name = src.name

        needAppend = False if playerGBID in self.siegeWarScoreData else True
        scoreObj = self.siegeWarScoreData.get(playerGBID, SiegeWarScore(src.gbId, school, name, [0, 0]))
        scoreObj.addScore(val, scoreTp)
        self.siegeWarScoreData[playerGBID] = scoreObj
        if needAppend:
            self.siegeWarscoreList[camp].append(scoreObj)

        DEBUG_MSG("[lj]onPlayerScoreChange: scoreObj", scoreObj.getData(), self.siegeWarscoreList[camp])

    def _getSiegeWarScoreData(self, camp):
        if camp not in self.siegeWarscoreList:
            WARNING_MSG("[lj]getSiegeWarScoreData: camp is not in self.siegeWarscoreList", camp)
            return []
        self.siegeWarscoreList[camp].sort(key=lambda x: x.totalScore, reverse=True)
        res = []
        for obj in self.siegeWarscoreList[camp][:siegeWarScoreListQueueSize]:
            res.append(obj.getData())
        return res

    def getSiegeWarScoreData(self, player, camp):
        res = self._getSiegeWarScoreData(camp)

        playerData = self.siegeWarScoreData.get(player.gbId, SiegeWarScore(player.gbId, player.school, player.name, [0, 0]))
        return res, playerData.getData()

    def onSiegeWarPlayerDead(self, src, killer):
        killer = utils.getHostEntity(killer)
        if not killer:
            DEBUG_MSG("[lj]onSiegeWarPlayerDead: killer is None", src)
            return

        if killer.IsAvatar and src.IsAvatar:
            if killer.siegeWarCamp != src.siegeWarCamp:
                DEBUG_MSG("[lj]onSiegeWarPlayerDead: src, killer", src, killer, src.name, killer.name)
                self.onPlayerScoreChange(killer, SiegeWarScoreVal.SCORE_KILL, 0)
                if killer.isCrossServerInOtherServer:
                     killer.base.syncMethodCallToLocalServerBase(
                         'triggerAchievement',
                         (AchieveType.SIEGE_KILL,)
                     )
                else:
                    killer.triggerAchievement(AchieveType.SIEGE_KILL)

    def checkCanEnterCell(self, camp, box, args):
        limitNum = 0
        if camp == 1:
            limitNum = CBC.datas['cityBattle_attackNumber']['value']
            if self.reinforceCamp == 1:
                limitNum += CBC.datas['cityBattle_increasePeople']['value']
            if self.offenseNum < limitNum:
                box.onCheckCanEnterCell(True, 0, args)
                return
        elif camp == 2:
            limitNum = CBC.datas['cityBattle_defendNumber']['value']
            if self.defenseNum < limitNum:
                box.onCheckCanEnterCell(True, 0, args)
                return

        box.onCheckCanEnterCell(False, limitNum, args)

    ################################# gm #################################
    def onGmAddTime(self, minutes):
        self.officalStartTime -= minutes * 60
        self.officalEndTime -= minutes * 60
        self.kickLoserTime -= minutes * 60
        self.closeTime -= minutes * 60
        self.lastBuffCreateTime -= minutes * 60

        DEBUG_MSG("[lj]battle fast forward", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.officalStartTime)),
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.officalEndTime)),
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.kickLoserTime)),
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.closeTime)))

    #玩家分数依次设置为0,100,200,300...
    def onGmTestScores(self):
        DEBUG_MSG("[lj]onGmTestScores")
        score = 0
        for playerId in self.players:
            playerEnt = KBEngine.entities.get(playerId)
            if playerEnt:
                self.onPlayerScoreChange(playerEnt, score, 0)
                score += 100

