# -*- coding: utf-8 -*-

import utils
import userType
import appearance


WRITE_TO_DB_SQL_TEMP = """
INSERT INTO `game_account_characters`
(`id`, `parentID`, `gbId`, `authDbId`, `dbId`, `name`, `school`, `sex`, `level`, `tLastOnline`)
VALUES
{}
ON DUPLICATE KEY UPDATE
    `name`       = VALUES(`name`),
    `school`     = VALUES(`school`),
    `sex`        = VALUES(`sex`),
    `level`      = VALUES(`level`),
    `tLastOnline`= VALUES(`tLastOnline`);
"""


class CharacterVal(userType.UserSoleType):
    def __init__(self, gbId, dbId, school, name, sex, level, birthInDB, tLastOnline, charAppearance, selfDbId, authDbId, parentID):
        self.gbId = gbId
        self.dbId = dbId
        self.school = school
        self.name = name
        self.sex = sex
        self.level = level
        self.tLastOnline = tLastOnline
        self.birthInDB = birthInDB
        self.selfDbId = selfDbId
        self.authDbId = authDbId
        if not charAppearance:
            weapon, breast = appearance.getDefaultAppearanceEquipPartId()
            charAppearance = appearance.Appearance(weapon=weapon, breast=breast)
        self.charAppearance = charAppearance
        self.parentID = parentID
        self._dirty = False

    def setLevel(self, level):
        self.level = level
        self._dirty = True

    def setName(self, name):
        self.name = name
        self._dirty = True

    def setAuthDbId(self, authDbId):
        self.authDbId = authDbId

    def dirty(self):
        return self._dirty

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
            charAppearance,
            data['selfDbId'],
            data['authDbId'],
            data['parentID']
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
            'charAppearance': self.charAppearance,
            'selfDbId': self.selfDbId,
            'authDbId': self.authDbId,
            'parentID': self.parentID
        }

    def toSqlValues(self):
        #(`id`, `parentID`, `gbId`, `authDbId`, `dbId`, `name`, `school`, `sex`, `level`, `tLastOnline`)
        _name = utils.escape_string(self.name)
        return f'({self.selfDbId}, {self.parentID}, {self.gbId}, {self.authDbId}, {self.dbId}, {_name}, {self.school}, {self.sex}, {self.level}, {self.tLastOnline})'

    def setAppearance(self, appr):
        self.charAppearance = appr

    def _lateReload(self):
        super(CharacterVal, self)._lateReload()


class Characters(userType.UserDictType):
    def addCharacter(self, parentID, selfDbId, authDbId, gbId, dbId, school, name, sex, level, birthInDB,  charAppearance = None):
        self[gbId] = CharacterVal(gbId, dbId, school, name, sex, level, birthInDB, 0, charAppearance, selfDbId, authDbId, parentID)

    def genWriteToDBSql(self, ignoreDirty=False):
        values = []
        for cVal in self.values():
            if ignoreDirty and not cVal.dirty():
                continue

            values.append(cVal.toSqlValues())

        if not values:
            return None

        valuesStr = ','.join(values)
        sql = WRITE_TO_DB_SQL_TEMP.format(valuesStr)
        return sql

    def setSelfDbId(self, gbId, selfDbId):
        _cVal = self.get(gbId)
        if not _cVal:
            return

        _cVal.selfDbId = selfDbId

    def getZeroSelfDbIdGbIds(self):
        return [cVal.gbId for cVal in self.values() if cVal.selfDbId == 0]

    def removeCharacter(self, gbId):
        return self.pop(gbId, None)

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
