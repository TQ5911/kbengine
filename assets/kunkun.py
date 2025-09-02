#!/usr/bin/python3
# coding: utf-8
import os
import sys
import re
import xml.sax
import argparse


class CfgHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.tagStack = []
        self.host = ''
        self.dbname = ''
 
   # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.tagStack.append(tag)
 
   # 元素结束事件处理
    def endElement(self, tag):
        self.tagStack.pop()
 
   # 内容事件处理
    def characters(self, content):
        if 'databaseInterfaces' in self.tagStack:
            if 'host' in self.tagStack:
                self.host = content
            elif 'databaseName' in self.tagStack:
                self.dbname = content

def parseCfg(filename):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = CfgHandler()
    parser.setContentHandler( Handler )
    parser.parse(filename)
    return Handler.host.strip(), Handler.dbname.strip()

def getAssetsDir():
    absPath = os.path.abspath(__file__)
    return os.path.dirname(absPath)
    
def chAssets():
    os.chdir(getAssetsDir())
    
def getKberoot(assetspath):
    pat = re.compile(r'^(.*kbengine)')
    find = pat.search(assetspath)
    if find:
        return find.groups()[0]

def isLinux():
    return sys.platform.startswith('linux')
    
def restart():
    assetsPath = getAssetsDir()
    kberoot = getKberoot(assetsPath)
    defaultCfgPath = os.path.join(kberoot, 'kbe', 'res', 'server', 'kbengine_defaults.xml')
    chAssets()
    if isLinux():
        os.system("sh start_server.sh")
    else:
        os.system("start_server.bat")
    opscriptPath = os.path.join(assetsPath, 'serverOperate')
    sys.path.append(opscriptPath)
    import serverState
    host, dbname = parseCfg(defaultCfgPath)
    serverState.ServerState().init(host, 'kbengine', 'kbe123', dbname)
    serverState.ServerState().loop()
    sys.exit(serverState.ServerState().exitCode)
    
def refresh():
    pass
    
def reload():
    if isLinux():
        chAssets()
        os.system("sh serverOperate/refresh.sh serverOperate/kunkun_reload.py")
    else:
        chAssets()
        os.system("serverOperate\\kunkun_reload.bat serverOperate\\kunkun_reload.py")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", help="restart", action="store_true")
    group.add_argument("-f", help="refresh", action="store_true")
    group.add_argument("-l", help="reload", action="store_true")
    args = parser.parse_args()
    
    if args.s:
        restart()
    elif args.f:
        refresh()
    elif args.l:
        reload()
        
    
    
