# coding: utf-8

from KBEDebug import *
import teamDunChallenge_config as TDC_CFG
import gameconst
import gameconfig



class IGuildCell(object):
    def syncModifyGuildInfo(self, attrDict):
        LOG_DBG('huyf: syncModifyGuildInfo', attrDict)
        if 'guildUUID' in attrDict:
            if self.guildUUID != attrDict['guildUUID']:
                self.guildUUID = attrDict['guildUUID']

        if 'guildName' in attrDict:
            if self.guildName != attrDict['guildName']:
                self.guildName = attrDict['guildName']

        if 'guildBox' in attrDict:
            self.guildBoxCell = attrDict['guildBox']

        if 'guildLevel' in attrDict:
            self.guildLevel = attrDict['guildLevel']
        
        if 'leagueUUID' in attrDict:
            self.leagueUUID = attrDict['leagueUUID']
            self.syncMethodCallToCrossServerCell('_syncLeagueUUID', (self.leagueUUID, ))

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
