namespace KBEngine
{
	using UnityEngine;
	using System;
	using System.Collections;
	using System.Collections.Generic;

	public class EntityCommon : EntityCommonProperty
	{
		public virtual void aiChatToPlayer(UInt32 arg1, UInt32 arg2) {} //Monster Summon Npc 
		public virtual void notifyCastingSkill(UInt32 arg1, double arg2) {} //Avatar Monster Summon Npc Creation 
		public virtual void onAddAureole(CLIENT_AUREOLE_VAL arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onAddAureoleFromOthers(CLIENT_AUREOLE_VAL arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onAddBuff(CLIENT_BUFF_VAL arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onAddPassiveSkill(UInt32 arg1, UInt32 arg2) {} //Avatar Monster Summon Npc Creation 
		public virtual void onAddSkill(UInt32 arg1, UInt32 arg2, Byte arg3, double arg4, float arg5, Byte arg6) {} //Avatar Monster Summon Npc Creation 
		public virtual void onAddStateRet(Int32 arg1, Int32 arg2, Int32 arg3, Int32 arg4) {} //Avatar Monster Summon Npc Creation 
		public virtual void onBornAction() {} //Monster Npc 
		public virtual void onBreakCastingSkill(Int32 arg1, UInt32 arg2, Int32 arg3) {} //Avatar Monster Summon Npc Creation 
		public virtual void onBreakChannelingSkill(Int32 arg1, UInt32 arg2, Int32 arg3) {} //Avatar Monster Summon Npc Creation 
		public virtual void onDead(Int32 arg1) {} //Avatar Monster Summon Npc 
		public virtual void onDropRuneIds(List<float> arg1, Int32 arg2, List<Int32> arg3) {} //Avatar Monster Summon Npc Creation 
		public virtual void onFlashSkillZed(Byte arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onGameConfigChanged(List<UInt16> arg1, List<string> arg2) {} //Account Avatar 
		public virtual void onGameConfigChangedByName(List<string> arg1, List<string> arg2) {} //Account Avatar 
		public virtual void onGetAureoleInfo(Int32 arg1, CLIENT_AUREOLES arg2) {} //Avatar Monster Summon Npc Creation 
		public virtual void onGetBuffInfo(Int32 arg1, CLIENT_BUFFS arg2) {} //Avatar Monster Summon Npc Creation 
		public virtual void onMessage(Int32 arg1, List<string> arg2) {} //Account Avatar Monster Summon Npc Creation 
		public virtual void onMultiAtkStage(Byte arg1, UInt32 arg2, Int32 arg3, List<float> arg4, List<Int32> arg5) {} //Avatar Monster Summon Npc Creation 
		public virtual void onOthersSkillDamage(Int32 arg1, List<Int32> arg2) {} //Avatar Monster Summon Npc Creation 
		public virtual void onRemoveAureole(Int32 arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onRemoveAureoleFromOthers(Int32 arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onRemoveBuff(Int32 arg1, List<UInt64> arg2) {} //Avatar Monster Summon Npc Creation 
		public virtual void onRemoveRune(UInt32 arg1, Int32 arg2) {} //Avatar Monster Summon Npc Creation 
		public virtual void onServerUseSkill(UInt32 arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onSetAddSkillCd(UInt32 arg1, float arg2, double arg3, Byte arg4, double arg5, SByte arg6, SByte arg7) {} //Avatar Monster Summon Npc Creation 
		public virtual void onShooterSkillCanUse(UInt32 arg1, double arg2, Byte arg3) {} //Avatar Monster Summon Npc Creation 
		public virtual void onSkillDamage(SKILL_DAMAGE_INFO arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onSkillTeleport(UInt32 arg1, Vector3 arg2) {} //Avatar Monster Summon Npc Creation 
		public virtual void onUpdateAureoles(CLIENT_AUREOLES arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onUpdateAureolesFromOthers(AUREOLE_FROM_OTHERS arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onUpdateBuff(CLIENT_BUFF_VAL arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onUpdateBuffs(CLIENT_BUFFS arg1) {} //Avatar Monster Summon Npc Creation 
		public virtual void onUseCasting(Int32 arg1, UInt32 arg2, Int32 arg3, List<float> arg4, List<Int32> arg5) {} //Avatar Monster Summon Npc Creation 
		public virtual void onUseChanneling(Int32 arg1, UInt32 arg2, Int32 arg3, List<float> arg4, List<Int32> arg5, Int32 arg6) {} //Avatar Monster Summon Npc Creation 
		public virtual void onUseSkill(Byte arg1, UInt32 arg2, Int32 arg3, List<float> arg4, List<Int32> arg5) {} //Avatar Monster Summon Npc Creation 
		public virtual void popDialog(Int32 arg1) {} //Avatar Monster Summon Npc Collection 
		public virtual void popDialogWithSelfHead(Int32 arg1) {} //Avatar Monster Summon Npc Collection 
		public virtual void showPopoverMsg(UInt32 arg1) {} //Avatar Monster Summon Npc Collection 
		public virtual void showPopoverMsgWithArg(UInt32 arg1, List<string> arg2) {} //Avatar Monster Summon Npc Collection 
		public virtual void skillTeleportBefore(UInt32 arg1) {} //Avatar Monster Summon Npc Creation 


		public virtual void onPVPDmgChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onPVPDmgAntiChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjAntiFatalChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjAntiMortalChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjBloodSuckChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjCDChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjDebilityAntiChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjDebilityEnhChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjDmgArmorChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjDodgeChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjFatalChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjFullHpChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjFullHpAbsChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjFullMpChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjFullMpAbsChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjHitChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjHpChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjIgnoreArmorChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjKnockAntiChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjKnockEnhChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjMortalChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjSilentAntiChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjSilentEnhChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjStunAntiChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAdjStunEnhChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAntiFatalChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAntiMortalChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onAtkBlessChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onBaseDmgArmorChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onBaseIgnoreArmorChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onBePushedSpeedChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onBloodSuckChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onBornStateChanged(Byte oldValue) {}	//Monster Summon Npc Collection 
		public virtual void onDebilityAntiChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onDebilityEnhChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onDmgArmorChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onDodgeChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onDunTimeFreezeFlagChanged(Byte oldValue) {}	//MonsterGrp Monster Summon Barrier Teleporter CityBattleTeleporter CoreAreaFlag Npc Collection Creation RebornPos 
		public virtual void onExtraDmgChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onExtraDmgDefChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onFatalChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onFinalDmgChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onFinalDmgAntiChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onForceChanged(Int32 oldValue) {}	//Space CubeSpaceMgr WonderLandSpaceMgr WorldLineSpaceMgr SiegeWarSpaceMgr DungeonSpaceMgr MonsterGrp Avatar Monster Summon Barrier Teleporter CityBattleTeleporter CoreAreaFlag Npc Collection Creation DuelFlag RebornPos 
		public virtual void onFrozenAntiChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onFrozenEnhChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onFullHpChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onFullMpChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onGameEntityIdChanged(Int64 oldValue) {}	//MonsterGrp Monster Summon Barrier Teleporter CityBattleTeleporter CoreAreaFlag Npc Collection Creation RebornPos 
		public virtual void onHitChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onHitRateChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onHostIdChanged(Int32 oldValue) {}	//Summon Creation 
		public virtual void onHpChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onIgnoreArmorChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onIsBossChanged(Byte oldValue) {}	//Monster Summon Npc 
		public virtual void onIsWitnessCompleteChanged(Byte oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onKnockAntiChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onKnockEnhChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onLevelChanged(UInt32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMagicArmorChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMaxMagicAtkChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMaxPhysicalAtkChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMinMagicAtkChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMinPhysicalAtkChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMonsterDmgChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMonsterDmgAntiChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMortalChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMoveAniChanged(Byte oldValue) {}	//Monster Summon Npc 
		public virtual void onMpCostRatioChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMulBloodSuckChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMulBossDmgChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMulCDChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMulFullHpChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMulFullMpChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onMulHpChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onNameChanged(string oldValue) {}	//Avatar Monster Summon Teleporter Npc Collection Creation 
		public virtual void onPhysicalArmorChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onRealDmgChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onRealDmgDefChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onRouteStateChanged(UInt32 oldValue) {}	//Avatar Monster Npc 
		public virtual void onSelectedTargetIdChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onServerIdChanged(UInt16 oldValue) {}	//Account Avatar 
		public virtual void onSiegeWarCampChanged(Int32 oldValue) {}	//Avatar Monster Summon 
		public virtual void onSilentAntiChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onSilentEnhChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onSkillCDChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onSlowAntiChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onSlowEnhChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onSpaceNoChanged(UInt32 oldValue) {}	//Space CubeSpaceMgr WonderLandSpaceMgr WorldLineSpaceMgr SiegeWarSpaceMgr DungeonSpaceMgr MonsterGrp Avatar Monster Summon Barrier Teleporter CityBattleTeleporter CoreAreaFlag Npc Collection Creation DuelFlag RebornPos 
		public virtual void onSpeedChanged(float oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onSpiritChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onStateChanged(Int64 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onState2Changed(Int64 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onStunAntiChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onStunEnhChanged(Int32 oldValue) {}	//Avatar Monster Summon Npc Creation 
		public virtual void onTeleporterIdChanged(Int32 oldValue) {}	//Teleporter CityBattleTeleporter 
	}
}
