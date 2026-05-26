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
    "ResourceRecovery": _tools.RODict({
        "function": "ResourceRecovery",
        "type": "welfare_resourceRecovery",
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
        "level": 0,
        "task": 86060146,
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
        "level": 999,
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
        "level": 0,
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
    "UIAbyssPanel": _tools.RODict({
        "function": "UIAbyssPanel",
        "type": "abyss",
        "level": 50,
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
        "level": 0,
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
        "task": 0,
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
    }),
    "worldLevel": _tools.RODict({
        "function": "worldLevel",
        "type": "worldLevel",
        "level": 20,
        "task": 0,
        "day": 1,
        "switch": 1
    }),
    "UIActivityNotice": _tools.RODict({
        "function": "UIActivityNotice",
        "type": "activityNotice",
        "level": 30,
        "task": 0,
        "day": 0,
        "switch": 1
    }),
    "UIWorldBoss": _tools.RODict({
        "function": "UIWorldBoss",
        "type": "worldBoss",
        "level": 30,
        "task": 0,
        "day": 0,
        "switch": 0
    }),
    "UIEquipSoul": _tools.RODict({
        "function": "UIEquipSoul",
        "type": "equip_soul",
        "level": 0,
        "task": 0,
        "day": 0,
        "switch": 0
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
ResourceRecovery = 21
UIActivitiesPanel = 22
SevenSign = 23
UISkillSystemPanel = 24
UIRewardTaskPanel = 25
Stronger = 26
UIAppearancePanel = 27
UIDrawPetPanel = 28
UIPetPanel = 29
UIEquipTrainingPanel = 30
UIEquipMakePanel = 31
UIEquipUnbundlePanel = 32
UITaskInfoPanel = 33
Team = 34
UIWarehousePanel = 35
ExitDun = 36
UIAttributePanel = 37
UIFriendPanel = 38
GrowthGuide = 39
Chat = 40
UIAchievementPanel = 41
Line = 42
UIMailPanel = 43
UIMapPanel = 44
UIPayStorePanel = 45
UIPKProtectPanel = 46
UIPortableSetPanel = 47
Raid = 48
UIRankPanel = 49
DeathDrop = 50
AutoCombat = 51
AutoCollect = 52
UIRedPacketPanel = 53
MonthCard = 54
quickTips = 55
UIPracticePanel = 56
UIEquipIntensifyPage = 57
Guild = 58
UIGuildPanel = 59
UIGuildLobbyPanel = 60
UITeamDunPanel = 61
UISquarePanel = 62
UICollectionPanel = 63
UISynthesisSystemPanel = 64
UIPropMakePanel = 65
GuildBossChallenge = 66
UIBusinessPanel = 67
UIEquipClassPage = 68
UIWonderLandPanel = 69
UIEquipEnchantingPage = 70
UICrusadeSystemPanel = 71
UIEquipRunePage = 72
UIEquipBlessPage = 73
MineBattle = 74
UIMineBattleManagePanel = 75
UIRoleAuthorizationPanel = 76
CityBattle = 77
UICityBattlePanel = 78
UIAbyssPanel = 79
GeneralAttack = 80
Dodge = 81
Sprint = 82
Jump = 83
Fly = 84
MageSkill01 = 85
MageSkill02 = 86
MageSkill03 = 87
MageSkill04 = 88
MageSkill05 = 89
MageSkill06 = 90
MageSkill07 = 91
MageSkill08 = 92
MageSkill09 = 93
MageSkill10 = 94
MageSkill11 = 95
MageSkill12 = 96
MageSkillUlt = 97
TaoistSkill01 = 98
TaoistSkill02 = 99
TaoistSkill03 = 100
TaoistSkill04 = 101
TaoistSkill05 = 102
TaoistSkill06 = 103
TaoistSkill07 = 104
TaoistSkill08 = 105
TaoistSkill09 = 106
TaoistSkill10 = 107
TaoistSkill11 = 108
TaoistSkill12 = 109
TaoistSkillUlt = 110
WarriorSkill01 = 111
WarriorSkill02 = 112
WarriorSkill03 = 113
WarriorSkill04 = 114
WarriorSkill05 = 115
WarriorSkill06 = 116
WarriorSkill07 = 117
WarriorSkill08 = 118
WarriorSkill09 = 119
WarriorSkill10 = 120
WarriorSkill11 = 121
WarriorSkill12 = 122
WarriorSkillUlt = 123
xinyuanchengopentask = 124
tongxingguopentask = 125
feishayaosaiopentask = 126
jinglingcunopentask = 127
jinglingbaodianopentask = 128
shikuzoulangopentask = 129
xinyuanchenjiaoopentask = 130
zuke1Fopentask = 131
zuke2Fopentask = 132
zuke3Fopentask = 133
zuke4Fopentask = 134
zuke5Fopentask = 135
zuke6Fopentask = 136
yueguang1Fopentask = 137
yueguang2Fopentask = 138
yueguang3Fopentask = 139
yueguang4Fopentask = 140
yueguang5Fopentask = 141
wudu1Fopentask = 142
wudu2Fopentask = 143
wudu4Fopentask = 144
UISettingsPanel = 145
UIRedeemCodePanel = 146
UIMainMenu = 147
HotGift = 148
HolidayGift = 149
Rmb = 150
UIGrowthGuidePanel = 151
PKStateArea = 152
UISocialPanel = 153
Hotkey = 154
MountBtn = 155
CardChangeBtn = 156
UIDeathPunishmentPanel = 157
UIMainLockPanel = 158
CurrencyExchange = 159
worldLevel = 160
UIActivityNotice = 161
UIWorldBoss = 162
UIEquipSoul = 163



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
    "ResourceRecovery" : 21,
    "UIActivitiesPanel" : 22,
    "SevenSign" : 23,
    "UISkillSystemPanel" : 24,
    "UIRewardTaskPanel" : 25,
    "Stronger" : 26,
    "UIAppearancePanel" : 27,
    "UIDrawPetPanel" : 28,
    "UIPetPanel" : 29,
    "UIEquipTrainingPanel" : 30,
    "UIEquipMakePanel" : 31,
    "UIEquipUnbundlePanel" : 32,
    "UITaskInfoPanel" : 33,
    "Team" : 34,
    "UIWarehousePanel" : 35,
    "ExitDun" : 36,
    "UIAttributePanel" : 37,
    "UIFriendPanel" : 38,
    "GrowthGuide" : 39,
    "Chat" : 40,
    "UIAchievementPanel" : 41,
    "Line" : 42,
    "UIMailPanel" : 43,
    "UIMapPanel" : 44,
    "UIPayStorePanel" : 45,
    "UIPKProtectPanel" : 46,
    "UIPortableSetPanel" : 47,
    "Raid" : 48,
    "UIRankPanel" : 49,
    "DeathDrop" : 50,
    "AutoCombat" : 51,
    "AutoCollect" : 52,
    "UIRedPacketPanel" : 53,
    "MonthCard" : 54,
    "quickTips" : 55,
    "UIPracticePanel" : 56,
    "UIEquipIntensifyPage" : 57,
    "Guild" : 58,
    "UIGuildPanel" : 59,
    "UIGuildLobbyPanel" : 60,
    "UITeamDunPanel" : 61,
    "UISquarePanel" : 62,
    "UICollectionPanel" : 63,
    "UISynthesisSystemPanel" : 64,
    "UIPropMakePanel" : 65,
    "GuildBossChallenge" : 66,
    "UIBusinessPanel" : 67,
    "UIEquipClassPage" : 68,
    "UIWonderLandPanel" : 69,
    "UIEquipEnchantingPage" : 70,
    "UICrusadeSystemPanel" : 71,
    "UIEquipRunePage" : 72,
    "UIEquipBlessPage" : 73,
    "MineBattle" : 74,
    "UIMineBattleManagePanel" : 75,
    "UIRoleAuthorizationPanel" : 76,
    "CityBattle" : 77,
    "UICityBattlePanel" : 78,
    "UIAbyssPanel" : 79,
    "GeneralAttack" : 80,
    "Dodge" : 81,
    "Sprint" : 82,
    "Jump" : 83,
    "Fly" : 84,
    "MageSkill01" : 85,
    "MageSkill02" : 86,
    "MageSkill03" : 87,
    "MageSkill04" : 88,
    "MageSkill05" : 89,
    "MageSkill06" : 90,
    "MageSkill07" : 91,
    "MageSkill08" : 92,
    "MageSkill09" : 93,
    "MageSkill10" : 94,
    "MageSkill11" : 95,
    "MageSkill12" : 96,
    "MageSkillUlt" : 97,
    "TaoistSkill01" : 98,
    "TaoistSkill02" : 99,
    "TaoistSkill03" : 100,
    "TaoistSkill04" : 101,
    "TaoistSkill05" : 102,
    "TaoistSkill06" : 103,
    "TaoistSkill07" : 104,
    "TaoistSkill08" : 105,
    "TaoistSkill09" : 106,
    "TaoistSkill10" : 107,
    "TaoistSkill11" : 108,
    "TaoistSkill12" : 109,
    "TaoistSkillUlt" : 110,
    "WarriorSkill01" : 111,
    "WarriorSkill02" : 112,
    "WarriorSkill03" : 113,
    "WarriorSkill04" : 114,
    "WarriorSkill05" : 115,
    "WarriorSkill06" : 116,
    "WarriorSkill07" : 117,
    "WarriorSkill08" : 118,
    "WarriorSkill09" : 119,
    "WarriorSkill10" : 120,
    "WarriorSkill11" : 121,
    "WarriorSkill12" : 122,
    "WarriorSkillUlt" : 123,
    "xinyuanchengopentask" : 124,
    "tongxingguopentask" : 125,
    "feishayaosaiopentask" : 126,
    "jinglingcunopentask" : 127,
    "jinglingbaodianopentask" : 128,
    "shikuzoulangopentask" : 129,
    "xinyuanchenjiaoopentask" : 130,
    "zuke1Fopentask" : 131,
    "zuke2Fopentask" : 132,
    "zuke3Fopentask" : 133,
    "zuke4Fopentask" : 134,
    "zuke5Fopentask" : 135,
    "zuke6Fopentask" : 136,
    "yueguang1Fopentask" : 137,
    "yueguang2Fopentask" : 138,
    "yueguang3Fopentask" : 139,
    "yueguang4Fopentask" : 140,
    "yueguang5Fopentask" : 141,
    "wudu1Fopentask" : 142,
    "wudu2Fopentask" : 143,
    "wudu4Fopentask" : 144,
    "UISettingsPanel" : 145,
    "UIRedeemCodePanel" : 146,
    "UIMainMenu" : 147,
    "HotGift" : 148,
    "HolidayGift" : 149,
    "Rmb" : 150,
    "UIGrowthGuidePanel" : 151,
    "PKStateArea" : 152,
    "UISocialPanel" : 153,
    "Hotkey" : 154,
    "MountBtn" : 155,
    "CardChangeBtn" : 156,
    "UIDeathPunishmentPanel" : 157,
    "UIMainLockPanel" : 158,
    "CurrencyExchange" : 159,
    "worldLevel" : 160,
    "UIActivityNotice" : 161,
    "UIWorldBoss" : 162,
    "UIEquipSoul" : 163,
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
    21 : "ResourceRecovery",
    22 : "UIActivitiesPanel",
    23 : "SevenSign",
    24 : "UISkillSystemPanel",
    25 : "UIRewardTaskPanel",
    26 : "Stronger",
    27 : "UIAppearancePanel",
    28 : "UIDrawPetPanel",
    29 : "UIPetPanel",
    30 : "UIEquipTrainingPanel",
    31 : "UIEquipMakePanel",
    32 : "UIEquipUnbundlePanel",
    33 : "UITaskInfoPanel",
    34 : "Team",
    35 : "UIWarehousePanel",
    36 : "ExitDun",
    37 : "UIAttributePanel",
    38 : "UIFriendPanel",
    39 : "GrowthGuide",
    40 : "Chat",
    41 : "UIAchievementPanel",
    42 : "Line",
    43 : "UIMailPanel",
    44 : "UIMapPanel",
    45 : "UIPayStorePanel",
    46 : "UIPKProtectPanel",
    47 : "UIPortableSetPanel",
    48 : "Raid",
    49 : "UIRankPanel",
    50 : "DeathDrop",
    51 : "AutoCombat",
    52 : "AutoCollect",
    53 : "UIRedPacketPanel",
    54 : "MonthCard",
    55 : "quickTips",
    56 : "UIPracticePanel",
    57 : "UIEquipIntensifyPage",
    58 : "Guild",
    59 : "UIGuildPanel",
    60 : "UIGuildLobbyPanel",
    61 : "UITeamDunPanel",
    62 : "UISquarePanel",
    63 : "UICollectionPanel",
    64 : "UISynthesisSystemPanel",
    65 : "UIPropMakePanel",
    66 : "GuildBossChallenge",
    67 : "UIBusinessPanel",
    68 : "UIEquipClassPage",
    69 : "UIWonderLandPanel",
    70 : "UIEquipEnchantingPage",
    71 : "UICrusadeSystemPanel",
    72 : "UIEquipRunePage",
    73 : "UIEquipBlessPage",
    74 : "MineBattle",
    75 : "UIMineBattleManagePanel",
    76 : "UIRoleAuthorizationPanel",
    77 : "CityBattle",
    78 : "UICityBattlePanel",
    79 : "UIAbyssPanel",
    80 : "GeneralAttack",
    81 : "Dodge",
    82 : "Sprint",
    83 : "Jump",
    84 : "Fly",
    85 : "MageSkill01",
    86 : "MageSkill02",
    87 : "MageSkill03",
    88 : "MageSkill04",
    89 : "MageSkill05",
    90 : "MageSkill06",
    91 : "MageSkill07",
    92 : "MageSkill08",
    93 : "MageSkill09",
    94 : "MageSkill10",
    95 : "MageSkill11",
    96 : "MageSkill12",
    97 : "MageSkillUlt",
    98 : "TaoistSkill01",
    99 : "TaoistSkill02",
    100 : "TaoistSkill03",
    101 : "TaoistSkill04",
    102 : "TaoistSkill05",
    103 : "TaoistSkill06",
    104 : "TaoistSkill07",
    105 : "TaoistSkill08",
    106 : "TaoistSkill09",
    107 : "TaoistSkill10",
    108 : "TaoistSkill11",
    109 : "TaoistSkill12",
    110 : "TaoistSkillUlt",
    111 : "WarriorSkill01",
    112 : "WarriorSkill02",
    113 : "WarriorSkill03",
    114 : "WarriorSkill04",
    115 : "WarriorSkill05",
    116 : "WarriorSkill06",
    117 : "WarriorSkill07",
    118 : "WarriorSkill08",
    119 : "WarriorSkill09",
    120 : "WarriorSkill10",
    121 : "WarriorSkill11",
    122 : "WarriorSkill12",
    123 : "WarriorSkillUlt",
    124 : "xinyuanchengopentask",
    125 : "tongxingguopentask",
    126 : "feishayaosaiopentask",
    127 : "jinglingcunopentask",
    128 : "jinglingbaodianopentask",
    129 : "shikuzoulangopentask",
    130 : "xinyuanchenjiaoopentask",
    131 : "zuke1Fopentask",
    132 : "zuke2Fopentask",
    133 : "zuke3Fopentask",
    134 : "zuke4Fopentask",
    135 : "zuke5Fopentask",
    136 : "zuke6Fopentask",
    137 : "yueguang1Fopentask",
    138 : "yueguang2Fopentask",
    139 : "yueguang3Fopentask",
    140 : "yueguang4Fopentask",
    141 : "yueguang5Fopentask",
    142 : "wudu1Fopentask",
    143 : "wudu2Fopentask",
    144 : "wudu4Fopentask",
    145 : "UISettingsPanel",
    146 : "UIRedeemCodePanel",
    147 : "UIMainMenu",
    148 : "HotGift",
    149 : "HolidayGift",
    150 : "Rmb",
    151 : "UIGrowthGuidePanel",
    152 : "PKStateArea",
    153 : "UISocialPanel",
    154 : "Hotkey",
    155 : "MountBtn",
    156 : "CardChangeBtn",
    157 : "UIDeathPunishmentPanel",
    158 : "UIMainLockPanel",
    159 : "CurrencyExchange",
    160 : "worldLevel",
    161 : "UIActivityNotice",
    162 : "UIWorldBoss",
    163 : "UIEquipSoul",
})
levelDic = _tools.RODict({
    15 : _tools.ROList([
        19,
        91,
        104,
        117,
        158,
    ]),
    999 : _tools.ROList([
        32,
        54,
        77,
        78,
    ]),
    4 : _tools.ROList([
        52,
    ]),
    9 : _tools.ROList([
        53,
        55,
        89,
        102,
        115,
    ]),
    30 : _tools.ROList([
        74,
        75,
        131,
        132,
        133,
        134,
        135,
        141,
        161,
        162,
    ]),
    50 : _tools.ROList([
        79,
        142,
    ]),
    6 : _tools.ROList([
        88,
        101,
        114,
    ]),
    12 : _tools.ROList([
        90,
        103,
        116,
    ]),
    20 : _tools.ROList([
        92,
        105,
        118,
        160,
    ]),
    26 : _tools.ROList([
        93,
        106,
        119,
    ]),
    32 : _tools.ROList([
        94,
        107,
        120,
    ]),
    40 : _tools.ROList([
        95,
        108,
        121,
        129,
        136,
    ]),
    48 : _tools.ROList([
        96,
        109,
        122,
    ]),
    35 : _tools.ROList([
        126,
    ]),
    23 : _tools.ROList([
        130,
    ]),
    10 : _tools.ROList([
        137,
    ]),
    16 : _tools.ROList([
        138,
    ]),
    22 : _tools.ROList([
        139,
    ]),
    28 : _tools.ROList([
        140,
    ]),
    52 : _tools.ROList([
        143,
    ]),
    56 : _tools.ROList([
        144,
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
        34,
        35,
        36,
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
        50,
        52,
        53,
        54,
        55,
        76,
        84,
        148,
        149,
        150,
        152,
        153,
        157,
    ]),
    86010014 : _tools.ROList([
        15,
        56,
    ]),
    86010082 : _tools.ROList([
        20,
        21,
        22,
        23,
    ]),
    86050075 : _tools.ROList([
        24,
    ]),
    86010013 : _tools.ROList([
        25,
        26,
        151,
    ]),
    86010027 : _tools.ROList([
        27,
        155,
    ]),
    86010038 : _tools.ROList([
        28,
        29,
    ]),
    86010096 : _tools.ROList([
        30,
        57,
    ]),
    86050003 : _tools.ROList([
        31,
        32,
    ]),
    86060104 : _tools.ROList([
        33,
    ]),
    86060146 : _tools.ROList([
        51,
    ]),
    86050035 : _tools.ROList([
        58,
        59,
        60,
    ]),
    86010068 : _tools.ROList([
        61,
    ]),
    86010070 : _tools.ROList([
        62,
    ]),
    86010069 : _tools.ROList([
        67,
    ]),
    86010020 : _tools.ROList([
        68,
    ]),
    86010081 : _tools.ROList([
        69,
    ]),
    86010131 : _tools.ROList([
        70,
    ]),
    86010077 : _tools.ROList([
        71,
    ]),
    86010072 : _tools.ROList([
        72,
    ]),
    86010149 : _tools.ROList([
        73,
    ]),
    86010083 : _tools.ROList([
        74,
        75,
    ]),
    86060105 : _tools.ROList([
        82,
    ]),
    86060055 : _tools.ROList([
        85,
        98,
        111,
    ]),
    86060061 : _tools.ROList([
        86,
        99,
        112,
    ]),
    86060089 : _tools.ROList([
        87,
        100,
        113,
    ]),
    86060090 : _tools.ROList([
        97,
        110,
        123,
    ]),
    86010024 : _tools.ROList([
        124,
        130,
    ]),
    86010058 : _tools.ROList([
        126,
    ]),
    86010087 : _tools.ROList([
        127,
        128,
    ]),
    86010057 : _tools.ROList([
        129,
        142,
        143,
        144,
    ]),
    86010195 : _tools.ROList([
        131,
        132,
        133,
        134,
        135,
        136,
    ]),
    86010029 : _tools.ROList([
        137,
        138,
        139,
        140,
        141,
    ]),
    86010037 : _tools.ROList([
        156,
    ]),
})
dayDic = _tools.RODict({
    1 : _tools.ROList([
        160,
    ]),
})
maxBit = 163

typeToMain = {'UI_camera': 'UI', 'UI_cards': 'UI', 'UI_hp': 'UI', 'UI_level': 'UI', 'UI_score': 'UI', 'welfare_tenSign': 'welfare', 'welfare_attention': 'welfare', 'welfare_phoneBind': 'welfare', 'welfare_levelReward': 'welfare', 'welfare_pcLogin': 'welfare', 'welfare_resourceRecovery': 'welfare', 'welfare_sevenSign': 'welfare', 'equip_make': 'equip', 'equip_unbundle': 'equip', 'equip_strengthen': 'equip', 'equip_class': 'equip', 'equip_spirit': 'equip', 'equip_weaponGlyph': 'equip', 'equip_bless': 'equip', 'settings_giftKey': 'settings', 'pay_hotGift': 'pay', 'pay_holidayGift': 'pay', 'pay_rmb': 'pay', 'settings_hotKey': 'settings', 'equip_soul': 'equip'}
