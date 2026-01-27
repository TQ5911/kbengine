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
        "rewardMessage": ('<color=&color211>任务完成</color>', '完成<color=&color57>{0}</color>任务<color=&color57>{1}</color>，获得奖励：', '完成任务，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
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
        "rewardMessage": ('开启礼包，获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
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
        "rewardMessage": ('<color=&color211>邮件附件</color>', '查收邮件，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
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
        "rewardMessage": ('<color=&color211>交易成功</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
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
        "messageId": 54001997,
        "rewardMessage": ('<color=&color211>分解获得</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
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
        "rewardMessage": ('<color=&color211>购买成功</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    46: _tools.RODict({
        "ID": 46,
        "name": "BONUS_SRC_BUY_CURRENCY_GIFT",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001990,
        "rewardMessage": ('<color=&color211>购买成功</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
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
        "rewardMessage": ('<color=&color211>成就达成</color>', '达成<color=&color57>{0}</color>成就，获得奖励：', '达成成就，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
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
        "rewardMessage": ('<color=&color211>活动奖励</color>', '参与活动，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
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
    }),
    91: _tools.RODict({
        "ID": 91,
        "name": "BONUS_SRC_EXCHANGE_STORE_ITEMS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001992,
        "rewardMessage": ('<color=&color211>兑换成功</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    92: _tools.RODict({
        "ID": 92,
        "name": "BONUS_SRC_UPGRADE_BAG_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    93: _tools.RODict({
        "ID": 93,
        "name": "BONUS_SRC_UPGRADE_BODY_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    94: _tools.RODict({
        "ID": 94,
        "name": "BONUS_SRC_BINDVALUE_WASHING_BAG_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    95: _tools.RODict({
        "ID": 95,
        "name": "BONUS_SRC_BINDVALUE_WASHING_BODY_EQUIP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    96: _tools.RODict({
        "ID": 96,
        "name": "BONUS_SRC_BUYCREDIT_MONTHCARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001993,
        "rewardMessage": ('<color=&color211>激活月卡</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    97: _tools.RODict({
        "ID": 97,
        "name": "BONUS_SRC_MONTHCARD_DAILY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001994,
        "rewardMessage": ('<color=&color211>月卡奖励</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    98: _tools.RODict({
        "ID": 98,
        "name": "BONUS_SRC_HANG_UP_INCOME",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    99: _tools.RODict({
        "ID": 99,
        "name": "BONUS_SRC_GIFT_CDK_ITEMS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001992,
        "rewardMessage": ('<color=&color211>兑换成功</color>', '获得道具：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    100: _tools.RODict({
        "ID": 100,
        "name": "BONUS_SRC_TEAM_FIRST_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    101: _tools.RODict({
        "ID": 101,
        "name": "BONUS_SRC_TEAM_CLEAR_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    102: _tools.RODict({
        "ID": 102,
        "name": "BONUS_SRC_RAID_FIRST_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    103: _tools.RODict({
        "ID": 103,
        "name": "BONUS_SRC_RAID_CLEAR_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    104: _tools.RODict({
        "ID": 104,
        "name": "BONUS_SRC_GULID_DUNGEON_FIRST_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    105: _tools.RODict({
        "ID": 105,
        "name": "BONUS_SRC_GULID_DUNGEON_CLEAR_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    106: _tools.RODict({
        "ID": 106,
        "name": "BONUS_SRC_GULID_DUNGEON_OPEN_COIN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    107: _tools.RODict({
        "ID": 107,
        "name": "BONUS_SRC_GULID_DUNGEON_OPEN_MONEY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    108: _tools.RODict({
        "ID": 108,
        "name": "BONUS_SRC_GULID_DUNGEON_RESERVE_COIN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    109: _tools.RODict({
        "ID": 109,
        "name": "BONUS_SRC_GULID_DUNGEON_RESERVE_MONEY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    110: _tools.RODict({
        "ID": 110,
        "name": "BONUS_SRC_GULID_DUNGEON_CANCEL_COIN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    111: _tools.RODict({
        "ID": 111,
        "name": "BONUS_SRC_GULID_DUNGEON_CANCEL_MONEY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    112: _tools.RODict({
        "ID": 112,
        "name": "BONUS_SRC_MINE_WAR_SCORE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    113: _tools.RODict({
        "ID": 113,
        "name": "BONUS_SRC_MINE_WAR_GUILD_SHARE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    114: _tools.RODict({
        "ID": 114,
        "name": "BONUS_SRC_EXP_ACTION",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    115: _tools.RODict({
        "ID": 115,
        "name": "BONUS_SRC_TEAM_GOLD_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    116: _tools.RODict({
        "ID": 116,
        "name": "BONUS_SRC_RAID_GOLD_PASS_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    117: _tools.RODict({
        "ID": 117,
        "name": "BONUS_SRC_SHARE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001988,
        "rewardMessage": ('<color=&color211>活动奖励</color>', '参与活动，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    118: _tools.RODict({
        "ID": 118,
        "name": "BONUS_SRC_GULID_DUNGEON_RETURN_COIN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    119: _tools.RODict({
        "ID": 119,
        "name": "BONUS_SRC_GULID_DUNGEON_RETURN_MONEY",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    120: _tools.RODict({
        "ID": 120,
        "name": "BONUS_SRC_WELFARE_LEVEL",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    121: _tools.RODict({
        "ID": 121,
        "name": "BONUS_SRC_CUBE_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001995,
        "rewardMessage": ('<color=&color211>混沌回廊奖励</color>', '战利品：{0}')
    }),
    122: _tools.RODict({
        "ID": 122,
        "name": "BONUS_SRC_WONDERLAND_REWARD",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001996,
        "rewardMessage": ('<color=&color211>试炼峰奖励</color>', '战利品：{0}')
    }),
    123: _tools.RODict({
        "ID": 123,
        "name": "BONUS_SRC_CURRENCY_EXCHANGE_COST",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    124: _tools.RODict({
        "ID": 124,
        "name": "BONUS_SRC_CURRENCY_EXCHANGE_GET",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    125: _tools.RODict({
        "ID": 125,
        "name": "BONUS_SRC_GUILD_TOKEN_BID_FAILED",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    126: _tools.RODict({
        "ID": 126,
        "name": "BONUS_SRC_WELFARE_PCDRAINAGE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    127: _tools.RODict({
        "ID": 127,
        "name": "BONUS_SRC_WELFARE_TEN_SIGN_IN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 54001988,
        "rewardMessage": ('<color=&color211>活动奖励</color>', '参与活动，获得奖励：', '<color=&color211>{0}秒</color>后自动关闭，点击屏幕可直接关闭窗口')
    }),
    128: _tools.RODict({
        "ID": 128,
        "name": "BONUS_SRC_CUBE_PRAY_COST_ITEM",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    129: _tools.RODict({
        "ID": 129,
        "name": "BONUS_SRC_SIEGEWAR_SIGNUP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    130: _tools.RODict({
        "ID": 130,
        "name": "BONUS_SRC_SIEGEWAR_BIDDING_FAILED",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    131: _tools.RODict({
        "ID": 131,
        "name": "BONUS_SRC_SIEGEWAR_BIDDING_SUCCESS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    132: _tools.RODict({
        "ID": 132,
        "name": "BONUS_SRC_SIEGEWAR_NOTICE_BATTLE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    133: _tools.RODict({
        "ID": 133,
        "name": "BONUS_SRC_SIEGEWAR_BROATCAST_LEADER",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    134: _tools.RODict({
        "ID": 134,
        "name": "BONUS_SRC_EQUIPMENT_DROP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    135: _tools.RODict({
        "ID": 135,
        "name": "BONUS_SRC_SIEGEWAR_REWARD_LEADER",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    136: _tools.RODict({
        "ID": 136,
        "name": "BONUS_SRC_SIEGEWAR_REWARD_MVP",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    137: _tools.RODict({
        "ID": 137,
        "name": "BONUS_SRC_SIEGEWAR_REWARD_RANK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    138: _tools.RODict({
        "ID": 138,
        "name": "BONUS_SRC_REDPACKAGE_RETURN",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    139: _tools.RODict({
        "ID": 139,
        "name": "BONUS_SRC_EQUIPMENT_TAKE_EXPIRE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    140: _tools.RODict({
        "ID": 140,
        "name": "BONUS_SRC_EQUIPMENT_TAKE_OK",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    141: _tools.RODict({
        "ID": 141,
        "name": "BONUS_SRC_EQUIPMENT_DROP_REMOVE",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    142: _tools.RODict({
        "ID": 142,
        "name": "BONUS_SRC_MONTHCARD_OFFLINE_BONUS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    }),
    143: _tools.RODict({
        "ID": 143,
        "name": "BONUS_SRC_DRAWCARD_GUARANTEED_BONUS",
        "isAntiAddicted": 0,
        "abandonWhenBagFull": 0,
        "rewardDescribe": "",
        "messageId": 0,
        "rewardMessage": None
    })
})
minKey = 1
maxKey = 143