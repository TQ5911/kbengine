# -*- coding: utf-8 -*-
# 设计思路：
#   gamelog作为暴漏给外部的调用接口,内部封装具体的log writer和log data
#   log writer: TLOG中根据配置，设置具体的写日志具体的实现方式
#   log data: 通过gametlog 和 gamewlog这样的方式去切换不同的数据需求和格式
#             不管gametlog和gamewlog都可以自由的切换数据格式，之所以并存，纯粹兼容

from KBEDebug import *

import functools
import traceback
import platform
import json

import gameconfig
import gameengine
import gameconst
import formula
import utils
import time

import inspect
import gamewlog

if platform.system() == 'Linux':
    import syslog
else:
    import logging
    import logging.handlers



class Rsyslogger(object):
    def __init__(self, name):
        syslog.closelog()
        syslog.openlog(name, 0, syslog.LOG_LOCAL0)

    def info(self, message):
        syslog.syslog(syslog.LOG_INFO, message)


# data--dict
def log(logId, data):
    if not isinstance(data, dict):
        LOG_WARN("data{0} not dict".format(data))
        return

    logData = {
        'server': gameconfig.serverId(),
        'log_id': logId,
        'log_timestamp': utils.getTimestamp64(),
    }
    logData.update(data)
    try:
        s = json.dumps(logData, ensure_ascii=False)
    except Exception as e:
        LOG_ERR('json dump obj err:', e, logId)
        return
    TLOG(logId, s)


# kbengine test server
if platform.system() == 'Linux':
    syslogLogger = Rsyslogger('kbengine@{0}'.format(gameconfig.serverId()))


#####################################
class ADDORREDUCE(object):
    """MACROSGROUP::ADDORREDUCE: """

    ADD = 0  # 加
    REDUCE = 1  # 减


class iMoneyType(object):
    """MACROSGROUP::iMoneyType: 货币类型，根据游戏情况自定义"""

    Coin = 0  # 元贝
    AusCoin = 1  # 瑞羽
    XunScore = 2  # 巽值
    GongJian = 3  # 共建值
    HomeCoin = 4  # 家园币


class IINVATION_LOG_STATUS(object):
    INVALID_INVITER = 1  # 被邀请者注册时间早于邀请者
    INVITED = 2  # 已经被邀请过了
    SELF_INVITECODE = 3  # 自己的邀请码
    INVALID_INVITECODE = 4  # 无效的邀请码
    TIMEOUT = 5  # 邀请码已过时


class iTASKTYPE(object):
    """MACROSGROUP::iTASKTYPE: 根据游戏情况自定义"""

    TYPE_1 = 1  # 主线任务
    TYPE_2 = 2  # 支线任务
    TYPE_3 = 3  # 其他


class iSTATE(object):
    """MACROSGROUP::iSTATE: 根据游戏情况自定义"""

    CLAIM = 1  # 接取
    SUBMIT = 2  # 完成
    TARGET_REACH = 3  # 目标达成
    TARGET_FAILED = 4  # 目标失败
    QUIT = 5  # 放弃



class ChangeNameType(object):
    """MACROSGROUP::MallBuyOrSell: 从商城购买物品或出售物品"""

    ITEM = 1  # 购买
    GM = 0  # 出售


################################## wlog start ########################################
WLogClassMap = None


def registerWLogClasses():
    global WLogClassMap
    if WLogClassMap:
        return

    clss = inspect.getmembers(sys.modules['gamewlog'], inspect.isclass)
    WLogClassMap = {}
    for name, cls in clss:
        if name != 'StructLogBasic':
            WLogClassMap[name] = cls


registerWLogClasses()


def getWLogClass(name):
    if WLogClassMap:
        return WLogClassMap[name]


################################## wlog end########################################

def TLOG(name="", logData="", fromTracking=False):
    if not fromTracking:
        gameengine.panicStack('use old tlog', name)

    logFlag = gameconfig.logFlag()
    if logFlag == gameconst.LogType.NORMAL:
        LOG_IFO(logData)
    elif logFlag == gameconst.LogType.WLOG:
        LOG_DBG(logData)
        if platform.system() == 'Linux':
            syslogLogger.info(str(logData))


def makeResourceFlowLog(logDataDic):
    pass


def logMailOpData(gbId, name, mVal, op, srcType):
    mailLogData = {
        'role_id': gbId,
        'role_name': name,
        'mailId': mVal.mailId,
        'mailUUID': mVal.mailUUID,
        'mailType': mVal.mailType,
        'readState': mVal.readState,
        'sender': mVal.sender,
        'title': mVal.title,
        'titleArgs': mVal.titleArgs,
        'content': mVal.content,
        'contentArgs': mVal.contentArgs,
        'attach': str(mVal.attach),
        'attachState': mVal.attachState,
        'recvSrcType': mVal.srcType,
        'op': op,
        'opSrc': srcType,
        'opUUID': mVal.opUUID,
        'detail': str(mVal.detail),
        'tCreate': mVal.tCreate,
        'tExpire': mVal.tExpire,
    }
    log('Mail', mailLogData)
