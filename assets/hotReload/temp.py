# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    import KBEngine
    import formula
    import gameconst
    import utils
    import sMath
    import gamePlay_gamePlay as DDID
    import impAutoCombat
    def getNearestEnemy(self):
        target = None
        _inFightBack = self.getCommonFlagCell(gameconst.AvatarFlagCell.FIGHT_BACK)
        if _inFightBack:
            target = KBEngine.entities.get(self.fightBackTarget)
        if not target:
            targetId = self.autoCombatInfo.get('targetEnemyId', 0)
            target = KBEngine.entities.get(targetId, None)
        if not target and self.selectedTargetId:
            target = KBEngine.entities.get(self.selectedTargetId, None)
            if not target:
                self.setSelectedTargetId(0)
        _hateRecord = self.getTempMiscProp(gameconst.AvatarProps.hateRecord, {})
        closeAutoRangel = DDID.datas.get(formula.getMapId(self.spaceNo), {}).get('closeAutoRangel', None)
        if not target or target.spaceNo != self.spaceNo or not target.IsCombatUnit or sMath.distance2D(target.position, self.position) > self._getAutoFightRange(target) or not utils.checkTargetType('Enemy', self, target) or not self.checkCombatRangeY(target):
            targetsList = []
            entityIds = self.getTargetIdsByTargetType('Enemy')
            priorityTargetEnemyIds = self.autoCombatInfo.get('priorityTargetEnemyId', None)
            _teamTargetIds = self.getTeamTargets()
            _maxVal = None
            target = None
            for eId in entityIds:
                entity = KBEngine.entities.get(eId)
                if not entity:
                    continue
                if entity.id == self.id:
                    continue
                if not self.checkCombatRangeY(entity):
                    continue
                if _inFightBack and eId not in _hateRecord:
                    continue
                if entity.IsCombatUnit and utils.checkCachedTargetType('Enemy', self, entity):
                    targetsList.append(entity)
                    _val = 1 if eId in _hateRecord else 0, 1 if entity.IsMonster and priorityTargetEnemyIds and entity.monsterId in priorityTargetEnemyIds else 0, 1 if eId in _teamTargetIds else 0, -sMath.distance2DToCompareFrom3DPosition(self.position, entity.position)
                    if not closeAutoRangel and _val < (0, 0, 0, 1.0) and self.combatReturnInfo.switch and sMath.distance2D(entity.position, self.combatReturnInfo.pos) > self.combatReturnInfo.range:
                        continue
                    if _maxVal is None:
                        _maxVal = _val
                        target = entity
                    elif _maxVal < _val:
                        _maxVal = _val
                        target = entity
            if not target:
                self.autoCombatInfo['targetEnemyId'] = 0
            else:
                self.autoCombatInfo['targetEnemyId'] = target.id
                return target
        return target
    impAutoCombat.ImpAutoCombat.getNearestEnemy = getNearestEnemy
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
