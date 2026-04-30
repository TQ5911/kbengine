# coding: utf-8
import warnings
import collections
import KBEngine # noqa
import math, sMath

from KBEDebug import *  # noqa

import random
import formula

import utils
import gameconst

import MaxHeap


class TargetHate(object):
    def reloadScript(self):
        import utils
        utils.resetCls(self)

    def __init__(self, targetId, hate=0):
        self.targetId = targetId
        self.currentHate = hate
        self.absoluteMaxHate = hate
        self.localMaxHate = hate

        self._previousHate = 0

    def __repr__(self):
        return "{className}({obj})".format(
            className=self.__class__.__name__,
            obj=', '.join(['{}={}'.format(k, v)
                           for k, v in self.__dict__.items()])
        )

    def _syncMaxHate(self):
        if self.currentHate < 0:
            self.currentHate = 0

        if self.currentHate > self.absoluteMaxHate:
            self.absoluteMaxHate = self.currentHate

        if self.currentHate > self._previousHate:
            self.localMaxHate = self.currentHate

    def _syncPVHate(self):
        self._previousHate = self.currentHate

    def reset(self):
        self._syncPVHate()
        self.currentHate = self.localMaxHate = self.absoluteMaxHate = 0

    def modify(self, value):
        self._syncPVHate()
        self.currentHate = value
        self._syncMaxHate()
        return self

    def increase(self, value):
        return self.modify(self.currentHate + value)

    def decrease(self, value):
        return self.modify(self.currentHate - value)

    def decreaseByPercentage(self, pct):
        return self.modify(self.currentHate - (self.localMaxHate * pct))


class MonsterMaxHeap(MaxHeap.MaxHeap):

    def getDataKey(self, data: TargetHate):
        return data.currentHate


class MonsterHate(object):

    @staticmethod
    def calculateHate(damage, x=1.0):
        return damage * x

    @staticmethod
    def calculateHateByLevel(level, x=100.0):
        return level * x

    @staticmethod
    def damageToHate(damage, symbol='-'):
        if symbol == '-':
            return abs(damage) if damage < 0 else 0
        elif symbol == '+':
            return damage if damage > 0 else 0
        else:
            raise TypeError('unsupported symbol: {}'.format(symbol))

    def reloadScript(self):
        import utils
        utils.resetCls(self)

        for hv in self._hateDict.values():
            hv.reloadScript()

    def __init__(self, owner):
        # _hateDict<OrderedDict>{targetId, obj::TargetHate}
        self._hateDict = collections.OrderedDict()
        self.ownerId = owner.id
        #所有造成过伤害的来源id
        self._dmgSrcSet = set()

    @property
    def owner(self):
        return KBEngine.entities.get(self.ownerId)

    def __repr__(self):
        hateList = sorted(self._hateDict.items(),
                          key=lambda hate: hate[1].currentHate, reverse=True)

        oStr = ', '.join(["{}={}".format(v[0], v[1]) for v in hateList[:3]])

        if len(hateList) > 3:
            oStr = "{}, ...".format(oStr)

        return "{clsName}({obj})".format(
            clsName=self.__class__.__name__,
            obj=oStr
        )

    def __contains__(self, targetId):
        return targetId in self._hateDict

    @property
    def length(self):
        return len(self._hateDict)

    def isEmpty(self, skipVisible=True):
        if skipVisible:
            return self._isEmptySkipVisible()
        return False if self._hateDict else True

    def _isEmptySkipVisible(self):
        _canSeeHiddenEnt = self.owner and self.owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt)
        for tid in self._hateDict:
            ent = KBEngine.entities.get(tid)
            if ent:
                if (self.owner and self.owner.isVisible(ent) or _canSeeHiddenEnt) and ent.isAttackable(self.owner):
                    return False
        return True

    def getFirstVisibleHateTargetByRange(self, skillRange, withOutArea = None):
        _square = skillRange * skillRange
        _canSeeHiddenEnt = self.owner and self.owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt)
        _maxHate = None
        _maxTid = 0
        for tid, hateVal in self._hateDict.items():
            ent = KBEngine.entities.get(tid)
            if not ent or not self.owner:
                continue
            if sMath.distance2DToCompareFrom3DPosition(ent.position, self.owner.position) > _square:
                continue
            if not self.owner.isVisible(ent) and not _canSeeHiddenEnt:
                continue
            if not ent.isAttackable(self.owner):
                continue
            if withOutArea:
                if ent.position.x > withOutArea[0].x and ent.position.x < withOutArea[1].x:
                    if ent.position.y > withOutArea[0].y and ent.position.y < withOutArea[1].y:
                        if ent.position.z > withOutArea[0].z and ent.position.z < withOutArea[1].z:
                            continue

            if _maxHate is None or hateVal.currentHate > _maxHate.currentHate:
                _maxHate = hateVal
                _maxTid = tid

        return _maxTid, _maxHate

    def getFirstVisibleHateTarget(self):
        entDic = {}
        _canSeeHiddenEnt = self.owner and self.owner.hasBuffTag(gameconst.BuffTag.TagSeeHiddenEnt)
        for tid, hateVal in self._hateDict.items():
            ent = KBEngine.entities.get(tid)
            if not ent or not self.owner:
                continue
            if not self.owner.isVisible(ent) and not _canSeeHiddenEnt:
                continue
            if not ent.isAttackable(self.owner):
                continue
            entDic[tid] = hateVal
        return max(entDic.items(), key=lambda hate: hate[1].currentHate, default=(0, None))

    def iterHatedEntities(self):
        for eid, hateVal in self._hateDict.items():
            yield (eid, hateVal)

    @property
    def firstHatredTargetId(self):
        return self.getMaximumHatredTarget()[0]

    def getMaximumHatredTarget(self):
        if not self._hateDict:
            return 0, None
        return max(self._hateDict.items(), key=lambda hate: hate[1].currentHate)

    @property
    def firstEnterTargetId(self):
        return next(iter(self._hateDict.keys()), 0)

    def getRankInNTopTargetId(self, topN=1):
        return self._getRankInNTopTargetId(topN)

    def _getRankInNTopTargetId(self, topN):
        sortedHateData = sorted(self._hateDict.items(), key=lambda hate: hate[1].currentHate, reverse=True)
        _rList = []
        for idx, (k, v) in enumerate(sortedHateData):
            if idx >= topN:
                break
            _rList.append(v.targetId)
        return _rList

    def pickMaxHaterdMonsterTarget(self):
        maxHate = 0
        monsterId = 0
        for tid, hateVal in self._hateDict.items():
            ent = KBEngine.entities.get(tid)
            if not ent:
                continue
            if not ent.IsMonster:
                continue
            if not maxHate or maxHate < hateVal.currentHate:
                maxHate = hateVal.currentHate
                monsterId = tid

        if not monsterId:
            return []
        return [monsterId, ]

    def pickRandomHatredTargetIds(self, exceptHighest=0, number=1, minRange=0, maxRange=0):
        if not exceptHighest:
            return self._getRandomHatredTargetIds(number, minRange=minRange, maxRange=maxRange)
        return self._getRandomHatredTargetIdsExceptNHighest(exceptHighest, number, minRange=minRange, maxRange=maxRange)

    def _getRandomHatredTargetIds(self, number, minRange, maxRange):
        _hateIdList = list(self._hateDict)
        if not _hateIdList:
            return []

        if any([minRange, maxRange]):
            _tempList = []
            for id_ in _hateIdList:
                _pEnt = KBEngine.entities.get(id_)
                if _pEnt and minRange <= sMath.distance2D(self.owner.position, _pEnt.position) <= maxRange:
                    _tempList.append(id_)

            _hateIdList = _tempList

        if len(_hateIdList) < number:
            return _hateIdList

        return random.sample(_hateIdList, number)

    def _getRandomHatredTargetIdsExceptNHighest(self, exceptHighest, number, minRange, maxRange):
        sortedHateData = sorted(self._hateDict.items(), key=lambda hate: hate[1].currentHate, reverse=True)
        # if len(sortedHateData) <= exceptHighest:
        #     return [v.targetId for k, v in sortedHateData][-number:]

        _ll = [v.targetId for k, v in sortedHateData]
        _skpl = []
        fl = _ll[exceptHighest:]
        fl.extend(reversed(_ll[:exceptHighest]))
        if any([minRange, maxRange]):
            _tl = []
            for id_ in fl:
                _pEnt = KBEngine.entities.get(id_)
                if _pEnt and minRange <= sMath.distance2D(self.owner.position, _pEnt.position) <= maxRange:
                    _tl.append(id_)
                    if len(_tl) >= number:
                        break
                    continue

                _skpl.append(id_)

            fl = _tl

        lstnumber = number - len(fl)
        if lstnumber < 0:
            return random.sample(fl, number)
        elif lstnumber == 0:
            return fl
        else:
            return fl + _skpl[:lstnumber]

    def reset(self):
        self._hateDict.clear()

    def getHate(self, targetId):
        return self._hateDict.get(targetId)

    def setHate(self, targetId, value):
        if self.isInHateList(targetId):
            self._hateDict[targetId].modify(value)
            # if getattr(self.owner.aiController, 'logHate', 0):
            #     LOG_DBG("MonsterHate setHate modify targetId value ~~~~~~~~~~~~~~~~~~~~~~", targetId, value, self.__repr__)
        else:
            _targetHate = TargetHate(targetId, value)
            self._hateDict[targetId] = _targetHate
            self.owner.setTargetHateRecord(targetId)
            # if getattr(self.owner.aiController, 'logHate', 0):
            #     LOG_DBG("MonsterHate setHate targetId value ~~~~~~~~~~~~~~~~~~~~~~", targetId, value, self.__repr__)

    def syncHateList(self, owner):
        rmIds = []
        for targetId in self._hateDict:
            target = self.getTarget(targetId)
            if not target or target.isDie() or target.spaceNo!=owner.spaceNo or not utils.isEnemy(owner, target):
                rmIds.append(targetId)
                continue

        for targetId in rmIds:
            # if getattr(self.owner.aiController, 'logHate', 0):
            #     LOG_DBG("MonsterHate syncHateList pop ~~~~~~~~~~~~~~~~~~~~~~", _)
            self.removeHate(targetId)

    def getTarget(self, targetId):
        return KBEngine.entities.get(targetId)

    def increaseHateByAttack(self, targetId, damage, **kwargs):
        value = self._calcIncreaseHate(damage, **kwargs)
        currentHate = self._hateDict[targetId].increase(value)
        # LOG_DBG("MonsterHate increaseHateByAttack targetId, targetLevel, value",
        #           targetId, damage, value, self.__repr__())
        return currentHate

    def getDmgSrcSet(self):
        return self._dmgSrcSet

    def addDmgSrc(self, targetId):
        target = KBEngine.entities.get(targetId)
        if not target:
            LOG_ERR('in addDmgSrc, not found target:', targetId)
        target = utils.getEntityRealEntity(target)
        target and target.IsAvatar and self._dmgSrcSet.add(target.gbId)


    def addToHateListByAttack(self, targetId, damage, **kwargs):
        value = self._calcIncreaseFirstHate(damage, **kwargs) if self.isEmpty() \
            else self._calcIncreaseHate(damage, **kwargs)
        currentHate = self._hateDict[targetId] = TargetHate(targetId, value)
        self.owner.setTargetHateRecord(targetId)
        # if getattr(self.owner.aiController, 'logHate', 0):
        self.addDmgSrc(targetId)
        return currentHate

    def addToHateListByVisionTrigger(self, targetId, targetLevel, isFirstHate = True):
        value = self._increaseFirstHateByVisionTrigger(targetLevel) if self.isEmpty() and isFirstHate \
            else self._increaseHateByVisionTrigger(targetLevel)
        currentHate = self._hateDict[targetId] = TargetHate(targetId, value)
        self.owner.setTargetHateRecord(targetId)
        # if getattr(self.owner.aiController, 'logHate', 0):
        return currentHate

    def isInHateList(self, targetId):
        return True if targetId in self._hateDict else False

    def _increaseHateByVisionTrigger(self, targetLevel):
        return self.calculateHateByLevel(targetLevel) + 1.0

    def _calcIncreaseHate(self, damage, **kwargs):
        return self.calculateHate(damage)

    def _increaseFirstHateByVisionTrigger(self, targetLevel):
        return self.calculateHateByLevel(targetLevel, 100.0 * 2) + 1.0

    def _calcIncreaseFirstHate(self, damage, **kwargs):
        return self.calculateHate(damage, x=5.0)

    def decreaseHateByValue(self, targetId, value, **kwargs):
        if self.isInHateList(targetId):
            targetHate = self._hateDict[targetId]
            targetHate.decrease(value)
            return targetHate

    def decreaseHateByPercentage(self, targetId, value, **kwargs):
        def isPctValidate():
            return True if 0 < value < 1 else False

        if not isPctValidate():
            raise ValueError('decrease hate in percentage must in 0~1,'
                             ' got {}'.format(value))

        if self.isInHateList(targetId):
            targetHate = self._hateDict[targetId]
            targetHate.decreaseByPercentage(value)

            return targetHate

    def removeHate(self, targetId):
        # if getattr(self.owner.aiController, 'logHate', 0):
        #     LOG_DBG("MonsterHate removeHate targetId~~~~~~~~~~~~~~~~~~~~~~", targetId)
        if self.isInHateList(targetId):
            self.owner and self.owner.unsetTargetHateRecord(targetId)
            d = self._hateDict.pop(targetId, None)

            if self.isEmpty():
                self.owner and self.owner.removeState(gameconst.StateEnum.Fighting)
            return d

    def clearHate(self, owner):
        # if getattr(self.owner.aiController, 'logHate', 0):
        #     LOG_DBG("MonsterHate clearHate ~~~~~~~~~~~~~~~~~~~~~~")
        for targetId in self._hateDict:
            self.owner and self.owner.unsetTargetHateRecord(targetId)
        self._hateDict.clear()
        owner.removeState(gameconst.StateEnum.Fighting)

    def inheritHate(self, inheritorId):
        LOG_DBG("inheritHate inheritor ", inheritorId, self._hateDict)
        inheritor = KBEngine.entities.get(inheritorId)
        if not inheritor or not inheritor.IsAvatar:
            return
        for targetId in list(self._hateDict):
            target = KBEngine.entities.get(targetId)
            LOG_DBG("inheritHate target", targetId, target)
            if not target or not hasattr(target, 'aiController') or not target.aiController:
                continue
            targetHate = target.aiController.hateDict.getHate(self.owner.id)
            if not targetHate:
                continue
            if targetHate.currentHate <= 0:
                continue
            LOG_DBG("inheritHate increaseHate", inheritor.id, targetHate.currentHate)
            target.aiController.increaseHate(inheritor.id, targetHate.currentHate)

    def clearSourceHate(self, owner):
        for targetId in self._hateDict:
            self.owner and self.owner.unsetTargetHateRecord(targetId)
        owner.removeState(gameconst.StateEnum.Fighting)

    def getRandomHateTarget(self):
        if not self.length: return 0
        return random.choice(list(self._hateDict.keys()))
