# coding: utf-8

from KBEDebug import *
import KBEngine
import gamedecorator
import conflict_conflict_def as CCD
import posture_config as PC
import posture_posture as PP
import gameconst
import gametimer
import utils

class IEmote(object):
    def __init__(self):
        DEBUG_MSG("IEmote::__init__")
        self.emoteId = 0
        self.playTimerId = 0
        self.lastPlayTime = 0

    def checkPlayEmote(self, emoteId):
        now = utils.curTS()
        DEBUG_MSG("IEmote::checkPlayEmote", emoteId)
        emoteCfg = PP.datas.get(emoteId, None)
        if not emoteCfg:
            ERROR_MSG("IEmote::checkPlayEmote cfg error", emoteId)
            return False
        if not emoteCfg.get('isOpen', True):
            WARNING_MSG("IEmote::checkPlayEmote not open", emoteId)
            return False

        if now < self.lastPlayTime + PC.datas['postureCd']['value']:
            self.showMsg(PC.datas['postureCdMsg']['value'], [])
            return False

        self.lastPlayTime = now
        return True

    def cannelPlayTimer(self):
        if not self.playTimerId:
            return
        self.cancelTimerCB(self.playTimerId, gametimer.TIMER_TAG_STOP_PLAY_EMOTE)
        self.playTimerId = 0

    @gamedecorator.crossServer
    @utils.isMyself
    def reqPlayEmote(self, exposed, emoteId):
        INFO_MSG("IEmote::reqPlayEmote", emoteId)
        if not self.checkPlayEmote(emoteId):
            return
        
        if not self.checkConflictState(CCD.datas.posture):
            WARNING_MSG('IEmote::reqPlayEmote checkConflictState')
            return
        
        self.base.checkPlayEmoteCond(emoteId)

    def onCheckPlayEmoteCond(self, emoteId):
        INFO_MSG("IEmote::onCheckPlayEmoteCond", emoteId)
        if not self.checkConflictState(CCD.datas.posture):
            INFO_MSG('IEmote::onCheckPlayEmoteCond checkConflictState')
            return
        emoteCfg = PP.datas.get(emoteId, None)
        if not emoteCfg:
            ERROR_MSG("IEmote::onCheckPlayEmoteCond cfg error", emoteId)
            return

        self.cannelPlayTimer()
        if emoteCfg['loop'] in (gameconst.EmoteTimeType.ONE_SHOT,):
            self.playTimerId = self.addTimerCB(emoteCfg['time'] + 1, 'stopPlayEmote', (gameconst.StopPlayEmoteReason.TimeOut, ), gametimer.TIMER_TAG_STOP_PLAY_EMOTE, 'playTimerId')
        self.emoteId = emoteId
        self.setState(gameconst.StateEnum.posture)
        self.suspendAutoCombat(gameconst.SuspendAutoCombatReason.PlayEmote)
        self.allClients.onStartPlayEmote(emoteId)

    @gamedecorator.crossServer
    @utils.isMyself
    def reqStopPlayEmote(self, exposed):
        INFO_MSG("IEmote::reqStopPlayEmote", self.emoteId)
        self.stopPlayEmote(gameconst.StopPlayEmoteReason.Client)

    def stopPlayEmote(self, reason):
        INFO_MSG("IEmote::stopPlayEmote", self.emoteId, reason)
        if not self.hasState(gameconst.StateEnum.posture):
            return
        self.removeState(gameconst.StateEnum.posture)

    def exitPlayEmote(self, byConflictState, removeReason):
        INFO_MSG("IEmote::exitPlayEmote", byConflictState, removeReason)
        self.emoteId = 0
        self.cannelPlayTimer()
        self.allClients.onStopPlayEmote()
        self.recoverAutoCombat(self.spaceNo, gameconst.SuspendAutoCombatReason.PlayEmote)