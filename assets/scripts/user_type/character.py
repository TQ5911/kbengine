# -*- coding: utf-8 -*-

import userType
import appearance


class CharacterVal(userType.UserSoleType):
    def __init__(self, gbId, dbId, school, name, sex, level, birthInDB, tLastOnline, charAppearance):
        self.gbId = gbId
        self.dbId = dbId
        self.school = school
        self.name = name
        self.sex = sex
        self.level = level
        self.tLastOnline = tLastOnline
        self.birthInDB = birthInDB
        if not charAppearance:
            weapon, breast = appearance.getDefaultAppearanceEquipPartId()
            charAppearance = appearance.Appearance(weapon=weapon, breast=breast)
        self.charAppearance = charAppearance

    @staticmethod
    def fromSavedData(data):
        charAppearance = appearance.Appearance()
        charAppearance.initFromDict(data['charAppearance'])
        return CharacterVal(
            data['gbId'],
            data['dbId'],
            data['school'],
            data['name'],
            data['sex'],
            data['level'],
            data['birthInDB'],
            data['tLastOnline'],
            charAppearance
        )

    def toSavedData(self):
        return {
            'gbId': self.gbId,
            'dbId': self.dbId,
            'school': self.school,
            'name': self.name,
            'sex': self.sex,
            'level': self.level,
            'tLastOnline': self.tLastOnline,
            'birthInDB': self.birthInDB,
            'charAppearance': self.charAppearance.toSavedDict()
        }

    def setAppearance(self, appr):
        self.charAppearance = appr

    def _lateReload(self):
        super(CharacterVal, self)._lateReload()


class Characters(userType.UserDictType):
    def addCharacter(self, gbId, dbId, school, name, sex, level, birthInDB,  charAppearance = None):
        self[gbId] = CharacterVal(gbId, dbId, school, name, sex, level, birthInDB, 0, charAppearance)

    def removeCharacter(self, gbId):
        self.pop(gbId, None)

    def modifyCharacterName(self, gbId, name):
        cVal = self.get(gbId)
        if not cVal:
            return

        cVal.name = name

    def _lateReload(self):
        super(Characters, self)._lateReload()

        for v in self.values():
            v.reloadScript()

        return
