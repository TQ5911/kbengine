# -*- encoding:utf-8 -*-

import os
import sys
import xml.etree.ElementTree as ET

pyPath = os.path.dirname(os.path.abspath(__file__))
configPath = "/".join([pyPath, 'res', 'server', 'kbengine.xml'])

def createCombineSql():
    fConfig = open(configPath, 'rb')
    content = ''.join([str(line, 'utf-8') for line in fConfig.readlines()])
    fConfig.close()
    __KBE_CONFIG_ROOT = ET.fromstring(content)
    element = __KBE_CONFIG_ROOT.find('sql_script_filename')
    xzjSqlPath = element.text.strip()
    with open(xzjSqlPath, 'r') as f:
        xzjSql = f.read()

    otherSqlPath = "/".join([pyPath,'startServerDb.sql'])
    with open(otherSqlPath, 'r') as f:
        otherSql = f.read()

    combineSql = xzjSql+otherSql
    combineSqlPath =  "/".join([pyPath,'combineSql.sql'])
    with open(combineSqlPath, 'w') as f:
        f.write(combineSql)

def sourceSql():
    fConfig = open(configPath, 'rb')
    content = ''.join([str(line, 'utf-8') for line in fConfig.readlines()])
    fConfig.close()
    __KBE_CONFIG_ROOT = ET.fromstring(content)
    element = __KBE_CONFIG_ROOT.find('dbmgr')
    element = element.find('databaseInterfaces')
    element = element.find('default')
    hostElement = element.find('host')
    portElement = element.find('port')
    authElement = element.find('auth')
    usernameElement = authElement.find('username')
    passwordElement = authElement.find('password')
    host = hostElement.text.strip()
    port = portElement.text.strip()
    username = usernameElement.text.strip()
    password = passwordElement.text.strip()
    combineSqlPath = "/".join([pyPath, 'combineSql.sql'])
    # print("mysql -h%s -P%s -%s -p%s < %s" % (host, port, username, password,combineSqlPath))
    os.system("mysql -h%s -P%s -u%s -p%s < %s" % (host, port, username, password,combineSqlPath))



if __name__=='__main__':
    if len(sys.argv) == 1:
        args = 0
    else :
        args = sys.argv[1]

    if args == 0:
        createCombineSql()
    else :
        createCombineSql()
        sourceSql()