# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: relationConfig/relationConfig
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "msgId_relationBeFriendMsg": _tools.RODict({
        "ID": "msgId_relationBeFriendMsg",
        "value": 58000005,
    }),
    "relationFriendNumMax": _tools.RODict({
        "ID": "relationFriendNumMax",
        "value": 100,
    }),
    "relationRecentlyNumMax": _tools.RODict({
        "ID": "relationRecentlyNumMax",
        "value": 30,
    }),
    "relationStateRefreshInterval": _tools.RODict({
        "ID": "relationStateRefreshInterval",
        "value": 1800,
    }),
    "relationMsgNumMax_s": _tools.RODict({
        "ID": "relationMsgNumMax_s",
        "value": 100,
    }),
    "relationMsgNumMax_c": _tools.RODict({
        "ID": "relationMsgNumMax_c",
        "value": 1000,
    }),
    "relationApplicationMax_receive": _tools.RODict({
        "ID": "relationApplicationMax_receive",
        "value": 100,
    }),
    "relationBlacklistNumMax": _tools.RODict({
        "ID": "relationBlacklistNumMax",
        "value": 50,
    }),
    "relationChatSpacing": _tools.RODict({
        "ID": "relationChatSpacing",
        "value": 1800,
    }),
    "relationApplicationExpiryDate": _tools.RODict({
        "ID": "relationApplicationExpiryDate",
        "value": 10,
    }),
    "offLineTime1": _tools.RODict({
        "ID": "offLineTime1",
        "value": "{0}分钟前",
    }),
    "offLineTime2": _tools.RODict({
        "ID": "offLineTime2",
        "value": "{0}小时前",
    }),
    "offLineTime3": _tools.RODict({
        "ID": "offLineTime3",
        "value": "{0}天前",
    }),
    "msgId_relationFriendNumMax_self": _tools.RODict({
        "ID": "msgId_relationFriendNumMax_self",
        "value": 54000421,
    }),
    "msgId_friendDeleteConfirm": _tools.RODict({
        "ID": "msgId_friendDeleteConfirm",
        "value": 54000423,
    }),
    "msgId_blacklistConfirm": _tools.RODict({
        "ID": "msgId_blacklistConfirm",
        "value": 54000424,
    }),
    "relationApplicationMax_target": _tools.RODict({
        "ID": "relationApplicationMax_target",
        "value": 54000425,
    }),
    "msgId_relationApplicationClearConfirm": _tools.RODict({
        "ID": "msgId_relationApplicationClearConfirm",
        "value": 54000426,
    }),
    "msgId_relationApplication_empty": _tools.RODict({
        "ID": "msgId_relationApplication_empty",
        "value": 54000427,
    }),
    "msgId_relationSearch_empty": _tools.RODict({
        "ID": "msgId_relationSearch_empty",
        "value": 54000428,
    }),
    "msgId_relationSearchFailed": _tools.RODict({
        "ID": "msgId_relationSearchFailed",
        "value": 54000429,
    }),
    "msgId_relationApplication_expired": _tools.RODict({
        "ID": "msgId_relationApplication_expired",
        "value": 54000430,
    }),
    "msgId_relationTargetInBlacklist": _tools.RODict({
        "ID": "msgId_relationTargetInBlacklist",
        "value": 54000384,
    }),
    "soundId_friend_invitation": _tools.RODict({
        "ID": "soundId_friend_invitation",
        "value": 85010046,
    }),
    "soundId_friend_msg": _tools.RODict({
        "ID": "soundId_friend_msg",
        "value": 85010047,
    }),
    "chatButtonGroup_friend": _tools.RODict({
        "ID": "chatButtonGroup_friend",
        "value": 1,
    }),
    "chatButtonGroup_blacklist": _tools.RODict({
        "ID": "chatButtonGroup_blacklist",
        "value": 3,
    }),
    "msgId_relationRecently_delete": _tools.RODict({
        "ID": "msgId_relationRecently_delete",
        "value": 54000431,
    }),
    "relationFriendChatCD": _tools.RODict({
        "ID": "relationFriendChatCD",
        "value": 1,
    }),
    "relationAddFriendConfirm": _tools.RODict({
        "ID": "relationAddFriendConfirm",
        "value": 54000432,
    }),
    "relationFriendApplySentMsg": _tools.RODict({
        "ID": "relationFriendApplySentMsg",
        "value": 54000106,
    }),
    "relationFriendNumMaxMsg": _tools.RODict({
        "ID": "relationFriendNumMaxMsg",
        "value": 54000388,
    }),
    "blacklistNumMaxMsg": _tools.RODict({
        "ID": "blacklistNumMaxMsg",
        "value": 54000385,
    }),
    "searchKeywordColor": _tools.RODict({
        "ID": "searchKeywordColor",
        "value": 28,
    }),
    "enemySearchItem": _tools.RODict({
        "ID": "enemySearchItem",
        "value": 30000303,
    }),
    "enemySearchItemNum": _tools.RODict({
        "ID": "enemySearchItemNum",
        "value": 1,
    }),
    "enemySearchCD": _tools.RODict({
        "ID": "enemySearchCD",
        "value": 600,
    }),
    "enemyCurrentNum": _tools.RODict({
        "ID": "enemyCurrentNum",
        "value": "仇敌：{0}/{1}",
    }),
    "enemyResearchFontColor": _tools.RODict({
        "ID": "enemyResearchFontColor",
        "value": "<color=#54e7f2>{0}</color>\n<color=#9e9886>{1}</color>",
    }),
    "enemyNotResearch": _tools.RODict({
        "ID": "enemyNotResearch",
        "value": "暂未探查",
    }),
    "enemySkillTip1": _tools.RODict({
        "ID": "enemySkillTip1",
        "value": "<color=#c60c0c>被击败</color>",
    }),
    "enemySkillTip2": _tools.RODict({
        "ID": "enemySkillTip2",
        "value": "<color=#038304>击败</color>",
    }),
    "enemyResearchAgain": _tools.RODict({
        "ID": "enemyResearchAgain",
        "value": "{0}\n后可再次探查",
    }),
    "enemyDeleteConfirm": _tools.RODict({
        "ID": "enemyDeleteConfirm",
        "value": 54001920,
    }),
    "enemyNotOnline": _tools.RODict({
        "ID": "enemyNotOnline",
        "value": 54001921,
    }),
    "enemyCompassLack": _tools.RODict({
        "ID": "enemyCompassLack",
        "value": 54001922,
    }),
    "enemyResearchConfirm": _tools.RODict({
        "ID": "enemyResearchConfirm",
        "value": 54001923,
    }),
    "enemyResearchResult": _tools.RODict({
        "ID": "enemyResearchResult",
        "value": 54001924,
    }),
    "relationSentFriendRequest": _tools.RODict({
        "ID": "relationSentFriendRequest",
        "value": 54000433,
    }),
    "relationSearch_tryLater": _tools.RODict({
        "ID": "relationSearch_tryLater",
        "value": 54000434,
    }),
    "enemyPositionRefreshTime": _tools.RODict({
        "ID": "enemyPositionRefreshTime",
        "value": 60,
    }),
    "enemyNumLimit": _tools.RODict({
        "ID": "enemyNumLimit",
        "value": 30,
    }),
    "enemyRecordNumLimit": _tools.RODict({
        "ID": "enemyRecordNumLimit",
        "value": 100,
    }),
    "enemyPositionCrossServer": _tools.RODict({
        "ID": "enemyPositionCrossServer",
        "value": "跨服场景",
    }),
    "enemyReserachName": _tools.RODict({
        "ID": "enemyReserachName",
        "value": "<color=#d35a66>{0}</color>",
    }),
    "enemyReserachNameOffline": _tools.RODict({
        "ID": "enemyReserachNameOffline",
        "value": "<color=#727272>{0}({1})</color>",
    }),
    "enemyReserachPlace": _tools.RODict({
        "ID": "enemyReserachPlace",
        "value": "<color=#54e7f2>{0}</color>",
    }),
    "enemyReserachNamePlaceOffline": _tools.RODict({
        "ID": "enemyReserachNamePlaceOffline",
        "value": "<color=#727272>{0}</color>",
    }),
    "enemyReserachNPC": _tools.RODict({
        "ID": "enemyReserachNPC",
        "value": 18000504,
    }),
    "enemyReserachText": _tools.RODict({
        "ID": "enemyReserachText",
        "value": "离线",
    }),
    "enemyReserachPlaceUpdate": _tools.RODict({
        "ID": "enemyReserachPlaceUpdate",
        "value": "<color=#d35a66>{0}</color>位置已更新至<color=#54e7f2>{1}</color>",
    }),
    "enemyReserachText2": _tools.RODict({
        "ID": "enemyReserachText2",
        "value": "持续探索中，每{0}秒探查一次仇敌位置",
    }),
    "hostileCurrentNum": _tools.RODict({
        "ID": "hostileCurrentNum",
        "value": "敌对：{0}/{1}",
    }),
    "hostileNumLimit": _tools.RODict({
        "ID": "hostileNumLimit",
        "value": 30,
    }),
    "hostileListMax": _tools.RODict({
        "ID": "hostileListMax",
        "value": 54000435,
    }),
    "hostileAddSuccess": _tools.RODict({
        "ID": "hostileAddSuccess",
        "value": 54000436,
    })
})