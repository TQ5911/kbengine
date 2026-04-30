# coding: utf-8

from KBEDebug import *
import KBEngine

import gameconst
import dataUtils
import LogTrackingMgr
import json
import utils
import sMath
import formula
from BountyInfo import bountyItem
import gamePlay_gamePlay as GPGPD
import gameglobal
import gameengine
import const_const as CONST

class IBounty(object):
    def __init__(self):
        DEBUG_MSG("IBounty::__init__")
        self.cellPreyInfo = None
        self.cellHunterInfo = None
        self.hunterDamageSet = set()

    def setPreyInfo(self, preyDict):
        INFO_MSG("IBounty::setPreyInfo1", preyDict)
        preyItem = bountyItem()
        preyItem.initFromSyncDict(preyDict)
        self.preyFlag = preyItem.flag
        if preyItem.state in gameconst.BountyState.INVALID_CELL_SET_PREY_TYPE:
            DEBUG_MSG("IBounty::setPreyInfo set none", self.cellPreyInfo)
            preyItem = None
        self.cellPreyInfo = preyItem
        INFO_MSG("IBounty::setPreyInfo2", self.cellPreyInfo)

    def updatePreyBuff(self, flag):
        INFO_MSG("IBounty::updatePreyBuff", flag)
        if flag == gameconst.UpdatePreyBuffFlag.ADD:
            self.addBuff(CONST.datas["Bounty_LoserDebuff"]["value"], 1, self.id)
        elif flag == gameconst.UpdatePreyBuffFlag.REMOVE:
            self.removeBuff(CONST.datas["Bounty_LoserDebuff"]["value"])

    def setHunterInfo(self, hunterDict, flag):
        INFO_MSG("IBounty::setHunterInfo1", hunterDict)
        hunterItem = bountyItem()
        hunterItem.initFromSyncDict(hunterDict)
        self.updateHunterBuff(flag)
        if hunterItem.state in gameconst.BountyState.INVALID_CELL_SET_HUNTER_TYPE:
            DEBUG_MSG("IBounty::setHunterInfo set none", self.cellHunterInfo)
            hunterItem = None
        self.cellHunterInfo = hunterItem
        INFO_MSG("IBounty::setHunterInfo2", self.cellHunterInfo)
        if not self.cellHunterInfo or self.cellHunterInfo.state in gameconst.BountyState.VALID_CELL_CLEAR_SET_HUNTER_TYPE:
            self.clearDamageSetOutofFighting()

    def updateHunterBuff(self, flag):
        INFO_MSG("IBounty::updateHunterBuff", flag)
        if flag == gameconst.UpdateHunterBuffFlag.ADD:
            self.addBuff(CONST.datas["Bounty_KillerBuff"]["value"], 1, self.id)
        elif flag == gameconst.UpdateHunterBuffFlag.REMOVE:
            self.removeBuff(CONST.datas["Bounty_KillerBuff"]["value"])

    def onGetPreyInfo(self, playerBox, uuid):
        INFO_MSG("IBounty::onGetPreyInfo", uuid, self.level, self.totalScore, self.position, self.spaceNo)
        if not self.cellPreyInfo or self.cellPreyInfo.uuid != uuid:
            ERROR_MSG("IBounty::onGetPreyInfo error", uuid, self.cellPreyInfo)
            return

        self.cellPreyInfo.preyOnline = True
        self.cellPreyInfo.preyLevel = self.level
        self.cellPreyInfo.preyScore = self.totalScore
        self.cellPreyInfo.preyPos = self.position
        self.cellPreyInfo.preySpaceNo = self.spaceNo
        playerBox.client.onAvatarBountyInfo(gameconst.AvatarBountyInfoType.HUNTER, gameconst.AvatarBountyInfoUpdateType.CLIENT, [self.cellPreyInfo.toClientDict()])
        INFO_MSG("IBounty::onGetPreyInfo end", self.cellPreyInfo)

    def addDamageSetInFighting(self, src):
        #INFO_MSG("IBounty::addDamageSetInFighting")
        if not src:
            return

        if not src.IsAvatar:
            return

        if not self.cellHunterInfo or self.cellHunterInfo.state != gameconst.BountyState.ACCEPTED:
            return

        self.hunterDamageSet.add(src.gbId)
        DEBUG_MSG("IBounty::addDamageSetInFighting end", src.gbId)

    def clearDamageSetOutofFighting(self):
        INFO_MSG("IBounty::clearDamageSetOutofFighting", self.hunterDamageSet)
        self.hunterDamageSet = set()

    def checkInDamageSet(self, gbid):
        INFO_MSG("IBounty::checkInDamageSet", self.hunterDamageSet, gbid)
        return gbid in self.hunterDamageSet

    def checkPreyBeKilledByHunter(self, killer):
        INFO_MSG("IBounty::checkPreyBeKilledByHunter cellPreyInfo", self.cellPreyInfo)

        if not self.cellPreyInfo or self.cellPreyInfo.state != gameconst.BountyState.ACCEPTED:
            INFO_MSG("IBounty::checkPreyBeKilledByHunter cellPreyInfo")
            return

        hunter = utils.getAvatarByGbId(self.cellPreyInfo.hunterGbId)
        if not hunter:
            INFO_MSG("IBounty::checkPreyBeKilledByHunter hoster is None")
            return

        if self.spaceNo != hunter.spaceNo:
            INFO_MSG("IBounty::checkPreyBeKilledByHunter not in same spaceNo", self.spaceNo, hunter.spaceNo)
            return

        distance = sMath.distance2DToCompareFrom3DPosition(self.position, hunter.position)
        if distance > 2500:
            INFO_MSG("IBounty::checkPreyBeKilledByHunter not in distance range", self.position, hunter.position)
            return

        deathPenaltyID = GPGPD.datas[formula.fetchMapId(self.spaceNo)]['deathPenaltyID']
        if deathPenaltyID not in gameconst.DeathPenaltyType.VALID_HUNTER_KILL_PREY_TYPE:
            INFO_MSG("IBounty::checkPreyBeKilledByHunter dp type", deathPenaltyID, gameconst.DeathPenaltyType.VALID_HUNTER_KILL_PREY_TYPE)
            return

        if not hunter.checkInDamageSet(self.gbId):
            INFO_MSG("IBounty::checkPreyBeKilledByHunter not in damge set")
            return

        if not hunter.hasState(gameconst.StateEnum.Fighting):
            DEBUG_MSG("IBounty::checkPreyBeKilledByHunter check hoster")
            hoster = utils.getHostEntity(killer)
            if not hoster:
                INFO_MSG("IBounty::checkPreyBeKilledByHunter not in fighting1")
                return
            if not hoster.IsAvatar:
                INFO_MSG("IBounty::checkPreyBeKilledByHunter not in fighting2")
                return
            if hoster.gbId != self.cellPreyInfo.hunterGbId:
                INFO_MSG("IBounty::checkPreyBeKilledByHunter not in fighting3", hoster.gbId)
                return

        # pk击杀不过滤
        self.cellPreyInfo.state = gameconst.BountyState.PRE_COMPLATE
        hunter.cellHunterInfo.state = gameconst.BountyState.PRE_COMPLATE
        self.updatePreyBuff(gameconst.UpdatePreyBuffFlag.ADD)
        gameengine.getGlobalBase('BountyStub').complateBounty(self.base, hunter.base, self.cellPreyInfo.uuid)
        INFO_MSG("IBounty::checkPreyBeKilledByHunter cellHunterInfo", hunter.cellHunterInfo)
        INFO_MSG("IBounty::checkPreyBeKilledByHunter end")
