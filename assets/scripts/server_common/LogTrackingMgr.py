# -*- coding: utf-8 -*-
import json
from enum import Enum
from KBEDebug import *
import KBEngine
import gamelog
import gameconfig
import utils

class LogTrackingMgr:
    Path_Server_Recharge_Complete            = "/server/recharge/complete"
    Path_Server_Pcu                          = "/server/pcu"
    Path_Server_Logout                       = "/server/logout"
    Path_Server_Login                        = "/server/login"
    Path_Server_Role_Login                   = "/server/role/login"
    Path_Server_Role_Logout                  = "/server/role/logout"
    Path_Server_Create_Role                  = "/server/create/role"
    # 充值完成事件
    @staticmethod
    def Server_Recharge_Complete(accountId, roleId, itemType, itemId, price, orderId):
        args = {}
        args["path"] = LogTrackingMgr.Path_Server_Recharge_Complete
        args["accountId"] = accountId
        args["roleId"] = roleId
        args["itemType"] = itemType
        args["itemId"] = itemId
        args["price"] = price
        args["orderId"] = orderId
        LogTrackingMgr.LOG(args)

    # PCU事件
    @staticmethod
    def Server_Pcu(pcu):
        args = {}
        args["path"] = LogTrackingMgr.Path_Server_Pcu
        args["pcu"] = pcu
        LogTrackingMgr.LOG(args)

    # 用户登出事件
    @staticmethod
    def Server_Logout(accountId, deviceModel, ipAddress, operatingSystem, channelSource):
        args = {}
        args["path"] = LogTrackingMgr.Path_Server_Logout
        args["accountId"] = accountId
        args["deviceModel"] = deviceModel
        args["ipAddress"] = ipAddress
        args["operatingSystem"] = operatingSystem
        args["channelSource"] = channelSource
        LogTrackingMgr.LOG(args)

    # 用户登录事件
    @staticmethod
    def Server_Login(accountId, deviceModel, ipAddress, operatingSystem, channelSource):
        args = {}
        args["path"] = LogTrackingMgr.Path_Server_Login
        args["accountId"] = accountId
        args["deviceModel"] = deviceModel
        args["ipAddress"] = ipAddress
        args["operatingSystem"] = operatingSystem
        args["channelSource"] = channelSource
        LogTrackingMgr.LOG(args)

    # 角色登录事件
    @staticmethod
    def Server_Role_Login(accountId, gbId, school, name, level):
        args = {}
        args["path"] = LogTrackingMgr.Path_Server_Role_Login
        args["accountId"] = accountId
        args["gbId"] = gbId
        args["school"] = school
        args["name"] = name
        args["level"] = level
        LogTrackingMgr.LOG(args)

    # 角色登出事件
    @staticmethod
    def Server_Role_Logout(accountId, gbId, school, name, level):
        args = {}
        args["path"] = LogTrackingMgr.Path_Server_Role_Logout
        args["accountId"] = accountId
        args["gbId"] = gbId
        args["school"] = school
        args["name"] = name
        args["level"] = level
        LogTrackingMgr.LOG(args)

    # 创建角色事件
    @staticmethod
    def Server_Create_Role(accountId, gbId, school, name):
        args = {}
        args["path"] = LogTrackingMgr.Path_Server_Create_Role
        args["accountId"] = accountId
        args["gbId"] = gbId
        args["school"] = school
        args["name"] = name
        LogTrackingMgr.LOG(args)

    @staticmethod
    def LOG(args):
        logData = {
        'server': gameconfig.serverId(),
        'log_id': "LogTracking",
        'sentTimestamp': utils.getTimestamp64(),
        }
        logData.update(args)
        gamelog.TLOG("", json.dumps(logData), True)
