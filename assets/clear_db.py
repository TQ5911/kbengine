# -*- coding: utf-8 -*-
import pymysql
import sys

server = {'host':'192.168.10.31', 'user':'xzj', 'password':'xzj123'}

if __name__=='__main__':
    _args = sys.argv

    _dbName = _args[1]

    db = pymysql.connect(db=_dbName, **server)
    cursor = db.cursor()

    dropSql = 'drop database {}'.format(_dbName)
    createSql = 'create database {}'.format(_dbName)

    cursor.execute(dropSql)
    cursor.execute(createSql)
    db.commit()
