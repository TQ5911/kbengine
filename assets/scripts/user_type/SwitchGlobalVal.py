# coding=utf-8

from KBEDebug import *

import gamesql
import TableColumn
import functools
import gameglobal
import gameconst


class TbNode(object):
    def __init__(self, tbName, fatherName=''):
        self.tbName = tbName
        self.fatherName = fatherName
        self.children = []

    def setFatherName(self, fatherName):
        self.fatherName = fatherName

    def addSonNode(self, sonNode):
        self.children.append(sonNode)


class SwitchGlobalVal(object):
    def __init__(self, tblLevelData=None, tblColumnDatas=None):
        self.tblLevelData = tblLevelData
        self.tblColumnDatas = tblColumnDatas

    @staticmethod
    def checkRootOk(rootName):
        if gameglobal.switchGlobalVal is None:
            return False

        if rootName not in gameglobal.switchGlobalVal.tblLevelData:
            return False

        return True

    def getNode(self, tbName):
        return self.tblLevelData[tbName]

    def getColumnVal(self, tbName):
        return self.tblColumnDatas[tbName]

    @staticmethod
    def fromTblNameToLevelData(tbNames):
        _allDic = {}
        for _tbName in tbNames:
            _allDic[_tbName] = TbNode(_tbName)

        for _sonName, _sonNode in _allDic.items():
            _tempFatherName = None
            for _fatherName, _fatherNode in _allDic.items():
                _prefix = _fatherName + '_'
                if _prefix not in _sonName:
                    continue

                if _tempFatherName is None:
                    _tempFatherName = _fatherName

                elif len(_tempFatherName) < len(_fatherName):
                    _tempFatherName = _fatherName

            if _tempFatherName is not None:
                _sonNode.setFatherName(_tempFatherName)
                _fatherNode = _allDic[_tempFatherName]
                _fatherNode.addSonNode(_sonNode)

        return {
            'all': _allDic,
        }

    @classmethod
    def loadLevelData(cls, rootTbName, cb):
        """
        加载全局数据
        :return:
        """
        _cache = {}
        gamesql.getLevelData(
            rootTbName,
            lambda ret, num, insertId, err: cls.onGetLevelData(ret, num, insertId, err, _cache, cb)
        )

    @classmethod
    def onGetLevelData(cls, ret, num, insertId, err, cache, cb):
        if err:
            LOG_ERR('SwitchGlobalVal::onGetLevelData query db err.', err)
            return

        _tbNames = []
        for _tbName, in ret:
            _tbNames.append(_tbName.decode('utf-8'))

        _dic = cls.fromTblNameToLevelData(_tbNames)
        cache['tblLevelData'] = _dic['all']
        cache['tblColumnDatas'] = {}
        cls.loadColumns(iter(_tbNames), cache, cb)

    @classmethod
    def loadColumns(cls, iter, cache, cb):
        _tbName = next(iter, None)
        if _tbName is None:
            # cls.done(cache, cb)
            cls.loadMailData(cb, cache)
            return

        TableColumn.TableColumn.loadColumns(
            _tbName,
            functools.partial(cls.onGetTableColumnVal, iter, cache, _tbName, cb)
        )

    @classmethod
    def onGetTableColumnVal(cls, iter, cache, tbName, cb, tbColumnVal):
        cache['tblColumnDatas'][tbName] = tbColumnVal
        cls.loadColumns(iter, cache, cb)

    @classmethod
    def loadMailData(cls, cb, cache):
        cache['tblLevelData'][gameconst.TABLE_NAME_GAME_MAIL] = TbNode(gameconst.TABLE_NAME_GAME_MAIL)
        TableColumn.TableColumn.loadColumns(
            gameconst.TABLE_NAME_GAME_MAIL,
            functools.partial(cls.onGetMailTableColumnVal, cb, cache)
        )

    @classmethod
    def onGetMailTableColumnVal(cls, cb, cache, tbColumnVal):
        cache['tblColumnDatas'][gameconst.TABLE_NAME_GAME_MAIL] = tbColumnVal
        cls.done(cache, cb)

    @classmethod
    def done(cls, cache, cb):
        if gameglobal.switchGlobalVal is None:
            gameglobal.switchGlobalVal = SwitchGlobalVal(**cache)

        else:
            gameglobal.switchGlobalVal.tblLevelData.update(cache['tblLevelData'])
            gameglobal.switchGlobalVal.tblColumnDatas.update(cache['tblColumnDatas'])

        cb()




