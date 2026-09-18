# coding: utf-8

from KBEDebug import *
import KBEngine
import teamDunChallenge_config as TDC_CFG
import gameconst
import gameconfig
import gameengine


class IGuildCell(object):
    def syncModifyGuildInfo(self, attrDict):
        LOG_DBG('syncModifyGuildInfo', attrDict)
        relationChanged = False
        if 'guildUUID' in attrDict:
            if self.guildUUID != attrDict['guildUUID']:
                self.guildUUID = attrDict['guildUUID']
                relationChanged = True
        if 'guildName' in attrDict:
            if self.guildName != attrDict['guildName']:
                self.guildName = attrDict['guildName']

        if 'guildBox' in attrDict:
            self.guildBoxCell = attrDict['guildBox']

        if 'guildLevel' in attrDict:
            self.guildLevel = attrDict['guildLevel']
        
        if 'leagueUUID' in attrDict:
            if self.leagueUUID != attrDict['leagueUUID']:
                self.leagueUUID = attrDict['leagueUUID']
                relationChanged = True

        if gameconfig.isCrossServer():
            self.base.onAfterSyncLeagueUUID(self.leagueUUID, self.guildUUID)
        else:
            self.syncMethodCallToCrossServerCell('syncModifyGuildInfo', (attrDict, ))

        if relationChanged:
            self._refreshPKTargetTypeCache()

    def _refreshPKTargetTypeCache(self):
        LOG_DBG('_refreshPKTargetTypeCache', self.guildUUID, self.leagueUUID)
        self.resetAllTargetTypeCache()
        self.changePKModeResetTargetId()
        for _eid in list(self.cacheSelfSet):
            _ent = KBEngine.entities.get(_eid)
            if _ent and hasattr(_ent, 'changePKModeResetTargetId'):
                _ent.changePKModeResetTargetId()

    def doFinishGuildDungeonTask(self):
        if not self.guildUUID:
            return

        self.base.completeGuildTask(
            gameconst.GuildTaskType.COMPLETEMAP, 
            TDC_CFG.datas['teamDunChallengeActID']['value'],
            1)
        
    def doKillMonster(self):
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerCell('_doKillMonster', ())
        else:
            self._doKillMonster()

    def _doKillMonster(self):
        if not self.guildUUID:
            return
        self.guildBoxCell.statGuildData(gameconst.GuildGamePlayType.WORLD_BOSS_KILLER)
