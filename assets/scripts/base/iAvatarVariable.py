# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine
import dataUtils
import gameengine
import taskVar as TVD
import formula
import value_value as V_VD
import AvatarDataVar
import value_value_def as VLVLD_DEF
import itemData_itemData as IDIDD
import gameconst


class VarCycleDef(object):
    VAR_CYCLE_DAILY = 1
    VAR_CYCLE_WEEKLY = 2


class ImpAvatarVariable(object):

    def onAvatarVariableDailyUpdate(self):
        _resetValIds = []
        _resetValVals = []
        for varId in list(self.avatarVarDict.keys()):
            varData = dataUtils.getVariableData(varId)
            if varData['cycle'] == VarCycleDef.VAR_CYCLE_DAILY:
                self.avatarVarDict.pop(varId, None)
                _resetValIds.append(varId)
                _resetValVals.append(varData['defaultValue'])
        self.onAvatarVarValueChanged(_resetValIds, _resetValVals)

    def onAvatarVariableWeeklyUpdate(self):
        _resetValIds = []
        _resetValVals = []
        for varId in list(self.avatarVarDict.keys()):
            varData = dataUtils.getVariableData(varId)
            if varData['cycle'] == VarCycleDef.VAR_CYCLE_WEEKLY:
                self.avatarVarDict.pop(varId, None)
                _resetValIds.append(varId)
                _resetValVals.append(varData['defaultValue'])
        self.onAvatarVarValueChanged(_resetValIds, _resetValVals)

    def sendVariableData(self):
        _varIdList = []
        varValueList = []
        if hasattr(V_VD, "clientValueSet"):
            for varId in V_VD.clientValueSet:
                value = self.getVariable(varId)
                if value is None:
                    gameengine.panicStack('sendVariableData, variable is None:', varId)
                    continue
                _varIdList.append(varId)
                varValueList.append(value)
        self.client.onGetVariableData(_varIdList, varValueList)

    def getVariable(self, varId, default=None):
        if varId in V_VD.AvatarDataVarIdDic:
            # 与角色数据关联的变量
            charDataName = V_VD.AvatarDataVarIdDic[varId]
            _varFunc = AvatarDataVar.AvatarDataVarFunDic.get(charDataName)
            if not _varFunc:
                return default
            return _varFunc(self, varId)
        elif dataUtils.isAvatarVar(varId):
            return self.avatarVarDict.get(varId, dataUtils.getVariableDefaultVal(varId))
        elif dataUtils.isSpaceVar(varId):
            _dungeonNo = dataUtils.getVariableData(varId)['cntGamePlay']
            return self.spaceVarDic.get(_dungeonNo, {}).get(varId, dataUtils.getVariableDefaultVal(varId))
        else:
            return default

    def setAvatarVariableByTag(self, varName, newVal, opUUID, valueSrc, desc):
        LOG_INFO('in setAvatarVariableByTag:', varName, newVal, valueSrc, desc)
        valIdList = V_VD.varTagDic.get(varName, [])
        for valId in valIdList:
            self.setAvatarVariable(valId, newVal, opUUID, valueSrc, desc)

    def incAvatarVariable(self, varId, deltaVal, opUUID, valueSrc, desc):
        # 变量值累加
        LOG_INFO('in incAvatarVariable:', varId, deltaVal, valueSrc, desc)
        _oldVal = self.getVariable(varId)
        self.setAvatarVariable(varId, _oldVal + deltaVal, opUUID, valueSrc, desc)

    def setAvatarVariable(self, varId, newVal, opUUID, varSrc, desc):
        LOG_INFO('in setAvatarVariable:', varId, newVal, varSrc, desc)
        # avatarVarDict 保存 avatar私有变量，包括avatar的非base属性及数据关联的变量；
        # avatar的base属性及数据关联的变量不需要保存在 avatarVarDict
        if not dataUtils.isAvatarVar(varId):
            return

        charDataName = V_VD.AvatarDataVarIdDic.get(varId)
        if charDataName:
            # 与角色数据关联的变量
            _varFunc = AvatarDataVar.AvatarDataVarFunDic.get(charDataName)
            if not _varFunc:
                gameengine.panicStack('   setAvatarVariable, charprop var has not _varFunc')
                return

        _oldVal = self.getVariable(varId)
        if _oldVal == newVal:
            return
        self.avatarVarDict[varId] = newVal
        LOG_INFO('     setAvatarVariable, varId:{} {} ==> {}'.format(varId, _oldVal, newVal))
        self.onAvatarVarValueChanged([varId], [newVal])
        return

    def onAvatarVarValueChanged(self, varIdList, varValueList):
        # avatar变量发生变化的回调， space变量不要调该接口
        LOG_INFO('in onAvatarVarValueChanged:', varIdList, varValueList)
        _cliValIdList = []
        cliValValueList = []
        for varId, varValue in zip(varIdList, varValueList):
            self.checkTaskVar(varId)
            if hasattr(V_VD, "clientValueSet"):
                if varId in V_VD.clientValueSet:
                    _cliValIdList.append(varId)
                    cliValValueList.append(varValue)

        if _cliValIdList and cliValValueList:
            self.client.onVariableChanged(_cliValIdList, cliValValueList)

    def checkTaskVar(self, varId):
        _taskIds = TVD.datas.get('succOrFailCondVar', {}).get(str(varId), [])
        for _taskId in _taskIds:
            self.onTaskVarChanged(_taskId, varId)
        self.triggerAutoClaimTask(TVD.datas.get('autoClaimCondVar', {}).get(str(varId), ()))

    def checkAvatarVariable(self, varId, methodName, args):
        _val = self.getVariable(varId)
        if _val is None:
            if methodName:
                getattr(self.cell, methodName)(False, 0, *args)
        else:
            if methodName:
                getattr(self.cell, methodName)(True, _val, *args)

    def updateHomeAdvMonsterNumAvatarVar(self, newMonsterNumber, src, opUUID=None, desc=None):
        LOG_INFO("updateHomeAdvMonsterNumAvatarVar::", newMonsterNumber)
        mVarId = VLVLD_DEF.datas.amountPillarSpirits
        mNewMonsterNum = self.getVariable(mVarId, -1)
        if mNewMonsterNum < 0:
            mNewMonsterNum = 0
        else:
            mNewMonsterNum += newMonsterNumber

        mNewMonsterNum = max(mNewMonsterNum, 0)
        opUUID = opUUID or KBEngine.genUUID64()
        desc = desc or ""
        self.setAvatarVariable(mVarId, mNewMonsterNum, opUUID, src, desc)

    def onVarItemCountChanged(self, itemIdList):
        for _checkItemId in itemIdList:
            if _checkItemId not in IDIDD.petEggItems:
                continue

            self.onAvatarVarValueChanged(
                [V_VD.AvatarDataVarPropDic['amountFistPetEgg']],
                [self.bagData.getItemCount(self.gbID, _checkItemId,
                gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED, ignoreCheck=True)])

    def updateFengLingZhouSpHelpCountAvatarVar(self, fengLingZhouSpHelpCount, src, opUUID=None, desc=None):
        LOG_INFO("updateFengLingZhouSpHelpCountAvatarVar::", fengLingZhouSpHelpCount)
        mVarId = VLVLD_DEF.datas.fengLingZhouSpecialTask
        mNewHelpCount = self.getVariable(mVarId, -1)
        if mNewHelpCount < 0 or src in (
        gameconst.VarChangeSrcEnum.VAR_SRC_TASK_QUIT, gameconst.VarChangeSrcEnum.VAR_SRC_TASK_SUBMIT):
            mNewHelpCount = 0
        else:
            mNewHelpCount = max(fengLingZhouSpHelpCount, mNewHelpCount)

        opUUID = opUUID or KBEngine.genUUID64()
        desc = desc or ""
        self.setAvatarVariable(mVarId, mNewHelpCount, opUUID, src, desc)

    #################################### space 变量 #################################
    def syncSpaceVariable(self, spaceNo, varDic):
        LOG_INFO('in syncSpaceVariable:', spaceNo, varDic)
        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        self.spaceVarDic.setdefault(dungeonNo, {})
        _varIdList = []
        varValueList = []
        for varId, newVal in varDic.items():
            if not dataUtils.isSpaceVar(varId):
                continue
            _oldVal = self.getVariable(varId)
            if _oldVal == newVal:
                continue
            self.spaceVarDic[dungeonNo][varId] = newVal
            _varIdList.append(varId)
            varValueList.append(newVal)
        self.client.onVariableChanged(_varIdList, varValueList)
        for varId in _varIdList:
            self.checkTaskVar(varId)
        return

    def clearSpaceVariable(self, dungeonNo):
        LOG_INFO('in clearSpaceVariable:', dungeonNo)
        # dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        varDic = self.spaceVarDic.pop(dungeonNo, None)
        if not varDic:
            return
        _varIdList = []
        varValueList = []
        for varId, newVal in varDic.items():
            _varIdList.append(varId)
            varValueList.append(0)
        LOG_INFO('in clearSpaceVariable:', _varIdList, varValueList)
        self.client.onVariableChanged(_varIdList, varValueList)

    #################################### space 变量 end #################################

    #################################### gm 指令 #################################
    def gmSetVar(self, varId, newVar, opUUID, varSrc, desc):
        LOG_INFO('in gmSetVar:', varId, newVar)
        if dataUtils.isAvatarVar(varId):
            self.setAvatarVariable(varId, newVar, opUUID, varSrc, '')

    def gmGetVar(self, varId):
        _val = self.getVariable(varId)
        if _val is None:
            return False, 'no this val'
        else:
            return True, str(_val)
    #################################### gm 指令 end #################################
