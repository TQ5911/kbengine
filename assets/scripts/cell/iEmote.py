# coding: utf-8

from KBEDebug import *
import KBEngine
import gamedecorator
import conflict_conflict_def as C_C_DD
import posture_config as PC
import posture_posture as PP
import gameconst
import gametimer
import utils

class IEmote(object):
    def __init__(self):
        LOG_DBG("IEmote::__init__")
        self.emoteId = 0
        self.playTimerId = 0
        self.lastPlayTime = 0

    def checkPlayEmote(self, emoteId):
        now = utils.curTS()
        LOG_DBG("IEmote::checkPlayEmote", emoteId)
        emoteCfg = PP.datas.get(emoteId, None)
        if not emoteCfg:
            LOG_ERR("IEmote::checkPlayEmote cfg error", emoteId)
            return False
        if not emoteCfg.get('isOpen', True):
            LOG_WARN("IEmote::checkPlayEmote not open", emoteId)
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
        LOG_INFO("IEmote::reqPlayEmote", emoteId)
        if not self.checkPlayEmote(emoteId):
            return
        
        if not self.checkConflictState(C_C_DD.datas.posture):
            LOG_WARN('IEmote::reqPlayEmote checkConflictState')
            return
        
        self.base.checkPlayEmoteCond(emoteId)

    def onCheckPlayEmoteCond(self, emoteId):
        LOG_INFO("IEmote::onCheckPlayEmoteCond", emoteId)
        if not self.checkConflictState(C_C_DD.datas.posture):
            LOG_INFO('IEmote::onCheckPlayEmoteCond checkConflictState')
            return
        emoteCfg = PP.datas.get(emoteId, None)
        if not emoteCfg:
            LOG_ERR("IEmote::onCheckPlayEmoteCond cfg error", emoteId)
            return

        self.cannelPlayTimer()
        if emoteCfg['loop'] in (gameconst.EmoteTimeType.ONE_SHOT,):
            self.playTimerId = self.addTimerCB(emoteCfg['time'] + 1, 'stopPlayEmote', (gameconst.StopPlayEmoteReason.TimeOut, ), gametimer.TIMER_TAG_STOP_PLAY_EMOTE, 'playTimerId')
        self.emoteId = emoteId
        self.setState(gameconst.StateEnum.posture)
        self.suspendAutoCombat(gameconst.SuspendAutoCombatReasonEnum.PlayEmote)
        self.allClients.onStartPlayEmote(emoteId)

    @gamedecorator.crossServer
    @utils.isMyself
    def reqStopPlayEmote(self, exposed):
        LOG_INFO("IEmote::reqStopPlayEmote", self.emoteId)
        self.stopPlayEmote(gameconst.StopPlayEmoteReason.Client)

    def stopPlayEmote(self, reason):
        LOG_DBG("IEmote::stopPlayEmote", self.emoteId, reason)
        if not self.hasState(gameconst.StateEnum.posture):
            return
        self.removeState(gameconst.StateEnum.posture)

    def exitPlayEmote(self, byConflictState, removeReason):
        LOG_INFO("IEmote::exitPlayEmote", byConflictState, removeReason)
        self.emoteId = 0
        self.cannelPlayTimer()
        self.allClients.onStopPlayEmote()
        self.resumeAutoCombat(self.spaceNo, gameconst.SuspendAutoCombatReasonEnum.PlayEmote)
