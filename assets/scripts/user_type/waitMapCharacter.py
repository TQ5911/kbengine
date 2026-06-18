# -*- coding: utf-8 -*-
import userType
import appearance


class WaitMapCharacter(object):
    def __init__(self, gbid=0, name='', level=0, sex=0, school=0, guildname='', ap=None):
        self.gbid = gbid
        self.name = name
        self.level = level
        self.sex = sex
        self.school = school
        self.guildname = guildname
        self.appearance = ap or appearance.Appearance()

    def toSavedDict(self):
        return {
            'gbId': self.gbid,
            'name': self.name,
            'level': self.level,
            'sex': self.sex,
            'school': self.school,
            'guildName': self.guildname,
            'appearance': self.appearance,
        }

    def initFromDict(self, dic):
        self.gbid = dic.get('gbid', 0)
        self.name = dic.get('name', '')
        self.level = dic.get('level', 0)
        self.sex = dic.get('sex', 0)
        self.school = dic.get('school', 0)
        self.guildname = dic.get('guildname', '')
        self.appearance = dic.get('appearance', appearance.Appearance())
        return self


class WaitMapCharacterInfo(object):
    def createObjFromDict(self, dic):
        return WaitMapCharacter().initFromDict(dic)

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is WaitMapCharacter


instance = WaitMapCharacterInfo()
