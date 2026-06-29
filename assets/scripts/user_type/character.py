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


class CharacterVal(userType.UserSingleType):
    def __init__(self, gbId=0, dbId=0, school=0, name='', sex=0, level=0, birthInDB=0,
                 tLastOnline=0, charAppearance=None, selfDbId=0, authDbId=0, authExpire=0, parentID=0):
        self.gbId = gbId
        # avatar的dbid
        self.dbId = dbId
        self.school = school
        self.name = name
        self.sex = sex
        self.level = level
        self.tLastOnline = tLastOnline
        self.birthInDB = birthInDB
        # game_account_characters 中的 数据的dbid
        self.selfDbId = selfDbId
        # 代理人的account的dbid
        self.authDbId = authDbId
        self.authExpire = authExpire
        if not charAppearance:
            weapon, breast = appearance.getDefaultAppearanceEquipPartId()
            charAppearance = appearance.Appearance(weapon=weapon, breast=breast)
        self.charAppearance = charAppearance
        # account 的 dbid
        self.parentID = parentID
        self._dirty = False

    def setDirty(self):
        self._dirty = True

    def setLevel(self, level):
        self.level = level
        self._dirty = True

    def setName(self, name):
        self.name = name
        self._dirty = True

    def setAuthDbId(self, authDbId, authExpire):
        self.authDbId = authDbId
        self.authExpire = authExpire

    def dirty(self):
        return self._dirty

    def clone(self):
        return CharacterVal(
            self.gbId,
            self.dbId,
            self.school,
            self.name,
            self.sex,
            self.level,
            self.birthInDB,
            self.tLastOnline,
            self.charAppearance.clone(),
            self.selfDbId,
            self.authDbId,
            self.authExpire,
            self.parentID
        )

    @staticmethod
    def fromSavedData(data):
        return CharacterVal(
            data['gbId'],
            data['dbId'],
            data['school'],
            data['name'],
            data['sex'],
            data['level'],
            data['birthInDB'],
            data['tLastOnline'],
            data['charAppearance'],
            data['selfDbId'],
            data['authDbId'],
            data['authExpire'],
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
            'authExpire': self.authExpire,
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
    def addCharacter(self, parentID=0, selfDbId=0, authDbId=0, authExpire=0,
            gbId=0, dbId=0, school=0, name='', sex=0, level=0, birthInDB=0,
            charAppearance = None):

        self[gbId] = CharacterVal(
            gbId=gbId, dbId=dbId, school=school, name=name, sex=sex, level=level, birthInDB=birthInDB,
            tLastOnline=0, charAppearance=charAppearance, selfDbId=selfDbId, authDbId=authDbId, authExpire=authExpire, parentID=parentID)

        self[gbId].setDirty()

    def addByCharObj(self, gbId, charObj):
        # 这里需要clone，因为很可能两个account是在同个进程，
        # 如果在同个进程，修改一个，另一个也会受影响
        self[gbId] = charObj.clone()

    def genWriteToDBSql(self, onlyDirty=False):
        values = []
        for cVal in self.values():
            if onlyDirty:
                if cVal.dirty():
                    values.append(cVal.toSqlValues())
            else:
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
        _cVal = self.get(gbId)
        if not _cVal:
            return

        _cVal.name = name

    def _lateReload(self):
        super(Characters, self)._lateReload()

        for _v in self.values():
            _v.reloadScript()

