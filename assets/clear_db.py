# -*- coding: utf-8 -*-
import pymysql
import sys

server = {'host':'192.168.10.31', 'user':'xzj', 'password':'xzj123'}

if __name__=='__main__':
    args = sys.argv

    dbName = args[1]

    db = pymysql.connect(db=dbName, **server)
    cursor = db.cursor()

    dropSql = 'drop database {}'.format(dbName)
    createSql = 'create database {}'.format(dbName)

    cursor.execute(dropSql)
    cursor.execute(createSql)
    db.commit()