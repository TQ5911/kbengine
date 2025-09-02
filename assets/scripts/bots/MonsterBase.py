# -*- encoding:utf-8 -*-
# defined in */scripts/entity_defs/Monster.def
# It is generated automatically, please do not modify manually
import KBEngine

class MonsterBase(KBEngine.Entity):
    def aiChatToPlayer(self, arg0, arg1): pass
    def notifyCastingSkill(self, arg0, arg1): pass
    def onAddAureole(self, arg0): pass
    def onAddAureoleFromOthers(self, arg0): pass
    def onAddBuff(self, arg0): pass
    def onAddPassiveSkill(self, arg0, arg1): pass
    def onAddSkill(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onAddStateRet(self, arg0, arg1, arg2, arg3): pass
    def onBornAction(self): pass
    def onBreakCastingSkill(self, arg0, arg1, arg2): pass
    def onBreakChannelingSkill(self, arg0, arg1, arg2): pass
    def onDead(self, arg0): pass
    def onDropRuneIds(self, arg0, arg1, arg2): pass
    def onFlashSkillZed(self, arg0): pass
    def onGetAureoleInfo(self, arg0, arg1): pass
    def onGetBuffInfo(self, arg0, arg1): pass
    def onMessage(self, arg0, arg1): pass
    def onMultiAtkStage(self, arg0, arg1, arg2, arg3, arg4): pass
    def onOthersSkillDamage(self, arg0, arg1): pass
    def onRemoveAureole(self, arg0): pass
    def onRemoveAureoleFromOthers(self, arg0): pass
    def onRemoveBuff(self, arg0, arg1): pass
    def onRemoveRune(self, arg0, arg1): pass
    def onServerUseSkill(self, arg0): pass
    def onSetAddSkillCd(self, arg0, arg1, arg2, arg3, arg4, arg5, arg6): pass
    def onShooterSkillCanUse(self, arg0, arg1, arg2): pass
    def onSkillDamage(self, arg0): pass
    def onSkillTeleport(self, arg0, arg1): pass
    def onUpdateAureoles(self, arg0): pass
    def onUpdateAureolesFromOthers(self, arg0): pass
    def onUpdateBuff(self, arg0): pass
    def onUpdateBuffs(self, arg0): pass
    def onUseCasting(self, arg0, arg1, arg2, arg3, arg4): pass
    def onUseChanneling(self, arg0, arg1, arg2, arg3, arg4, arg5): pass
    def onUseSkill(self, arg0, arg1, arg2, arg3, arg4): pass
    def popDialog(self, arg0): pass
    def popDialogWithSelfHead(self, arg0): pass
    def showPopoverMsg(self, arg0): pass
    def showPopoverMsgWithArg(self, arg0, arg1): pass
    def skillTeleportBefore(self, arg0): pass
