# -*- encoding:utf-8 -*-

from KBEDebug import *
import KBEngine

import userType
import gameconst

import petData_petData as PDPD
import petData_set as PDSD
import gametimer
import petData_unlock as PDUD
import petData_petGear as PDPGD
import itemData_itemData_set as IDIDS

import dataUtils
import LogTrackingMgr

class LingShou(userType.UserSoleType):
    def __init__(self, *args, **kwargs):
        super(LingShou, self).__init__(*args, **kwargs)
        self._score = 0

    @property
    def grade(self):
        return PDPD.datas[self.petId]['grade']

    @property
    def quality(self):
        return PDPD.datas[self.petId]['petRank']
    
    def _getLingShouScore(self):
        score = 0
        skill = PDPD.datas[self.petId]['skill']
        if type(skill) is int:
            skill = (skill,)
        for skillId in skill:
            score += dataUtils.getPassiveSkillScore(self.school, skillId)

        for itemId in self.equipList:
            if itemId:
                passiveSkill = PDPGD.datas[itemId]['passiveSkill']
                score += dataUtils.getPassiveSkillScore(self.school, passiveSkill)

        score += PDPD.datas[self.petId]['score']
        
        petCfg = PDPD.datas.get(self.petId, None)
        if petCfg:
            levelPropList = petCfg['levelProp']
            if levelPropList:
                levelAddScore = 0
                minLevel = int(PDSD.datas['petMinLevel']['value'])
                for propName, val in levelPropList:
                    minLevel += 1
                    if minLevel > self.level:
                        break
                    levelAddScore += dataUtils.calcFightPropScore(self.school, propName, val)
                score += levelAddScore
                INFO_MSG("_getLingShouScore", levelAddScore, score)
        return score

    def _getBaseLingShouScore(self):
        totalScore = 0
        petData = PDPD.datas[self.petId]
        prop = petData.get('prop', [])
        for propName, val in prop:
            totalScore += dataUtils.calcFightPropScore(self.school, propName, val)

        return totalScore

    def updateLingShouScore(self, owner):
        # oldValue = self.score
        newValue = self._getLingShouScore()
        self.score = newValue

        owner.updatePetScore()

    def updateLingShouBaseScore(self):
        self.baseScore = self._getBaseLingShouScore()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, newScore):
        self._score = newScore

    def initFromDict(self, dataDict):
        self.petId = dataDict['petId']
        self.equipList = dataDict['equipList']
        # 这里兼容处理
        gearNum = dataUtils.getPetGearNum(self.petId)
        expandCount = gearNum - len(self.equipList)
        if expandCount > 0:
            # 扩容处理
            petEquipStatus = dataUtils.getPetEquipDefaultStatus()
            for _ in range(0, expandCount):
                self.equipList.append(petEquipStatus)

        self.school = dataDict.get('school', 0)
        minLevel = int(PDSD.datas['petMinLevel']['value'])
        self.level = dataDict.get('level', minLevel)
        self.exp = dataDict.get('exp', 0)
        self.baseScore = self._getBaseLingShouScore()
        self._score = self._getLingShouScore()

    def _lateReload(self):
        super(LingShou, self)._lateReload()

        return

    # 服务器解析的数据结构可以和前端不一样,增加petMirror节点只做缓存不做入库处理以便通过checkProperty的检查
    def toSavedDict(self):
        retDt = self.toClientDict()
        retDt['school'] = self.school
        return retDt

    def toClientDict(self):
        return {
            'petId': self.petId,
            'equipList': self.equipList,
            'level': self.level,
            'exp': self.exp
        }

    def toClientData(self):
        clientData = self.toClientDict()
        clientData.update({
            'score': self.score,
            #'score': self.score + self.baseScore,
        })
        return clientData

    def canReplaceEquip(self, slotId, itemId):
        if slotId < 0:
            return False

        if slotId >= len(self.equipList):
            return False

        if itemId in self.equipList:
            return False

        return True

    def modifyPetEquip(self, owner, slotId, itemId):
        self.equipList[slotId] = itemId
        self.updateLingShouScore(owner)
        owner.client.onUpdateLingShouEquip(self.petId, slotId, itemId)
        if owner.lingShouInfo.isInBattleList(owner, self.petId):
            petSlotId = owner.lingShouInfo.getSlotIdByPetId(self.petId, owner.battleIndex)
            owner.cell.onUpdateLingShouBattleList((self.petId, self.equipList), petSlotId)
    
    def getLevel(self):
        return self.level

    def getExp(self):
        return self.exp
    
    def setLevelAndExp(self, level, exp, owner):
        self.level = level
        self.exp = exp
        self.updateLingShouScore(owner)
    
class LingShouBattleListVal(userType.UserSoleType):
    def __init__(self, battleName, petIdList):
        self.battleName = battleName
        self.petIdList = petIdList

    def toClientData(self):
        dic = {
            'name': self.battleName,
            'petIdList': self.petIdList
        }
        return dic

    def setPetIdBySlot(self, petId, slotId):
        self.petIdList[slotId] = petId

    def getPetIdBySlot(self, slotId):
        for i in range(len(self.petIdList)):
            if i == slotId:
                return self.petIdList[i]
        return 0

    def setBattleName(self, name):
        self.battleName = name

    def getPetCount(self):
        totalCount = 0
        for v in self.petIdList:
            if v > 0:
                totalCount += 1
        return totalCount

    def checkPet(self, petId):
        for d in self.petIdList:
            if d == petId:
                return True
        return False 

class LingShouInfo(userType.UserSoleType):
    def __init__(self):
        self.pets = {}
        self.battleList = []

    def _lateReload(self):
        super(LingShouInfo, self)._lateReload()

        for v in self.pets.values():
            v.reloadScript()

        return

    # db -> obj
    def initFromDict(self, savedDataDict):
        for dataDict in savedDataDict['lingShouList']:
            pet = LingShou()
            pet.initFromDict(dataDict)
            self.pets[dataDict['petId']] = pet

        for battleList in savedDataDict['battleList']:
            battleListVal = LingShouBattleListVal(battleList['name'], battleList['petIdList'])
            self.battleList.append(battleListVal)

    # obj -> db
    def toSavedDict(self):
        lingShouList = []
        for pet in self.pets.values():
            lingShouList.append(pet.toSavedDict())

        battleList = []
        for val in self.battleList:
            battleList.append(val.toClientData())

        return {
            'lingShouList': lingShouList,
            'battleList': battleList,
        }

    def toClientData(self, petIds=None):
        if not petIds:
            petIds = self.pets.keys()

        lingShouList = []
        for petId in petIds:
            lingShouList.append(self.pets[petId].toClientData())

        return lingShouList

    def lingShouNum(self):
        return len(self.pets)

    def sendLingShouData(self, owner):
        sendDic = {}
        sendNum = 0
        for petId, pet in self.pets.items():
            key = int(sendNum / 10)
            lingShouList = sendDic.get(key, [])
            lingShouList.append(pet)
            sendDic[key] = lingShouList
            sendNum += 1
        for key, petList in sendDic.items():
            if not key:
                owner._sendLingShouData(petList)
            else:
                owner._callback(key * 0.1, '_sendLingShouData', (petList,), gametimer.TIMER_TAG_SEND_LING_SHOU_DATA)

        owner._callback((int(sendNum / 10) + 1) * 0.1, '_sendBattleListData', (),
                        gametimer.TIMER_TAG_SEND_LING_SHOU_DATA)

    def sendBattleListData(self, owner):
        battleList = []
        for val in self.battleList:
            battleList.append(val.toClientData())
        owner.client.onGetLingShouBattleList(battleList)

    def _addLingShou(self, owner, addContext):
        pet = addContext.pet
        self.pets[pet.petId] = pet
        pet.updateLingShouBaseScore()
        owner.client.onUpdateLingShouData(self.toClientData([pet.petId]))

        pet.updateLingShouScore(owner)
        owner.onMessagePre(PDSD.datas['petUnlockTips']['value'], [str(IDIDS.petIndexDatas[pet.petId])])

        LogTrackingMgr.LogTrackingMgr.Pet_Get(owner.gbID, pet.petId, pet.quality, addContext.reason)

    def addLingShou(self, owner, addContext):
        pet = LingShou()
        data = addContext.extra['item'].attr2LingShouData()
        data['school'] = addContext.extra['school']
        pet.initFromDict(data)

        addContext.setPet(pet)
        self._addLingShou(owner, addContext)

    def getBattleListByIndex(self, battleIndex):
        return self.battleList[battleIndex].petIdList

    def getTotalPetScore(self, owner):
        totalScore = 0
        for pet in self.pets.values():
            totalScore += pet.baseScore
        for petId in self.battleList[owner.battleIndex].petIdList:
            pet = self.pets.get(petId, None)
            if pet:
                totalScore += pet.score
        return totalScore

    def getLingShouByPetId(self, petId):
        return self.pets.get(petId, None)

    def isInBattleList(self, owner, petId):
        if petId in self.battleList[owner.battleIndex].petIdList:
            return True
        return False

    # --------------- battle list -------------------
    @staticmethod
    def isSlotValid(slotId):
        return slotId < PDUD.maxKey

    @staticmethod
    def isBattleIndexValid(index):
        petTeamNum = PDSD.datas['petTeamNum']['value']
        return index < petTeamNum

    def updateBattleList(self, owner, battleIndex, slotId, petId):
        INFO_MSG("updateBattleList", battleIndex, slotId, petId)
        oldPetId = self.battleList[battleIndex].getPetIdBySlot(slotId)
        self.battleList[battleIndex].setPetIdBySlot(petId, slotId)
        battleType = gameconst.PetMakeTeamType.LEAVE
        if petId > 0:
            battleType = gameconst.PetMakeTeamType.JOIN
        petLevel = 0
        petQuality = 0
        # 如果是取消出战，那就用旧的宠物数据
        if battleType == gameconst.PetMakeTeamType.LEAVE:
            petId = oldPetId
        # 这里玩家可能重复取消，避免一下，只有真正取消出战和出战上阵才记录
        petData = self.getLingShouByPetId(petId)
        if petData:
            petLevel = petData.level
            petQuality = petData.quality
            joinBattleCount = 0
            for v in self.battleList:
                if v.checkPet(petId):
                    joinBattleCount += 1
            battleCount = self.battleList[battleIndex].getPetCount()

            LogTrackingMgr.LogTrackingMgr.Pet_MakeTeam(owner.gbID, owner.getAvatarLevel(), battleIndex, battleType, \
                                                    petId, petQuality, petLevel, battleType, joinBattleCount, battleCount)
        
        owner.client.onUpdateLingShouBattleList(battleIndex, petId, slotId)

    def modifyBattleListName(self, battleIndex, name):
        self.battleList[battleIndex].setBattleName(name)

    def getSlotIdByPetId(self, petId, battleListIndex):
        return self.battleList[battleListIndex].petIdList.index(petId)
    # --------------- battle list -------------------
