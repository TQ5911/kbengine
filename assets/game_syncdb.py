# -*- encoding:utf-8 -*-

import sys
import os
import xml.etree.ElementTree as ET

PY_PATH = os.path.dirname(os.path.abspath(__file__))
configPath = "/".join([PY_PATH, 'res', 'server', 'kbengine.xml'])

def createCombineSql():
    _fConfig = open(configPath, 'rb')
    content = ''.join([str(line, 'utf-8') for line in _fConfig.readlines()])
    _fConfig.close()
    __KBE_CONFIG_ROOT = ET.fromstring(content)
    _element = __KBE_CONFIG_ROOT.find('sql_script_filename')
    _xzjSqlPath = _element.text.strip()
    with open(_xzjSqlPath, 'r') as f:
        xzjSql = f.read()

    _otherSqlPath = "/".join([PY_PATH,'startServerDb.sql'])
    with open(_otherSqlPath, 'r') as f:
        otherSql = f.read()

    combineSql = xzjSql+otherSql
    combineSqlPath =  "/".join([PY_PATH,'combineSql.sql'])
    with open(combineSqlPath, 'w') as f:
        f.write(combineSql)

def sourceSql():
    _fConfig = open(configPath, 'rb')
    content = ''.join([str(line, 'utf-8') for line in _fConfig.readlines()])
    _fConfig.close()
    __KBE_CONFIG_ROOT = ET.fromstring(content)
    _element = __KBE_CONFIG_ROOT.find('dbmgr')
    _element = _element.find('databaseInterfaces')
    _element = _element.find('default')
    _hostElement = _element.find('host')
    portElement = _element.find('port')
    authElement = _element.find('auth')
    _usernameElement = authElement.find('username')
    passwordElement = authElement.find('password')
    host = _hostElement.text.strip()
    port = portElement.text.strip()
    username = _usernameElement.text.strip()
    _password = passwordElement.text.strip()
    combineSqlPath = "/".join([PY_PATH, 'combineSql.sql'])
    os.system("mysql -h%s -P%s -u%s -p%s < %s" % (host, port, username, _password,combineSqlPath))



if __name__=='__main__':
    if len(sys.argv) == 1:
        _args = 0
    else :
        _args = sys.argv[1]

    createCombineSql()
    if _args == 0:
        pass
    else :
        sourceSql()
