# coding: utf-8
from KBEDebug import *

import gamesql


class ColumnVal(object):
    def __init__(self, name, columnType):
        self.name = name
        self.columnType = columnType


class TableColumn(object):
    def __init__(self, tableName, columns, columnStr, columnToIdxDic):
        self.tableName = tableName
        self.columns = columns
        self.columnStr = columnStr
        self.columnToIdxDic = columnToIdxDic

    def toColumnStrWithoutId(self):
        return ','.join(_column.name for _column in self.columns if _column.name != 'id')

    def getTypeByIdx(self, idx):
        return self.columns[idx].columnType

    @classmethod
    def loadColumns(cls, tbName, cb):
        gamesql.loadColumns(
            tbName,
            lambda ret, num, insertId, err: cls.onLoadColumns(ret, num, insertId, err, cb, tbName)
        )

    @classmethod
    def onLoadColumns(cls, ret, num, insertId, err, cb, tbName):
        if err:
            ERROR_MSG('TableColumn::onLoadColumns query db err.', err)
            return

        _columns = []
        for _column in ret:
            _columnName = _column[0].decode('utf-8')
            _type = _column[1].decode('utf-8')
            _columns.append(ColumnVal(_columnName, _type))

        _columns = sorted(_columns, key=lambda x: x.name)

        _columnToIdxDic = {}
        for _idx, _column in enumerate(_columns):
            _columnToIdxDic[_column.name] = _idx

        _tableColumn = TableColumn(
            tbName,
            _columns,
            ','.join([_column.name for _column in _columns]),
            _columnToIdxDic
        )

        cb(_tableColumn)

    def loadData(self, condition, cb):
        gamesql.loadTableData(
            self.columnStr,
            self.tableName,
            condition,
            lambda ret, num, insertId, err: self.onLoadData(ret, num, insertId, err, cb)
        )

    def onLoadData(self, ret, num, insertId, err, cb):
        if err:
            ERROR_MSG('TableColumn::onLoadData query db err.', err)
            return

        _rows = []
        for _row in ret:
            _rowAfterProcess = []
            for _idx, _val in enumerate(_row):
                _type = self.getTypeByIdx(_idx)
                if 'int' in _type:
                    _rowAfterProcess.append(int(_val))

                elif _type == 'float':
                    _rowAfterProcess.append(float(_val))

                elif _type == 'double':
                    _rowAfterProcess.append(float(_val))

                else:
                    _rowAfterProcess.append(_val)

            _rows.append(_rowAfterProcess)

        cb(_rows)




