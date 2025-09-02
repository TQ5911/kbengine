# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine
import dataUtils
import gamelog
import gameengine
import taskVar as TVD
import formula
import value_value as VLVLD
import AvatarDataVar
import value_value_def as VLVLD_DEF
import gameconst
import itemData_itemData as IDIDD


class VarCycleDef(object):
    VAR_CYCLE_DAILY = 1
    VAR_CYCLE_WEEKLY = 2


class ImpAvatarVariable(object):

    def onAvatarVariableDailyUpdate(self):
        resetValIds = []
        resetValVals = []
        for varId in list(self.avatarVarDic.keys()):
            varData = dataUtils.getVariableData(varId)
            if varData['cycle'] == VarCycleDef.VAR_CYCLE_DAILY:
                self.avatarVarDic.pop(varId, None)
                resetValIds.append(varId)
                resetValVals.append(varData['defaultValue'])
        self.onAvatarVarValueChanged(resetValIds, resetValVals)
        return

    def onAvatarVariableWeeklyUpdate(self):
        resetValIds = []
        resetValVals = []
        for varId in list(self.avatarVarDic.keys()):
            varData = dataUtils.getVariableData(varId)
            if varData['cycle'] == VarCycleDef.VAR_CYCLE_WEEKLY:
                self.avatarVarDic.pop(varId, None)
                resetValIds.append(varId)
                resetValVals.append(varData['defaultValue'])
        self.onAvatarVarValueChanged(resetValIds, resetValVals)
        return

    def sendVariableData(self):
        varIdList = []
        varValueList = []
        if hasattr(VLVLD, "clientValueSet"):
            for varId in VLVLD.clientValueSet:
                value = self.getVariable(varId)
                if value is None:
                    gameengine.reportCritical('sendVariableData, variable is None:', varId)
                    continue
                varIdList.append(varId)
                varValueList.append(value)
        self.client.onGetVariableData(varIdList, varValueList)
        return

    def getVariable(self, varId, default=None):
        if varId in VLVLD.AvatarDataVarIdDic:
            # 与角色数据关联的变量
            charDataName = VLVLD.AvatarDataVarIdDic[varId]
            varFunc = AvatarDataVar.AvatarDataVarFunDic.get(charDataName)
            if not varFunc:
                return default
            return varFunc(self, varId)
        elif dataUtils.isAvatarVar(varId):
            return self.avatarVarDic.get(varId, dataUtils.getVariableDefaultVal(varId))
        elif dataUtils.isSpaceVar(varId):
            dungeonNo = dataUtils.getVariableData(varId)['cntGamePlay']
            return self.spaceVarDic.get(dungeonNo, {}).get(varId, dataUtils.getVariableDefaultVal(varId))
        else:
            return default

    def incAvatarVariableByTag(self, varName, deltaVal, opUUID, valueSrc, desc):
        DEBUG_MSG('in incAvatarVariableByTag:', varName, deltaVal, valueSrc, desc)
        valIdList = VLVLD.varTagDic.get(varName, [])
        for valId in valIdList:
            self.incAvatarVariable(valId, deltaVal, opUUID, valueSrc, desc)
        return

    def setAvatarVariableByTag(self, varName, newVal, opUUID, valueSrc, desc):
        DEBUG_MSG('in setAvatarVariableByTag:', varName, newVal, valueSrc, desc)
        valIdList = VLVLD.varTagDic.get(varName, [])
        for valId in valIdList:
            self.setAvatarVariable(valId, newVal, opUUID, valueSrc, desc)
        return

    def incAvatarVariable(self, varId, deltaVal, opUUID, valueSrc, desc):
        # 变量值累加
        DEBUG_MSG('in incAvatarVariable:', varId, deltaVal, valueSrc, desc)
        oldVal = self.getVariable(varId)
        self.setAvatarVariable(varId, oldVal + deltaVal, opUUID, valueSrc, desc)
        return

    def setAvatarVariable(self, varId, newVal, opUUID, varSrc, desc):
        DEBUG_MSG('in setAvatarVariable:', varId, newVal, varSrc, desc)
        # avatarVarDic 保存 avatar私有变量，包括avatar的非base属性及数据关联的变量；
        # avatar的base属性及数据关联的变量不需要保存在 avatarVarDic
        if not dataUtils.isAvatarVar(varId):
            return

        charDataName = VLVLD.AvatarDataVarIdDic.get(varId)
        if charDataName:
            # 与角色数据关联的变量
            varFunc = AvatarDataVar.AvatarDataVarFunDic.get(charDataName)
            if not varFunc:
                gameengine.reportCritical('   setAvatarVariable, charprop var has not varFunc')
                return

        oldVal = self.getVariable(varId)
        if oldVal == newVal:
            return
        self.avatarVarDic[varId] = newVal
        DEBUG_MSG('     setAvatarVariable, varId:{} {} ==> {}'.format(varId, oldVal, newVal))
        self.onAvatarVarValueChanged([varId], [newVal])
        return

    def onAvatarVarValueChanged(self, varIdList, varValueList):
        # avatar变量发生变化的回调， space变量不要调该接口
        DEBUG_MSG('in onAvatarVarValueChanged:', varIdList, varValueList)
        cliValIdList = []
        cliValValueList = []
        for varId, varValue in zip(varIdList, varValueList):
            self.checkTaskVar(varId)
            if hasattr(VLVLD, "clientValueSet"):
                if varId in VLVLD.clientValueSet:
                    cliValIdList.append(varId)
                    cliValValueList.append(varValue)

        if cliValIdList and cliValValueList:
            self.client.onVariableChanged(cliValIdList, cliValValueList)
        return

    def checkTaskVar(self, varId):
        taskIds = TVD.datas.get('succOrFailCondVar', {}).get(str(varId), [])
        for taskId in taskIds:
            self.onTaskVarChanged(taskId, varId)
        self.triggerAutoClaimTask(TVD.datas.get('autoClaimCondVar', {}).get(str(varId), []))
        return

    def checkAvatarVariable(self, varId, methodName, args):
        val = self.getVariable(varId)
        if val is None:
            methodName and getattr(self.cell, methodName)(False, 0, *args)
        else:
            methodName and getattr(self.cell, methodName)(True, val, *args)
        return

    def updateHomeAdvMonsterNumAvatarVar(self, newMonsterNumber, src, opUUID=None, desc=None):
        DEBUG_MSG("updateHomeAdvMonsterNumAvatarVar::", newMonsterNumber)
        m_varId = VLVLD_DEF.datas.amountPillarSpirits
        m_newMonsterNum = self.getVariable(m_varId, -1)
        if m_newMonsterNum < 0:
            m_newMonsterNum = 0
        else:
            m_newMonsterNum += newMonsterNumber

        m_newMonsterNum = max(m_newMonsterNum, 0)
        opUUID = opUUID or KBEngine.genUUID64()
        desc = desc or ""
        self.setAvatarVariable(m_varId, m_newMonsterNum, opUUID, src, desc)

    def onVarItemCountChanged(self, itemIdList):
        for checkItemId in itemIdList:
            if checkItemId in IDIDD.petEggItems:
                self.onAvatarVarValueChanged([VLVLD.AvatarDataVarPropDic['amountFistPetEgg']],
                                             [self.bagData.getItemCount(checkItemId,
                                                                        gameconst.ItemBindType.BINDTYPE_NOT_SPECIFIED)])

    def updateFengLingZhouSpHelpCountAvatarVar(self, fengLingZhouSpHelpCount, src, opUUID=None, desc=None):
        DEBUG_MSG("updateFengLingZhouSpHelpCountAvatarVar::", fengLingZhouSpHelpCount)
        m_varId = VLVLD_DEF.datas.fengLingZhouSpecialTask
        m_newHelpCount = self.getVariable(m_varId, -1)
        if m_newHelpCount < 0 or src in (
        gameconst.VarChangeSrc.VAR_SRC_TASK_QUIT, gameconst.VarChangeSrc.VAR_SRC_TASK_SUBMIT):
            m_newHelpCount = 0
        else:
            m_newHelpCount = max(fengLingZhouSpHelpCount, m_newHelpCount)

        opUUID = opUUID or KBEngine.genUUID64()
        desc = desc or ""
        self.setAvatarVariable(m_varId, m_newHelpCount, opUUID, src, desc)

    #################################### space 变量 #################################
    def syncSpaceVariable(self, spaceNo, varDic):
        DEBUG_MSG('in syncSpaceVariable:', spaceNo, varDic)
        dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        self.spaceVarDic.setdefault(dungeonNo, {})
        varIdList = []
        varValueList = []
        for varId, newVal in varDic.items():
            if not dataUtils.isSpaceVar(varId):
                continue
            oldVal = self.getVariable(varId)
            if oldVal == newVal:
                continue
            self.spaceVarDic[dungeonNo][varId] = newVal
            varIdList.append(varId)
            varValueList.append(newVal)
        self.client.onVariableChanged(varIdList, varValueList)
        for varId in varIdList:
            self.checkTaskVar(varId)
        return

    def clearSpaceVariable(self, dungeonNo):
        DEBUG_MSG('in clearSpaceVariable:', dungeonNo)
        # dungeonNo = formula.getDungeonNoBySpaceNo(spaceNo)
        varDic = self.spaceVarDic.pop(dungeonNo, None)
        if not varDic:
            return
        varIdList = []
        varValueList = []
        for varId, newVal in varDic.items():
            varIdList.append(varId)
            varValueList.append(0)
        DEBUG_MSG('in clearSpaceVariable:', varIdList, varValueList)
        self.client.onVariableChanged(varIdList, varValueList)

    #################################### space 变量 end #################################

    #################################### gm 指令 #################################
    def gmSetVar(self, varId, newVar, opUUID, varSrc, desc):
        DEBUG_MSG('in gmSetVar:', varId, newVar)
        if dataUtils.isAvatarVar(varId):
            self.setAvatarVariable(varId, newVar, opUUID, varSrc, '')

        return

    def gmGetVar(self, varId):
        val = self.getVariable(varId)
        if val is None:
            return False, 'no this val'
        else:
            return True, str(val)
    #################################### gm 指令 end #################################
