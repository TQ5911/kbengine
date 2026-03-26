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
    "UIBagPanel": _tools.RODict({
        "function": "UIBagPanel",
        "type": "bag",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "ChangeTarget": _tools.RODict({
        "function": "ChangeTarget",
        "type": "changeTarget",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 1
    }),
    "UI_camera": _tools.RODict({
        "function": "UI_camera",
        "type": "UI_camera",
        "level": 0,
        "task": 86010003,
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
    "QuickSettings": _tools.RODict({
        "function": "QuickSettings",
        "type": "quickSettings",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "queueServer": _tools.RODict({
        "function": "queueServer",
        "type": "queueServer",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "photograph": _tools.RODict({
        "function": "photograph",
        "type": "photograph",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "shareBtn": _tools.RODict({
        "function": "shareBtn",
        "type": "shareBtn",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "shareSystem": _tools.RODict({
        "function": "shareSystem",
        "type": "shareSystem",
        "level": 0,
        "task": 0,
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
    "TenSign": _tools.RODict({
        "function": "TenSign",
        "type": "welfare_tenSign",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "Meridian": _tools.RODict({
        "function": "Meridian",
        "type": "UIPracticePanel",
        "level": 0,
        "task": 86010014,
        "day": 0,
        "switch": 0
    }),
    "Attention": _tools.RODict({
        "function": "Attention",
        "type": "welfare_attention",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "phoneBind": _tools.RODict({
        "function": "phoneBind",
        "type": "welfare_phoneBind",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "LevelReward": _tools.RODict({
        "function": "LevelReward",
        "type": "welfare_levelReward",
        "level": 0,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "Questionnaire": _tools.RODict({
        "function": "Questionnaire",
        "type": "questionnaire",
        "level": 15,
        "task": 86010003,
        "day": 0,
        "switch": 0
    }),
    "PcLoginReward": _tools.RODict({
        "function": "PcLoginReward",
        "type": "welfare_pcLogin",
        "level": 0,
        "task": 86010082,
        "day": 0,
        "switch": 0
    }),
    "UIActivitiesPanel": _tools.RODict({
        "function": "UIActivitiesPanel",
        "type": "welfare",
        "level": 0,
        "task": 86010082,
        "day": 0,
        "switch": 0
    }),
    "SevenSign": _tools.RODict({
        "function": "SevenSign",
        "type": "welfare_sevenSign",
        "level": 0,
        "task": 86010082,
        "day": 0,
        "switch": 0
    }),
    "UISkillSystemPanel": _tools.RODict({
        "function": "UISkillSystemPanel",
        "type": "skillUpgrade",
        "level": 0,
        "task": 86050075,
        "day": 0,
        "switch": 1
    }),
    "UIRewardTaskPanel": _tools.RODict({
        "function": "UIRewardTaskPanel",
        "type": "rewardTask",
        "level": 0,
        "task": 86010013,
        "day": 0,
        "switch": 0
    }),
    "Stronger": _tools.RODict({
        "function": "Stronger",
        "type": "stronger",
        "level": 0,
        "task": 86010013,
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
    "UIDrawPetPanel": _tools.RODict({
        "function": "UIDrawPetPanel",
        "type": "drawPet",
        "level": 0,
        "task": 86010038,
        "day": 0,
        "switch": 0
    }),
    "UIPetPanel": _tools.RODict({
        "function": "UIPetPanel",
        "type": "pet",
        "level": 0,
        "task": 86010038,
        "day": 0,
        "switch": 1
    }),
    "UIEquipTrainingPanel": _tools.RODict({
        "function": "UIEquipTrainingPanel",
        "type": "equip",
        "level": 0,
        "task": 86010096,
        "day": 0,
        "switch": 0
    }),
    "UIEquipMakePanel": _tools.RODict({
        "function": "UIEquipMakePanel",
        "type": "equip_make",
        "level": 0,
        "task": 86050003,
        "day": 0,
        "switch": 0
    }),
    "UIEquipUnbundlePanel": _tools.RODict({
        "function": "UIEquipUnbundlePanel",
        "type": "equip_unbundle",
        "level": 999,
        "task": 86050003,
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
    "UIWarehousePanel": _tools.RODict({
        "function": "UIWarehousePanel",
        "type": "warehouse",
        "level": 0,
        "task": 86060115,
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
    "UIAttributePanel": _tools.RODict({
        "function": "UIAttributePanel",
        "type": "myPage",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
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
    "Chat": _tools.RODict({
        "function": "Chat",
        "type": "chat",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "UIAchievementPanel": _tools.RODict({
        "function": "UIAchievementPanel",
        "type": "achievement",
        "level": 0,
        "task": 86060115,
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
        "type": "quickSettings",
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
    "DeathDrop": _tools.RODict({
        "function": "DeathDrop",
        "type": "deathDrop",
        "level": 0,
        "task": 86060115,
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
    "AutoCollect": _tools.RODict({
        "function": "AutoCollect",
        "type": "autoCollect",
        "level": 4,
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
    "MonthCard": _tools.RODict({
        "function": "MonthCard",
        "type": "monthCard",
        "level": 9,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "quickTips": _tools.RODict({
        "function": "quickTips",
        "type": "quickTips",
        "level": 9,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIPracticePanel": _tools.RODict({
        "function": "UIPracticePanel",
        "type": "UIPracticePanel",
        "level": 0,
        "task": 86010014,
        "day": 0,
        "switch": 1
    }),
    "UIEquipIntensifyPage": _tools.RODict({
        "function": "UIEquipIntensifyPage",
        "type": "equip_strengthen",
        "level": 0,
        "task": 86010096,
        "day": 0,
        "switch": 0
    }),
    "Guild": _tools.RODict({
        "function": "Guild",
        "type": "guild",
        "level": 0,
        "task": 86050035,
        "day": 0,
        "switch": 0
    }),
    "UIGuildPanel": _tools.RODict({
        "function": "UIGuildPanel",
        "type": "guild",
        "level": 0,
        "task": 86050035,
        "day": 0,
        "switch": 0
    }),
    "UIGuildLobbyPanel": _tools.RODict({
        "function": "UIGuildLobbyPanel",
        "type": "guild",
        "level": 0,
        "task": 86050035,
        "day": 0,
        "switch": 0
    }),
    "UITeamDunPanel": _tools.RODict({
        "function": "UITeamDunPanel",
        "type": "teamDungeon",
        "level": 0,
        "task": 86010068,
        "day": 0,
        "switch": 0
    }),
    "UISquarePanel": _tools.RODict({
        "function": "UISquarePanel",
        "type": "square",
        "level": 0,
        "task": 86010070,
        "day": 0,
        "switch": 0
    }),
    "UICollectionPanel": _tools.RODict({
        "function": "UICollectionPanel",
        "type": "collection",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UISynthesisSystemPanel": _tools.RODict({
        "function": "UISynthesisSystemPanel",
        "type": "synthesis",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIPropMakePanel": _tools.RODict({
        "function": "UIPropMakePanel",
        "type": "workshop",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "GuildBossChallenge": _tools.RODict({
        "function": "GuildBossChallenge",
        "type": "guildBossChallenge",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIBusinessPanel": _tools.RODict({
        "function": "UIBusinessPanel",
        "type": "business",
        "level": 0,
        "task": 86010069,
        "day": 0,
        "switch": 0
    }),
    "UIEquipClassPage": _tools.RODict({
        "function": "UIEquipClassPage",
        "type": "equip_class",
        "level": 0,
        "task": 86010020,
        "day": 0,
        "switch": 0
    }),
    "UIWonderLandPanel": _tools.RODict({
        "function": "UIWonderLandPanel",
        "type": "wonderLand",
        "level": 0,
        "task": 86010081,
        "day": 0,
        "switch": 0
    }),
    "UIEquipEnchantingPage": _tools.RODict({
        "function": "UIEquipEnchantingPage",
        "type": "equip_spirit",
        "level": 0,
        "task": 86010131,
        "day": 0,
        "switch": 0
    }),
    "UICrusadeSystemPanel": _tools.RODict({
        "function": "UICrusadeSystemPanel",
        "type": "raidDungeon",
        "level": 0,
        "task": 86010077,
        "day": 0,
        "switch": 0
    }),
    "UIEquipRunePage": _tools.RODict({
        "function": "UIEquipRunePage",
        "type": "equip_weaponGlyph",
        "level": 0,
        "task": 86010072,
        "day": 0,
        "switch": 0
    }),
    "UIEquipBlessPage": _tools.RODict({
        "function": "UIEquipBlessPage",
        "type": "equip_bless",
        "level": 0,
        "task": 86010149,
        "day": 0,
        "switch": 0
    }),
    "MineBattle": _tools.RODict({
        "function": "MineBattle",
        "type": "mineBattle",
        "level": 30,
        "task": 86010083,
        "day": 0,
        "switch": 0
    }),
    "UIMineBattleManagePanel": _tools.RODict({
        "function": "UIMineBattleManagePanel",
        "type": "mineBattle",
        "level": 30,
        "task": 86010083,
        "day": 0,
        "switch": 0
    }),
    "UIRoleAuthorizationPanel": _tools.RODict({
        "function": "UIRoleAuthorizationPanel",
        "type": "roleAuthorization",
        "level": 999,
        "task": 86060115,
        "day": 0,
        "switch": 0
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
        "task": 86060105,
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
    "xinyuanchengopentask": _tools.RODict({
        "function": "xinyuanchengopentask",
        "type": "mapTask",
        "level": 0,
        "task": 86010024,
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
        "level": 35,
        "task": 86010058,
        "day": 0,
        "switch": 0
    }),
    "jinglingcunopentask": _tools.RODict({
        "function": "jinglingcunopentask",
        "type": "mapTask",
        "level": 0,
        "task": 86010087,
        "day": 0,
        "switch": 0
    }),
    "jinglingbaodianopentask": _tools.RODict({
        "function": "jinglingbaodianopentask",
        "type": "mapTask",
        "level": 0,
        "task": 86010087,
        "day": 0,
        "switch": 0
    }),
    "shikuzoulangopentask": _tools.RODict({
        "function": "shikuzoulangopentask",
        "type": "mapTask",
        "level": 40,
        "task": 86010057,
        "day": 0,
        "switch": 0
    }),
    "xinyuanchenjiaoopentask": _tools.RODict({
        "function": "xinyuanchenjiaoopentask",
        "type": "mapTask",
        "level": 23,
        "task": 86010024,
        "day": 0,
        "switch": 0
    }),
    "zuke1Fopentask": _tools.RODict({
        "function": "zuke1Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 86010195,
        "day": 0,
        "switch": 0
    }),
    "zuke2Fopentask": _tools.RODict({
        "function": "zuke2Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 86010195,
        "day": 0,
        "switch": 0
    }),
    "zuke3Fopentask": _tools.RODict({
        "function": "zuke3Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 86010195,
        "day": 0,
        "switch": 0
    }),
    "zuke4Fopentask": _tools.RODict({
        "function": "zuke4Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 86010195,
        "day": 0,
        "switch": 0
    }),
    "zuke5Fopentask": _tools.RODict({
        "function": "zuke5Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 86010195,
        "day": 0,
        "switch": 0
    }),
    "zuke6Fopentask": _tools.RODict({
        "function": "zuke6Fopentask",
        "type": "mapTask",
        "level": 40,
        "task": 86010195,
        "day": 0,
        "switch": 0
    }),
    "yueguang1Fopentask": _tools.RODict({
        "function": "yueguang1Fopentask",
        "type": "mapTask",
        "level": 10,
        "task": 86010029,
        "day": 0,
        "switch": 0
    }),
    "yueguang2Fopentask": _tools.RODict({
        "function": "yueguang2Fopentask",
        "type": "mapTask",
        "level": 16,
        "task": 86010029,
        "day": 0,
        "switch": 0
    }),
    "yueguang3Fopentask": _tools.RODict({
        "function": "yueguang3Fopentask",
        "type": "mapTask",
        "level": 22,
        "task": 86010029,
        "day": 0,
        "switch": 0
    }),
    "yueguang4Fopentask": _tools.RODict({
        "function": "yueguang4Fopentask",
        "type": "mapTask",
        "level": 28,
        "task": 86010029,
        "day": 0,
        "switch": 0
    }),
    "yueguang5Fopentask": _tools.RODict({
        "function": "yueguang5Fopentask",
        "type": "mapTask",
        "level": 30,
        "task": 86010029,
        "day": 0,
        "switch": 0
    }),
    "wudu1Fopentask": _tools.RODict({
        "function": "wudu1Fopentask",
        "type": "mapTask",
        "level": 50,
        "task": 86010057,
        "day": 0,
        "switch": 0
    }),
    "wudu2Fopentask": _tools.RODict({
        "function": "wudu2Fopentask",
        "type": "mapTask",
        "level": 52,
        "task": 86010057,
        "day": 0,
        "switch": 0
    }),
    "wudu4Fopentask": _tools.RODict({
        "function": "wudu4Fopentask",
        "type": "mapTask",
        "level": 56,
        "task": 86010057,
        "day": 0,
        "switch": 0
    }),
    "UISettingsPanel": _tools.RODict({
        "function": "UISettingsPanel",
        "type": "settings",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIRedeemCodePanel": _tools.RODict({
        "function": "UIRedeemCodePanel",
        "type": "settings_giftKey",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIMainMenu": _tools.RODict({
        "function": "UIMainMenu",
        "type": "menu",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "HotGift": _tools.RODict({
        "function": "HotGift",
        "type": "pay_hotGift",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "HolidayGift": _tools.RODict({
        "function": "HolidayGift",
        "type": "pay_holidayGift",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "Rmb": _tools.RODict({
        "function": "Rmb",
        "type": "pay_rmb",
        "level": 999,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIGrowthGuidePanel": _tools.RODict({
        "function": "UIGrowthGuidePanel",
        "type": "stronger",
        "level": 0,
        "task": 86010013,
        "day": 0,
        "switch": 0
    }),
    "PKStateArea": _tools.RODict({
        "function": "PKStateArea",
        "type": "PKState",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 2
    }),
    "UISocialPanel": _tools.RODict({
        "function": "UISocialPanel",
        "type": "chat",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 1
    }),
    "Hotkey": _tools.RODict({
        "function": "Hotkey",
        "type": "settings_hotKey",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "MountBtn": _tools.RODict({
        "function": "MountBtn",
        "type": "appearance",
        "level": 0,
        "task": 86010027,
        "day": 0,
        "switch": 1
    }),
    "CardChangeBtn": _tools.RODict({
        "function": "CardChangeBtn",
        "type": "pet",
        "level": 0,
        "task": 86010037,
        "day": 0,
        "switch": 1
    }),
    "UIDeathPunishmentPanel": _tools.RODict({
        "function": "UIDeathPunishmentPanel",
        "type": "deathDrop",
        "level": 0,
        "task": 86060115,
        "day": 0,
        "switch": 0
    }),
    "UIMainLockPanel": _tools.RODict({
        "function": "UIMainLockPanel",
        "type": "mainLock",
        "level": 15,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "CurrencyExchange": _tools.RODict({
        "function": "CurrencyExchange",
        "type": "currencyExchange",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 1
    })
})


UIBagPanel = 0
ChangeTarget = 1
UI_camera = 2
UI_cards = 3
UI_hp = 4
UI_level = 5
UI_score = 6
QuickSettings = 7
queueServer = 8
photograph = 9
shareBtn = 10
shareSystem = 11
Enemy = 12
Duel = 13
TenSign = 14
Meridian = 15
Attention = 16
phoneBind = 17
LevelReward = 18
Questionnaire = 19
PcLoginReward = 20
UIActivitiesPanel = 21
SevenSign = 22
UISkillSystemPanel = 23
UIRewardTaskPanel = 24
Stronger = 25
UIAppearancePanel = 26
UIDrawPetPanel = 27
UIPetPanel = 28
UIEquipTrainingPanel = 29
UIEquipMakePanel = 30
UIEquipUnbundlePanel = 31
UITaskInfoPanel = 32
Team = 33
UIWarehousePanel = 34
ExitDun = 35
UIAttributePanel = 36
UIFriendPanel = 37
GrowthGuide = 38
Chat = 39
UIAchievementPanel = 40
Line = 41
UIMailPanel = 42
UIMapPanel = 43
UIPayStorePanel = 44
UIPKProtectPanel = 45
UIPortableSetPanel = 46
Raid = 47
UIRankPanel = 48
DeathDrop = 49
AutoCombat = 50
AutoCollect = 51
UIRedPacketPanel = 52
MonthCard = 53
quickTips = 54
UIPracticePanel = 55
UIEquipIntensifyPage = 56
Guild = 57
UIGuildPanel = 58
UIGuildLobbyPanel = 59
UITeamDunPanel = 60
UISquarePanel = 61
UICollectionPanel = 62
UISynthesisSystemPanel = 63
UIPropMakePanel = 64
GuildBossChallenge = 65
UIBusinessPanel = 66
UIEquipClassPage = 67
UIWonderLandPanel = 68
UIEquipEnchantingPage = 69
UICrusadeSystemPanel = 70
UIEquipRunePage = 71
UIEquipBlessPage = 72
MineBattle = 73
UIMineBattleManagePanel = 74
UIRoleAuthorizationPanel = 75
CityBattle = 76
UICityBattlePanel = 77
GeneralAttack = 78
Dodge = 79
Sprint = 80
Jump = 81
Fly = 82
MageSkill01 = 83
MageSkill02 = 84
MageSkill03 = 85
MageSkill04 = 86
MageSkill05 = 87
MageSkill06 = 88
MageSkill07 = 89
MageSkill08 = 90
MageSkill09 = 91
MageSkill10 = 92
MageSkill11 = 93
MageSkill12 = 94
MageSkillUlt = 95
TaoistSkill01 = 96
TaoistSkill02 = 97
TaoistSkill03 = 98
TaoistSkill04 = 99
TaoistSkill05 = 100
TaoistSkill06 = 101
TaoistSkill07 = 102
TaoistSkill08 = 103
TaoistSkill09 = 104
TaoistSkill10 = 105
TaoistSkill11 = 106
TaoistSkill12 = 107
TaoistSkillUlt = 108
WarriorSkill01 = 109
WarriorSkill02 = 110
WarriorSkill03 = 111
WarriorSkill04 = 112
WarriorSkill05 = 113
WarriorSkill06 = 114
WarriorSkill07 = 115
WarriorSkill08 = 116
WarriorSkill09 = 117
WarriorSkill10 = 118
WarriorSkill11 = 119
WarriorSkill12 = 120
WarriorSkillUlt = 121
xinyuanchengopentask = 122
tongxingguopentask = 123
feishayaosaiopentask = 124
jinglingcunopentask = 125
jinglingbaodianopentask = 126
shikuzoulangopentask = 127
xinyuanchenjiaoopentask = 128
zuke1Fopentask = 129
zuke2Fopentask = 130
zuke3Fopentask = 131
zuke4Fopentask = 132
zuke5Fopentask = 133
zuke6Fopentask = 134
yueguang1Fopentask = 135
yueguang2Fopentask = 136
yueguang3Fopentask = 137
yueguang4Fopentask = 138
yueguang5Fopentask = 139
wudu1Fopentask = 140
wudu2Fopentask = 141
wudu4Fopentask = 142
UISettingsPanel = 143
UIRedeemCodePanel = 144
UIMainMenu = 145
HotGift = 146
HolidayGift = 147
Rmb = 148
UIGrowthGuidePanel = 149
PKStateArea = 150
UISocialPanel = 151
Hotkey = 152
MountBtn = 153
CardChangeBtn = 154
UIDeathPunishmentPanel = 155
UIMainLockPanel = 156
CurrencyExchange = 157



funcDic = _tools.RODict({
    "UIBagPanel" : 0,
    "ChangeTarget" : 1,
    "UI_camera" : 2,
    "UI_cards" : 3,
    "UI_hp" : 4,
    "UI_level" : 5,
    "UI_score" : 6,
    "QuickSettings" : 7,
    "queueServer" : 8,
    "photograph" : 9,
    "shareBtn" : 10,
    "shareSystem" : 11,
    "Enemy" : 12,
    "Duel" : 13,
    "TenSign" : 14,
    "Meridian" : 15,
    "Attention" : 16,
    "phoneBind" : 17,
    "LevelReward" : 18,
    "Questionnaire" : 19,
    "PcLoginReward" : 20,
    "UIActivitiesPanel" : 21,
    "SevenSign" : 22,
    "UISkillSystemPanel" : 23,
    "UIRewardTaskPanel" : 24,
    "Stronger" : 25,
    "UIAppearancePanel" : 26,
    "UIDrawPetPanel" : 27,
    "UIPetPanel" : 28,
    "UIEquipTrainingPanel" : 29,
    "UIEquipMakePanel" : 30,
    "UIEquipUnbundlePanel" : 31,
    "UITaskInfoPanel" : 32,
    "Team" : 33,
    "UIWarehousePanel" : 34,
    "ExitDun" : 35,
    "UIAttributePanel" : 36,
    "UIFriendPanel" : 37,
    "GrowthGuide" : 38,
    "Chat" : 39,
    "UIAchievementPanel" : 40,
    "Line" : 41,
    "UIMailPanel" : 42,
    "UIMapPanel" : 43,
    "UIPayStorePanel" : 44,
    "UIPKProtectPanel" : 45,
    "UIPortableSetPanel" : 46,
    "Raid" : 47,
    "UIRankPanel" : 48,
    "DeathDrop" : 49,
    "AutoCombat" : 50,
    "AutoCollect" : 51,
    "UIRedPacketPanel" : 52,
    "MonthCard" : 53,
    "quickTips" : 54,
    "UIPracticePanel" : 55,
    "UIEquipIntensifyPage" : 56,
    "Guild" : 57,
    "UIGuildPanel" : 58,
    "UIGuildLobbyPanel" : 59,
    "UITeamDunPanel" : 60,
    "UISquarePanel" : 61,
    "UICollectionPanel" : 62,
    "UISynthesisSystemPanel" : 63,
    "UIPropMakePanel" : 64,
    "GuildBossChallenge" : 65,
    "UIBusinessPanel" : 66,
    "UIEquipClassPage" : 67,
    "UIWonderLandPanel" : 68,
    "UIEquipEnchantingPage" : 69,
    "UICrusadeSystemPanel" : 70,
    "UIEquipRunePage" : 71,
    "UIEquipBlessPage" : 72,
    "MineBattle" : 73,
    "UIMineBattleManagePanel" : 74,
    "UIRoleAuthorizationPanel" : 75,
    "CityBattle" : 76,
    "UICityBattlePanel" : 77,
    "GeneralAttack" : 78,
    "Dodge" : 79,
    "Sprint" : 80,
    "Jump" : 81,
    "Fly" : 82,
    "MageSkill01" : 83,
    "MageSkill02" : 84,
    "MageSkill03" : 85,
    "MageSkill04" : 86,
    "MageSkill05" : 87,
    "MageSkill06" : 88,
    "MageSkill07" : 89,
    "MageSkill08" : 90,
    "MageSkill09" : 91,
    "MageSkill10" : 92,
    "MageSkill11" : 93,
    "MageSkill12" : 94,
    "MageSkillUlt" : 95,
    "TaoistSkill01" : 96,
    "TaoistSkill02" : 97,
    "TaoistSkill03" : 98,
    "TaoistSkill04" : 99,
    "TaoistSkill05" : 100,
    "TaoistSkill06" : 101,
    "TaoistSkill07" : 102,
    "TaoistSkill08" : 103,
    "TaoistSkill09" : 104,
    "TaoistSkill10" : 105,
    "TaoistSkill11" : 106,
    "TaoistSkill12" : 107,
    "TaoistSkillUlt" : 108,
    "WarriorSkill01" : 109,
    "WarriorSkill02" : 110,
    "WarriorSkill03" : 111,
    "WarriorSkill04" : 112,
    "WarriorSkill05" : 113,
    "WarriorSkill06" : 114,
    "WarriorSkill07" : 115,
    "WarriorSkill08" : 116,
    "WarriorSkill09" : 117,
    "WarriorSkill10" : 118,
    "WarriorSkill11" : 119,
    "WarriorSkill12" : 120,
    "WarriorSkillUlt" : 121,
    "xinyuanchengopentask" : 122,
    "tongxingguopentask" : 123,
    "feishayaosaiopentask" : 124,
    "jinglingcunopentask" : 125,
    "jinglingbaodianopentask" : 126,
    "shikuzoulangopentask" : 127,
    "xinyuanchenjiaoopentask" : 128,
    "zuke1Fopentask" : 129,
    "zuke2Fopentask" : 130,
    "zuke3Fopentask" : 131,
    "zuke4Fopentask" : 132,
    "zuke5Fopentask" : 133,
    "zuke6Fopentask" : 134,
    "yueguang1Fopentask" : 135,
    "yueguang2Fopentask" : 136,
    "yueguang3Fopentask" : 137,
    "yueguang4Fopentask" : 138,
    "yueguang5Fopentask" : 139,
    "wudu1Fopentask" : 140,
    "wudu2Fopentask" : 141,
    "wudu4Fopentask" : 142,
    "UISettingsPanel" : 143,
    "UIRedeemCodePanel" : 144,
    "UIMainMenu" : 145,
    "HotGift" : 146,
    "HolidayGift" : 147,
    "Rmb" : 148,
    "UIGrowthGuidePanel" : 149,
    "PKStateArea" : 150,
    "UISocialPanel" : 151,
    "Hotkey" : 152,
    "MountBtn" : 153,
    "CardChangeBtn" : 154,
    "UIDeathPunishmentPanel" : 155,
    "UIMainLockPanel" : 156,
    "CurrencyExchange" : 157,
})
reverseFuncDic = _tools.RODict({
    0 : "UIBagPanel",
    1 : "ChangeTarget",
    2 : "UI_camera",
    3 : "UI_cards",
    4 : "UI_hp",
    5 : "UI_level",
    6 : "UI_score",
    7 : "QuickSettings",
    8 : "queueServer",
    9 : "photograph",
    10 : "shareBtn",
    11 : "shareSystem",
    12 : "Enemy",
    13 : "Duel",
    14 : "TenSign",
    15 : "Meridian",
    16 : "Attention",
    17 : "phoneBind",
    18 : "LevelReward",
    19 : "Questionnaire",
    20 : "PcLoginReward",
    21 : "UIActivitiesPanel",
    22 : "SevenSign",
    23 : "UISkillSystemPanel",
    24 : "UIRewardTaskPanel",
    25 : "Stronger",
    26 : "UIAppearancePanel",
    27 : "UIDrawPetPanel",
    28 : "UIPetPanel",
    29 : "UIEquipTrainingPanel",
    30 : "UIEquipMakePanel",
    31 : "UIEquipUnbundlePanel",
    32 : "UITaskInfoPanel",
    33 : "Team",
    34 : "UIWarehousePanel",
    35 : "ExitDun",
    36 : "UIAttributePanel",
    37 : "UIFriendPanel",
    38 : "GrowthGuide",
    39 : "Chat",
    40 : "UIAchievementPanel",
    41 : "Line",
    42 : "UIMailPanel",
    43 : "UIMapPanel",
    44 : "UIPayStorePanel",
    45 : "UIPKProtectPanel",
    46 : "UIPortableSetPanel",
    47 : "Raid",
    48 : "UIRankPanel",
    49 : "DeathDrop",
    50 : "AutoCombat",
    51 : "AutoCollect",
    52 : "UIRedPacketPanel",
    53 : "MonthCard",
    54 : "quickTips",
    55 : "UIPracticePanel",
    56 : "UIEquipIntensifyPage",
    57 : "Guild",
    58 : "UIGuildPanel",
    59 : "UIGuildLobbyPanel",
    60 : "UITeamDunPanel",
    61 : "UISquarePanel",
    62 : "UICollectionPanel",
    63 : "UISynthesisSystemPanel",
    64 : "UIPropMakePanel",
    65 : "GuildBossChallenge",
    66 : "UIBusinessPanel",
    67 : "UIEquipClassPage",
    68 : "UIWonderLandPanel",
    69 : "UIEquipEnchantingPage",
    70 : "UICrusadeSystemPanel",
    71 : "UIEquipRunePage",
    72 : "UIEquipBlessPage",
    73 : "MineBattle",
    74 : "UIMineBattleManagePanel",
    75 : "UIRoleAuthorizationPanel",
    76 : "CityBattle",
    77 : "UICityBattlePanel",
    78 : "GeneralAttack",
    79 : "Dodge",
    80 : "Sprint",
    81 : "Jump",
    82 : "Fly",
    83 : "MageSkill01",
    84 : "MageSkill02",
    85 : "MageSkill03",
    86 : "MageSkill04",
    87 : "MageSkill05",
    88 : "MageSkill06",
    89 : "MageSkill07",
    90 : "MageSkill08",
    91 : "MageSkill09",
    92 : "MageSkill10",
    93 : "MageSkill11",
    94 : "MageSkill12",
    95 : "MageSkillUlt",
    96 : "TaoistSkill01",
    97 : "TaoistSkill02",
    98 : "TaoistSkill03",
    99 : "TaoistSkill04",
    100 : "TaoistSkill05",
    101 : "TaoistSkill06",
    102 : "TaoistSkill07",
    103 : "TaoistSkill08",
    104 : "TaoistSkill09",
    105 : "TaoistSkill10",
    106 : "TaoistSkill11",
    107 : "TaoistSkill12",
    108 : "TaoistSkillUlt",
    109 : "WarriorSkill01",
    110 : "WarriorSkill02",
    111 : "WarriorSkill03",
    112 : "WarriorSkill04",
    113 : "WarriorSkill05",
    114 : "WarriorSkill06",
    115 : "WarriorSkill07",
    116 : "WarriorSkill08",
    117 : "WarriorSkill09",
    118 : "WarriorSkill10",
    119 : "WarriorSkill11",
    120 : "WarriorSkill12",
    121 : "WarriorSkillUlt",
    122 : "xinyuanchengopentask",
    123 : "tongxingguopentask",
    124 : "feishayaosaiopentask",
    125 : "jinglingcunopentask",
    126 : "jinglingbaodianopentask",
    127 : "shikuzoulangopentask",
    128 : "xinyuanchenjiaoopentask",
    129 : "zuke1Fopentask",
    130 : "zuke2Fopentask",
    131 : "zuke3Fopentask",
    132 : "zuke4Fopentask",
    133 : "zuke5Fopentask",
    134 : "zuke6Fopentask",
    135 : "yueguang1Fopentask",
    136 : "yueguang2Fopentask",
    137 : "yueguang3Fopentask",
    138 : "yueguang4Fopentask",
    139 : "yueguang5Fopentask",
    140 : "wudu1Fopentask",
    141 : "wudu2Fopentask",
    142 : "wudu4Fopentask",
    143 : "UISettingsPanel",
    144 : "UIRedeemCodePanel",
    145 : "UIMainMenu",
    146 : "HotGift",
    147 : "HolidayGift",
    148 : "Rmb",
    149 : "UIGrowthGuidePanel",
    150 : "PKStateArea",
    151 : "UISocialPanel",
    152 : "Hotkey",
    153 : "MountBtn",
    154 : "CardChangeBtn",
    155 : "UIDeathPunishmentPanel",
    156 : "UIMainLockPanel",
    157 : "CurrencyExchange",
})
levelDic = _tools.RODict({
    15 : _tools.ROList([
        19,
        89,
        102,
        115,
        156,
    ]),
    999 : _tools.ROList([
        31,
        75,
        76,
        77,
        148,
    ]),
    4 : _tools.ROList([
        50,
        51,
    ]),
    9 : _tools.ROList([
        52,
        53,
        54,
        87,
        100,
        113,
    ]),
    30 : _tools.ROList([
        73,
        74,
        129,
        130,
        131,
        132,
        133,
        139,
    ]),
    6 : _tools.ROList([
        86,
        99,
        112,
    ]),
    12 : _tools.ROList([
        88,
        101,
        114,
    ]),
    20 : _tools.ROList([
        90,
        103,
        116,
    ]),
    26 : _tools.ROList([
        91,
        104,
        117,
    ]),
    32 : _tools.ROList([
        92,
        105,
        118,
    ]),
    40 : _tools.ROList([
        93,
        106,
        119,
        127,
        134,
    ]),
    48 : _tools.ROList([
        94,
        107,
        120,
    ]),
    35 : _tools.ROList([
        124,
    ]),
    23 : _tools.ROList([
        128,
    ]),
    10 : _tools.ROList([
        135,
    ]),
    16 : _tools.ROList([
        136,
    ]),
    22 : _tools.ROList([
        137,
    ]),
    28 : _tools.ROList([
        138,
    ]),
    50 : _tools.ROList([
        140,
    ]),
    52 : _tools.ROList([
        141,
    ]),
    56 : _tools.ROList([
        142,
    ]),
})
taskDic = _tools.RODict({
    86010003 : _tools.ROList([
        1,
        2,
        9,
        14,
        16,
        17,
        18,
        19,
    ]),
    86060115 : _tools.ROList([
        7,
        33,
        34,
        35,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        51,
        52,
        53,
        54,
        75,
        82,
        146,
        147,
        148,
        150,
        151,
        152,
        155,
    ]),
    86010014 : _tools.ROList([
        15,
        55,
    ]),
    86010082 : _tools.ROList([
        20,
        21,
        22,
    ]),
    86050075 : _tools.ROList([
        23,
    ]),
    86010013 : _tools.ROList([
        24,
        25,
        149,
    ]),
    86010027 : _tools.ROList([
        26,
        153,
    ]),
    86010038 : _tools.ROList([
        27,
        28,
    ]),
    86010096 : _tools.ROList([
        29,
        56,
    ]),
    86050003 : _tools.ROList([
        30,
        31,
    ]),
    86060104 : _tools.ROList([
        32,
    ]),
    86050035 : _tools.ROList([
        57,
        58,
        59,
    ]),
    86010068 : _tools.ROList([
        60,
    ]),
    86010070 : _tools.ROList([
        61,
    ]),
    86010069 : _tools.ROList([
        66,
    ]),
    86010020 : _tools.ROList([
        67,
    ]),
    86010081 : _tools.ROList([
        68,
    ]),
    86010131 : _tools.ROList([
        69,
    ]),
    86010077 : _tools.ROList([
        70,
    ]),
    86010072 : _tools.ROList([
        71,
    ]),
    86010149 : _tools.ROList([
        72,
    ]),
    86010083 : _tools.ROList([
        73,
        74,
    ]),
    86060105 : _tools.ROList([
        80,
    ]),
    86060055 : _tools.ROList([
        83,
        96,
        109,
    ]),
    86060061 : _tools.ROList([
        84,
        97,
        110,
    ]),
    86060089 : _tools.ROList([
        85,
        98,
        111,
    ]),
    86060090 : _tools.ROList([
        95,
        108,
        121,
    ]),
    86010024 : _tools.ROList([
        122,
        128,
    ]),
    86010058 : _tools.ROList([
        124,
    ]),
    86010087 : _tools.ROList([
        125,
        126,
    ]),
    86010057 : _tools.ROList([
        127,
        140,
        141,
        142,
    ]),
    86010195 : _tools.ROList([
        129,
        130,
        131,
        132,
        133,
        134,
    ]),
    86010029 : _tools.ROList([
        135,
        136,
        137,
        138,
        139,
    ]),
    86010037 : _tools.ROList([
        154,
    ]),
})
dayDic = _tools.RODict({
})
maxBit = 157

typeToMain = {'UI_camera': 'UI', 'UI_cards': 'UI', 'UI_hp': 'UI', 'UI_level': 'UI', 'UI_score': 'UI', 'welfare_tenSign': 'welfare', 'welfare_attention': 'welfare', 'welfare_phoneBind': 'welfare', 'welfare_levelReward': 'welfare', 'welfare_pcLogin': 'welfare', 'welfare_sevenSign': 'welfare', 'equip_make': 'equip', 'equip_unbundle': 'equip', 'equip_strengthen': 'equip', 'equip_class': 'equip', 'equip_spirit': 'equip', 'equip_weaponGlyph': 'equip', 'equip_bless': 'equip', 'settings_giftKey': 'settings', 'pay_hotGift': 'pay', 'pay_holidayGift': 'pay', 'pay_rmb': 'pay', 'settings_hotKey': 'settings'}
