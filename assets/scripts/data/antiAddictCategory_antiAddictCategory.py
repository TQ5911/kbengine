# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: antiAddictCategory/antiAddictCategory
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    1: _tools.RODict({
        "ID": 1,
        "name": "BONUS_SRC_KILL_MONSTER",
        "isAntiAddicted": 1,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    2: _tools.RODict({
        "ID": 2,
        "name": "BONUS_SRC_COMPLETE_TASK",
        "isAntiAddicted": 1,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001985,
        "rewardMessage": ('<color=&color211>任务完成</color>', '完成<color=&color57>{0}</color>任务<color=&color57>{1}</color>，获得奖励：', '完成任务，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    }),
    3: _tools.RODict({
        "ID": 3,
        "name": "BONUS_SRC_GM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54000009,
        "rewardMessage": None,
        "group": 1
    }),
    4: _tools.RODict({
        "ID": 4,
        "name": "BONUS_SRC_UNLOCK_GRIDS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    5: _tools.RODict({
        "ID": 5,
        "name": "BONUS_SRC_ENTER_DUNGEON",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    6: _tools.RODict({
        "ID": 6,
        "name": "BONUS_SRC_FROM_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001984,
        "rewardMessage": ('开启礼包，获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 2
    }),
    7: _tools.RODict({
        "ID": 7,
        "name": "BONUS_SRC_CLAIM_TASK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 3
    }),
    8: _tools.RODict({
        "ID": 8,
        "name": "BONUS_SRC_BAG_SORT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 3
    }),
    9: _tools.RODict({
        "ID": 9,
        "name": "BONUS_SRC_GATHER",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    10: _tools.RODict({
        "ID": 10,
        "name": "BONUS_SRC_ITEMS_RECYCLE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    11: _tools.RODict({
        "ID": 11,
        "name": "BONUS_SRC_ENHANCE_BAG_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    12: _tools.RODict({
        "ID": 12,
        "name": "BONUS_SRC_ENHANCE_BODY_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    13: _tools.RODict({
        "ID": 13,
        "name": "BONUS_SRC_EQUIP_SWAP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    14: _tools.RODict({
        "ID": 14,
        "name": "BONUS_SRC_EQUIP_AFFIX_IDENTIFY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    15: _tools.RODict({
        "ID": 15,
        "name": "BONUS_SRC_MAIL_ATTACH",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001987,
        "rewardMessage": ('<color=&color211>邮件附件</color>', '查收邮件，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    }),
    16: _tools.RODict({
        "ID": 16,
        "name": "BONUS_SRC_ACTIVITY_COMPLETE",
        "isAntiAddicted": 1,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    17: _tools.RODict({
        "ID": 17,
        "name": "BONUS_SRC_DROP_ITEMS",
        "isAntiAddicted": 1,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    18: _tools.RODict({
        "ID": 18,
        "name": "BONUS_SRC_EQUIP_SELL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    19: _tools.RODict({
        "ID": 19,
        "name": "BONUS_SRC_BUY_ITEMS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    20: _tools.RODict({
        "ID": 20,
        "name": "BONUS_SRC_BUY_STORE_ITEMS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001990,
        "rewardMessage": ('<color=&color211>交易成功</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": (1, 2)
    }),
    21: _tools.RODict({
        "ID": 21,
        "name": "BONUS_SRC_SELL_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    22: _tools.RODict({
        "ID": 22,
        "name": "BONUS_SRC_GATHER_DROP",
        "isAntiAddicted": 1,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    23: _tools.RODict({
        "ID": 23,
        "name": "BONUS_SRC_EXCHANGE_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    24: _tools.RODict({
        "ID": 24,
        "name": "BONUS_SRC_ADD_TASK_ITEMS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    25: _tools.RODict({
        "ID": 25,
        "name": "BONUS_SRC_ABANDON_TASK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    26: _tools.RODict({
        "ID": 26,
        "name": "BONUS_SRC_EQUIP_DRESS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 3
    }),
    27: _tools.RODict({
        "ID": 27,
        "name": "BONUS_SRC_EQUIP_SELL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    28: _tools.RODict({
        "ID": 28,
        "name": "BONUS_SRC_EQUIP_DISASSEMBLE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001997,
        "rewardMessage": ('<color=&color211>分解获得</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": (1, 2)
    }),
    29: _tools.RODict({
        "ID": 29,
        "name": "BONUS_SRC_EQUIP_MANUFACTURE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    30: _tools.RODict({
        "ID": 30,
        "name": "BONUS_SRC_RANDOM_SYNTHESIS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    31: _tools.RODict({
        "ID": 31,
        "name": "BONUS_SRC_UPGRADE_SYNTHESIS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    32: _tools.RODict({
        "ID": 32,
        "name": "BONUS_SRC_EQUIP_AFFIX_WASHING",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    33: _tools.RODict({
        "ID": 33,
        "name": "BONUS_SRC_PETGEAR_DRESS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 3
    }),
    34: _tools.RODict({
        "ID": 34,
        "name": "BONUS_SRC_SKILL_UPGRADE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    35: _tools.RODict({
        "ID": 35,
        "name": "BONUS_SRC_CRUSADE_ADD_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    36: _tools.RODict({
        "ID": 36,
        "name": "BONUS_SRC_WEAPON_GLYPH_WASHING",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    37: _tools.RODict({
        "ID": 37,
        "name": "BONUS_SRC_EQUIP_BLESSING",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    38: _tools.RODict({
        "ID": 38,
        "name": "BONUS_SRC_DEAD_PENALTY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    39: _tools.RODict({
        "ID": 39,
        "name": "BONUS_SRC_RECOVER_DEAD_PENALTY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    40: _tools.RODict({
        "ID": 40,
        "name": "BONUS_SRC_RECOVER_DEAD_PENALTY_DEDUCT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    41: _tools.RODict({
        "ID": 41,
        "name": "BONUS_SRC_CLIENT_DELETE_MAIL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 3
    }),
    42: _tools.RODict({
        "ID": 42,
        "name": "BONUS_SRC_EXCEED_DELETE_MAIL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 3
    }),
    43: _tools.RODict({
        "ID": 43,
        "name": "BONUS_SRC_EXPIRE_DELETE_MAIL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 3
    }),
    44: _tools.RODict({
        "ID": 44,
        "name": "BONUS_SRC_CUBE_ROOM_ADD_TIMES",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    45: _tools.RODict({
        "ID": 45,
        "name": "BONUS_SRC_BUYCREDIT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001990,
        "rewardMessage": ('<color=&color211>购买成功</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    }),
    46: _tools.RODict({
        "ID": 46,
        "name": "BONUS_SRC_BUY_CURRENCY_GIFT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001990,
        "rewardMessage": ('<color=&color211>购买成功</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": (1, 2)
    }),
    47: _tools.RODict({
        "ID": 47,
        "name": "BONUS_SRC_CREATE_GUILD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    48: _tools.RODict({
        "ID": 48,
        "name": "BONUS_SRC_PETROLL_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    49: _tools.RODict({
        "ID": 49,
        "name": "BONUS_SRC_PETROLL_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    50: _tools.RODict({
        "ID": 50,
        "name": "BONUS_SRC_PETROLL_SECURED",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    51: _tools.RODict({
        "ID": 51,
        "name": "BONUS_SRC_GUILD_TRAIN_UPGRADE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    52: _tools.RODict({
        "ID": 52,
        "name": "BONUS_SRC_BAG_WAREHOUSE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    53: _tools.RODict({
        "ID": 53,
        "name": "BONUS_SRC_BAG_WAREHOUSE_UNLOCK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    54: _tools.RODict({
        "ID": 54,
        "name": "BONUS_SRC_GUILD_ASSIST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 4)
    }),
    55: _tools.RODict({
        "ID": 55,
        "name": "BONUS_SRC_GUILD_BUILDING_UPGRADE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    56: _tools.RODict({
        "ID": 56,
        "name": "BONUS_SRC_GUILD_MONEY_TO_FUND",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    57: _tools.RODict({
        "ID": 57,
        "name": "BONUS_SRC_MODIFY_GUILD_NAME",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    58: _tools.RODict({
        "ID": 58,
        "name": "BONUS_SRC_GUILD_DONATE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2, 4)
    }),
    59: _tools.RODict({
        "ID": 59,
        "name": "BONUS_SRC_GUILDTRAIN_RESET",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2, 4)
    }),
    60: _tools.RODict({
        "ID": 60,
        "name": "BONUS_SRC_AUCTION_LISTING_FEE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (2, 5)
    }),
    61: _tools.RODict({
        "ID": 61,
        "name": "BONUS_SRC_AUCTION_UNLIST_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 5)
    }),
    62: _tools.RODict({
        "ID": 62,
        "name": "BONUS_SRC_COIN_AUCTION_BUY_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 5)
    }),
    63: _tools.RODict({
        "ID": 63,
        "name": "BONUS_SRC_COIN_AUCTION_SALE_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (2, 5)
    }),
    64: _tools.RODict({
        "ID": 64,
        "name": "BONUS_SRC_AUCTION_TRANSACTION_TAX",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (2, 5)
    }),
    65: _tools.RODict({
        "ID": 65,
        "name": "BONUS_SRC_AUCTION_WITHDRAW_SETTLED_CURRENCY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 5)
    }),
    66: _tools.RODict({
        "ID": 66,
        "name": "BONUS_SRC_ACHIEVEMENT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001986,
        "rewardMessage": ('<color=&color211>成就达成</color>', '达成<color=&color57>{0}</color>成就，获得奖励：', '达成成就，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    }),
    67: _tools.RODict({
        "ID": 67,
        "name": "BONUS_SRC_TAKE_BACK_DROP_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    68: _tools.RODict({
        "ID": 68,
        "name": "BONUS_SRC_REDEEM_EQUIP_DROP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    69: _tools.RODict({
        "ID": 69,
        "name": "BONUS_SRC_REDEEM_FOR_PICKER",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    70: _tools.RODict({
        "ID": 70,
        "name": "BONUS_SRC_FETCH_OTHER_GIVEUP_DROP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    71: _tools.RODict({
        "ID": 71,
        "name": "BONUS_SRC_SCAN_ENEMY_POS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (2, 3)
    }),
    72: _tools.RODict({
        "ID": 72,
        "name": "BONUS_SRC_ADD_WONDER_LAND_TIMES",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    73: _tools.RODict({
        "ID": 73,
        "name": "BONUS_SRC_SUMMON_BOOSS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    74: _tools.RODict({
        "ID": 74,
        "name": "BONUS_SRC_COLLECTIBLE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    75: _tools.RODict({
        "ID": 75,
        "name": "BONUS_SRC_WELFARE_SIGN_IN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001988,
        "rewardMessage": ('<color=&color211>活动奖励</color>', '参与活动，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    }),
    76: _tools.RODict({
        "ID": 76,
        "name": "BONUS_SRC_GUILD_CITY_BATTLE_SIGN_UP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    77: _tools.RODict({
        "ID": 77,
        "name": "BONUS_SRC_CITY_BATTLE_BIDDING",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    78: _tools.RODict({
        "ID": 78,
        "name": "BONUS_SRC_TEAMDUN_ADD_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    79: _tools.RODict({
        "ID": 79,
        "name": "BONUS_SRC_QIXIE_ASSIST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    80: _tools.RODict({
        "ID": 80,
        "name": "BONUS_SRC_GUILD_CITY_BATTLE_TOKEN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    81: _tools.RODict({
        "ID": 81,
        "name": "BONUS_SRC_GUILD_ENEMY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    82: _tools.RODict({
        "ID": 82,
        "name": "BONUS_SRC_EQUIP_REPLACEMENT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    83: _tools.RODict({
        "ID": 83,
        "name": "BONUS_SRC_GUILD_CITY_BATTLE_MONEY_TO_COIN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    84: _tools.RODict({
        "ID": 84,
        "name": "BONUS_SRC_GUILD_COMPLETE_TASK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 4)
    }),
    85: _tools.RODict({
        "ID": 85,
        "name": "BONUS_SRC_TRANSPORT_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    86: _tools.RODict({
        "ID": 86,
        "name": "BONUS_SRC_RECYCLE_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    87: _tools.RODict({
        "ID": 87,
        "name": "BONUS_SRC_WORKSHOP_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    88: _tools.RODict({
        "ID": 88,
        "name": "BONUS_SRC_HEAL_WOUNDS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    89: _tools.RODict({
        "ID": 89,
        "name": "BONUS_SRC_SEND_RED_PACKET_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    90: _tools.RODict({
        "ID": 90,
        "name": "BONUS_SRC_GET_RED_PACKET_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    91: _tools.RODict({
        "ID": 91,
        "name": "BONUS_SRC_EXCHANGE_STORE_ITEMS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001992,
        "rewardMessage": ('<color=&color211>兑换成功</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": (1, 2)
    }),
    92: _tools.RODict({
        "ID": 92,
        "name": "BONUS_SRC_UPGRADE_BAG_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    93: _tools.RODict({
        "ID": 93,
        "name": "BONUS_SRC_UPGRADE_BODY_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    94: _tools.RODict({
        "ID": 94,
        "name": "BONUS_SRC_BINDVALUE_WASHING_BAG_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    95: _tools.RODict({
        "ID": 95,
        "name": "BONUS_SRC_BINDVALUE_WASHING_BODY_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    96: _tools.RODict({
        "ID": 96,
        "name": "BONUS_SRC_BUYCREDIT_MONTHCARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001993,
        "rewardMessage": ('<color=&color211>激活月卡</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    }),
    97: _tools.RODict({
        "ID": 97,
        "name": "BONUS_SRC_MONTHCARD_DAILY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001994,
        "rewardMessage": ('<color=&color211>月卡奖励</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    }),
    98: _tools.RODict({
        "ID": 98,
        "name": "BONUS_SRC_HANG_UP_INCOME",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001994,
        "rewardMessage": ('<color=&color211>月卡奖励</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    }),
    99: _tools.RODict({
        "ID": 99,
        "name": "BONUS_SRC_GIFT_CDK_ITEMS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001992,
        "rewardMessage": ('<color=&color211>兑换成功</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    }),
    100: _tools.RODict({
        "ID": 100,
        "name": "BONUS_SRC_TEAM_FIRST_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    101: _tools.RODict({
        "ID": 101,
        "name": "BONUS_SRC_TEAM_CLEAR_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    102: _tools.RODict({
        "ID": 102,
        "name": "BONUS_SRC_RAID_FIRST_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    103: _tools.RODict({
        "ID": 103,
        "name": "BONUS_SRC_RAID_CLEAR_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    104: _tools.RODict({
        "ID": 104,
        "name": "BONUS_SRC_GULID_DUNGEON_FIRST_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    105: _tools.RODict({
        "ID": 105,
        "name": "BONUS_SRC_GULID_DUNGEON_CLEAR_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    106: _tools.RODict({
        "ID": 106,
        "name": "BONUS_SRC_GULID_DUNGEON_OPEN_COIN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    107: _tools.RODict({
        "ID": 107,
        "name": "BONUS_SRC_GULID_DUNGEON_OPEN_MONEY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    108: _tools.RODict({
        "ID": 108,
        "name": "BONUS_SRC_GULID_DUNGEON_RESERVE_COIN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    109: _tools.RODict({
        "ID": 109,
        "name": "BONUS_SRC_GULID_DUNGEON_RESERVE_MONEY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    110: _tools.RODict({
        "ID": 110,
        "name": "BONUS_SRC_GULID_DUNGEON_CANCEL_COIN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    111: _tools.RODict({
        "ID": 111,
        "name": "BONUS_SRC_GULID_DUNGEON_CANCEL_MONEY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    112: _tools.RODict({
        "ID": 112,
        "name": "BONUS_SRC_MINE_WAR_SCORE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    113: _tools.RODict({
        "ID": 113,
        "name": "BONUS_SRC_MINE_WAR_GUILD_SHARE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    114: _tools.RODict({
        "ID": 114,
        "name": "BONUS_SRC_EXP_ACTION",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    115: _tools.RODict({
        "ID": 115,
        "name": "BONUS_SRC_TEAM_GOLD_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    116: _tools.RODict({
        "ID": 116,
        "name": "BONUS_SRC_RAID_GOLD_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    117: _tools.RODict({
        "ID": 117,
        "name": "BONUS_SRC_SHARE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001988,
        "rewardMessage": ('<color=&color211>活动奖励</color>', '参与活动，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    }),
    118: _tools.RODict({
        "ID": 118,
        "name": "BONUS_SRC_GULID_DUNGEON_RETURN_COIN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    119: _tools.RODict({
        "ID": 119,
        "name": "BONUS_SRC_GULID_DUNGEON_RETURN_MONEY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    120: _tools.RODict({
        "ID": 120,
        "name": "BONUS_SRC_WELFARE_LEVEL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    121: _tools.RODict({
        "ID": 121,
        "name": "BONUS_SRC_CUBE_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001995,
        "rewardMessage": ('<color=&color211>混沌回廊奖励</color>', '战利品：{0}'),
        "group": 1
    }),
    122: _tools.RODict({
        "ID": 122,
        "name": "BONUS_SRC_WONDERLAND_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001996,
        "rewardMessage": ('<color=&color211>天劫崖奖励</color>', '战利品：{0}'),
        "group": 1
    }),
    123: _tools.RODict({
        "ID": 123,
        "name": "BONUS_SRC_CURRENCY_EXCHANGE_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    124: _tools.RODict({
        "ID": 124,
        "name": "BONUS_SRC_CURRENCY_EXCHANGE_GET",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    125: _tools.RODict({
        "ID": 125,
        "name": "BONUS_SRC_GUILD_TOKEN_BID_FAILED",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    126: _tools.RODict({
        "ID": 126,
        "name": "BONUS_SRC_WELFARE_PCDRAINAGE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    127: _tools.RODict({
        "ID": 127,
        "name": "BONUS_SRC_WELFARE_TEN_SIGN_IN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001988,
        "rewardMessage": ('<color=&color211>活动奖励</color>', '参与活动，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    }),
    128: _tools.RODict({
        "ID": 128,
        "name": "BONUS_SRC_CUBE_PRAY_COST_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    129: _tools.RODict({
        "ID": 129,
        "name": "BONUS_SRC_SIEGEWAR_SIGNUP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    130: _tools.RODict({
        "ID": 130,
        "name": "BONUS_SRC_SIEGEWAR_BIDDING_FAILED",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    131: _tools.RODict({
        "ID": 131,
        "name": "BONUS_SRC_SIEGEWAR_BIDDING_SUCCESS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    132: _tools.RODict({
        "ID": 132,
        "name": "BONUS_SRC_SIEGEWAR_NOTICE_BATTLE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    133: _tools.RODict({
        "ID": 133,
        "name": "BONUS_SRC_SIEGEWAR_BROATCAST_LEADER",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 4
    }),
    134: _tools.RODict({
        "ID": 134,
        "name": "BONUS_SRC_EQUIPMENT_DROP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    135: _tools.RODict({
        "ID": 135,
        "name": "BONUS_SRC_SIEGEWAR_REWARD_LEADER",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    136: _tools.RODict({
        "ID": 136,
        "name": "BONUS_SRC_SIEGEWAR_REWARD_MVP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    137: _tools.RODict({
        "ID": 137,
        "name": "BONUS_SRC_SIEGEWAR_REWARD_RANK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    138: _tools.RODict({
        "ID": 138,
        "name": "BONUS_SRC_REDPACKAGE_RETURN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    139: _tools.RODict({
        "ID": 139,
        "name": "BONUS_SRC_EQUIPMENT_TAKE_EXPIRE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    140: _tools.RODict({
        "ID": 140,
        "name": "BONUS_SRC_EQUIPMENT_TAKE_OK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    141: _tools.RODict({
        "ID": 141,
        "name": "BONUS_SRC_EQUIPMENT_DROP_REMOVE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 3
    }),
    142: _tools.RODict({
        "ID": 142,
        "name": "BONUS_SRC_MONTHCARD_OFFLINE_BONUS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    143: _tools.RODict({
        "ID": 143,
        "name": "BONUS_SRC_DRAWCARD_GUARANTEED_BONUS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    144: _tools.RODict({
        "ID": 144,
        "name": "BONUS_SRC_PET_LEVEL_UP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    145: _tools.RODict({
        "ID": 145,
        "name": "BONUS_SRC_MAP_HANG_UP_INCOME",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 10)
    }),
    146: _tools.RODict({
        "ID": 146,
        "name": "BONUS_SRC_ENTER_CUBE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    147: _tools.RODict({
        "ID": 147,
        "name": "BONUS_SRC_CUBE_AUTO_RENEW",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    148: _tools.RODict({
        "ID": 148,
        "name": "BONUS_SRC_CUBE_FAILED_REWIND",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    149: _tools.RODict({
        "ID": 149,
        "name": "BONUS_SRC_ENTER_WONDER_LAND",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    150: _tools.RODict({
        "ID": 150,
        "name": "BONUS_SRC_WONDER_LAND_AUTO_RENEW",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    151: _tools.RODict({
        "ID": 151,
        "name": "BONUS_SRC_WONDER_LAND_FAILED_REWIND",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    152: _tools.RODict({
        "ID": 152,
        "name": "BONUS_SRC_ITEM_DISASSEMBLE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001997,
        "rewardMessage": ('<color=&color211>分解获得</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": (1, 2)
    }),
    153: _tools.RODict({
        "ID": 153,
        "name": "BONUS_SRC_AUTO_ENHANCE_BAG_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    154: _tools.RODict({
        "ID": 154,
        "name": "BONUS_SRC_AUTO_ENHANCE_BODY_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    155: _tools.RODict({
        "ID": 155,
        "name": "BONUS_SRC_LEVEL_UP_MERIDIAN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    156: _tools.RODict({
        "ID": 156,
        "name": "BONUS_SRC_ENHANCE_MERIDIAN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    157: _tools.RODict({
        "ID": 157,
        "name": "BONUS_SRC_BIND_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    158: _tools.RODict({
        "ID": 158,
        "name": "BONUS_SRC_KILLER_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    159: _tools.RODict({
        "ID": 159,
        "name": "BONUS_SRC_FINANCIER_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    160: _tools.RODict({
        "ID": 160,
        "name": "BONUS_SRC_BOUNTY_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    161: _tools.RODict({
        "ID": 161,
        "name": "BONUS_SRC_BOUNTY_BACK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    162: _tools.RODict({
        "ID": 162,
        "name": "BONUS_SRC_REWARD_BACK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    163: _tools.RODict({
        "ID": 163,
        "name": "BONUS_SRC_MAIL_CLEAR_DUETIME",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 3
    }),
    164: _tools.RODict({
        "ID": 164,
        "name": "BONUS_SRC_DEPOSIT_REFUND",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    165: _tools.RODict({
        "ID": 165,
        "name": "BONUS_SRC_DEPOSIT_ALL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    166: _tools.RODict({
        "ID": 166,
        "name": "BONUS_SRC_PET_REROLL_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    167: _tools.RODict({
        "ID": 167,
        "name": "BONUS_SRC_REDEEM_EXPIRE_TAKE_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    168: _tools.RODict({
        "ID": 168,
        "name": "BONUS_SRC_DROP_RETURN_BACK_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    169: _tools.RODict({
        "ID": 169,
        "name": "BONUS_SRC_DROP_REMOVE_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    170: _tools.RODict({
        "ID": 170,
        "name": "BONUS_SRC_EQUIP_SOUL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    171: _tools.RODict({
        "ID": 171,
        "name": "BONUS_SRC_RECOVERY_TICKET",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    172: _tools.RODict({
        "ID": 172,
        "name": "BONUS_SRC_ENTER_ABYSS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": (1, 2)
    }),
    173: _tools.RODict({
        "ID": 173,
        "name": "BONUS_SRC_ADD_ABYSS_TIMES",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    174: _tools.RODict({
        "ID": 174,
        "name": "BONUS_SRC_ABYSS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001998,
        "rewardMessage": ('<color=&color211>归墟奖励</color>', '战利品：{0}'),
        "group": 1
    }),
    175: _tools.RODict({
        "ID": 175,
        "name": "BONUS_SRC_ENTER_ABYSS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    176: _tools.RODict({
        "ID": 176,
        "name": "BONUS_SRC_ABYSS_AUTO_RENEW",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 2
    }),
    177: _tools.RODict({
        "ID": 177,
        "name": "BONUS_SRC_ABYSS_FAILED_REWIND",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": 1
    }),
    178: _tools.RODict({
        "ID": 178,
        "name": "BONUS_SRC_LEASE_ADD_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    179: _tools.RODict({
        "ID": 179,
        "name": "BONUS_SRC_LEASE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    180: _tools.RODict({
        "ID": 180,
        "name": "BONUS_SRC_LEASE_CANCEL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    181: _tools.RODict({
        "ID": 181,
        "name": "BONUS_SRC_LEASE_RETURN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    182: _tools.RODict({
        "ID": 182,
        "name": "BONUS_SRC_LEASE_INCOME",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    183: _tools.RODict({
        "ID": 183,
        "name": "BONUS_SRC_DROP_PAY_PRICE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    184: _tools.RODict({
        "ID": 184,
        "name": "BONUS_SRC_DROP_GIVE_UP_RETURN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    185: _tools.RODict({
        "ID": 185,
        "name": "BONUS_SRC_EQUIP_WASH",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    186: _tools.RODict({
        "ID": 186,
        "name": "BONUS_SRC_EXPLORATION_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    187: _tools.RODict({
        "ID": 187,
        "name": "BONUS_SRC_DUNGEON_FINISHED",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    188: _tools.RODict({
        "ID": 188,
        "name": "BONUS_SRC_INNER_DEMON_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    189: _tools.RODict({
        "ID": 189,
        "name": "BONUS_SRC_AUCTION_SNATCH_FAIL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    190: _tools.RODict({
        "ID": 190,
        "name": "BONUS_SRC_DROP_PAY_PRICE_RETURN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    191: _tools.RODict({
        "ID": 191,
        "name": "BONUS_SRC_COST_HORN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None,
        "group": None
    }),
    192: _tools.RODict({
        "ID": 192,
        "name": "BONUS_SRC_PET_GACHA",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001997,
        "rewardMessage": ('<color=&color211>精灵召唤</color>', '获得精灵：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口'),
        "group": 1
    })
})
minKey = 1
maxKey = 192