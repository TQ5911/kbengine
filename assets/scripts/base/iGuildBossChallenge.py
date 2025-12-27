#coding: utf-8

from KBEDebug import *

import gamedecorator
import utils
import gameconst
import AuthClsWraper
import agent_agentFunction as A_AFD
import guildChallenge_basicInfo as GCBI
import guildChallenge_config as GCC
import gamePlay_gamePlay as GP_GP

class IGuildBossChallenge(object):
    def __init__(self):        
        pass
    
    def enterBossChallengeDungeon(self, openId):
        INFO_MSG('IGuildBossChallenge::enterBossChallengeDungeon:', openId)

        dungeoncfg = GCBI.datas.get(openId, None)
        if not dungeoncfg:
            WARNING_MSG('IGuildBossChallenge::enterBossChallengeDungeon: wrong dungeon cfg 1', openId)
            return
        
        dungeonNo = dungeoncfg['dunID']
        if not dungeonNo:
            WARNING_MSG('IGuildBossChallenge::enterBossChallengeDungeon: wrong dungeon cfg 2', openId)
            return
        
        currentScore = self.getTotalScore()
        # 检查战力
        needScore = dungeoncfg['minScore']
        if currentScore < needScore:
            self.client.onEnterGuildDungeon(gameconst.GuildChallengeOpenDungeonResult.NO_ENOUGH_SCORE, openId)
            WARNING_MSG('IGuildBossChallenge::enterBossChallengeDungeon: score is not enough', openId, currentScore, needScore)
            return
        
        extra = {}
        extra['name'] = self.characterName
        extra['school'] = self.getRoleCacheAttr('school', 0)
        extra['level'] = self.getRoleCacheAttr('level', 0)
        extra['sex'] = self.getRoleCacheAttr('sex', 0)
        extra['gbId'] = self.gbID
        extra['eId'] = self.id

        self.guildBox.enterBossChallengeDungeon(self.gbID, self, openId, extra)
