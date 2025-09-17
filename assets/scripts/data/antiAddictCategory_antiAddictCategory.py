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
        "rewardMessage": None
    }),
    2: _tools.RODict({
        "ID": 2,
        "name": "BONUS_SRC_COMPLETE_TASK",
        "isAntiAddicted": 1,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001985,
        "rewardMessage": ('<color=&color18>任务完成</color>', '完成<color=&color18>{0}</color>任务<color=&color18>{1}</color>，获得奖励：', '完成任务，获得奖励：', '<color=&color8>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    3: _tools.RODict({
        "ID": 3,
        "name": "BONUS_SRC_GM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54000009,
        "rewardMessage": None
    }),
    4: _tools.RODict({
        "ID": 4,
        "name": "BONUS_SRC_UNLOCK_GRIDS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    5: _tools.RODict({
        "ID": 5,
        "name": "BONUS_SRC_ENTER_DUNGEON",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    6: _tools.RODict({
        "ID": 6,
        "name": "BONUS_SRC_FROM_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001984,
        "rewardMessage": ('开启礼包，获得道具：', '<color=&color8>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    7: _tools.RODict({
        "ID": 7,
        "name": "BONUS_SRC_CLAIM_TASK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    8: _tools.RODict({
        "ID": 8,
        "name": "BONUS_SRC_BAG_SORT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    9: _tools.RODict({
        "ID": 9,
        "name": "BONUS_SRC_GATHER",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    10: _tools.RODict({
        "ID": 10,
        "name": "BONUS_SRC_ITEMS_RECYCLE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    11: _tools.RODict({
        "ID": 11,
        "name": "BONUS_SRC_ENHANCE_BAG_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    12: _tools.RODict({
        "ID": 12,
        "name": "BONUS_SRC_ENHANCE_BODY_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    13: _tools.RODict({
        "ID": 13,
        "name": "BONUS_SRC_EQUIP_SWAP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    14: _tools.RODict({
        "ID": 14,
        "name": "BONUS_SRC_EQUIP_AFFIX_IDENTIFY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    15: _tools.RODict({
        "ID": 15,
        "name": "BONUS_SRC_MAIL_ATTACH",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001987,
        "rewardMessage": ('<color=&color18>邮件附件</color>', '查收邮件，获得奖励：', '<color=&color8>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    16: _tools.RODict({
        "ID": 16,
        "name": "BONUS_SRC_ACTIVITY_COMPLETE",
        "isAntiAddicted": 1,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    17: _tools.RODict({
        "ID": 17,
        "name": "BONUS_SRC_DROP_ITEMS",
        "isAntiAddicted": 1,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    18: _tools.RODict({
        "ID": 18,
        "name": "BONUS_SRC_EQUIP_SELL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    19: _tools.RODict({
        "ID": 19,
        "name": "BONUS_SRC_BUY_ITEMS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    20: _tools.RODict({
        "ID": 20,
        "name": "BONUS_SRC_BUY_STORE_ITEMS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001990,
        "rewardMessage": ('<color=&color18>购买成功</color>', '获得道具：', '<color=&color8>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    21: _tools.RODict({
        "ID": 21,
        "name": "BONUS_SRC_SELL_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    22: _tools.RODict({
        "ID": 22,
        "name": "BONUS_SRC_GATHER_DROP",
        "isAntiAddicted": 1,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    23: _tools.RODict({
        "ID": 23,
        "name": "BONUS_SRC_EXCHANGE_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    24: _tools.RODict({
        "ID": 24,
        "name": "BONUS_SRC_ADD_TASK_ITEMS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    25: _tools.RODict({
        "ID": 25,
        "name": "BONUS_SRC_ABANDON_TASK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    26: _tools.RODict({
        "ID": 26,
        "name": "BONUS_SRC_EQUIP_DRESS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    27: _tools.RODict({
        "ID": 27,
        "name": "BONUS_SRC_EQUIP_SELL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    28: _tools.RODict({
        "ID": 28,
        "name": "BONUS_SRC_EQUIP_DISASSEMBLE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    29: _tools.RODict({
        "ID": 29,
        "name": "BONUS_SRC_EQUIP_MANUFACTURE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    30: _tools.RODict({
        "ID": 30,
        "name": "BONUS_SRC_RANDOM_SYNTHESIS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    31: _tools.RODict({
        "ID": 31,
        "name": "BONUS_SRC_UPGRADE_SYNTHESIS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    32: _tools.RODict({
        "ID": 32,
        "name": "BONUS_SRC_EQUIP_AFFIX_WASHING",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    33: _tools.RODict({
        "ID": 33,
        "name": "BONUS_SRC_PETGEAR_DRESS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    34: _tools.RODict({
        "ID": 34,
        "name": "BONUS_SRC_SKILL_UPGRADE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    35: _tools.RODict({
        "ID": 35,
        "name": "BONUS_SRC_CRUSADE_ADD_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    36: _tools.RODict({
        "ID": 36,
        "name": "BONUS_SRC_WEAPON_GLYPH_WASHING",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    37: _tools.RODict({
        "ID": 37,
        "name": "BONUS_SRC_EQUIP_BLESSING",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    38: _tools.RODict({
        "ID": 38,
        "name": "BONUS_SRC_DEAD_PENALTY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    39: _tools.RODict({
        "ID": 39,
        "name": "BONUS_SRC_RECOVER_DEAD_PENALTY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    40: _tools.RODict({
        "ID": 40,
        "name": "BONUS_SRC_RECOVER_DEAD_PENALTY_DEDUCT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    41: _tools.RODict({
        "ID": 41,
        "name": "BONUS_SRC_CLIENT_DELETE_MAIL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    42: _tools.RODict({
        "ID": 42,
        "name": "BONUS_SRC_EXCEED_DELETE_MAIL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    43: _tools.RODict({
        "ID": 43,
        "name": "BONUS_SRC_EXPIRE_DELETE_MAIL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    44: _tools.RODict({
        "ID": 44,
        "name": "BONUS_SRC_CUBE_ROOM_ADD_TIMES",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    45: _tools.RODict({
        "ID": 45,
        "name": "BONUS_SRC_BUYCREDIT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001990,
        "rewardMessage": ('<color=&color18>购买成功</color>', '获得道具：', '<color=&color8>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    46: _tools.RODict({
        "ID": 46,
        "name": "BONUS_SRC_BUY_CURRENCY_GIFT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    47: _tools.RODict({
        "ID": 47,
        "name": "BONUS_SRC_CREATE_GUILD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    48: _tools.RODict({
        "ID": 48,
        "name": "BONUS_SRC_PETROLL_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    49: _tools.RODict({
        "ID": 49,
        "name": "BONUS_SRC_PETROLL_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    50: _tools.RODict({
        "ID": 50,
        "name": "BONUS_SRC_PETROLL_SECURED",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    51: _tools.RODict({
        "ID": 51,
        "name": "BONUS_SRC_GUILD_TRAIN_UPGRADE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    52: _tools.RODict({
        "ID": 52,
        "name": "BONUS_SRC_BAG_WAREHOUSE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    53: _tools.RODict({
        "ID": 53,
        "name": "BONUS_SRC_BAG_WAREHOUSE_UNLOCK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    54: _tools.RODict({
        "ID": 54,
        "name": "BONUS_SRC_GUILD_ASSIST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    55: _tools.RODict({
        "ID": 55,
        "name": "BONUS_SRC_GUILD_BUILDING_UPGRADE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    56: _tools.RODict({
        "ID": 56,
        "name": "BONUS_SRC_GUILD_MONEY_TO_FUND",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    57: _tools.RODict({
        "ID": 57,
        "name": "BONUS_SRC_MODIFY_GUILD_NAME",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    58: _tools.RODict({
        "ID": 58,
        "name": "BONUS_SRC_GUILD_DONATE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    59: _tools.RODict({
        "ID": 59,
        "name": "BONUS_SRC_GUILDTRAIN_RESET",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    60: _tools.RODict({
        "ID": 60,
        "name": "BONUS_SRC_AUCTION_LISTING_FEE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    61: _tools.RODict({
        "ID": 61,
        "name": "BONUS_SRC_AUCTION_UNLIST_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    62: _tools.RODict({
        "ID": 62,
        "name": "BONUS_SRC_COIN_AUCTION_BUY_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    63: _tools.RODict({
        "ID": 63,
        "name": "BONUS_SRC_COIN_AUCTION_SALE_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    64: _tools.RODict({
        "ID": 64,
        "name": "BONUS_SRC_AUCTION_TRANSACTION_TAX",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    65: _tools.RODict({
        "ID": 65,
        "name": "BONUS_SRC_AUCTION_WITHDRAW_SETTLED_CURRENCY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    66: _tools.RODict({
        "ID": 66,
        "name": "BONUS_SRC_ACHIEVEMENT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001986,
        "rewardMessage": ('<color=&color18>成就达成</color>', '达成<color=&color18>{0}</color>成就，获得奖励：', '达成成就，获得奖励：', '<color=&color8>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    67: _tools.RODict({
        "ID": 67,
        "name": "BONUS_SRC_TAKE_BACK_DROP_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    68: _tools.RODict({
        "ID": 68,
        "name": "BONUS_SRC_REDEEM_EQUIP_DROP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    69: _tools.RODict({
        "ID": 69,
        "name": "BONUS_SRC_REDEEM_FOR_PICKER",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    70: _tools.RODict({
        "ID": 70,
        "name": "BONUS_SRC_FETCH_OTHER_GIVEUP_DROP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    71: _tools.RODict({
        "ID": 71,
        "name": "BONUS_SRC_SCAN_ENEMY_POS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    72: _tools.RODict({
        "ID": 72,
        "name": "BONUS_SRC_ADD_WONDER_LAND_TIMES",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    73: _tools.RODict({
        "ID": 73,
        "name": "BONUS_SRC_SUMMON_BOOSS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    74: _tools.RODict({
        "ID": 74,
        "name": "BONUS_SRC_COLLECTIBLE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    75: _tools.RODict({
        "ID": 75,
        "name": "BONUS_SRC_WELFARE_SIGN_IN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001988,
        "rewardMessage": ('<color=&color18>活动奖励</color>', '参与活动，获得奖励：', '<color=&color8>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    76: _tools.RODict({
        "ID": 76,
        "name": "BONUS_SRC_GUILD_CITY_BATTLE_SIGN_UP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    77: _tools.RODict({
        "ID": 77,
        "name": "BONUS_SRC_CITY_BATTLE_BIDDING",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    78: _tools.RODict({
        "ID": 78,
        "name": "BONUS_SRC_TEAMDUN_ADD_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    79: _tools.RODict({
        "ID": 79,
        "name": "BONUS_SRC_QIXIE_ASSIST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    80: _tools.RODict({
        "ID": 80,
        "name": "BONUS_SRC_GUILD_CITY_BATTLE_TOKEN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    81: _tools.RODict({
        "ID": 81,
        "name": "BONUS_SRC_GUILD_ENEMY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    82: _tools.RODict({
        "ID": 82,
        "name": "BONUS_SRC_EQUIP_REPLACEMENT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    83: _tools.RODict({
        "ID": 83,
        "name": "BONUS_SRC_GUILD_CITY_BATTLE_MONEY_TO_COIN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    84: _tools.RODict({
        "ID": 84,
        "name": "BONUS_SRC_GUILD_COMPLETE_TASK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    85: _tools.RODict({
        "ID": 85,
        "name": "BONUS_SRC_TRANSPORT_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    86: _tools.RODict({
        "ID": 86,
        "name": "BONUS_SRC_RECYCLE_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    87: _tools.RODict({
        "ID": 87,
        "name": "BONUS_SRC_WORKSHOP_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    88: _tools.RODict({
        "ID": 88,
        "name": "BONUS_SRC_HEAL_WOUNDS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    89: _tools.RODict({
        "ID": 89,
        "name": "BONUS_SRC_SEND_RED_PACKET_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    90: _tools.RODict({
        "ID": 90,
        "name": "BONUS_SRC_GET_RED_PACKET_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    })
})
minKey = 1
maxKey = 90