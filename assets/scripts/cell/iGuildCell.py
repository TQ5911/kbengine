# coding: utf-8

from KBEDebug import *
import teamDunChallenge_config as TDC_CFG
import gameconst



class IGuildCell(object):
    def syncModifyGuildInfo(self, attrDict):
        DEBUG_MSG('huyf: syncModifyGuildInfo', attrDict)
        if 'guildUUID' in attrDict:
            if self.guildUUID != attrDict['guildUUID']:
                self.guildUUID = attrDict['guildUUID']

        if 'guildName' in attrDict:
            if self.guildName != attrDict['guildName']:
                self.guildName = attrDict['guildName']

        if 'guildBox' in attrDict:
            self.guildBoxCell = attrDict['guildBox']

    def doFinishGuildDungeonTask(self):
        if not self.guildUUID:
            return

        self.base.completeGuildTask(
            gameconst.GuildTaskType.COMPLETEMAP, 
            TDC_CFG.datas['teamDunChallengeActID']['value'],
            1)

