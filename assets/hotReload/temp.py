# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    import gameconst
    import gametimer
    import conflict_status as CSD
    import conflict_status_def as CCDD
    import SkillManager
    def _onRemovedState(self, states, byConflictState=-1, removeReason=0):
        for state in states:
            if state == gameconst.State.Fighting:
                self.leaveFightingState()
            elif state == gameconst.State.autoFight:
                DEBUG_MSG('ZTQ ', states, byConflictState)
                self._stopAutoCombat()
            elif state == gameconst.State.Moving and hasattr(self, 'removeMoveController'):
                self.removeMoveController()
            elif state == gameconst.State.Channeling or state == gameconst.State.moveChannel:
                DEBUG_MSG('removeState  killChannelingSkill ')
                if removeReason:
                    self.killChannelingSkill(removeReason)
                else:
                    self.killChannelingSkill(gameconst.ChannelingBreak.CONFLICT_STATE)
            elif state == gameconst.State.Casting:
                DEBUG_MSG('removeState  killCastingSkill ', byConflictState)
                if byConflictState >= 0 and byConflictState in (gameconst.State.Moving, gameconst.State.Idle):
                    self.killCastingSkill(gameconst.EndCasting.Move)
                elif byConflictState == gameconst.State.Death:
                    self.killCastingSkill(gameconst.EndCasting.Dead)
                elif byConflictState == gameconst.State.clientPick:
                    self.killCastingSkill(gameconst.EndCasting.clientPick)
                else:
                    self.killCastingSkill(gameconst.EndCasting.ConflictState)
            elif state == gameconst.State.riding:
                self._onExitRiding(byConflictState)
            elif state == gameconst.State.clientPick:
                self._onExitClientPick()
            elif state == gameconst.State.GeneralAttack:
                if removeReason != gameconst.RemoveStateReason.SKILL_DONE:
                    self._breakGeneralSkill()
            elif state == gameconst.State.Shifting or state == gameconst.State.Dodging:
                self.endMovement()
            elif state == gameconst.State.Sprinting:
                self.leaveSprintingState()
            elif state == gameconst.State.Flying:
                self._callback(1, '_onRemoveFlyingState', (), gametimer.TIMER_TAG_ON_REMOVE_FLY_STATE)
            elif state == CCDD.datas.duel:
                self.leaveDuelState()
            buffTag = CSD.datas[state].get('buffTag')
            if buffTag:
                self.removeBuffByTag(buffTag)
    SkillManager.SkillManager._onRemovedState = _onRemovedState
    # --auto genterate mark--
    pass
def refreshBase():
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
