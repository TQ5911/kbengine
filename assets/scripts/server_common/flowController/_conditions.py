# coding: utf-8
# ----------------------------------------------
# CONDITIONS
# ----------------------------------------------
from KBEDebug import *
import KBEngine

import gameconst
import utils

import ep_ctrl


__all__ = [
    'ConditionCheckValue', 'conditionCheckValue',
    'ConditionDungeonHaveCreationInRange', 'conditionDungeonHaveCreationInRange',
]


class ConditionCheckValue(object):
    def __init__(self, control, formulaID, dungeonVarIds):
        self._controller = control
        self._formulaId = formulaID
        self._dungeonVarIds = dungeonVarIds

    def __call__(self, *params, **kwargs):
        return self._conditionCheckValue(self._controller, self._formulaId, self._dungeonVarIds)

    @staticmethod
    def _conditionCheckValue(control, formulaID, dungeonVarIds):
        LOG_WARN("DUNGEON FLOW -- CONDITION: dungeon check value -> {}: {}".format(
            formulaID, dungeonVarIds))

        spaceMgr = control.owner
        if not spaceMgr:
            LOG_WARN("FlowController::ConditionCheckValue:: spaceMgr not found")
            return False

        # construct params
        mParams = {}
        for _i_varID in dungeonVarIds:
            _i_varVal = spaceMgr.getSpaceVar(_i_varID)
            if _i_varVal is not None:
                mParams[_i_varID] = _i_varVal

        m_result = utils.getValByFormula(formulaID, mParams)
        return bool(m_result)


conditionCheckValue = ConditionCheckValue



class ConditionDungeonHaveCreationInRange(object):
    def __init__(self, control, monsterGID, creationID, iRange):
        self._controller = control
        self._monsterGID = monsterGID
        self._creationID = creationID
        self._rng = iRange

    def __call__(self, *args, **kwargs):
        return self._conditionDunCreationInRange(
            self._controller, self._monsterGID, self._creationID, self._rng)

    @staticmethod
    def _conditionDunCreationInRange(control, monsterGID, creationID, iRange):
        LOG_WARN('DUNGEON FLOW -- CONDITION: dungeon have creation in range -> {}: {}(iRange={})'.format(
            monsterGID, creationID, iRange))

        spaceMgr = control.owner
        gidTag = 'gid_{}'.format(monsterGID)

        for ent in spaceMgr.listEntitiesByTag(gidTag):
            for cEnt in ent.entitiesInRange(iRange, 'Creation'):
                if cEnt.creationId == creationID:
                    return True
        return False


conditionDungeonHaveCreationInRange = ConditionDungeonHaveCreationInRange

