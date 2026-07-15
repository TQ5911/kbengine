
# coding: utf-8

import KBEngine
from KBEDebug import *

import LogTrackingMgr
import gameconfig
import userType
import utils
import gameclass
import gameengine
import dropAward
import gameconst
import achievement_details as A_DD
import AchievementValInfo
import actionContext
import antiAddictCategory_antiAddictCategory_def as AAC_AAC_DD
import message_chatMessage as M_CMD
import json
import gzip

class AchievementsVal(userType.UserSingleType):
    '''ACHIEVEMENTS_DATA_INFO'''
    def __init__(self, achieveList=(), maxVersion=-1, finishedIds=(), sumPoint=0):
        self.maxVersion = maxVersion
        self.achieveDic = {}
        self.typeDic = {}
        self.sumPoint = sumPoint
        for achieveVal in achieveList:
            self.achieveDic[achieveVal.achieveId] = achieveVal

            self._addTypeDic(achieveVal)

        self.finishedIds = list(finishedIds)


    @classmethod
    def _checkIgnores_(cls):
        return 'typeDic',

    def toAchievementsSavedDict(self):
        return {
            'achieveList': [achieveVal for achieveVal in self.achieveDic.values()],
            'maxVersion': self.maxVersion,
            'finishedIds': self.finishedIds,
            'sumPoint': self.sumPoint,
        }

    def onLvUpAchievement(self, ls, le, avatar):
        LOG_DBG('onLvUpAchievement', ls, le, avatar.gbID, avatar.getRoleCacheAttr('level', 1))
        for _lv in range(ls + 1, le + 1):
            self.takeNewAchievementWhenLevelUp(_lv, avatar)

        self.triggerAchieveByType(
            avatar,
            gameconst.AchieveType.LEVEL,
            actionContext.AchievementCtx())

    def takeNewAchievementWhenLevelUp(self, level, avatar):
        _waitList = A_DD.level2AchieveDic.get(level, [])
        _updateList = self._updateByWaitList(avatar, _waitList, actionContext.AchievementCtx())

        if _updateList:
            avatar.client.onUpdateAchieveDatas(_updateList)

    def triggerAchieveByType(self, avatar, targetType, ctx):
        #玩家在跨服，本服却触发了成就直接跳过
        if avatar.isCrossServerInLocalServer:
            if (isinstance(ctx, dict) and not ctx.get('fromCrossServer')) or (not isinstance(ctx, dict) and not hasattr(ctx, 'fromCrossServer')):
                LOG_WARN('triggerAchieveByType isCrossServerInLocalServer and skip', targetType, ctx)
                return
        LOG_DBG('triggerAchieveByType', targetType, ctx)
        _waitList = self.typeDic.get(targetType, [])
        _updateList = self._updateByWaitList(avatar, _waitList, ctx)

        if _updateList:
            avatar.client.onUpdateAchieveDatas(_updateList)
            avatar.syncMethodCallToLocalServerBase("onCrossServerTriggerAchieveByType", (targetType, ctx))

    def _addTypeDic(self, achieveVal):
        _list = self.typeDic.setdefault(achieveVal.targetType(), [])
        if achieveVal.achieveId not in _list:
            _list.append(achieveVal.achieveId)

    def _removeTypeDic(self, achieveVal):
        _list = self.typeDic.get(achieveVal.targetType(), [])
        _list.remove(achieveVal.achieveId)

    def addAchieveVal(self, achieveVal):
        if achieveVal.achieveId in self.achieveDic:
            return False

        self.achieveDic[achieveVal.achieveId] = achieveVal
        self._addTypeDic(achieveVal)
        return True

    def popAchieveVal(self, achieveId):
        if achieveId in self.achieveDic:
            _achieveVal = self.achieveDic.pop(achieveId)
            self._removeTypeDic(_achieveVal)
            return _achieveVal

    def _checkCouldTakeAchieve(self, avatar, achieveId):
        _achieveData = A_DD.datas[achieveId]
        if not AchievementValInfo.AchievementValVal.checkSupport(_achieveData['targetType']):
            LOG_ERR('这个成就类型服务端还没支持:', _achieveData['targetType'], _achieveData['levelDisplay'])
            return False

        if avatar.getRoleCacheAttr('level', 1) < _achieveData['openLevel']:
            return False

        _shuPreAch = _achieveData['shuPreAch']
        if _shuPreAch:
            if _shuPreAch in self.finishedIds:
                return True

            _achieveVal = self.achieveDic.get(_shuPreAch)
            if not _achieveVal:
                return False

            if not _achieveVal.isFinished():
                return False

        return True

    def _updateByWaitList(self, avatar, waitList, ctx):
        waitList = waitList[:] # 复制一份，防止修改原列表
        _updateList = []
        # 貌似成就有一万个了，这个先改大点，这个数主要用来防止无限循环
        _maxTimes = 9999
        while waitList:
            _maxTimes -= 1
            if _maxTimes <= 0:
                LOG_ERR('achieve wait list loop too much')
                break

            _achieveId = waitList.pop(0)
            if _achieveId in self.finishedIds:
                continue

            if not self._checkCouldTakeAchieve(avatar, _achieveId):
                continue

            _achieveVal = self.achieveDic.get(_achieveId)
            _oldIsFinished = False
            if _achieveVal:
                _oldIsFinished = _achieveVal.isFinished()
                if _achieveVal.updateFromNewAchieveData(avatar, A_DD.datas[_achieveId], ctx, gameconst.ACHIEVE_SRC_UPDATE):
                    _updateList.append(_achieveVal)

            else:
                _achieveVal = AchievementValInfo.AchievementValVal.fromAchieveData(
                    avatar, 
                    A_DD.datas[_achieveId], 
                    ctx)

                self.addAchieveVal(_achieveVal)
                _updateList.append(_achieveVal)

            if _oldIsFinished != self.achieveDic[_achieveId].isFinished():
                self._notifyFinishMsg(_achieveVal, _achieveId, avatar)

                # 这里如果是完成状态，更新wait列表
                _sons = A_DD.sonAchieveDic.get(_achieveId, [])

                for _sonId in _sons:
                    if _sonId not in waitList:
                        waitList.append(_sonId)

        LOG_DBG('updateByWaitList left times:', _maxTimes)

        return _updateList

    def _notifyFinishMsg(self, achieveVal, achieveId, avatar):
        if not gameconfig.visibleConfigEnabled('achievement'):
            return

        _name = avatar.getRoleCacheAttr('name', '')
        _gbId = str(avatar.gbID)
        _msgIds = achieveVal.configData()['finishMessage']
        for _msgId in _msgIds:
            _msgData = M_CMD.datas[_msgId]

            if gameconst.ChatChannelEnum.WORLD in _msgData['channelID']:
                gameengine.broadcastBaseapp(
                    'broadcastToAllAvatar',
                    (
                        gameconst.BASE,
                        'onMessagePre',
                        (_msgId, [str(achieveId), _name, _gbId]),
                        (),
                    )
                )
            else:
                avatar.onMessagePre(_msgId, [str(achieveId)])

    def updateAchieveData(self, avatar):
        _index = utils.binarySearchFirstGreater(A_DD.versionList, self.maxVersion)
        _versions = A_DD.versionList[_index:]

        _waitList = []
        for _version in _versions:
            _achieveList = A_DD.versionDict[_version]
            _waitList.extend(_achieveList)

        self._updateByWaitList(avatar, _waitList, actionContext.AchievementCtx())

        self.maxVersion = A_DD.versionList[-1]

    def takeAllAchievementRewards(self, achievementIds, avatar):
        _takeIds = []
        _src = AAC_AAC_DD.datas.BONUS_SRC_ACHIEVEMENT
        popRewardUUID = KBEngine.genUUID64()
        for _achieveId in achievementIds:
            _achieveVal = self.achieveDic.get(_achieveId)
            if not _achieveVal:
                continue

            if not _achieveVal.isFinished():
                continue

            _rewardId = _achieveVal.configData()['reward']
            _ctx = avatar.getAvatarAwardCtx(_rewardId, None)
            _awardVal = dropAward.getAwardOne(_rewardId, _ctx)
            _opUUID = KBEngine.genUUID64()
            _detail = gameclass.AwardDetailCls(achievementId=[_achieveId], popRewardUUID=popRewardUUID)
            avatar.addWealth(_src, _awardVal, _opUUID, _detail, directly=False)

            self.popAchieveVal(_achieveId)
            if _achieveId in self.finishedIds:
                LOG_ERR('takeAllAchievementRewards but already has id', _achieveId)
                continue

            self.finishedIds.append(_achieveId)
            _takeIds.append(_achieveId)

            self.sumPoint += _achieveVal.configData()['achPoint']

            LogTrackingMgr.LogTrackingMgr.Achievement_Update(
                avatar.gbID,
                avatar.accountEntity.clientDistinctId,
                avatar.accountEntity.accountName,
                avatar.gbID,
                gameconfig.gameId(),
                _achieveVal.achieveId,
                self.maxVersion,
                gameconst.ACHIEVE_STATE_RECEIVE,
                _achieveVal.step,
                self.sumPoint
            )

        avatar._showPopReward(_src, popRewardUUID, gameclass.AwardDetailCls(achievementId=_takeIds))
        avatar.client.onTakeAchievementRewards(_takeIds, self.sumPoint)

    def sendInitDataToClient(self, avatar):
        jsonStr = json.dumps([[obj.toAchievementValSavedDict() for obj in self.achieveDic.values()], self.finishedIds, self.sumPoint]).encode('ascii')
        LOG_DBG('in sendInitDataToClient:', len(jsonStr))
        zStr = gzip.compress(jsonStr)
        LOG_DBG('in sendInitDataToClient:', len(zStr))
        avatar.streamStringProxy(zStr, '', gameconst.StreamStringID.ACHIEVEMENT_DATA)

    def __str__(self):
        return 'AchievementsVal: %s, maxVersion: %s, finishedIds: %s' % (self.achieveDic, self.maxVersion, self.finishedIds)


class AchievementsInfo(object):
    def createObjFromDict(self, dataDict):
        obj = AchievementsVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toAchievementsSavedDict()

    def isSameType(self, obj):
        return type(obj) is AchievementsVal


AchievementsInstance = AchievementsInfo()

