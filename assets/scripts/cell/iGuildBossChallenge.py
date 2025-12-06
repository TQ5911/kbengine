#coding: utf-8

from KBEDebug import *

import gamedecorator
import utils
import gameconst
import agent_agentFunction as A_AFD
import guildChallenge_basicInfo as GCBI
import guildChallenge_config as GCC
import gameengine
import complexTeleportOption
import formula

class IGuildBossChallenge(object):
    def __init__(self):        
        pass
    
    def isInGuildBossDungeon(self):
        return self.guildBossDungeonID > 0

    def setGuildBossDungeonID(self, dungeonID):
        INFO_MSG('setGuildBossDungeonID::', dungeonID)
        self.guildBossDungeonID = dungeonID

    def clearGuildBossDungeonID(self, dungeonNo):
        INFO_MSG('clearGuildBossDungeonID::', dungeonNo)
        self.guildBossDungeonID = 0

    def doEnterGuildBossDungeon(self, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        eContext = {'spaceUUID': spaceUUID,
                    'spaceBox': spaceBox,
                    'spaceMgrBox': spaceMgrBox,
                    'guildUUID': extra['guildUUID'],
                    'extra': extra}
        lContext = {}
        src = extra.get('src')
        context = {'e': eContext, 'l': lContext, 'src': src}
        options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.ENTER)
        INFO_MSG('doEnterGuildBossDungeon::', context)
        canLeave = self.packageComplexTeleportLeaveData(lContext)
        if not canLeave:
            return

        self.teleportFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

    def doLeaveGuildBossDungeon(self, extra):
        lContext = {'guildUUID': extra['guildUUID'],
                    'spaceMgrBox': self.spaceMgr.base,
                    'extra': extra}
        eContext = {}
        options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.LEAVE)
        context = {'e': eContext, 'l': lContext, 'src': 0}
        INFO_MSG('doLeaveGuildBossDungeon::', context)
        spaceType = self._getPrmBydungeonNo(formula.getDungeonNoBySpaceNo(self.spaceNo), 'type')
        _m_mapId, _m_outsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=spaceType)
        spaceNo = formula.getLineSpaceNo(_m_mapId)
        self.doLeaveFromSapceToSpace(self.spaceNo, spaceNo, options, context, spaceType=spaceType)

        
