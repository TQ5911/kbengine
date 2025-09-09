# -*- encoding:utf-8 -*-
import os
import sys
import re
import functools
import ctypes
import glob

sys.path.append('./external/toolLib')

import paramiko

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
#字体颜色定义 text colors
FOREGROUND_BLUE = 0x0B # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_YELLOW = 0x0e # yellow.

# 背景颜色定义 background colors
BACKGROUND_YELLOW = 0xe0 # yellow.

# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

#reset white
def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

#green
def printGreen(mess, newline=True):
    set_cmd_text_color(FOREGROUND_GREEN)
    ch = '\n' if newline else ''
    sys.stdout.write(mess + ch)
    resetColor()

#blue
def printBlue(mess, newline=True):
    set_cmd_text_color(FOREGROUND_BLUE)
    ch = '\n' if newline else ''
    sys.stdout.write(mess + ch)
    resetColor()

#red
def printRed(mess, newline=True):
    set_cmd_text_color(FOREGROUND_RED)
    ch = '\n' if newline else ''
    sys.stdout.write(mess + ch)
    resetColor()

#yellow
def printYellow(mess, newline=True):
    set_cmd_text_color(FOREGROUND_YELLOW)
    ch = '\n' if newline else ''
    sys.stdout.write(mess + ch)
    resetColor()

#white bkground and black text
def printYellowRed(mess, newline=True):
    set_cmd_text_color(BACKGROUND_YELLOW | FOREGROUND_RED)
    ch = '\n' if newline else ''
    sys.stdout.write(mess + ch)
    resetColor()

def logError(*args):
    printRed(' '.join([str(a) for a in args]))

def getServerAbsPath():
    curDir = os.getcwd()
    dirComps = curDir.split(os.path.sep)
    rootDir = ['trunk', 'publish', 'branch', 'Server']
    for rd in rootDir:
        if rd in dirComps:
            fromIdx = dirComps.index(rd)
            break
    else:
        logError('获取当前工作路径失败：', curDir)
        exit(0)
    absPath = '/home/%s/shared-data/%s'%(VM_USER, '/'.join(dirComps[fromIdx:]))
    return absPath

def getServerRelPath():
    curDir = os.getcwd()
    dirComps = curDir.split(os.path.sep)
    rootDir = ['trunk', 'publish', 'branch', 'Server']
    for rd in rootDir:
        if rd in dirComps:
            fromIdx = dirComps.index(rd)
            break
    else:
        logError('获取当前工作路径失败：', curDir)
        exit(0)
    relPath = '/'+'/'.join(dirComps[fromIdx:])
    return relPath

GAME_SERVER_IP = '192.168.10.161'

VM_USER = 'fengyan'
VM_PASSWD = '123456'
HOME = '/home/%s'%VM_USER
GAME_SERVER_WORK_PATH = '%s/gameserver/kbengine/assets'%HOME
GAME_SERVER_ABS_PATH = getServerAbsPath()
GAME_SERVER_REL_PATH = getServerRelPath()

KBENGINE_CONFIG = '%s/res/server/kbengine.xml'%os.getcwd()
serverIdPt = re.compile('<serverId>\s*(.*)\s*</serverId>')

CMDS = {}
def subcommand(cid, desc):
    def _subcommand(func):
        if cid not in CMDS:
            CMDS[cid] = (func.__name__, desc)
        else:
            raise Exception('duplicated command id:', cid)
        @functools.wraps(func)
        def _func(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        return _func

    return _subcommand

class GameServerStub(object):
    def __init__(self):
        if not self._validateClientConfig():
            exit(-1)

        if not GAME_SERVER_ABS_PATH:
            exit(-1)

        printYellow('connecting game service on %s ...'%GAME_SERVER_IP)
        printYellow('shared path=%s'%GAME_SERVER_ABS_PATH)
        self.sshClient = paramiko.SSHClient()
        self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.sshClient.connect(GAME_SERVER_IP, username = VM_USER, password=VM_PASSWD)
        except:
            logError('连接失败，检查下虚拟机是否开启, ip=%s'%GAME_SERVER_IP)
            exit(-2)
        printGreen('init gameServerStub')
        cmd = 'sudo vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other'
        self._exeSSHCommand(cmd)

    def closeSSH(self):
        self.sshClient.close()

    def _validateClientConfig(self, setServerId=True):
        if not GAME_SERVER_IP:
            logError('未获取到服务器地址，请等待30s稍后重试')
            return False

        if not os.path.exists(KBENGINE_CONFIG):
            logError('文件%s不存在'%KBENGINE_CONFIG)
            return False

        needSetServerId = False
        with open(KBENGINE_CONFIG, 'rb') as cc:
            content = cc.read().decode('utf-8')
            match = serverIdPt.search(content)
            if not match:
                logError('kbengine.xml中serverId格式错误')
                return False

            if not setServerId:
                return False
            serverId = match.groups()[0]
            try:
                serverId = int(serverId)
            except:
                serverId = 0
            finally:
                if not serverId:
                    logError('服务器ID设置错误，在/配置表/serverList-服务器数据表.xlsx中查找，新服务器找策划配，当前IP：%s'%GAME_SERVER_IP)

            while serverId==0:
                try:
                    printYellow('请在本窗口输入服务器ID(20xxx)：',newline=False)
                    serverId = int(input())
                except:
                    serverId = 0

                needSetServerId = True
                if serverId:
                    content = serverIdPt.sub('<serverId> %s </serverId>'%serverId, content, 1)

        if serverId and needSetServerId:
            with open(KBENGINE_CONFIG, 'w', encoding='utf-8') as cc:
                cc.write(content)

        return True

    def _exeSSHCommand(self, cmd, timeout=None):
        stdint, stdout, stderr = self.sshClient.exec_command(cmd, timeout=timeout)

        while True:
            try:
                line = stdout.readline()
            except:
                line = None
            if not line:
                break
            printBlue(line.strip())

    @subcommand(1, '启动服务器，会自动先强制关服')
    def startServer(self, *args):
        printGreen('start server')
        cmd = 'cd %s/serverController && bash remote_init_server.sh %s'%(HOME, GAME_SERVER_ABS_PATH)
        self._exeSSHCommand(cmd)

        cmd = 'cd %s/serverController && bash remote_start_server.sh "%s"'%(HOME, GAME_SERVER_REL_PATH)
        self._exeSSHCommand(cmd, timeout=20)

    @subcommand(2, '强制关服（快速关服，可能丢失数据，测试时不关心数据丢失时使用）')
    def killServer(self, *args):
        printGreen('kill server')

        self._exeSSHCommand('cd %s && ./kill_server.sh'%GAME_SERVER_WORK_PATH)

    @subcommand(3, '安全关服（保存数据，速度较慢）')
    def safeKillServer(self, *args):
        printGreen('safe kill server')

        self._exeSSHCommand('cd %s && ./safe_kill.sh'%GAME_SERVER_WORK_PATH)

    @subcommand(4, '初始化服务器：可重复执行，不会删除数据, 需要先关服')
    def initServer(self, *args):
        printGreen('init server')
        cmd = 'cd %s/serverController && bash remote_init_server.sh %s'%(HOME, GAME_SERVER_ABS_PATH)
        self._exeSSHCommand(cmd)

    @subcommand(5, '清除当前服务器数据：不可恢复, 需要先关服')
    def clearDB(self, *args):
        printGreen('clear db')
        cmd = 'cd %s/serverController && bash remote_init_server.sh %s 1'%(HOME, GAME_SERVER_ABS_PATH)
        self._exeSSHCommand(cmd)

    @subcommand(6, '为当前服务器创建新的数据库：需要先关服')
    def switchToDB(self, *args):
        printYellow('输入新数据名字（任意英文字符串）并回车：', newline=False)
        dbName = input()
        printGreen('switch to db %s, create if not exists'%dbName)
        cmd = 'cd %s/serverController && bash remote_init_server.sh %s 0 %s'%(HOME, GAME_SERVER_ABS_PATH, dbName)
        self._exeSSHCommand(cmd)

    @subcommand(7, '查看服务器各个进程状态')
    def queryServerStatus(self, *args):
        cmd = 'cd %s && ./query_server.sh'%(GAME_SERVER_WORK_PATH, )
        self._exeSSHCommand(cmd)

    @subcommand(8, '拉取到新分支，重启服务')
    def restartGameService(self, *args):
        cmd = 'sudo service gamesvc restart'
        self._exeSSHCommand(cmd)
        printGreen('重启成功')

    @subcommand(9, '启动渠道版本服务器，会自动先强制关服')
    def startChannelServer(self, *args):
        printGreen('start channel server')
        cmd = 'cd %s/serverController && bash remote_init_server.sh %s'%(HOME, GAME_SERVER_ABS_PATH)
        self._exeSSHCommand(cmd)

        for sdir in ('scripts', 'scripts.dist'):
            if os.path.exists('./{}'.format(sdir)):
                channel_list = ['']
                for ddir in os.listdir('./%s' % (sdir)):
                    if os.path.isdir('./%s/%s' % (sdir, ddir)) and ddir[:5] == 'data_': channel_list.append(ddir[5:])
                print('[1] 通用渠道')
                for i in range(1, len(channel_list)):
                    print('[%s] %s' % (i+1, channel_list[i]))
                channel_idx = int(input('请输入目标渠道：')) - 1

                cmd = '''sed -i 's|<internationalVersion>.*</internationalVersion>|<internationalVersion> {} </internationalVersion>|g' {}/res/server/kbengine.xml \
                         && cd {}/serverController \
                         && bash remote_start_server.sh "{}"'''.format(channel_list[channel_idx], GAME_SERVER_WORK_PATH, HOME, GAME_SERVER_REL_PATH)
                self._exeSSHCommand(cmd, timeout=20)
                return
        printRed('脚本目录不存在')

if __name__=='__main__':
    stub = GameServerStub()

    for cid in range(1,len(CMDS)+1):
        print('[%s]: %s'%(cid, CMDS[cid][1]))

    while True:
        printYellow('输入操作编号：', newline=False)
        selectCmd = input()
        try:
            funcName, _ = CMDS[int(selectCmd)]
        except:
            funcName = None

        if not funcName:
            printGreen('结束操作')
            break

        getattr(stub, funcName)()

    stub.closeSSH()

