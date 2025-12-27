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
        "level": 4,
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
        "level": 999,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "UICityBattlePanel": _tools.RODict({
        "function": "UICityBattlePanel",
        "type": "cityBattle",
        "level": 999,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "MineBattle": _tools.RODict({
        "function": "MineBattle",
        "type": "mineBattle",
        "level": 30,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIMineBattleManagePanel": _tools.RODict({
        "function": "UIMineBattleManagePanel",
        "type": "mineBattle",
        "level": 30,
        "task": 0,
        "day": 0,
        "switch": 0
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
        "level": 9,
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
    "Fly": _tools.RODict({
        "function": "Fly",
        "type": "skill",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "MageSkill01": _tools.RODict({
        "function": "MageSkill01",
        "type": "skillMage",
        "level": 0,
        "task": 86060055,
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
        "task": 86060055,
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
        "task": 86060055,
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
    "UIPropMakePanel": _tools.RODict({
        "function": "UIPropMakePanel",
        "type": "workshop",
        "level": 19,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UITaskInfoPanel": _tools.RODict({
        "function": "UITaskInfoPanel",
        "type": "task",
        "level": 0,
        "task": 86060104,
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
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "SevenSign": _tools.RODict({
        "function": "SevenSign",
        "type": "welfare",
        "level": 0,
        "task": 86010003,
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
        "level": 90,
        "task": 86060115,
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
    }),
    "QuickSettings": _tools.RODict({
        "function": "QuickSettings",
        "type": "quickSettings",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "TenSign": _tools.RODict({
        "function": "TenSign",
        "type": "welfare",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "Meridian": _tools.RODict({
        "function": "Meridian",
        "type": "UIPracticePanel",
        "level": 0,
        "task": 86010005,
        "day": 0,
        "switch": 1
    }),
    "Attention": _tools.RODict({
        "function": "Attention",
        "type": "welfare",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "phoneBind": _tools.RODict({
        "function": "phoneBind",
        "type": "welfare",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "LevelReward": _tools.RODict({
        "function": "LevelReward",
        "type": "welfare",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "MonthCard": _tools.RODict({
        "function": "MonthCard",
        "type": "monthCard",
        "level": 9,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "Enemy": _tools.RODict({
        "function": "Enemy",
        "type": "enemy",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "Duel": _tools.RODict({
        "function": "Duel",
        "type": "duel",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "Questionnaire": _tools.RODict({
        "function": "Questionnaire",
        "type": "questionnaire",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "PcLoginReward": _tools.RODict({
        "function": "PcLoginReward",
        "type": "welfare",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "xinyuanchengopentask": _tools.RODict({
        "function": "xinyuanchengopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "tongxingguopentask": _tools.RODict({
        "function": "tongxingguopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "feishayaosaiopentask": _tools.RODict({
        "function": "feishayaosaiopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "jinglingcunopentask": _tools.RODict({
        "function": "jinglingcunopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "jinglingbaodianopentask": _tools.RODict({
        "function": "jinglingbaodianopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "shikuzoulangopentask": _tools.RODict({
        "function": "shikuzoulangopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "xinyuanchenjiaoopentask": _tools.RODict({
        "function": "xinyuanchenjiaoopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke1Fopentask": _tools.RODict({
        "function": "zuke1Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke2Fopentask": _tools.RODict({
        "function": "zuke2Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke3Fopentask": _tools.RODict({
        "function": "zuke3Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke4Fopentask": _tools.RODict({
        "function": "zuke4Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke5Fopentask": _tools.RODict({
        "function": "zuke5Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "zuke6Fopentask": _tools.RODict({
        "function": "zuke6Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "yueguang1Fopentask": _tools.RODict({
        "function": "yueguang1Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "yueguang2Fopentask": _tools.RODict({
        "function": "yueguang2Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "yueguang3Fopentask": _tools.RODict({
        "function": "yueguang3Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "yueguang4Fopentask": _tools.RODict({
        "function": "yueguang4Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "yueguang5Fopentask": _tools.RODict({
        "function": "yueguang5Fopentask",
        "type": "mapTask",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "GuildBossChallenge": _tools.RODict({
        "function": "GuildBossChallenge",
        "type": "guildBossChallenge",
        "level": 19,
        "task": 0,
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
MineBattle = 10
UIMineBattleManagePanel = 11
UICollectionPanel = 12
UICrusadeSystemPanel = 13
UIDrawPetPanel = 14
UIEquipMakePanel = 15
UIEquipTrainingPanel = 16
UIEquipEnchantingPanel = 17
ExitDun = 18
UIFriendPanel = 19
GrowthGuide = 20
Guild = 21
UIGuildPanel = 22
UIGuildLobbyPanel = 23
Line = 24
UIMailPanel = 25
UIMapPanel = 26
UIPayStorePanel = 27
UIPetPanel = 28
UIPKProtectPanel = 29
UIPortableSetPanel = 30
Raid = 31
UIRankPanel = 32
UIRedPacketPanel = 33
UIRewardTaskPanel = 34
GeneralAttack = 35
Dodge = 36
Sprint = 37
Jump = 38
Fly = 39
MageSkill01 = 40
MageSkill02 = 41
MageSkill03 = 42
MageSkill04 = 43
MageSkill05 = 44
MageSkill06 = 45
MageSkill07 = 46
MageSkill08 = 47
MageSkill09 = 48
MageSkill10 = 49
MageSkill11 = 50
MageSkill12 = 51
MageSkillUlt = 52
TaoistSkill01 = 53
TaoistSkill02 = 54
TaoistSkill03 = 55
TaoistSkill04 = 56
TaoistSkill05 = 57
TaoistSkill06 = 58
TaoistSkill07 = 59
TaoistSkill08 = 60
TaoistSkill09 = 61
TaoistSkill10 = 62
TaoistSkill11 = 63
TaoistSkill12 = 64
TaoistSkillUlt = 65
WarriorSkill01 = 66
WarriorSkill02 = 67
WarriorSkill03 = 68
WarriorSkill04 = 69
WarriorSkill05 = 70
WarriorSkill06 = 71
WarriorSkill07 = 72
WarriorSkill08 = 73
WarriorSkill09 = 74
WarriorSkill10 = 75
WarriorSkill11 = 76
WarriorSkill12 = 77
WarriorSkillUlt = 78
UISkillSystemPanel = 79
UISquarePanel = 80
UISynthesisSystemPanel = 81
UIPropMakePanel = 82
UITaskInfoPanel = 83
Team = 84
UITeamDunPanel = 85
UI_camera = 86
UI_cards = 87
UI_hp = 88
UI_level = 89
UI_score = 90
UIWarehousePanel = 91
UIActivitiesPanel = 92
SevenSign = 93
UIWonderLandPanel = 94
UIRoleAuthorizationPanel = 95
UIPracticePanel = 96
DeathDrop = 97
QuickSettings = 98
TenSign = 99
Meridian = 100
Attention = 101
phoneBind = 102
LevelReward = 103
MonthCard = 104
Enemy = 105
Duel = 106
Questionnaire = 107
PcLoginReward = 108
xinyuanchengopentask = 109
tongxingguopentask = 110
feishayaosaiopentask = 111
jinglingcunopentask = 112
jinglingbaodianopentask = 113
shikuzoulangopentask = 114
xinyuanchenjiaoopentask = 115
zuke1Fopentask = 116
zuke2Fopentask = 117
zuke3Fopentask = 118
zuke4Fopentask = 119
zuke5Fopentask = 120
zuke6Fopentask = 121
yueguang1Fopentask = 122
yueguang2Fopentask = 123
yueguang3Fopentask = 124
yueguang4Fopentask = 125
yueguang5Fopentask = 126
GuildBossChallenge = 127



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
    "MineBattle" : 10,
    "UIMineBattleManagePanel" : 11,
    "UICollectionPanel" : 12,
    "UICrusadeSystemPanel" : 13,
    "UIDrawPetPanel" : 14,
    "UIEquipMakePanel" : 15,
    "UIEquipTrainingPanel" : 16,
    "UIEquipEnchantingPanel" : 17,
    "ExitDun" : 18,
    "UIFriendPanel" : 19,
    "GrowthGuide" : 20,
    "Guild" : 21,
    "UIGuildPanel" : 22,
    "UIGuildLobbyPanel" : 23,
    "Line" : 24,
    "UIMailPanel" : 25,
    "UIMapPanel" : 26,
    "UIPayStorePanel" : 27,
    "UIPetPanel" : 28,
    "UIPKProtectPanel" : 29,
    "UIPortableSetPanel" : 30,
    "Raid" : 31,
    "UIRankPanel" : 32,
    "UIRedPacketPanel" : 33,
    "UIRewardTaskPanel" : 34,
    "GeneralAttack" : 35,
    "Dodge" : 36,
    "Sprint" : 37,
    "Jump" : 38,
    "Fly" : 39,
    "MageSkill01" : 40,
    "MageSkill02" : 41,
    "MageSkill03" : 42,
    "MageSkill04" : 43,
    "MageSkill05" : 44,
    "MageSkill06" : 45,
    "MageSkill07" : 46,
    "MageSkill08" : 47,
    "MageSkill09" : 48,
    "MageSkill10" : 49,
    "MageSkill11" : 50,
    "MageSkill12" : 51,
    "MageSkillUlt" : 52,
    "TaoistSkill01" : 53,
    "TaoistSkill02" : 54,
    "TaoistSkill03" : 55,
    "TaoistSkill04" : 56,
    "TaoistSkill05" : 57,
    "TaoistSkill06" : 58,
    "TaoistSkill07" : 59,
    "TaoistSkill08" : 60,
    "TaoistSkill09" : 61,
    "TaoistSkill10" : 62,
    "TaoistSkill11" : 63,
    "TaoistSkill12" : 64,
    "TaoistSkillUlt" : 65,
    "WarriorSkill01" : 66,
    "WarriorSkill02" : 67,
    "WarriorSkill03" : 68,
    "WarriorSkill04" : 69,
    "WarriorSkill05" : 70,
    "WarriorSkill06" : 71,
    "WarriorSkill07" : 72,
    "WarriorSkill08" : 73,
    "WarriorSkill09" : 74,
    "WarriorSkill10" : 75,
    "WarriorSkill11" : 76,
    "WarriorSkill12" : 77,
    "WarriorSkillUlt" : 78,
    "UISkillSystemPanel" : 79,
    "UISquarePanel" : 80,
    "UISynthesisSystemPanel" : 81,
    "UIPropMakePanel" : 82,
    "UITaskInfoPanel" : 83,
    "Team" : 84,
    "UITeamDunPanel" : 85,
    "UI_camera" : 86,
    "UI_cards" : 87,
    "UI_hp" : 88,
    "UI_level" : 89,
    "UI_score" : 90,
    "UIWarehousePanel" : 91,
    "UIActivitiesPanel" : 92,
    "SevenSign" : 93,
    "UIWonderLandPanel" : 94,
    "UIRoleAuthorizationPanel" : 95,
    "UIPracticePanel" : 96,
    "DeathDrop" : 97,
    "QuickSettings" : 98,
    "TenSign" : 99,
    "Meridian" : 100,
    "Attention" : 101,
    "phoneBind" : 102,
    "LevelReward" : 103,
    "MonthCard" : 104,
    "Enemy" : 105,
    "Duel" : 106,
    "Questionnaire" : 107,
    "PcLoginReward" : 108,
    "xinyuanchengopentask" : 109,
    "tongxingguopentask" : 110,
    "feishayaosaiopentask" : 111,
    "jinglingcunopentask" : 112,
    "jinglingbaodianopentask" : 113,
    "shikuzoulangopentask" : 114,
    "xinyuanchenjiaoopentask" : 115,
    "zuke1Fopentask" : 116,
    "zuke2Fopentask" : 117,
    "zuke3Fopentask" : 118,
    "zuke4Fopentask" : 119,
    "zuke5Fopentask" : 120,
    "zuke6Fopentask" : 121,
    "yueguang1Fopentask" : 122,
    "yueguang2Fopentask" : 123,
    "yueguang3Fopentask" : 124,
    "yueguang4Fopentask" : 125,
    "yueguang5Fopentask" : 126,
    "GuildBossChallenge" : 127,
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
    10 : "MineBattle",
    11 : "UIMineBattleManagePanel",
    12 : "UICollectionPanel",
    13 : "UICrusadeSystemPanel",
    14 : "UIDrawPetPanel",
    15 : "UIEquipMakePanel",
    16 : "UIEquipTrainingPanel",
    17 : "UIEquipEnchantingPanel",
    18 : "ExitDun",
    19 : "UIFriendPanel",
    20 : "GrowthGuide",
    21 : "Guild",
    22 : "UIGuildPanel",
    23 : "UIGuildLobbyPanel",
    24 : "Line",
    25 : "UIMailPanel",
    26 : "UIMapPanel",
    27 : "UIPayStorePanel",
    28 : "UIPetPanel",
    29 : "UIPKProtectPanel",
    30 : "UIPortableSetPanel",
    31 : "Raid",
    32 : "UIRankPanel",
    33 : "UIRedPacketPanel",
    34 : "UIRewardTaskPanel",
    35 : "GeneralAttack",
    36 : "Dodge",
    37 : "Sprint",
    38 : "Jump",
    39 : "Fly",
    40 : "MageSkill01",
    41 : "MageSkill02",
    42 : "MageSkill03",
    43 : "MageSkill04",
    44 : "MageSkill05",
    45 : "MageSkill06",
    46 : "MageSkill07",
    47 : "MageSkill08",
    48 : "MageSkill09",
    49 : "MageSkill10",
    50 : "MageSkill11",
    51 : "MageSkill12",
    52 : "MageSkillUlt",
    53 : "TaoistSkill01",
    54 : "TaoistSkill02",
    55 : "TaoistSkill03",
    56 : "TaoistSkill04",
    57 : "TaoistSkill05",
    58 : "TaoistSkill06",
    59 : "TaoistSkill07",
    60 : "TaoistSkill08",
    61 : "TaoistSkill09",
    62 : "TaoistSkill10",
    63 : "TaoistSkill11",
    64 : "TaoistSkill12",
    65 : "TaoistSkillUlt",
    66 : "WarriorSkill01",
    67 : "WarriorSkill02",
    68 : "WarriorSkill03",
    69 : "WarriorSkill04",
    70 : "WarriorSkill05",
    71 : "WarriorSkill06",
    72 : "WarriorSkill07",
    73 : "WarriorSkill08",
    74 : "WarriorSkill09",
    75 : "WarriorSkill10",
    76 : "WarriorSkill11",
    77 : "WarriorSkill12",
    78 : "WarriorSkillUlt",
    79 : "UISkillSystemPanel",
    80 : "UISquarePanel",
    81 : "UISynthesisSystemPanel",
    82 : "UIPropMakePanel",
    83 : "UITaskInfoPanel",
    84 : "Team",
    85 : "UITeamDunPanel",
    86 : "UI_camera",
    87 : "UI_cards",
    88 : "UI_hp",
    89 : "UI_level",
    90 : "UI_score",
    91 : "UIWarehousePanel",
    92 : "UIActivitiesPanel",
    93 : "SevenSign",
    94 : "UIWonderLandPanel",
    95 : "UIRoleAuthorizationPanel",
    96 : "UIPracticePanel",
    97 : "DeathDrop",
    98 : "QuickSettings",
    99 : "TenSign",
    100 : "Meridian",
    101 : "Attention",
    102 : "phoneBind",
    103 : "LevelReward",
    104 : "MonthCard",
    105 : "Enemy",
    106 : "Duel",
    107 : "Questionnaire",
    108 : "PcLoginReward",
    109 : "xinyuanchengopentask",
    110 : "tongxingguopentask",
    111 : "feishayaosaiopentask",
    112 : "jinglingcunopentask",
    113 : "jinglingbaodianopentask",
    114 : "shikuzoulangopentask",
    115 : "xinyuanchenjiaoopentask",
    116 : "zuke1Fopentask",
    117 : "zuke2Fopentask",
    118 : "zuke3Fopentask",
    119 : "zuke4Fopentask",
    120 : "zuke5Fopentask",
    121 : "zuke6Fopentask",
    122 : "yueguang1Fopentask",
    123 : "yueguang2Fopentask",
    124 : "yueguang3Fopentask",
    125 : "yueguang4Fopentask",
    126 : "yueguang5Fopentask",
    127 : "GuildBossChallenge",
})
levelDic = _tools.RODict({
    4 : _tools.ROList([
        3,
    ]),
    999 : _tools.ROList([
        8,
        9,
    ]),
    30 : _tools.ROList([
        10,
        11,
        120,
    ]),
    18 : _tools.ROList([
        12,
    ]),
    26 : _tools.ROList([
        13,
        48,
        61,
        74,
    ]),
    28 : _tools.ROList([
        17,
    ]),
    19 : _tools.ROList([
        21,
        22,
        23,
        81,
        82,
        127,
    ]),
    9 : _tools.ROList([
        33,
        44,
        57,
        70,
        104,
    ]),
    6 : _tools.ROList([
        43,
        56,
        69,
    ]),
    12 : _tools.ROList([
        45,
        58,
        71,
    ]),
    15 : _tools.ROList([
        46,
        59,
        72,
    ]),
    20 : _tools.ROList([
        47,
        60,
        73,
    ]),
    32 : _tools.ROList([
        49,
        62,
        75,
    ]),
    40 : _tools.ROList([
        50,
        63,
        76,
    ]),
    48 : _tools.ROList([
        51,
        64,
        77,
    ]),
    27 : _tools.ROList([
        94,
    ]),
    90 : _tools.ROList([
        95,
    ]),
    10 : _tools.ROList([
        96,
    ]),
})
taskDic = _tools.RODict({
    86060115 : _tools.ROList([
        0,
        7,
        18,
        19,
        20,
        24,
        25,
        26,
        27,
        29,
        30,
        31,
        32,
        33,
        39,
        84,
        91,
        95,
        97,
        104,
    ]),
    86010027 : _tools.ROList([
        1,
    ]),
    86010050 : _tools.ROList([
        5,
    ]),
    86010037 : _tools.ROList([
        14,
        28,
    ]),
    86050006 : _tools.ROList([
        15,
        16,
    ]),
    86010018 : _tools.ROList([
        34,
    ]),
    86060055 : _tools.ROList([
        40,
        53,
        66,
    ]),
    86060061 : _tools.ROList([
        41,
        54,
        67,
    ]),
    86060089 : _tools.ROList([
        42,
        55,
        68,
    ]),
    86060090 : _tools.ROList([
        52,
        65,
        78,
    ]),
    86010016 : _tools.ROList([
        79,
    ]),
    86010070 : _tools.ROList([
        80,
    ]),
    86060104 : _tools.ROList([
        83,
    ]),
    86010068 : _tools.ROList([
        85,
    ]),
    86010003 : _tools.ROList([
        92,
        93,
        99,
        101,
        102,
        103,
        107,
        108,
    ]),
    86010005 : _tools.ROList([
        96,
        100,
    ]),
})
dayDic = _tools.RODict({
})
maxBit = 127