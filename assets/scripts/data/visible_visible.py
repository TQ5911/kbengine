# coding: utf-8

# NOTE: This file is AUTO GENERATE by excel export script, please NOT MODIFIED
#       file data manually.
# ------------------------------------------------------------------
# Copyright QianHui.INC 2023-2023
# ------------------------------------------------------------------
# SHEET NAME: visible/visible
import gamedatatools as _tools
# useful import
import collections
import random
import math
import re
import crontab

datas = _tools.RODict({ 
    "_": _tools.RODict({
        "function": "_",
        "type": "_",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "x": _tools.RODict({
        "function": "x",
        "type": "_",
        "level": 999,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIAchievementPanel": _tools.RODict({
        "function": "UIAchievementPanel",
        "type": "achievement",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIAppearancePanel": _tools.RODict({
        "function": "UIAppearancePanel",
        "type": "appearance",
        "level": 0,
        "task": 86010027,
        "day": 0,
        "switch": 1
    }),
    "AutoCollect": _tools.RODict({
        "function": "AutoCollect",
        "type": "autoCollect",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "AutoCombat": _tools.RODict({
        "function": "AutoCombat",
        "type": "autoCombat",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIBagPanel": _tools.RODict({
        "function": "UIBagPanel",
        "type": "bag",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "UIBusinessPanel": _tools.RODict({
        "function": "UIBusinessPanel",
        "type": "business",
        "level": 0,
        "task": 86010050,
        "day": 0,
        "switch": 0
    }),
    "ChangeTarget": _tools.RODict({
        "function": "ChangeTarget",
        "type": "changeTarget",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "Chat": _tools.RODict({
        "function": "Chat",
        "type": "chat",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "CityBattle": _tools.RODict({
        "function": "CityBattle",
        "type": "cityBattle",
        "level": 43,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "UICityBattlePanel": _tools.RODict({
        "function": "UICityBattlePanel",
        "type": "cityBattle",
        "level": 43,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "UICollectionPanel": _tools.RODict({
        "function": "UICollectionPanel",
        "type": "collection",
        "level": 18,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UICrusadeSystemPanel": _tools.RODict({
        "function": "UICrusadeSystemPanel",
        "type": "crusade",
        "level": 26,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIDrawPetPanel": _tools.RODict({
        "function": "UIDrawPetPanel",
        "type": "drawPet",
        "level": 0,
        "task": 86010037,
        "day": 0,
        "switch": 0
    }),
    "UIEquipMakePanel": _tools.RODict({
        "function": "UIEquipMakePanel",
        "type": "equip",
        "level": 0,
        "task": 86050006,
        "day": 0,
        "switch": 0
    }),
    "UIEquipTrainingPanel": _tools.RODict({
        "function": "UIEquipTrainingPanel",
        "type": "equip",
        "level": 0,
        "task": 86050006,
        "day": 0,
        "switch": 0
    }),
    "UIEquipEnchantingPanel": _tools.RODict({
        "function": "UIEquipEnchantingPanel",
        "type": "equip",
        "level": 28,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "ExitDun": _tools.RODict({
        "function": "ExitDun",
        "type": "exitDun",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIFriendPanel": _tools.RODict({
        "function": "UIFriendPanel",
        "type": "friend",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "GrowthGuide": _tools.RODict({
        "function": "GrowthGuide",
        "type": "growth",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "Guild": _tools.RODict({
        "function": "Guild",
        "type": "guild",
        "level": 19,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIGuildPanel": _tools.RODict({
        "function": "UIGuildPanel",
        "type": "guild",
        "level": 19,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIGuildLobbyPanel": _tools.RODict({
        "function": "UIGuildLobbyPanel",
        "type": "guild",
        "level": 19,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "Line": _tools.RODict({
        "function": "Line",
        "type": "line",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIMailPanel": _tools.RODict({
        "function": "UIMailPanel",
        "type": "mail",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIMapPanel": _tools.RODict({
        "function": "UIMapPanel",
        "type": "map",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "UIPayStorePanel": _tools.RODict({
        "function": "UIPayStorePanel",
        "type": "pay",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIPetPanel": _tools.RODict({
        "function": "UIPetPanel",
        "type": "pet",
        "level": 0,
        "task": 86010037,
        "day": 0,
        "switch": 1
    }),
    "UIPKProtectPanel": _tools.RODict({
        "function": "UIPKProtectPanel",
        "type": "pkProtect",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIPortableSetPanel": _tools.RODict({
        "function": "UIPortableSetPanel",
        "type": "quickItem",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "Raid": _tools.RODict({
        "function": "Raid",
        "type": "raid",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 2
    }),
    "UIRankPanel": _tools.RODict({
        "function": "UIRankPanel",
        "type": "rank",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIRedPacketPanel": _tools.RODict({
        "function": "UIRedPacketPanel",
        "type": "redPacket",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIRewardTaskPanel": _tools.RODict({
        "function": "UIRewardTaskPanel",
        "type": "rewardTask",
        "level": 0,
        "task": 86010018,
        "day": 0,
        "switch": 0
    }),
    "GeneralAttack": _tools.RODict({
        "function": "GeneralAttack",
        "type": "skill",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "Dodge": _tools.RODict({
        "function": "Dodge",
        "type": "skill",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "Sprint": _tools.RODict({
        "function": "Sprint",
        "type": "skill",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "Jump": _tools.RODict({
        "function": "Jump",
        "type": "skill",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill01": _tools.RODict({
        "function": "MageSkill01",
        "type": "skillMage",
        "level": 0,
        "task": 86060056,
        "day": 0,
        "switch": 1
    }),
    "MageSkill02": _tools.RODict({
        "function": "MageSkill02",
        "type": "skillMage",
        "level": 0,
        "task": 86060061,
        "day": 0,
        "switch": 1
    }),
    "MageSkill03": _tools.RODict({
        "function": "MageSkill03",
        "type": "skillMage",
        "level": 0,
        "task": 86060089,
        "day": 0,
        "switch": 1
    }),
    "MageSkill04": _tools.RODict({
        "function": "MageSkill04",
        "type": "skillMage",
        "level": 6,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill05": _tools.RODict({
        "function": "MageSkill05",
        "type": "skillMage",
        "level": 9,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill06": _tools.RODict({
        "function": "MageSkill06",
        "type": "skillMage",
        "level": 12,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill07": _tools.RODict({
        "function": "MageSkill07",
        "type": "skillMage",
        "level": 15,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill08": _tools.RODict({
        "function": "MageSkill08",
        "type": "skillMage",
        "level": 20,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill09": _tools.RODict({
        "function": "MageSkill09",
        "type": "skillMage",
        "level": 26,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill10": _tools.RODict({
        "function": "MageSkill10",
        "type": "skillMage",
        "level": 32,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill11": _tools.RODict({
        "function": "MageSkill11",
        "type": "skillMage",
        "level": 40,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkill12": _tools.RODict({
        "function": "MageSkill12",
        "type": "skillMage",
        "level": 48,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MageSkillUlt": _tools.RODict({
        "function": "MageSkillUlt",
        "type": "skillMage",
        "level": 0,
        "task": 86060090,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill01": _tools.RODict({
        "function": "TaoistSkill01",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060056,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill02": _tools.RODict({
        "function": "TaoistSkill02",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060061,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill03": _tools.RODict({
        "function": "TaoistSkill03",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060089,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill04": _tools.RODict({
        "function": "TaoistSkill04",
        "type": "skillTaoist",
        "level": 6,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill05": _tools.RODict({
        "function": "TaoistSkill05",
        "type": "skillTaoist",
        "level": 9,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill06": _tools.RODict({
        "function": "TaoistSkill06",
        "type": "skillTaoist",
        "level": 12,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill07": _tools.RODict({
        "function": "TaoistSkill07",
        "type": "skillTaoist",
        "level": 15,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill08": _tools.RODict({
        "function": "TaoistSkill08",
        "type": "skillTaoist",
        "level": 20,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill09": _tools.RODict({
        "function": "TaoistSkill09",
        "type": "skillTaoist",
        "level": 26,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill10": _tools.RODict({
        "function": "TaoistSkill10",
        "type": "skillTaoist",
        "level": 32,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill11": _tools.RODict({
        "function": "TaoistSkill11",
        "type": "skillTaoist",
        "level": 40,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkill12": _tools.RODict({
        "function": "TaoistSkill12",
        "type": "skillTaoist",
        "level": 48,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "TaoistSkillUlt": _tools.RODict({
        "function": "TaoistSkillUlt",
        "type": "skillTaoist",
        "level": 0,
        "task": 86060090,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill01": _tools.RODict({
        "function": "WarriorSkill01",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060056,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill02": _tools.RODict({
        "function": "WarriorSkill02",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060061,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill03": _tools.RODict({
        "function": "WarriorSkill03",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060089,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill04": _tools.RODict({
        "function": "WarriorSkill04",
        "type": "skillWarrior",
        "level": 6,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill05": _tools.RODict({
        "function": "WarriorSkill05",
        "type": "skillWarrior",
        "level": 9,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill06": _tools.RODict({
        "function": "WarriorSkill06",
        "type": "skillWarrior",
        "level": 12,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill07": _tools.RODict({
        "function": "WarriorSkill07",
        "type": "skillWarrior",
        "level": 15,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill08": _tools.RODict({
        "function": "WarriorSkill08",
        "type": "skillWarrior",
        "level": 20,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill09": _tools.RODict({
        "function": "WarriorSkill09",
        "type": "skillWarrior",
        "level": 26,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill10": _tools.RODict({
        "function": "WarriorSkill10",
        "type": "skillWarrior",
        "level": 32,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill11": _tools.RODict({
        "function": "WarriorSkill11",
        "type": "skillWarrior",
        "level": 40,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkill12": _tools.RODict({
        "function": "WarriorSkill12",
        "type": "skillWarrior",
        "level": 48,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "WarriorSkillUlt": _tools.RODict({
        "function": "WarriorSkillUlt",
        "type": "skillWarrior",
        "level": 0,
        "task": 86060090,
        "day": 0,
        "switch": 1
    }),
    "UISkillSystemPanel": _tools.RODict({
        "function": "UISkillSystemPanel",
        "type": "skillUpgrade",
        "level": 0,
        "task": 86010016,
        "day": 0,
        "switch": 1
    }),
    "UISquarePanel": _tools.RODict({
        "function": "UISquarePanel",
        "type": "square",
        "level": 0,
        "task": 86010070,
        "day": 0,
        "switch": 0
    }),
    "UISynthesisSystemPanel": _tools.RODict({
        "function": "UISynthesisSystemPanel",
        "type": "synthesis",
        "level": 19,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UITaskInfoPanel": _tools.RODict({
        "function": "UITaskInfoPanel",
        "type": "task",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 2
    }),
    "Team": _tools.RODict({
        "function": "Team",
        "type": "team",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 2
    }),
    "UITeamDunPanel": _tools.RODict({
        "function": "UITeamDunPanel",
        "type": "teamDungeon",
        "level": 0,
        "task": 86010068,
        "day": 0,
        "switch": 0
    }),
    "UI_camera": _tools.RODict({
        "function": "UI_camera",
        "type": "UI_camera",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 2
    }),
    "UI_cards": _tools.RODict({
        "function": "UI_cards",
        "type": "UI_cards",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 2
    }),
    "UI_hp": _tools.RODict({
        "function": "UI_hp",
        "type": "UI_hp",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 2
    }),
    "UI_level": _tools.RODict({
        "function": "UI_level",
        "type": "UI_level",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 2
    }),
    "UI_score": _tools.RODict({
        "function": "UI_score",
        "type": "UI_score",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 2
    }),
    "UIWarehousePanel": _tools.RODict({
        "function": "UIWarehousePanel",
        "type": "warehouse",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIActivitiesPanel": _tools.RODict({
        "function": "UIActivitiesPanel",
        "type": "welfare",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "SevenSign": _tools.RODict({
        "function": "SevenSign",
        "type": "welfare",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIWonderLandPanel": _tools.RODict({
        "function": "UIWonderLandPanel",
        "type": "wonderLand",
        "level": 27,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIRoleAuthorizationPanel": _tools.RODict({
        "function": "UIRoleAuthorizationPanel",
        "type": "roleAuthorization",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "xinyuanchengopentask": _tools.RODict({
        "function": "xinyuanchengopentask",
        "type": "mapTask",
        "level": 0,
        "task": 86010024,
        "day": 0,
        "switch": 0
    }),
    "UIPracticePanel": _tools.RODict({
        "function": "UIPracticePanel",
        "type": "UIPracticePanel",
        "level": 10,
        "task": 86010005,
        "day": 0,
        "switch": 1
    }),
    "DeathDrop": _tools.RODict({
        "function": "DeathDrop",
        "type": "deathDrop",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    })
})


UIAchievementPanel = 0
UIAppearancePanel = 1
AutoCollect = 2
AutoCombat = 3
UIBagPanel = 4
UIBusinessPanel = 5
ChangeTarget = 6
Chat = 7
CityBattle = 8
UICityBattlePanel = 9
UICollectionPanel = 10
UICrusadeSystemPanel = 11
UIDrawPetPanel = 12
UIEquipMakePanel = 13
UIEquipTrainingPanel = 14
UIEquipEnchantingPanel = 15
ExitDun = 16
UIFriendPanel = 17
GrowthGuide = 18
Guild = 19
UIGuildPanel = 20
UIGuildLobbyPanel = 21
Line = 22
UIMailPanel = 23
UIMapPanel = 24
UIPayStorePanel = 25
UIPetPanel = 26
UIPKProtectPanel = 27
UIPortableSetPanel = 28
Raid = 29
UIRankPanel = 30
UIRedPacketPanel = 31
UIRewardTaskPanel = 32
GeneralAttack = 33
Dodge = 34
Sprint = 35
Jump = 36
MageSkill01 = 37
MageSkill02 = 38
MageSkill03 = 39
MageSkill04 = 40
MageSkill05 = 41
MageSkill06 = 42
MageSkill07 = 43
MageSkill08 = 44
MageSkill09 = 45
MageSkill10 = 46
MageSkill11 = 47
MageSkill12 = 48
MageSkillUlt = 49
TaoistSkill01 = 50
TaoistSkill02 = 51
TaoistSkill03 = 52
TaoistSkill04 = 53
TaoistSkill05 = 54
TaoistSkill06 = 55
TaoistSkill07 = 56
TaoistSkill08 = 57
TaoistSkill09 = 58
TaoistSkill10 = 59
TaoistSkill11 = 60
TaoistSkill12 = 61
TaoistSkillUlt = 62
WarriorSkill01 = 63
WarriorSkill02 = 64
WarriorSkill03 = 65
WarriorSkill04 = 66
WarriorSkill05 = 67
WarriorSkill06 = 68
WarriorSkill07 = 69
WarriorSkill08 = 70
WarriorSkill09 = 71
WarriorSkill10 = 72
WarriorSkill11 = 73
WarriorSkill12 = 74
WarriorSkillUlt = 75
UISkillSystemPanel = 76
UISquarePanel = 77
UISynthesisSystemPanel = 78
UITaskInfoPanel = 79
Team = 80
UITeamDunPanel = 81
UI_camera = 82
UI_cards = 83
UI_hp = 84
UI_level = 85
UI_score = 86
UIWarehousePanel = 87
UIActivitiesPanel = 88
SevenSign = 89
UIWonderLandPanel = 90
UIRoleAuthorizationPanel = 91
xinyuanchengopentask = 92
UIPracticePanel = 93
DeathDrop = 94



funcDic = _tools.RODict({
    "UIAchievementPanel" : 0,
    "UIAppearancePanel" : 1,
    "AutoCollect" : 2,
    "AutoCombat" : 3,
    "UIBagPanel" : 4,
    "UIBusinessPanel" : 5,
    "ChangeTarget" : 6,
    "Chat" : 7,
    "CityBattle" : 8,
    "UICityBattlePanel" : 9,
    "UICollectionPanel" : 10,
    "UICrusadeSystemPanel" : 11,
    "UIDrawPetPanel" : 12,
    "UIEquipMakePanel" : 13,
    "UIEquipTrainingPanel" : 14,
    "UIEquipEnchantingPanel" : 15,
    "ExitDun" : 16,
    "UIFriendPanel" : 17,
    "GrowthGuide" : 18,
    "Guild" : 19,
    "UIGuildPanel" : 20,
    "UIGuildLobbyPanel" : 21,
    "Line" : 22,
    "UIMailPanel" : 23,
    "UIMapPanel" : 24,
    "UIPayStorePanel" : 25,
    "UIPetPanel" : 26,
    "UIPKProtectPanel" : 27,
    "UIPortableSetPanel" : 28,
    "Raid" : 29,
    "UIRankPanel" : 30,
    "UIRedPacketPanel" : 31,
    "UIRewardTaskPanel" : 32,
    "GeneralAttack" : 33,
    "Dodge" : 34,
    "Sprint" : 35,
    "Jump" : 36,
    "MageSkill01" : 37,
    "MageSkill02" : 38,
    "MageSkill03" : 39,
    "MageSkill04" : 40,
    "MageSkill05" : 41,
    "MageSkill06" : 42,
    "MageSkill07" : 43,
    "MageSkill08" : 44,
    "MageSkill09" : 45,
    "MageSkill10" : 46,
    "MageSkill11" : 47,
    "MageSkill12" : 48,
    "MageSkillUlt" : 49,
    "TaoistSkill01" : 50,
    "TaoistSkill02" : 51,
    "TaoistSkill03" : 52,
    "TaoistSkill04" : 53,
    "TaoistSkill05" : 54,
    "TaoistSkill06" : 55,
    "TaoistSkill07" : 56,
    "TaoistSkill08" : 57,
    "TaoistSkill09" : 58,
    "TaoistSkill10" : 59,
    "TaoistSkill11" : 60,
    "TaoistSkill12" : 61,
    "TaoistSkillUlt" : 62,
    "WarriorSkill01" : 63,
    "WarriorSkill02" : 64,
    "WarriorSkill03" : 65,
    "WarriorSkill04" : 66,
    "WarriorSkill05" : 67,
    "WarriorSkill06" : 68,
    "WarriorSkill07" : 69,
    "WarriorSkill08" : 70,
    "WarriorSkill09" : 71,
    "WarriorSkill10" : 72,
    "WarriorSkill11" : 73,
    "WarriorSkill12" : 74,
    "WarriorSkillUlt" : 75,
    "UISkillSystemPanel" : 76,
    "UISquarePanel" : 77,
    "UISynthesisSystemPanel" : 78,
    "UITaskInfoPanel" : 79,
    "Team" : 80,
    "UITeamDunPanel" : 81,
    "UI_camera" : 82,
    "UI_cards" : 83,
    "UI_hp" : 84,
    "UI_level" : 85,
    "UI_score" : 86,
    "UIWarehousePanel" : 87,
    "UIActivitiesPanel" : 88,
    "SevenSign" : 89,
    "UIWonderLandPanel" : 90,
    "UIRoleAuthorizationPanel" : 91,
    "xinyuanchengopentask" : 92,
    "UIPracticePanel" : 93,
    "DeathDrop" : 94,
})
reverseFuncDic = _tools.RODict({
    0 : "UIAchievementPanel",
    1 : "UIAppearancePanel",
    2 : "AutoCollect",
    3 : "AutoCombat",
    4 : "UIBagPanel",
    5 : "UIBusinessPanel",
    6 : "ChangeTarget",
    7 : "Chat",
    8 : "CityBattle",
    9 : "UICityBattlePanel",
    10 : "UICollectionPanel",
    11 : "UICrusadeSystemPanel",
    12 : "UIDrawPetPanel",
    13 : "UIEquipMakePanel",
    14 : "UIEquipTrainingPanel",
    15 : "UIEquipEnchantingPanel",
    16 : "ExitDun",
    17 : "UIFriendPanel",
    18 : "GrowthGuide",
    19 : "Guild",
    20 : "UIGuildPanel",
    21 : "UIGuildLobbyPanel",
    22 : "Line",
    23 : "UIMailPanel",
    24 : "UIMapPanel",
    25 : "UIPayStorePanel",
    26 : "UIPetPanel",
    27 : "UIPKProtectPanel",
    28 : "UIPortableSetPanel",
    29 : "Raid",
    30 : "UIRankPanel",
    31 : "UIRedPacketPanel",
    32 : "UIRewardTaskPanel",
    33 : "GeneralAttack",
    34 : "Dodge",
    35 : "Sprint",
    36 : "Jump",
    37 : "MageSkill01",
    38 : "MageSkill02",
    39 : "MageSkill03",
    40 : "MageSkill04",
    41 : "MageSkill05",
    42 : "MageSkill06",
    43 : "MageSkill07",
    44 : "MageSkill08",
    45 : "MageSkill09",
    46 : "MageSkill10",
    47 : "MageSkill11",
    48 : "MageSkill12",
    49 : "MageSkillUlt",
    50 : "TaoistSkill01",
    51 : "TaoistSkill02",
    52 : "TaoistSkill03",
    53 : "TaoistSkill04",
    54 : "TaoistSkill05",
    55 : "TaoistSkill06",
    56 : "TaoistSkill07",
    57 : "TaoistSkill08",
    58 : "TaoistSkill09",
    59 : "TaoistSkill10",
    60 : "TaoistSkill11",
    61 : "TaoistSkill12",
    62 : "TaoistSkillUlt",
    63 : "WarriorSkill01",
    64 : "WarriorSkill02",
    65 : "WarriorSkill03",
    66 : "WarriorSkill04",
    67 : "WarriorSkill05",
    68 : "WarriorSkill06",
    69 : "WarriorSkill07",
    70 : "WarriorSkill08",
    71 : "WarriorSkill09",
    72 : "WarriorSkill10",
    73 : "WarriorSkill11",
    74 : "WarriorSkill12",
    75 : "WarriorSkillUlt",
    76 : "UISkillSystemPanel",
    77 : "UISquarePanel",
    78 : "UISynthesisSystemPanel",
    79 : "UITaskInfoPanel",
    80 : "Team",
    81 : "UITeamDunPanel",
    82 : "UI_camera",
    83 : "UI_cards",
    84 : "UI_hp",
    85 : "UI_level",
    86 : "UI_score",
    87 : "UIWarehousePanel",
    88 : "UIActivitiesPanel",
    89 : "SevenSign",
    90 : "UIWonderLandPanel",
    91 : "UIRoleAuthorizationPanel",
    92 : "xinyuanchengopentask",
    93 : "UIPracticePanel",
    94 : "DeathDrop",
})
levelDic = _tools.RODict({
    43 : _tools.ROList([
        8,
        9,
    ]),
    18 : _tools.ROList([
        10,
    ]),
    26 : _tools.ROList([
        11,
        45,
        58,
        71,
    ]),
    28 : _tools.ROList([
        15,
    ]),
    19 : _tools.ROList([
        19,
        20,
        21,
        78,
    ]),
    6 : _tools.ROList([
        40,
        53,
        66,
    ]),
    9 : _tools.ROList([
        41,
        54,
        67,
    ]),
    12 : _tools.ROList([
        42,
        55,
        68,
    ]),
    15 : _tools.ROList([
        43,
        56,
        69,
    ]),
    20 : _tools.ROList([
        44,
        57,
        70,
    ]),
    32 : _tools.ROList([
        46,
        59,
        72,
    ]),
    40 : _tools.ROList([
        47,
        60,
        73,
    ]),
    48 : _tools.ROList([
        48,
        61,
        74,
    ]),
    27 : _tools.ROList([
        90,
    ]),
    10 : _tools.ROList([
        93,
    ]),
})
taskDic = _tools.RODict({
    86060115 : _tools.ROList([
        0,
        7,
        16,
        17,
        18,
        22,
        23,
        24,
        25,
        27,
        28,
        29,
        30,
        31,
        80,
        87,
        88,
        89,
        91,
        94,
    ]),
    86010027 : _tools.ROList([
        1,
    ]),
    86010050 : _tools.ROList([
        5,
    ]),
    86010037 : _tools.ROList([
        12,
        26,
    ]),
    86050006 : _tools.ROList([
        13,
        14,
    ]),
    86010018 : _tools.ROList([
        32,
    ]),
    86060056 : _tools.ROList([
        37,
        50,
        63,
    ]),
    86060061 : _tools.ROList([
        38,
        51,
        64,
    ]),
    86060089 : _tools.ROList([
        39,
        52,
        65,
    ]),
    86060090 : _tools.ROList([
        49,
        62,
        75,
    ]),
    86010016 : _tools.ROList([
        76,
    ]),
    86010070 : _tools.ROList([
        77,
    ]),
    86010068 : _tools.ROList([
        81,
    ]),
    86010024 : _tools.ROList([
        92,
    ]),
    86010005 : _tools.ROList([
        93,
    ]),
})
dayDic = _tools.RODict({
})
maxBit = 94