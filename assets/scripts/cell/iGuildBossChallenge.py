#coding: utf-8

from KBEDebug import *
import datetime
import gamedecorator
import utils
import gameconst
import guildChallenge_basicInfo as GCBI
import guildChallenge_config as GCC
import gamePlay_gamePlay as GP_GP
import complexTeleportOption
import formula

class IGuildBossChallenge(object):
    def __init__(self):        
        pass
    
    def isInGuildBossDungeon(self):
        return self.guildBossDungeonID > 0

    def setGuildBossDungeonID(self, dungeonID):
        LOG_INFO('setGuildBossDungeonID::', dungeonID)
        self.guildBossDungeonID = dungeonID

    def clearGuildBossDungeonID(self, dungeonNo):
        LOG_INFO('clearGuildBossDungeonID::', dungeonNo)
        self.guildBossDungeonID = 0

    def doEnterGuildBossDungeon(self, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        eCtx = {'spaceUUID': spaceUUID,
                    'spaceBox': spaceBox,
                    'spaceMgrBox': spaceMgrBox,
                    'guildUUID': extra['guildUUID'],
                    'extra': extra}
        lCtx = {}
        src = extra.get('src')
        context = {'e': eCtx, 'l': lCtx, 'src': src}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.ENTER)
        LOG_INFO('doEnterGuildBossDungeon::', context)
        canLeave = self.packComplexTeleportLeaveData(lCtx)
        if not canLeave:
            return

        self.telFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

    def doLeaveGuildBossDungeon(self, extra):
        lCtx = {'guildUUID': extra['guildUUID'],
                    'spaceMgrBox': self.spaceMgr.base,
                    'extra': extra}
        eCtx = {}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.LEAVE)
        context = {'e': eCtx, 'l': lCtx, 'src': 0}
        LOG_INFO('doLeaveGuildBossDungeon::', context)
        spaceType = self._getParamBydungeonNo(formula.parseDungeonNoBySpaceNo(self.spaceNo), 'type')
        _, _mOutsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=spaceType)
        spaceNo = _mOutsideRecord.spaceNo if _mOutsideRecord else formula.combineLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)
        self.doLeaveFromSapceToSpace(self.spaceNo, spaceNo, options, context, spaceType=spaceType)

    def checkGuildBossChallengeCond(self):
        if not self.guildUUID:
            LOG_WARN('IGuildBossChallenge::checkGuildBossChallengeCond: guild uuid is none')
            return False

        if not self.guildBoxCell:
            LOG_WARN('IGuildBossChallenge::checkGuildBossChallengeCond: guild box is none')
            return False
        
        return True
    
    def getGuildBossChallengeDungeonId(self, openId):
        cfg = GCBI.datas.get(openId, None)
        if not cfg:
            LOG_WARN('IGuildBossChallenge::getGuildBossChallengeDungeonId: wrong opened id', openId)
            return None
        
        dungeonID = cfg['dunID']
        if not GP_GP.datas.get(dungeonID, None):
            LOG_WARN('IGuildBossChallenge::getGuildBossChallengeDungeonId: wrong gameplay dungeon cfg', openId)
            return None
        return dungeonID
    
    @gamedecorator.checkGameconfigEnable('guildBossChallenge')
    @gamedecorator.limitcall(1)
    def openGuildDungeon(self, exposed, openTime, openType, openId):
        LOG_INFO('IGuildBossChallenge::openGuildDungeon:', exposed, openTime, openType, openId)
        if not self.checkGuildBossChallengeCond():
            return
        
        if openType not in gameconst.GuildChallengeDungeonOpenType.VALID_TYPE:
            LOG_WARN('IGuildBossChallenge::openGuildDungeon: wrong opened type', exposed, openType, openId)
            return
        
        dungeonID = self.getGuildBossChallengeDungeonId(openId)
        if not dungeonID:
            return
        
        guildChallengeCfgID = GCBI.dungeonIdxDic.get(dungeonID, None)
        if not guildChallengeCfgID:
            LOG_WARN('IGuildBossChallenge::openGuildDungeon: wrong dungeon id', exposed, openType, dungeonID)
            return
        
        # 检查是否可以预约
        now = utils.curTS()
        frontTime, _ = utils.nextByCronTupleList(GCC.datas['timeNotScheduledFront']['value'])
        laterTime, _ = utils.nextByCronTupleList(GCC.datas['timeNotScheduledLater']['value'])
        resetTime, _ = utils.nextByCronTupleList(GCC.datas['guildChallengeResetTime']['value'])
        # 1.未正确配置，不可开启
        if not frontTime or not laterTime or not resetTime:
            LOG_WARN('IGuildBossChallenge::openGuildDungeon: not in time range 0', exposed, openType, openId)
            self.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NOT_VALID_TIME, openType, openId)
            return
        
        frontTime += now
        laterTime += now
        resetTime += now
        # 预约开启
        if openType == gameconst.GuildChallengeDungeonOpenType.APPOINT:
            # 3.跨周期不可预约
            if openTime >= resetTime:
                LOG_WARN('IGuildBossChallenge::openGuildDungeon: not in time range 2', exposed, openType, openId)
                self.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NOT_VALID_TIME, openType, openId)
                return
            # 4.每日重置点不可预约
            if openTime >= frontTime and openTime <= laterTime:
                LOG_WARN('IGuildBossChallenge::openGuildDungeon: not in time range 4', exposed, openType, openId)
                self.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NOT_VALID_TIME, openType, openId)
                return
            # 计算下一个预约时间点
            # 后退时间
            backTime = int(GCC.datas['timeScheduledAhead']['value'])
            # 找到下一个半个整点
            curHalfTime = utils.getNextHoursTimestamp(now)
            openHalfTime = utils.getNextHoursTimestamp(openTime)
            # 5.不满足后退时间不可预期
            if openHalfTime - curHalfTime < backTime:
                LOG_WARN('IGuildBossChallenge::openGuildDungeon: not in time range 5', exposed, openType, openId)
                self.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NOT_VALID_TIME, openType, openId)
                return
            
            openTime = openHalfTime
        # 直接开启
        else:
            # 2.每日重置区间不可以开启
            if frontTime >= laterTime:
                LOG_WARN('IGuildBossChallenge::openGuildDungeon: not in time range 1', exposed, openType, openId)
                self.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NOT_VALID_TIME, openType, openId)
                return
            
            if now >= frontTime and now <= laterTime:
                LOG_WARN('IGuildBossChallenge::openGuildDungeon: not in time range 6', exposed, openType, openId)
                self.client.onOpenGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NOT_VALID_TIME, openType, openId)
                return
            
            openTime = now

        self.guildBoxCell.openGuildChallenge(self.gbId, self.base, openType, openId, openTime)

    @gamedecorator.checkGameconfigEnable('guildBossChallenge')
    @gamedecorator.limitcall(1)
    def getChangllengeDataInfo(self, exposed):
        LOG_INFO('IGuildBossChallenge::getChangllengeDataInfo:', exposed)
        if not self.checkGuildBossChallengeCond():
            return
        
        self.guildBoxCell.getChangllengeDataInfo(self.gbId, self.base)

    @gamedecorator.checkGameconfigEnable('guildBossChallenge')
    @gamedecorator.limitcall(1)
    def cancelGuildDungeonOrder(self, exposed, openId):
        LOG_INFO('IGuildBossChallenge::cancelGuildDungeonOrder:', exposed, openId)
        if not self.checkGuildBossChallengeCond():
            return
        
        dungeonID = self.getGuildBossChallengeDungeonId(openId)
        if not dungeonID:
            return
        
        self.guildBoxCell.cancelGuildDungeonOrder(self.gbId, self.base, openId)

    @gamedecorator.checkGameconfigEnable('guildBossChallenge')
    @gamedecorator.limitcall(1)
    def enterBossChallengeDungeon(self, exposed, openId):
        LOG_INFO('IGuildBossChallenge::enterBossChallengeDungeon:', exposed, openId)
        if not self.checkGuildBossChallengeCond():
            return
        
        dungeonNo = self.getGuildBossChallengeDungeonId(openId)
        if not dungeonNo:
            return
        
        if not utils.checkCanChangeSceneAndShowMsg(self, self.spaceNo, dungeonNo) or not self.canDoCompleteTeleport(noErrorMsg=True):
            return
        
        self.base.enterBossChallengeDungeon(openId)
        
    @gamedecorator.checkGameconfigEnable('guildBossChallenge')
    @gamedecorator.limitcall(1)
    def leaveBossChallengeDungeon(self, exposed, openId):
        LOG_INFO('IGuildBossChallenge::leaveBossChallengeDungeon:', exposed, openId)
        if not self.checkGuildBossChallengeCond():
            return
        
        dungeonID = self.getGuildBossChallengeDungeonId(openId)
        if not dungeonID:
            return
        
        self.guildBoxCell.leaveBossChallengeDungeon(self.gbId, self.base, openId)

    @gamedecorator.checkGameconfigEnable('guildBossChallenge')
    @gamedecorator.limitcall(1)
    def getGuildBossHP(self, exposed, openId):
        LOG_DBG('IGuildBossChallenge::getGuildBossHP:', exposed, openId)
        if not self.checkGuildBossChallengeCond():
            return
        
        dungeonID = self.getGuildBossChallengeDungeonId(openId)
        if not dungeonID:
            return
        
        self.guildBoxCell.getGuildBossHP(self.gbId, self.base, openId)
    
