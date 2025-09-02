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
    def __init__(self, controller, formulaId, dungeonVarIds):
        self._controller = controller
        self._formulaId = formulaId
        self._dungeonVarIds = dungeonVarIds

    def __call__(self, *args, **kwargs):
        return self._conditionCheckValue(self._controller, self._formulaId, self._dungeonVarIds)

    @staticmethod
    def _conditionCheckValue(controller, formulaId, dungeonVarIds):
        WARNING_MSG("DUNGEON FLOW -- CONDITION: dungeon check value -> {}: {}".format(
            formulaId, dungeonVarIds))

        spaceMgr = controller.owner
        if not spaceMgr:
            WARNING_MSG("FlowController::ConditionCheckValue:: spaceMgr not found")
            return False

        # build params
        m_params = {}
        for _i_varID in dungeonVarIds:
            _i_varVal = spaceMgr.getSpaceVar(_i_varID)
            if _i_varVal is not None:
                m_params[_i_varID] = _i_varVal

        m_result = utils.getValByFormula(formulaId, m_params)
        return bool(m_result)


conditionCheckValue = ConditionCheckValue



class ConditionDungeonHaveCreationInRange(object):
    def __init__(self, controller, monsterGID, creationID, rng):
        self._controller = controller
        self._monsterGID = monsterGID
        self._creationID = creationID
        self._rng = rng

    def __call__(self, *args, **kwargs):
        return self._conditionDungeonHaveCreationInRange(
            self._controller, self._monsterGID, self._creationID, self._rng)

    @staticmethod
    def _conditionDungeonHaveCreationInRange(controller, monsterGID, creationID, rng):
        WARNING_MSG('DUNGEON FLOW -- CONDITION: dungeon have creation in range -> {}: {}(rng={})'.format(
            monsterGID, creationID, rng))

        spaceMgr = controller.owner
        gidTag = 'gid_{}'.format(monsterGID)

        for ent in spaceMgr.getEntitiesByTag(gidTag):
            for cEnt in ent.entitiesInRange(rng, 'Creation'):
                if cEnt.creationId == creationID:
                    return True
        return False


conditionDungeonHaveCreationInRange = ConditionDungeonHaveCreationInRange

