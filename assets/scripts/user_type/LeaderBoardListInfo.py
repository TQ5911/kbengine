
# coding: utf-8

import userType
import LeaderBoard


class LeaderBoardListVal(userType.UserListType):
    '''LEADER_BOARD_LIST_DATA_INFO'''
    def __init__(self, listData=(), leaderBoardType=0, schoolsData=()):
        self.leaderBoardType = leaderBoardType
        self.schoolsDic = {}
        _cls = self.instaniateCls()
        if not _cls:
            return

        for _data in listData:
            self.append(_cls(**_data))

        for _data in schoolsData:
            _list = []
            for _oneData in _data.get('listData', []):
                _list.append(_cls(**_oneData))

            self.schoolsDic[_data.get('school')] = _list

    def getSchoolData(self, school):
        return self.schoolsDic.get(school, [])

    def replaceSchoolData(self, school, listData):
        self.schoolsDic[school] = listData

    def instaniateCls(self):
        return LeaderBoard.TypeToDic.get(self.leaderBoardType)

    def toLeaderBoardListSavedDict(self):
        _schoolsData = []
        for _school, _list in self.schoolsDic.items():
            _schoolsData.append({
               'school': _school,
                'listData': [obj.toLeaderBoardCacheSavedDict() for obj in _list],
            })

        return {
            'listData': [obj.toLeaderBoardCacheSavedDict() for obj in self],
            'leaderBoardType': self.leaderBoardType,
            'schoolsData': _schoolsData,
        }


class LeaderBoardListInfo(object):
    def createObjFromDict(self, dataDict):
        obj = LeaderBoardListVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toLeaderBoardListSavedDict()

    def isSameType(self, obj):
        return type(obj) is LeaderBoardListVal


LeaderBoardListInstance = LeaderBoardListInfo()

