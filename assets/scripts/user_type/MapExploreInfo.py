
# coding: utf-8

import userType
import gameconst
import gamePlay_explorationRate as GED
import gamePlay_explorationReward as GER


class MapExploreVal(userType.UserSingleType):
    '''MAP_EXPLORE_DATA_INFO'''
    def __init__(self, mapId, personalBox, viewPoint, hookTask, areaTask, rewardData, rewardSlot):
        self.mapId = mapId
        self.personalBox = personalBox
        self.viewPoint = viewPoint
        self.hookTask = hookTask
        self.areaTask = areaTask
        self.rewardData = rewardData
        self.rewardSlot = rewardSlot

    def toMapExploreSavedDict(self):
        return {
            'mapId': self.mapId,
            'personalBox': self.personalBox,
            'viewPoint': self.viewPoint,
            'hookTask': self.hookTask,
            'areaTask': self.areaTask,
            'rewardData': self.rewardData,
            'rewardSlot': self.rewardSlot
        }


class MapExploreInfo(object):
    def createObjFromDict(self, dataDict):
        obj = MapExploreVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toMapExploreSavedDict()

    def isSameType(self, obj):
        return type(obj) is MapExploreVal


MapExploreInstance = MapExploreInfo()

class MapExploreDictVal(userType.UserSingleType):
    '''MAP_EXPLORE_DICT'''
    def __init__(self, mapIds, dataList):
        self.mapIds = mapIds
        self.dataList = dataList
        self.mapDatas = {}
        for i in range(len(self.mapIds)):
            self.mapDatas[self.mapIds[i]] = self.dataList[i]

    def toMapExploreDictSavedDict(self):
        return {
            'mapIds': self.mapIds,
            'dataList': self.dataList
        }
    
    def checkNewMapExploreData(self):
        for mapId, ids in GED.mapId2Ids.items():
            if mapId not in self.mapDatas:
                personalBox = [0, 5]
                viewPoint = [0, 5]
                hookTask = [0, 5]
                areaTask = [0, 5]
                rewardData = [0, 90]
                for id in ids:
                    targetType = GED.datas[id]['targetType']
                    if targetType == gameconst.AchieveType.PERSONAL_BOX:
                        personalBox = [0, GED.datas[id]['targetParam'][0]]
                    elif targetType == gameconst.AchieveType.VIEWPOINT:
                        viewPoint = [0, GED.datas[id]['targetParam'][0]]
                    elif targetType == gameconst.AchieveType.HOOK_TASK_REWARD:
                        hookTask = [0, GED.datas[id]['targetParam'][0]]
                    elif targetType == gameconst.AchieveType.AREA_TASK:
                        areaTask = [0, GED.datas[id]['targetParam'][0]]
                rewardDataIds = GER.mapId2Ids[mapId]
                rewardData[-1] = GER.datas[rewardDataIds[-1]]['acPoint']
                self.mapDatas[mapId] = MapExploreVal(mapId=mapId, personalBox=personalBox, viewPoint=viewPoint, hookTask=hookTask,\
                    areaTask=areaTask, rewardData=rewardData, rewardSlot=-1)
                self.mapIds.append(mapId)
                self.dataList.append(self.mapDatas[mapId])


class MapExploreDictInfo(object):
    def createObjFromDict(self, dataDict):
        obj = MapExploreDictVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toMapExploreDictSavedDict()

    def isSameType(self, obj):
        return type(obj) is MapExploreDictVal


MapExploreDictInstance = MapExploreDictInfo()