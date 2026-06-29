# coding: utf-8
import warnings
import collections
import KBEngine # noqa
import sMath

from KBEDebug import *  # noqa

import random

import utils
import gameconst


class TargetHate(object):
    def reloadScript(self):
        import utils
        utils.resetClass(self)

    def __init__(self, targetId, hate=0):
        self.currentHate = hate
        self.targetId = targetId
        self.absoluteMaxHate = hate
        self._previousHate = 0
        self.localMaxHate = hate

    def _syncMaxHate(self):
        if self.currentHate < 0:
            self.currentHate = 0

        if self.currentHate > self._previousHate:
            self.localMaxHate = self.currentHate

        if self.currentHate > self.absoluteMaxHate:
            self.absoluteMaxHate = self.currentHate

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ', '.join(['{}={}'.format(_k, v)
                           for _k, v in self.__dict__.items()])
        )

    def reset(self):
        self._syncPVHate()
        self.currentHate = self.localMaxHate = self.absoluteMaxHate = 0

    def _syncPVHate(self):
        self._previousHate = self.currentHate

    def modify(self, value):
        self._syncPVHate()
        self.currentHate = value
        self._syncMaxHate()
        return self

    def decreaseByPercentage(self, pct):
        return self.modify(self.currentHate - (self.localMaxHate * pct))

    def decrease(self, value):
        return self.modify(self.currentHate - value)

    def increase(self, value):
        return self.modify(self.currentHate + value)


class MonsterHate(object):

    def __init__(self, owner, **kwargs):
        # _hateDict<OrderedDict>{targetId, obj::TargetHate}
        self._hateDict = collections.OrderedDict()
        self.ownerId = owner.id
        #所有造成过伤害的来源id
        self._dmgSrcSet = set()

    @staticmethod
    def calculateHateByLevel(level, x=100.0):
        return level * x

    @staticmethod
    def calculateHate(damage, x=1.0):
        return damage * x

    @staticmethod
    def damageToHate(damage, symbol='-'):
        if symbol == '-':
            if damage < 0:
                return abs(damage)
            else:
                return 0
        elif symbol == '+':
            return damage if damage > 0 else 0
        else:
            raise TypeError('unsupported symbol: {}'.format(symbol))

    @property
    def owner(self):
        return KBEngine.entities.get(self.ownerId)

    def reloadScript(self):
        import utils
        utils.resetClass(self)

        for hv in self._hateDict.values():
            hv.reloadScript()

    def __repr__(self):
        _hateList = sorted(self._hateDict.items(),
                          key=lambda v: v[1].currentHate, reverse=True)

        _oStr = ', '.join(["{}={}".format(_v[0], _v[1]) for _v in _hateList[:3]])

        if len(_hateList) > 3:
            _oStr = "{}, ...".format(_oStr)

        return "{clsName}({obj})".format(
            clsName=self.__class__.__name__,
            obj=_oStr
        )

    @property
    def length(self):
        return len(self._hateDict)

    def __contains__(self, targetId):
        return targetId in self._hateDict

    def _isEmptySkipVisible(self):
        _canSeeHiddenEnt = self.owner and self.owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt)
        for _tid in self._hateDict:
            ent = KBEngine.entities.get(_tid)
            if ent:
                if (self.owner and self.owner.isVisible(ent) or _canSeeHiddenEnt) and ent.canAttackable(self.owner):
                    return False
        return True

    def isEmpty(self, skipVisible=True):
        if skipVisible:
            return self._isEmptySkipVisible()
        return False if self._hateDict else True

    def getFirstVisibleHateTargetByRange(self, skillRange, withOutArea = None):
        _square = skillRange * skillRange
        _canSeeHiddenEnt = self.owner and self.owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt)
        _maxHate = None
        _maxTid = 0
        for _tid, hateVal in self._hateDict.items():
            ent = KBEngine.entities.get(_tid)
            if not ent or not self.owner:
                continue
            if sMath.distance2DToCompareFrom3DPosition(ent.position, self.owner.position) > _square:
                continue
            if not self.owner.isVisible(ent) and not _canSeeHiddenEnt:
                continue
            if not ent.canAttackable(self.owner):
                continue
            if withOutArea:
                if ent.position.x > withOutArea[0].x and ent.position.x < withOutArea[1].x:
                    if ent.position.y > withOutArea[0].y and ent.position.y < withOutArea[1].y:
                        if ent.position.z > withOutArea[0].z and ent.position.z < withOutArea[1].z:
                            continue

            if _maxHate is None or hateVal.currentHate > _maxHate.currentHate:
                _maxHate = hateVal
                _maxTid = _tid

        return _maxTid, _maxHate

    def getFirstVisibleHateTarget(self):
        _canSeeHiddenEnt = self.owner and self.owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt)
        
        best_tid = 0
        best_hate_val = None
        max_hate = -1  # 初始化一个极小值
        
        for _tid, hateVal in self._hateDict.items():
            # 1. 实体与所有者检查
            _ent = KBEngine.entities.get(_tid)
            if not _ent or not self.owner:
                continue
                
            # 2. 可见性检查
            if not self.owner.isVisible(_ent) and not _canSeeHiddenEnt:
                continue
                
            # 3. 可攻击性检查
            if not _ent.canAttackable(self.owner):
                continue
                
            # 4. 动态比较仇恨值（替代 max 函数）
            current_hate = hateVal.currentHate
            if current_hate > max_hate:
                max_hate = current_hate
                best_tid = _tid
                best_hate_val = hateVal
                
        return (best_tid, best_hate_val)

    def iterHatedEntities(self):
        for _eid, hateVal in self._hateDict.items():
            yield (_eid, hateVal)

    def getMaxHatredTarget(self):
        if not self._hateDict:
            return 0, None
        return max(self._hateDict.items(), key=lambda v: v[1].currentHate)

    @property
    def firstHatredTargetId(self):
        return self.getMaxHatredTarget()[0]

    def getRankInNTopTargetId(self, topN=1):
        return self._getRankInNTopTargetId(topN)

    @property
    def firstEnterTargetId(self):
        return next(iter(self._hateDict.keys()), 0)

    def _getRankInNTopTargetId(self, topN):
        _sortedHateData = sorted(self._hateDict.items(), key=lambda v: v[1].currentHate, reverse=True)
        _rList = []
        for _idx, (k, v) in enumerate(_sortedHateData):
            if _idx >= topN:
                break
            _rList.append(v.targetId)
        return _rList

    def pickMaxHaterdMonsterTarget(self):
        maxHate = 0
        monsterId = 0
        for _tid, hateVal in self._hateDict.items():
            _ent = KBEngine.entities.get(_tid)
            if not _ent:
                continue
            if not _ent.IsMonster:
                continue
            if not maxHate or maxHate < hateVal.currentHate:
                maxHate = hateVal.currentHate
                monsterId = _tid

        if not monsterId:
            return []
        return [monsterId, ]

    def pickRandomHatredTargetIds(self, exceptHighest=0, number=1, minRange=0, maxRange=0):
        if not exceptHighest:
            return self._fetchRandomHatredTargetIds(number, minRange, maxRange)
        return self._fetchRandomHatredTargetIdsExceptNHighest(exceptHighest, number, minRange=minRange, maxRange=maxRange)

    def _fetchRandomHatredTargetIds(self, num, minRng, maxRng):
        _hateIdList = list(self._hateDict.keys())
        if not _hateIdList:
            return []

        if any([minRng, maxRng]):
            _tempList = []
            for id_ in _hateIdList:
                _pEnt = KBEngine.entities.get(id_)
                if _pEnt and minRng <= sMath.distance2D(self.owner.position, _pEnt.position) <= maxRng:
                    _tempList.append(id_)

            _hateIdList = _tempList

        if len(_hateIdList) < num:
            return _hateIdList

        return random.sample(_hateIdList, num)

    def _fetchRandomHatredTargetIdsExceptNHighest(self, exceptHighest, number, minRange, maxRange):
        _sortedHateData = sorted(self._hateDict.items(), key=lambda hate: hate[1].currentHate, reverse=True)

        _ll = [v.targetId for k, v in _sortedHateData]
        _skpl = []
        _fl = _ll[exceptHighest:]
        _fl.extend(reversed(_ll[:exceptHighest]))
        if any([minRange, maxRange]):
            _tl = []
            for _id in _fl:
                _pEnt = KBEngine.entities.get(_id)
                if _pEnt and minRange <= sMath.distance2D(self.owner.position, _pEnt.position) <= maxRange:
                    _tl.append(_id)
                    if len(_tl) >= number:
                        break
                    continue

                _skpl.append(_id)

            _fl = _tl

        lstnumber = number - len(_fl)
        if lstnumber < 0:
            return random.sample(_fl, number)
        elif lstnumber == 0:
            return _fl
        else:
            return _fl + _skpl[:lstnumber]

    def getHate(self, targetId):
        return self._hateDict.get(targetId)

    def reset(self):
        self._hateDict.clear()

    def setHate(self, tgtId, value):
        if self.isInHateList(tgtId):
            self._hateDict[tgtId].modify(value)
        else:
            _targetHate = TargetHate(tgtId, value)
            self._hateDict[tgtId] = _targetHate
            self.owner.setTargetHateRecord(tgtId)

    def syncHateList(self, owner):
        _rmIds = []
        for _targetId in self._hateDict:
            target = self.getTarget(_targetId)
            if not target or target.isDie() or target.spaceNo!=owner.spaceNo or not utils.isEnemy(owner, target):
                _rmIds.append(_targetId)
                continue

        for _targetId in _rmIds:
            self.removeHate(_targetId)

    def getTarget(self, targetId):
        return KBEngine.entities.get(targetId)

    def incHateByAttack(self, tgtId, damage, **kwargs):
        value = self._calcIncreaseHate(damage, **kwargs)
        currentHate = self._hateDict[tgtId].increase(value)
        return currentHate

    def addDmgSrc(self, targetId):
        target = KBEngine.entities.get(targetId)
        if not target:
            LOG_ERR('in addDmgSrc, not found target:', targetId)
        target = utils.getEntityRealEntity(target)
        if target and target.IsAvatar:
            self._dmgSrcSet.add(target.gbId)

    def getDmgSrcSet(self):
        return self._dmgSrcSet

    def addHateListByAttack(self, targetId, damage, **kwargs):
        _value = self._calcIncreaseFirstHate(damage, **kwargs) if self.isEmpty() \
            else self._calcIncreaseHate(damage, **kwargs)
        _currentHate = self._hateDict[targetId] = TargetHate(targetId, _value)
        self.owner.setTargetHateRecord(targetId)
        self.addDmgSrc(targetId)
        return _currentHate

    def addToHateListByVisionTrigger(self, targetId, targetLevel, isFirstHate = True):
        _value = self._increaseFirstHateByVisionTrigger(targetLevel) if self.isEmpty() and isFirstHate \
            else self._increaseHateByVisionTrigger(targetLevel)
        _currentHate = self._hateDict[targetId] = TargetHate(targetId, _value)
        self.owner.setTargetHateRecord(targetId)
        return _currentHate

    def _increaseHateByVisionTrigger(self, targetLevel):
        return self.calculateHateByLevel(targetLevel) + 1.0

    def isInHateList(self, targetId):
        return True if targetId in self._hateDict else False

    def _increaseFirstHateByVisionTrigger(self, targetLevel):
        return self.calculateHateByLevel(targetLevel, 100.0 * 2) + 1.0

    def _calcIncreaseHate(self, damage, **kwargs):
        return self.calculateHate(damage)

    def _calcIncreaseFirstHate(self, damage, **kwargs):
        return self.calculateHate(damage, x=5.0)

    def decHateByValue(self, targetId, value, **kwargs):
        if self.isInHateList(targetId):
            _targetHate = self._hateDict[targetId]
            _targetHate.decrease(value)
            return _targetHate

    def decHateByPercentage(self, tgtId, value, **kwargs):
        if not (0 < value < 1):
            raise ValueError(' when decrease hate in percentage must in 0~1,'
                             ' got {}'.format(value))

        if self.isInHateList(tgtId):
            _targetHate = self._hateDict[tgtId]
            _targetHate.decreaseByPercentage(value)

            return _targetHate

    def removeHate(self, targetId):
        if self.isInHateList(targetId):
            if self.owner:
                self.owner.unsetTargetHateRecord(targetId)

            d = self._hateDict.pop(targetId, None)

            if self.isEmpty():
                if self.owner:
                    self.owner.removeState(gameconst.StateEnum.Fighting)

            return d

    def clearHate(self, owner):
        for targetId in self._hateDict:
            if not self.owner:
                continue

            self.owner.unsetTargetHateRecord(targetId)

        self._hateDict.clear()
        owner.removeState(gameconst.StateEnum.Fighting)

    def inheritHate(self, inheritorId):
        LOG_DBG("inheritHate inheritor ", inheritorId, self._hateDict)
        inheritor = KBEngine.entities.get(inheritorId)
        if not (inheritor and inheritor.IsAvatar):
            return

        for targetId in list(self._hateDict):
            _target = KBEngine.entities.get(targetId)
            LOG_DBG("inheritHate target", targetId, _target)
            if not _target or not hasattr(_target, 'aiController') or not _target.aiController:
                continue
            targetHate = _target.aiController.hateDic.getHate(self.owner.id)
            if not targetHate:
                continue
            if targetHate.currentHate <= 0:
                continue
            LOG_DBG("inheritHate doIncreaseHate", inheritor.id, targetHate.currentHate)
            _target.aiController.doIncreaseHate(inheritor.id, targetHate.currentHate)

    def clearSourceHate(self, owner):
        for targetId in self._hateDict:
            if not self.owner:
                continue

            self.owner.unsetTargetHateRecord(targetId)

        owner.removeState(gameconst.StateEnum.Fighting)

    def getRandomHateTarget(self):
        if self.length:
            return random.choice(list(self._hateDict.keys()))

        return 0


