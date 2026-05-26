#!/usr/bin/env python
# coding: utf-8
import sys
import os
import smtplib
import traceback
import time
import datetime
import re
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import platform

pidfile = 0
sendMailTime = 0
'''将当前进程fork为一个守护进程 
'''
cf = configparser.ConfigParser()
cf.read('logDaemonize.cfg', encoding='utf-8')
def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # 重定向标准文件描述符（默认情况下定向到/dev/null）
    try:
        pid = os.fork()
        # 父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            sys.exit(0)  # 父进程退出
    except OSError as err:
        sys.stderr.write("fork #1 failed:  %s\n" % (err))
        sys.exit(1)

        # 从母体环境脱离
    os.chdir("/")  # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.umask(0)  # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()  # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

    # 执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # 第二个父进程退出
    except OSError as err:
        sys.stderr.write("fork #2 failed:  %s\n" % (err))
        sys.exit(1)

        # 进程已经是守护进程了，重定向标准文件描述符

    for f in sys.stdout, sys.stderr: f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 1)
    os.dup2(si.fileno(), sys.stdin.fileno())  # dup2函数原子化关闭和复制文件描述符
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def sendmail(subject, msg, toaddrs, fromaddr, smtpaddr, password):
    mail_msg = MIMEMultipart()
    mail_msg['Subject'] = subject
    mail_msg['From'] = fromaddr
    mail_msg['To'] = ','.join(toaddrs)
    mail_msg.attach(MIMEText(msg, 'plain', 'utf-8'))
    try:
        s = smtplib.SMTP()
        s.connect(smtpaddr)  # 连接smtp服务器
        s.login(fromaddr, password)  # 登录邮箱
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string())  # 发送邮件
        s.quit()
        print("发送邮件中...", subject)
    except Exception as err:
        print("Error: unable to send email")
        print(err)
		
def ApplicationInstance(): 
    global pidfile
    import fcntl
    pidfile = open(os.path.realpath(__file__), "r")
    try:
        fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)  # 创建一个排他锁,并且所被锁住其他进程不会阻塞
    except Exception as err:
        sys.stderr.write('another instance is running...\n')
        sys.exit(1)
    pass

def getNextMailTime(nowTime, hour=22, minute=0):
    timeType = cf.getint('log_config', 'timeType')
    if timeType == 1:
        return nowTime + cf.getint('log_config', 'timeSend')
    if timeType == 2:
        hour = cf.getint('log_config', 'dateSendHour')
        minute = cf.getint('log_config', 'dateSendMinute')
        a = datetime.datetime.now().strftime("%Y-%m-%d") + " %02d:%02d:00" % (hour, minute)
        timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        if nowTime >= timeStamp:
            timeStamp = timeStamp + 3600 * 24
        return timeStamp
    return 0

# 示例函数：每秒打印一个数字和时间戳
def main():
    rootLogDir = cf.get('log_config', 'rootLogDir')
    fromaddr = cf.get('mail_config', 'fromaddr')
    smtpaddr = cf.get('mail_config', 'smtpaddr')
    password = cf.get('mail_config', 'password')
    strKeyWords = cf.get('log_config', 'keyWordsList')
    strToaddrs = cf.get('mail_config', 'toaddrs')
    toaddrs = []
    sendMailTime = cf.getint('log_config', 'sendMailTime')
    sendMailLastTime = cf.getint('log_config', 'sendMailLastTime')

    time_local = time.localtime(sendMailTime)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    sys.stdout.write('下一次发送日志的时间 : %s \n' % (dt))

    for addrs in strToaddrs.split(','):
        toaddrs.append(addrs)
    while True:
        nowTime = int(time.time())
        # sys.stdout.write('nowTime : %s\n' % (nowTime))
        if (nowTime - sendMailLastTime >= 3 and sendMailTime <= nowTime):
            for keyword in strKeyWords.split(','):
                mailMsg = getErrorLog(rootLogDir, keyword, sendMailLastTime)
                if mailMsg == "":
                    continue
                subject = time.strftime('%y-%m-%d  %H:%M:%S', time.localtime(time.time()))
                subject = subject + keyword
                sendmail(subject, mailMsg, toaddrs, fromaddr, smtpaddr, password)
                mailMsg = ""
            sendMailTime = getNextMailTime(nowTime)
            time_local = time.localtime(sendMailTime)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            sys.stdout.write('下一次发送日志的时间 : %s \n' % (dt))
            sendMailLastTime = nowTime
            cf.set('log_config', 'sendMailTime', str(sendMailTime))
            cf.set('log_config', 'sendMailLastTime', str(sendMailLastTime))
            cfgPath = os.path.join(rootLogDir, 'logDaemonize.cfg')
            cf.write(open(cfgPath, 'w'))
        sys.stdout.flush()
        sys.stderr.flush()
        time.sleep(1)

def get_FileCreateTime(filePath):
    # filePath = unicode(filePath,'utf8')
    t = os.path.getctime(filePath)
    return t

def checkPath(path):
    if not os.path.isfile(path):
        return False
    if not (path.endswith('.log') or path.endswith('.log.1')):
        return False
    return True


def checkAddLine(strLine, keyword, isAddLine, beginTime):
    strDateTemp = re.search(" \[.*\] ", strLine)
    if not strDateTemp:
        if isAddLine == True:
            return True
    else:
        if keyword not in strLine:
            return False
        strDate = strDateTemp.group()
        if len(strDate) < 27:
            if isAddLine == True:
                return True
            return False
        timestring = strDate[-25:-6]
        intDate = 0
        try:
            intDate = int(time.mktime(time.strptime(timestring, '%Y-%m-%d %H:%M:%S')))
        except Exception as err:
            print(strDateTemp)
            sys.stdout.write('%d  timestring %s is err  strDate %s \n' % (len(strDate), timestring, strDate))
            return False
        if intDate >= beginTime:
            return True
    return False


def addMsg(tempMsg, count_dict, msg_dict):
    keyMsg = re.sub(r'\{.*\}\n', '', tempMsg)
    keyMsg = re.sub(r'\[.*\]', '', keyMsg)

    key_dict = {}
    for keyword in keyMsg.split('\n'):
        if keyword == '':
            continue
        key_dict[keyword] = 1

    keyMsg = ""
    for tempKey in key_dict:
        keyMsg += tempKey

    count = count_dict.setdefault(keyMsg, 0)
    count += 1
    count_dict[keyMsg] = count
    msg_dict[keyMsg] = tempMsg


def getErrorLog(rootLogDir, keyword, beginTime):
    msg = ""
    count_dict = {}
    msg_dict = {}
    list = os.listdir(rootLogDir)
    for i in range(0, len(list)):
        path = os.path.join(rootLogDir, list[i])
        if checkPath(path) == False:
            continue
        # sys.stdout.write('path %s\n' % path)
        fileObject = open(path, 'rb')
        if not fileObject:
            continue
        numMax = 0
        isAddLine = False
        tempMsg = ""
        for line in fileObject:
            strLine = line.decode('utf-8', 'ignore')
            isAddLine = checkAddLine(strLine, keyword, isAddLine, beginTime)
            if isAddLine == False:
                if tempMsg != "":
                    addMsg(tempMsg, count_dict, msg_dict)
                tempMsg = ""
                continue
            tempMsg += strLine
            numMax = numMax + 1
            if numMax >= 10000:
                break
        fileObject.close()
    for keyMsg in msg_dict:
        msg += msg_dict[keyMsg] + "count: " + str(count_dict[keyMsg]) + "\n"

    return msg

if __name__ == "__main__":
    rootLogDir = cf.get('log_config', 'rootLogDir')
    if platform.system() == 'Linux':
        ApplicationInstance()
    list = os.listdir(rootLogDir)
    for i in range(0, len(list)):
        path = os.path.join(rootLogDir, list[i])
        if checkPath(path) == False:
            continue

    if platform.system() == 'Linux':
        cf.set('log_config', 'rootlogdir', str(os.getcwd()))
        cfgPath = os.path.join(rootLogDir, 'logDaemonize.cfg')
        cf.write(open(cfgPath, 'w'))
        daemonize()
        # daemonize('/dev/null', '/tmp/daemon_stdout.log', '/tmp/daemon_error.log')

    main()
