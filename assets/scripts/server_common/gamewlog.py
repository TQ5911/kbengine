# coding: utf-8
# !/usr/bin/env python3
# 设计思路：
#   StructLogBasic 定义公用的数据
#   其子类定义具体log需要的数据
#  TODO: 子类名从表格导出，自动生成，或者此模块从表格导出的数据中生成。

from KBEDebug import *
import KBEngine

import time
import utils
import gameconfig
import gameconst
import datetime
import json
import time


def getLogOutput(logDic):
    _s = ""
    for k in logDic.keys():
        _s += k
        _s += ":"
        _s += str(logDic.get(k, '')).replace(' ', '')
        _s += " "

    return _s


class StructLogBasic(object):

    @property
    def wlogname(self):
        return self.__class__.__name__

    def __init__(self, params):
        self.__base_slots__ = ("server", "log_timestamp", "log_id")
        for slot in (self.__base_slots__ + self.__slots__):
            setattr(self, slot, params.get(slot, ''))

        setattr(self, "log_id", self.wlogname)
        setattr(self, "log_timestamp", int(round(time.time() * 1000)))

    def __repr__(self):
        data = {}
        for k in (self.__base_slots__ + self.__slots__):
            data[k] = getattr(self, k, '')

        try:
            s = json.dumps(data, ensure_ascii=False)
        except Exception as e:
            LOG_ERR('StructLogBasic json dump err:', e, getattr(self, 'log_id', 0))
            s = ''
        return s


class ServerOnClientConeect(StructLogBasic):
    __slots__ = ("gate", "client_id", "ip", "account_id", "udid", "role_name", "role_id")

    @property
    def wlogname(self):
        return 'server_on_client_connect'

    def __init__(self, params):
        super().__init__(params)


class ServerParseAccountInfo(StructLogBasic):
    __slots__ = ("gate", "account_id", "login_channel", "udid", "role_name", "role_id", "app_channel")

    @property
    def wlogname(self):
        return 'server_parse_account_info'

    def __init__(self, params):
        super().__init__(params)


class ServerLogin(StructLogBasic):
    __slots__ = ("gate", "client_id", "account_id", "role_name", "role_id", "udid")

    @property
    def wlogname(self):
        return 'server_login'

    def __init__(self, params):
        super().__init__(params)


class ServerBanByWhiteList(StructLogBasic):
    __slots__ = ("gate", "client_id", "app_channel", "accont_id", "role_name", "role_id")

    @property
    def wlogname(self):
        return 'server_ban_by_whitelist'

    def __init__(self, params):
        super().__init__(params)


class ServerOnClientLost(StructLogBasic):
    __slots__ = ("gate", "client_id", "accont_id", "udid", "role_name", "role_id")

    @property
    def wlogname(self):
        return 'server_on_client_lost'

    def __init__(self, params):
        super().__init__(params)


class OnlineRoleNum(StructLogBasic):
    __slots__ = ("online", "logic_host_id")

    def __init__(self, params):
        super().__init__(params)


class RegisterNum(StructLogBasic):
    __slots__ = ("all", "today_add")

    def __init__(self, params):
        super().__init__(params)


class CreateRole(StructLogBasic):
    __slots__ = ("ip", "ipv6", "device_model", "os_name", "os_ver", "mac_addr", "udid",
                 "app_channel", "app_ver", "imei", "client_type", "location", "country_code",
                 "account_id", "role_id", "role_name", "face_id", "clothes_id", "create_time"
                 )

    def __init__(self, params):
        super().__init__(params)


class LoginRole(StructLogBasic):
    __slots__ = ("ip", "ipv6", "device_model", "device_name", "device_height", "device_width",
                 "os_name", "os_ver", "mac_addr", "udid", "isp", "app_channel", "login_channel",
                 "app_ver", "network", "imei", "client_type", "location", "country_code",
                 "sauth_login_type", "caid", "display_quality_fps", "display_quality", "is_root",
                 "realnameStatus", "real_age", "account_id", "role_id", "role_name", "create_time", "login_time",
                 "last_logout_time", "role_gender", "space_id", "space_uuid", "dup", "init_type",
                 "id_hash", "x", "y", "z", "total_time", "YuanBei", "RuiYu")

    def __init__(self, params):
        super().__init__(params)


class LogoutRole(StructLogBasic):
    __slots__ = ("ip", "ipv6", "device_model", "device_name", "device_height", "device_width",
                 "os_name", "os_ver", "mac_addr", "udid", "isp", "app_channel", "login_channel",
                 "app_ver", "network", "imei", "client_type", "location", "country_code",
                 "sauth_login_type", "caid", "display_quality_fps", "display_quality", "is_root",
                 "realnameStatus", "real_age", "account_id", "role_id", "role_name", "create_time", "logout_time",
                 "role_gender", "space_id", "space_uuid", "dup", "init_type",
                 "id_hash", "x", "y", "z", "total_time", "YuanBei", "RuiYu", "reason", "isEmulator", "emulatorName")

    def __init__(self, params):
        super().__init__(params)


class TaskClaim(StructLogBasic):
    '''
    接任务时
    '''
    __slots__ = ("role_id", "role_name", "op_nuid", "taskIds", "claim_source")

    def __init__(self, params):
        super().__init__(params)


class TaskQuit(StructLogBasic):
    '''
    退出任务时
    '''
    __slots__ = ("role_id", "role_name", "op_nuid", "taskIds", "reason")

    def __init__(self, params):
        super().__init__(params)


class TaskSubmit(StructLogBasic):
    '''
    提交任务时
    '''
    __slots__ = ("role_id", "role_name", "op_nuid", "taskIds", "rewards")

    def __init__(self, params):
        super().__init__(params)


class CurrencyAdd(StructLogBasic):
    '''
    添加货币
    '''
    __slots__ = ("account_id", "role_name", "role_id", "ip", "ipv6", "device_model", "os_name", "os_ver",
                 "mac_addr", "udid", "app_channel", "caid", "aid", "is_emulator", "is_root", "op_nuid", "change_type",
                 "commodity_id", "coin_type", "Coin", "left_Coin", "change_time", "id_hash", "darkFlag")

    @property
    def wlogname(self):
        return str(getattr(self, 'coin_type', 'YuanShi')) + 'Gain'

    def __init__(self, params):
        super().__init__(params)


class PickSuccess(StructLogBasic):
    '''
    采集成功时
    '''
    __slots__ = ("role_id", "role_name", "op_nuid", "pick_id", "pick_num", "space_id",
                 "item_cost", "rewards", "task", "panel", "send")

    def __init__(self, params):
        super().__init__(params)



class BagItemChanged(StructLogBasic):
    '''
    背包道具变化时
    '''

    __slots__ = (
    "role_id", "role_name", "inv_id", "item_id", "item_name", "item_uuid", "op_nuid", "delta", "left_count",
    "change_type", "detail", "id_hash", 'change_detail', 'darkFlag')

    def __init__(self, params):
        super().__init__(params)


class DoGmCmd(StructLogBasic):
    '''
    用户gm日志
    '''
    __slots__ = ("role_id", "cmd_name", "cmd_args", "reason")

    def __init__(self, params):
        super().__init__(params)



class ChangeName(StructLogBasic):
    '''
    改名日志
    '''
    __slots__ = ("role_id", "op_nuid", "old_name", "new_name", "change_type")

    def __init__(self, params):
        super().__init__(params)
